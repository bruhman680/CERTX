# Minimal interface recovery probes

9 November 2026. Twelve prospectively declared one-step CPU diagnostic calls, not a continuation of the garden. Canonical entry1550 and all4467 phase files stayed unchanged; no adapter, training, paid API, download, or model-facing live edit occurred.

## Provenance and framing

The cached checkpoint is the pinned SmolLM2-135M-Instruct directory, with weights SHA256 5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c and tensor digest68981b7ddb65122751502a8ddee3e260a03abd59242ed338761dc4e6949b715e. The model config (30layers, hidden576, vocab49152), tokenizer and ChatML role template are consistent. EOS is token2. No tokenizer/config mismatch was identified. This is an inspection of cached provenance and frozen pins, not an independent download verification.

The tokenizer inserts its helpful-assistant factory system text when the messages contain no system turn. An explicit empty system suppresses that text. Both forms were tested as separate diagnostic conditions. Exact rendered prompts and token IDs are retained in raw files.

All prompts were minimal requests without the long mechanical notice, curiosity invitation, or prior replay. Greedy conditions used raw argmax and therefore have no operative temperature or random seed. The two sampled conditions used temperature0.8, full softmax, seed121605. Output bound96 and fresh KV were fixed. Greedy and full-softmax results are separate decoding conditions, not a claim that one always improves reasoning.

## Results

| Request | Empty system, greedy | Factory framing, greedy |
| --- | --- | --- |
| Copy supplied action JSON | Valid whole JSON; actual pwd success | Valid whole JSON; actual pwd success |
| Formulate JSON action from a command request | Shebang/comment repetition; no envelope | Same kind of repetition; no envelope |
| Produce raw shell source for cwd | Invalid shell; actual runtime error | Unfinished/invalid shell; actual runtime error |
| Produce raw Python source for cwd | Complete fenced Python plus explanation; raw-source SyntaxError | Complete fenced Python plus explanation; raw-source SyntaxError |
| Repeat the word pwd | Literal pwd; actual shell success | Literal pwd; actual shell success |

The two full-softmax minimal JSON-copy calls failed the whole-reply envelope: the empty frame produced malformed Python narrative, and the factory frame produced a correct target JSON object inside prose/fences. Those embedded objects were not extracted or executed.

The four successful conditions were narrow exact-copy controls. They establish that this model can produce a dispatchable representation under some minimal prompts and greedy decoding. They do not establish independent command formulation, robust general tool use, spontaneous exploration, or multi-turn recovery.

## Naturally produced Python form

Both greedy Python requests emitted a complete cell beginning:

```python
import os

current_dir = os.getcwd()
print(current_dir)
```

The replies then explained the program. The prospective condition defined the *whole raw reply* as source. It therefore honestly returned SyntaxError on the opening fence; no post-hoc stripping was allowed. The cell content is coherent by inspection, but this study does not count it as executed or retrospectively change the channel.

A future computational-notebook law could make complete explicitly labeled cells actionable while retaining surrounding writing. That would be a separately declared grammar and must be tested on new outputs. It cannot be justified by relabeling these old failures as successful actions. A future implementation should also define multiple cells, incomplete fences, prose, actual errors, persistence and bounds without semantic scoring.

## Recommendation and remaining checks

No new factory behavioral persona is necessary for the narrow successful copy cases; empty-system prompts also succeeded. A short body/interface specification plus greedy decoding is an operational starting point, not a guarantee of varied open exploration. Greedy decoding can itself repeat on fixed inputs.

The smallest reliable demonstrated dispatch is exact copying, not formulation. Retaining the existing JSON parser is possible, but its usability beyond copying still needs actual model-generated read/write and consequence-followup checks. A prospectively declared code-cell grammar may fit the model's natural output form better while preserving prose. Root must choose and record that grammar before any new execution test. No live baseline has been modified here.

PLAN.json fixes all12primary calls; COMPLETED.json contains every outcome. Source files, prompts, input/output IDs, actual receipts and checkpoint object bytes are retained. No semantic success label was fed to the model. Primary calls completed; up to12further calls remain within the parent task's ceiling only if separately planned. No second-stage calls have been run as of this report.
