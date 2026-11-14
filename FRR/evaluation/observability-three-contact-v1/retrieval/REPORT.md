# Prompted retrieval controls

13 November 2026, America/Chicago. This is an explicit task diagnostic on copied worlds, not the main garden's open exploration. No model inference, execution, or world write was performed by this readout.

## Fixture and input controls

Two ordinary readable files contain different values, K7M4Q9 and R2V8T6, at the same path `probe_value.json`. Their supported filesystem snapshots differ only in that file. Their first model inputs are exactly identical and neither target appears in those messages. The task asks for the value field to be read and printed. A third world has the same supported filesystem as A; it supplies the same task plus an authentic operator-originated Python read receipt showing A's value. The operator attribution is explicit. This extra receipt changes input length/content and makes the target directly available; it is not evidence of model-chosen retrieval.

Each branch receives at most two replies. The second input appends only the first actual assistant reply and factual consequences, without repeating the task or adding a solution. All complete cells run unchanged. `PREPARATION_CHECKS.json`, `FIXTURE_PAIR_AUDIT.json`, source commands and receipts ground the controls.

| Case | Turn | Complete cells | Code exit codes | Target appears in text | Target appears in code stdout |
|---|---:|---:|---|---|---|
| retrieval_hidden_a | 1 | 1 | [0] | False | False |
| retrieval_hidden_a | 2 | 1 | [0] | False | False |
| retrieval_hidden_b | 1 | 1 | [0] | False | False |
| retrieval_hidden_b | 2 | 1 | [0] | False | False |
| retrieval_provided_a | 1 | 0 | [] | False | False |
| retrieval_provided_a | 2 | 0 | [] | False | False |

## Interpretation

All six replies omit the exact target string from both their visible text and executed stdout. The two supplied-read replies return to the source network-program text, with unfinished fences and no dispatched cell, despite the value being directly present in the authentic operator receipt. Thus this contact observes neither successful prompted retrieval nor successful use of the supplied value. It does not prove either capability impossible under other wording, context, model or horizon.

Read the executed sources and actual stdout separately from process exit. The hidden-pair code calls `json.loads` on the literal filename string `probe_value.json`, instead of opening the valid file and parsing its contents. It catches the resulting JSONDecodeError and prints an invalid-JSON message plus None, exiting normally with code0. That is a handled error in the generated procedure; it does not show that the fixture file is invalid or that sandbox access was denied. The real operator read and decoded fixture bytes establish readability and valid JSON.

The hidden first replies are identical, and their second input token IDs, output token IDs and text also match exactly across the two different files. The described target changes from value to boundary without performing the intended file access. Receipt-schema vocabulary appearing in code or prose is not itself retrieval or error resolution.

For the supplied-read case, target text or stdout, if present, can use information already delivered in the prompt. That outcome cannot by itself establish an actual file read. The per-case static call inventory is an aid to source inspection rather than a universal dynamic tracing system; actual receipts and complete source remain authoritative.

`RESULTS_INTERPRETATION.json` records every row, exact pair comparisons, stdout/stderr, source calls and final fixture state. A zero exit code, a complete fence, mention of the filename, an answer in prose, and a successful read are distinct observations. This small selected-context diagnostic does not establish general inability to retrieve or success on future retrieval tasks.
