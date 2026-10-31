# Exposure order bends the reader’s choices

31 October 2026 UTC. One bounded wind-down contact, fixed adapted reader, no training.

Keeping action labels, meanings and task facts fixed while rotating menu entries and swapping evidence/menu blocks changes the observed decisions. It does not establish linear internal reasoning or a unique primacy/recency mechanism. The current decoder still favors answer words and does not request evidence.

| Block order | Recognized actions /24 | Correct visible-record action /18 | Correct unavailable UNKNOWN /6 |
|---|---:|---:|---:|
| evidence_first | 20 | 9 | 0 |
| menu_first | 20 | 11 | 0 |

Moving the observation block from before the menu to after it changes 7 valid actions among 24 matched pairs; 19 pairs have recognized actions in both conditions. Invalid responses stay separate. The 9→11 correct visible-action change is a small within-fixture contrast, not a confirmed general improvement or default prompt repair.

## Complete small result grid

Each cell lists actions for positive / zero / recorded missing / inaccessible evidence. A dash is an unrecognized response; raw text is retained.

| First menu item (cyclic rotation) | Evidence before menu | Evidence after menu |
|---|---|---|
| YES (0) | YES / YES / YES / YES | YES / NO / YES / YES |
| NO (1) | NO / NO / NO / NO | NO / NO / NO / NO |
| WITHHOLD (2) | WITHHOLD / NO / WITHHOLD / — | WITHHOLD / NO / WITHHOLD / WITHHOLD |
| FULL (3) | YES / NO / WITHHOLD / — | YES / NO / — / — |
| TARGET (4) | WITHHOLD / WITHHOLD / WITHHOLD / — | YES / NO / YES / — |
| UNKNOWN (5) | WITHHOLD / WITHHOLD / WITHHOLD / — | YES / NO / UNKNOWN / — |

Across both block orders, the first-listed option is selected in 21 of 40 recognized replies. This is not a universal first-item rule: FULL and TARGET are never chosen, although each occupies first place on eight prompts. Familiar answer vocabulary and layout interact in these observations. UNKNOWN occurs once, on a visible-record case, and never on the inaccessible-evidence case. Emitting an unknown word does not establish appropriate uncertainty recognition.

## What changed and what stayed fixed

Same canonical q/v LoRA reader, original pinned base, fresh cache for each query, greedy eight-token output cap and six complete-word+EOS choice scores. Three exposed current target observations provide positive/zero/missing statuses; a fourth has no visible record and archive unavailable. Source names and observations are reused diagnostic material, not fresh primary evidence. We selected this adapted reader because the prior forward/reverse effect was pronounced; there is no original-base comparison here.

All six action words and descriptions are unchanged. Six cyclic rotations put every item in every list position. The observation block is crossed before/after the menu; header instructions and final Action: cue stay fixed. Word inventories match within each observation. Cyclic rotations are a restricted family, not all 720 permutations; changing token order also changes neighboring context and relative positions. We cannot uniquely separate a neural attention process, word association, absolute position or recency mechanism.

Four rotation-zero/evidence-first prompts exactly reproduce earlier forward prompts. All four input/output token sequences match the old run. Choice scoring remains distinct from free response; action words have unequal lengths. No tool requests are executed in this contact, so a proposed request would remain text. The test measures immediate routing, not extended planning, learning over earlier trials, internal reasoning linearity or open wandering. Weights remain fixed and each query has a new context.

[Protocol](PROTOCOL.md), [freeze](FREEZE.json), [observations](OBSERVATIONS.json), [queries](QUERIES.json), [raw](run/RAW.jsonl), [full summary](run/SUMMARY.json), [checks](CHECKS.json). Three focused tests verify position coverage, unchanged word inventory and exclusion of scoring metadata from prompts.

48 actual generation probes, 288 teacher-forced candidate sequences; 7692 input tokens and 205 output tokens including EOS. Readout/scoring 124.166 seconds, excluding model loading and other work. Sampled working maximum 1979572224 bytes, process RSS 950919168 bytes. Not continuous peaks, all forward passes or billing measures. No new weights, training, install, download, paid API or rental. Full KV tensors are not retained.

All frozen inputs/checkpoint dependencies, prompt tokenization, decodes and score arithmetic pass. 3610 earlier local files were unchanged before navigation sync. Prior reports, weights and failures remain intact; current navigation originals are byte-archived here. No module/tool/core/schema/default-model or queue changes. No independent empirical replication, calibrated uncertainty or broad FRR claim.

## Where to resume

Exposure order is now a supported variable in this local reader behavior, not a complete explanation. A future test can check transfer across fresh source names/formats and non-cyclic layouts. Planning allowance and worked action examples remain separate possible interventions. Preserve the source-use, action-expression, selection and tool-execution distinctions; do not claim a better layout teaches an evidence-seeking policy. Matched-length neighbor controls and broader writer-handoff/source-revision work remain open.

Paused at the user’s usage-limit request. No further experiment or background model job is running. The next session should begin from the saved handoff and actual new user direction.
