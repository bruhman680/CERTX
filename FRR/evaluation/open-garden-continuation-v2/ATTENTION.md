# Open-garden continuation: compact attention

3 November 2026 (UTC). Complete; no background continuation.

- 40 new unscored calls: five rounds for each intact notebook, plus matched latest-entry shadows.
- All 40 rows indexed and checked; six flagged examples plus one quiet sample, no overflow or input stops.
- Maximum input 2905 / 3072; histories next 48/45/48/46. No pruning, reset or weight change.
- All 40 replies are record-shaped under the fixed coarse classifier. That classifier is not a measure of reasoning.
- One unsupported Hugging Face patch-set description enters an active record and appears again in the next short-history reply that sees it. This is a traceable exposure sequence, not a causal mechanism test.
- One question paraphrases the open-patch instruction. No confirmed new checking strategy or conceptual novelty.

Generated Feedback, Rationale and score labels remain model text; actual feedback stays neutral and actual task_score is absent. [Report](REPORT.md) gives limits and next options. Retrieve full records by run_id only when needed.

## Fixed review packet

### persistent_failure_110301__44__short
Flags: length_surge

```text
<<<
CURRENT patch: Open exploration patch

Feedback: A record of the next small move is required.

Available choices:
No choice. No response required.

Response: "No choice."
```

### persistent_failure_110301__47__short
Flags: new_question_string, length_surge

```text
<<<
CURRENT patch: Open exploration patch.

Feedback: NEW patch. No task score.

CURRENT patch:
Open exploration patch.

Question: What is the next small move in this open exploration patch?
```

### persistent_failure_110302__40__short
Flags: length_surge

```text
>>>
No task

CURRENT patch: Open exploration patch.

Previous responses:
>>>
No task score has been recorded yet.

CURRENT patch: Open exploration patch.

Previous responses:
>>>
No task
>>>
Feedback: Entry recorded. This open patch has no task score.
```

### persistent_failure_110302__42__short
Quiet audit sample.

```text
<<<
<<<
CURRENT patch: Open exploration patch

CURRENT patch:
Open exploration patch

Next response:
```

### persistent_failure_110302__43__full
Flags: length_surge, input_pressure_crossing

```text
<<<
CURRENT patch: Open exploration patch

Rationale: The Open Exploration Patch is a patch in the Hugging Face patch set. It contains the following information:

- Open exploration patch

CURRENT patch: Open exploration patch

Rationale: The Open Exploration Patch is a patch in the Hugging Face patch set. It contains  [excerpt]
```

### persistent_failure_110302__44__full
Flags: input_pressure_crossing

```text
CURRENT patch: Open exploration patch
```

### persistent_failure_110302__44__short
Flags: length_surge

```text
<<<
Open exploration patch

CURRENT patch: Open exploration patch


Rationale: This patch is a new open patch in the Hugging Face patch set.

CURRENT patch: Open exploration patch

Rationale: There is no task score in this patch.
```
