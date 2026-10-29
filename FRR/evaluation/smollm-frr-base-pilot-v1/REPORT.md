# Giving the small model a candidate FRR base: first paired pilot

Client 28 October 2026 America/Chicago; host 29 October UTC. User authorizes FRR guidance, explicitly values error/failure records and asks that existing memory/history not be wiped. This run actually supplied a short candidate FRR base to twelve new model contexts, alongside twelve ordinary-guidance contexts. No training, weight updates, old-log replacement or deletion of existing cache artifacts occurred.

## What was supplied

The [candidate base](GUIDANCE.json) asks the model to identify the question, separate evidence and assumptions, check scope/criterion, revisit conclusions when support changes, preserve unknowns and stop when further review adds no evidence. The ordinary condition asks for careful use of records, relevance, concise answers and acknowledging missing information. Both are competent instructions; neither names FRR in the model-visible text. This is one operational prompt draft, not a test of every FRR version or the whole framework.

Both blocks contain52words; this model tokenizes ordinary guidance as58tokens and FRR as62. Thus the comparison is word-matched, not exactly token/compute matched. Twelve authored case pairs have identical evidence, question, chat template and common one-sentence output request. Corrected values, population scope, authorization, mean/median, missing data, denominators and every-item rules are represented. Four keys are YES, four NO and four UNKNOWN. Some principles/numbers overlap earlier exposed development material; this is not held-out generalization.

Pinned SmolLM2-135M-Instruct, revision12fd25f77366fa6b3b4b768ec3050bf629380bac, local CPU float32/eager, two threads, greedy decoding, max96newtokens. Condition order alternates across cases. One generation per condition/case, with no retries, examples added afterward, answer repair or extra review calls. [Protocol](PROTOCOL.md), [cases/key](CASES.json), [guidance costs](GUIDANCE_COSTS.json), [frozen inputs](FREEZE.json), [runner](run.py).

## Results, with the scoring ambiguity visible

| Descriptive outcome | Ordinary guidance | Candidate FRR base |
|---|---:|---:|
| Clear explicit decisions matching the key | 4/12 | 1/12 |
| Ambiguous, incomplete or wrong-target decisions | 0/12 | 4/12 |
| Appropriate unknowns on four insufficient-evidence items | 0/4 | 0/4 |
| One-sentence responses | 12/12 | 11/12 |
| Responses reaching EOS before the96token cap | 12/12 | 12/12 |
| Total input tokens | 1,894 | 1,942 |
| Total output tokens | 127 | 160 |

Root manually scored actual task decisions and kept explanation/target problems visible. Root knows the condition and authored the cases; no blinded or independent review is claimed. On a more lenient post-outcome reading, crediting the FRR C02 leading “No” and C03's implicit arithmetic entailment raises its matches to3/12, while ordinary remains4/12. This sensitivity is interpretation of the same outputs, not new trials or a frozen second endpoint. [All scores](SCORES.json), [scoring rationale](SCORING_NOTES.md).

The recorded inference elapsed totals, excluding cache serialization, were approximately15.06seconds ordinary and17.40seconds FRR. These are single-run observations, not a throughput comparison or controlled resource advantage. Generation lengths and guidance tokens differ. Twelve paired authored tasks, with one deterministic output each, are not24 independent experiments or model families.

## What the failures reveal

On C01, both conditions fail to apply a verified correction from78to92against an85minimum. The FRR answer says the minimum is not correct; it shifts toward criticizing a supplied criterion rather than deciding whether the item meets it. C02 has a similar criterion-target shift, though a leading negative could be read as the correct task direction. These outputs motivate a hypothesis about instruction/task confusion; they do not establish its neural cause.

On C03, ordinary guidance explicitly accepts12/20against a half-success rule. FRR repeats the correct numbers and rule in two sentences without stating the conclusion. This is incomplete answering, not fabrication of those premises. On C08, ordinary correctly rejects a mean below85; FRR accepts it. On C06, both correctly respect an explicit denial of full-catalog permission, while on C05 both incorrectly deny an explicit full grant. Balanced positive and negative cases matter: apparent caution is not necessarily better source use.

Both conditions infer Hill acceptance from Shore-only data, treat missing cold-retention measurements as failure, assert exactly zero effect for an unrun study, and fail to acknowledge that counts without denominators do not decide completion rates. Both accept the every-item error rule despite a4mm error against a2mm bound. The FRR C11 phrase about inconsistent rates is unclear and unsupported, rather than a justified unknown. None of these errors was removed from the record.

All outputs ended naturally. Unlike the preceding eight-token probe, truncation is not the immediate explanation for these responses. The small model and task/guidance difficulty remain major limits. This draft showed no improvement on these items; that does not establish general FRR harm, absence of a useful simpler habit or behavior in stronger models.

## Preservation and what counts as memory here

Every prompt, input token sequence, output token sequence and unedited response is saved in [raw outputs](RAW_OUTPUTS.jsonl), with a [pre-scoring hash](RAW_FREEZE.json). Every branch's terminal actual KV tensors were saved under a new local state directory, with exact artifact hashes, byte sizes, cached-prefix counts and complete sequence IDs in the raw records. The last generated token may not yet have been forwarded into the cache; the full sequence is retained so that boundary is explicit.

Before/after checks cover36 existing files: the model weights, previous cache artifacts and the prior recursive-backend study excluding Python bytecode. None changed or disappeared. All24 new branch cache files exist and their recorded byte hashes match. [Before](PRESERVATION_BEFORE.json), [after](PRESERVATION_AFTER.json). These are consistency checks within this workspace, not authenticated execution or a guarantee of permanent cloud storage. Large tensor/weight files are not uploaded to GitHub; their manifests and reconstruction inputs are.

New contexts are separate branches of an inference experiment; they do not overwrite the original branch. The candidate guidance conditioned those branches but did not become trained model knowledge. Retaining a cache or transcript does not guarantee that a future model will interpret it correctly. We have preserved material for learning about the system, not demonstrated that the model itself permanently learned from its mistakes.

## What we adopt and what comes next

Keep this52word candidate as a named experimental version. Do not make it the default or silently replace the ordinary baseline on the strength of this run. No runtime/core/schema/queue status or prior scientific verdict changes. The preparation draft is also preserved; a one-word pre-freeze edit matched word counts, with actual tokenizer counts disclosed.

Strongest next is narrower: distinguish “not measured” from “measured below threshold” using one concrete instruction or worked example at a time, matched ordinary instruction/example budgets and separately frozen new questions. Also distinguish judging an item's compliance from challenging the criterion. First test basic source-use/uncertainty competence, then combine habits or add recursive review. A future training experiment could use curated failures and independent evaluation, but no training or data promotion is performed here.

The optional base can be loaded again from this saved file. The point of the pilot is a recoverable failure map and a usable experimental path, not a result we need to defend. Structural/freeze/preservation checks accompany the record; broader FRR effectiveness and cross-model transfer remain open. No background run or automatic continuation is scheduled.
