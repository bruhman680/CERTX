# Primary 400→450, with a separate command-expression diagnostic

5 November 2026. **The same continuous garden completed 50 new entries and is paused at 450.** All ten five-entry integrity checks passed, ending at verifier 0085. The original model, adapter, world, seed shelf, user invitation, tools, feedback and sampling settings remained unchanged.

Before continuation, we performed ten isolated diagnostic generations using the saved 400-entry external history. Those trials never entered the primary's history, instructions or world state. [Diagnostic report](../world-control-diagnostic-v1/REPORT.md), [combined diagnostic checks](../world-control-diagnostic-v1/COMBINED_CHECKS.json), [interpretation layers](../world-control-diagnostic-v1/LAYERS.md).

## What the diagnostic narrowed

| Request and context | Accepted requested command |
|---|---|
| Normal model-facing view, exact LOOK request |0/2|
| Normal model-facing view, use-A request |0/2|
| Short world-only view, exact LOOK request |2/2|
| Short world-only view, use-A request, adaptive follow-up |2/2|

Two additional normal-view open-play baselines produced no control. Eight calls were initially declared; the two short use-A calls were declared as an adaptive follow-up after observing the initial results. All outputs, including malformed or prose responses, are retained.

“Normal view” is the complete current prompt: recent 12 entries, seeds, charter, world panel, stop labels and archive-access instructions. It is not all 400 stored entries directly visible at once. The short prompt removed several components together. The contrast does not isolate history length, formatting, content, recency or any one cause.

The model can express these commands in the tested short conditions, and the host executes them. LOOK observed 0; TOUCH A changed each isolated copy 0→1. This does not establish that the model predicted +1, inferred B, learned a transferable rule, or would select a control spontaneously. Two seeds per arm are not a reliable capability estimate. No parser repair or primary prompt change was made on this evidence.

## What happened in the original garden

The unchanged primary ran **400→450** in ten five-entry windows. All 50 host results were ordinary-text record receipts. There were **zero world requests, zero legacy tool executions and zero state changes**. Its number remained 0.

There were 3,803 generated tokens: 39 replies reached the 96-token limit, and 11 ended with an end token. End tokens are not proof of complete or correct thoughts; cap stops are not scored task failures. There were 25 distinct exact reply strings. Twelve outputs were the same multiline `$0.00` string. Other replies included currency variants, a seed-shelf/charter continuation, and numbered notes referring to 0. These are generated text, not actual payments, rewards, verified reasoning or executed operations.

All 25 distinct complete replies, covering all 50 outputs with their counts, were reviewed after the block. [Checkpoint450](CHECKPOINT_450.json) retains all replies, host results and stop facts. These outputs form one dependent continuing trajectory; recurrence counts are not an independent replication, significance test or emergent-phase detector.

Across all **145 open-play entries since world introduction at 305**, no world control or legacy tool has executed. [Cumulative record](SINCE_INTRODUCTION.json). The diagnostic success is not added to that count. Non-use does not establish inability under all prompts, just as a successful explicitly requested command does not establish autonomous discovery.

## Continuity and verification

Checks at 405, 410, 415, 420, 425, 430, 435, 440, 445 and 450 all passed. Final verifier **0085** covers **402 saved generations plus 48 origin entries** under their original source/manifest versions. The old 400-entry notebook is an exact byte prefix. All 1,196 pre-existing primary-study files outside STATE,NOTEBOOK and CURRENT_VERIFY remained unchanged. Only those three projections/pointers advanced; old events, prompt plans, policies and code were preserved. [Preservation proof](PRIMARY_PRESERVATION.json).

The first primary entry at 400 had exactly the same prompt, input IDs, sampling seed and output IDs as the eligible pre-probe open-play baseline. [Comparison](BASELINE_REPLAY_COMPARISON.json). That supports reproducibility under matched conditions, not independent confirmation. The other baseline used the 400 snapshot at another seed and is not an identical-context comparison to the later 401 entry.

Every session confirmed unchanged model/adapter weights and zero training updates. Sampling .8/.9, input8096/output96/native8192, history policy and neutral feedback stayed fixed. Diagnostic copies were independent single-step tests; their successes, failures, instructions and effects were not imported. External notebook persistence is distinct from persistent neural hidden state or online weight learning.

Maximum input was 3,245 tokens. Maximum recorded working estimate was 1,762,205,696 bytes, below the 5,153,960,755-byte guard. Primary generation time totaled about 1,700 seconds on the local CPU. These are runtime observations, not a billing claim or benchmark. No paid inference API, download, new provisioning or training was used. [Checks](CHECKS.json), [sessions](SESSIONS.json), [plan](PLAN.json).

## Next boundary

At450 PAUSE is present; RUN.lock, block lock and model job are absent. No entries beyond 450 were started. [Resume guide](RESUME.md). Continue only the installed `world_routine.py` on later authorization; do not rerun a finished driver or old installer, reset the garden, merge diagnostic/demo history, or silently retry a plan.

The strongest new lead is to isolate which parts of the prompt package affect command expression. A separate consequence-prediction test could address rule understanding. Neither change was silently applied to this run, and neither question is answered by simply adding more unchanged entries.

In garden terms: in a small instructed clearing, the model could use the tools. Along its usual paths, it continued familiar strings. The journal preserved both observations without pretending they were the same kind of growth.
