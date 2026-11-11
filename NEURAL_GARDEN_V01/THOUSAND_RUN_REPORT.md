# Neural Garden — 1,000 matched synthetic simulation runs

**Execution:** Completed in the research workspace, 2026-11-11. **Count:** exactly 1,000 independent seeded simulator runs (not 1,000 biological generations, scientific discoveries, or successive design modifications).

## Predeclared design

- Four policy arms, **250 matched fresh seeds** per arm, seeds 300–549; each run has a **16×16 grid (256 cells)** and **600 synchronous ticks**. Total 600,000 whole-grid run-ticks.
- All arms use the **original** v0.1 environmental coefficients (`.06` regrowth, `.08` diffusion, `.18` resource consumption, `.03` metabolism, `.055` harvest action expense, `.008` resting subsidy, `.25` resource-to-energy benefit). No world-law edits.
- `v01_learning`: original independent neural controllers update their weights; `v01_frozen`: same initialized neural architecture without learning; `v02_stewardship`: same world with explicitly designer-modified learning reward (+0.65 × local resource change); `threshold_055`: deterministic, **non-neural** local resource threshold .55, chosen from prior exploratory work.
- This is a same-seed, same-law, same-horizon **matched comparison** that the earlier 200-run series lacked. Seed matching controls initial conditions but *not* all stochastic downstream trajectories; cells within each run are not independent samples.

## Final tick 600 (means across 250 seeds per arm)

| Arm | Mean cell energy | Mean resource | Harvest fraction at tick 600 | Fraction cells at energy floor ≤.01 | Mean resource/action covariance over full run |
| --- | ---: | ---: | ---: | ---: | ---: |
| v0.1 learning | **0.00818** | .33955 | .65158 | 71.30% | −.00046 |
| v0.1 frozen | **0.03211** | .40026 | .50281 | 30.42% | −.00061 |
| v0.2 stewardship neural | **0.05884** | .44234 | .42164 | 16.01% | −.00035 |
| **Fixed threshold .55, no neural learning** | **0.48557** | .52088 | .32356 | **0%** | **+.01033** |

Mean energy for .55 exceeds original learned neural by **+.47738** and stewardship learned neural by **+.42672** on the 250 matched seeds; across-seed paired SDs are .00679 and .00761 respectively. The original neural learner is below its frozen control (−.02393), while the stewardship reward improves over original learner (+.05066). This is a **within-simulator descriptive comparison**; deliberately chosen policies and world parameters preclude general claims of biological significance or statistical independence across spatially coupled cells.

## Distinguish accumulated energy from long-term balance

The simulator clips energy to `[0,1]`. This study also calculates the **unclipped** raw energy budget on each tick, before clipping, using the original law. Averaged across 600 steps, mean raw energy drift per step was approximately:

| Arm | Whole-run mean raw drift/tick | Mean raw drift in last 100 ticks |
| --- | ---: | ---: |
| v0.1 learning | −.005910 | −.007630 |
| v0.1 frozen | −.003366 | −.003568 |
| v0.2 stewardship | −.002570 | −.002134 |
| fixed threshold .55 | **−.000108** | **−.000120** |

**Important correction:** The threshold policy retains a much larger energy reserve through tick 600 and has a much less negative raw energy budget. Its **mean raw drift over the final 100 ticks is still slightly negative** in this 1,000-run study. Earlier single-tick measurements sometimes showed positive drift; those did not establish long-run equilibrium. Even this considerably stronger policy is **not demonstrated indefinitely sustainable**.

The resource–action covariance is a potentially important mechanism. The threshold policy preferentially harvests when resources are high, creating a *positive covariance* not captured by homogeneous constant-rate mean-field analysis. Learned policies have small negative covariances in this particular simulator. This mechanism is consistent with the energy advantage but does not imply universal optimality or learned intelligence.

## Provenance, checks and continuation

- Runner: [`THOUSAND_RUN_SWEEP.py`](THOUSAND_RUN_SWEEP.py), using existing model sources unmodified.
- Each individual run, its configuration SHA-256, five measured trajectory checkpoints at ticks 0/100/200/400/600, pre-clipping drift, covariance, tail metrics and full model-state fingerprint: [`THOUSAND_RUN_ROWS.jsonl`](THOUSAND_RUN_ROWS.jsonl).
- Source SHA-256, model configuration, Python/NumPy/platform version: [`THOUSAND_RUN_META.json`](THOUSAND_RUN_META.json).
- Aggregate descriptive statistics, matched comparisons, archival JSONL SHA-256: [`THOUSAND_RUN_RESULTS.json`](THOUSAND_RUN_RESULTS.json).
- The script supports interrupted/bounded progress using per-run durable newline JSON records and validates its metadata/source hashes on resumption.
- Post-run checks: exactly 1,000 JSONL records and unique IDs, aggregate SHA-256 matched bytes, and exact deterministic full-state fingerprint replay of the first run.

**Limitations:** This remains an artificial, fixed-coefficient toy environment. The .55 threshold was informed by prior screens, so there is selection bias. We have not tested changing seasons, unseen costs, external resource shocks, births, deaths, mutation, inheritance, transfer learning, or natural language. The .55 policy does **not** learn. The neural policies do update weights, but they do not currently produce superior ecological outcomes.

**Next discriminating experiment:** Introduce an *action-conditioned* learning rule that can use its own observed resource to infer the consequences of harvesting, without hard-coding the .55 threshold; freeze the comparator. Then jointly test on fresh, held-out resource-law perturbations and longer horizons, measuring both reserve energy and raw resource budget. Keep policy architecture, world-law changes, and evolutionary reproduction as distinct interventions.
