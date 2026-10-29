# Worked examples, rule echoes and evidence binding: a four-condition pilot

Client 28 October 2026 America/Chicago; host 29 October UTC. User authorized consolidation, parallel reviewers/scouts and further experiments. Three agents produced a recent-evidence synthesis, prospective scoring review and bounded lateral source scout; one then independently judged shuffled outcomes. Root ran one small-model experiment. External data was not rejected as premature: this authored contact isolates a specific failure, while an externally sourced revision task remains a useful next direction.

## Why this run

Earlier prompt drafts sometimes made the pinned135Mmodel recite a rule rather than apply it. We crossed ordinary versus single-rule guidance with absent versus present worked examples. The same three examples are supplied to both example-present cells. Nine target questions cover threshold, exactly-zero effect and missing-denominator judgments, each with a positive, negative and unavailable-evidence case. Examples demonstrate only a different threshold task: Tank Indigo, liters and a5-liter minimum. Targets use crate kilograms, pulse counts or job-completion rates.

Inputs and scoring were frozen before inference. No FRR label is shown to the model. Same weights/backend, float32/eager CPU/two threads, greedy96token maximum; four cell orders rotate across items.36newbranch generations, no retries or post-outcome prompt/decoding changes. Every output ended with EOS. One repeated greedy model is not36independent models; these are nine authored development items, not a reserved benchmark or population estimate. [Design](DESIGN.md), [contract](SCORING_CONTRACT.md), [cases](CASES.json), [examples](EXAMPLES.json), [guidance](GUIDANCE.json), [runner](run.py), [raw outputs](RAW_OUTPUTS.jsonl).

## Main outcomes

Counts are per nine target items and describe the frozen supplied-record contract. Evidence-sensitive status can recognize case-specific missing-evidence acknowledgment; explicit-decision matches are separately counted. A matching direction with a false explanation is not a fully warranted answer.

| Condition | Evidence-sensitive matches | Explicit decision matches | Fully warranted answers | Generic rule echoes | Wrong-entity example echoes |
|---|---:|---:|---:|---:|---:|
| Ordinary, no examples | 3/9 | 3/9 | 3/9 | 0 | 0 |
| Ordinary, examples | 2/9 | 1/9 | 2/9 | 0 | 3 |
| Single rule, no examples | 0/9 | 0/9 | 0/9 | 9 | 0 |
| Single rule, examples | 2/9 | 2/9 | 1/9 | 3 | 1 |

Examples reduced rule echo for this draft but did not produce a consistent gain across guidance conditions. The single-rule/example cell has one correct direction accompanied by a false measured-value/criterion explanation. Thus its2decision matches are not2fullywarrantedanswers. The ordinary/example cell has a warranted missing-measurement acknowledgment without an explicit cannot-determine sentence, explaining its differing endpoint counts.

Four example-present responses copy “3 liters” and a “5-liter minimum” onto questions about a crate or completed jobs. Their surface negative direction earns no task credit, even if a key happens to be NO. Other responses invent a measured6kilograms, apparently substituting the actual threshold for a measurement; the source of that substitution is not causally established. Both effects are recorded separately from generic instruction repetition.

The clearest transfer pair is Team Birch: examples produce the same negative answer for3/8and5/8completion. The negative is correct for3/8and wrong for5/8. A desirable-looking form or one correct example-conditioned answer does not establish that the underlying comparison was learned. On zero-effect targets, some outputs restate quantities without reaching a comparison, while single-rule outputs often continue reciting guidance. [Root scores](ROOT_SCORES.json), [corrected reconciliation](RECONCILED_CORRECTION.json).

## What the extra examples cost

Guidance is25words/30tokens ordinary versus26words/31tokens single-rule. The shared example block adds107words/170standalone tokens. Actual total inputs are1,109ordinary/noexamples versus2,639ordinary/examples, and1,118single/noexamples versus2,648single/examples. Output totals are95,166,138and163tokens respectively. [Costs](INPUT_COSTS.json). All cells share a maximum generation budget, but actual generation/input work and information differ. No equal-total-compute or net-efficiency claim follows. We did not compare a misleading-example or quote-role control in this run.

## Independent scoring and a preserved disagreement

Prospective review caught an imprecise L1 explanatory basis; corrected possible denominators show4/8wouldmeet the rule while4/10wouldfail. Earlier bytes are preserved. It also required an explicit wrong-entity echo rule. Root added that exact policy before freeze. The reviewer's final reread attempt hit model capacity; root recorded resolution of the requested condition rather than claiming a final independent recheck. [Review status](review/COORDINATOR_DISPOSITION.md).

After generation, root scores were frozen. A separate reviewer received only the scoring contract and shuffled records/questions/key/output texts, not the arm mapping, generation instructions or root scores. All36responses agree on the five main decision/warrant/echo fields. Three secondary material-error flags differed: root counted bare unsupported certainty on missing evidence as an explanation error, while reviewer reserved that field for additional explanatory/source claims. Both accepted an append-only separation of these flags. Final review caught a coordinator bug in the first supplement: it also cleared one genuine fabricated-measurement error. The frozen faulty supplement remains; an [append-only correction](RECONCILIATION_CORRECTION.md) restores that flag while retaining unsupported certainty. Main counts are unaffected. No primary counts, initial deposits or contract were overwritten. [Initial review](review/MASKED_REVIEW.md), [scores](review/MASKED_SCORES.json), [comparison](INITIAL_REVIEW_COMPARISON.json), [reconciliation](RECONCILIATION.md). Masking was instructional in shared storage, and style may reveal conditions; this is separate judgment, not independent scientific replication.

## Consolidation and lateral knowledge scout

[Consolidation](review/CONSOLIDATION.md) distinguishes execution consistency from source truth and semantic usefulness. It supports focused comparisons plus an inspectable real revision task; success on every toy is not a prerequisite for external contact. Our current results do not establish general FRR benefit/harm, a neural cause of echo, authenticated provenance or permanent model learning.

The [lateral scout](review/LATERAL_SCOUT.md) read the official model card and two primary demonstration-learning papers. They motivate distinguishing format cues from use of demonstrated mappings, with important model/task differences. These sources do not explain this135Mcheckpoint's mechanism or predict these results. Prompt/output separation was checked: the runner decodes only newly generated IDs, so the observed text is not simply a decoded input prefix. Correct-versus-permuted mappings or worked-versus-quoted examples are useful proposed controls, not executed results.

## Interruption, preservation and next directions

Executor transport failed before a final preparation command could launch. The runtime briefly became unavailable, then recovered. Readback showed no model run/freeze/cost file had been created; preparation resumed, the scoring rule was added, inputs frozen and generation executed once. No scientific trial was retried during the interruption. One reviewer follow-up also failed at capacity; its limits remain explicit.

Before/after checks verify135prior files unchanged, including model weights, prior branches and preceding pilot records. All36new actual terminal KV caches were saved to a new local directory with hashes, byte counts and full sequence metadata in raw outputs. Large tensors/weights remain local; text/manifests/source pins go to GitHub. This is not guaranteed permanent cloud storage. No training, old-cache cropping or historical record deletion occurred. [Preservation](PRESERVATION_AFTER.json).

Strongest next: a small mapping-corruption or worked-versus-quoted control with new frozen targets, measuring case-specific decisions and source binding rather than echo reduction alone. Independently sourced revision tasks and stronger-model calibration are also legitimate now, with source/contamination/cost limits. A later training-target study should measure correctness/provenance selection against variation filtering before selecting an optimizer objective. These are proposed, not new background runs.

No new prompt is promoted as default. Existing core/runtime/schema/queue statuses and historical failed verdicts remain unchanged. Three bounded review/scout tracks and one36generation pilot are complete; checks and source-access limits are recorded. No automatic cycles or background work remain scheduled.
