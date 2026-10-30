# CD-C1: extraction, comparison and a useful inference boundary

29 October 2026, America/Chicago. The user authorized the next experiment and parallel inference scouting/integration. Completed: one frozen 40-generation diagnostic, a retrospective saved-response composition, three primary-source contacts, and an optional exact threshold instrument linked into FRR's verification guidance. No training, paid model API, GPU rental or prompt-default promotion.

## What we learned

The little model can return the correct value for every present measurement in this narrow task, yet says YES to both an inclusive-pass question and its below-minimum inverse. It substitutes the requirement for both absent measurements, and once substitutes a measurement for the requirement. Neutral labels obey the output form but always say MISSING, including measured records.

This separates observable extraction, formatting, source-field binding and comparison behavior. It does not identify an internal reasoning circuit, prove that the model used a correct representation, or establish a general incapacity. Independently prompted tasks are not an observed internal causal pipeline.

The useful engineering extraction is **source/field check → typed validation → exact computation → task acceptance**. The new instrument implements only the structured validation/computation boundary. A correct-looking computed label can still be unwarranted if its input fact is wrong.

## Frozen primary experiment

[Design](DESIGN.md), [records](RECORDS.json), [40 queries and keys](CASES.json), [scoring contract](SCORING_CONTRACT.md), [prospective review](review/PROSPECTIVE.md), [freeze](FREEZE.json), [runner](run.py).

Eight authored records use two templates:

- Cobalt Prism: minimum 11 cm; measurement absent, 7, 11, or 14 cm.
- Bronze Bag: minimum 6 kg; measurement absent, 4, 6, or 9 kg.

Five independent queries accompany each record: extract the measurement (or MISSING); extract the minimum; ask whether measurement is at least minimum; ask whether it is strictly below minimum; classify BELOW/AT_OR_ABOVE/MISSING. All requests ask for only the value/label without explanation. Each gets a fresh context with the original record; no generated extraction is supplied to a later model query. Query order rotates within records as bookkeeping. Questions differ in wording, answer vocabulary and input length; this is not an information/token-matched instruction comparison.

The unchanged pinned SmolLM2-135M-Instruct checkpoint runs locally on CPU, float32/eager attention, two threads, greedy generation with a 96-new-token cap. Revision: `12fd25f77366fa6b3b4b768ec3050bf629380bac`. All 40 answers stop at EOS; no semantic retry, tuning or weight update. Gold is evaluator metadata, not an inserted answer; actual supplied facts legitimately determine it. These are exposed authored development inputs, not held-out generalization or 40 independent models. Equality is tested explicitly. Combined pass/inverse directions balance; each family separately does not.

## Primary outcomes

| Query family | Semantic matches | Fully warranted under contract | Strict requested format | Wrong-field assertions |
|---|---:|---:|---:|---:|
| Measurement | 6/8 | 6/8 | 0/8 | 2/8 |
| Minimum | 7/8 | 7/8 | 0/8 | 1/8 |
| At least minimum? | 4/8 | 4/8 | 8/8 | 0/8 |
| Below minimum? | 2/8 | 2/8 | 8/8 | 0/8 |
| Neutral classification | 2/8 | 2/8 | 8/8 | 0/8 |

The extraction sentences include extra words, so none meets the literal number+unit-only format. Their semantic extraction score is evaluated separately. Conversely, all 24 classification responses obey the requested vocabulary but only eight are correct. Valid syntax is not sufficient for the requested conclusion.

All six present measurements are extracted correctly. For C1/C5, the absent measurement is incorrectly reported as 11 cm/6 kg, matching the requirement field. For C8, the model reports the minimum as 9 kg, actually its measurement; the supplied minimum is 6 kg. These are three material factual/field errors. Returning the shared number at equality cannot distinguish which equal-valued field was accessed, so no source-access proof is inferred there.

All eight pass answers and all eight inverse answers are YES. Thus none of the eight pairs is correct or complementary under its actual evidence state. Direct gold has four YES, two NO, two UNKNOWN; inverse has two YES, four NO, two UNKNOWN. Always-YES baselines are accordingly 4/8 and 2/8, not a balanced three-way baseline. All neutral outputs are MISSING: correct only on the two absent-measurement records. This does not establish calibrated abstention or recognition of missing evidence.

Five records have both extracted fields warranted by the source. On those independently prompted records, direct pass is correct on three and inverse on two. That is a behavioral disparity across prompts, not causal localization inside the model. The contract's “fully warranted” means keyed task agreement with no material false additional claim; a bare correct label does not certify an internally correct derivation.

[All five outputs per record and costs](SUMMARY.json), [raw prompts/generated-only continuations/tokens/cache manifests](RAW_OUTPUTS.jsonl). Total: 5,456 input and 255 generated tokens; measured forward/generation time about 34.24 seconds, excluding loading and serialization. Workloads are not dollar cost, energy, controlled speed comparisons or a remaining-compute allowance.

## Separate scoring judgment

Root read all outputs, deposited and froze initial scores before providing another agent shuffled question/record/gold/output packets. Query type is visible from wording: ID/order-masked, not family-blind. The reviewer did not inspect raw logs, root scores or the mapping while coding. Both deposits were frozen before comparison. [400 field comparisons](REVIEW_COMPARISON.json) agree, with no reconciliation. [Masked review](review/MASKED_REVIEW.md), [review freeze](REVIEW_FREEZE.json). Shared-filesystem masking is instructional; another agent's judgment is not independent scientific/model replication.

## Retrospective composition: computation helps only where its inputs hold

After primary outputs were observed, we specified and froze a separate [saved-response replay](REPLAY_DESIGN.md). [Code](replay_extractions.py), [freeze](REPLAY_FREEZE.json), [results](REPLAY_RESULTS.json), [independent audit](review/REPLAY_REVIEW.md).

It parses one number+literal unit from each generated measurement/minimum response (or exact MISSING), then applies the new typed comparator. Caller question context supplies entity/unit/run association; **both numeric fields come from the generated text**. No gold value, correctness flag or missing-state repair chooses the action. Original facts and the frozen extraction-warrant scores are used only afterward for evaluation.

The eight composed results match task labels on 6/8, versus 4/8 for direct pass; only 5/8 are fully warranted, versus 4/8 direct. Two below-threshold cases become correct NO using correctly extracted fields. Both absent measurements remain wrong YES because their invented values survive. C8 yields a correct YES from the wrong generated minimum 9 kg: exact computation does not make that basis valid.

This uses two extraction prompts versus one direct prompt: 2,048 input/191 output tokens and 19.43 seconds of already-counted primary inference, versus 1,080 input/16 output tokens and 4.30 seconds for direct pass. No new model generation occurred. This is a post-hoc saved-response construction, not a prospectively generated pipeline arm, equal-budget causal benefit, learned improvement or basis for promotion. All eight records remain in the denominator; no parse rejection happened on these particular strings. A prospective parser/pipeline comparison on fresh records remains open.

### Peer-found parser boundary and append-only repair

The frozen replay parser accepts `-1 cm` as positive 1, despite its intended nonnegative-integer scope. This counterexample was found outside the eight actual positive-integer response pairs. The original frozen parser, eight computed outcomes and receipts are retained unchanged. An appended [parser correction](REPLAY_PARSER_CORRECTION.md), repaired parser and regressions expose the issue and verify that the actual sixteen extraction strings retain their parsed values. Do not describe the original run as having executed under repaired code. No general natural-language interpretation, negation handling or source authentication follows from either surface parser.

## Inference scout → concrete optional integration

[Three-source primary scout](review/INFERENCE_SCOUT.md):

- [PAL, ICML 2023](https://proceedings.mlr.press/v202/gao23f/gao23f.pdf): separate language compilation from interpreter computation. Different larger/code-capable models; no claim our 135M can generate reliable programs.
- [Grammar-Aligned Decoding](https://arxiv.org/html/2405.21047v1): output syntax and globally conditioned distribution are distinct; neither alone ensures task correctness. No ASAp/constrained decoder was implemented here.
- [Language Models (Mostly) Know What They Know](https://arxiv.org/html/2207.05221v4): uncertainty elicitation depends on model/task/prompting; P(IK) is a finetuned experiment, not an automatic inference-only capability. No calibrated confidence gate is adopted for our 135M model.

These are selected primary-section readings, not full-paper/code replications. The supported practical adoption is deliberately smaller: [evidence_threshold.py](../../tools/evidence_threshold.py), linked from the [optional verification module](../../modules/verification-layer.md), with [working command/example](../../examples/typed-threshold-inference.md).

The helper checks exact schema, bound evidence bytes, literal entity/scope/unit, finite decimal inputs and an explicitly named `at_least` criterion, then compares exactly. Equality/negatives work; booleans, binary floats, nonfinite/exponent inputs and implicit unit conversion are unsupported. Conflicting values remain unresolved even if they would imply the same label; no aggregation/precedence is invented. Repeated equal observations do not become independent evidence. Receipt stages distinguish invalid contract/evidence, inaccessible file, hash/identity mismatch, no supplied observations, explicit missing measurement, conflict and valid comparison. These support different repair routes instead of collapsing everything into failure or zero.

[19 test methods](test_evidence_threshold.py), including boundary/type/binding/path/JSON regressions, pass under builder, coordinator and [independent instrument review](review/INSTRUMENT_REVIEW.md). The first 17-test version and receipts remain archived; the refined version adds empty-versus-explicit-missing and deeply nested JSON handling. See [refinement receipt](THRESHOLD_REFINEMENT_RECEIPT.json). Curated instrument success is not model performance. This is a trusted-local-workspace utility, not a hardened arbitrary-input service or a truth/authenticity verifier. It reads structured claims; it cannot determine that they came from the right natural-language field.

## Preservation, current scope and next contacts

2439 prior files were checked unchanged after primary generation, before intentional navigation/guidance updates. All 40 new terminal cache artifacts are saved locally and hash-verified; last-token forwarding scope is recorded. Prior branches/weights/caches/deposits remain. Binary caches/weights are not uploaded; manifests preserve reconstruction information, not guaranteed workspace durability. Original navigation and verification guidance are byte-archived before update, with original-path/hash receipts. Relative links inside moved archives retain their original base; use their parent-commit paths. Core runtime 0.2, inquiry schema 0.1 and queue statuses are unchanged. Historical failures are not relabeled.

Strongest next proposed: prospectively test a typed extraction-plus-comparison workflow on separately frozen records, with source-field correctness, absent evidence and contradictory records kept explicit. Distinguish caller-vetted structured facts, model-extracted claims and the actual task's evidence. Count extraction/control costs; use independent source binding rather than an unchecked self-confidence threshold. Counterbalance phrasing/order or use independently sourced revision records to test whether the observed disparities transfer. External source contact remains legitimate now; another toy success is not a prerequisite.

The helper and worked guidance are available as optional infrastructure. Broad confidence gating, grammar-constrained generation, self-consistency, autonomous recursion or a universal FRR controller have not been installed or validated. All primary model outputs remain failures/successes as observed. No background model task remains at delivery.

[Final independent review](review/FINAL_REVIEW.md) found no blocking correction. [Final scoped checks](FINAL_CHECKS.json) verify preserved artifacts, archived replacements, usable links and structural consistency; they do not certify source truth or general efficacy.
