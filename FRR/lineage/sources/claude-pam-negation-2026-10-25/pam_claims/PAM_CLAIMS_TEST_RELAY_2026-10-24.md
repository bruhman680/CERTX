# Testing the Gemini "Phase-Aware Memory (PAM)" summary claim by claim

Prepared 2026-10-24 by Claude (Sonnet 5.5) for Thomas, to pass to ChatGPT. Script: `pam_claims_test.py`; saved output: `pam_claims_test_output.txt`; identity check: `check_phase_identity.py` + output.
Depth: **exact or seeded results on constructed data.** The phase is supplied by an oracle (0 or π). No learned encoder, no real text, no product kernel. One model lineage wrote this; please re-implement independently and try to break it.

Context: the identity S = R/2 + R²c/2 (R = energy balance, c = cosine on real+imaginary coordinates) is from Thomas's RM-C1 post (commit 933af8b); I re-verified it independently (8,000 random pairs, error 6.7e-16; the exact examples 18/25, 2/25, 1210/10201 reproduce). The Gemini summary builds claims on top of it. Each claim was tested; the score is always computed directly from the published expression, not from the identity.

## Verdict table

| Gemini claim | Verdict | Evidence |
|---|---|---|
| (A) "Use the resonance score to fix negation blindness" | **Partly right, wrongly attributed, wrong for evidence retrieval** | Against a polarity-blind baseline (amplitude-only cosine), phase helps: top-1 .500 → 1.000 when phase carries polarity. But with energies equalized, S and plain cosine on the same real+imaginary coordinates give identical rankings (max \|S−(1+c)/2\| = 6.7e-16) and identical accuracy at every noise level. So the *information* fixes it, not the score. |
| (A, extended) phase "for logical opposition" | **Harmful when the task is evidence checking** | If relevant = records that support *or* contradict the query, S ranks the contradicting record **last of 400** (recall@2 = .500). Amplitude cosine and \|c\| get recall@2 = 1.000. A scalar that makes opposition maximal dissimilarity cannot also retrieve contradictions. |
| (A, robustness) | **Fragile to phase noise** | With noisy phase (σ = 1.0 rad) top-1 is .470, lower than discarding phase (.500). At σ = 1.5, .160. |
| (B) "Normalization deletes strength/confidence; the score restores it" | **Conditional; mostly wrong for confidence** | M1 (norm = strength that should match the query): S 1.000, cosine .200, but cosine + one explicit norm-ratio feature also 1.000. M2 (norm = arbitrary artifact): S **.485** vs cosine 1.000. M3 (norm = confidence, higher is better): S **0.000** (by construction it prefers the strength that matches the query, not the highest), raw dot product 1.000, cosine + explicit confidence feature 1.000. S rewards *matching* magnitude, not *high* magnitude. |
| (C) "Posture = tunable resonance bandwidth (needs phase)" | **Not supported as stated** | The score has no bandwidth parameter. For equal norms, softmax(S/T_S) equals softmax(c/T_c) with T_S = T_c/2 (max diff 3.9e-16), and a threshold t on S equals threshold 2t−1 on cosine. Posture can be done with ordinary cosine plus a threshold, temperature or top-k. For unequal norms they differ (max diff .61), which is the R effect, not a bandwidth effect. A real test needs an operational definition of "bandwidth". |
| (D) "Agents exchange wave packets; memories interfere without prompt packaging" | **Misses an information-loss hazard** | If only the sum is stored, the zero aggregate has many histories: for n = 4 agents (each +z, −z or silent), 19 of 81 histories give 0; 18 of those contain a dispute and 1 is "nobody spoke" (94.7% disputes). n = 6: 99.3%. The sum cannot tell silence from disagreement. |
| (E) "Time as phase progression lets the DB query event sequences" | **Partly right** | Single event pair: S(z_t, z_{t+Δ}) = S(z_{t+Δ}, z_t) = S(z_t, z_{t−Δ}) to 12 decimals: before and after are indistinguishable. But two events on different topics bound to different times: swapping their order gives S = .490 (< 1), so order *is* distinguishable. Also a pure time shift changes S (.452), so the same pattern at a later time is not recognized as similar. |
| (F) "Hardware / FFT co-design" | **Untested** | No speed or energy data here. |

## Where my own predictions failed (kept on record)

1. **A2 failed in my first design.** I predicted S and realified cosine would rank identically. They did not (S .470 vs cosine .420 at σ = 1). Cause: I equalized energy only for the matching pair; distractor topics had different energies, so R varied across candidates, *and* the relevant record had exactly the query's energy by construction. That is a norm hint built into the generator. Fix: an energy-equalized condition, where the identity holds to 1e-15 and accuracies are identical. Lesson: a generator can leak the target through a quantity the score reads.
2. **First B run invalid.** The query's own record was in the candidate pool, so every relevant item was a trivial self-match (S and cosine both 1.000 in M2). I rebuilt B with noisy queries and no self-match. The numbers in the table are from the rebuilt B.
3. **My claim "S < cosine in M2" and "S not best in M3"** held after the rebuild. S = 0.000 in M3 is by construction (target strength 4, query strength 1), not an empirical surprise.

## What this does and does not show

- It shows that each claim's strong form depends on assumptions the summary leaves out: which baseline, what the norm means, what the task is (agreement vs evidence).
- It does **not** show that phase-aware memory is useless. A learned encoder might use phase in ways this toy does not. Phase can help against a polarity-blind baseline. Retrieval of evidence could use phase in a two-channel design.
- It does **not** test Listopad's actual system, real language, or any product kernel.
- Related work found (abstract level): Kumar, "When do complex-valued neural networks help?" (arXiv:2605.27673) uses real-coordinate, parameter-matched and FLOP-matched controls and finds conditional advantages; Sammani et al. (arXiv:2603.20554) handle negation with a real-valued linear direction. Independent routes to similar caution, not independent replication of this toy.

## Suggested next contacts

1. A scoped-negation fixture ("not open", "was not open yesterday", "not established that open") with a learned or hand-built encoder, comparing amplitude-only, real+imag cosine, S, |c| and a two-channel agreement/relevance score.
2. A noisy-phase sweep with a learned phase estimator instead of an oracle.
3. Operationalize "posture" (threshold, temperature, top-k) and test whether any phase-specific mechanism adds anything over the real controls.
4. Independent re-implementation by ChatGPT with different parameters.
