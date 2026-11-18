# Matched-length content controls: three complete cells, no correct print result

17 November 2026, America/Chicago. Three new cached-model calls under one prospectively frozen three-call protocol. No main-garden entries advanced and no live prompt changed.

## Result

FRR, a geology passage and a textiles passage were each placed after the same native helpful-assistant preface. All received the identical observation packet and original print-1 question. All inputs were exactly 400 tokens. All three replies naturally closed a Python cell and stopped at EOS before the 256-token output ceiling. All three cells were actually executed once, and none achieved the requested result.

| Passage after native preface | Input tokens | Output tokens / stop | Actual Python cells | Actual stdout | Exit | Exact task met |
|---|---:|---|---:|---|---:|---|
| Verbatim FRR component | 400 | 176 / EOS | 1 | `Usage: python program.py <num>\n` | 0 | No |
| Geology control | 400 | 131 / EOS | 1 | Empty | 0 | No |
| Textiles control | 400 | 200 / EOS | 1 | `Usage: python program.py <number>\n` | 1 | No |

All stderr streams were empty and no resource boundary was reached. All three physical ticks also succeeded; they are separate environment operations, not the requested print result.

The preserved native-plus-packet reference, without an added passage, used 141 input tokens and actually printed `1\n` with exit 0. That is a previous trajectory, not a fourth call or a fresh replicate here. The three new failures are compatible with sensitivity to added context but do not identify length as their cause. Multiple particular texts can fail; this contact does not support singling out FRR as the unique source of task failure.

## What the programs did

The FRR case emitted the same raw text and generated token sequence as the earlier FRR-only case without the native preface. It defines a print function, checks for a command-line argument, and otherwise prints a usage line. In this runtime the argument is absent. The literal receipt contains the usage line and exit 0. Its explanation nevertheless says direct execution prints 1. Adding the native preface did not alter this particular greedy output. This is not a general claim that prefaces have no effect.

The geology case defines a print function but never calls it. It instead runs four shell echo commands redirected to `/dev/null`. Consequently its actual stdout is empty, with exit 0. The trailing claim that the program prints 1 is not used as task evidence. We did not invoke its unused function, change the redirection, supply arguments or repair the source.

The textiles case emits a naturally closed program with a required command-line argument. Its missing-argument branch prints a usage line and calls `sys.exit(1)`. That is exactly what the actual receipt records. Its explanation describes a print-1 program, but the requested execution did not produce 1.

All three are complete handoffs; two are error-free processes with the wrong visible result, and one has a nonzero exit. None reads field.bin or creates a file in the persistent world. No fence was repaired or automatically closed. Because all replies ended at EOS within the allowance, the token ceiling did not truncate these three errors. More output allowance alone is not an evidenced repair for this contact.

## Frozen design and exact matching

The task remains: “Produce one complete executable Python cell that prints the digit 1.” The initial packet and task ordering are byte-identical across all three cases and match the original full-context user message. The later no-argument clarification is not supplied.

The common system preface is extracted from the official tokenizer's saved native rendering: “You are a helpful AI assistant named SmolLM, trained by Hugging Face”. Each system message consists of that exact preface, two newlines and its passage. The FRR passage is the verbatim earlier FRR component. Thus the new FRR case differs from the earlier 382-token FRR-only case by an explicit native preface; it is not silently treated as an identical input.

The two task-irrelevant control sources, on geology and textiles, were independently authored and frozen in CONTROL_PASSAGES.json before token matching and before any inference. They contain no program, print solution or instruction to carry out the task. They are comparison texts, not assumed cognitively neutral. Their topics, lexical choices, genre and coherence may affect the model.

The target input count is the native-preface-plus-verbatim-FRR input: 400 official-template tokens including system, fixed user message and generation marker. For each control source, the fixed algorithm tests its decoded token prefixes in increasing length, appending a period, and retains the first prefix whose complete rendered prompt also has 400 tokens. No generation is involved in matching and no passage was replaced after observing an output. Exact selected text, original sources, cutoff indices, native preface, templates and token IDs are retained in MATCHING.json and INITIAL_INPUT.json.

This matching rule can leave an awkward sentence ending. The geology selection ends with “an exterior surface that.”; the textiles selection ends at a sentence about weaving. That is a declared limitation, not silently corrected after seeing outcomes. Equal total token count does not mean equal semantics, positions, word boundaries, attention demands, or cognitive neutrality. This contact matches input length within one framing; it does not create a pure intervention on length itself.

## Interpretation and limits

The shared length does not force identical behavior: the three programs and runtime outcomes differ. All nevertheless fail the exact task. That outcome neither establishes a special FRR failure mechanism nor proves that 400 tokens is a hard capability threshold. The successful 141-token reference differs in content as well as length. Truncated control prose, system-role content and deterministic prompt-specific effects remain possible influences.

Each passage has one greedy trajectory for one task. There is no general success-rate estimate, statistical significance, broad competence comparison, measured internal reasoning trajectory, learning or emergence claim. The model's explanations of its own programs are not substitutes for actual execution. The strongest observation is narrow: under these exact inputs, complete transport occurred in all cases while exact task success occurred in none.

This also retains the distinction developed in earlier contacts: supported complete cell, actual process outcome and requested task success are separate layers. An exit code of 0 alone would falsely count two of these cases as successes. The existing literal task criterion already prevents that; no new behavioral rule is added to the model's world.

## Integrity

The body remains the cached HuggingFaceTB/SmolLM2-135M-Instruct, verified repository revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. Fixed float32 weights, eager attention, two CPU threads, greedy argmax, fresh attention caches, 256-token output bound and identical 62-byte seed worlds are retained. Tensor digests are checked before and after each call. No downloads, paid inference, external teachers, training, retries or source repairs were used.

The completed audit passes. It recomputes the matching, checks identical target input counts, exact messages/templates/tokens and decoded raw output, literal parser/source/interpreter receipts, engine event/checkpoint links and paused states. All 2,360 earlier protected files are unchanged, including the entire previous component/order contact. Three actual actor cells and three physical ticks are recorded. The selected main garden stays at entry 1630 and the reference candidate at turn 38, both paused; the active pointer and world physics are unchanged. All three detached cases are paused after one reply, with no pending action, background inference or queued continuation.

To verify records without inference, run audit.py using the cached Python environment. Do not replay run.py: its saved state prevents another call in these cases. The manifest covers the frozen experiment, outputs, report and navigation snapshots. No observed failure is overwritten.

## Next strongest comparison

Test a shorter matched input, provisionally 200 total tokens, using the same native preface, observation, original task and fixed source passages. For the shorter FRR condition, explicitly use a prefix of the FRR source rather than calling it the full FRR orientation. Apply and freeze a deterministic prefix rule before inference for all three sources; preserve both the complete source and exact retained fragment. Prefer a prospective coherent-boundary design if exact matching permits it; if padding or truncation is needed, declare it before observing outputs. Do not assume monotonic success as the passage grows.

That comparison would ask whether shorter versions of the same source families restore task success in any case. It still changes which text is present as well as length, so a transition would be a local elicitation finding rather than proof of a universal context-capacity boundary. No call is queued and no live-garden prompt repair is justified by the present results.

Garden view: three equal-sized baskets reached the workbench. One held a usage sign, another sent its contents down a drain, and the third asked for something absent. The baskets arriving safely is real; the requested harvest is still missing. We will try less material next, while keeping our labels honest about what changed.
