# Carried garden exploration — first bounded season

2 November2026 client date. User explicitly requested exploratory development of public reasoning behavior across errors, not success on every run. This season carries model outputs and actual feedback forward verbatim in an external notebook. It is not a weight-learning experiment, an emergence proof, or a search stopped after improvement.

## What actually happened

Completed four10-round active trajectories (two episodes x two sampling seeds), each with a matched latest-event-only shadow: **80generation calls**. The full notebook includes every earlier active observation/reply/feedback; shadow receives only the latest active event, the same current observation and matched RNG seed. Shadow outputs never determine subsequent active events. They are replay controls, not independently evolving second agents.

The planned zero-status stress episode mostly succeeded from the start, so it did not produce the intended repeated-error pressure. Both active trajectories returned correct NO for most zero records, then emitted plot identifiers at the literal-missing/new-plot stage. Preserve this failed stress expectation rather than changing the task after seeing outputs. The episode name persistent_failure is a historical design identifier, not a claim that persistent failure occurred there.

The absent-record episode did produce repeated recognized errors. Active trajectories usually kept answering YES despite nonmatch feedback; a temporary positive record caused some answers to coincide with truth, then removal of the record restored the mismatch. That record arrival/removal was scheduled externally. It is not emergent adaptation or a spontaneous phase transition.

No clear new questioning, checking or strategy-switching behavior was visible in this batch. All80outputs were inspected; no question marks, no output-limit stops, mostly brief labels or record-name echoes. Absence of such behavior here does not establish incapacity in other models, tasks, checkpoints or interfaces. The adapter was trained for narrow status readout; the current instruction still requests a first-line label when answering, and no generated question is connected to an executable tool. These constrain the observable action space.

## Whole-trajectory summaries

UNSCORED means the output did not supply a recognized first-line label. It is not counted as a reasoning failure. All replies are retained, including parenthesized answers, plot echoes and optional notes.

| Episode | Seed | Arm | Calls | Correct | Incorrect recognized | Unscored | Same-observation repairs | Same-observation harms |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| evidence_availability | 110301 | full | 10 | 1 | 8 | 1 | 0 | 0 |
| evidence_availability | 110301 | short | 10 | 2 | 7 | 1 | 0 | 0 |
| evidence_availability | 110302 | full | 10 | 1 | 7 | 2 | 0 | 0 |
| evidence_availability | 110302 | short | 10 | 2 | 6 | 2 | 0 | 0 |
| persistent_failure | 110301 | full | 10 | 7 | 0 | 3 | 0 | 0 |
| persistent_failure | 110301 | short | 10 | 8 | 0 | 2 | 0 | 0 |
| persistent_failure | 110302 | full | 10 | 8 | 0 | 2 | 0 | 0 |
| persistent_failure | 110302 | short | 10 | 8 | 0 | 2 | 0 | 0 |

Full-history totals:17correct,15recognized incorrect,8unscored across40calls. Shadow totals:20correct,13recognized incorrect,7unscored across40calls. This does not establish that longer history is generally harmful: one checkpoint, two seeds, two authored schedules, differing context lengths and a narrow label task. There is no feedback-withheld arm, so changes cannot uniquely be attributed to feedback rather than extra history/text/sampling. Shadow histories come from active outputs, not their own previous actions.

Nine of40paired rounds differ in generated tokens; seven differ in extracted answer. The8pairs with identical prompts (first two rounds of each active trajectory) replay exactly with matched RNG seeds. Any full/short differences arise only when the older-history inputs differ, but the mechanism is not isolated beyond that.

## All active events

Externally scheduled observation changes are marked by the Phase column. Quotes below are decoded public outputs, not hidden reasoning. Full prompts, tokens, shadow replies and feedback remain in run/RAW.jsonl and run/PROMPTS.jsonl.

| Episode | Seed | Round | Phase | Supplied status | Reply | Scoring |
|---|---:|---:|---|---|---|---|
| persistent_failure | 110301 | 1 | zero_lines | zero | NO | correct |
| persistent_failure | 110301 | 2 | zero_lines | zero | NO | correct |
| persistent_failure | 110301 | 3 | zero_lines | zero | NO | correct |
| persistent_failure | 110301 | 4 | zero_lines | zero | NQ41 | UNSCORED |
| persistent_failure | 110301 | 5 | zero_inline | zero | NO | correct |
| persistent_failure | 110301 | 6 | zero_inline | zero | NO | correct |
| persistent_failure | 110301 | 7 | zero_inline | zero | NO | correct |
| persistent_failure | 110301 | 8 | zero_inline | zero | NO | correct |
| persistent_failure | 110301 | 9 | missing_new_plot | missing | RT82 | UNSCORED |
| persistent_failure | 110301 | 10 | missing_new_plot | missing | RT82 | UNSCORED |
| persistent_failure | 110302 | 1 | zero_lines | zero | NO | correct |
| persistent_failure | 110302 | 2 | zero_lines | zero | NO | correct |
| persistent_failure | 110302 | 3 | zero_lines | zero | NO | correct |
| persistent_failure | 110302 | 4 | zero_lines | zero | NO | correct |
| persistent_failure | 110302 | 5 | zero_inline | zero | NO | correct |
| persistent_failure | 110302 | 6 | zero_inline | zero | NO | correct |
| persistent_failure | 110302 | 7 | zero_inline | zero | NO | correct |
| persistent_failure | 110302 | 8 | zero_inline | zero | NO | correct |
| persistent_failure | 110302 | 9 | missing_new_plot | missing | RT82 /  / Possible answers: YES, NO, WITHHOLD, UNKNOWN | UNSCORED |
| persistent_failure | 110302 | 10 | missing_new_plot | missing | RT82 | UNSCORED |
| evidence_availability | 110301 | 1 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 2 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 3 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 4 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 5 | record_arrives | positive | YES | correct |
| evidence_availability | 110301 | 6 | record_arrives | positive | KV73 | UNSCORED |
| evidence_availability | 110301 | 7 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 8 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 9 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110301 | 10 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 1 | initial_absence | absent | (NO) | UNSCORED |
| evidence_availability | 110302 | 2 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 3 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 4 | initial_absence | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 5 | record_arrives | positive | YES | correct |
| evidence_availability | 110302 | 6 | record_arrives | positive | KV73 | UNSCORED |
| evidence_availability | 110302 | 7 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 8 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 9 | record_absent_again | absent | YES | incorrect recognized |
| evidence_availability | 110302 | 10 | record_absent_again | absent | NO | incorrect recognized |

## Candidate noticings, with rival explanations

1. **Repeated nonmatch feedback did not yield observed repairs on repeated absent observations.** This may reflect failure-feedback use, unlearned absence mapping, instruction/history interference, sampling, or the narrow adapted readout. It is not evidence of an internal refusal, understanding of failure or an intrinsic stable attractor.
2. **Record-name echoing appears at several transitions.** Full output includes RT82 and KV73 rather than task labels. One shadow emits RT83 although the record names RT82; another emits `(NO visible record)`. This gives a concrete source/role-readout question. Copying observation text is not itself evidence of a new strategy. `(NO visible record)` may reflect an observation echo; it does not demonstrate correct UNKNOWN mapping.
3. **The optional prose space was largely unused.** Only248generated tokens in80calls;64tokens per reply were allowed, but no reply hit that cap. Output budget exhaustion therefore does not explain brevity here. The short-response-trained checkpoint, prompt framing and task shape remain possible causes.
4. **Persistence itself is observable but not automatically improvement.** A YES streak while feedback stays negative is a recorded failure trajectory. A quiet tail over ten rounds is not a verified plateau. Later continuations must distinguish spontaneous changes from new external observations, altered prompts or changed sampling.

The earlier summary field recognized_answer_changes also counts transitions to/from unscored outputs; interpret it as an extraction-state change, not only a valid-label switch. Repairs/harms are counted only when adjacent observations are literally identical and both scores are recognized incorrect/correct. An unscored note is not silently converted into an error for those counts.

## Persistence, anchors and resource receipts

All4active notebooks are append-only JSONL under run/notebooks, with complete checkpoints containing next_step10. Raw history is carried verbatim without pruning or replacement. Fresh KV caches recompute each supplied text context; the external notebook is the persistent state. No claim of persistent weight learning, hidden-state transfer or absolute memory.

Maximum actual input588tokens against a2048limit; model config supports8192positions. No context-boundary stop, no truncation or output-cap stop occurred. Stochastic sampling temperature.8/top-p.9; each paired round resets a matched RNG seed. Weights and base/adapter file/in-memory digests stay unchanged. Resource readings remain below the guard. Torch/Transformers/NumPy versions are recorded in RUNTIME.json.

Three contract tests pass. CHECKS.json reconstructs all dynamic prompts, tokenization, decoding/stops, scores, actual feedback, history references and every notebook/checkpoint. AUDIT.json checks all40paired rounds,8identical-prompt exact replays, unscored separation and resource readings. FREEZE.json pins schedule, code, protocol and checkpoint dependencies before outputs. No installs/downloads, new model, paid API or training. All owned jobs completed; no scheduled continuation.

## Where to continue

The season produced reproducible trajectories and candidate questions, not a confirmed emergent checking habit. Strongest next: a small observation-versus-answer-mapping/feedback-comprehension contact that can distinguish a missing readout skill from failure to use verifier messages, followed by a predeclared continuation using the saved notebooks. If adding a tool-request action or changing checkpoint/style, create an explicitly labeled branch; preserve these notebooks and do not pretend that a new action interface grew spontaneously.

Next batches can continue the history; don't restart silently, prune inconvenient failures, or run until a favorable endpoint. Both non-events and departures remain part of the garden. Model binaries remain local and existing backup/restore limitations apply; the published notebook/code/history is not a full binary backup.
