#!/usr/bin/env python3
"""Show which answer files exist for round 1 (by guide letter and unit)."""
import json, pathlib

R1 = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme/tests/r1")
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))
done = missing = 0
rows = []
for cid, c in sorted(runs["conversations"].items(), key=lambda kv: (kv[1]["guide"], kv[1]["unit"])):
    have = [n for n in range(1, c["turns"] + 1) if (R1 / f"out/{cid}_t{n}.md").exists()]
    ok = len(have) == c["turns"]
    done += ok
    missing += not ok
    if not ok:
        rows.append(f"{c['guide']} {c['unit']:5} {cid} turns {len(have)}/{c['turns']}")
print(f"complete {done} / {done + missing}")
print("\n".join(rows))
