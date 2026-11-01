# More output allowance, worked examples, and the next-action gap

1 November 2026 UTC. Completed fixed-reader comparison and an outcome-informed example-order check. No model training or default-policy adoption.

We opened two different kinds of support: a longer response allowance and six worked action examples. The response-cap comparison did not change any decisions: the immediate replies stopped before exhausting eight tokens. Asking for a brief public plan changed response format, but produced no preamble before a final action tag. Worked examples introduced many UNKNOWN answers, including warranted unavailable-evidence cases, while also deferring many cases with accessible evidence. Rotating those same examples made UNKNOWN disappear whenever its example moved away from the final position in this small diagnostic.

A meaningful part of the apparent planning failure was an interface mismatch: the model often said “Report insufficient evidence” instead of the literal command UNKNOWN. The formal decoder result and a separate semantic readback are both preserved. Neither valid syntax nor a recognizable uncertainty phrase alone establishes a reliable evidence-seeking policy.

## Factorial comparison

Same saved canonical reader, three response settings crossed with no examples versus six fixed examples. Direct8 and direct64 have identical prompts; only the maximum output count changes. Plan64 asks for one brief public action plan and a final ACTION:word. Examples are context demonstrations, not weight updates. They teach three visible status answers, TARGET for unavailable/wrong-target visible evidence when archive access exists, and UNKNOWN without source/access. FULL remains allowed but is not demonstrated as the preferred request.

| Examples | Response setting | Grounded answers /48 | Justified source-unknown /48 | Formal task terminals /48 | Requests | Deferrals with accessible evidence |
|---|---|---:|---:|---:|---:|---:|
| none | direct8 | 8 | 0 | 8 | 0 | 0 |
| none | direct64 | 8 | 0 | 8 | 0 | 0 |
| none | plan64 | 0 | 0 | 0 | 0 | 0 |
| examples | direct8 | 6 | 12 | 18 | 0 | 22 |
| examples | direct64 | 6 | 12 | 18 | 0 | 22 |
| examples | plan64 | 6 | 0 | 6 | 2 | 0 |

These are 48 logical source scenarios per cell, driven by 16 distinct visible observations. Hidden worlds with the same observation reuse one actual router response per condition. Do not treat those replays as independent samples. Formal task terminals mean a source-supported correct answer or warranted unknown under this toy’s access assumptions, not universal correctness. UNKNOWN with accessible evidence is reported as a deferral, not proof of dishonesty or of calibrated model confidence.

All 32 short/long identical-prompt pairs share the same generated prefix. More strongly, the direct8/direct64 final actions are identical and every immediate reply stops by EOS before its cap. The extra allowance was unused; this cannot show that productive extended deliberation would be useless.

Without examples, the plan request yields no recognized command under the frozen parser. With examples, it yields fifteen YES actions and one TARGET among sixteen distinct observations; none includes text before a final action tag. There is no observed public plan to evaluate as useful or harmful reasoning. We tested an instruction/allowance package, not hidden thinking time. Valid action tags may be copied formatting rather than evidence of a plan.

The single TARGET tag leads to two logical retrievals on repeated record-order variants of one bracket-format zero record. The target was already visible, and the tool returned a canonical representation which the worker read correctly. This could serve reformatting for a limited reader, but does not establish recognizing a missing-source condition. The raw response continues with “Example 7” and repeats the current task, so pattern continuation is a live rival explanation. [Raw router outputs](run/ROUTER_RAW.jsonl) retain that continuation.

## A description is not the same as an accepted API command

Fifteen of sixteen no-example/plan-setting responses literally say `ACTION: Report insufficient evidence`; the remaining response says `ACTION: Report Sufficient Evidence`. The strict action parser rejects both because neither names an allowed action word after the tag. Calling all sixteen simply ‘no uncertainty’ would lose useful information.

The post-run [semantic readback](SEMANTIC_READBACK.json) maps only the exact insufficient-evidence description to UNKNOWN, while deliberately leaving the opposite sufficient-evidence phrase unmapped. It affects 46 logical replays of those 15 actual responses: 12 would be warranted source-unknown terminals and 34 would defer despite accessible evidence. This is an interpretation diagnostic, not a changed primary score or a new executed policy. No model/tool calls were added and no general semantic decoder was adopted.

The distinction matters for the wider harness: a rejected command can carry recognizable meaning. Conversely, a recognizable uncertainty phrase can be insensitive to the actual evidence. A future interface should declare supported aliases prospectively, include polarity/negation countertests, and then measure actual routing. Do not silently convert every free-text reply into the action the evaluator wanted.

## Same examples, different order

After observing many UNKNOWN replies, a separately frozen follow-up holds the current task/menu/instructions fixed and cyclically rotates the six entire worked-example blocks. Each block retains its number and all facts/labels. Four exposed line-format observations cross six rotations: 24 actual router probes. Correctness and request outcomes are kept; identical measured worker responses would be reused explicitly if a request occurred.

| Last worked-example action | Rotation | Outputs across four observations | Formal task terminals /4 |
|---|---:|---|---:|
| UNKNOWN | 0 | {'UNKNOWN': 3, 'YES': 1} | 2 |
| YES | 1 | {'NO': 1, 'YES': 3} | 1 |
| NO | 2 | {'NO': 3, 'YES': 1} | 1 |
| WITHHOLD | 3 | {'NO': 3, 'YES': 1} | 1 |
| TARGET | 4 | {'NO': 3, 'YES': 1} | 1 |
| TARGET | 5 | {'NO': 3, 'YES': 1} | 1 |

UNKNOWN appears three times with the original order, where its example is last, and zero times under the other five rotations. There is no general “copy the last action” rule: last-example matches are only 9/24, TARGET is never selected even when last, and WITHHOLD does not appear when last. The result supports an order/context interaction with familiar answer vocabulary, not a unique neural recency mechanism or robust conditional learning. The attached example numbers and restricted cyclic permutations remain possible contributors.

All four rotation-zero prompts exactly reproduce their earlier input/output token sequences. This is a controlled replay on exposed observations, not independent replication or fresh primary validation. [Follow-up protocol](example-order-check/PROTOCOL.md), [raw](example-order-check/run/RAW.jsonl), [summary](example-order-check/run/SUMMARY.json), [checks](example-order-check/CHECKS.json).

## Environment and comparators

The primary source worlds cross three statuses, both record orders, four observation/access kinds and two name/visible-format packages: line-format target Juniper and bracket-format target Hemlock. Lesson names Iris/Moss are absent from test sources. Format and target identity are coupled, so they cannot be separately attributed. The bracket syntax is not demonstrated in the lesson. A fixed non-cyclic menu is held constant; broader layout generalization is untested.

Every chosen action executes, including errors and unavailable requests. The router sees only displayed evidence, target name and archive availability; hidden state/source keys do not enter its prompt. A narrow external parser normalizes the two declared visible-record grammars for comparison/source receipts; the model sees the original display. Source receipts are conditional on the authored literal source, not authentication or external-world truth.

Four mechanical comparators run regardless of router failure. The observed-input rule gives 36 grounded answers plus 12 justified unknowns out of 48, with 24 nominal query units and no unavailable requests. Always TARGET also resolves all 48 but costs 48 units and attempts 12 unavailable requests. Always FULL produces 18 grounded answers plus 12 justified unknowns, costing 96 units; the fixed worker still struggles with two-record context. Always UNKNOWN defers all 36 cases with accessible evidence. Tool-unavailable UNKNOWN remains different from model-chosen UNKNOWN. No universal utility scalar is imposed.

## Execution, checks and error history

[Protocol](PROTOCOL.md), [freeze](FREEZE.json), [sources](DATA.json), [queries](QUERIES.json), [links](LINKS.json), [raw](run/ROUTER_RAW.jsonl), [actual worker probes](run/WORKER_RAW.jsonl), [executed routes](run/ROUTES.jsonl), [summary](run/SUMMARY.json), [checks](CHECKS.json), [final audit](FINAL_CHECKS.json). Six focused tests pass. All frozen/checkpoint hashes, prompt tokenization, decoded outputs, action extraction, source normalization, tool traces and exact cache reuse verify. The source-state field is audited against literal source parsing; the observed rule reads the shown record, not a hidden key.

Primary: 96 actual router generations plus 18 worker generations; no candidate-scoring passes. Router input/output tokens: 26642/400; worker input/output: 1668/60. Generation time 81.780 seconds excludes model loading/calibration/other work. Maximum prompt390tokens, no truncation; last-logit head calibrated against the full head on six explicit-action inputs (12prefill forwards), same argmax and max error<=1e-4. This is a scoped numerical check, not a global equivalence proof or a new production optimization.

Follow-up: 24 router generations, no new worker generations, 9156/62 input/output tokens and 21.418 generation seconds. Overall138actual generation probes and504executed logical routes;102distinct prompt strings, reused router decisions/worker responses explicit. Semantic readback is counterfactual and excluded from executed-route totals. Sampled main maximum working estimate1962700800bytes/RSS932941824bytes; these are phase samples, not continuous peaks or financial costs.

Preparation initially used system Python for a helper importing PyTorch; it failed before any model load/forward. The subsequent missing-freeze run also stopped before model load; original logs remain under [preparation-failure](preparation-failure/NOTE.md). The corrected invocation uses the existing model venv. A later file-only interpretation audit hit the same import dependency; that unfrozen audit helper was corrected to standard-library hashing/JSON I/O and now runs without PyTorch. [Audit dependency note](preparation-failure/AUDIT_INTERPRETER_NOTE.md). Experimental code and results were not altered to hide these failures. No packages were installed.

Original base/adapter and 3,638 earlier local files were unchanged before navigation sync. Existing model snapshot remains the earlier local 12.8 MB capsule; no new model binaries, weight training, paid APIs, rentals, downloads or restore claims. Full KV tensors are not retained here. No independent empirical replication, FRR/no-FRR advantage, self-awareness, linear-thinking or physical-law claim. These are one fixed small reader and coordinator-authored toy fixtures.

## Confident next directions, still unexecuted

First separate recognizable language from an executable interface: prospectively allow exact offered action descriptions with polarity countertests, keeping strict and permissive results distinct. Then compare a short explicit conditional rule with worked demonstrations under counterbalanced example order and fresh observations. Check state recognition and actual end-to-end routes together; a poor intermediate result need not stop a separate failure/repair branch.

Longer output allowance remains different from generating or using a public plan; this model stopped early or imitated output patterns. Alternative planning/interaction scaffolds can be tested without claiming this run disproves their value. Matched-length neighbor controls and broader writer-handoff/source-revision work remain open. No default controller, generic decoder or core/schema change follows from this contact.
