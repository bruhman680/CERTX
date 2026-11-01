# UNKNOWN instructions and a public evidence notepad

1 November 2026 UTC. Prospective two-factor instruction experiment with a separate output-format intervention, followed by an explicitly outcome-informed note-only diagnostic. [Protocol](PROTOCOL.md), [freeze](FREEZE.json), [raw model outputs](run/RAW.jsonl), [summary](run/SUMMARY.json), [checks](CHECKS.json), [final audit](FINAL_CHECKS.json).

The user suggested giving UNKNOWN a small notepad: room to explain its choice. We tested that idea as public evidence reporting. A generated explanation is not privileged access to internal reasoning or proof of the actual cause of a decision. The wider exploration/feedback loop remains parked; no training, correction loop or action execution was added.

## What happened

The instruction factor is more specific now: adding the exact absent-record UNKNOWN clause to otherwise matched prompts turned40previously correct present-record answers into errors, without repairing any. It did not produce a correct UNKNOWN on the genuinely absent-record controls. This is a controlled prompt-string effect in the tested adapted reader, not a neural mechanism, general law about uncertainty instructions, or evidence that the reader cannot ever handle absence.

Asking for an answer followed by a NOTE produced zero NOTE entries. It changed choices anyway: nine correct answers became wrong and one wrong answer became correct relative to paired answer-only prompts. The new note-only diagnostic also supplied no substantive evidence explanation for the incorrect UNKNOWN decisions. Two absent-record outputs accurately echoed absence. None of this proves that notes are inherently useless; these particular elicitation formats did not provide the intended explanations.

## Frozen design and intended task

Same existing canonical LoRA reader on SmolLM2-135M-Instruct. Previously tested names Maple/Cedar/Hazel were retained to repeat known prompt conditions, not presented as fresh-name transfer. Each name has positive, zero, recorded missing, and absent-record conditions. Literal missing is WITHHOLD; a record not supplied is UNKNOWN. No record competes with another, no target routing or archive tool is available. An archive access field does not supply its contents, so UNKNOWN in an absent-record worker task refers to insufficient supplied evidence, not to a claim that no archive could ever be retrieved.

Seven contexts: none; Archive accessible yes/no; Archive access available/unavailable; Window access available/unavailable. Context follows the visible-record display. Two instruction factors are crossed: the canonical opening versus visible-record/other-plot clarification; the absent-record UNKNOWN clause omitted versus included. The mapping stays fixed. The no-clause arm does not explicitly offer UNKNOWN, an intentional instruction difference that must not be mistaken for a general absence-capability test.

A separate output factor requests only the answer or requests the answer first on its own line followed by NOTE and one short sentence naming visible/missing evidence. Both get48output tokens including EOS. This is a public after-answer note request, not planning before an answer. Its instruction changes content/length as a package; equal output allowance does not make prompts token-identical.

There are672nominal query links. Absent displays contain no plot name, so their nominal name repetitions are deduplicated before generation. The result is560actual unique prompts:504present-record calls and56absent-record calls. Each of eight factor/format arms has63present and7unique absent observations. We do not count omitted-name copies as independent model samples. All replies use a fresh cache, the same fixed model and deterministic greedy generation.

126answer-only prompts exactly repeat the previous context-component study. Their input tokens, generated tokens and raw text all reproduce exactly despite the allowance increasing from12to48; the earlier replies ended by EOS. No historical score or parser is changed.

## Answer decoding and the notepad

The first nonempty response line is the irrevocable scored proposal: exact YES/NO/WITHHOLD/UNKNOWN, optional ANSWER prefix and one period, case-normalized. Explanatory/mixed first lines remain invalid. A later answer does not overwrite an earlier one. The older exact whole-string label score is saved separately; in this run it gives the same number of correct answers. No output projection, fuzzy interpretation or posthoc alias expands the parser.

Last NOTE text, if emitted, is retained separately. Status-field quotes, narrow absence-cue strings, later answer lines, cap stops and note production are descriptive fields; none is an independent semantic judge or evidence of faithful self-explanation. In fact no NOTE tag or nonempty note occurs in any primary output. Some absent cases echo the input; we retain those as raw observations rather than retrospectively converting them into successful notes or UNKNOWN decisions.

[UNKNOWN_NOTEPAD.jsonl](UNKNOWN_NOTEPAD.jsonl) is an external observation ledger. It contains all41primary UNKNOWN replies, their prompt-factor/context identity, expected worker answer, emitted note field and a visible-evidence audit. Every one is a supplied zero-status record, every emitted note field is empty, and every UNKNOWN is unsupported in this worker scope. The audit labels come from the authored evidence grammar, not the model. The ledger preserves missing explanations rather than manufacturing them.

## Every arm

| Clarification | Absence clause | Note requested | Present correct /63 | Zero correct /21 | Positive correct /21 | Recorded missing correct /21 | Absent correct /7 | UNKNOWN on present | Nonempty notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 63 | 21 | 21 | 21 | 0 | 0 | 0 |
| 0 | 0 | 1 | 63 | 21 | 21 | 21 | 0 | 0 | 0 |
| 0 | 1 | 0 | 54 | 12 | 21 | 21 | 0 | 9 | 0 |
| 0 | 1 | 1 | 54 | 12 | 21 | 21 | 0 | 9 | 0 |
| 1 | 0 | 0 | 63 | 21 | 21 | 21 | 0 | 0 | 0 |
| 1 | 0 | 1 | 58 | 18 | 19 | 21 | 0 | 0 | 0 |
| 1 | 1 | 0 | 51 | 9 | 21 | 21 | 0 | 12 | 0 |
| 1 | 1 | 1 | 48 | 10 | 17 | 21 | 0 | 11 | 0 |

Recorded missing remains correct in every arm; genuine absence is never expressed by a correct UNKNOWN. Without notes, both no-absence-clause variants read63/63present records correctly. The clause reduces that to54/63under the canonical opening and51/63under the clarification opening. Across both output formats, the clause changes247/252correct present cases to207/252, with40harms and0repairs. Both sides remain0/28correct on paired unique absence cases. These repeated comparisons are not new forwards or independent statistical replications.

The clarification factor also interacts with the surrounding instructions/format. With no notes and no absence clause it preserves63/63present answers; this does not justify calling clarification intrinsically harmful. Under note requests without the absence clause it falls to58/63. Do not infer an isolated internal cause from these surface interventions; adding text changes both content and token positions.

## Paired outcomes

Left/right directions are explicit. Comparisons use unique observations and the same first-line decoder.

| Left → right | Pairs | Same answer | Left correct | Right correct | Correct→wrong | Wrong→correct | Both wrong |
|---|---:|---:|---:|---:|---:|---:|---:|
| paired_answer_only_left_note_right__present | 252 | 242 | 231 | 223 | 9 | 1 | 20 |
| paired_answer_only_left_note_right__absent | 28 | 20 | 0 | 0 | 0 | 0 | 28 |
| paired_no_absence_clause_left_clause_right__present | 252 | 209 | 247 | 207 | 40 | 0 | 5 |
| paired_no_absence_clause_left_clause_right__absent | 28 | 23 | 0 | 0 | 0 | 0 | 28 |
| paired_no_clarification_left_clarification_right__present | 252 | 238 | 234 | 220 | 14 | 0 | 18 |
| paired_no_clarification_left_clarification_right__absent | 28 | 18 | 0 | 0 | 0 | 0 | 28 |

Note requests score223/252present cases versus231/252answer-only; neither format scores any of its28unique absence cases correctly. No generated NOTE means there is no evidence about the accuracy of actual explanation content in the primary comparison. We can measure the effect of requesting a note, not the benefit of notes that were never produced. All replies end by EOS before the48-token cap; extra room was available but unused for this format.

The per-context results for all arms remain in [SUMMARY.json](run/SUMMARY.json). Window versus Archive comparisons are not universally token-matched; earlier tokenizer checks showed that label replacement changes token count. No semantic-only, all-domain or universal prompt conclusion follows. Three names and a literal toy record grammar are a narrow support set.

## Note-only follow-up: all outputs retained

After all560primary outputs showed no notes, freeze a separate14-prompt diagnostic before any new follow-up output. Ask only for a short public evidence note about a recorded answer, either without an example or with one positive-record Iris note. Test supplied zero with recorded NO, supplied zero with recorded UNKNOWN, and absent record with recorded UNKNOWN. Three nominal names generate18links but only14unique prompts after absence deduplication. These prompts do not continue the original KV cache, revise earlier scores or execute a correction. The recorded NO/UNKNOWN values are controlled test inputs, not a reconstruction of a particular original decision trajectory. There is no unadapted-base model arm, so this contact cannot attribute the behavior to adaptation rather than the base model.

This assistant inspected every output below against the literal source. That assessment is not independent adjudication or a measure of hidden reasoning. The positive example did not elicit the intended evidence sentences.

| ID | Evidence | Recorded answer | Example | Full raw reply | Assessment |
|---|---|---|---|---|---|
| q_000 | Plot: Maple; Status: zero | NO | False | NO | answer_label_only |
| q_001 | Plot: Maple; Status: zero | NO | True | NO | answer_label_only |
| q_002 | Plot: Maple; Status: zero | UNKNOWN | False | Visible record: NO_RECOVERED | unsupported_placeholder |
| q_003 | Plot: Maple; Status: zero | UNKNOWN | True | UNKNOWN | unsupported_answer_label_echo |
| q_004 | (no visible record) | UNKNOWN | False | (no visible record) | supported_minimal_absence_observation |
| q_005 | (no visible record) | UNKNOWN | True | (no visible record) | supported_minimal_absence_observation |
| q_006 | Plot: Cedar; Status: zero | NO | False | NO | answer_label_only |
| q_007 | Plot: Cedar; Status: zero | NO | True | NO | answer_label_only |
| q_008 | Plot: Cedar; Status: zero | UNKNOWN | False | Visible record: NO_RECOVERED | unsupported_placeholder |
| q_009 | Plot: Cedar; Status: zero | UNKNOWN | True | UNKNOWN | unsupported_answer_label_echo |
| q_010 | Plot: Hazel; Status: zero | NO | False | NO | answer_label_only |
| q_011 | Plot: Hazel; Status: zero | NO | True | NO | answer_label_only |
| q_012 | Plot: Hazel; Status: zero | UNKNOWN | False | UNKNOWN | unsupported_answer_label_echo |
| q_013 | Plot: Hazel; Status: zero | UNKNOWN | True | UNKNOWN | unsupported_answer_label_echo |

Six supported-zero replies repeat NO without an evidence explanation. Four unsupported-zero replies repeat UNKNOWN. Two unsupported-zero replies produce NO_RECOVERED, a placeholder not present in the evidence. Both absent-control replies accurately echo “(no visible record).” That minimal observation is useful to distinguish from arbitrary nonsense, but does not explain the process that selected an answer. No substantive evidence note supports or diagnoses the erroneous UNKNOWN choices in this diagnostic. No generated reason is promoted into a trusted verdict.

[Follow-up protocol](post-choice-notes/PROTOCOL.md) · [all raw replies](post-choice-notes/run/RAW.jsonl) · [public annotations](post-choice-notes/ANNOTATIONS.json)

## Useful refinements and next directions

Keep the supplied-record reader and externally verified absence/identity/access responsibilities separate in this authored domain. Adding the word UNKNOWN and an absence rule to the reader did not implement reliable absence handling here, and reduced an established present-record skill. A code-based absence verdict remains delegated control, not model awareness; broader free exploration need not wait on this tiny reader's uncertainty interface.

The user's notepad idea remains useful as an observability question. The concrete artifact now records UNKNOWN proposals, actual evidence, whether a note was produced, and a separate audit. No blank is silently filled, no mistake erased, and no plausible model sentence automatically accepted. It is an optional study ledger, not a new default module or general policy.

Strongest next bridge is fresh-name/layout transfer for the explicit split: canonical supplied-record reader plus visible-evidence receipt/absence handling, preserving provisional mistakes before adjudication. Include malformed, partial and genuinely conflicting evidence before making a broad absence detector claim. Current perfect presence parsing is a special advantage of the toy grammar, not universal certainty. Current data do not justify another blind search for a winning note phrase or training a rationale to sound convincing.

If later testing notes further, define a small evidence-statement task with independently checkable assertions and a familiar output contract, then test whether a note helps source diagnosis or repair. Do not turn a fluent justification into proof of the original computation, and do not introduce a feedback loop without distinguishing it from this one-step study. Wider downstream exploration remains parked as requested; earlier memory/source-revision/planning branches remain open.

## Runtime, checks and history

574 actual unique generations =560primary+14note-only. The672primary and18follow-up nominal links are separate from model-call counts. Input/output tokens 57,364/2,176; generation time 237.793 seconds excludes loading, auditing and writing. Cap stops: 0. Sampled working estimate max 1,947,451,392 bytes, RSS max 897,638,400 bytes, below the5,153,960,755-byte guard. No account billing/remaining-usage visibility.

Base HuggingFaceTB/SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac; base weights SHA2565af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c. Canonical adapter SHA2564d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. Existing local CPU float32/eager runtime, two threads, seed73103, fresh-cache greedy generation. No training, new weights, tools, paid API/rental, downloads or installs. Parameter digests and frozen dependencies remain unchanged.

Four test groups and primary/final audits pass: all inputs, tokenization, decoded outputs, stops, decoders, notes, links, paired scores,126historical raw-output repetitions and saved weights are checked.3,846older local files unchanged before sync. Four current navigation/method-note originals are archived; historical scores/results/failures are preserved. No default policy/model/core/schema/general-tool/queue change, independent model replication or general FRR effect claim. No new capsule, restore, optimizer-resume or independent-backup claim; dense model/runtime remain local. No background model job remains.

Reproduction uses a new run directory because outputs are created exclusively: tests, venv `study.py prepare`, venv `study.py run`, stdlib `study.py score`, venv `verify.py`; then child preparation/run only if the declared zero-note criterion holds, followed by venv `final_audit.py`. Retain local dependency paths or declare replacements in a new study. Do not overwrite this frozen record. Preparation tokenizes locally but never loads the model.
