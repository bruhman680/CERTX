# Evidence-only teacher contact: simplification did not make a reliable teacher

2 November 2026. Existing canonical LoRA SmolLM2-135M-Instruct, fixed weights, CPU. Three parallel agents provided design review, primary-source scouting and the separate guard control. No new model, install, download, paid inference call or training step.

## Outcome

On 24 balanced fresh cases, the original task scores **15/24**. The simpler no-feedback review scores **10/24**; adding faithful evidence drops this to **7/24**, with **zero repairs and three harms** relative to its own no-feedback control. Wrong-source evidence scores6/24. None of these review arms establishes a reliable self-teacher, and no distillation follows.

This is a new24-case test, not the historical15/21 result. Three synthetic name pairs, two layouts and four statuses are stimulus variation on one fixed model/checkpoint, not independent model replications. Every original task explicitly specifies genuine absence; the old canonical template did not. Keep those template differences visible.

## All frozen conditions

Each row has24 cases. Faithful and wrong-source changes are measured against that interface's no-feedback row. Gold log probability is the absolute complete-label-plus-EOS log probability; delta is in natural-log units, averaged over all24 cases. It is not a probability-point or accuracy change.

| Interface | Note | Correct | Invalid | Repairs vs own none | Harms vs own none | Mean gold logp delta vs own none |
|---|---|---:|---:|---:|---:|---:|
| no_list | irrelevant | 6 | 1 | 0 | 0 | -2.235871 |
| no_list | none | 6 | 1 | 0 | 0 | +0.000000 |
| no_list | verified | 6 | 3 | 0 | 0 | -0.590740 |
| old_menu | irrelevant | 6 | 0 | 0 | 0 | -0.085094 |
| old_menu | none | 6 | 0 | 0 | 0 | +0.000000 |
| old_menu | verified | 6 | 0 | 0 | 0 | +0.041214 |
| original | none | 15 | 3 | 0 | 0 | +0.000000 |
| simple | irrelevant | 6 | 2 | 0 | 4 | -4.330484 |
| simple | none | 10 | 5 | 0 | 0 | +0.000000 |
| simple | verified | 7 | 5 | 0 | 3 | -0.809598 |

## What changed and what stayed difficult

The simpler package recovers four correct answers relative to old-menu/no-list no-feedback reviews, but remains five below the original task. This is partial presentation recovery. Faithful duplication removes three initially correct literal-missing answers under the simple interface: missing accuracy falls4/6 ->1/6. Positive stays6/6. Zero and genuine absence remain0/6 in every review condition. Original task reads zero4/6 and missing5/6; it also gets genuine absence0/6. Thus the feedback wrappers harm behaviors the same model already displays under its original prompt, while absence is a failure already present in the fresh original task.

Simple faithful evidence raises correct complete-sequence likelihood on8/24 cases and lowers it on16/24 relative to simple-none, with mean delta-.809598. Against the original task, only3/24 increase,21/24 decrease, mean-1.211696. Old-menu faithful evidence has a small positive mean likelihood change+.041214 against its degraded no-feedback control, but no accuracy repair and substantially lower mean likelihood than the original task. A favorable local statistic is not enough for teacher adoption.

No-list faithful evidence has the same6/24 accuracy as no-list none, while invalid replies rise1->3. Identical accuracy is not identical output behavior. Wrong-source notes remain harmful in probability even when a collapsed YES response leaves accuracy unchanged.

## Execution and verification

Executed **247 generations**:240 fresh-condition calls plus7 legacy anchors. Scored **960 complete candidate sequences** with separate forward passes, plus8 full-versus-limited-head validation forwards. Generation has its own variable number of forward steps; these are not claimed as247 total model forward passes. All7 historical anchors match previous input and generated-token sequences exactly.

Three design tests pass. Preparation first exposed duplicate absence prompts across nominal layouts; inline task rendering was corrected before outputs. Independent review then caught omitted summary metrics, an overly tight directional-count tolerance, and length-only tokenization. Exact token IDs and1e-5 numerical ties were saved and all affected artifacts re-frozen before model execution. Initial preparation bytes remain in before_prepare; no favorable-output prompt search took place.

The head-equivalence check passes at tolerance1e-4. The saved-token verifier checks exact prompts/input tokens, decoded replies, EOS/cap stops, strict labels, candidate target tokens, per-token selected-logit-minus-normalizer arithmetic, sequence sums and candidate normalization. An additional audit matches all247 inputs to the pre-run token IDs and reconstructs960 first-token probabilities. Saved-file and in-memory base/adapter digests match the acquisition manifest before and after the run. Resource checks pass; no background model job remains.

See [PROTOCOL.md](PROTOCOL.md), [FREEZE.json](FREEZE.json), [CHECKS.json](CHECKS.json), [ROOT_AUDIT.json](ROOT_AUDIT.json), [run/SUMMARY.json](run/SUMMARY.json), and [raw replies and token scores](run/RAW.jsonl). Every candidate-relative/absolute mass, state/layout breakdown, invalid output and paired logp delta is retained. No normalization is used to project an answer into the label set: free generation is scored separately.

## Interpretation and limits

Evidence notes duplicate supplied facts; no tool retrieves new evidence. There is no previous attempt in these prompts, and the model never receives evaluator labels. This tests response to a feedback-style presentation, not an autonomous model observing an actual failure and learning persistently from it. Each prompt starts a fresh KV cache; weights stay fixed. No private reasoning trajectory, neuron mechanism or general FRR efficacy is established.

The original, old-menu, no-list and simple renderings differ in length and wording. Results concern these prompt packages; they do not isolate one harmful phrase. Six cases per status and one checkpoint are narrow evidence. Four complete candidate strings cover only a fraction of full-vocabulary output space, and their relative masses are not calibrated beliefs. The faithful source is planted and trusted by construction; there is no authenticated-source retrieval experiment.

[Primary-source scout](scouts/FEEDBACK_KNOWLEDGE.md) distinguishes intrinsic correction, oracle stopping and actual external evidence. Its model scales differ from ours. The findings support our all-case repairs/harms controls, not predicted transfer.

## Next strongest contact — not run

Do not distill these review contexts. First isolate duplicated-record effects from added-text/authority effects with fixed observation, matched padding and note-placement controls, retaining original and per-interface none baselines. Predeclare a small explanatory test and an untouched confirmation set instead of searching many prompts for a positive result. Genuine absence remains a separate unresolved readout requirement; additional contextual evidence did not solve it. Training, source-selection delegation and model reasoning must continue to have separate receipts.
