# Small paired task panel: task paraphrases versus unfinished code

17 November 2026, America/Chicago. Six new cached-model calls under one prospectively frozen protocol: three tasks, each under native and fixed minimal-FRR framing. The completed integrity audit passes. No live-garden prompt change or continuation is activated.

## Results

None of the six cases handed a complete supported cell to the interpreter. Native replies paraphrased the requested task and stopped at EOS. Minimal-FRR replies began Python fences, then repeated or extended unrelated functions until reaching the256-token output bound without closing them. There were zero actor operations, six separate successful physical ticks and zero exact task successes.

| Task and exact requested stdout | Native input / output tokens | Native observed behavior | Minimal-FRR input / output tokens | Minimal-FRR observed behavior |
|---|---|---|---|---|
| Literal: `moss\n` | 156 / 29 | Paraphrased task, EOS, no cell | 205 / 256 | Open Python fence, unfinished file-processing functions |
| Arithmetic: `12\n` for7+5 | 163 / 36 | Paraphrased task, EOS, no cell | 212 / 256 | Open Python fence, repeated decimal-named functions |
| Sorting: `1 2 3\n` for ascending3,1,2 | 172 / 45 | Paraphrased task, EOS, no cell | 221 / 256 | Open Python fence, repeated newline replacements |

All six strict outcomes fail. This is not evidence that the model cannot compute7+5 or sort three values: the requested code responses did not produce complete programs to run, and these are not direct plain-answer knowledge tests. The panel broadens the observed prompt failures beyond the earlier repeatedly varied print1 request, while introducing a shared, more explicit task wording. That shared wording remains a possible influence.

The extra minimal-FRR text changes output form in these three trajectories—from task paraphrase to unfinished code—but that is not task improvement. Content, role-message length and token positions change together, so a causal benefit/harm claim about FRR is not supported. One deterministic reply per case is not a population success rate or broad capability score.

## Frozen panel and context

Task questions and exact outcomes were defined before any model call in PANEL.json and CASES.json. They request exactly one complete executable Python cell, only the requested stdout, and one final newline. Literal output asks for the word moss. Arithmetic asks for7+5. Sorting asks for3,1,2 in ascending order separated by single spaces. The prompts retain ordinary spaces around numerical expressions; compact labels in this report are not replacement prompts.

No implementation, program, code example, previous error or solution demonstration is supplied. These are outcome requests. All cases receive the identical actual initial world packet, followed by the task question. Within each task pair, the user message is byte-identical.

The native system is the exact helpful-assistant preface from the official tokenizer's earlier saved default rendering. The minimal-FRR system appends two newlines and the verbatim FIRST COMPLETE FRR PARAGRAPH from the preserved full system. That paragraph begins “An idea can have several related representations” and ends “A relation useful in one setting may fail in another.” It is a fixed coherent fragment, not the full FRR orientation, a trained capability or an installation into weights. It adds49 input tokens in each pair. No other context component varies within a pair, but total input length is not matched.

Order was frozen as literal_native, literal_frr, arithmetic_native, arithmetic_frr, sorting_native, sorting_frr. Each uses fresh attention caches and an independent identical seed world. No reply, runtime error or researcher analysis from an earlier case is included in a later input. The model does not learn from the panel, and these are not six continuing garden entries.

## Literal observations

Native literal replies: “Produce a complete executable Python cell. When run, it must write only the word moss to standard output, followed by one newline.” The arithmetic and sorting replies similarly restate their requested outputs. They contain no supported executable fence. They stop after29,36 and45 generated tokens, respectively; their failure is not truncation at the output cap.

Minimal-FRR literal opens a Python fence and defines `generate_moss_cell` and related file-processing functions. It reaches the token limit mid-definition without a closing fence. Those function definitions and operations are unexecuted text; there are no model-created or removed files to attribute to them.

Minimal-FRR arithmetic opens a Python fence and defines decimal-named functions involving multiplication by10, additions and newline concatenation. It expands function names rather than delivering a closed addition program and reaches the limit mid-definition. This is not an executed incorrect arithmetic result. No actual stdout12, or any other actor stdout, exists for this case.

Minimal-FRR sorting opens a Python fence and defines a file-reading function with repeated newline replacements, reaching the limit inside a string operation. It does not provide a complete supported cell or an actually executed sort. Again, the runtime has no actor receipt to score as a calculation.

The unchanged adapter accepts only naturally closed supported fences. We submit each full raw response once and do not infer a closing fence, extract a preferred fragment, repair a function, or choose a better reply. Automatic execution of incomplete source would be a different transport protocol and is not tested here. A larger generation budget also remains untested by this panel; the unfinished, task-divergent source does not itself establish that more tokens would fix the task.

## Scoring and what did change

The prospective exact predicate requires one actual Python operation, stdout exactly the task target plus one newline, exit0, no stderr and no boundary. Extra cells, missing/extra characters and merely stating the task do not pass. Partial observable effects are recorded separately from strict correctness. Here no actor operation occurred, so the missing handoff precedes runtime success/failure; we do not label these as interpreter errors.

Each raw reply nevertheless receives one unchanged physical tick. All six ticks succeed. They change field.bin according to the supplied world law, independently of actor task success. The resulting world contains only field.bin, with no model-written artifact. Tick success is not counted as a model solving the task. The operator-verification path does not establish autonomous action or learning.

The earlier native print1 positive remains intact, including its independent exact replication in the prior contact. This panel neither reruns nor erases that positive. It demonstrates that success on that single prompt was insufficient to justify assuming robust code handoff for these broader requests. It does not identify which task wording, packet content, length or training pattern explains the failures.

## Integrity

The cached body remains HuggingFaceTB/SmolLM2-135M-Instruct, verified revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. Calls use unchanged float32 weights, eager attention, two CPU threads, greedy argmax, fresh caches and maximum256 generated tokens. Tensor digests are checked before and after each call. No training, download, paid endpoint, external teacher, source repair, code hint, supplied argument, inference retry or extra call is used.

Preflight verifies six identical initial62-byte world checkpoints and saves exact rendered prompts/token IDs. The completed audit verifies panel order, within-pair messages/targets, the verbatim first-paragraph context, token/template/raw decode, literal parsing, receipts/events/checkpoints and paused states. All2,691 earlier protected files remain unchanged, including the complete prior three-round contact and its archived failed preparation. No new preparation incident occurred in this panel.

The selected main garden stays at entry1630 and the reference candidate at turn38, both paused. The active garden pointer, prior histories, world laws and model weights are unchanged. All six diagnostic cases are paused after one reply, with no pending action, live engine/run lock, background inference or queued continuation. The audit passing means the records and invariants verify; it does not mean the tasks passed.

The local audit.py can verify the records using the cached Python without inference. Persisted runner state prevents replay. PANEL.json, CASES.json, raw replies, initial/final checkpoints, engine/tick events, results, report, navigation snapshots and manifest are retained.

## Next strongest

Separate direct-answer competence from code-generation competence under minimal native chat before adding the world packet. Predeclare a small pair of plain-answer and code requests for the same underlying task, with exact observable criteria and no supplied implementation. Keep native framing and model settings fixed; then reintroduce the unchanged observation packet in separately frozen conditions if a useful baseline appears. Report all prompts and ordinary failures rather than selecting a successful wording after a search.

This can distinguish failure to deliver an executable answer from failure on a direct task, while still leaving wording as an explicit experimental factor. It must not be called an internal reasoning measurement or proof of a particular training cause. Any subsequent artifact task needs a file-state predicate; these stdout requests do not verify file creation. No such follow-up is queued, and this panel provides no justified live-garden prompt repair.

Garden view: with the shorter label, the model repeated the sign; with the added FRR paragraph, it started building but left the structure unfinished. Neither delivered the requested crop. We can now see another seam between reading a request, stating it, writing source and completing an action. Our next check belongs at that seam, before attributing the result to arithmetic knowledge or the garden's deeper soil.
