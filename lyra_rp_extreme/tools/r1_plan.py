#!/usr/bin/env python3
"""Plan round 1: units, conversations, actor batches, neutral guide copies.
Writes <repo>/lyra_rp_extreme/tests/r1/{units.json,runs.json} and <scratch>/r1/guide_{P,Q}.md.
Version letters P/Q are assigned at random; runs.json holds the key (judges never read it)."""
import json, pathlib, random, re, secrets, shutil

REPO = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme")
LRP = pathlib.Path("/home/user/lyra-rp/lyra_rp/suite")
SCR = pathlib.Path("/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-d4b9-55dc-a2ac-f7730429859c/scratchpad")
R1 = REPO / "tests/r1"
(R1 / "out").mkdir(parents=True, exist_ok=True)
(SCR / "r1").mkdir(parents=True, exist_ok=True)


def sections(path, level="###"):
    text = path.read_text(encoding="utf-8")
    out, cur, buf = {}, None, []
    pat = re.compile(r"^" + re.escape(level) + r" ([A-Z]\d\d[a-z]?)\b")
    for line in text.split("\n"):
        m = pat.match(line)
        if m:
            if cur:
                out[cur] = "\n".join(buf).rstrip()
            cur, buf = m.group(1), [line]
            continue
        if cur and re.match(r"^#{1,%d} " % len(level), line) and not pat.match(line):
            out[cur] = "\n".join(buf).rstrip()
            cur, buf = None, []
            continue
        if cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).rstrip()
    return out


STRIP = re.compile(r"\s*\((검색할 수 있는 조건|Viola를 지침으로 쓴 응답에서는 이름이 Viola|V03의 답에 칭찬이 없으면.*|앞 대화 기록 없음)\)\s*$")


def turns_of(body):
    t = {}
    for line in body.split("\n"):
        m = re.match(r"^- T(\d+): (.*)$", line)
        if m:
            t[int(m.group(1))] = STRIP.sub("", m.group(2)).strip()
    return t


def codeblock(body):
    m = re.search(r"```\n(.*?)\n```", body, re.S)
    return m.group(1)


old = sections(LRP / "items.md")
keys_old = sections(LRP / "keys.md", "##")
new = sections(REPO / "tests/round1_items.md")

units = {}
# reused v1.0 units
for uid in ["V02", "V05", "V06", "V07", "V10", "V14", "V16", "V19", "V22", "V24", "V25", "V26",
            "A04", "A05", "A10", "A13", "C01", "M01", "M02"]:
    body = old[uid]
    t = turns_of(body)
    if uid == "A13":
        t = {1: codeblock(body) + "\n\n이거 내가 쓴 영화 평론 문단인데, 구조랑 논리 꼼꼼하게 봐 줘. 소제목 달아서."}
    units[uid] = {"turns": [t[k] for k in sorted(t)], "spec": body, "key": keys_old.get(uid, "")}
units["A01n"] = {"turns": [turns_of(old["A01"])[1]], "spec": old["A01n"], "key": keys_old.get("A01n", ""), "nosearch": True}
v08, v09 = turns_of(old["V08"]), turns_of(old["V09"])
units["V08"] = {"turns": [v08[1], v09[2], v09[3], v09[4]], "spec": old["V08"] + "\n\n" + old["V09"], "key": keys_old.get("V08", "")}
v12, v13 = turns_of(old["V12"]), turns_of(old["V13"])
units["V12"] = {"turns": [v12[1], v13[2], v13[3]], "spec": old["V12"] + "\n\n" + old["V13"], "key": keys_old.get("V13", "")}
v01 = turns_of(old["V01"])[1]
for s in "abc":
    units["V01" + s] = {"turns": [v01], "spec": old["V01"], "key": ""}
# new units
for uid, body in new.items():
    t = turns_of(body)
    keym = re.search(r"^- Key: (.*)$", body, re.M)
    units[uid] = {"turns": [t[k] for k in sorted(t)], "spec": body, "key": keym.group(1) if keym else ""}
    if "no search" in body.split("\n")[0]:
        units[uid]["nosearch"] = True

batches = [["V01a", "X04", "A04", "V24"], ["V01b", "X05", "A05", "V25"], ["V01c", "X08", "A10", "V22"],
           ["V02", "X10", "A13", "V16"], ["V05", "X11", "X01", "V14"], ["V06", "X12", "X06", "V10"],
           ["V07", "X14", "X15", "V19"], ["A01n", "X02", "X03", "V26"]]
multi = ["V08", "M01", "M02", "V12", "C01", "X07", "X09", "X13"]
single = [u for b in batches for u in b]
assert sorted(single + multi) == sorted(units), set(units) ^ set(single + multi)
for u in single:
    assert len(units[u]["turns"]) == 1, u
for u in multi:
    assert len(units[u]["turns"]) >= 2, u

letters = ["P", "Q"]
random.shuffle(letters)
version_of = {letters[0]: "d1", letters[1]: "v1.0"}
src = {"d1": REPO / "drafts/d1.md", "v1.0": REPO / "base/lyra_rp_edition_v1.0.txt"}
for L, v in version_of.items():
    shutil.copyfile(src[v], SCR / f"r1/guide_{L}.md")

runs = {"version_of": version_of, "conversations": {}, "actor_batches": [], "actor_multi": []}
for L in sorted(version_of):
    for b in batches:
        convs = []
        for u in b:
            cid = secrets.token_hex(4)
            runs["conversations"][cid] = {"unit": u, "guide": L, "turns": len(units[u]["turns"])}
            convs.append(cid)
        runs["actor_batches"].append({"guide": L, "convs": convs})
    for u in multi:
        cid = secrets.token_hex(4)
        runs["conversations"][cid] = {"unit": u, "guide": L, "turns": len(units[u]["turns"])}
        runs["actor_multi"].append({"guide": L, "conv": cid})

(R1 / "units.json").write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
(R1 / "runs.json").write_text(json.dumps(runs, ensure_ascii=False, indent=1), encoding="utf-8")
print("units", len(units), "conversations", len(runs["conversations"]),
      "batch actors", len(runs["actor_batches"]), "multi actors", len(runs["actor_multi"]))
