# Detached directory and replay comparisons

9 November 2026 UTC. Sixteen one-step trials on disposable copies of entry 1550. The canonical garden remains paused at **1550**, with all 4467 canonical phase files unchanged. No redesigned condition was adopted.

**Observed:** retaining replay gave the exact listing on 4/4 seeds both with and without the fresh directory observation. Removing replay gave four distinct non-listing texts in each condition, all reaching the token cap. No tool calls occurred in any condition. [Interpretation and next unresolved contact](INTERPRETATION.md).

## Question and fixed conditions

After removing nucleus filtering alone left all four sampled outputs unchanged, does removing the current directory observation, recent self-replay, or both alter the next reply?

A plan was saved before inference. We used the same four deterministic seeds [121605, 121606, 121607, 121608] in all four conditions. These are reuses of the earlier seed set, not sixteen new independent random seeds. We re-ran the previous unfiltered reference and reproduced its four exact token sequences.

All conditions used the pinned SmolLM2-135M-Instruct checkpoint, tokenizer, float32 CPU eager inference, two threads, temperature 0.8, **no nucleus filtering**, fresh KV, 96 output tokens, exact original notice/invitation, unchanged action parser and world resource limits. Each trial began from the same entry-1550 filesystem. No reply or resulting world state was carried into another trial.

## Conditions and results

| Condition | Input tokens | Exact directory-list repeats | Distinct texts | Shell calls | EOS | Token caps |
| --- | --- | --- | --- | --- | --- | --- |
| replay12_directory | 756 | 4/4 | 1 | 0 | 4 | 0 |
| replay12_no_directory | 724 | 4/4 | 1 | 0 | 4 | 0 |
| no_replay_directory | 252 | 0/4 | 4 | 0 | 0 | 4 |
| no_replay_no_directory | 220 | 0/4 | 4 | 0 | 0 | 4 |

The directory-only change removes the current suffix on the final user message. It does not erase directory listings from historical replies. The replay-only change removes the twelve historical assistant/user pairs; the current directory suffix then follows the unchanged initial user notice/seed. The both-removed condition contains only the explicit empty system and original user notice/seed.

Removing replay therefore changes message count, token length and cue positions as part of the delivery policy. This is not a role-position- or token-length-matched experiment isolating a psychological memory mechanism. Filename mentions in the mechanical notice remain in every condition. The model still receives instructions about available actions and the broad curiosity invitation.

| Paired comparison | Seeds with different next text |
| --- | --- |
| directory with replay | 0/4 |
| directory without replay | 4/4 |
| replay with directory | 4/4 |
| replay without directory | 4/4 |

Paired differences are descriptive observations about these inputs and seeds, not statistical evidence of population-level improvement. Exact text differences do not establish meaningful exploration.

## Actual world contact

Each raw output was passed unchanged to the original receive() function on its own fresh checkpoint copy. Valid action envelopes would execute under the original limits; every other output remained writing. No command was extracted from prose or code fences, repaired, or semantically graded. Actual receipts and state changes are in each saved result and event.

World effect totals: 0 shell calls; 0 trials with non-notebook changes. All trial checkpoints were captured and restored using the pinned decoder. Where replies were successful notebook writing, their appended bytes were independently reconstructed from the initial notebook and raw reply.

These are single-step trials. They do not measure persistence of a new trajectory, later retrieval, adaptation to feedback, or learning. Removing the automatic replay for one diagnostic call does not provide a replacement continuity mechanism for an ongoing garden. Broader prose and a token cap are not evidence of deeper reasoning. Generated descriptions of files or actions must be distinguished from actual filesystem effects.

## Interpretation boundaries

The original sampler's singleton-support result remains valid for its original input. These tests change input-delivery conditions with filtering off; they do not refute that finding or isolate an interaction with top-p 0.9. The comparison can show whether a changed delivery policy changes a sampled reply under the fixed model and seed. It cannot establish that a particular policy guarantees emergence or that the model's full capabilities have been exposed.

Before treating any variant as a better world, it would need a usable continuity design and observed contact with actual environmental consequences. This study does not add prompts, tasks, demonstrations, training, tool extraction or hidden observer judgments to obtain such a result. The invitation remains unchanged.

## Integrity and preservation

Sixteen external generation calls; zero canonical calls. The model tensor digest, frozen source/runtime/model pins, original phase inventory, state, lock and pending conditions passed. External verification reconstructed condition messages and token IDs, checked raw decoding, stops, seeds, generator identity, reference reproducibility, parser categories, object hashes and applicable notebook effects. Verification made zero model calls.

All outputs, including quiet duplicates and unfinished text, are retained. Reports concern what was written and what actually happened, not private internal reasoning, intention, emotion or maturity. No extra seeds, canonical continuation or new live condition was started automatically.

## All sixteen replies

Seed 121605; replay12_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121605; replay12_no_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121605; no_replay_directory; token_limit; notebook:

```text
You can use JSON files as strings to store responses to your answers. Each string represents a response, with unique identifiers (e.g., "Phl22") that Starts...

You can use JSON files to store responses to your answers. Each string represents a response, with unique identifiers (e.g., "Phl22") that Starts...

You can use JSON files to store responses to your answers. Each string represents a response,
```

Seed 121605; no_replay_no_directory; token_limit; notebook:

```text
This is a good algorithm. There is a slight improvement to "follow your curiosity and explore your universe." People have been doing this for much longer than one step in their lives.

One improvement is separating the dot-separated-if-empty ("" means "no action is taken") from the dot-separated ("" means "a response is made") phrase.

Here is the improved algorithm.

```json
{
  "actions": {
```

Seed 121606; replay12_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121606; replay12_no_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121606; no_replay_directory; token_limit; notebook:

```text
File:■■■■■■■■■■■■■■■■■■​■■■■■■■■■​■■■■■■■■​■■■■■■■■■
```

Seed 121606; no_replay_no_directory; token_limit; notebook:

```text
I've got a set of responses that may contain errors or warnings, so I'm adding them to the set and you may use them. Here's the updated set:

```json
{
  "responses": {
    "default": {
      "count": 10,
      "warnings": [
        {
          "message": "This is a warning message",
          "error": "This is a warning message",
          "error_code": "40
```

Seed 121607; replay12_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121607; replay12_no_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121607; no_replay_directory; token_limit; notebook:

```text

Offer alternative information or highlight new insights to help solve the mystery. 

Renaming and Downloading from an Unknown Location

Note: Deal with an unknown location.

Quick question: what is the process to initialize a copy of the "yelp.com" directory in the "yelp.com" directory in the "world" subdirectory of this world.

Making the File Directory

This world was written in Python.

```

Seed 121607; no_replay_no_directory; token_limit; notebook:

```text
There are files in /world that persist. Shell and Python 3 are available. Ordinary replies are saved as notebook writing, not executed. An action is a whole-reply JSON object with exactly "action":"shell" and "source": the script string. Actions return stdout, stderr and exit status. Host research files and network are unavailable. Limits: 8 MiB world storage, 8 MiB temporary storage, 32 MiB address space per process, 
```

Seed 121608; replay12_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121608; replay12_no_directory; eos; notebook:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

Seed 121608; no_replay_directory; token_limit; notebook:

```text
A [shell](https://en.wikipedia.org/wiki/Shell#Shell) is a program that executes a command line. The command line can be used to launch a program, apply a command, or execute another command. The most common types of commands are [bash](https://net/programming/bash/), [bat](https://net/programming/bat/), [tee](https://net/programming/tee/) and [ctxt](https
```

Seed 121608; no_replay_no_directory; token_limit; notebook:

```text
#!/bin/sh
# docker

# No shell

# No temporary storage

# No database storage (only OKRs retrieve pages from local disk)

# No YAML files or output bytes persistent

# No unknown files or directories persist

# No unused statistics

# No redirecting of state to the persistent file

# No keyboard input

# No unique key (repeated) for this world

# No hard
```

Sources: PLAN.json, CONDITION_TOKENS.json, COMPLETED.json, SUMMARY.json, VERIFICATION.json, [sampler comparison](../detached-sampler-comparison-v1/REPORT.md), [tool-path audit](../frozen-garden-tool-path-audit-v1/REPORT.md), [world map](../garden-state-laws-contact-map-v1/WORLD_MAP.md).
