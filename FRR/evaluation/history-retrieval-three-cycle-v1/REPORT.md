# Context, file retrieval and the difference between a procedure and its selection

Date: 2026-11-14 America/Chicago. Detached diagnostics; selected main garden remains entry **1580**, paused. Four model-contact cycles produced **17 new replies**. A subsequent artifact check executed one saved generated program twice, with **zero additional model calls**.

## Main finding

The same cached 135M model and unchanged execution interface can produce a working file-reading procedure. Whether it does so depends strongly on the supplied conversational context and task presentation in these fixtures. Earlier failures therefore do not establish that the model lacks this operation or that the sandbox blocks it.

This is a local capability witness and a set of presentation-sensitive outcomes, not a general reliability result. No weights were trained, no main memory policy was adopted, and none of these explicit-task diagnostics is an unprompted emergence run.

## What was held fixed

- Body: locally cached HuggingFaceTB/SmolLM2-135M-Instruct, revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, float32 CPU, eager attention, two threads, greedy decoding, maximum 256 output tokens, fresh KV per reply. Parameter digest remained `68981b7ddb65122751502a8ddee3e260a03abd59242ed338761dc4e6949b715e`.
- Task wording: “Use Python to read the value field in probe_value.json and print its exact value.” Format/layout changes are explicit conditions below.
- Execution: unchanged original complete-fence parser and sandbox. Complete cells ran once, without repairs; real receipts alone returned on second turns. An ordinary error was an outcome, not grounds for suppressing a reply.
- Files: saved **pre-model** retrieval fixtures from the preceding observability study, not their post-failure notebooks. Hidden A contains `{"value":"K7M4Q9"}` semantically; hidden B contains `{"value":"R2V8T6"}`. Actual whitespace is preserved in fixture objects. Their only supported-file data difference is `probe_value.json`.
- Every new world received the same extra mechanical declaration permitting these counterfactual diagnostic contexts. The latest appendix explicitly extends the older recent-eight-view diagnostic description. No behavioral hints, example solution or success requirement were added to the physical world.
- The full inherited notebook and archive remain in fresh-input worlds. “Fresh” means a fresh conversational input, not an empty filesystem or erased history.

The source worlds, their objects, exact inputs and token IDs, replies, execution batches and final world snapshots are retained. `PLAN.json` preceded inference. Conditional cycle-two selection is recorded in `CYCLE2_DECISION.json`; the format followup and artifact check each have separate plans written before their actions.

## Cycle 1: inherited history versus a fresh role-shell

Four branches cross two hidden files with two conversational framings. Each gets two replies; the second receives only the first reply's actual execution receipt, without another task or hint.

Inherited input is the prior selected recent-eight-pair history with the final empty user receipt replaced by the exact JSON operator task. Fresh role-shell input is the exact original initial system/user framing, one empty assistant message, then the identical JSON task user message. This deliberately synthetic role-shell preserves a place for the task but changes length, role count and position together.

| Condition | New replies | Input tokens, turns 1/2 | Result |
|---|---:|---|---|
| Inherited, file A | 2 | 2257 / 2580 | One complete cell each; filename parsed as JSON; caught error and `None` |
| Inherited, file B | 2 | 2257 / 2580 | Same inputs and generated token IDs as A; same failure |
| Fresh role-shell, file A | 2 | 132 / 169 | Echoed task JSON; no executable cell |
| Fresh role-shell, file B | 2 | 132 / 169 | Same echo as A; no executable cell |

Inherited code calls `json.loads("probe_value.json")`, rather than opening the file. It catches the resulting JSONDecodeError, prints an error message and `None`, and exits zero. The source file is valid JSON; the program's input to the parser is the wrong object. Process exit zero is therefore distinct from correct retrieval.

The first fresh reply emits 27 tokens including EOS and simply repeats the operator task object. This is a changed behavior, not improved task performance. These comparisons establish context dependence broadly; they do not isolate a repetition, position or length mechanism.

## Cycle 2: same total length and role topology, substituted content

Because first replies differed by framing, the predeclared adaptive branch used two filler controls crossed with both hidden files. Each gets one reply. All assistant-history contents were emptied, then the first assistant slot received enough repeated ` stone` or ` river` words to match the inherited **2257-token** input exactly. Initial framing, user slots and final JSON task were retained.

All four replies immediately emitted EOS: one generated token, empty decoded text, zero complete cells. A/B input token IDs match within each filler condition. No hidden value was exposed in the prompts.

This narrows the observation: equal total length and role topology do not force the inherited faulty-code response. It does **not** isolate semantic meaning. The fillers are unnatural counterfactuals, concentrate their content in the earliest assistant slot and do not match content distribution across positions. Two repeated words are narrow coverage; neither is assumed neutral.

## Cycle 3: authentic document versus parsed-value receipts

One fresh role-shell branch receives an actual operator receipt for reading the full document text; another receives an actual operator receipt for reading and extracting its value. Both use file A. These are extra supplied observations, with different information, lengths and punctuation—not a single controlled causal factor. Operator preparation source and receipts are saved separately and never counted as model-chosen actions.

| Supplied receipt | Input tokens | Observed model result |
|---|---:|---|
| Full document text | 188 | Echoed the supplied receipt and task JSON; no complete cell |
| Parsed value | 182 | Generated and executed a correct file-reading procedure; stdout `Value: K7M4Q9` |

The document echo contains the nonce because that nonce was supplied in the input. Target-substring presence alone would falsely make this look like acquisition or extraction.

The parsed-value branch is different. Its generated code contains **no nonce literal**. It uses `with open(file_path, "r")`, `json.load(f)`, and `json_data["value"]`, then executes that program successfully. Its receipt reports the correct file value with a label. This witnesses a working procedure under supplied-value context; it does not show that the supplied value was necessary or that the model reliably selects that procedure without it.

## Cycle 4: task format crossed with message layout

The fresh role-shell's task echo warranted a smaller decomposition before any body-capability conclusion. All four message arrays were declared in `format-followup/PLAN.json`; the existing fresh-JSON reply supplies one corner, and three new one-reply branches use file A. The merged layout retains the empty system message and puts initial framing, two newlines and the task into one user message.

| Layout | JSON task | Plain task |
|---|---|---|
| Empty-assistant role-shell | Existing reference: echoes task | New: parses literal `"value"` as JSON, catches error |
| Initial framing and task merged in one user message | New: opens correct hidden file, extracts field, prints correct labeled value | New: reads wrong path `/world.json`; real FileNotFoundError |

The merged-JSON branch has **123 input tokens**. It generates a complete program using `open('probe_value.json')` via a variable, `json.load`, and field indexing. The hidden nonce is absent from both its input and generated text, yet appears in actual stdout:

`The value field in probe_value.json is: K7M4Q9`

This is the strongest capability witness in the run: this body/interface combination can select and execute a correct hidden-file read under one tested presentation. Plain wording did not uniformly help; layout and serialization interact in these examples. Three additional replies and one reused reference do not identify a universal best prompt or establish transfer to new tasks.

## Check of the generated artifact, without another model call

We executed the **unchanged full saved notebook text** from the parsed-value branch against fresh A and B fixtures. The actual outputs were:

| File value | Actual stdout |
|---|---|
| K7M4Q9 | `Value: K7M4Q9` |
| R2V8T6 | `Value: R2V8T6` |

The generated artifact's output follows the file contents. This is stronger evidence for that program's file dependence than merely spotting an `open` token. It is **two program executions**, not two independently generated solutions or a generalization score. No repaired code, hidden hint or model continuation was used. This was a newly declared counterfactual action, not replay of an unresolved action.

## Success labels and failure labels remain separate

Across the 17 new model replies, two branches print the correct field value in real stdout. Both add prose labels. The predeclared **bare exact-value stdout** measure remains false for every reply. We retain that result instead of changing the metric after seeing a useful output.

The meaningful layers are:

1. A complete executable cell is present.
2. The cell actually executes and returns a known receipt.
3. Its procedure opens the intended file and extracts the requested field.
4. Its output contains the correct file-dependent value.
5. Its output obeys the exact requested output convention.
6. The procedure is selected reliably across new contexts or tasks.

These are different observations. This run contains witnesses for layers 1–4, misses the strict output convention, and does not establish layer 6. No access tracer was installed; conclusions use unchanged generated source, actual sandbox receipts and the explicit file-swap artifact check. An open-attempt trace by itself would be weaker than successful read/extraction evidence.

## Integrity, interruption and limits

The experiment recorder initially assumed every operation had a feedback dictionary. Notebook-only operations legitimately have `None`. After the first action completed and its raw output/batch were saved, readout stopped with AttributeError. The original source and failure log are preserved. A separate recovery script verified the known completed world state, recovered the result from saved artifacts and cleared its outer pending marker. **Zero model generations or cell actions were replayed.** The recorder now handles empty feedback fields; this fix does not change the model prompt, sampling or sandbox.

Both artifact audits pass: exact input token IDs and decoded outputs recompute, actual receipt chaining matches saved prompts, hidden nonces are absent where required, paired initial inputs match, supported initial world IDs match within each file condition, and every detached store verifies. All **823** selected-main non-cache files retain their before hashes. There are no unresolved pending outcomes. Weights are unchanged.

The main remains at entry1580 because its next full-history input is 8104 tokens, beyond the 7936 input limit. It was not silently resumed with a shorter view. These experiments do not select a new main continuity policy.

This is a tiny deterministic diagnostic on one body and one toy file task, with a narrow set of counterfactual contexts. Repeated identical token inputs under greedy decoding are not independent statistical samples. Supplied receipts, merged layouts and fillers each change multiple relevant properties. No claims of consciousness, maturation, new learning, broad competence or superiority follow.

## Garden interpretation and next contact

The gate was not a locked file door. In some contexts the small model chose the wrong motion; in another it copied the request; with one different arrangement it used the door correctly. The same soil, body and tools can support different acts. That shifts our attention from “can this body ever do it?” toward “what makes this body select that procedure, and how stable is the selection?”

The next strongest contact is a small **prospective presentation/transfer matrix**, declared before new outputs: retain both successful and failed formats, change nonce and filename/key separately, and assess file acquisition, field extraction and output formatting independently. Include changed names so a fixed successful template is not mistaken for general tool use. Keep failures and use held-out variants rather than repeatedly tuning this one fixture.

In parallel conceptually, a bounded main-memory policy remains a separate decision requiring preservation and explicit activation. The successful prompted read does not justify silently replacing the live history. No new main changes are recommended by this report alone.

## Records

- `PLAN.json`, `CYCLE2_DECISION.json`, `jobs/`: declared inputs and adaptive choice.
- `results/`: exact raw messages, token IDs, text, execution batches and readouts.
- `worlds/`: detached ledgers, bundles and content-addressed files.
- `format-followup/`: layout/serialization comparison, separately planned and counted.
- `program-transfer/`: unchanged artifact file-swap check; zero new inference.
- `AUDIT.json`, `FOLLOWUP_AUDIT.json`: artifact and main-preservation checks.
- `RECORDER_FAILURE.txt`, `RECORDER_RECOVERY.json`, `run_before_recorder_fix.py`: preserved tooling failure and recovery.
- `before/`: previous navigation records, archived without alteration.

Interpretation draws on the preceding `../source-weave-three-pass-v1/` and `../observability-three-contact-v1/` records. Those sources motivated controls; they did not execute or independently replicate these local outcomes.
