# Eight-state transition-law transfer: parity is not adaptation

**Status:** Executed synthetic rule-change test, 2026-11-10 UTC.  
**Code:** `rule_shift_probe.py` (PyTorch). No canonical Garden changes or online adaptation.

## Purpose

The earlier `transition_shift_probe.py` changed only the flip probability of the *same* XOR3 rule. A predictor that learns the parity sign can remain optimal for all epsilon <= 0.5, so such generalization is not evidence of adapting to a different causal law. This test changes the deterministic relation itself while keeping transition noise at 10%.

## Construction

The stationary eight-state process has state `(a,b,c)=(x_t,x_(t-1),x_(t-2))`. Train one 16-hidden-unit GRU on the update `x_(t+1)=a XOR b XOR c XOR eta`, with `eta~Bernoulli(.1)`, for 450 Adam steps, three initial seeds (7,17,29), fresh 128×24 sequences per step. No further optimization occurs at evaluation. Held-out sets contain 2,048 independent 24-step sequences for each of four rule conditions; first two prediction positions are masked.

Four evaluated true rules (each still has eight microstates): original XOR3, complement/inverted XOR3, `a XOR c`, and `b XOR c`, each plus independent noise of .1. Including the oldest bit `c` in every rule preserves a bijective shift-register transition before noise, so uniform stationarity holds for all four arms. All have matching one-bit marginals, and the noise rate does not change.

## Findings

| Test rule | Seed 7 accuracy | Seed 17 | Seed 29 | Average |
| --- | ---: | ---: | ---: | ---: |
| Original XOR3 | 89.88% | 90.11% | 90.08% | 90.03% |
| Inverted XOR3 | 10.08% | 10.07% | 9.90% | 10.02% |
| a XOR c | 49.62% | 50.02% | 50.37% | 50.00% |
| b XOR c | 50.13% | 49.78% | 49.79% | 49.90% |

Cross-entropy for original rule is about 0.323–0.328; for inverted rule about 1.96–2.02; for the two reduced rules about 1.17–1.23. The model predicts parity of the three observed recent bits with high confidence. Once the actual law changes, its stored history remains available but its interpretation no longer produces the correct prediction. For the inverted law it is confidently wrong around 90% of the time. This is **task-rule transfer failure**, not loss of information in its recurrent state.

## What survives

- A model can retain exactly useful memory under its training dynamics and fail sharply when the dynamics change.
- Adjusting noise magnitude without changing the decision rule was an easier robustness test than this intervention.
- The model's output calibration should be evaluated under rule shift, not assumed from clean accuracy.

## What does not follow

No adaptation attempt was made after the law changed. The results do not establish inability to adapt if provided feedback or additional training. They do not test intrinsic robustness of all neural models, FRR efficacy, or a universal memory law. Data are generated, and predictions within trajectories are correlated; uncertainty estimation should resample whole trajectories.

## Next controlled contact

Offer limited post-shift feedback in separately declared arms: recurrent-state continuation with frozen weights, online gradient updates, external Bayesian change-point detection, and explicit rule-hypothesis tracking. Compare adaptation speed, false alarm rate, predictive log loss, and dependence on evidence availability; do not silently equate any behavior to a model changing its weights.
