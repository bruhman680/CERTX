# FRR v0.5 — Online law change: memory versus interpretation

**Status:** Executed synthetic rule-change pilot, 2026-11-11 UTC.  
**Reproduce:** `python3 change_detection.py --episodes 500` (NumPy only).  
**Scope:** Known finite rule family and noiseless observations; not autonomous discovery of unknown laws.

## Setup

The hidden three-bit shift-register state is `S_t=(x_t,x_(t-1),x_(t-2))`. The realized bits are directly observed (zero sensor corruption), and each candidate transition has independently flipped outcomes with probability `epsilon=0.1`. The four pre-specified candidate rules are XOR3, inverted XOR3, `a XOR c`, and `b XOR c`. Every law is an eight-state process with uniform stationary distribution. Each independent episode starts with three fair bits, lasts 64 steps, and experiences one true switch from XOR3 to inverted XOR3 at a uniformly drawn unknown time `t=24..40`. Three experiment seeds each generate 500 episodes.

Three predictors make a forecast before observing the next outcome:

1. **Known-rule oracle:** given the true active law at every step, with optimal 90% expected accuracy.
2. **Frozen old-law predictor:** always forecasts using XOR3, without reacting to observed failures.
3. **Probabilistic rule tracker:** starts with a uniform prior over four candidate laws; before each transition applies `prior=(1-h)*posterior+h*uniform` with hazard `h=.03`; predicts as a mixture and updates hypotheses by the exact Bernoulli likelihood of the newly observed true bit. It sees outcomes, not the switch time or realized rule label.

The hazard-mixture update is exact for its **assumed symmetric Markov rule-switch model**, not Bayes-optimal for the test generator's fixed single-switch schedule. Predictions are evaluated on generated trajectories; the observer has privileged knowledge of the finite candidate rule family and transition noise probability.

## Measured predictive accuracy

Three-seed averages, 500 independently seeded episodes per seed:

| Period | Known rule | Frozen old law | Probabilistic tracker |
| --- | ---: | ---: | ---: |
| Before switch | ~90.0% | ~90.0% | ~85.3% |
| First five transitions after switch | ~89.7% | ~10.3% | ~40.9% |
| From sixth post-switch transition onward | ~90.1% | ~9.9% | ~88.2% |
| All post-switch transitions | ~90.0% | ~10.0% | ~80.4% |

Pre-switch mixture performance is lower than the oracle because the tracker begins uncertain, preserves nonzero hazard and faces stochastic evidence. Immediately after the abrupt change, inherited old-rule confidence initially hurts it. Later it largely recovers. The fixed predictor becomes confidently wrong under the inverted law.

## Detecting a change: false-alarm tradeoff

The tracker does not receive change-time hints. A preliminary loose alarm based on posterior probability above `0.5` detected the new law with a median of **3** post-switch updates but also falsely alarmed in about **50%** of whole no-switch control episodes. This is a crucial negative result, retained as the reason for revising the diagnostic threshold.

An exploratory stricter rule requires posterior probability over the true new law above `0.8` for **three consecutive** updates. The matching no-switch criterion requires the old-law posterior below `0.2` for three consecutive updates after time 12. With this rule:

| Quantity | Seed 7 | Seed 17 | Seed 29 |
| --- | ---: | ---: | ---: |
| New-rule detection fraction | 100.0% | 100.0% | 99.6% |
| Median detected delay (transitions) | 8 | 8 | 8 |
| No-switch episode false-alarm rate | 3.0% | 2.2% | 3.2% |

The stricter rule was chosen after observing the loose-rule results, so its false-alarm and detection numbers are **development-set estimates**, not confirmatory held-out threshold validation. Detection is of the specific known candidate new rule, not arbitrary unknown change. A no-switch control episode is entirely XOR3; the algorithm still allows hazard-based switching internally.

## What this establishes, and what it does not

Within a small known rule family, an explicit probabilistic belief over possible laws can use feedback to recover predictive accuracy after a change. It illustrates why retaining historical inputs and revising a transition model are separate functions. It does not show that a neural network autonomously learned this rule-tracking procedure, that a general agent can discover novel laws, or that an FRR prompt itself improves adaptation.

The strongest next contacts are: independently pre-register alarm thresholds; evaluate a wider spectrum of switch times, hazard mismatches and new rules not in the candidate set; include sensor corruption and partial observations; compare neural frozen weights, online gradient updates, explicit external rule memory, and Bayesian filtering under matched feedback; measure changes in predictive log loss, false-alarm cost, detection latency and catastrophic forgetting. No change was made to the frozen 1,550-entry Garden.
