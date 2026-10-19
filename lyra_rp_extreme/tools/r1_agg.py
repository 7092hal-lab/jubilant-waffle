#!/usr/bin/env python3
"""Aggregate round 1 judge results (unblinded with mapping.json and runs.json).
Writes tests/r1/agg.json and tests/r1/agg.md only if every result is complete.
Use --r1-dir to aggregate an isolated copy of a round."""
import argparse, collections, json, pathlib, statistics

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--r1-dir", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parents[1] / "tests/r1")
R1 = parser.parse_args().r1_dir
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))
mapping = json.loads((R1 / "mapping.json").read_text(encoding="utf-8"))
ver = runs["version_of"]  # letter -> version
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))

per_unit = collections.defaultdict(lambda: {"votes": collections.defaultdict(list), "scores": collections.defaultdict(lambda: collections.defaultdict(list)),
                                             "hard": collections.defaultdict(list), "overuse": collections.defaultdict(list),
                                             "markers": collections.defaultdict(list), "facts_wrong": collections.defaultdict(list), "reasons": []})
missing = []
for k, packet in mapping.items():
    for side in "AB":
        p = R1 / f"results/{k}{side}.json"
        if not p.exists():
            missing.append(f"{k}{side}")
            continue
        try:
            res = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            missing.append(f"{k}{side} (bad json: {e})")
            continue
        if not isinstance(res, list) or any(
                not isinstance(r, dict) or not isinstance(r.get("unit"), str) for r in res):
            missing.append(f"{k}{side} (expected an array of objects with string unit IDs)")
            continue
        counts = collections.Counter(r["unit"] for r in res)
        absent = sorted(set(packet) - counts.keys())
        unexpected = sorted(counts.keys() - set(packet))
        duplicates = sorted(u for u, count in counts.items() if count > 1)
        if absent or unexpected or duplicates:
            missing.append(f"{k}{side} (missing IDs: {absent}; duplicate IDs: {duplicates}; "
                           f"unexpected IDs: {unexpected})")
            continue
        for r in res:
            u = r["unit"]
            uid = packet[u]["unit"]
            xy = packet[u][side]  # {"X": letter, "Y": letter}
            V = {"X": ver[xy["X"]], "Y": ver[xy["Y"]]}
            rec = per_unit[uid]
            pref = r.get("preference", {})
            for dim in ("voice", "persona", "accuracy_task"):
                v = pref.get(dim, "동률")
                rec["votes"][dim].append(V.get(v, "tie") if v in ("X", "Y") else "tie")
            for s in ("X", "Y"):
                for crit, val in (r.get("scores", {}).get(s, {}) or {}).items():
                    if isinstance(val, (int, float)):
                        rec["scores"][V[s]][crit].append(val)
                rec["hard"][V[s]] += r.get("hard_fails", {}).get(s, []) or []
                rec["overuse"][V[s]] += r.get("overuse", {}).get(s, []) or []
                rec["markers"][V[s]] += r.get("markers", {}).get(s, []) or []
                for fc in r.get("fact_claims", {}).get(s, []) or []:
                    if isinstance(fc, dict) and fc.get("status") == "틀림":
                        rec["facts_wrong"][V[s]].append(fc.get("claim", ""))
            rec["reasons"].append(f"[{side}] conf {pref.get('confidence','')}: {r.get('reason','')}")

if missing:
    raise SystemExit("Refusing to aggregate incomplete or invalid judge results:\n" + "\n".join(missing))

def outcome(votes):
    c = collections.Counter(votes)
    if c["d1"] > c["v1.0"]:
        return "d1"
    if c["v1.0"] > c["d1"]:
        return "v1.0"
    return "tie"

summary = {"missing": missing, "units": {}}
tot = {d: collections.Counter() for d in ("voice", "persona", "accuracy_task")}
means = {v: collections.defaultdict(list) for v in ("d1", "v1.0")}
for uid, rec in sorted(per_unit.items()):
    o = {d: outcome(rec["votes"][d]) for d in ("voice", "persona", "accuracy_task")}
    for d in o:
        tot[d][o[d]] += 1
    for v in ("d1", "v1.0"):
        for crit, vals in rec["scores"][v].items():
            means[v][crit].append(statistics.mean(vals))
    summary["units"][uid] = {"outcome": o, "votes": {d: rec["votes"][d] for d in rec["votes"]},
                             "mean_scores": {v: {c: round(statistics.mean(x), 2) for c, x in rec["scores"][v].items()} for v in rec["scores"]},
                             "hard": dict(rec["hard"]), "overuse": dict(rec["overuse"]), "markers": dict(rec["markers"]),
                             "facts_wrong": dict(rec["facts_wrong"]), "reasons": rec["reasons"]}
summary["totals"] = {d: dict(tot[d]) for d in tot}
summary["mean_by_criterion"] = {v: {c: round(statistics.mean(x), 2) for c, x in means[v].items()} for v in means}
(R1 / "agg.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")

lines = ["# Round 1 aggregate (d1 vs v1.0)\n", f"missing results: {missing}\n", "## Unit outcomes (d1 / tie / v1.0)\n"]
for d in ("voice", "persona", "accuracy_task"):
    t = tot[d]
    lines.append(f"- {d}: d1 {t['d1']} / tie {t['tie']} / v1.0 {t['v1.0']}")
lines.append("\n## Mean scores per criterion (unit means averaged)\n")
for v in ("d1", "v1.0"):
    lines.append(f"- {v}: " + ", ".join(f"{c} {x}" for c, x in sorted(summary['mean_by_criterion'][v].items())))
lines.append("\n## Per unit\n")
lines.append("| unit | voice | persona | acc/task | d1 hard | v1.0 hard | d1 overuse | d1 J-scores | v1.0 J-scores |")
lines.append("|---|---|---|---|---|---|---|---|---|")
for uid, s in sorted(summary["units"].items()):
    o = s["outcome"]
    ms = s["mean_scores"]
    lines.append(f"| {uid} | {o['voice']} | {o['persona']} | {o['accuracy_task']} | {len(s['hard'].get('d1', []))} | {len(s['hard'].get('v1.0', []))} | {len(s['overuse'].get('d1', []))} | "
                 + " ".join(f"{c}{x}" for c, x in sorted(ms.get('d1', {}).items())) + " | " + " ".join(f"{c}{x}" for c, x in sorted(ms.get('v1.0', {}).items())) + " |")
lines.append("\n## Hard fails, overuse, wrong facts (by version)\n")
for uid, s in sorted(summary["units"].items()):
    for v in ("d1", "v1.0"):
        for h in s["hard"].get(v, []):
            lines.append(f"- {uid} {v} HARD: {h}")
        for h in s["overuse"].get(v, []):
            lines.append(f"- {uid} {v} overuse: {h}")
        for h in s["facts_wrong"].get(v, []):
            lines.append(f"- {uid} {v} wrong fact: {h}")
(R1 / "agg.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:12]))
