# Three contacts: observation, decoding and prompted retrieval

The run was planned13 November2026 and reviewed14 November2026, America/Chicago. The local worker completed during the assistant usage interruption:15 planned replies and one extra teacher-forced profile pass were retained. No completed generation or sandbox action was rerun after the reset. Main remains1580 with unchanged weights, source and selected phase.

| Contact | Actual result | Supported interpretation |
|---|---|---|
| Truthful observations | Three different inputs, same old unfinished output;0code cells | These supplied facts did not change the visible greedy reply; not proof of absent perception or representation |
| Decoder support | Top-p.9:3/3 old repeats. Top-p1.0:3 distinct texts,2 new variants. All0cells | Sampling can alter text here, without demonstrated action improvement |
| Prompted file retrieval | Six replies; four cells exit0 but parse a filename as JSON text. No target value appears | Process completion and goal success differ; valid file data was not actually read by those cells |

## Experiment1: actual world facts

The label-only control receives an empty operator-observation object. Two other cases receive true measured notebook/history facts from saved before/after worlds:124576 bytes/30 records versus127237 bytes/33 records. The exact base input is otherwise the same2231-token view. Label-only input is2240 tokens; factual inputs2261 each. All three changed inputs map to the same256-token unfinished reply. No count-dependent objective was assigned to this free-writing condition, so task accuracy is not defined here. Different observations can legitimately share an action; no internal-perception claim is inferred. [Detailed report](observation/REPORT.md).

## Experiment2: changing the decoder

Three paired seeds compare top-p0.9 and1.0 at fixed temperature0.8 and identical input. Default nucleus output repeats three times. Full-support sampling changes two of three texts but produces no complete cell. Along one saved greedy path, the default nucleus has one available token at255/256 positions and two at one position. The profile is path-specific and numerically approximate relative to incremental generation. [Detailed report](decoder/REPORT.md).

## Experiment3: file access versus supplied information

Two hidden-file worlds differ only in one valid JSON value. The values are absent from their identical inputs. A third control has the same first world plus its authentic operator read receipt supplied explicitly. Each gets a marked reading task and one subsequent actual-feedback turn; this is a prompted diagnostic, not an open-garden instruction or new behavioral requirement.

The hidden branches produce identical inputs and replies on both turns. Their four complete cells call `json.loads` on the filename string instead of opening the file. They catch the resulting parse error, print an invalid-JSON message and None, and exit0. Their source files are valid; there is no observed filesystem blockage. In the supplied-read control, the target is present in the input but the model returns old unfinished network-program text; no target appears in the response or stdout. These are narrow failure observations, not a general inability claim. [Detailed report](retrieval/REPORT.md).

## Ground and verification

Every generated complete cell runs unchanged within its own copied sandbox. Known errors remain consequences; the second retrieval turn receives only the actual first reply and projected receipt. No answer hint, sample promotion or forced syntax repair follows an outcome. The probe transport is declared in each fixture's rules: selected source view plus explicit operator probe and at most one actual followup; old archive files are fixture data, not automatically extended by this lab.

`WORKER_PLAN.json`, job inputs, exact raw token IDs, code/receipt batches, world events/objects and final verifiers preserve all outcomes. Metadata, labels and expected values are not inserted into model input. Hidden-world and supplied-read controls have supported-file equality audits. Source/canonical preservation is asserted by the worker and checked independently; no main-world count or policy changed.

The primary-source scout distinguishes partial observability, selection, information access and consequential use; it does not establish a mechanistic diagnosis of this model. [Scout with access depths](scout/SCOUT.md). No fresh-model download or paid inference endpoint was used.

## What this changes in our understanding

There are separate gates in the evidence chain: a fact exists, it is available, it reaches input, it affects output, an action executes, and the action achieves its specified effect. This contact gives counterexamples to merging those layers. In particular, exit0 is not a goal verifier, altered text is not a successful action, and a host archive is not automatically a model-accessible memory.

The next research pass should seek methods and counterexamples around those distinctions, including task-state verification, representation/reference errors, active observation, and memory-view evaluation. Keep all suggested changes separate from main adoption. The main garden remains1580; no background continuation is scheduled.
