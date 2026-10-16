# Bounded Prony audit of the relay's imperfect-probe idea

This is a **new constructed inverse-problem test**, not reproduction of the missing Claude `erase_gate.py`. It implements the mathematical two-exponential family independently; the family, notation and parameter values remain shared conceptual ancestry. It does not implement physical carrier interventions.

Script: [relay-prony-audit.py](../experiments/relay-prony-audit.py). Full exact laws, measurements, classifications and summaries: [relay-prony-audit.json](results/relay-prony-audit.json).

## Predictions and construction

Predictions were placed in the script header before execution: the Hankel determinant equals `F P (a−b)^2`; separated nonzero components are recoverable from four noiseless points, up to permutation; equal rates collapse to one amplitude sum; noisy fits can fail or become nonphysical.

Parameters are `F=.128`, `P=.06`, `a=.95`, `b=a−gap`, with gaps `.8,.5,.2,.05,.01,0`. For `k=0..3`, the law is `c_k=F a^k+P b^k`.

The sampling model is explicitly new: independent binomial arms with `p_plus=(1+c_k)/2` and `p_minus=(1−c_k)/2`, each with 200,000 trials per k and replicate. Their observed difference estimates `c_k`. There are 50 replicates per gap and one fixed RNG seed, 20261016. These are independent draws within the declared toy, not empirical intervention outcomes or independent benchmark replications.

The solver derives a second-order recurrence from the four measured points, extracts its two roots and solves a two-by-two amplitude system. It neither clips roots nor repairs nonphysical outputs. Classification first rejects degeneracy/complex roots, then rates outside `[0,1]`, then negative amplitudes or total amplitude above one. These are mutually exclusive first-failure categories, not a count of every violated constraint.

The larger root is assigned to `F` **by stipulation**. That ordering cannot identify an environmental rather than private carrier.

## Results

All six exact determinant checks passed. Every nonzero-gap noiseless law recovered both rates and amplitudes within numerical tolerance, up to the stipulated root ordering. At gap zero, the solver reports degeneracy and verifies the reduced law `(F+P)a^k`; individual amplitudes are not identifiable.

| Rate gap | Valid fits / 50 | Rates outside interval | Nonphysical amplitudes | Complex roots | Median absolute F error, conditional on valid fit |
|---|---:|---:|---:|---:|---:|
| .80 | 42 | 8 | 0 | 0 | .00818 |
| .50 | 24 | 26 | 0 | 0 | .02679 |
| .20 | 7 | 42 | 1 | 0 | .04773 |
| .05 | 1 | 43 | 4 | 2 | .05642 |
| .01 | 3 | 41 | 5 | 1 | .05540 |
| .00 | 2 | 46 | 1 | 1 | .05714* |

*At exact collision, this numerical error is measured against the generator's arbitrary split; the split is not uniquely defined by the population observation law. A physically admissible fitted two-component decomposition is therefore not evidence that the true split was recovered.

Conditional medians must be read alongside the valid counts. The small-gap medians describe one to three selected surviving fits, not overall reliable recovery. Even the widest gap has eight invalid fits. The high true slow rate `.95`, the chosen noise model, four-point estimator and lack of regularization all matter; this is not a universal error curve or a limit on better estimators. Cross-gap sampling was not paired, and no statistically monotone rate was claimed.

## What survived

This supports a precise distinction in the relay: **distinct rates can be algebraically identifiable while their finite-sample recovery is fragile**. At exact collision, there is a genuine identifiability failure. Finite-noise failed roots and arbitrary component splits illustrate why valid-fit counts and model-order checks belong beside reported parameter errors.

It does not verify Claude's reported median errors or claimed sample threshold. The sampling law may differ, and the original code is absent. It also does not locate a memory carrier, establish selectivity of repeated clearing, test the exponential intervention law, or compare against a statistically efficient estimator.

The next useful extension would use more than four probe counts, hold out some counts for prediction, compare one- and two-component models, and test nonexponential or coupled responses. A separately validated probe is still needed to attach carrier labels.

Primary mathematical context and scoped assumptions are in [CLAUDE_RELAY_SOURCE_WEAVE.md](../lineage/CLAUDE_RELAY_SOURCE_WEAVE.md).
