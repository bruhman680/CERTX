# Independent adversarial audit — regime-shift and world-law robustness probes

**Scope:** `REGIME_garden.py`, `REGIME_sweep.py`, `REGIME_results.json`, `REGIME_DYNAMICS_probe.py`, `REGIME_DYNAMICS_results.json`, and surrounding adaptive/dynamical lineage. These are synthetic exploratory experiments, *not* 200 research loops or evidence of a new universal law.

## Audit outcome at artifact freeze

**Reproducibility checks PASS:** the adaptive regime archive contains 24 trained/test seed pairs, 6 policy arms, and eight checkpoints per run, i.e. **144 simulations and 1,152 checkpoint rows**, not 1,152 independent runs. Train seeds 2500–2523 and test seeds 12500–12523 are disjoint. The separate coefficient screen contains **160 simulations** = 8 world regimes ×5 thresholds ×4 matched fresh seeds, with 5,000 ticks per simulation. All SHA-256 source digests recorded in both JSON files match present source bytes. An exact numerical replay of the coefficient screen's `base` / threshold .50 / seed 1040 condition matched every numeric result field, including t5000 energy and raw tail drift.

**Interpretation:** The two experiments test different questions. The 144-run adaptive experiment changes regrowth *and* harvesting cost *and* applies a resource shock at a shared boundary; it tests policy response to a severe combined exogenous regime. The 160-run dynamics experiment changes one physical coefficient at a time for an *entire* 5,000-tick world, and cannot tell us about adaptation to a midlife shock. Neither should be called an original-law homogeneous baseline.

## Adaptive regime experiment: what the data actually discriminate

Each tested world starts with the same seed-dependent resources and energy across policy arms. At the transition step when internal tick first equals 1000, resource is multiplied by **0.7 before the cell actions**, regrowth changes `.06 → .025`, and harvest cost changes `.055 → .070`. At internal tick 2000, both coefficients revert to original values, but the lost resources and energy are **not** reset. Distinguish the zero-based internal transition tick from post-step snapshot labels (shock first appears in the next completed tick).

| Arm | Mean energy t999 | t1200 | t3000 | Floor fraction t3000 |
| --- | ---: | ---: | ---: | ---: |
| Online stochastic neural threshold learning | .265 | .001 | **.1995** | .223 |
| Same pretrained thresholds, frozen stochastic | .263 | .001 | **.1943** | .228 |
| Same pretrained thresholds, frozen deterministic | .311 | .002 | **.2702** | .430 |
| Untrained stochastic heterogeneous thresholds | .242 | .001 | **.1861** | .238 |
| Uniform deterministic .50 | .618 | .002 | **.0220** | .000 |
| Uniform deterministic .51 | .617 | .000 | **.0469** | .000 |

### Causal interpretation constraints

1. **Learning effect is modest in the chosen regime:** at t3000 online minus matched pretrained-frozen stochastic energy is **+.00519** across 24 paired worlds (seed SD .00699; descriptive normal-approximate mean interval ~[+.00240,+.00799]). This is measurable *within this generator*, but far below the between-controller architecture/deployment differences. Online compared to frozen deterministic changes both learning and action stochasticity; that contrast **does not isolate learning**.
2. **The deterministic pretrained arm has highest mean energy but poor coverage:** about **43%** of its cells are near the energy floor at t3000. Conversely fixed .50 has near-zero average energy although few cells meet the strict ≤.01 floor definition at t3000. Report energetic fraction above .10, floor fraction, and raw drift together rather than calling the highest mean a healthy society.
3. **Catastrophic scarcity is common to all arms:** by t1200, ~94–100% of cells in each arm are close to the floor. Mean-energy recovery after the world's original coefficients return is not evidence of pre-shock resilience.
4. **The shocks are confounded by design:** resource×.7, reduced regrowth, and increased action cost happen together. This is an externally imposed *combined* stress test. A factorial ablation is required to say which factor caused threshold .50's failure or adaptive recovery differences.
5. **Pretraining-state caveat:** the trained threshold vectors are transferred into freshly initialized test worlds, but online eligibility traces and running reward baselines are reset; this is *parameter transfer plus new online learning*, **not** uninterrupted continuation of the full trained recurrent/eligibility state. Exact train/test seed disjointness is good, but the test world's per-coordinate threshold mapping is fixed spatially. The controller is a scalar logistic threshold, not the original 12-unit recurrent neural network.
6. **Fairness controls:** online and frozen stochastic share their initial trained thresholds and action RNG seeds; their future sampled actions diverge as online thresholds adapt. Frozen deterministic lacks exploration cost and is an important *deployment* comparator, not a matched stochastic learning counterfactual. Uniform fixed thresholds have different policy representation and should remain labeled external baselines.
7. **Reporting:** the archive stores per-arm trajectories, floor/ceiling, raw tail drift, resource–action covariance, threshold movement and source hashes. Paired seed is the replication unit. The 256 coupled cells and eight checkpoints are not independent trials. The window lengths/timing and world laws were researcher-chosen; this is exploratory within-model evidence, not external confirmation.

## Fixed-rule coefficient screen: what survives changing physics?

All 160 runs use one coefficient deviation at a time relative to (`alpha` regrowth .06, `beta` harvest depletion .18, `kappa` diffusion .08), five already screen-informed thresholds `.48,.50,.51,.525,.55`, and just **four matched seeds** per condition. This is a sensitivity map, not a statistically powerful independent generalization study.

### Important controls and cautions

- **Resource budget verified:** mean diffusion sums to zero on the toroidal grid, and the archived maximum resource conservation residual is near floating-point precision (~2e-17). The mean-energy identity residual is similarly tiny. Thus the reported law effects are consistent with the explicit simulated balance equations.
- **World-law improvements can saturate the ceiling:** lowering harvest consumption or increasing regrowth drives nearly all tested thresholds close to energy 1.0. This is a physical-law intervention, not learned policy competence; clipping can conceal surplus and reduce discriminatory power.
- **World-law degradations can saturate the floor:** lower regrowth or higher consumption pushes thresholds toward depleted energies. A policy ranking near the floor is not necessarily meaningful without raw energy deficits and fraction below a biologically relevant reserve.
- **Diffusion modifies harvest-time resource amount**, not necessarily harvest interval; existing phase probes found three-tick cycles with and without diffusion. A high-energy state near `.50` depends on precisely chosen original-world coefficients; do not promote it to a universal optimum or stable attractor.
- **Source checks PASS**, but the study is still posthoc and only uses four seed replicates. Validate important candidates on new seeds and much longer horizons with intervention response and unclipped budgets before claiming robustness.

## Next high-value loops

1. **Disentangle the combined scarcity event:** run a four-arm ablation on the exact same pretrained seed/world forks: no change, resource shock only, coefficient change only, combined change. Keep action stochasticity matched and report recovery time of resources and energy separately.
2. **Test a frozen, explicit controller benchmark under changed laws** before adding learning complexity. Threshold .50 and .525 have near-neutral raw energy budgets in one physics regime; show where their viability corridor collapses. Change **one law at a time** and use both raw drift and boundary occupancy.
3. **Discriminate adaptive selection from inherited heterogeneity:** compare online stochastic vs frozen stochastic starting from identical thresholds, then compare deterministic deployments and an independently optimized static heterogeneous policy. Avoid conflating heterogeneity, online learning, stochastic exploration cost, and environmental adaptation.
4. **Preserve the Living Garden as primary historical subject:** fork exact checkpoint twins before applying treatments, name every exogenous change and starting tick, and never silently overwrite the world laws or conflate shared long-history observations with independent replicate seeds.

### Separate operator audit update

`LIVING_GARDEN.status` now exposes **read-only** `metric_log_health`: number of step rows, highest logged tick, non-increasing tick transitions, malformed JSON rows, and whether logged ticks lie ahead of the saved checkpoint. This detects a common crash-consistency ambiguity without discarding or rewriting any historical records. It cannot repair an interrupted checkpoint or guarantee that all unique steps were recorded; automatic reconciliation is a separate engineering task. `LIVING_GARDEN_GUIDE.md` documents the warning and the exact pre-intervention full-state backup/recovery fork mechanism.
