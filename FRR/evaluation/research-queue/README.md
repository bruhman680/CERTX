# Research queue: HPGM gates and retained-memory follow-ups

This is a saved dependency-aware plan, not a running scheduler. It queues every explicit HPGM test direction from [the post review](../HPGM_POST_CONTACT.md), the nearest unresolved relay/RR1 contacts, and references older test families rather than replacing their detailed records. It does not claim a new exhaustive audit of every historical CERTX statement.

**Current status:** 33 entries: two completed prior research contacts, one checked software instrument, and 30 unfinished research/source entries. One unfinished entry now has a partial subreddit contact. A family can contain several eventual trials. The queue is not evidence those trials ran.

The machine-readable source of current queue status is [QUEUE.json](QUEUE.json). Prioritized entries have question, comparison, outcomes, prerequisites, dependencies and a result reference only when appropriate. Lower priority number means nearer contact; it does not mean scientific importance or evidential confidence.

## Nearest work

- **HG1 / HPGM-01 and HPGM-03:** [protocol draft](../hpgm-gates-study/PROTOCOL_DRAFT.md), comparing operations and labels and testing the next reader. Cases, exact actor/reader text, keys and cost instrumentation still need preparation before launch. The proposed 96-call development cap is a planning setting, not an executed run.
- **CAL-TOOLS:** forecast scorer is implemented and four known-answer software tests passed. [Scope/input](FORECAST_TOOL.md) and [actual test output](FORECAST_SOFTWARE_CHECKS.txt). No actor forecasts were collected.
- **RR2:** unknown-preparation mixture reader is the nearest numerical follow-up to [RR1](../RESET_READER_STUDY.md). Its prospective mixture rule and acceptance conditions still need freezing; no second reset-reader result exists.
- **SOURCE-REDDIT:** URL received; [first pass](../SUBREDDIT_FIRST_PASS.md) records six selected posts and incomplete access. ARCHIVE-01 and FIELD-01 capture two new test directions. Broader source coverage remains pending.

## Status meanings

`protocol_draft` is a concrete design with open prerequisites, not final registration. `queued` is an unexecuted test or family. `blocked_inputs` identifies missing evidence/model definitions. `awaiting_url` identifies an offered source still awaiting a URL; `partial_contact` has an actual scoped report plus explicit remaining coverage needs. `completed_prior_scope` refers only to an existing scoped report; `instrument_checked` means software fixtures passed, not that a scientific hypothesis succeeded. No background process will silently change these states.

## Entries

| ID | Test or source contact | Status | Priority | Dependencies |
|---|---|---|---:|---|
| PRIOR-RR1 | Reset-reader finite comparison | completed_prior_scope | 0 | — |
| PRIOR-RECOVERY | Fresh-reader recovery pilot | completed_prior_scope | 0 | — |
| CAL-TOOLS | Forecast scoring instrumentation | instrument_checked | 1 | — |
| HPGM-01 | Operations versus phase labels | protocol_draft | 1 | CAL-TOOLS |
| HPGM-02 | ORIENT and DREAM ablation | queued | 2 | HPGM-01 |
| HPGM-03 | Closing record judged by next reader | protocol_draft | 1 | HPGM-01 |
| HPGM-04 | Review versus extra generation versus retrieval | queued | 2 | HPGM-01 |
| HPGM-05 | Literal waiting intervention | queued | 3 | HPGM-04 |
| HPGM-06 | Flow/pause schedule sweep | queued | 3 | HPGM-02, HPGM-04 |
| HPGM-07 | Calibration and skip-review effect | queued | 2 | CAL-TOOLS, HPGM-02 |
| HPGM-08 | Cycle frequencies and nesting | blocked_inputs | 4 | — |
| HPGM-09 | Architecture transfer | queued | 4 | HPGM-01, HPGM-07 |
| HPGM-10 | Original quantitative-claim reconstruction | blocked_inputs | 4 | — |
| HPGM-11 | Phase count and ordering | queued | 3 | HPGM-01, HPGM-02 |
| HPGM-12 | Adaptive versus fixed gates | queued | 3 | HPGM-02, HPGM-04 |
| HPGM-13 | Physical analogy boundary | blocked_inputs | 5 | — |
| RR2 | Unknown reset-preparation reader | queued | 1 | PRIOR-RR1 |
| MEM-01 | Probability-weighted backward states | queued | 2 | — |
| MEM-02 | Boundary-channel identity and dissipation | queued | 2 | — |
| MEM-03 | Robust mixture recovery | queued | 2 | — |
| MEM-04 | Real-agent provenance and moving context | queued | 2 | HPGM-03, RR2 |
| LEGACY-01 | Field/log observers and probe disturbance | queued | 4 | — |
| LEGACY-02 | Wake-to-law escape and reversibility | queued | 4 | — |
| LEGACY-03 | Transformer context/cache controls | queued | 4 | — |
| LEGACY-04 | Optimizer consistency versus curvature | queued | 4 | — |
| LEGACY-05 | General FRR effectiveness | queued | 4 | — |
| LEGACY-06 | Role rotation and evidence lineage | queued | 4 | — |
| LEGACY-07 | Swarm boundaries and scale | queued | 5 | — |
| LEGACY-08 | Shared-weight subspace robustness | queued | 5 | — |
| LEGACY-09 | DecepEval actor/evaluator contact | queued | 5 | — |
| SOURCE-REDDIT | Subreddit timeline and idea scouting | partial_contact | 1 | — |
| ARCHIVE-01 | Claim scope across rewrites | queued | 2 | — |
| FIELD-01 | Shared readout validity versus coordination | queued | 2 | — |

## Start and completion rules

Choose one ready question; inspect the linked source and unresolved prerequisites. Use the [bounded loop](../../modules/bounded-experiment-loop.md) and [trial card](../../examples/bounded-trial-card.md) or an equivalent existing protocol. Freeze a specific candidate, evaluator, data split and budget before outcome collection. Preserve rejected candidates and evaluator repairs. Do not promote a test to complete merely because its protocol or checker exists.

Update QUEUE.json with an actual result reference and narrow scope after execution; revise this navigation view with it. Keep raw results and prior commit layers. A queue validator checks IDs, dependencies, status/result consistency and local references; it cannot determine scientific validity or make an agent follow the plan.

## Subreddit intake: partial contact

Read the supplied URL and accessible linked posts as a historical idea/source collection. Preserve permalinks and observed dates/edits, distinguish the user's wording from quoted model outputs, follow primary evidence where consequential, and link corrections instead of treating chronology as cumulative proof. Trace cross-post and shared-model ancestry so repetition is not counted as independent confirmation. Keep author interpretation separate from code/results. For promising ideas record a concrete question, existing related contact and a possible discriminating test; useful play need not already be a validated claim. Mark incomplete access rather than imply the whole subreddit was read. The URL has now been supplied. [First-pass report](../SUBREDDIT_FIRST_PASS.md) and [catalogue](../../lineage/subreddit/FIRST_PASS_CATALOG.json) record what was inspected. Earlier queueing-check receipts remain historical and do not describe current access. Broader browsing is still pending.
