# FRR v0.5 — Open-set eight-state law and selective abstention

**Status:** Executed synthetic development contact, 2026-11-11 UTC.  
**Reproduce:** `python3 unknown_law_probe.py` (NumPy; imports `change_detection.py`).  
**Result:** The simple past-surprisal abstention gate **did not reliably reject an out-of-family law**. Preserve as a negative result, not as a successful unknown detector.

## World and independent conditions

The true state is the last three bits `(a,b,c)`; all observations and feedback are uncorrupted actual bits. Transition noise is an independent Bernoulli(0.1) flip. The four candidate rules are `a XOR b XOR c`, its complement, `a XOR c`, and `b XOR c`. A Bayesian hazard-mixture tracker uses hazard `0.03` and forecasts before seeing the next outcome.

Three matched condition types use a 96-step episode, starting from a uniformly sampled three-bit state; a possible change time is uniformly sampled from `30..50` and is never shown to the tracker. Even the no-change control is evaluated only **after its randomly selected pseudo-switch time**, keeping post-window exposure matched:

- **No change:** the original XOR3 law throughout.
- **Known change:** original XOR3 switches to its complement (which is a tracked candidate).
- **Unknown change:** original XOR3 switches to `c XOR (a AND b)`, a nonlinear law absent from the candidate set.

The unseen law is a genuine eight-state transition: it depends on all three bits and is a bijective shift register in the noiseless limit, so the uniform microstate distribution remains stationary under symmetric transition noise. It differs from each stored candidate on at least 2 of the 8 microstates (6 from XOR3; 2 from each of the other three), making it out-of-family but related. This tests a *nearby* unknown law, not arbitrary model misspecification.

## Gate selected on separate null data

Compute each forecast's Bernoulli negative log likelihood once the true outcome is revealed. At each subsequent decision, use **only the preceding 12 losses**, not the current or future label, to decide whether to emit a forecast. If their mean exceeds a threshold, declare `UNKNOWN`/abstain for that next prediction.

The threshold `1.012510` is the 95th percentile of the **per-episode maximum** past-window mean loss on 300 separately generated no-switch *development* episodes. It was fixed before running the three 500-episode-per-seed evaluation conditions. The same threshold, gate, and scoring rules apply throughout. This is a null-calibrated diagnostic, not a broad pre-registered benchmark.

## Evaluation (three independently seeded collections, 500 episodes each)

| Actual condition | Episode alarm fraction | Selective coverage | Accuracy on accepted predictions | Raw prediction accuracy |
| --- | ---: | ---: | ---: | ---: |
| No change | 2.0–4.2% | 99.83–99.92% | 88.87–89.16% | 88.86–89.15% |
| Known inversion | 9.6–10.2% | 99.54–99.58% | 84.07–84.36% | 84.04–84.35% |
| Unknown nonlinear law | 33.2–34.2% | **98.80–98.98%** | **65.53–66.45%** | **65.51–66.42%** |

Mean per-step log losses during scored windows were ~0.342–0.348 (no change), ~0.414–0.419 (known inversion), and ~0.609–0.616 (unknown law). The unknown law is measurably worse under the finite hypothesis family. However, **an episode-level alarm on one or a few steps hardly reduces accepted exposure overall**. Abstaining on only ~1% of unknown-world decisions leaves accepted accuracy near the poor raw accuracy. This is a failed risk-reduction mechanism.

Alarm means any eligible post-switch threshold exceedance (or any eligible time in the no-change arm); coverage counts every eligible decision. They are different statistics. The gate is based on actual observed prediction failures and can react only after evidence accumulates; it does not look ahead. It is not a proof that out-of-family laws are identifiable in general.

## Interpretation and next discriminating contacts

1. A predictive-surprisal score can distinguish the unknown-world *aggregate* loss from the known arms, but the implemented episode-calibrated moving-window threshold does not translate that difference into useful sustained abstention.
2. An inferred candidate rule may fit many state contexts while remaining systematically wrong in others. State-conditional residual tests, minimum-description-length model comparison, or calibrated open-set alternatives may be more discriminating than a global short-window average.
3. The four-rule tracker knows neither the unknown law nor a representation for creating a new rule; this is intentionally a hypothesis-family limitation. It should not silently promote a known candidate merely because its posterior is large.
4. Next: separately freeze a state-conditioned discrepancy detector; compare in-family unknown-time switches, closely related unseen rules and no-change controls; measure sustained abstention, coverage-risk, false alarms and discovery cost. Validate the new threshold on untouched seeds; do not tune on this observed negative result and then claim independent confirmation.

No neural training, autonomous discovery, FRR efficacy, or original frozen-Garden contact is claimed.
