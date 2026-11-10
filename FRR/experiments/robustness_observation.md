# Observation-noise robustness in an eight-state neural-memory world

**Status:** Executed controlled synthetic probe; 2026-11-10 UTC.  
**Code:** `robustness_observation.py`  
**Relation:** Extends `eight_state_nonlumpable_rnn.py` without changing the frozen 1,550-entry Garden.

## Question and controls

The world is the stationary eight-state parity process `S_t=(x_t,x_(t-1),x_(t-2))` with `x_(t+1)=x_t XOR x_(t-1) XOR x_(t-2) XOR eta_t`, where `eta~Bernoulli(.1)`. The model receives the current *observed* bit; independently corrupt each observation with `xi~Bernoulli(.1)`. The target is still the actual next world bit.

Train separate 16-hidden-unit GRUs on clean observations and 10%-corrupted observations, 350 Adam steps each, fresh 128×24 batches per step. Evaluate on **2,048 new independent world sequences**, using identical evaluation seeds across each model condition. Exclude first two positions (missing initial history). Three network seeds: 7, 17, 29. Reset model state between independent episodes. A second control resets recurrent state at *every timestep* during evaluation.

## Measured accuracy

| Seed | Clean trained, clean tested | Clean trained, noisy tested | Noise-trained, noisy tested | Hidden reset with noisy observations |
| --- | ---: | ---: | ---: | ---: |
| 7 | 90.02% | 70.89% | 77.21% | 49.69% / 50.31% |
| 17 | 89.66% | 70.15% | 77.26% | 50.56% / 50.53% |
| 29 | 89.87% | 70.63% | 77.24% | 49.86% / 49.64% |

The last column reports reset controls for the clean-trained/noisy-trained models respectively. Evaluation is finite-sample; numbers vary around expectation.

## Why this is interesting

The clean-trained model almost reaches the exact 90% Bayes accuracy available with all three **clean** current/past bits. Under 10% bit-flip observation noise, its performance falls to ~70.6%. Re-training under that noise raises held-out accuracy to ~77.2% across three seeds. A no-history model returns to ~50%, as predicted by the balanced stationary process.

As a useful reference, merely combining the three most recent noisy observations by parity yields exact expectation `1 - (.1 + .8*(1-.8^3)/2) = .7048` accuracy. The noise-trained recurrent model does better than that short-window baseline, plausibly by exploiting additional temporal consistency in the dynamical history. That attribution remains an **inference**, not a separately isolated representation analysis. A full Bayesian filter over the eight hidden states should be computed as a stronger comparator before labeling the improvement optimal.

## Limits and next controls

- The network is trained anew for the noise condition; this is adaptation through training, not spontaneous recovery or lifelong learning.
- The result is a model-specific, constructed process with only 3 seeds. It is not evidence for universal CERTX constants, decentralized memory, or general neural robustness.
- The same held-out evaluation world generator is seeded consistently per condition, but training sets differ and the clean/noisy training runs draw separate streams.
- Next: exact eight-state Bayesian filter on corrupted observations; simple 3-bit and longer-window feedforward baselines; independently varied noise levels and transition strengths; evaluation uncertainty by sequence; ablate history beyond three steps.
