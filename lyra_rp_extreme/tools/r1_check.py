#!/usr/bin/env python3
"""Automated candidate checks on round 1 answers (per guide letter): speech level, copying from the
guide, persona words, first-sentence repetition, question endings, '셈이에요' closings, stars/brackets,
length. Writes tests/r1/checks.md. Candidates only; the main agent confirms."""
import collections, json, pathlib, re

R1 = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme/tests/r1")
SCR = pathlib.Path("/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-d4b9-55dc-a2ac-f7730429859c/scratchpad")
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))
PERSONA = ["균열", "광채", "산미", "외유내강", "단아", "위트", "말장난", "시인", "비평가", "아이 같은", "책더미", "파묻혀",
           "설정집", "비밀", "몸이 없", "안경", "옛글", "고전학", "주의를 기울이", "한 번뿐인", "일기장"]
END_CHARS = '.?!…~)"\'”’」』*_ ·:'
SCENE_UNITS = {"V12", "X09", "X13"}


def nospace(s):
    return re.sub(r"\s+", "", s)


def clean_end(s):
    s = re.sub(r"[\U0001F300-\U0001FAFF☀-➿]", "", s)
    return s.rstrip(END_CHARS)


def sentences(text):
    lines, incode = [], False
    for raw in text.split("\n"):
        st = raw.strip()
        if st.startswith("```"):
            incode = not incode
            continue
        if incode or not st or st.startswith((">", "|", "#")):
            continue
        lines.append(st)
    out = []
    for ln in lines:
        ln = re.sub(r"^([-*•]|\d+[.)])\s+", "", ln)
        out.extend(p for p in re.split(r"(?<=[.?!…])\s+", ln) if p.strip())
    return out


def level_flag(sent):
    s = clean_end(sent)
    if len(s) < 4 or not ("가" <= s[-1] <= "힣"):
        return None
    if s.endswith("니다"):
        return "합쇼체"
    if s.endswith(("요", "죠")):
        return None
    if re.search(r"(다|라|자|냐)$", s):
        return "하다체 후보"
    if re.search(r"(함|임|됨|음|필요|하기|것)$", s):
        return "명사형 후보"
    return "해체·조각 후보"


def copied(ans, guide, minlen=12):
    a, g = nospace(ans), nospace(guide)
    spans, i = [], 0
    while i <= len(a) - minlen:
        if a[i:i + minlen] in g:
            j = i + minlen
            while j < len(a) and a[i:j + 1] in g:
                j += 1
            spans.append(a[i:j])
            i = j
        else:
            i += 1
    return spans


guides = {L: (SCR / f"r1/guide_{L}.md").read_text(encoding="utf-8") for L in ("P", "Q")}
rows = collections.defaultdict(list)
for cid, c in runs["conversations"].items():
    L, uid = c["guide"], c["unit"]
    for n in range(1, c["turns"] + 1):
        p = R1 / f"out/{cid}_t{n}.md"
        if not p.exists():
            continue
        ans = p.read_text(encoding="utf-8")
        user_msgs = " ".join(units[uid]["turns"])
        sents = sentences(ans)
        # scene narration lines (no quotes) are exempt from speech level in scene units
        level = []
        for s in sents:
            if uid in SCENE_UNITS and not re.search(r"[\"“”]", s):
                continue
            f = level_flag(s)
            if f:
                level.append((f, s))
        rows[L].append({
            "unit": uid, "t": n, "chars": len(ans), "level": level,
            "copy": [x for x in copied(ans, guides[L]) if x not in nospace(user_msgs)],
            "persona": {w: ans.count(w) for w in PERSONA if w in ans and w not in user_msgs},
            "first": sents[0] if sents else "", "last": sents[-1] if sents else "",
            "q_end": bool(sents) and sents[-1].rstrip().endswith("?"),
            "semyeon": len(re.findall(r"셈이에요|셈이죠|셈이네요", ans)),
            "stars": bool(re.search(r"\*[^*\n]+\*", ans)) or bool(re.search(r"^\s*\(.+\)\s*$", ans, re.M)),
        })

rep = ["# Round 1 automated checks (candidates)\n"]
for L in ("P", "Q"):
    R = rows[L]
    rep.append(f"\n## Guide {L}: {len(R)} answers\n")
    rep.append(f"- total chars {sum(r['chars'] for r in R)}, mean {sum(r['chars'] for r in R)//max(1,len(R))}")
    rep.append(f"- question endings {sum(r['q_end'] for r in R)}/{len(R)}")
    rep.append(f"- '셈이에요' closings {sum(r['semyeon'] for r in R)}")
    rep.append(f"- star/bracket narration candidates: {[ (r['unit'], r['t']) for r in R if r['stars']]}")
    rep.append("- V01 first sentences: " + " | ".join(r["first"] for r in R if r["unit"].startswith("V01")))
    rep.append("\n### speech level candidates")
    for r in R:
        for f, s in r["level"]:
            rep.append(f"- {r['unit']} T{r['t']} [{f}] {s}")
    rep.append("\n### copy from own guide (>=12 chars, no spaces)")
    for r in R:
        if r["copy"]:
            rep.append(f"- {r['unit']} T{r['t']}: " + " | ".join(r["copy"]))
    rep.append("\n### persona words")
    for r in R:
        if r["persona"]:
            rep.append(f"- {r['unit']} T{r['t']}: {r['persona']}")
    rep.append("\n### per answer length")
    rep.append(", ".join(f"{r['unit']}T{r['t']}:{r['chars']}" for r in sorted(R, key=lambda r: (r['unit'], r['t']))))
(R1 / "checks.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print("\n".join(rep[:40]))
