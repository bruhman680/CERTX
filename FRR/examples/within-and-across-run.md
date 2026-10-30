# One bed, many beds, and the label on a statistic

[CO-C1](../evaluation/claude-soil-observer-intake-v1/REPORT.md) uses a specified toy: each run receives a fixed hidden error probability P. Across fresh runs P takes two values, equally weighted, with mean0.2 and variance0.032. Within each run, outcomes are iid given P.

A within-run observer estimates its own fixed rate. Across independently resampled soils, per-run average rates remain dispersed. Across many runs that all share one fixed soil, the per-run averages instead concentrate around that same rate. More observers of one bed do not resample the soil.

```text
Mean error probability: 0.2
Variance between fresh hidden soil conditions: 0.032
Variance of a T-outcome mean across fresh soils: 0.032 + 0.128/T
Variance of that mean conditional on one fixed p: p(1-p)/T
```

This is a conditional mathematical result, not a real-agent measurement. Known-family likelihood can still classify one long run: it knows which candidate distributions to compare. A within-run centered statistic failing to reveal population heterogeneity does not make every kind of inference from that run impossible.

Before reusing a reported covariance, dispersion or accuracy, retain:

- The observation/sampling unit: outcome, window, episode, environment or group.
- What is held fixed and what is resampled between units.
- Whether the statistic conditions on a latent/context value or averages across it.
- How independence/calibration/model-family assumptions enter the conclusion.
- Whether apparent patterns can arise from the estimator itself.

For the demeaned lag1 statistic in the toy, an iid record split into20windows has expected value about-0.05. That finite-centering effect does not establish negative underlying dependence. Pooling across hidden conditions gives a different quantity. The word-order audit likewise shows a reversal-symmetric family can conceal an index convention mismatch; a non-reversible test exposes it.

These annotations help select a discriminating check. They do not certify that a real source is independent, calibrate an effective sample size, or establish that FRR improves behavior. The current source-role guard binds literal source quotations only; statistical interpretation is a separate obligation.
