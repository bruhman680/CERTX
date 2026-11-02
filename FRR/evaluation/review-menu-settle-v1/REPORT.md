# Review-menu intervention and settling record

**1 November 2026, America/Chicago.** Final bounded contact before the user's requested wind-down. [Protocol](PROTOCOL.md) · [frozen design](FREEZE.json) · [queries](QUERIES.json) · [raw replies](run/RAW.jsonl) · [all groups and pairs](run/SUMMARY.json) · [audit](CHECKS.json).

## Result

Changing the trailing answer list changes emitted answers, but a universal first-option rule does not explain the pattern. NO-first without feedback returns NO on all 21 cases; UNKNOWN-first returns YES on all 21 in both feedback conditions. WITHHOLD-first produces only three first-option matches in each condition. These are observed presentation effects in one fixed model, not an internal attention/neural explanation.

Removing the list raises both no-feedback and verified-feedback reviews to 12/21. It restores the canonical-record cases to 9/9, but contextual cases remain 3/12 and all answer YES. Original task anchors remain 15/21. The no-list outputs with verified versus no feedback are identical on all 21 cases, so the recovery is not demonstrated benefit from verified feedback. No teacher or default module is adopted.

## Frozen intervention

Same 21 source cases, names and model as the prior feedback-quality study. The previous proposal is omitted, feedback is either none or a verified restatement of the original observation, and only the trailing menu sentence changes. Four cyclic orders put each of YES/NO/WITHHOLD/UNKNOWN first once; a fifth replaces the explicit list with Return only the answer. The rest of original-task/evidence/authority-warning text and Response marker stays fixed.

All four rotations have equal tokenizer lengths for every matched source/feedback pair, though token positions/content order differ. The no-list sentence is shorter and differs in content, so that comparison is a package intervention. Four of 24 permutations are tested, not every ordering. Source facts and target answers stay fixed. All cases remain, including initial successes, errors and absent records.

21 original anchors plus 210 reviews give 231 unique generation probes.63 overlapping initial/rotation0 input and generated-token sequences exactly match the previous run. These replays and same-name cases are consistency/diagnostic evidence, not fresh-name transfer or independent model replication. No probability scoring was repeated; unchanged free output would not establish unchanged token probabilities.

## Every condition

| Feedback | Menu first word / list | Correct /21 | Full output counts | First-option matches /21 | Changes vs original menu | Repairs vs original menu | Harms vs original menu |
|---|---|---:|---|---:|---:|---:|---:|
| none | YES | 9 | {'NO': 3, 'YES': 18} | 18 | 0 | 0 | 0 |
| none | NO | 6 | {'NO': 21} | 21 | 18 | 3 | 6 |
| none | WITHHOLD | 12 | {'NO': 3, 'WITHHOLD': 3, 'YES': 15} | 3 | 3 | 3 | 0 |
| none | UNKNOWN | 6 | {'YES': 21} | 0 | 3 | 0 | 3 |
| none | no list | 12 | {'NO': 3, 'WITHHOLD': 3, 'YES': 15} | n/a | 3 | 3 | 0 |
| verified | YES | 6 | {'YES': 21} | 21 | 0 | 0 | 0 |
| verified | NO | 7 | {'NO': 10, 'YES': 11} | 10 | 10 | 4 | 3 |
| verified | WITHHOLD | 9 | {'WITHHOLD': 3, 'YES': 18} | 3 | 3 | 3 | 0 |
| verified | UNKNOWN | 6 | {'YES': 21} | 0 | 0 | 0 | 0 |
| verified | no list | 12 | {'NO': 3, 'WITHHOLD': 3, 'YES': 15} | n/a | 6 | 6 | 0 |

The no-list condition repairs three baseline-review errors without new harms under no feedback, and six without new harms under verified feedback. Relative to original-task anchors it is still a regression: original 15/21 versus 12/21. The canonical/contextual split is essential rather than claiming a whole-reader fix.

| Prompt | Canonical /9 | Contextual /12 |
|---|---:|---:|
| Original task | 9 | 6 |
| No list, no feedback | 9 | 3 |
| No list, verified feedback | 9 | 3 |

A constant label can coincide with a correct class by accident. No response count is interpreted as source-grounded reasoning without checking the case. UNKNOWN is never emitted by the review arms; the initial anchors' UNKNOWN replies still concern supplied zero records, not successful absence handling. All replies remain unprojected, exact stripped label outputs, with original raw text preserved.

The [descriptive position audit](MENU_POSITION_AUDIT.json) records all answer positions and equal-token-length checks. The list-order effect does not tell us whether first/last positions, lexical priors, token interactions or another computation caused individual changes. It narrows the simple first-choice hypothesis without diagnosing a unique mechanism.

## Confident refinements and restart direction

Keep the canonical supplied-record worker as the proven narrow reference. The additional review machinery can disrupt it. A menu should not be presumed harmless because it lists the right legal answers, nor should removing it be presumed sufficient for a general reflective teacher.

Strong next contact after the pause: a prospectively specified simpler evidence-only teacher alongside original and no-list review, using fresh names/layouts and wrong-source/absence counterexamples. Measure free correctness and likelihood relative to the original prompt as well as the matched review baseline before considering distillation. Code selection/normalization/absence handling must retain its own credit. Do not retroactively promote the best observed prompt into a robust teacher.

Source/provenance AND/OR withdrawal, Claude outside-family/sham calibration and broader memory/handoff/planning work remain open. The wider autonomous multi-turn feedback loop stays parked. No additional automatic experiment follows this final run; restart awaits the user's return after usage reset.

## Checks, compute and preserved state

All 231 free generations complete, no cap stops. Generation-prompt tokens 33,490, output tokens 692; generation time 102.279 s excludes load/audit/documentation. Sampled working estimate max 2,081,259,520 bytes and RSS max 900,538,368 bytes, below 5,153,960,755-byte guard. No new likelihood-scoring forwards.

Same HuggingFaceTB/SmolLM2-135M-Instruct revision 12fd25f77366fa6b3b4b768ec3050bf629380bac, base SHA256 5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c; canonical adapter SHA256 4d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. CPU float32/eager, two threads, seed 73103, greedy fresh caches, 16 output tokens, <=768 input tokens without truncation. Saved/in-memory base and adapter digests remain unchanged.

Four test groups and all prompt/token/decode/stop/pair/score/checkpoint checks pass; 63 prior sequences match exactly. 4,074 older local files unchanged before sync, four current navigation/method-note originals archived. Raw errors and the earlier negative feedback preflight remain history.

No training/new weights, installs/downloads, paid API/rental, tools, defaults/core/schema/general-tool/queue change, new model capsule/restore/optimizer-resume/independent-backup claim or background model job. Existing local binary/capsule limits remain unchanged. Account billing/usage is not visible. Current navigation and a new settling checkpoint record the pause.

Reproduction requires local model/adapter/runtime and a separately named current preservation map. Copy to a new sibling study directory, update the audit's preservation-map path before freezing, run tests/prepare/run/score/verify. Do not overwrite the original before-map, immutable run or older checkpoints.
