#!/usr/bin/env python3
"""Build blind judge packets for round 1.
Each packet holds up to 6 units; X/Y is random per unit. Judge A reads packet_<k>A.md, judge B reads
packet_<k>B.md (same units, X and Y swapped). The key is written to tests/r1/mapping.json."""
import json, pathlib, random, re

R1 = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme/tests/r1")
PK = R1 / "packets"
PK.mkdir(exist_ok=True)
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))

conv = {}
for cid, c in runs["conversations"].items():
    conv[(c["guide"], c["unit"])] = cid

SPEC_FIX = {
    "V12": [("지문이 짧고 담백함", "지문은 장면에 필요한 만큼(한 답에 대개 서너 줄 안쪽)이고 구체적임")],
}
DROP = re.compile(r"^- (확정|단위):.*$|\s*\(Viola를 지침으로 쓴 응답에서는 이름이 Viola\)|\s*\(V03의 답에 칭찬이 없으면.*\)", re.M)


def clean_spec(uid):
    s = units[uid]["spec"]
    s = DROP.sub("", s)
    s = re.sub(r"^### ", "", s, flags=re.M)
    for a, b in SPEC_FIX.get(uid, []):
        s = s.replace(a, b)
    s = re.sub(r"```\n.*?\n```", "(사용자의 글은 아래 대화에 그대로 있음)", s, flags=re.S)
    return s.strip()


def transcript(L, uid):
    cid = conv[(L, uid)]
    out = []
    for n, um in enumerate(units[uid]["turns"], 1):
        ans = (R1 / f"out/{cid}_t{n}.md").read_text(encoding="utf-8").strip()
        out.append(f"[T{n}] SJ:\n{um}\n\n[T{n}] 응답:\n{ans}")
    return "\n\n".join(out)


order = list(units)
random.shuffle(order)
packets = [order[i:i + 6] for i in range(0, len(order), 6)]
mapping = {}
for k, plist in enumerate(packets, 1):
    blocks = {"A": [], "B": []}
    mapping[str(k)] = {}
    for j, uid in enumerate(plist, 1):
        X, Y = random.sample(["P", "Q"], 2)
        mapping[str(k)][f"u{j}"] = {"unit": uid, "A": {"X": X, "Y": Y}, "B": {"X": Y, "Y": X}}
        key = units[uid]["key"].strip()
        for side, (xl, yl) in (("A", (X, Y)), ("B", (Y, X))):
            nt = len(units[uid]["turns"])
            head = f"## u{j}\n\n### 문항 정보\n{clean_spec(uid)}\n"
            if key:
                head += f"\n### 정답 키\n{key}\n"
            head += f"\n### 채점할 턴\n{', '.join(f'T{n}' for n in range(1, nt + 1))}\n"
            body = f"\n### X의 대화\n{transcript(xl, uid)}\n\n### Y의 대화\n{transcript(yl, uid)}\n"
            blocks[side].append(head + body)
    for side in "AB":
        (PK / f"packet_{k}{side}.md").write_text(
            f"# 심사 묶음 {k}{side}\n\n단위 {len(plist)}개. 단위마다 따로 판단한다.\n\n" + "\n\n".join(blocks[side]) + "\n",
            encoding="utf-8")
(R1 / "mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
print("packets", len(packets), [len(p) for p in packets])
