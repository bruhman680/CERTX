# Equal length, different behavior: repeated evidence and its surroundings

2 November 2026, client date. Fixed canonical SmolLM2-135M-Instruct LoRA reader, CPU. No training, retained memory update, new model or paid inference.

## Finding

Duplicated evidence is **not uniformly harmful** once compared with token-matched filler. The duplication contrast has a small positive net correctness effect on both predeclared name sets. Placement has the clearer repeated direction: supplementary blocks after the original task produce more harms than placing those same blocks before it. The authority reminder does not reproduce an accuracy gain on the confirmation name.

The original task scores **11/16**; padded-original control **5/16**. Highest-scoring added-context arm is duplicate/no-authority/before at **10/16** (one repair and two harms against original), while duplicate/no-authority/after scores **4/16**. No added-context arm exceeds the original task. No teacher or default is adopted.

These are new cases, not a rescore of earlier15/24. Both original and duplicate-before split scores, all contrasts and invalids remain below. The prior observation that faithful notes harmed a particular review package remains true; its broader explanation must allow the matched controls here.

## Frozen design and all arms

Two names, two record layouts and four balanced statuses give16cases. First name supplies8discovery cases and the second8prospectively held-back confirmation cases. Both sets and every arm were fixed before outputs; no selection/tuning occurred between sets. The confirmation tests another name on the same layouts, mapping and model; it is not broad independent replication.

Each case has original and padded-original baselines plus content(duplicate/filler) x authority reminder(present/absent) x placement(before/after). All144added-context prompts are **exactly144chat-template input tokens**. Original-task and7historical anchors stay unpadded. Padding is repeated ` memo`, chosen from input token lengths before outputs. There is no previous proposal, gold answer, retrieved evidence or actual failure message in the prompt.

| Condition | Correct /16 | Discovery /8 | Confirmation /8 | Invalid | Repairs vs original | Harms vs original |
|---|---:|---:|---:|---:|---:|---:|
| duplicate__authority_0__after | 4 | 2 | 2 | 0 | 0 | 7 |
| duplicate__authority_0__before | 10 | 5 | 5 | 0 | 1 | 2 |
| duplicate__authority_1__after | 7 | 4 | 3 | 1 | 0 | 4 |
| duplicate__authority_1__before | 7 | 4 | 3 | 0 | 1 | 5 |
| filler__authority_0__after | 4 | 2 | 2 | 0 | 0 | 7 |
| filler__authority_0__before | 6 | 3 | 3 | 0 | 0 | 5 |
| filler__authority_1__after | 5 | 3 | 2 | 0 | 0 | 6 |
| filler__authority_1__before | 8 | 4 | 4 | 0 | 1 | 4 |
| original | 11 | 6 | 5 | 0 | 0 | 0 |
| padded | 5 | 2 | 3 | 0 | 0 | 6 |

## Prespecified paired factors

Each factor has **32paired contrasts from8distinct cases per split**: every case participates at four settings of the other factors. These are not32independent people, agents or task examples. Delta is right-minus-left absolute gold complete-label-plus-EOS log probability, in natural-log units. All casewise effects and status/layout breakdowns are saved; no p-values or population guarantees are claimed.

| Contrast | Split | Correct before -> after /32 | Repairs | Harms | Mean gold logp delta | Logp increases / decreases |
|---|---|---|---:|---:|---:|---|
| reminder minus absent | confirmation | 12 -> 12 | 2 | 2 | +0.793915 | 13 / 19 |
| reminder minus absent | discovery | 12 -> 15 | 4 | 1 | +1.157052 | 18 / 14 |
| duplicate minus filler | confirmation | 11 -> 13 | 3 | 1 | +0.103105 | 21 / 11 |
| duplicate minus filler | discovery | 12 -> 15 | 3 | 0 | +0.228716 | 24 / 8 |
| after minus before | confirmation | 15 -> 9 | 1 | 7 | -0.370242 | 12 / 20 |
| after minus before | discovery | 16 -> 11 | 0 | 5 | -0.427557 | 11 / 21 |

Duplication yields3repairs/0harms in discovery and3repairs/1harm in confirmation. It helps relative to these particular filler packages, not universally relative to the original task. Placement after yields0repairs/5harms in discovery and1repair/7harms in confirmation. The authority reminder yields a discovery net gain but confirmation2repairs/2harms; positive mean likelihood changes are not a replicated accuracy benefit. On confirmation its mean likelihood gain coexists with13increases and19decreases, illustrating why a mean is not universal improvement.

Original status accuracy is positive4/4, zero3/4, literal missing4/4, genuine absence0/4. Duplicate-before/no-authority reads zero4/4 and missing2/4, trading one zero repair against two missing harms. Genuine absence remains0/4 in every arm. A recognizable UNKNOWN output on a different status does not count as solving absence.

## Position audit: equal length is a limited control

[SPAN_AUDIT.json](SPAN_AUDIT.json) checks exact token offsets of the frozen original observation. Adding the authority reminder moves the original record **eight tokens earlier** in every before-placement arm, because some padding transfers to the ending reminder. In after-placement arms the original record starts at the same token. The authority contrast therefore includes a padding/position redistribution in the before arm; it does not isolate the semantics of that sentence alone. This caveat comes from tokenized inputs, not an inferred neural explanation.

Equal total tokens remove a simple unequal-length explanation for differences among the factorial arms, but do not neutralize word choice, instruction position, filler count, repetition or attention. `memo` is not proved neutral. Before/after effects are consistent with presentation/recency sensitivity, without identifying a unique internal mechanism. The padded-original baseline is one additional-text package, not a pure universal length intervention.

## Execution, preservation and audit

**167generations** =160fresh-condition calls plus7historical anchors; **640candidate-scoring forwards**, plus8head-equivalence checks. Generation uses its own variable forward steps. All7historical input and output sequences replay exactly. Three design tests pass. Prompt construction and matching, exact input tokens, candidate targets, code, protocol and checkpoint dependencies were frozen before model load. Input matching used no model outputs.

Saved output verification reconstructs prompts, decoded replies, stops, strict labels, per-token log probabilities and candidate normalization. [ROOT_AUDIT.json](ROOT_AUDIT.json) independently checks all192factor contrasts, equal-length pairings, pre-run inputs,640candidate target/first-token scores and resource readings. Saved-file and in-memory base/adapter digests remain unchanged. Head check passes at1e-4 tolerance. Invalid output is preserved. No background model job remains.

[PROTOCOL.md](PROTOCOL.md), [FREEZE.json](FREEZE.json), [QUERIES.json](QUERIES.json), [TOKENIZATION.json](TOKENIZATION.json), [PADDING.json](PADDING.json), [raw records](run/RAW.jsonl), [full summary](run/SUMMARY.json), and [CHECKS.json](CHECKS.json) retain the evidence. No old report or raw model output was changed.

## Next strongest and confidence

The clearest repeated directional finding here is before/after placement sensitivity at fixed total input length. Duplication's earlier package-level harm does not generalize to all matched comparisons. Confidence is narrow: one checkpoint, one filler family, two names, four statuses and two layouts. Candidate-normalized masses are not calibrated beliefs or full-vocabulary KL; generation and likelihood remain separate outcomes.

Next, predeclare a position-preserving authority contrast and a second filler family on untouched names. Match original-record offsets as well as total length where the intended factor permits; save the offsets before execution. Retain original-task comparisons and absence failures. Do not distill the present teacher contexts or choose a prompt simply because it won this small table.
