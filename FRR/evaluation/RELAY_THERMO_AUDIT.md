# Relay thermodynamic rebuild: reproduction and scope audit

Source: archived unmodified `lineage/sources/claude-relay-2026-10-15/thermo2.py`, `verify.py`, and relay notebook. Both original scripts executed successfully. `verify.py` retains Claude's obsolete scratchpad path, but Python also searches the script directory and found the archived `thermo2.py` and `wake.py`; no original needed editing. Saved stdout is in `evaluation/results/relay-thermo-original.txt` and `relay-thermo-verify-original.txt`.

Additional executable: `experiments/relay-thermo-audit.py`. Machine-readable output: `evaluation/results/relay-thermo-audit.json`. This audit uses an independent linear stationary solve and directly sums microscopic paths for selected word lengths rather than relying solely on the imported forward algorithm. It is an implementation cross-check with shared model ancestry, not independent real-system replication.

## What reproduced

- The common normalizer plus self-loops gives the Boltzmann stationary law at zero affinity. Original power-method errors were about 1e-14–6e-14; the direct linear solve agrees to numerical tolerance. Zero-affinity entropy production is numerical zero.
- At affinity A=2, the six-state chain has stationary entropy production `sigma = 0.03558049` nats per uniformized step.
- The ternary labeling `[0,0,1,1,2,2]` gives `d_3/sigma = 1.09958`: finite-increment monotonicity and the claimed pointwise upper bound by sigma are false. The original script records the failed prediction; the relay correctly retracts it.
- The cumulative block bound `D_n <= (n-1)*sigma` holds in the tested ranges. Nonnegative increments hold to floating-point tolerance.
- `d_2` equals the stationary first-order lumped flux entropy production in every tested partition.
- Full-state observation gives `D_n = (n-1)*sigma`, checked through n=5. Direct microscopic path summation agrees with the original word algorithm at n=2,3,5.
- The three-state binary observation gives zero detectable time asymmetry through n=14 despite positive microscopic dissipation. Its singleton-state regenerative structure supports the alternating-renewal explanation, rather than extrapolating from a finite zero alone.

## A new scope correction: boundary-edge equality is conditional

The relay says first-order lumped EPR equals dissipation on block-boundary edges. The verification script tests only the two listed ternary partitions. Those have exactly one microscopic boundary edge per unordered pair of macro labels, so no distinct boundary channels are merged. Equality is valid there, but not for arbitrary partitions.

| Chain / partition, A=2 | Full sigma | Boundary-edge sigma | First-order lumped sigma |
|---|---:|---:|---:|
| 3-ring `[0,0,1]` | 0.15566029 | 0.10403016 | 0 |
| 4-ring `[0,0,1,1]` | 0.08078517 | 0.04009977 | 0 |
| 6-ring `[0,0,0,1,1,1]` | 0.03558049 | 0.01106305 | 0 |
| 6-ring alternating | 0.03558049 | 0.03558049 | 0 |
| 6-ring `[0,0,1,1,2,2]` | 0.03558049 | 0.01786188 | 0.01786188 |
| 6-ring `[0,1,1,1,1,2]` | 0.03558049 | 0.01497136 | 0.01497136 |

For every stationary binary process, total one-step flux from label 0 to label 1 equals the reverse flux. Thus the first-order binary lumped EPR is zero, even when microscopic boundary channels dissipate. Longer words can still reveal asymmetry: at n=14 the six-state halves partition recovers roughly 2.34% of microscopic sigma, whereas its one-step flux remains exactly symmetric.

Writing stationary micro flux as `f_ij = pi_i P_ij`, aggregation sums several fluxes into `F_ab`. The log-sum inequality gives:

`sigma_lumped <= sigma_boundary <= sigma_full`.

Equality in the first inequality requires equal forward/reverse flux ratios across the microscopic channels being aggregated (a single channel is a sufficient special case). In these binary partitions opposing channels cancel net macro flux while retaining dissipation. This is an example of the compression erasing a distinction between parallel routes, rather than merely hiding internal block motion.

## What the mathematical bounds actually say

Let `D_n` be relative entropy between the stationary visible n-word law and its reversal. Marginalization maps the n-word comparison onto the `(n-1)`-word comparison; data processing therefore gives `D_n >= D_(n-1)`. This establishes `d_n >= 0`.

Applying the label map to a stationary microscopic n-path and its reversal gives `D_n <= (n-1)*sigma`. The microscopic path identity uses stationarity and the discrete-time Markov chain; no claim that the visible process is Markov is needed.

These two inequalities do not imply that successive increments increase or that every increment is at most sigma. If an increment limit exists, its Cesàro average equals the block-rate limit, so that limit is bounded by sigma. Finite calculations do not independently prove existence or the value of the limiting rate. The relay's near-one ratios at n=9 are convergence evidence within this toy, not a general theorem of eventual full recovery under a ternary partition.

## Physical and implementation boundaries

- The measured quantity is stationary path irreversibility in nats per uniformized step. Interpreting it as physical entropy production requires the stated local-detailed-balance model and a thermodynamic implementation. Multiply by Boltzmann's constant for entropy units when justified.
- Continuous-time rates `r` are uniformized using `Z=1.05*max row sum`. Physical-time entropy production equals `Z*sigma_step` if those rates define the physical time unit. Z changes with energies and affinity; per-step values should not be silently compared as equal-duration physical rates.
- For N>=3, neighboring forward/backward rate ratios have energy term `-beta*(E_j-E_i)` and affinity increment `A/N`; the cycle affinity is A. At A=0 detailed balance holds with Boltzmann weights because the shared normalizer cancels.
- `ring_chain` should be regarded as N>=3: at N=2 the forward and backward neighbor coincide and assignment overwrites a rate. No claim above uses N=2.
- `epr` skips unsupported reverse edges instead of reporting infinite entropy production. All tested ring chains have bidirectional support, so this does not affect the present outputs. Reusing it on one-way chains would require a guard or revised implementation.
- The original power-method stationary function uses a fixed number of iterations. The independent solver checks the supplied small cases; this is not a general convergence certificate for arbitrary parameters.
- Nothing here validates CERTX numerical constants, fiber spread as physical entropy production, or general claims that “all hidden EPR” disappears under every coarse-graining.

## Effect on the open exploration

The valid stationary-chain rebuild is now executable and reproduced in the stated small-ring domain. The unresolved question moves from “is the chain thermodynamically consistent?” to “which label maps, histories, channel records, and time observations preserve which irreversibility?”

A useful next contact is to record boundary-channel identity as an extra observable, then compare one-step and longer-word EPR at matched physical time. That would isolate loss through channel merging from loss through omitted temporal structure. It should preserve the binary counterexample as an explicit control.
