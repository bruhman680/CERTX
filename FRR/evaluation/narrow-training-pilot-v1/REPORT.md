# First narrow training pilot: one update, preserved partial checkpoint

30 October 2026. User-authorized local training-readiness study, with parallel primary-paper scouting. Three stages complete: design/freeze, bounded actual update plus evaluation, preserve/integrate. Coordinator designed and reviewed the experiment; one scout researched papers. No independent experimental replication, masked scoring, paid API, rental, package install or automatic model promotion.

## What actually happened

**The model made one full-weight AdamW update, then the predeclared memory-headroom guard stopped training.** The proposed 48-step schedule was not completed. A separate partial model checkpoint and optimizer state were saved. The original model and its old cache files remain unchanged.

On the frozen 48-case structural-holdout test, the original model matched 4/48 exact normalized labels; the one-step checkpoint matched 16/48, answering **NO on all 48 cases**. Every constant-label predictor scores 16/48 on this balanced test. This is a numerical score increase without demonstrated semantic discrimination. It is not a successful learned positive/zero/missing classifier, a completed fine-tuning study, or evidence for general FRR efficacy.

## The narrow lesson and dataset

The task removes arithmetic. Decide whether the explicitly recorded sampled-soil count is positive:

- YES: a recorded positive count.
- NO: an explicitly recorded zero.
- WITHHOLD: the target count is unavailable; `null`, `unavailable` and `not recorded` are declared missing markers.

Here WITHHOLD is an ordinary semantic class about the source. It is not calibrated model uncertainty or an epistemic reject option. Unsupported generated answers are separately UNRESOLVED and remain errors in the full denominator.

The fixed generator produced [96 supervised training records](TRAIN.json), [12 familiar-structure development and 48 structural-holdout test records](EVAL_CASES.json), and [separate evaluation keys](KEYS.json). Classes are balanced in every split:32each in training,4each in development,16each in test. Training structures are fields, prose, flat JSON and table. Test structures are past-tense prose, reordered fields, nested JSON and explicit target/distractor contrast. Entire structural families are withheld, alongside different positive counts. Unrelated zero and missing fields occur in every record to make “any zero” and “any missing marker” insufficient rules.

The coordinator authored and checked keys using the typed state oracle; there was no independent source-key review. These are synthetic diagnostic examples, not real-world garden measurements or independent draws from a deployment population. A structural split is more demanding than a random row split, but it does not establish every kind of out-of-distribution generalization.

[Data checks](DATA_CHECKS.json) record source overlap checks and family disjointness. The first preparation detected duplicated development zero/missing sources; the development distractor was changed to unused13 before any model evaluation. The overlap assertion remained in place. [Preparation note](PREPARATION_NOTE.md) preserves that failure and correction.

## Resource check, actual update and stop

The local checkpoint is HuggingFaceTB/SmolLM2-135M-Instruct, pinned revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`,134515008 parameters. Runtime: CPU float32/eager, two threads, local files only, torch2.6.0+cpu, transformers4.57.1. This model was already pretrained and instruction-tuned; this was our first additional weight-training pilot.

A [backward-only feasibility probe](FEASIBILITY.json) used batch2 at113tokens:1.701seconds and process peak RSS2022031360bytes. It computed gradients without an optimizer update. A rough weights/gradients/two-Adam-moments estimate was2152240128bytes. This supported a bounded attempt, not a guarantee of a full schedule: the actual longest training sequence was163tokens, and the probe did not measure the full optimizer/cgroup working-memory footprint.

Frozen schedule: full-model AdamW, batch2, learningrate0.0001, weightdecay0.01, gradientnormclip1, seed20261030,48steps through one shuffled96-example pass; no scheduler or hyperparameter search. Teacher-forced loss covers assistant label plus EOS only, normalized per example before averaging, so longer label tokenizations do not automatically receive greater per-example weight. Padding is masked and training cache disabled.

Between completed steps, stop at240seconds, nonfinite loss/gradient, or loss of40% memory headroom. The implementation estimates cgroup working memory as current minus inactive_file, accounting approximately for reclaimable file cache. At step2's precheck it reported `memory_headroom` and stopped. The threshold was60%of8GiB. The runner did **not** retain the exact triggering cgroup reading; this is an instrumentation gap. The recorded peak process RSS was3320123392bytes, which is a different quantity. No out-of-memory crash occurred, and no claim follows that this environment cannot train this model with another memory policy or training method.

Actual training: **one completed optimizer step, two examples,2.784seconds** excluding checkpoint serialization. The examples were one zero flat-JSON record and one positive table record. **No missing-class example received an update.** Loss2.9363842010498047 and preclip gradient norm58.84357833862305 are in [TRAINING_LOG.jsonl](TRAINING_LOG.jsonl). One loss value cannot establish a decreasing training-loss curve.

All272stored weight tensors differ numerically from the original after float32 comparison; maximum absolute change0.00010633468627929688; all adapted values checked finite. A changed file hash alone would not prove learning because serialization/dtype can differ; the numerical tensor comparison establishes that weights changed. It still does not establish useful learning.

The partial full checkpoint and optimizer state are local at `/workspace/narrow_training_checkpoint_v1`; their hashes are in [TRAINING_MANIFEST.json](TRAINING_MANIFEST.json). They are not silently substituted for the original checkpoint or uploaded as large binary Git objects. Local workspace retention is not an independent archival guarantee.

## Input-guard failure and controlled continuation

The first runner completed12baseline-development calls, then stopped at its160-token input assertion before creating an optimizer. The separate preflight had found163tokens, but the coordinator launched the runner before consuming that result. This was a sequencing mistake.

The original runner, freeze, plan, raw prefix and logs are preserved in [failed_preflight](failed_preflight/PLAN.md). The guard was raised to192 without truncating or changing examples, prompts, learning rate or batch schedule. The amended protocol and runner were frozen before the first optimizer update and any test forward pass. The12baseline-development calls were reused byte-for-byte after prompt/cache validation, not regenerated or counted twice. No test outputs existed when this repair was made. The only subsequent training attempt was the single bounded pilot above; no second schedule was substituted after its memory stop.

[FREEZE.json](FREEZE.json) records the amended pre-training inputs, including the baseline prefix; [RAW_FREEZE.json](RAW_FREEZE.json) binds completed outputs and training records before structured scoring. Some log completions were already viewed, so review was not blinded. Evaluation keys were integrity-hashed but not parsed or inserted into generation prompts; training labels were intentionally used for supervised updates.

## Evaluation and full-denominator results

Generation: fresh context per call, argmax decoder,8new-token cap, no continuation/retry or posthoc phrase extraction. This short exact-label task is different from earlier64-token full-variance prompts; do not compare scores as though the tasks and caps were identical. A capped explanatory answer is UNRESOLVED under this frozen interface; it is not proof that its unfinished semantic intent was wrong.

The original checkpoint's development slice was evaluated before training. Final development and both original/adapted test evaluations occurred only after the update and checkpoint save. There were120unique generation calls total:12originaldev,12adapteddev,48adaptedtest,48originaltest. A fixed evaluation order is not a randomized timing experiment.

| Split/checkpoint | Exact matches | Output behavior | EOS / cap |
|---|---:|---|---:|
| Development, original | 1/12 |3YES,9UNRESOLVED |3 /9|
| Development, partial adapted |4/12 |12NO |12 /0|
| Structural test, original |4/48 |12YES,36UNRESOLVED |12 /36|
| Structural test, partial adapted |16/48 |48NO |48 /0|

On test, original recalls are YES4/16,NO0/16,WITHHOLD0/16; adapted recalls are YES0/16,NO16/16,WITHHOLD0/16. Every adapted structural family scores4/12, exactly the always-NO baseline. Paired changes:16adapted-only matches,4original-only matches,28neither,0both. The adapted model replaced many unfinished explanations with a uniform valid label. Formatting/completion improved under this interface, while the intended three-class distinction was not demonstrated. This narrow comparison does not establish catastrophic forgetting or broad improvement/degradation; unrelated abilities were not tested.

Full [summary](SUMMARY.json) includes confusion matrices, family breakdowns, token counts and timings. Total generation usage:18806inputtokens,510generatedtokens includingEOS. All120newterminal caches are preserved locally under `/workspace/smollm_narrow_training_states_v1`,885138664bytes total. These caches preserve inference state; the separately updated weights are what make this actual training.

The unchanged [stored-run auditor](../../tools/stored_run_audit.py) checks each declared cohort and source binding: [original test receipt](original_test/RECEIPT.json), [adapted test receipt](adapted_test/RECEIPT.json), plus development receipts. [Scorer](score.py) checks all120ordered IDs before deriving views; unsupported generations stay in the denominator. Source identity, typed roles, exact labels and bytes are checked, not empirically proven source truth.

[Artifact checks](ARTIFACT_CHECKS.json) confirm all120cache byte/shape/prefix bindings, prompt tokenizations and decoded outputs; all370recorded prior model/cache files unchanged; final checkpoint and optimizer hashes; frozen inputs and raw results unchanged. Coordinator consistency checks are not independent replication.

## What the research scout contributed

[Research scout](RESEARCH_SCOUT.md) supplies exact read depths and limits for primary sources:

- [HANS, McCoy et al.](https://arxiv.org/abs/1902.01007): diagnose lexical/structural shortcuts and test withheld subcases; successful augmentation can still leave replacement shortcuts.
- [SCAN, Lake & Baroni](https://arxiv.org/abs/1711.00350): random splits do not establish systematic compositional transfer. Different models/tasks limit direct extrapolation.
- [SelectiveNet](https://arxiv.org/abs/1901.09192): rejection needs coverage/risk evaluation; source MISSING is not that reject option.
- [SmolLM2 report](https://arxiv.org/abs/2502.02737): capacity-aware post-training data curation supports trying a narrow task, not a135Mlearning ceiling or a CPU hyperparameter guarantee.
- [Shortcut-learning perspective](https://arxiv.org/abs/2004.07780): abstract-only broader framing, not another independently audited experiment.

A separate [memory scout](MEMORY_SCOUT.md) follows the stop with original [LoRA](https://arxiv.org/abs/2106.09685): freezing base weights and learning low-rank updates reduces trainable parameters and optimizer-state demand, while base-weight and activation memory remain. GPU savings reported in another setting cannot be assumed for this CPU setup. No adapter implementation or second training run was installed in this contact.

## Decision and next strongest direction

No trained model is promoted. The partial checkpoint is an inspectable branch, not a new trusted gardener. The completed result is: actual weight updates are locally possible, full-AdamW resource estimates need improvement, and a single two-example update can change output behavior without demonstrating the intended distinction.

Next strongest training contact is a **parameter-efficient or restricted-parameter resource probe**, followed by a newly frozen pilot only if it fits. Measure optimizer allocation plus activations and retain the exact guard-trigger readings. Balance classes within each early effective update using accumulation if needed; otherwise a short budget may never expose one class. Do not infer any class-generalization result from this two-example step. Current48testexamples are now exposed and should be regression data, not a fresh test for subsequent tuning. Preserve new structural holdouts for the next primary evaluation.

The read-only station registry remains a compatible larger infrastructure direction: it should relay scope, ancestry, changed weights, partial-training status and unresolved cases. A central summary must not relabel4/48→16/48as successful semantic learning merely because the fraction rose. Existing deterministic tools, earlier failed source-reading gates, broadqueue/core/schema and historical results stay unchanged.
