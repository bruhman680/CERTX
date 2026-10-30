# Soil-design reader: the toy distinctions did not transfer reliably

SR-C1, 30 October 2026 UTC. Follow-up to [SD-C1/2/3](../soil-design-three-cycle-v1/REPORT.md), parent commit `2865321a76e6588150d14353b3a8fbf2376da499`.

**The numerical distinctions remain valid, but the small reader did not reliably use them.** Eight newly authored source records each received three separate questions: source reading, calculation or feasible-set reconstruction, and final conclusion. Across 24 fresh local generations, the respective semantic matches were **2/8, 0/8, and 2/8**. No record had all three separately elicited answers correct.

This is a diagnostic failure on these fixtures with the current prompt and model, not a general limit of models or FRR, and not evidence that the earlier mathematics failed.

## What actually ran

- Local `HuggingFaceTB/SmolLM2-135M-Instruct`, revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`; text only, CPU float32, eager attention, two threads, eval/inference mode. Python 3.12.14, torch 2.6.0+cpu, transformers 4.57.1.
- Eight new records, three independently initialized chat contexts each, 24 greedy argmax generations, 64-new-token cap, EOS stopping. No sampling, answer retries, continuation, model training, or reused old inference context.
- One ordinary record-and-rule instruction, no examples or dedicated broad FRR-base intervention. There is **no comparison arm**, so this is not an FRR-versus-ordinary evaluation or a claim about the main assistant's abilities.
- The supplied sources contain the formulas and task criterion. Gold keys were stored separately and not parsed into the model prompts; the runner checks their file hash as part of the frozen-input manifest. No claim of pretraining independence or uncontaminated population sampling follows.
- [Protocol](PROTOCOL.md), [records](RECORDS.json), [questions](CASES.json), [keys](KEYS.json), [guidance](GUIDANCE.json), [runner](run.py), model pin and preservation receipt were hash-frozen in [FREEZE.json](FREEZE.json) before inference. [Author key checks](AUTHOR_KEY_CHECKS.json) use exact fractions for the variance/reset answers.
- [Raw outputs](RAW_OUTPUTS.jsonl), [stdout](RUN.log), [stderr](RUN.stderr), and [manifest](RUN_MANIFEST.json) were frozen after completion and before systematic scoring. Partial output was inspected for progress updates; this was not a blinded review. Stderr contains a dtype deprecation warning, not a failed run. No prompt, key, or token cap was changed after observing outputs.

## The eight records and their frozen answers

All grouping records have 64 total observations, mean propensity .2, between-soil variance .032, and average conditional emission variance .128. Their target is the population-average estimator, with supplied formula `variance=.032/k+.128/64`. The supplied iid criterion requires a fresh independent soil for each observation. Unknown grouping leaves the required k undetermined.

| Record | What changes in the source | Reading key | Calculation key | Conclusion key |
|---|---|---|---|---|
| G1 | 64 fresh soils, one observation each | k=64 | .0025 | iid justified: YES |
| G2 | 4 fresh soils, sixteen observations each | k=4 | .0100 | iid justified: NO |
| G3 | 1 fresh soil, sixty-four observations | k=1 | .0340 | iid justified: NO |
| G4 | Grouping not recorded | UNKNOWN | UNKNOWN | iid justified: UNKNOWN |

All reset records use the earlier exact no-cross-effect model: `D0=.160`, `DA=D0*(1-pi*qA)`, `DS=D0*(1-(1-pi)*qS)`, with pi and unspecified efficacies in [0,1]. pi is a fraction of runs assigned an internal carrier, not memory bits inside one agent. The quantities describe the next observation conditioned on an observed first error, followed by a reset; they do not describe forcing the first error with do().

| Record | Readouts DA,DS | Supplied efficacies | Reading key | Compatible pi interval | Point identified? |
|---|---|---|---|---|---|
| R1 | .128,.088 | qA=.50,qS=.75 | PROVIDED | [.40,.40] | YES |
| R2 | .128,.088 | Neither supplied | MISSING | [.20,.55] | NO |
| R3 | .160,.160 | qA=0,qS=0 | PROVIDED | [0,1] | NO |
| R4 | .096,.064 | Neither supplied | MISSING | [.40,.40] | YES |

R4 is an essential negative case for an overbroad abstention rule. Under this model, missing efficacy values do not necessarily prevent point identification: the observed attenuations force a singleton feasible set. Provided efficacies can conversely be completely uninformative when both are zero.

## Results, without merging the obligations

| Elicited facet | Semantic matches | Explicitly wrong | Unresolved/truncated before an answer |
|---|---:|---:|---:|
| Source reading | 2/8 | 3/8 | 3/8 |
| Calculation / set reconstruction | 0/8 | 8/8 | 0/8 |
| Conclusion | 2/8 | 6/8 | 0/8 |
| Total | 4/24 | 17/24 | 3/24 |

[Scores](SCORES.json) retain the full response, expected answer, and coordinator rationale for every judgment. [Summary](SUMMARY.json) provides totals, per-record facets and costs. Semantic scoring considered the whole response and accepted sentences or case variants when their meaning was clear. A correct answer with additional materially false relevant claims would not receive a warranted-match mark; the four matching responses contain no such additions. This observable match does not certify an internal reasoning process.

The four matches were G1's conclusion, R1's reading answer, R2's conclusion, and R3's reading answer. Every other record/facet combination failed or remained unresolved. A three-of-three record would still have represented three separate prompted answers, not one coherent generated report or a demonstrated internal pipeline; here there were zero such records.

### Source reading

G1/G2/G3 reading calls copied the same source prefix and stopped at 64 tokens, before giving an independent-soil count. Mentioning “64 observations” in copied source text is not an explicit k answer. We mark these unresolved rather than assuming what a longer continuation would have said. More output budget was not tested.

G4 explicitly answered `The number of independent soil draws k is 64.` That converts the observed sample count into an invented independent-condition count. The record says grouping was unrecorded.

All four reset-reading responses asserted that both numerical effectiveness values were provided. This yields two correct answers on R1/R3 and two false source claims on R2/R4. The repeated affirmative answer is not evidence of reliable calibration-status recognition.

### Calculation and target roles

For G1 the model wrote:

`0.032/64 + 0.128/64 = 0.045/64 = 0.00025.`

The correct variance is .0025; the displayed equalities are false. G2 additionally moved the denominators across the supplied roles, ending at .00068 rather than .0100. G3 repeated G1's wrong result instead of retaining the one-soil variance .0340. G4 gave a numerical variance despite the missing grouping fact. These observations establish visible answer/arithmetic defects, not their neural cause.

R1's interval response repeatedly named `.50` and `.75` as pi values: those are the supplied effectiveness values. R2 and R4 instead copied readout values as pi bounds, with the purported lower endpoint larger than the upper endpoint. R3 repeated `pi=0.00` instead of returning the full [0,1] set.

Thus correct arithmetic over typed inputs remains a separate obligation from selecting the right quantity and recognizing when only a set is identified. Our exact numerical experiment did not teach those obligations to this model.

### Conclusions and format

All four grouping conclusions were `Yes`, yielding only the G1 match. The reset conclusions were `No, No, Yes, No`, matching only R2. R2's correct non-identification label coexisted with a false calibration-reading claim and a wrong feasible interval in the other two independent calls. It is a correct label, not evidence of the intended reasoning path.

Nineteen calls reached EOS; five hit the cap. Three capped reading calls lacked an answer; the other two capped calls already asserted wrong pi values before repeating. Exact requested output format was 0/24. A case-insensitive format-only sensitivity gives 8/24, because the eight conclusion calls returned only `Yes` or `No` instead of uppercase labels. Semantic scoring already accepts those case variants. Format failure alone therefore does not explain the poor semantic results, and capitalization is not treated as a reasoning error.

## Costs and state preservation

The 24 calls consumed 5,932 input tokens and 735 emitted tokens, with 70.5673 seconds of measured inference excluding serialization/model loading. Model load was 1.3695 seconds; cache serialization totaled .5653 seconds. These are observed local timings, not a service-speed or billing guarantee. No separately paid API or resource was invoked.

Twenty-four new terminal cache files totaling 306,227,568 bytes are retained under `/workspace/smollm_soil_reader_states_v1`. Every file's byte hash, sequence dimension, cached-prefix token hash and full generated token sequence was checked. The final emitted token is not necessarily forwarded into cache; token counts and reconstruction information preserve that boundary. Binary caches remain local; hashes, token IDs and the model pin are recorded here for reconstruction. Workspace persistence is not a durability guarantee, and this does not give access to the main assistant's hidden state or improve this chat's storage.

[Post-generation preservation](PRESERVATION_AFTER_GENERATION.json) verifies all 2,580 earlier FRR files and 216 recorded model/old-cache files unchanged before integration. Historical model branches were not reset, deleted or overwritten. The later optional documentation edits are separately archived. [Final checks](FINAL_CHECKS.json) record their allowlist and preservation scope.

## Refinement adopted, and what was not repaired

The optional [verification guidance](../../modules/verification-layer.md) and [design-label example](../../examples/soil-design-and-reset-calibration.md) now explicitly distinguish an appropriate mathematical diagnostic from a reader that can use it. Preserve observed number roles and source-missing facts, check the arithmetic separately, and keep compatible sets distinct from point answers. Correct labels from separate prompts do not certify a joined reasoning path. A cap-ended source echo remains an unfinished readout, not a source-supported extraction.

This is a reporting/workflow refinement. It is not a demonstrated behavioral repair, a new prompt default, a statistical/causal validator, or a reason to impose resets. The field-role guard and threshold comparator remain unchanged and are outside this source language. No repair to the earlier valid toy mathematics was needed. Core/runtime/schema and queue statuses are unchanged; no claim of broad FRR benefit or harm is drawn.

Seven previous navigation/guidance files are byte-archived in [ARCHIVE_RECEIPT.json](ARCHIVE_RECEIPT.json). Their moved relative links keep the original bases; use the original paths at the parent commit for historical navigation. All earlier raw results, source originals, failed predictions and numerical programs remain unchanged.

## Strongest next

Test the prerequisite more narrowly: use matched questions on the full source versus an explicitly selected relevant source clause, beginning with the soil count and whether effectiveness values are actually present. Freeze the clause selection and keys before generation. Keep selection cost and answer correctness visible; do not call supplied clauses autonomous source discovery. If reading improves, arithmetic can be delegated to an explicit calculator under validated input roles; if reading still fails, more sophisticated control algebra is premature for this model/prompt.

No broad conclusion about long-run capability follows from 24 authored calls, one small model, one cap and one prompt style. The next contact remains proposed; no background job is running. Coordinator semantic review and saved-data checks were not independent or masked agent review.
