"""Run with: python -m unittest discover -s lyra_rp_extreme/tests -p 'test_*.py' -v.

Every script invocation uses a temporary fixture; committed experiment data is never written.
"""
import copy
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parents[1] / "tools"
DIMENSIONS = ("voice", "persona", "accuracy_task")
BATCH_RULE = "아래 대화들은 서로 관계없는 새 대화다. 대화마다 다른 대화를 모르는 상태로 답 하나를 쓴다."


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def run_tool(name, *args):
    return subprocess.run(
        [sys.executable, str(TOOLS / name), *map(str, args)],
        capture_output=True, encoding="utf-8", timeout=20,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )


class AggregateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.r1 = Path(self.temp.name) / "r1"
        self.mapping = {
            "1": {u: {"unit": uid, "A": {"X": "Q", "Y": "P"},
                      "B": {"X": "P", "Y": "Q"}}
                  for u, uid in (("u1", "A01"), ("u2", "A02"))},
            # Unit IDs are local to each packet; reusing u1 here is valid.
            "2": {"u1": {"unit": "A03", "A": {"X": "Q", "Y": "P"},
                          "B": {"X": "P", "Y": "Q"}}},
        }
        write_json(self.r1 / "mapping.json", self.mapping)
        write_json(self.r1 / "runs.json", {"version_of": {"P": "v1.0", "Q": "d1"}})
        write_json(self.r1 / "units.json", {u: {} for u in ("A01", "A02", "A03")})
        self.results = {}
        for packet, units in self.mapping.items():
            for side in "AB":
                preferred = "X" if side == "A" else "Y"
                rows = [{"unit": u, "preference": {d: preferred for d in DIMENSIONS},
                         "scores": {s: {"J1": 4 if s == preferred else 2} for s in "XY"}}
                        for u in units]
                self.results[packet + side] = rows
                write_json(self.r1 / "results" / f"{packet}{side}.json", rows)
        self.previous = {"agg.json": b'{"previous": true}\n', "agg.md": b"Previous aggregate\n"}
        for name, content in self.previous.items():
            (self.r1 / name).write_bytes(content)

    def aggregate(self):
        return run_tool("r1_agg.py", "--r1-dir", self.r1)

    def assert_rejected(self, *diagnostics):
        result = self.aggregate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        for diagnostic in diagnostics:
            self.assertIn(diagnostic, result.stderr)
        for name, content in self.previous.items():
            self.assertEqual((self.r1 / name).read_bytes(), content)

    def test_complete_results_aggregate_all_units_with_two_votes(self):
        result = self.aggregate()
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads((self.r1 / "agg.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["missing"], [])
        self.assertEqual(set(summary["units"]), {"A01", "A02", "A03"})
        for dim in DIMENSIONS:
            self.assertEqual(summary["totals"][dim], {"d1": 3})
        for unit in summary["units"].values():
            for dim in DIMENSIONS:
                self.assertEqual(unit["votes"][dim], ["d1", "d1"])
            self.assertEqual(unit["mean_scores"], {"d1": {"J1": 4}, "v1.0": {"J1": 2}})

    def test_result_order_does_not_matter(self):
        write_json(self.r1 / "results/1B.json", list(reversed(self.results["1B"])))
        result = self.aggregate()
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads((self.r1 / "agg.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["totals"]["voice"], {"d1": 3})

    def test_checkpointed_partial_results_rejected_on_either_side(self):
        for side in "AB":
            with self.subTest(side=side):
                target = self.r1 / f"results/1{side}.json"
                write_json(target, self.results["1" + side][:1])
                self.assert_rejected("1" + side, "missing IDs: ['u2']")
                write_json(target, self.results["1" + side])

    def test_empty_checkpoint_rejected(self):
        write_json(self.r1 / "results/1A.json", [])
        self.assert_rejected("1A", "missing IDs: ['u1', 'u2']")

    def test_duplicate_rejected_even_when_no_unit_is_missing(self):
        write_json(self.r1 / "results/1B.json", self.results["1B"] + self.results["1B"][:1])
        self.assert_rejected("1B", "missing IDs: []", "duplicate IDs: ['u1']")

    def test_duplicate_cannot_replace_missing_unit(self):
        write_json(self.r1 / "results/1A.json", self.results["1A"][:1] * 2)
        self.assert_rejected("missing IDs: ['u2']", "duplicate IDs: ['u1']")

    def test_unexpected_id_rejected_even_when_all_expected_units_exist(self):
        extra = {**self.results["1A"][0], "unit": "u99"}
        write_json(self.r1 / "results/1A.json", self.results["1A"] + [extra])
        self.assert_rejected("missing IDs: []", "unexpected IDs: ['u99']")

    def test_unknown_id_cannot_replace_expected_id_at_same_count(self):
        rows = copy.deepcopy(self.results["1A"])
        rows[1]["unit"] = "u99"
        write_json(self.r1 / "results/1A.json", rows)
        self.assert_rejected("missing IDs: ['u2']", "unexpected IDs: ['u99']")

    def test_missing_result_file_rejected(self):
        (self.r1 / "results/2B.json").unlink()
        self.assert_rejected("2B")

    def test_invalid_json_rejected(self):
        (self.r1 / "results/2A.json").write_text('[{"unit":', encoding="utf-8")
        self.assert_rejected("2A", "bad json")

    def test_invalid_result_shape_and_unit_types_rejected(self):
        for value in ({}, None, [None], [{}], [{"unit": None}], [{"unit": 1}], [{"unit": []}]):
            with self.subTest(value=value):
                write_json(self.r1 / "results/1A.json", value)
                self.assert_rejected("1A", "array of objects with string unit IDs")

    def test_invalid_round_creates_no_aggregate_when_none_exists(self):
        for name in self.previous:
            (self.r1 / name).unlink()
        write_json(self.r1 / "results/1A.json", self.results["1A"][:1])
        result = self.aggregate()
        self.assertNotEqual(result.returncode, 0)
        for name in self.previous:
            self.assertFalse((self.r1 / name).exists())


class RoundTwoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "project"
        self.scratch = Path(self.temp.name) / "scratch"
        self.r1 = self.repo / "tests/r1"
        self.r2 = self.repo / "tests/r2"
        write_json(self.r1 / "units.json", {
            "U1": {"turns": ["single"], "nosearch": True},
            "U2": {"turns": ["first", "second"]},
        })
        (self.repo / "drafts").mkdir()
        (self.repo / "drafts/d2.md").write_text("fixture d2 guide\n", encoding="utf-8")
        (self.scratch / "r1/tasks").mkdir(parents=True)

    def plan(self):
        return run_tool("r2_plan.py", "U1,U2", "--repo", self.repo, "--scratch", self.scratch)

    def assert_comparator(self, version_of, letter):
        write_json(self.r1 / "runs.json", {"version_of": version_of})
        # Only the actual baseline's template exists; a hard-coded P read fails for Q.
        template = self.scratch / f"r1/tasks/batch_{letter}1.md"
        template.write_text(f"Guide: {self.scratch / f'r1/guide_{letter}.md'}\n{BATCH_RULE}\n"
                            "<conversation id=\"old\">old</conversation>\n", encoding="utf-8")
        before = {p: p.read_bytes() for p in self.r1.rglob("*") if p.is_file()}
        result = self.plan()
        self.assertEqual(result.returncode, 0, result.stderr)
        runs = json.loads((self.r2 / "runs.json").read_text(encoding="utf-8"))
        self.assertEqual(runs["comparator"], f"r1 guide {letter} (v1.0)")
        self.assertEqual(runs["version_of"], {"R": "d2"})
        self.assertEqual({c["unit"] for c in runs["conversations"].values()}, {"U1", "U2"})
        self.assertEqual(len(runs["actor_batches"]), 1)
        self.assertEqual(len(runs["actor_multi"]), 1)
        tasks = list((self.scratch / "r2/tasks").glob("*.md"))
        self.assertEqual(len(tasks), 2)
        for task in tasks:
            text = task.read_text(encoding="utf-8")
            self.assertIn(str(self.scratch / "r2/guide_R.md"), text)
            self.assertNotIn(f"guide_{letter}.md", text)
            self.assertNotIn('id="old"', text)
        self.assertEqual((self.scratch / "r2/guide_R.md").read_bytes(),
                         (self.repo / "drafts/d2.md").read_bytes())
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_current_assignment_uses_p(self):
        self.assert_comparator({"Q": "d1", "P": "v1.0"}, "P")

    def test_reversed_assignment_uses_q(self):
        self.assert_comparator({"P": "d1", "Q": "v1.0"}, "Q")

    def test_invalid_baseline_assignment_fails_before_writing(self):
        for version_of in ({"P": "d1", "Q": "d2"}, {"P": "v1.0", "Q": "v1.0"}):
            with self.subTest(version_of=version_of):
                write_json(self.r1 / "runs.json", {"version_of": version_of})
                result = self.plan()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("exactly one guide letter", result.stderr)
                self.assertFalse(self.r2.exists())
                self.assertFalse((self.scratch / "r2").exists())


class StoredRoundOneTests(unittest.TestCase):
    r1 = Path(__file__).resolve().parent / "r1"

    def test_raw_results_match_packet_headers_mapping_and_unit_inventory(self):
        mapping = json.loads((self.r1 / "mapping.json").read_text(encoding="utf-8"))
        units = json.loads((self.r1 / "units.json").read_text(encoding="utf-8"))
        mapped = Counter(record["unit"] for packet in mapping.values() for record in packet.values())
        self.assertEqual(mapped, Counter(list(units)))
        for key, packet in mapping.items():
            for side in "AB":
                with self.subTest(packet=key + side):
                    text = (self.r1 / f"packets/packet_{key}{side}.md").read_text(encoding="utf-8")
                    packet_ids = re.findall(r"^## (u\d+)\s*$", text, re.MULTILINE)
                    results = json.loads((self.r1 / f"results/{key}{side}.json").read_text(encoding="utf-8"))
                    self.assertEqual(Counter(packet_ids), Counter(list(packet)))
                    self.assertEqual(Counter(r["unit"] for r in results), Counter(packet_ids))

    def test_historical_aggregate_reproduced_without_changing_source_data(self):
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.r1.rglob("*") if p.is_file()}
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "r1"
            shutil.copytree(self.r1, copied)
            result = run_tool("r1_agg.py", "--r1-dir", copied)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads((copied / "agg.json").read_text(encoding="utf-8"))
            self.assertEqual(summary, json.loads((self.r1 / "agg.json").read_text(encoding="utf-8")))
            self.assertEqual((copied / "agg.md").read_text(encoding="utf-8"),
                             (self.r1 / "agg.md").read_text(encoding="utf-8"))
            for unit in summary["units"].values():
                for dim in DIMENSIONS:
                    self.assertEqual(len(unit["votes"][dim]), 2)
        after = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.r1.rglob("*") if p.is_file()}
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
