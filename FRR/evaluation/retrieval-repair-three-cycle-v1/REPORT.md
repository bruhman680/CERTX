# Repair attempts: actual feedback, explicit corrections, and paired effects

15 November2026 UTC. Three detached cycles: **six new local model replies**, then **six additional unchanged-artifact executions**. No training or diagnostic activation. The preserved original main1580 phase remains unchanged; the separate authorized bounded-main continuation is recorded in its own phase.

## What we attempted to mend

The prior task-transfer matrix exposed three different merged-layout failures: a wrong pathname for a changed field, passing a string to `json.load` for a changed filename, and an unfinished code fence when both changed. We compared two declared responses to those same completed failures.

Cycle1 clones each actual **post-failure** A world and supplies the exact failed assistant reply plus its actual receipt. It then allows one new reply, with no repair instruction or repeated task. The unfinished-fence branch gets the actual empty receipt; we do not invent a runtime error when no cell executed.

Cycle2 independently clones the same post-failure A states and inputs, adding one clearly labeled operator correction. These corrections name the intended path/key, explain the file-object versus string parser distinction where relevant, or ask for a short complete Python fence. Exact texts were saved in `PLAN.json` before inference. They are diagnostic coaching, not discovered observations or new main behavior rules. They change information, wording and length together.

Cycle3 executes all six unchanged new replies on corresponding B post-failure worlds. This checks the generated artifacts against changed file values without another model call. Target values are absent from prompts; the paired initial supported worlds differ only in target-file bytes.

The same cached pinned SmolLM2-135M-Instruct body, float32 CPU/eager/two threads, greedy256/fresh KV and unchanged parser/runtime are used. Ordinary errors and incomplete code are preserved. No code is repaired after generation.

## Results

| Prior failure | Actual feedback only | Feedback plus explicit correction |
|---|---|---|
| Changed key / wrong path | Complete cell again selects `/world.json`; FileNotFoundError | Same wrong path; exact prior failed output token IDs |
| Changed filename / parser-input type | Complete cell again passes a string to `json.load`; AttributeError | Same parser-input error; exact prior failed output token IDs |
| Both changed / incomplete fence | Unfinished fence; no cell; exact prior output token IDs | Unfinished fence; no executable cell |

All six replies reach the256-token output limit. Four contain one complete Python cell; two have no complete executable cell. None prints the requested value on A. None of the six paired B executions prints B's value. Bare exact-value stdout remains false throughout. These are counts for the declared conditions, not estimates of broad repair ability.

The feedback-only wrong-path reply changes an unused helper's field name to `boundary`, a word present in the structured receipt, and changes explanatory prose. Its executed main still opens the wrong path. This is observable vocabulary/schema drift; it is not successful boundary reasoning or repair. The latent helper error does not replace the first actual executed error in our attribution.

The corrections therefore did not mend retrieval behavior in this contact. Some outputs changed in wording, but the requested effects did not. We cannot conclude that the model internally ignored feedback, that all coaching fails, or that this body can never repair. We can say that these six explicitly specified contexts did not produce the correct operation.

## What was repaired and what was not

The observed **context-capacity problem** is addressed separately by the newly authorized bounded-main continuity version. That engineering repair changes immediate input selection while preserving complete external history; it is not model learning or a retrieval repair.

The observer harness now supports a more precise distinction between request copying, code completion, process execution, path/field binding, file-dependent output and strict output convention. Exact token comparisons prevent changed introductions from being called improved behavior. That improves our observations; it does not improve the small model's weights or establish a better reasoning policy.

No correction from this study enters the open main invitation. No successful-looking branch is selected into the main trajectory. The garden can continue independently of whether these explicit diagnostic tasks succeeded.

## Integrity and interpretation limits

`AUDIT.json` recomputes exact prompts/token IDs/decoded texts and verifies receipt fidelity, declared coaching labels, paired initial fixture differences, unchanged artifact text and all12 detached stores. All823 original-main files match their before hashes, tensor digest is unchanged, and no pending outcome remains. Model effects are retained in their own worlds even when unsuccessful.

Two coached responses reproduce the old failed output IDs exactly; this is a deterministic conditional output observation, not an independent sample or a hidden-state measurement. Paired artifact executions test saved code; they are not six more model solutions. No external tool-access tracer or weight update is installed.

Next useful diagnostic, if pursued: hold the actual error information fixed while changing how receipt metadata and task-specific names are presented, with a predeclared comparison. This could test whether schema vocabulary participates in binding errors without assuming a causal mechanism from a single lexical drift. Any such presentation change belongs in detached diagnostics first.

Records: `PLAN.json`, `jobs/`, `preparation/`, `results/`, `artifacts/`, `worlds/`, `AUDIT.json`. See `../bounded-main-continuation-v1/` for the separately authorized main50 and its activation/continuity law.
