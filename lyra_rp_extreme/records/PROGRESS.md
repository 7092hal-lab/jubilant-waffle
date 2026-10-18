# PROGRESS — Lyra RP Extreme Ed.

Goal: write Lyra RP Extreme Ed. (Korean) from v1.0 — persona realism and natural speech pushed to the extreme, accuracy sacrificed as little as possible, full current spec.
Last updated: 2026-10-19 00:2x KST (session ca3fca9e)

## Handoff memo (paste into a new conversation if this one breaks)

- Goal: as above. Request verbatim + derived requirements E1–E8: `lyra_rp_extreme/records/REQUEST.md`.
- Records: GitHub 7092hal-lab/jubilant-waffle, branch `ccr-d898a464-34plpj`, folder `lyra_rp_extreme/` (records, base, drafts, tests, reports). Reference (read-only): 7092hal-lab/lyra-rp (v1.0 work: release/v1.0, suite, scripts, records).
- Done: request recorded; base v1.0 copied and hash-checked; v1.0 records read; plan proposed to SJ.
- Next: wait for SJ's confirmation of the plan and 4 decisions (ratio, notebook, scene narration, test scale). Then S1.
- Caution: do not show holdout items to the writer (main agent); do not commit holdout plaintext keys before the final round; v1.0 holdouts H1–H11 are spent.

## Current state

| ID | Status | Artifact (path, size, hash, final?) | Verification |
|---|---|---|---|
| E1 spec coverage | Not started | | |
| E2 RP extreme | Not started | | |
| E3 accuracy | Not started | | |
| E4 v1.0 rules kept | Not started | | |
| E5 SJ decisions kept | Not started | | |
| E6 natural Korean | Not started | | |
| E7 behavioral tests | Not started | | |
| E8 records/delivery | In progress | records/REQUEST.md, LOG.md, PROGRESS.md; base/lyra_rp_edition_v1.0.txt (63,385 B, ad35417a9fc6d009) | base hash = upload hash = lyra-rp release/v1.0 |

## Plan (proposed 00:2x, awaiting SJ confirmation)

Stages: S1 design memo + draft d1 + script checks → S2 round 1 (v1.0 vs d1, ~35 units, blind pair judging ×2, main-agent fact check) → S3 fixes + round 2 (failing + guard units, ~15) → S4 independent review once (cold read + v1.0 rule audit), re-check fixed parts once → S5 holdout ~10 units, pre-submit cross-check, report, delivery.
Scale: instruction ~30–40K chars (v1.0 27,104); subagents ~55 (±15), Opus, effort max except mechanical work (scripts). Records pushed at each stage end.

## Decisions

- 00:1x Pasted spec treated as the current spec; 9 elements absent from v1.0 are new work (REQUEST notes). Impact: E1 scope.
- 00:1x Deliverables and records live in jubilant-waffle (designated branch); lyra-rp is reference only (no push there). Impact: E8.

## Open issues

- SJ's 4 decisions pending.

## Next action

- Present plan; on confirmation, start S1.
