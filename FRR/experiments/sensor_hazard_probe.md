# FRR v0.5 — Joint hidden-state and rule-belief stress test

**Date:** 2026-11-11 UTC  
**Status:** Executed synthetic sensitivity experiment; exact filtering under a declared model, not a general adaptation result.  
**Code:** `sensor_hazard_probe.py`, plus machine-readable `sensor_hazard_results.json` (18 rows).

## Why this experiment

The earlier rule tracker observed the true bit sequence. Realistic perception may be corrupted. When observations are noisy, the observer cannot treat the last three observed bits as exact microstates. The correct filter must maintain joint uncertainty over eight latent states **and** the possible transition rules.

## Construction

- True world is the eight-state three-bit parity register, transition flip noise epsilon=0.1.
- At an unknown randomized step 24–40 of each 64-bit episode, the true law changes from XOR3 to its inverted version, carrying the state through the switch.
- Each true bit is independently flipped before reaching the observer with probability `sensor ∈ {0, 0.1}`. Truth is held aside for scoring and never entered into the filter.
- The observer maintains a normalized 4×8 joint posterior: four known candidate rules (`XOR3`, inverted XOR3, `a XOR c`, `b XOR c`) crossed with eight possible states. Between transitions it mixes rule mass with symmetric hazard `h ∈ {0.003, 0.03, 0.15}` and propagates the 8-state Markov transition, then assimilates the next noisy observation.
- The competitor is a correctly observed, **old-law-only eight-state hidden-state filter**, not a naïve raw-bit parity calculation. Both predict the next *true* bit before seeing its corrupted observation.
- Three RNG seeds, 150 switch episodes and 150 matched no-switch control episodes each per condition.
- The development detection criterion from the previous experiment stays fixed here: new-rule posterior >0.8 for three consecutive updates. On no-switch controls we record **two separate diagnostics** after t=12: broad old-rule rejection (old-rule posterior <0.2, three times) and a matched confidence criterion (any one alternative rule posterior >0.8, three times). We did not retune thresholds for noisy sensors.

The update is exact Bayes for its **assumed** symmetric Markov rule-hazard model and emission/transition probabilities, not for the experimental generator's exactly one rule switch at a time uniformly sampled in 24–40.

## Representative results (seed 7)

| Sensor error | Assumed hazard | Hybrid pre accuracy | First 5 post | Later post | Detection rate | Median detection delay | No-change broad rejection | Confirmed alternative alarm |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0% | 0.003 | 86.85% | 24.27% | 88.14% | 100% | 8 | 0.67% | 0.67% |
| 0% | 0.03 | 86.26% | 42.27% | 88.21% | 100% | 8 | 4.00% | 0.67% |
| 0% | 0.15 | 83.14% | 54.40% | 85.49% | 98% | 11 | 7.33% | 1.33% |
| 10% | 0.003 | 73.92% | 58.67% | 70.78% | 48.67% | 20 | 18.67% | 8.67% |
| 10% | 0.03 | 74.07% | 60.27% | 73.84% | 58% | 17 | 26.00% | 6.67% |
| 10% | 0.15 | 73.11% | 62.53% | 72.45% | 29.33% | 17.5 | 56.00% | 0.67% |

Across seeds 17 and 29, the corresponding qualitative pattern survives. With a 10% noisy sensor and hazard 0.03, switch detection was 54–58%, median detected delay 17–22 updates, **broad** no-change old-rule rejections 26–30%, but confirmed-alternative false alarms only 3.33–6.67%. The corresponding late-post hybrid accuracy was 72.29–73.84%, versus 58–59% from the old-rule-only hidden-state filter. With clean sensors and hazard 0.03, detection was 100% in all three seeds, median delay eight updates. The broad and alternative-confirmation diagnostics answer different questions: *is the old rule in doubt?* versus *is one replacement supported strongly?* They must not be conflated into a single alarm rate.

## What survives and what fails

The joint filter can recover useful predictive performance in a noisy partially observed world, but **a detection threshold acceptable in the clean-observation development setting deteriorates sharply when the sensor becomes unreliable**. Greater assumed hazard raises early responsiveness at the cost of old-rule confidence; it yields many broad rejections without necessarily producing confidence in one alternative. Very low hazard slows adaptation to change, particularly when sensor noise makes evidence weak.

This is not evidence that the model cannot adapt: the rule family and sensor model were known, and the horizon is finite. Detection rates are **whole-episode**, and delay medians condition on detection. A lower detection fraction can make the detected-delay median look deceptively favorable. Results use only 150 episodes per seed and a fixed threshold inherited from earlier development; report uncertainty with episode-resampled intervals before claims of reliable deployment.

Crucially, the filtered belief and the true microstate were kept separate. The original noiseless-rule tracker would be miscalibrated if fed corrupted bit triples as though they were truth.

## Next useful contact

Preregister a sensor-aware alarm rule on a separate development set and test on held-out episodes, including gradual rule drift, change rules outside the four-hypothesis set, and sensor miscalibration. Compare count-based CUSUM, full Bayesian run-length tracking, and selective abstention under an explicit false-alarm cost. Preserve the original clean-sensor false-alarm result as historical evidence rather than retroactively replacing it.
