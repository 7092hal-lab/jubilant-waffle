#!/usr/bin/env python3
"""Print the SendMessage text for the next turn of a multi-turn conversation.
Usage: r1_next.py <guide letter> <unit>   (finds the conversation, the next missing turn)"""
import json, pathlib, sys

REPO = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme")
R1 = REPO / "tests/r1"
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))
L, unit = sys.argv[1], sys.argv[2]
cid = next(c for c, v in runs["conversations"].items() if v["guide"] == L and v["unit"] == unit)
n = 1
while (R1 / f"out/{cid}_t{n}.md").exists():
    n += 1
turns = units[unit]["turns"]
if n > len(turns):
    print(f"DONE {cid}")
    sys.exit(0)
path = R1 / f"out/{cid}_t{n}.md"
print(f"같은 대화에서 대화 상대가 보낸 다음 메시지다. 앞의 지시대로 답을 {path} 에 저장하고 \"저장:\"과 경로만 보고하라.\n<user>{turns[n-1]}</user>")
