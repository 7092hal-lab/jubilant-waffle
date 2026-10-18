# PROGRESS — Lyra RP Extreme Ed.

Goal: write Lyra RP Extreme Ed. (Korean) from v1.0 — persona realism and natural speech pushed to the extreme, accuracy sacrificed as little as possible, full current spec.
Last updated: 2026-10-19 01:4x KST (session ca3fca9e)

## Handoff memo (paste into a new conversation if this one breaks)

- Goal: as above. Request verbatim + derived requirements E1–E8: `lyra_rp_extreme/records/REQUEST.md`.
- Records: GitHub 7092hal-lab/jubilant-waffle, branch `ccr-d898a464-34plpj`, folder `lyra_rp_extreme/` (records, base, drafts, tests, reports). Reference (read-only): 7092hal-lab/lyra-rp (v1.0 work: release/v1.0, suite, scripts, records).
- Done: request recorded; base v1.0 copied and hash-checked; v1.0 records read; plan proposed to SJ.
- Plan confirmed by SJ 00:3x (all recommended options: ratio 3:7, notebook 'one fragment if coaxed', scene narration 'as the scene needs', test scale 'standard'). SJ 00:4x: show draft d1 in session before test rounds; wait for SJ's reply before S2.
- S1: d1 written (drafts/d1.md, 76,946 B, sha256 fa7c695a98d29109, 32,825 chars; built from v1.0 by asserted edits, script kept in session scratchpad tools/build_d1.py). Static checks done: doccheck (no new 아니라/줄표/말줄임표; names 0; SJ facts 0), sentence audit (547/570 v1.0 sentences verbatim; 23 changed, all intended: extensions or SJ's scene-narration decision).
- d1 shared with SJ 01:2x; SJ replied "계속" 01:3x → S2 started.
- In progress (S2 actors): 32 actor agents (16 batch × 4 single-turn convs, 16 multi-turn) for guides P/Q (key in tests/r1/runs.json version_of). Answers → tests/r1/out/{conv}_t{n}.md. Task files in session scratchpad r1/tasks (regenerable: tools r1_plan.py/r1_tasks.py; plan already fixed in runs.json).
- Holdout writer agent (background) → scratchpad hold/h_msgs.md, h_keys.md (main agent must not read; encode into tests/hold_bundle.b64 unread). Not yet finished at 01:2x.
- Caution: do not show holdout items to the writer (main agent); do not commit holdout plaintext keys before the final round; v1.0 holdouts H1–H11 are spent.

## Current state

| ID | Status | Artifact (path, size, hash, final?) | Verification |
|---|---|---|---|
| E1 spec coverage | Awaiting verification | drafts/d1.md (not final) | mapping table and round 1 pending |
| E2 RP extreme | Not started | | |
| E3 accuracy | Not started | | |
| E4 v1.0 rules kept | Awaiting verification | drafts/d1.md | sentence audit: 547/570 verbatim, 23 intended changes (LOG 01:2x); formal table pending |
| E5 SJ decisions kept | Not started | | |
| E6 natural Korean | Not started | | |
| E7 behavioral tests | In progress | tests/round1_items.md (38 units: 23 reused, 15 new X01–X15); holdout agent running | |
| E8 records/delivery | In progress | records/REQUEST.md, LOG.md, PROGRESS.md; base/lyra_rp_edition_v1.0.txt (63,385 B, ad35417a9fc6d009) | base hash = upload hash = lyra-rp release/v1.0 |

## Plan (confirmed by SJ 00:3x)

Stages: S1 design memo + draft d1 + script checks → S2 round 1 (v1.0 vs d1, ~35 units, blind pair judging ×2, main-agent fact check) → S3 fixes + round 2 (failing + guard units, ~15) → S4 independent review once (cold read + v1.0 rule audit), re-check fixed parts once → S5 holdout ~10 units, pre-submit cross-check, report, delivery.
Scale: instruction ~30–40K chars (v1.0 27,104); subagents ~55 (±15), Opus, effort max except mechanical work (scripts). Records pushed at each stage end.

## Decisions

- 00:1x Pasted spec treated as the current spec; 9 elements absent from v1.0 are new work (REQUEST notes). Impact: E1 scope.
- 00:1x Deliverables and records live in jubilant-waffle (designated branch); lyra-rp is reference only (no push there). Impact: E8.

## Open issues

- None blocking.

## Next action

- S2: run actors (waves of ≤12), continue multi-turn convs by SendMessage, automated checks, blind packets (2 judges per packet, X/Y swapped), main-agent fact check.
