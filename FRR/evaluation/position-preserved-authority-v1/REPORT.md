# Cycle1 — authority with record positions preserved

2 November2026 client date. One fixed canonical135M CPU reader; no training. All128added-context prompts have141input tokens; authority/control pairs preserve identical original-record spans and prefix text. Both name sets, two layouts, four states, two filler families, all prompts and metrics were frozen before outputs. This repairs the earlier eight-token authority confound, while leaving lexical-control limitations explicit.

Authority-minus-matched-control has positive net correctness and mean gold-logp changes on both name sets: discovery4repairs/2harms, confirmation5repairs/0harms across32contrasts from8cases each. This is not32independent samples or a universal semantic-authority effect. The control is a same-width filler slot, not no text. Every added-context condition remains below original11/16; best filler/memo/authority8/16. No teacher/default adopted.

Duplication changes direction: discovery0repairs/4harms, confirmation4repairs/1harm. Therefore the previous matched-filler duplication gain is not a stable broad rule across these new name/control/filler packages. Paper-minus-memo also changes net accuracy direction between sets. Keep the full tables and failures.

| Condition | Correct /16 | Discovery /8 | Confirmation /8 | Invalid | Repairs vs original | Harms vs original |
|---|---:|---:|---:|---:|---:|---:|
| duplicate__memo__authority_0 | 5 | 2 | 3 | 0 | 1 | 7 |
| duplicate__memo__authority_1 | 6 | 2 | 4 | 0 | 1 | 6 |
| duplicate__paper__authority_0 | 6 | 3 | 3 | 3 | 1 | 6 |
| duplicate__paper__authority_1 | 6 | 2 | 4 | 0 | 1 | 6 |
| filler__memo__authority_0 | 4 | 2 | 2 | 0 | 0 | 7 |
| filler__memo__authority_1 | 8 | 4 | 4 | 0 | 1 | 4 |
| filler__paper__authority_0 | 5 | 3 | 2 | 1 | 0 | 6 |
| filler__paper__authority_1 | 7 | 4 | 3 | 0 | 0 | 4 |
| original | 11 | 6 | 5 | 0 | 0 | 0 |

| Paired factor | Split | Repairs | Harms | Mean gold complete-sequence logp delta |
|---|---|---:|---:|---:|
| authority | confirmation | 5 | 0 | +0.557304 |
| authority | discovery | 4 | 2 | +0.486864 |
| content | confirmation | 4 | 1 | +0.279080 |
| content | discovery | 0 | 4 | -0.244104 |
| family | confirmation | 1 | 2 | -0.471756 |
| family | discovery | 2 | 0 | -0.247884 |

151generations =144fresh-condition calls and7historical anchors;576candidate-scoring forwards plus8head checks. All7anchor input/output sequences match exactly. Three design tests pass; frozen files/dependencies, saved-file/in-memory model hashes, exact inputs/candidate targets, output decoding/stops, probability arithmetic and resource checks pass. ROOT_AUDIT.json independently reconstructs192factor contrasts and verifies all64authority pairs' original-record spans. Weights unchanged, no background model job. Invalid outputs remain raw.

See PROTOCOL.md, FREEZE.json, PADDING.json (pre-run positions), QUERIES.json, TOKENIZATION.json, run/RAW.jsonl, run/SUMMARY.json, CHECKS.json and ROOT_AUDIT.json. Generation and likelihood are separate outcomes; candidate normalization is not calibrated belief/full-vocabulary KL. One checkpoint, two names and two filler words do not establish broad generalization or a neural mechanism. Original versus added contexts still differ in length/presentation; the matched comparisons are within the declared slot design. Before-placement was selected from previous results, so this is a targeted follow-up, not fresh discovery of an optimal interface.

Next model contact: isolate which content is being read with a predeclared status-observation versus answer-mapping diagnostic, preserving original and slot controls, genuine absence and wrong-source cases. Prefer a mechanistic diagnostic to another search for the highest-scoring wrapper. No distillation of these contexts.
