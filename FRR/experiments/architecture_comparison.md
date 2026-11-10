# Eight-state parity: matched architecture and information controls

**Status:** Executed synthetic benchmark, 2026-11-10 UTC.  
**Code:** `architecture_comparison.py`. Requires PyTorch 2.9.1+cpu.  
**Scope:** Three seeds, independent synthetic held-out trajectories; no natural cognition or general-model advantage claim.

## System and exact limits

Let `S_t=(x_t,x_(t-1),x_(t-2))` be a three-bit state, with `x_(t+1)=x_t XOR x_(t-1) XOR x_(t-2) XOR eta_t`, `eta_t` iid Bernoulli(0.1). The initial three bits are uniform and independently chosen; the eight-state uniform distribution is stationary. The visible input at each time is the single current bit `x_t`.

The exact optimal next-bit accuracy under a uniformly distributed state is 50% from `x_t` alone, 50% from `(x_t,x_(t-1))`, and 90% from all three bits. This identifies two information-poor controls and the information-available ceiling before neural training. The current-only visible-state partition is not strongly lumpable: worst-case one-step total-variation defect is 0.8.

## Matched test

At every train step, generate a fresh 128-sequence batch, each 24 observations long. Predict the next bit at every time `t>=2`. Train each model for 450 Adam steps, learning rate 0.012, binary cross entropy. Evaluate on a separate 1,024-sequence set generated from a fixed held-out RNG stream (per seed). Independent seeds 7, 17, 29 initialize model and training stream. Feedforward MLPs have two tanh layers of width 32 and receive exact windows of one, two, or three bits. Recurrent simple Elman RNN, GRU, and LSTM each have 16 hidden units and receive only the successive current-bit observations; their recurrent state resets between independent sequences.

| Model | Seed 7 | Seed 17 | Seed 29 | Mechanism |
| --- | ---: | ---: | ---: | --- |
| FF current-only | 49.74% | 50.01% | 48.40% | No informative history |
| FF two-bit window | 49.76% | 49.58% | 48.97% | Still missing one relevant bit |
| FF three-bit window | 89.86% | 89.95% | 90.21% | Explicit sufficient history |
| Simple RNN | 89.86% | 89.95% | 90.21% | Learned internal history |
| GRU | 89.86% | 89.95% | 90.21% | Learned internal history |
| LSTM | 89.86% | 89.95% | 90.21% | Learned internal history |

The 90.21% result is slightly above 90% because evaluation is finite; it is not evidence against the Bayes ceiling. Exact test correctness coincides for the successful models at these seeds, while their cross-entropy losses vary (roughly 0.321–0.329). In this short-horizon task, no recurrent architecture has a demonstrated accuracy advantage over a simple RNN or an explicitly sufficient feedforward window. Good recurrent prediction shows internal use of observation history, **not** superior intrinsic intelligence or a unique memory mechanism.

## Controls and remaining pressure

This is a deliberately balanced synthetic generator, not external-world measurement. The train/test divide is by independently generated sequences; their underlying eight-state patterns recur by design. A fixed three-bit window is an explicit information oracle relative to the one-bit observation stream. No shuffling control, gradient/hidden-state analysis, long-delay stress, observation corruption, model-capacity matching, or out-of-family transition generalization is included here. Since all successful models reach essentially the same accuracy, the next experiment should look at learning efficiency, robustness, state identifiability, and adaptive transfer rather than describing a GRU/LSTM accuracy superiority.

The result is consistent with classical partial-observability theory: retaining enough of the observation history can recover predictive sufficiency without reconstructing a semantically meaningful hidden ontology. It does not establish FRR/CERTX thresholds, a persistent memory across resets, or a decentralized store. Keep the frozen 1,550-entry Garden untouched.
