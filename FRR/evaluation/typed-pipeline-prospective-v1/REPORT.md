# TP-C1: prospective pipeline contact exposes a source-role failure

29 October 2026, America/Chicago. User reported about40% allowance and authorized one bounded next experiment. We cannot inspect their account allowance. Completed21fresh CPU-model calls, a prospectively fixed two-extraction pipeline, independent scoring and saved-data review. No paidAPI, weight training, prompt tuning or extra semantic retries.

## Outcome first

The pipeline matches4of7task labels, versus2of7direct answers, but an always-UNKNOWN baseline also matches4of7. None of the seven pipeline results meets the full source-and-reason warrant contract. This is a failed pipeline contact, not evidence of improvement.

The concrete failure is at our adapter boundary: it accepts numbers from copied source paragraphs without retaining their field roles. A requirement number becomes a purported measurement. Natural-language absence is lost unless the literal MISSING token appears. Valid arithmetic over those misrepresented inputs can produce a plausible-looking but unjustified conflict/UNKNOWN.

All seven measurement continuations hit the96-token cap while repeating source/question material. A human role-aware reading still finds all distinct source observation claims in them; this is not seven compliant or complete extraction outputs. Formatting, content retention, field interpretation and a warranted task result are different endpoints.

## Prospective design

[Design](DESIGN.md), [cases](CASES.json), [records](RECORDS.json), [taskpolicy](TASK_POLICY.json), [scoringcontract](SCORING_CONTRACT.md), [pipeline design](DESIGN_PIPELINE.md), [code](pipeline.py), [pre-generation freeze](FREEZE.json), [ready-to-run checkpoint](READY_TO_RUN.md).

Seven new authored records cover absence, below threshold, equality, above threshold, crossing conflicting measurements, different measurements both above threshold, and simultaneous absence/measured reports. All prompts specify a task policy: one consistent reported measurement is required; no report has priority and no aggregation is permitted. Same-side disagreement is UNKNOWN **because of that declared policy**, not because threshold membership is mathematically unknowable when both possible values exceed the minimum. This is a contract choice, not a universal conflict rule.

Each record has three independent queries: directYES/NO/UNKNOWN, extract the minimum, list every observation including MISSING where explicitly absent. The two generated extraction responses enter the fixed pipeline. Original numerical facts and evaluator grades never choose, repair or gate its action. Entity/unit/runassociation are supplied question context, not generated proof of ownership. Full statements/examples were not added after outcomes. The pipeline, parser, checker hash, tests, prompts, keys and scoring definitions were frozen before firstgeneration.

Pinned SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac; CPUfloat32/eagerattention/twothreads, greedy96newtoken cap. One run,21branches, no training or model/pipeline rerun. This contact contains seven records; the preceding CD-C1 had eight. Inputs are authored/exposed development cases, not a held-out population. Different query forms/lengths and two extraction calls versus one direct call preclude equal-budget causal efficacy claims.

## Primary responses

| Query family | Semantic field/answer matches | Full response warrant | Strict requested format | Token-limit stops |
|---|---:|---:|---:|---:|
|Direct|2/7|2/7|0/7|0/7|
|Minimum|5/7|5/7|0/7|0/7|
|Measurements|7/7|5/7|0/7|7/7|

All direct answers affirm passing, including four records whose policy requiresUNKNOWN and one below-threshold record. Five minimum outputs match the required field; the other two report the measurement instead. Every measurement output repeats source content rather than returning the requested field-only list. All required distinct observation states/values occur with intelligible roles in each output, but two outputs invent NoteB/NoteC identifiers for sources containing onlyNoteA. Those extra provenance claims invalidate their full response warrant even though the observation-value set is retained. A cap does not mechanically make every retained fact false; a retained fact does not establish completion or instruction compliance.

This role-aware scoring intentionally differs from the pipeline's number harvesting: a criterion explicitly described as a criterion is not a human-coded measurement just because its number appears. All raw text and failed states remain available in [rawoutputs](RAW_OUTPUTS.jsonl).

Root initial deposits froze before another agent received shuffled source/question/gold/output packets. Query role remains visible; ID/order-masked, not family-blind. [189field comparisons](REVIEW_COMPARISON.json) agree after freezing both initial deposits. Observation-list ordering is ignored as the contract specifies; initial files are not rewritten. [Maskedreview](review/MASKED_REVIEW.md). Separate agent judgment is not independent model/scientific replication.

## Prospective pipeline results

The fixed [action runner](compute_actions.py) calls the surface parser and unchanged exact [threshold checker](../../tools/evidence_threshold.py), saves generated structured claims, and freezes [actions](PIPELINE_ACTIONS.json) before scoring source agreement. Twelve pipeline test methods pass; they establish the declared syntax/conditional computation, not natural-language understanding.

| Record | Actual source state | Direct | Pipeline | Gold | Pipeline issue |
|---|---|---|---|---|---|
|P1|No measurement; minimum8kg|YES|YES|UNKNOWN|Requirement8treated as measurement; natural absence lost|
|P2|6kg; minimum10kg|YES|UNKNOWN|NO|Wrong generated minimum6; criterion10also harvested as measurement|
|P3|12cm; minimum12cm|YES|YES|YES|Numeric fields agree, but raw output invents source-note identifiers|
|P4|9cm; minimum7cm|YES|UNKNOWN|YES|Wrong generated minimum9; criterion7also harvested|
|P5|6and11cm; minimum9cm|YES|UNKNOWN|UNKNOWN|Criterion9added to actual conflicting values|
|P6|10and12cm; minimum8cm|YES|UNKNOWN|UNKNOWN|Criterion8added; original same-sideconflict already requiresUNKNOWN|
|P7|Missing and7kg; minimum5kg|YES|UNKNOWN|UNKNOWN|Missing state lost, criterion5added; a different conflict produces the same label|

All seven pairs are syntactically usable under the permissive surface parser: no extraction_unusable fallback occurs. Two reach compared, five reach conflicting_measurements; none reaches missing_measurement. Thus the failures here are not simply parser rejection. All five typed conflict receipts describe the generated structured claims, not a validated interpretation of the original source.

OnlyP3has matching distinct parsed observation/minimum values and a correct conditional numeric reason. Its additional invented raw source-note claims prevent full source warrant. With raw provenance assertions included, reason_warranted and fully_warranted are both0/7. Report the intermediate numeric agreement as1/7 rather than hiding it. The four matched pipeline labels do not establish that missingness/conflict was correctly recognized.

Direct bare-label warrant has a weaker observable basis than auditing the pipeline's intermediate facts and reasons. These warrant counts therefore cannot by themselves establish a fair causal superiority/inferiority ranking. Label baselines are alwaysYES2/7, alwaysNO1/7, alwaysUNKNOWN4/7. [Allmetrics/parsed-source diagnostics](SUMMARY.json), [independent saved-data audit](review/PIPELINE_AUDIT.md).

## Costs and execution limits

Direct:1,320input/92outputtokens and10.56seconds measured inference. The two extraction calls:2,689input/766outputtokens and63.07seconds. Totals:4,009input/858generatedtokens,73.63seconds inference excluding load/serialization. These are workload observations, not dollar/energy costs or controlled speed comparisons. Checker execution was not separately timed; this is a measurement omission, so inference sums are not end-to-end walltime. Fourteen calls stop atEOS; seven measurement calls stop at cap. We did not increase the cap or reword prompts after seeing repetition.

A brief executor transport interruption occurred after generation/actions. Readback established the reviewer's initial deposit had actually completed despite its write error; it was not blindly repeated or overwritten. No scientific/model run was repeated. [Operationalnote](EXECUTOR_NOTE.md).

## What we adopt and what stays experimental

The existing exact typed checker remains useful on explicitly supplied structured facts. Its code/core behavior is unchanged. The permissive study parser/pipeline is **not promoted** into a default or a trusted extractor. The current [worked guidance](../../examples/typed-threshold-inference.md) adds the observed failure: do not harvest every number from copied context into measurement fields; preserve and verify field roles. Original guidance bytes are archived before this narrow addition.

Our prior source scout's separation of language extraction, syntax, computation and task acceptance is now operationally relevant: a program can satisfy its own input schema while the transformation into that schema has lost meaning. This is a concrete saved-input/readout failure, not proof of a universal reasoning mechanism or general FRR benefit. Merely broadening parser acceptance is not a justified repair. Raising the cap or imposing JSON could change behavior, but neither is validated here as a semantic fix.

Strongest next proposed: a separately frozen field-binding/format control that rejects copied context as a field response, exposes withholding reasons, and checks coverage as well as false support. Keep caller-vetted structured facts distinct from model-generated claims. Use fresh records or independently sourced revision material and count acquisition/validation costs. Do not turn an UNKNOWN caused by an infrastructure limitation into a claim that source uncertainty was understood. No further run is launched automatically.

## Preservation

2561priorfiles were verified unchanged after generation/actions, before intended navigation/guidanceupdates. All21newterminal cache artifacts are preserved locally with hashes, token sequences and cached-token counts. Last generated token forwarding scope is explicit. Text/manifests are published; binarycache durability is not guaranteed. Prior weights/states/results/failures remain unchanged. Original navigation and workedguidance are byte-archived with original paths; moved archive relative links retain their old bases. Core/runtime/schema and queue statuses remain unchanged. No background model task remains at delivery.

[Final independent review](review/FINAL_REVIEW.md) found no blocking correction. [Final scoped integrity/link/structure checks](FINAL_CHECKS.json) preserve the scientific artifacts and historical files; they do not change the failed-pipeline verdict.
