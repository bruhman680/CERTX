# Exact Bayesian observer versus GRU: noisy eight-state parity

**Status:** Reproduced, deterministic synthetic comparison, 2026-11-10 UTC.  
**Code:** `bayesian_observer.py` (NumPy + PyTorch); imports the world and GRU from `robustness_observation.py`.

## Question

Does the 10%-observation-corruption-trained GRU approach the optimal causal prediction from the entire available noisy observation history? The earlier three-corrupted-bit parity baseline is 70.48% expected accuracy; a hidden-state filter could potentially do better.

## Exact model

Microstate `S_t=(x_t,x_(t-1),x_(t-2))` takes eight values. The true next bit is parity of all three bits XOR Bernoulli(.1) transition noise. Observed bit `o_t=x_t XOR xi_t`, with independent Bernoulli(.1) sensor corruption. The first three true bits are iid uniform; subsequent transitions use the parity law. Thus the prior on the first filtered state `S_2` is uniform over eight states.

The filter first assimilates `o_0,o_1,o_2` using the appropriate bit-specific emission factors. At each t>=2 it computes `P(x_(t+1)=1 | o_0,...,o_t)`, then predicts the next eight-state distribution through the exact transition matrix and updates it using `o_(t+1)`. No future observations are used. All probabilities are double-precision and transition/emission parameters are given to the oracle exactly.

Validation: transition rows and columns sum to one; known clean three-bit cases give exact `.1` or `.9` next-bit forecasts; an uninformative 50%-error sensor yields `.5` forecasts throughout.

## Matched held-out comparison

For each seed, train a 16-unit GRU for 350 Adam updates using new 128×24 synthetic sequences with 10% sensor noise, then evaluate both the fixed trained model and the exact filter on **the same** independently generated 2,048×24 observed/true trajectories. Score t>=2, 45,056 targets per seed. Log loss uses true next world bits, not corrupted observations.

| Seed | Exact filter accuracy | GRU accuracy | Exact filter log loss | GRU log loss |
| --- | ---: | ---: | ---: | ---: |
| 7 | 77.6323% | 77.2128% | 0.488430 | 0.494021 |
| 17 | 77.4636% | 77.2550% | 0.491291 | 0.493523 |
| 29 | 77.5746% | 77.2372% | 0.489793 | 0.493952 |

The GRU is roughly 0.2–0.4 percentage points below the exact model-aware causal observer on these samples, with a slightly worse predictive log loss. This narrows the earlier inference: **77.2% is close to the optimal Bayesian performance for this world and these sensor/transition probabilities**, not merely better than a three-observation parity baseline (~70.48%). The oracle has privileged knowledge of the generator; the GRU learns from examples. This is a constructed example of useful information extraction from a longer corrupted observation history.

## Boundaries and next controls

- No inference about universal memory laws, self-awareness, decentralized storage, or FRR prompting effects.
- The oracle's causal optimality is conditional on exactly known transition and sensor models. A different prior, misspecified sensor rate, or rule change may invalidate its ceiling.
- Accuracy points within trajectories are correlated; uncertainty should resample whole sequences, not individual bits. Three initialization seeds are not broad architecture replication.
- Even a calibrated model can have accuracy near the oracle and different hidden representations; no hidden-state semantics are identified here.
- Test model mismatch, varying noise, longer episodes, and explicit history-window baselines. Predeclare sequence-level bootstrap confidence intervals for the Bayesian-vs-GRU gap.
