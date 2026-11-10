# FRR v0.5 — Transition noise shift in the eight-state parity world

**Status:** Executed synthetic distribution-shift control, 2026-11-10 UTC.  
**Code:** `transition_shift_probe.py` imports the unchanged eight-state parity generator and GRU architecture from `eight_state_nonlumpable_rnn.py`.

## Setup

The true state is the three-bit history, and next bit is the parity of those bits XOR independent noise `eta~Bernoulli(epsilon)`. Train a 16-unit GRU at epsilon=0.1 for 450 Adam steps on fresh 128×24 sequences, seeds 7/17/29. Evaluate without changing weights on independent 2,048×24 sequences with epsilon in {0, .05, .1, .25, .4, .5}. Mask first two steps. Only transition noise is changed; no sensor noise or new learning occurs at test time.

## Results

| Test noise | Exact full-history Bayes accuracy | Seed 7 | Seed 17 | Seed 29 |
| --- | ---: | ---: | ---: | ---: |
| 0.00 | 100% | 100% | 100% | 100% |
| 0.05 | 95% | 95.10% | 94.99% | 95.07% |
| 0.10 | 90% | 89.97% | 89.62% | 90.09% |
| 0.25 | 75% | 75.32% | 74.75% | 75.18% |
| 0.40 | 60% | 60.44% | 60.01% | 59.99% |
| 0.50 | 50% | 49.64% | 49.99% | 50.24% |

## Reading

For epsilon<=0.5 the optimal decision rule remains **predict parity**; only its irreducible noise changes. The GRU trained at 0.1 appears to learn that rule and generalizes to these noise magnitudes with accuracy near the corresponding Bayes ceiling. This is not evidence of online adaptation, calibrated probabilities, or robustness to a different transition *rule*; the sign of the predictive relation is unchanged.

At epsilon=.5 the next bit is independent of history and no method can exceed 50% in expectation. This is a useful negative control.

Next: flip or remap the parity rule itself, not just its noise; score log loss and calibration as well as accuracy; inspect failures on held-out sequences and evaluate uncertainty by sequence rather than treating correlated steps as independent.
