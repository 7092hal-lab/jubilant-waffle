# PROGRESS — Lyra RP Extreme Ed.

Goal: write Lyra RP Extreme Ed. (Korean) from v1.0 — persona realism and natural speech pushed to the extreme (assistant 3 : persona 7), accuracy sacrificed as little as possible, full current spec.
Last updated: 2026-10-19 01:3x KST (session ca3fca9e) — PAUSED at SJ's request (weekly usage ~95%).

## Handoff memo (paste into a new conversation to resume)

- Goal and requirements: `lyra_rp_extreme/records/REQUEST.md` (SJ's request, spec and work principles verbatim; E1–E8; SJ's later decisions at the end).
- Records: GitHub 7092hal-lab/jubilant-waffle, branch `ccr-d898a464-34plpj`, folder `lyra_rp_extreme/`. Reference (read-only): 7092hal-lab/lyra-rp (v1.0 suite `lyra_rp/suite/items.md`, `keys.md`).
- Done: plan confirmed (S0); d1 written, previewed by SJ ("계속"); round 1 (S2) actors 80/80 conversations, judges complete for all 7 packets (14 judges, 40 units); main-agent fact check of d1; d2 built from round-1 findings (not yet tested).
- Next actions, in order:
  1. Round 1 is complete and aggregated (`tests/r1/agg.md`). Read it before round 2.
  2. Round 2 (S3): d2 vs the round-1 v1.0 answers. Proposed units: targets V19, A10, V01a, V01b, V01c, X12, A04, V16, X15, C01, V12, X06 (voice); guards X04, X07, X10, M01. `tools/r2_plan.py <comma-separated units>` writes `tests/r2/{units,runs}.json` and actor task files. Still to write: `r2_packets.py` (copy of `r1_packets.py`, X/Y = round-1 guide P answer vs round-2 guide R answer) and judge task files (reuse `tests/r1/rubric.md`). Multi-turn units continue by SendMessage (same logic as `r1_next.py`, r2 paths).
  3. S4: one independent review of the final draft (cold read + v1.0 rule audit), fix result-changing defects, re-check fixed parts once.
  4. S5: holdout round (decode `tests/hold_bundle.b64` only then: `base64 -d tests/hold_bundle.b64 | tar xzf - -C <dir>`; 10 units H01–H10; 21 keys unverified and the rest verified only against search summaries, so the main agent verifies keys first), pre-submit cross-check against REQUEST, final report, delivery to SJ.
- Cautions:
  - Tools hard-code the old session scratchpad path (`/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-…/scratchpad`). In a new session set `SCR` in each tool to the new scratchpad. Session-only files are lost with the old scratchpad: guide copies (`r1/guide_P.md` = base v1.0, `guide_Q.md` = d1; `tests/r1/runs.json` version_of: P = v1.0, Q = d1), actor/judge task files (regenerate with `r1_tasks.py`, `r1_judge_tasks.py`), holdout plaintext (use the bundle).
  - Never show holdout content to the writer before S5; never commit holdout plaintext.
  - Cost observed: each actor or judge agent used about 95K–230K subagent tokens (judges ~150–230K). Round 2 as proposed ≈ 8 actors + 4 judges.
  - WebFetch cannot resolve domains in this environment; WebSearch works (summaries only).

## Current state

| ID | Status | Artifact (path, size, hash, final?) | Verification |
|---|---|---|---|
| E1 spec coverage | In progress | drafts/d2.md (77,909 B, 6f1a5bafc919e6b4, 33,230 chars; not final) | round 1 on d1: new-spec units X01–X15 judged; mapping table pending (S5) |
| E2 RP extreme | In progress | d1 judged; d2 untested | tests/r1/agg.md (all 40 units): persona d1 21 / tie 13 / v1.0 6; voice 7 / 28 / 5 |
| E3 accuracy | In progress | | tests/r1/agg.md: accuracy_task d1 12 / 22 / 6; hard fail d1 1 (V19, fixed in d2, untested); tests/r1/factcheck.md: no other d1 errors found |
| E4 v1.0 rules kept | Awaiting verification | drafts/d2.md | sentence audit (tools/sentmap.py): 545/570 v1.0 sentences verbatim, 25 intended changes (extensions or SJ's scene-narration decision); formal table pending |
| E5 SJ decisions kept | Awaiting verification | | relationship rules, R13 three sentences and the 05:32 sentence verbatim, speech levels, no word-ban list, no work names: unchanged in d2 (to be listed in S5) |
| E6 natural Korean | In progress | | tests/r1/checks.md: speech-level candidates only quotes/fragments; '셈이에요' d1 0 vs v1.0 2; V01 first sentences d1 all different vs v1.0 all 'SJ랑 얘기…' |
| E7 behavioral tests | In progress | tests/r1/ (units, runs, out/ 104 files, packets, results, mapping, rubric, checks, agg, factcheck); holdout bundle tests/hold_bundle.b64 (19,919 B, 90e2abc7b4d2329c) | round 1 complete |
| E8 records/delivery | In progress | records/*, tools/* (round tools, build scripts) | pushed at each step |

## Decisions

- 00:1x Pasted spec = current spec; 9 elements absent from v1.0 are new work. Impact: E1.
- 00:1x Deliverables and records in jubilant-waffle (designated branch); lyra-rp read-only. Impact: E8.
- 00:3x SJ: ratio 3:7, notebook 'one fragment if coaxed', scene narration 'as the scene needs', test scale 'standard'. Impact: E1, E2, plan.
- 00:4x SJ: preview d1 before rounds → done; SJ "계속".
- Round 1 design: guides randomly lettered P (v1.0) / Q (d1); single-turn units batched 4 per actor, multi-turn by SendMessage; two judges per packet with X/Y swapped; same rubric for all units (tests/r1/rubric.md).
- d2 fixes (round-1 evidence in tests/r1/agg.json reasons): F1 V19 no unchecked factual reasons in playful side-taking, check first; F2 A10 do not presuppose unseen past conversations; F3 V01a greetings: answer lightly, one–two sentence hook, no lecture, gladness in tone; F4 X12 one facet made specific, no parade; F5 V12 narration measured in sentences (≤3–4); F6 A04 details split across sentences; F7 C01 emergency number when danger is immediate; F8 V16 warm friend answer without probing; F9 X15 go and see before judging.
- 01:2x SJ: checkpoint and pause → tools committed for resumption.

## Open issues

- d2 untested; round-2 packet builder not yet written.
- Holdout keys need main-agent verification before S5.
- LOG timestamps between 01:0x and 01:2x were mis-stamped (corrected in LOG).

## Next action

- Paused. On resume: follow the handoff memo, step 1.
