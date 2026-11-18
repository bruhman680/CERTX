# Three sequential rounds: shorter context, near-task transfer and explicit cardinality

17 November 2026, America/Chicago. Nine actual model calls under three separately frozen budgets [3,3,3]. Three completed audits pass. One earlier preparation failure generated no model reply and is preserved separately. All runs are detached diagnostics; the main garden and reference candidate remain unchanged.

## Findings

Shortening the added passages from the previous400-token contact to199 total input tokens did not restore the original print1 task for any of the three sources. A fresh native/no-added-passage repeat reproduced the earlier print1 positive exactly. A nearby letter task exposed different failures: repeated output and unrelated file-reading code. Explicitly asking for the letter exactly once did not yield a strict success in the final round.

All nine actual replies contained supported complete cells. Ten cells ran because one reply supplied two alternatives. There was no semantic gate rejecting a complete submitted program. The runtime actually printed outputs and returned real argument, directory and missing-file errors. Handoff completion therefore cannot be equated with task success. These results do not establish reliable capability, learning, an FRR-specific cause, or a universal context-length threshold.

## The complete result table

Every case uses the same initial62-byte seed and serialized observation. Model weights, decoder, literal adapter and physical law remain fixed. The original requested target is1; later cases explicitly requestA. The strict target criterion and case budgets were frozen before their respective calls.

| Round / case | Input tokens | Generated tokens / stop | Actual Python cells | Actual stdout / effect | Exit | Strict task met |
|---|---:|---|---:|---|---|---|
| 1: short FRR, digit1 | 199 | 164 / EOS | 1 | Usage line | 0 | No |
| 1: short geology, digit1 | 199 | 178 / EOS | 1 | Usage line | 1 | No |
| 1: short textiles, digit1 | 199 | 174 / EOS | 1 | Usage line | 1 | No |
| 2: native digit1 repeat | 141 | 120 / EOS | 1 | `1\n` | 0 | Yes |
| 2: native uppercaseA | 142 | 132 / EOS | 1 | Eleven `A\n` lines | 0 | No |
| 2: short FRR, uppercaseA | 200 | 256 / limit | 1 | Empty; IsADirectoryError | 1 | No |
| 3: nativeA exactly once | 144 | 232 / EOS | 2 | Each cell prints `A \n` | 0,0 | No |
| 3: short FRR,A exactly once | 202 | 158 / EOS | 1 | Empty; FileNotFoundError | 1 | No |
| 3: short geology,A exactly once | 202 | 191 / EOS | 1 | Usage line | 1 | No |

This is a record of an adaptive sequence, not a9-trial population success-rate estimate. The native repeat is a deliberately frozen replication of a prior positive prompt, not a retry of a failed generated program. Its generated IDs and raw text equal the stored earlier native+packet case. No failed case was silently replaced.

The selected main garden remains at entry1630; the reference candidate remains at turn38. These nine independent one-reply probes do not advance a continuous garden by nine entries. Fresh attention caches and fresh detached worlds are used. The researcher carries findings between rounds; the model is not given the previous replies, errors or researcher diagnoses. No training or learning claim follows.

## Round1: shorter, matched source prefixes

The original question is unchanged: “Produce one complete executable Python cell that prints the digit1.” In actual prompts, the source wording retains the space in “digit 1”; prose here uses compact labels only. The same native helpful preface and initial packet are shared across all cases. Full FRR, geology and textiles sources come from the prior contact and are retained in CONTROL_PASSAGES.json.

Preparation initially requested exactly200 tokens using the fixed decoded-token-prefix-plus-period rule. That exact input count was unreachable for FRR under the rule. The preparation failed before creating case states or generating a reply. A shell-launched runner then loaded the model but failed on the missing initial state before reaching generation. Both scripts/protocol, resource record and fault evidence are retained under stage1_preflight_failure. It has zero RAW.json records and zero actual model calls; the incident is not hidden or called a completed experimental round.

Before any generation, a revised protocol selected the nearest COMMON reachable input count in192..208, with ties resolved toward the lower count. That count was199. The runner was also given a preflight/state precondition before model loading. This is a diagnostic preparation repair, not a repair to any model output or to the live world. The original failed preparation and its frozen text remain intact.

All three revised inputs match199 tokens exactly. Each source is shortened by the same deterministic prefix-plus-period rule, frozen before inference. The FRR condition is explicitly a short prefix, not the full FRR orientation. The resulting endings include “Exploration can branch, combine.”, “Coarse gravel often settles near.” and “The arrangement of.” Awkward cutoffs are preserved as attribution limits. Text content changes together with amount; a pure length effect is not isolated.

All three emit closed programs that require a command-line argument not supplied by the runtime. They print usage text. FRR exits0 and the other two exit1. Their natural-language explanations describe a successful print task, but actual receipts do not. All stop at EOS below256. Shortening to this particular199-token form therefore did not remedy the tested failures. It does not prove every short passage fails or establish a hard boundary between141 and199 tokens.

## Round2: current positive anchor and a nearby task

After round1's audit, the second protocol was frozen. native_repeat uses the exact previous user-only native+packet print1 prompt, rendered by the official chat template. It again prints1 with exit0 and identical generated IDs/text. This supports continued operation of the cached body, prompt path and literal executor on that narrow known task. It is not a general accuracy measurement.

native_letter changes the requested result to the uppercase letterA: “Produce one complete executable Python cell that prints the uppercase letter A.” The model defines a function that printsA for every character of an example string, then calls it on “Hello World”. Actual output contains elevenA lines. It can print the letter; it fails the prospectively defined strict single-target outcome. The wording may allow more interpretation than an exact-byte specification, which motivates round3. We keep the strict original score and also describe the actual behavior rather than implying an inability to emitA.

frr_letter uses that sameA question with the exact short native-prefaced FRR system from round1. Its code tries to open `/world` in binary read mode as if it were a file. The interpreter returns IsADirectoryError, stdout is empty, and exit code is1. The cell was naturally closed and executed even though subsequent explanatory prose reached the generation limit. The actual runtime failure was not a semantic rejection by the observer or an unclosed-cell issue.

No past output, directory-error explanation, source code, implementation or correction was supplied to the model. Native and FRR inputs are not length-matched in this round. The task change alters both wording and requested character, so it does not isolate a single token's causal role.

## Round3: make cardinality explicit

The final protocol, frozen after round2's audit, asks all three cases: “Produce one complete executable Python cell that prints the uppercase letter A exactly once.” The native framing and observation are retained. The FRR and geology system messages are exact copies from round1, not rewritten after outcomes. Their inputs both contain202 tokens; native has144. Geology+A is a new control, not a paired round2 replicate.

The native response contains two alternative, naturally closed Python cells. Each invokes a function with1 and printsA followed by a space and newline. The unchanged adapter executes BOTH in order, as its literal world law requires. We do not select a preferred alternative or throw away the second. This response violates the one-cell requirement and produces two effects; each also differs from the strict target by trailing space. It is not counted as exact success. The model's ability to generate working letter-printing programs remains visible in the raw evidence.

The FRR case opens a placeholder path `/path/to/your/file.bin` and returns FileNotFoundError. We do not create that placeholder file to make its program work. The geology case asks for a file-name argument, prints a usage line and exits1 when it is absent. Both are real executed consequences in the supplied runtime. No code or fence is repaired.

All three stop at EOS before the limit. Stating cardinality explicitly did not provide a strict-task repair here. No prompt is promoted to the live garden from these observations.

## What our observation can and cannot say

The transport accepted all nine responses' complete supported cells and committed ten actor operations. All nine separate physical ticks succeeded. Every case remained within a known runtime outcome; the resulting directory still contains only field.bin, whose changes come from the physical law. No model-written persistent artifact or successful field-content read is established. The two attempted file opens are actual actions, with runtime errors, not successful grounding in the observation.

This contact helps distinguish action availability from action suitability. It supports the narrow observation that these programs were allowed to operate and fail within their worlds. It does not show that the model understands the world, can recover from an error it has not subsequently been shown, lacks reasoning, is developing, is panicking, or needs a particular new behavioral framework. These are one-reply elicitation probes, not feedback-driven adaptation runs.

The raw replies often contain tutorial-style functions, example invocations, alternatives or invented path dependencies. That is an observed output pattern. Attributing it to particular pretraining data, a hidden mental state, or an internal mechanism remains a hypothesis. Similarly, failures in both FRR and unrelated control conditions do not uniquely identify FRR as harmful; shortening and added native framing did not establish a general fix.

The exact task checks remain external. They do not inject a success/failure grade into the small model's world or prevent complete code from executing. Current scores separately retain cells, runtime receipts, boundaries and the prospectively specified target, so exit0, fluent claims or “nearly right” output cannot silently become exact success. Partial observable abilities are described alongside strict failures.

## Integrity

The body is the unchanged cached HuggingFaceTB/SmolLM2-135M-Instruct, verified revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. All actual calls use fixed float32 weights, eager attention, two CPU threads, greedy argmax, fresh attention caches and output bound256. Tensor digests are checked before and after calls. No training, download, paid endpoint, external teacher, model-output repair or inference retry is used.

Each of the three completed stage audits passes. Exact prompts/templates/IDs and decoded raw outputs, parser/source correspondence, actual process receipts, engine events/checkpoints and paused state are verified. Round1 protects2,443 earlier files. Round2 also protects completed round1, archived preparation evidence and the sequence plan, totaling2,529. Round3 additionally protects completed round2, totaling2,605. These inventories overlap and are not added together as independent histories. The original failed preparation remains failed evidence, not an audited successful experiment.

The three new actual-call budgets are[3,3,3]; the preparation incident contributes0. All nine cases are paused after one reply. No pending actions, live locks, background inference or queued continuation remain. Main1630, reference38, the active garden pointer, prior studies and world physics are preserved. Root reports, manifest and navigation snapshots are separate from the frozen stage records.

Run the three stage audit.py scripts using the cached environment Python for record verification without inference. Do not rerun the inference runners: their persisted state and preconditions prohibit replay. The archived preparation has intentionally retained its original failure and absolute pins; it is evidence, not a current runnable success capsule.

## Next strongest

Freeze a small, varied task panel under two fixed contexts: native framing and one explicitly specified minimal FRR context. Include direct literal output and a simple computed result, with requirements about multiplicity and exact observable effects stated before generation. Use ordinary outcome requests rather than source examples, and keep every result. Treat the comparison as an operational capability check with content/length limits, not a causal estimate of FRR benefit. An artifact-writing task should have a file-state predicate rather than assuming stdout proves file creation.

This would broaden evidence beyond repeatedly changing a single print1 prompt. Keep strict compliance and useful partial execution separate. If a stable conditional capability appears, then design a bounded multi-turn feedback probe to test whether the model can use a real error; do not infer recovery ability from the present single-reply errors. No such call is queued here and no world redesign is justified by these data alone.

Garden view: the floor carried the weight, the doors opened, and the tools really struck material. Some programs asked for missing supplies; another offered two demonstrations when one action was requested. The familiar native1 sprout appeared again, so that small route remains real. What has grown most this session is our ability to distinguish a working door, a working tool, an unintended action and the actual harvest.
