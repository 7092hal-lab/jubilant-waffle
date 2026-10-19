#!/usr/bin/env python3
"""List v1.0 sentences that do not appear verbatim in a draft (E4 audit aid).
Usage: sentmap.py <v1.0> <draft>"""
import re, sys
a = open(sys.argv[1], encoding="utf-8").read()
b = open(sys.argv[2], encoding="utf-8").read()
def sents(t):
    out = []
    for ln in t.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        for s in re.split(r"(?<=[.?!])\s+(?=[^)\]'’])", ln):
            s = s.strip()
            if s:
                out.append(s)
    return out
A = sents(a)
missing = [s for s in A if s not in b]
print(f"v1.0 sentences: {len(A)}; verbatim in draft: {len(A)-len(missing)}; not verbatim: {len(missing)}")
for s in missing:
    print("-", s[:160])
