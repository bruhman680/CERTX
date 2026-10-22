# SR-C1 bounded protocol: different state space and imperfect resets

Frozen before first numerical execution. This implements the exact-population algebra slice of the AS-C1 priority1 draft, not the full calibration/noisy-sample study. No physical or actual-agent efficacy claim.

State is (m,s), with binary agent coordinate m and three-level soil coordinate s. Emission is p=.05+.2m+.2s, plus .08ms in a declared interaction stress case. Four mechanisms: shadow (soil fixed, agent redrawn), echo (soil redrawn, agent updated by outcome), wake (agent redrawn, soil updated by outcome), mixed (both updated). Agent update retains m with probability .6, otherwise draws Bernoulli(.1+.8y). Soil update retains s with probability .7, otherwise draws [.7,.2,.1] for y=0 or [.1,.2,.7] for y=1. Redraws are agent Bernoulli(.5) and uniform soil. These parameters are fixed; stationary error/covariance are NOT matched. Shadow stationary mixture is explicitly uniform soil.

A forced symbol y acts through update B_y without emission-based conditioning. A natural observed symbol additionally reweights the initial distribution by its emission likelihood. Compare forced1 versus forced0, plus both against the no-probe stationary baseline. Intervene immediately after that update. A reset independently replaces m by0 with probability rA, s by0 with probability rS. Reset rows: sham(0,0), agent-target(.8,.1), soil-target(.1,.8), shared(.6,.6), perfect-both(1,1). Matrices, stationary preparations, baseline shifts and six subsequent natural-outcome lags will be saved.

Predictions before execution:
- Additive first-outcome contrast is (1-rA)*a+(1-rS)*b, where a=.2 DeltaE[m], b=.2 DeltaE[s]. This must follow from actual matrices, not an imported decay fit.
- The shared reset plus sham cannot allocate two arbitrary contributions: its measurement rows are proportional. A coordinate-diverse design can. This is an identification result about this response summary and stipulated measurement model, not about all possible observations.
- Static shadow has zero forced contrast yet resetting soil can change its baseline; null probe contrast must not be called no environmental persistence.
- The interaction readout generally needs a third contribution c=.08 DeltaE[ms]. Its reset factor is (1-rA)(1-rS). Two-carrier fits can become inconsistent; three rows may support three contributions when calibrated and full-rank.
- Mislabeling imperfect/off-target resets as perfect will bias allocations. Known actual operators can recover the defined contributions in full-rank cases. No empirical witness calibration is provided here.

Before any noisy fitting: enumerate complete binary word laws to length4 under each preparation/reset for all8 world/readout combinations, compare pairwise TV, and return exact-within-tolerance candidate sets. Equality at length4 is only truncated observational equivalence. Tolerances: stochastic/stationary/algebra1e-10, rank/TV distinguishability1e-10, reported full-vector differences. No retuning, sampling, optimizer or outcome-driven parameter search.

Scope exclusions: finite-sample discrimination, equal-sampling-budget comparisons, calibration estimation/envelopes, gate-restoration witnesses, unknown-family identification and real resets remain deferred. Candidate laws assume known kernels and calibrated reset semantics; no claims of passive impossibility follow from this unmatched construction. Artifact checks and later report changes cannot alter the frozen protocol's original predictions.
