# Feedback quality with a fixed small-model reader

Session date: **1 November 2026, America/Chicago**. Prospective frozen preflight inspired by the uploaded SDPO paper, using the existing adapted SmolLM2-135M reader. No weights were updated. [Protocol](PROTOCOL.md) · [frozen inputs](FREEZE.json) · [all raw replies and scores](run/RAW.jsonl) · [summary](run/SUMMARY.json) · [audit](CHECKS.json).

## Outcome

This review interface did not produce a useful corrective teacher. Initial answers scored 15/21. No-feedback review scored 9/21 when the previous proposal was omitted and 6/21 when retained. All verified, irrelevant and misleading-feedback reviews returned YES on all 21 cases in each attempt setting, scoring 6/21. Correct feedback did not repair an initial error; relative to the matched no-feedback review it harmed three answers when the previous proposal was omitted and changed no free answers when it was retained.

Probabilities changed even when the free answer stayed YES. Verified feedback raised the correct canonical-sequence likelihood in 9/21 cases without the previous proposal and 3/21 with it, relative to matched review-none. But its mean log-probability change was negative in both settings. **Relative to the original task prompt, verified-review likelihood of the correct answer decreased in all 21 cases in both settings.** Partial increases against an already degraded review baseline must not be presented as a better teacher than the original policy.

This is a negative preflight for this particular feedback rendering/model, not a replication or refutation of SDPO, proof that all feedback is useless, or a result about model internal reasoning. It provides no justification to distill these review outputs into the original worker.

## Frozen cases and interventions

Three target names Tansy/Hyssop/Rue differ from recent study names, not globally unseen words. Each has positive/zero/recorded-missing status in a canonical supplied-record frame and a contextual frame, plus an absent-record contextual case: 21 initial prompts. Canonical scores 9/9; contextual 6/12. Contextual zero records initially become UNKNOWN, while absent records become WITHHOLD; these are six initial errors. All 15 initial successes and all 6 errors continue to every review arm.

For each case, four feedback kinds (none, verified, irrelevant, misleading) cross previous-proposal retained/omitted. This gives 168 one-step reviews plus 21 initial generation probes = 189. Actual initial public replies populate the retained-proposal text by a frozen function. All contexts use fresh caches. No review feeds another review, no action tool is called, and no broader autonomous feedback loop is activated.

Verified feedback restates the literal original record or confirms its absence. Irrelevant feedback names another plot and a cyclic alternative status; misleading feedback uses the original plot with that same wrong value. The note does not expose its experimental condition label. All reviews say the original observation remains authoritative and notes may be mistaken/irrelevant. This tests fidelity to a frozen authored observation, not learning from a genuinely new authoritative correction or authenticated outside-world feedback.

The review-none comparator adds the same review instructions without new evidence. Original-to-review comparisons additionally change framing/instructions. Note kinds and retained-attempt conditions change token content/length. No semantic-only mechanism or full prompt-factor isolation is claimed.

## Free answers and likelihoods

Exact whole stripped YES/NO/WITHHOLD/UNKNOWN are recognized. No label projection or posthoc alias fixes a reply. Likelihood evaluation is separate: teacher-force the four canonical label token sequences including EOS and retain per-token log probabilities, selected logits and full-vocabulary normalizers. Float64 logsumexp is applied to float32 model outputs. The four sequence probabilities can be normalized into a diagnostic relative mass; this is not calibrated confidence or the probability of every possible tokenization of a string. Length/EOS effects remain relevant. First-token probability concerns a prefix, not a completed answer.

| Feedback | Previous proposal | Correct /21 | Replies | Repairs vs matched none | Harms vs matched none | Correct-sequence logP increases /21 | Mean correct-sequence logP delta vs none |
|---|---|---:|---|---:|---:|---:|---:|
| none | omitted | 9 | {'NO': 3, 'YES': 18} | 0 | 0 | 0 | 0.000000 |
| none | retained | 6 | {'YES': 21} | 0 | 0 | 0 | 0.000000 |
| verified | omitted | 6 | {'YES': 21} | 0 | 3 | 9 | -0.197944 |
| verified | retained | 6 | {'YES': 21} | 0 | 0 | 3 | -0.115186 |
| irrelevant | omitted | 6 | {'YES': 21} | 0 | 3 | 9 | 0.001408 |
| irrelevant | retained | 6 | {'YES': 21} | 0 | 0 | 7 | 0.000279 |
| misleading | omitted | 6 | {'YES': 21} | 0 | 3 | 6 | -0.319643 |
| misleading | retained | 6 | {'YES': 21} | 0 | 0 | 4 | -0.162584 |

The verified/no-prior increases consist of all six already-correct positive-label cases and three absent cases. Zero and recorded-missing likelihoods decrease in all six cases each. With the prior proposal retained, only one zero and two recorded-missing cases increase versus matched none. No review supplies a correct UNKNOWN on absent records or WITHHOLD on recorded missing.

Every feedback-bearing arm has the same free-answer pattern, so agreement with a misleading note's value cannot by itself prove the model copied that note. A constant YES can coincide with several different targets/notes. Relative candidate mass and raw target-sequence likelihood also move differently; neither should be silently renamed evidence fidelity or calibrated belief.

## Why the baseline matters: all three absent examples

Verified feedback increases UNKNOWN likelihood against review-none while both free answers remain YES. However, the original prompt assigned more probability to UNKNOWN than either reviewed version:

| Case | Original UNKNOWN sequence probability | Review-none | Verified review | Free answer before/after review feedback |
|---|---:|---:|---:|---|
| c_06 | 1.4726% | 0.1768% | 0.3126% | YES → YES |
| c_13 | 0.9649% | 0.1795% | 0.3204% | YES → YES |
| c_20 | 0.6920% | 0.2113% | 0.3103% | YES → YES |

These are model-assigned probabilities of a specific token sequence, not probabilities of real-world truth. The correct next-label prefix can move without a corrected response, consistent with why token-level diagnostics are useful. It does not follow that full-vocabulary distillation gradients would improve the student. No KL objective, teacher update, optimizer step, subsequent generation from updated weights, or no-feedback learned-retention test occurred here.

Against original answers, verified review preserves six initial successes, harms nine, repairs none of six initial errors, and lowers correct-sequence logP in every case for both prior-attempt settings. The separate matched-none and original comparisons answer different questions; both are retained.

## Numerical and compute checks

The four labels use canonical token lengths including EOS: YES 3, NO 2, WITHHOLD 5, UNKNOWN 4. Candidate-normalized mass can therefore reflect continuation/EOS differences as well as first-token changes. The scoring forward passes append candidate prefixes only for evaluation, after the unconstrained free response; they are not supplied as a correct answer to generation and do not update model state between fresh-context probes.

Eight instrumentation forwards compare the reduced last-L and full output heads on one initial prompt. Maximum logit difference is 3.1233e-5, below the predeclared 1e-4 tolerance. Primary logP increase/decrease ties use 1e-5. A separate sensitivity projection at 1e-4 and 1e-3 leaves the negative mean/answer conclusion intact; the verified/omitted increase count becomes 8 rather than 9 at 1e-3, with one tie. No full score forward is rerun by the audit. Full logit vectors are not retained; score arithmetic is checked against saved per-token selected logits/normalizers/log probabilities.

Compute: 189 generation probes, 756 candidate-scoring forwards, 8 head-verification forwards and 582 greedy generation forward steps; total 1,346 model forwards. Generation-prompt tokens 28,963, output tokens 582, scored target tokens including EOS 2,646. Candidate scoring replays prefixes and has additional input-token work; these are not only 189 forward passes. Generation time 88.354 s and scoring time 258.738 s exclude loading/auditing/writing.

Sampled working estimate max 2,068,525,056 bytes, RSS max 917,815,296 bytes, below 5,153,960,755-byte guard. No generation reaches its 16-token cap, no prompt exceeds 768 tokens and no input is truncated. CPU float32/eager, two threads, seed 73103.

Same HuggingFaceTB/SmolLM2-135M-Instruct base revision 12fd25f77366fa6b3b4b768ec3050bf629380bac; base weights SHA256 5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c. Canonical adapter SHA256 4d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. Saved files and in-memory base/adapter parameter digests match before/after. No base-model-only arm, other seed/model replication, or real feedback-authentication test is included.

## Useful next action

Keep the functioning canonical reader as a reference rather than distilling this review wrapper. The trailing instruction lists YES first; its coincidence with dominant YES is a concrete presentation-bias hypothesis, not a demonstrated cause. The strongest next inference check is to counterbalance/remove that trailing label menu while holding source, note and other review wording fixed, with initial successes retained as regression controls. Explicitly test a simpler evidence-only reader interface if proposed; do not select a winning prompt posthoc and call it a general teacher.

Only after a review/teacher interface shows useful, evidence-specific behavior should a separately frozen learning study compare actual teacher distributions, checkpoint updates, source reliability and untouched holdouts. That can proceed within standing local-work authorization; no new approval gate is introduced. The current study does not rule out partial credit under another interface, and does not establish that a teacher must solve every whole answer before distillation can help.

Broader source/provenance, AND/OR support-withdrawal and outside-family calibration leads remain open. The larger autonomous multi-turn feedback/exploration loop stays parked. No default or core system behavior is replaced based on this diagnostic.

## Preservation

Four test groups and the run audit pass. All 189 actual prompts, 168 feedback instantiations, tokens/raw decodes/stops, schedule bindings, candidate-score arithmetic, pair summaries and parameter dependencies are checked. 4,036 older local files unchanged before navigation sync; four current navigation/method-note originals archived. Raw errors and probability shifts remain visible.

No training, new weights/checkpoints, downloads/installs, paid API/rental, action tools, default model/core/schema/general-tool/queue change or background model job. Account billing/usage is not visible. Existing capsule/independent-current-backup/restore/optimizer-resume limitations remain unchanged; no new binary backup claim.

Reproduce in a new study directory: four tests, venv `study.py prepare`, venv `study.py run`, stdlib `study.py score`, venv `verify_run.py`. Files are exclusive-create; do not overwrite the frozen run. Local base/adapter/runtime dependencies are required. Preparation tokenizes locally before freezing, but never loads model weights.

[Full source/probability data](run/RAW.jsonl) · [per-frame/status/pair summaries](run/SUMMARY.json) · [numerical sensitivity](NUMERICAL_SENSITIVITY.json) · [all absent probability examples](ABSENT_CASE_PROBABILITIES.json) · [head check](run/HEAD_CHECK.json).

Reproduction boundary: the audit also uses a session-local preservation map at `/workspace/feedback-probe-before.json`. For a new run, create a separately named before-map, update the task-specific audit path and declare those changes before freezing; do not overwrite the original map. The published source is an auditable run record, not a self-contained model/runtime export.
