# Context corners and runtime clarification: handoff differs from task success

17 November 2026, America/Chicago. Four new model calls, under two separately frozen two-call protocols. All are detached diagnostics; the selected garden remains paused at entry 1630 and the reference candidate at turn 38.

## Result

Native chat still emits and executes a correct print-1 cell when the same initial observation packet is included. Full FRR/mechanics framing without that packet emits a closed Python cell, but its program requires an unsupplied command-line argument, prints a usage message, and exits 1. Adding a truthful no-command-line-arguments constraint does not remedy either full-system case: the no-packet program still assumes an argument, while the packet case repeats the constraint without a supported cell.

This refines the previous result. Full framing does not invariably prevent a complete cell. Observation data alone does not invariably prevent a correct cell. Complete transport and correct task execution need separate observations. Neither table establishes a general capability rate, a measured internal reasoning mechanism, learning, or autonomous exploration.

## Fixed-task comparison

The identical question is: “Produce one complete executable Python cell that prints the digit 1.” The native/no-packet and full/packet rows are preserved results from minimal-cell-control-v1; only the other two rows are new calls here.

| System package | Initial serialized packet | Input tokens | Output tokens / stop | Actual Python cells | Actual stdout / exit | Exact task met |
|---|---|---:|---|---:|---|---|
| Native default | Absent | 44 | 127 / EOS | 1 | `1\n` / 0 | Yes |
| Native default | Present | 141 | 120 / EOS | 1 | `1\n` / 0 | Yes |
| Full FRR + mechanics | Absent | 969 | 256 / limit | 1 | `Usage: python program.py <number>\n` / 1 | No |
| Full FRR + mechanics | Present | 1063 | 256 / limit | 0 | No actor process | No |

The full/no-packet system has one narrowly documented correction to its initial-context sentence: it no longer claims that an initial observation packet was supplied. The full system still states the initial byte facts and mechanics. These are descriptive context corners, not a perfectly unchanged-system factorial design; prompt semantics, length and the sentence correction remain attribution limits. Exact inputs, rendered templates, IDs and replacement text are retained.

For complete-cell handoff, the packet difference is 0 under native framing and -1 under full framing in these particular trajectories. For exact print-1 success, both native cases pass and both full cases fail. The apparent pattern therefore depends on which outcome is measured. These arithmetic contrasts summarize observed cases, not interaction estimates for a population.

The new native/packet code was:

```python
def print_digit(num):
    if num == 1:
        print("1")
    else:
        print(f"1 {num}")

# Example usage:
print_digit(1)
```

The literal cell printed `1\n`, with no stderr or boundary and exit 0. Its accompanying prose misdescribes the unused else branch. We assess the actual requested execution, not the explanation's fluency. This program does not read the observation or field.bin; success with a packet does not establish observation grounding.

The full/no-packet cell was also naturally closed, but included:

```python
if len(sys.argv) < 2:
    print("Usage: python program.py <number>")
    sys.exit(1)
```

No argument was supplied to the cell process. The stored literal receipt records the usage line and exit 1, with empty stderr and no resource boundary. The requested outcome was not achieved even though the model's prose described a print-1 program. No operator added arguments, edited the code, or retried it.

## Separately frozen runtime clarification

After seeing that interface mismatch, we appended one factual sentence to the same task: “The cell will be executed without command-line arguments.” No program, fence example, previous failed source or desired implementation was supplied. Both new cases received that same added sentence, with fresh caches and fresh identical seed worlds.

| Full-system case | Input tokens | Output tokens / stop | Actual Python cells | Actual result | Exact task met |
|---|---:|---|---:|---|---|
| Without packet + clarification | 980 | 256 / limit | 1 | Same usage line, exit 1 | No |
| With packet + clarification | 1074 | 256 / limit | 0 | Repeated constraint text; no actor process | No |

The first emits a different program that retains the argument dependency. The second repeats “The cell is executed without command-line arguments.” These are observable output patterns, not evidence of an internal intention to ignore instructions. Mentioning a runtime fact in a reply is not using that fact in a working program. Clarification alone was not a fix in these calls.

The original four-corner comparison retains its original task wording. The clarification is a second protocol, not a retroactive change to the first. All original errors remain intact.

## Method and integrity

The verified cached body is HuggingFaceTB/SmolLM2-135M-Instruct, repository revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, model-file SHA-256 `5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c`. Calls use float32, eager attention, two CPU threads, greedy argmax, a fresh attention cache and at most 256 generated tokens. We verify the loaded parameter digest before and after each call; no weights are changed. No downloads, paid inference, training or external teacher are involved.

Each case starts from the same actual 62-byte seed and checkpoint ID. Each complete raw reply is submitted once to the unchanged literal-cell adapter. Only naturally closed Python/sh fences execute; no fence completion, code extraction repair or semantic approval is applied. Each raw submission receives the unchanged physical tick, including submissions without executable cells. All four physical ticks succeeded. The physical tick is not an actor's requested print result.

The audits independently connect prompt messages and token IDs, decoded generated IDs and raw text, parsed cells and literal interpreter source, actual receipts and engine events, resulting checkpoint and paused state. They distinguish cells from task success. The first audit protects 2,144 earlier files. The second protects those same files plus 53 files from the completed parent contact, totaling 2,197; these are overlapping inventories, not 4,341 different files. Both post-completion audits pass. Three actual Python cells ran across the four new calls; one achieved the requested result. No cell writes an artifact or reads field.bin.

Operator timing note: one early parent audit invocation occurred while RUN.lock still existed. Its precondition correctly refused to audit an in-progress run. The run continued normally; its completed audit subsequently passed. No model call, source repair or retry resulted from that early audit attempt.

All four cases are paused after one reply, with no pending action, engine lock or background inference. The selected main entry 1630, reference turn 38, active garden pointer, earlier study records, world physics and model weights are preserved. Consolidated reporting and sync snapshots live in this follow-up directory so the frozen parent files remain verifiable.

## What this supports and leaves open

High confidence in the recorded literal outcomes and preserved histories. The small model and unchanged executor can complete this particular task with the supplied packet under native framing. A full-system trajectory can complete transport but still fail at its assumed process interface. Adding a factual interface constraint did not fix the tested full cases.

Limited confidence about mechanism. The full package contains FRR text, runtime mechanics, state facts and considerably more tokens than native chat. We have not isolated semantic content from length, order, token identities or generic distractor effects. These short one-task greedy runs do not measure broad competence, general FRR benefit/harm, spontaneous discovery, sustained repair behavior, cognition or developmental phases. There is no training or self-improvement claim.

The strongest next two-call comparison is to separate the existing full system at its already present FRR/mechanics boundary: FRR-only plus the packet and unchanged original question, versus mechanics-only plus the same packet and question. Preserve the existing text verbatim within each component; do not rewrite it into a better prompt. This would locate a candidate component or combination to investigate, not prove why it behaves that way. Length-matched and order controls would follow only if that comparison supplies a useful distinction. No calls are queued and no live garden prompt is changed here.

In garden language: the seed can reach the workbench with the map in view. In the larger instruction canopy, one path reaches the bench carrying the wrong plug; another circles around the wording without reaching it. We can see those as different events without claiming to see the seed's inner experience. The useful improvement today is a clearer measuring station, not a new rule imposed on the garden.
