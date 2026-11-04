# Does the tool call follow the requested target or the example?

3 November 2026, America/Chicago client date. Completed separate diagnostic. Primary garden unchanged and paused at100.

## Motivation and scope

The user's proposal was to let space occupied by our descriptions of acting become usable room for activity and consequences, rather than add a literal canvas. Prior [action-room checks](../action-room-capability-checks-v1/REPORT.md) reduced prose without establishing reliable action gains: one valid initial calculator call copied the wrong syntax example, while three explicitly coached repairs worked. This next contact asks a prerequisite question: can the current model setup issue a real request bound to the requested expression when its visible example changes?

This is a controlled diagnostic, not a replacement for free exploration. Failure does not bar a garden continuation or require a reset, extra seed complexity or immediate training. Diagnostic replies never enter its primary history.

## Frozen design

32 calls: two contexts(clean notebook or frozen entry-100 context with the same recent12 visible), four target expressions, two sampling seeds, and two example relations. Targets are4+5=9,9-3=6,3*4=12,8/2=4. The matching example is the target itself; the different example is the next expression cyclically. Every expression is equally often a matching and a different example. Unique results help distinguish wrong-example execution from target execution. This balances demonstration identities across the set; it does not cover every possible target/example pairing or isolate operator-specific effects.

Use current scaffold only. Exactly one anchored current charter syntax example is replaced; task wording, tools, cards and history are otherwise constant. Matching-example success is an exact-copy positive control and does not establish transfer. In the carried context, historical2+3 strings remain unchanged: only the current example changes, so historical anchoring remains possible. The request always asks for calculator execution, not merely the numeric answer.

Same canonical cached135M+LoRA model, fixed weights, CPU float32 eager/two threads, temperature.8/top-p.9, input8096/output96. Fresh generation cache each call. RNGseed=seed*1000+target_index, shared across contexts/example relations. Each call independently starts from its frozen context; no online learning, retry, new seed material, paid API, download or installation. This is not a continuation or development experiment.

## Results

| Context / current example | Valid actual calculator request | Strict target success | Wrong-example execution | Cap stops |
|---|---:|---:|---:|---:|
| clean / matching | 0/8 | 0/8 | 0/8 | 0 |
| clean / different | 1/8 | 0/8 | 0/8 | 4 |
| carried / matching | 0/8 | 0/8 | 0/8 | 4 |
| carried / different | 0/8 | 0/8 | 0/8 | 5 |

Matching-example target successes: 0/16. Different-example target successes: 0/16. Wrong-example executions in different-example cases: 0/16. Same-target/seed/context pairs correct under BOTH examples: 0/16.

The single actual calculator invocation was `TRY 4 / 2`, yielding2, in clean_t3_2401_different. The requested target was8/2 and the current example was4+5: the execution matched neither. This is a concrete operand-binding failure, not proof that the example caused a hybrid operation. We did not observe a wrong-demo execution in this set, so the earlier wrong-example event does not justify a general example-copying explanation.

The first-seed packet also contains `4 + 5 = 9` and `3 * 4 = 12`: correct mathematical text that did not invoke a tool. Another output includes `TRY 3 * 4` buried in longer generated prose, which the unchanged full-response grammar does not execute. Thus the present observation is unreliable execution under the available contract, not that the model cannot ever represent the arithmetic. Some carried outputs repeat charter/record headings; no causal conclusion about history follows from that description.

Strict success requires a real host-dispatched calculation, AST binding to the requested target, and the correct host result. A bare number, expression without TRY, or generated receipt-looking text is not an executed request. Existing normalization allows whitespace, parentheses, integral float constants and commutative addition; this is not a universal symbolic-equivalence evaluator. Valid calculation and correct numeric value alone are reported separately from target binding. Matching and different results are descriptive small samples, not a statistical advantage claim.

Full per-target matched pairs are in [PAIRS](PAIRS.json); every scalar result is in [event index](EVENT_INDEX.json). The first sampling seed for all context/target/relation cells supplies a prespecified bounded [descriptive packet](REVIEW_SAMPLE.json). Additional indexed outputs may be inspected to substantiate a particular finding, without changing frozen scoring.

Total output 1538 tokens; 13/32 cap stops; maximum actual input 2204; generation 355.952s. Cap stops censor continuations. Small-model formatting difficulty and the retained canonical adapter are part of this setup; results do not establish a capability boundary for larger models, the base model without this adapter, or a trained tool-using model.

## Verification and preservation

Four preflight tests passed: target/demo discrimination using actual host dispatch, balance/unique case IDs, exact unchanged history with one-clause replacement, and matched-copy scoring scope. [CHECKS](CHECKS.json) verifies all32raw rows against frozen cases/prompts/tokenization/RNG/stops/dispatch/scoring, sampled resource limits, unchanged weight digests, and every pinned primary file. No result-dependent rerun, relaxed parser or dropped failure. These checks establish controller/record integrity, not model understanding.

Raw prompts, token IDs, complete outputs and real host results are saved in [run](run), with model run manifest and resource samples. Frozen [protocol](PROTOCOL.md), controller/dependency hashes, primary snapshot/state and original primary file hashes are retained. Prior current navigation files are archived in before/. Only this study and three navigation files are updated in publication; all earlier exploration files and primary state remain intact. No model job is left running.

## Interpretation and next direction

A successful matching call can come from copying the shown syntax. A different-example target call demonstrates narrow instruction binding for that expression and sampled context, but not autonomous intention, generalized repair or emergence. A wrong-example execution shows actual tool use with incorrect binding. Ordinary text failures leave open several explanations: output-format control, competing scaffold/history patterns, adapter specialization, sampling, or insufficient capability. This study does not identify which is causal.

No primary prompt change, training or automatic adoption follows from these32calls. The continuing garden is still at100 with its same routine.py, recent12/archive reader, charter and seeds. Free exploration and explicit tool competence remain different questions.

The strongest next diagnostic is a minimal stand-alone action interface compared with the existing scaffold, using multiple target expressions and an authentic worked tool receipt, with exact dispatch as criterion. Keep it separate from primary, hold response budget/model fixed, retain every failure and counterbalance examples. That would check whether usable action is available under more task-direct presentation before attributing non-use to freedom, seed complexity or history. If binding becomes dependable, a short fixed multi-turn consequence/revision contact can then examine feedback use. A longer primary continuation remains possible without requiring it to pass this diagnostic; any environment change should be explicit/versioned.

Garden reading: we are checking whether the small plant can use the gate rather than merely repeat its sign. The measured fruit gets its own label: actual execution, requested-target execution, or words only. All three stay in the record; none is silently promoted into growth.
