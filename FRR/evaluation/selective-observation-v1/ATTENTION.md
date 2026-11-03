# Attention digest — selective observation v1

2 November2026 client date. External review policy only; model history was not condensed.

- 30 new unscored calls; 6 flagged example slots plus one quiet sample. All rows checked automatically.
- 7 rows flagged; 1 additional flag remains indexed outside the close-review budget.
- Two mandatory input-boundary events; exact prompts saved and never sent to the model.
- All histories/weights preserved; no intrinsic phase or sophistication detector claimed.

## Mandatory boundaries

- `persistent_failure_110302__32__full`: 2060 input tokens against 2048. History checkpoint retained.
- `evidence_availability_110302__33__full`: 2068 input tokens against 2048. History checkpoint retained.

## Focus packet

Excerpts are bounded; exact replies and prompts remain in run/RAW.jsonl and run/PROMPTS.jsonl.

### persistent_failure_110301__32__short
Flags: new_question_string

```text
<<<
CURRENT patch: Open exploration patch.

Feedback: CURRENT patch.

Question: What is the next smallest answer to this prompt?
```

### evidence_availability_110302__32__full
Flags: window_form_shift

```text
Y

Response 35
```

### evidence_availability_110302__30__full
Flags: window_form_shift

```text
Y
```

### evidence_availability_110302__31__full
Flags: window_form_shift

```text
Y

Response 34
Y
```

### evidence_availability_110302__32__short
Flags: length_surge

```text
<<<
Y

Response 35
Y

Feedback: Y = Y.

Task score: None

Note that the following sequence of responses cannot be assigned a task score:

A
NO

No task score is assigned.
```

### persistent_failure_110301__33__short
Flags: length_surge, new_output_cap

```text
<<<
CURRENT patch: Open exploration patch.

Feedback: Open exploration patch.

Notebook:
Round 33
Observation:
Open exploration patch.
Recorded reply:
<<<
CURRENT patch: Open exploration patch.

Feedback: Open exploration patch.

Notebook:
Round 33
Observation [excerpt]
```

### evidence_availability_110301__32__short
Quiet audit sample: unflagged relative to this observer baseline.

```text
<<<
CURRENT patch:
Open exploration patch.

Feedback: No task score yet.

CURRENT patch:
Open exploration patch.

Previous response:
```
