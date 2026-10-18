#!/usr/bin/env python3
"""Plan round 2: d2 answers for selected units (comparator = v1.0 answers from round 1).
Usage: r2_plan.py <unit,unit,...>   writes tests/r2/{runs.json,units.json} and actor task files."""
import json, pathlib, secrets, shutil, sys

REPO = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme")
SCR = pathlib.Path("/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-d4b9-55dc-a2ac-f7730429859c/scratchpad")
R1, R2 = REPO / "tests/r1", REPO / "tests/r2"
(R2 / "out").mkdir(parents=True, exist_ok=True)
T = SCR / "r2/tasks"
T.mkdir(parents=True, exist_ok=True)
units_all = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
sel = sys.argv[1].split(",")
units = {u: units_all[u] for u in sel}
(R2 / "units.json").write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
shutil.copyfile(REPO / "drafts/d2.md", SCR / "r2/guide_R.md")

HEAD = (SCR / "r1/tasks/batch_P1.md").read_text(encoding="utf-8").split("\n<conversation")[0]
HEAD = HEAD.replace(str(SCR / "r1/guide_P.md"), str(SCR / "r2/guide_R.md"))
BATCH_RULE = "아래 대화들은 서로 관계없는 새 대화다. 대화마다 다른 대화를 모르는 상태로 답 하나를 쓴다."
MULTI_RULE = "아래 대화는 새 대화다. 답 하나를 쓴다. 이 대화는 이어질 수 있고, 같은 대화의 다음 메시지가 오면 앞의 대화를 기억한 채 같은 방식으로 답한다."
assert BATCH_RULE in HEAD

runs = {"version_of": {"R": "d2"}, "comparator": "r1 guide P (v1.0)", "conversations": {}, "actor_batches": [], "actor_multi": []}
single = [u for u in sel if len(units[u]["turns"]) == 1]
multi = [u for u in sel if len(units[u]["turns"]) > 1]


def block(cid, u):
    search = "검색 없음" if units[u].get("nosearch") else "검색 허용"
    return f'<conversation id="{cid}" search="{search}" save_to="{R2 / f"out/{cid}_t1.md"}">\n<user>{units[u]["turns"][0]}</user>\n</conversation>'


idx = []
for i in range(0, len(single), 4):
    b = single[i:i + 4]
    convs = []
    for u in b:
        cid = secrets.token_hex(4)
        runs["conversations"][cid] = {"unit": u, "guide": "R", "turns": 1}
        convs.append((cid, u))
    runs["actor_batches"].append({"guide": "R", "convs": [c for c, _ in convs]})
    p = T / f"batch_R{i // 4 + 1}.md"
    p.write_text(HEAD + "\n" + "\n\n".join(block(c, u) for c, u in convs) + "\n", encoding="utf-8")
    idx.append(str(p))
for u in multi:
    cid = secrets.token_hex(4)
    runs["conversations"][cid] = {"unit": u, "guide": "R", "turns": len(units[u]["turns"])}
    runs["actor_multi"].append({"guide": "R", "conv": cid})
    p = T / f"multi_R_{u}.md"
    p.write_text(HEAD.replace(BATCH_RULE, MULTI_RULE) + "\n" + block(cid, u) + "\n", encoding="utf-8")
    idx.append(str(p))
(R2 / "runs.json").write_text(json.dumps(runs, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(idx))
