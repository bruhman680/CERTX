# Exogenous resource shock pilot — learning is not the same as resilience

**Status:** Exploratory, 200 synthetic runs; not included in either earlier 100-run sweep or the separate matched 1,000-run unperturbed study. This extension was designed and evaluated after the .55-threshold observation and is not a preregistered confirmatory study.

## Intervention, controls, and provenance

- Original neural Garden v0.1 learned, frozen neural Garden v0.1, and fixed nonlearning local thresholds `.45`, `.55`, `.65`.
- **20 matched fresh seeds** `710..729`, grid 16×16, horizon 600 ticks; each policy tested **with and without shocks**: `5 policies × 20 seeds × 2 conditions = 200 runs`.
- Within each ordinary tick, both implementations use the **unchanged original v0.1 resource/energy laws**. Only the shocked arm receives a clearly labeled **external** resource-field multiplier `resource *= 0.40` immediately after steps 200 and 400. All other coefficients unchanged.
- The intervention changes the world state, rather than a growth coefficient. Shocks are uniform in time and space, externally scheduled, known to the experimenter, and are not realistically seasonal stochasticity.
- Code: `PERTURBATION_shock_pilot.py`; individual run trajectories and summaries: `PERTURBATION_shock_results.json`. JSON records Python/NumPy versions, SHA-256 source fingerprints, per-run trajectory checkpoints, explicit policy, seed and shock status.

## Outcomes at step 600

Each value is the mean of 20 runs per condition; the table reports one snapshot after the second shock, not a statistical proof of indefinite behavior.

| Policy | No-shock mean energy | Shocked mean energy | No-shock floor fraction | Shocked floor fraction | Median resource recovery after first shock |
| --- | ---: | ---: | ---: | ---: | ---: |
| Neural learner v0.1 | .00779 | .00817 | .7176 | .7061 | 27 ticks (among recovered runs) |
| Frozen neural v0.1 | .03091 | .03091 | .3176 | .3176 | 33 ticks |
| Threshold .45 | .29984 | .06580 | 0 | .1686 | 7 ticks |
| **Threshold .55** | **.48370** | **.11700** | **0** | **0** | **9 ticks** |
| Threshold .65 | .03840 | .05660 | .2004 | 0 | 11 ticks |

The naive reading “threshold .55 is resilient because the resource returns in nine ticks” is false. Under the two imposed shocks the resource pool does regrow quickly, but **cell energy takes a lasting hit**, falling from .484 without shocks to .117 by step 600. Resource recovery is not equivalent to population energy recovery. The fixed .55 rule remains the best of these five after two shocks at this endpoint; it did not maintain its original energy reservoir.

The .65 threshold **improved** final energy slightly relative to its unshocked condition. This is possible in a state-dependent, nonlinear, bounded system: resource removal changes action timing, and therefore extraction. It does not prove shock exposure is broadly beneficial; it is a conditional toy-world result requiring targeted replication.

For interpretation, action–resource covariance averaged over 600 steps was positive under fixed thresholds: `.55` unshocked `+.01030`, shocked `+.00491`; original neural learned unshocked `−.00046`, shocked `−.00045`. These are descriptive covariances within the simulated action/resource trajectories, consistent with resource-selective timing. The mean *raw pre-clipping* energy budget is recorded per run alongside floor/ceiling occupancy; end-state mean energy alone is not a sufficient sustainability metric.

## Failure modes and next questions

1. The neural learners were already close to the energy floor in the unshocked arm; apparently small shock effects on their final energy do **not** demonstrate resilience. The floor masks losses.
2. The resource recovery diagnostic means "first time aggregate mean resource returns to its value immediately **before** the shock," not individual cell restoration or recovery of energy. Some neural runs never met this condition by the next shock/end.
3. This study did not train on shock schedules or test adaptive thresholds. It cannot establish that neural cells are intrinsically worse than learning agents with suitable long-horizon objectives.
4. Original networks and fixed thresholds differ in policy class (stochastic learned action vs deterministic resource-conditioned action); the threshold is a deliberately strong hand-coded baseline.
5. Recovery, energy and covariance are correlated across time and cells; the independent replicate is the **seeded run**, not each tick or cell. The seeds are fresh relative to earlier studies, but the experiment was inspired by earlier results.

**Next evidence-driven iteration:** train or test an action-aware neural policy on changing environments, and compare its unseen-shock recovery against *frozen* fixed thresholds on matched seeds. Distinguish adaptation during shock from merely reducing harvest and track an energy-recovery window (not just resource recovery).
