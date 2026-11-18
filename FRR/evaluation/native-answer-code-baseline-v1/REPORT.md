# Native plain-answer / code baseline: correct arithmetic content and an off-target file effect

17 November 2026, America/Chicago. Six new calls under one frozen protocol. No FRR, world observation or mechanics text is supplied to the model. The integrity audit passes. Exact requested outcomes fail in all six cases, while distinct partial abilities and actual effects are retained rather than discarded.

## Results

| Underlying task | Plain reply under minimal native framing | Code request without world packet | Exact task result |
|---|---|---|---|
| Literal word moss | Defines moss in a sentence | Closed cell actually writes `moss` into `/world/test.txt`; stdout empty | Both fail |
| Sum7+5 | `7 + 5 = 12.` | Closed cell requests keyboard input; EOFError, exit1 | Both fail |
| Ascending3,1,2 | Final sentence includes1,2,3, but preceding numbered list is inconsistent and response has extra text | Open Python fence with repeated newline replacements, output limit | Both fail |

Plain arithmetic contains the correct sum, so the preceding failures to emit arithmetic code cannot be treated as evidence of inability to produce that particular arithmetic fact. The plain reply still fails the prospective answer-only requirement: it was asked for only the decimal answer, not an equation. We preserve both the strict failure and the correct visible content.

The literal code case creates a real file. This is not inferred from its explanation: the actual interpreter event changes test.txt, the final checkpoint retains it, and the stored content object decodes to exactly four bytes, `moss`. That is an off-target effect because the request was to write to standard output followed by a newline. It is not retroactively regraded as task success or described as autonomous storage choice. The complete source was executed through operator verification.

The three plain replies are never submitted to a runtime and have no worlds or physical ticks. Only the three code replies are submitted to identical isolated verification worlds. Across them there are two actual Python actor operations and three physical ticks; all ticks succeed. The sorting fragment remains unexecuted. No model weights change, previous errors are supplied, or live-garden entries advance.

## Frozen comparison

The three underlying tasks and targets match minimal-task-panel-v1: moss,12, and1 2 3. Every new input uses the identical native helpful-assistant system preface from the official tokenizer's earlier rendering. FRR text, the initial world packet, mechanics and prior dialogue are absent. Exact questions, targets, modes and order were frozen before inference in DESIGN.json and CASES.json.

Plain requests ask for the literal word, decimal sum or sorted values only. The frozen score strips only leading/trailing CR and LF from the raw response, then requires an exact target match. It does not strip spaces, extract an answer from prose, interpret a list, or assign a subjective pass. All three fail that predicate. Observations about correct or inconsistent content below are descriptive annotations, not changed scoring rules.

Code questions are byte-identical to the PREVIOUS panel's native questions; the preceding packet and its separating newlines are removed. They ask for exactly one complete executable Python cell and exactly the target plus one newline on stdout. Strict code success requires that actual cell, exit0, empty stderr and no runtime boundary. No source example, implementation, old error or corrective hint is supplied.

Order is literal_plain, literal_code, arithmetic_plain, arithmetic_code, sorting_plain, sorting_code. Plain/code pairs differ in wording, response form and input length. That is a declared diagnostic comparison, not a pure causal intervention on knowledge or reasoning. The earlier packet-present cases are preserved reference trajectories, not new paired replications. One fixed greedy reply per input does not establish general accuracy or an internal mechanism.

## Exact observations

### Plain responses

Literal,38 input tokens and13 generated tokens, EOS: “Moss is a plant that grows on rocks and soil.” This answers with a definition rather than the requested single word. The literal task is an instruction/copy control, not a domain-knowledge benchmark.

Arithmetic,46 input tokens and10 generated tokens, EOS: “7 + 5 = 12.” The arithmetic content is correct; answer-only formatting is not. This is direct visible evidence for this instance, not proof of a general arithmetic procedure or reliable format following.

Sorting,55 input tokens and38 generated tokens, EOS: the reply begins a numbered list with entries “1. 2” and “2. 3”, then concludes “So, the sorted values are: 1, 2, 3.” Its final sequence is correct, but the earlier presentation is inconsistent and it violates the requested space-separated-only answer. We retain the entire reply rather than selecting the correct final substring as a pass.

### Code responses and actual effects

Literal,59 input tokens and106 generated tokens, EOS: the naturally closed Python cell defines a function that opens a filename for writing, writes `moss`, and calls it with `test.txt`. The actual process exits0 with empty stdout and stderr. The path was absent in the initial checkpoint, appears in the actor event's changed_paths, and remains in the final checkpoint after the physical tick.

The independently decoded content-object SHA-256 is `9e135ab954828446379a956e7e12eb7254a482059c765a4e055b617ffe624057`. Its base64 payload decodes to `moss`, length4, and the hash matches the object and checkpoint entry. FILE_EFFECT_VERIFICATION.json retains the checks. File creation is a verified partial effect, not the requested stdout effect. No extra argument, file or code repair was supplied by the operator.

Arithmetic,66 input tokens and168 generated tokens, EOS: the naturally closed cell defines a decimal-named function returning `num * 10 + 5`, then calls input() with “Enter a number: ”. The actual process prints that prompt, receives EOF on its noninteractive input stream, returns EOFError on stderr and exits1. It is not an executed attempt computing7+5, and no hypothetical numeric stdin was provided. Removing the input call or changing its arithmetic would be a source repair, which we did not perform.

Sorting,75 input tokens and256 generated tokens: the reply starts an unclosed Python fence, swaps some string values into a list and repeatedly applies string replace expressions to the list variable. It reaches the token limit mid-expression. No actor process executes this fragment, so potential source issues are not counted as observed interpreter failures. No fence is completed or source extracted.

## Comparison with the previous packet-present panel

The previous native code questions with the packet produced no supported complete cells: three task paraphrases ending at EOS. With those same code questions and native system but without the packet, literal and arithmetic now produce complete cells, while sorting still does not. Neither completed program achieves its requested task. This is a local descriptive difference under packet omission, not proof that every world observation impairs the model or that length alone causes the effect.

The original native print1 positive and its explicit replication remain preserved. A single known positive did not guarantee robust task-following across the broader panel. Likewise, the current off-target artifact does not demonstrate persistent self-directed behavior or knowledge of the whole filesystem. The model receives no follow-up observation of that file in this contact, and independent cases cannot inspect each other's worlds.

Useful layers are now visibly separable: direct task-relevant content, response-format compliance, complete executable transport, actual process outcome, filesystem effect and exact requested result. A strict failure need not erase a verified partial ability; a partial ability must not silently become exact success.

## Integrity

The body remains cached HuggingFaceTB/SmolLM2-135M-Instruct, verified revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. All six calls use unchanged float32 weights, eager attention, two CPU threads, greedy argmax, fresh attention caches and maximum256 output tokens. Tensor digests are checked before and after each call. No training, downloads, paid endpoint, external teacher, retry, source/fence repair or best-of selection is used.

The completed audit verifies exact task/prompt pairing, native system, absence of supplied packet/FRR, templates/tokens/raw decode, mode-specific scoring, literal source/actual receipts/engine events, checkpoints and paused states. Plain replies have no runtime submission; code replies receive one raw submission and one separate physical tick each. The independent artifact check verifies actual persisted bytes, not a source-level promise.

All2,823 prior protected files remain unchanged, including the entire previous panel. The main garden remains paused at entry1630 and reference candidate at turn38; the active pointer and world law are unchanged. All six new cases are paused after one reply, with no pending action, live lock, background inference or queued continuation. The new test.txt exists only in the detached literal-code case. The audit passing means records verify, not that the six task predicates passed.

Local audit.py verifies records without inference; persisted state prevents replay of run.py. Plain cases have no world snapshots by design. Code cases retain initial/final checkpoints, literal source and receipts. Reports, mode-specific summary, content verification and navigation snapshots are covered by the manifest.

## Next strongest

A bounded feedback continuation from the actual arithmetic-code EOFError is now a useful next contact. Preserve the parent case unchanged and fork its post-error world/history. Give the model only its real stdout/stderr/exit receipt, without source repairs, a correct program, a substitute input value, analysis of the arithmetic, or an instruction describing how to fix it. Retain the original task and native framing. Observe its next response and literal effects under a small frozen budget. That would test whether this body can use an actual environmental failure, which the present independent one-reply cases do not measure.

A comparison continuation without error information would be needed before attributing a changed result specifically to feedback rather than another model turn or the added context. Declare exact control prompts and all outcomes before generation. Keep both strict task scores and partial effects, retain runtime errors, and do not infer learning from a single successful revision. FRR/context variants and the world sensor should be reintroduced explicitly only in separately frozen conditions. No feedback call is queued here and no live-garden change is activated.

Garden view: one small arithmetic fact is visible, and one program really left a four-byte mark in its own patch. Neither makes the requested behavior reliable. Another program asked the room for input and met a real wall. The next useful observation is whether its own error can become usable information, without us handing it a route around that wall.
