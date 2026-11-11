# Social observations without overwriting neural memory — one completed follow-up research loop

**Question/predeclared design:** `SOCIAL2_ADVICE_PLAN.md`. On 12 fresh seeds (10800–10811), each cell first trains its own energy-aware neural controller for 1,500 stable-world steps. Training is then disabled, its weights are kept exactly unchanged, and a matched fork evaluates 5 observation-sharing schemes through 2,000 deterministic deployment ticks in stable or mildly reduced regrowth. Results contain **120 policy deployments**, with paired outcomes at deployment ticks 500 and 2,000.

## Results at deployment tick 2,000

| Observation input | Stable mean energy | Stable energy floor | Mild-shift mean energy | Mild floor | Mild wins vs own, /12 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Own current resource only | .1657 | .130 | .0173 | .334 | reference |
| Own + fresh mean cardinal neighbor (50:50) | .2019 | .076 | .0221 | .334 | 11 |
| Own + fixed random cardinal neighbor (50:50) | .1964 | .111 | .0203 | .322 | 10 |
| Own + globally shuffled current resource (50:50) | .1882 | .078 | .0207 | .306 | 11 |
| Own + one-step-stale neighbor mean (50:50) | **.2170** | **.060** | **.0303** | **.295** | **12** |

All resource observations were used solely as input features to previously learned individual policies. Weight arrays were explicitly checked for byte-for-byte equality before/after deployment.

At tick 500, stable own-only mean energy was .0803, fresh-neighbor .1262, global shuffle .1106, and stale-neighbor .1432. Mild-shift values were .0172 own-only, .0224 fresh-neighbor, .0201 global shuffle, .0273 stale-neighbor. The signal was visible before the 2,000-tick endpoint.

## What we actually learned

Non-destructive observation sharing **can** improve these frozen neural policies in this synthetic world. This corrects the over-broad intuition drawn from `SOCIAL2_REPORT.md`: *copying the neighbor's entire neural policy* harmed performance, whereas *sharing an observation while retaining the cell's own learned policy* helped on matched forks.

However, the result does **not** isolate social learning. Global shuffling also helps, which suggests averaging noisy inputs (smoothing/regularization/threshold shifts) may explain much of the gain. Even more importantly, the one-step-**stale** neighbor signal is best, so fresher spatial information is not uniformly superior for this controller. It may be acting as a lagged low-pass filter that improves timing; the study cannot distinguish that from neighbor information per se. The observation rule is human-designed rather than discovered by the cells.

## Next discriminating pressure

Predeclare a simple **own-history temporal average** control (without any neighbor input), an independently time-shuffled neighbor history placebo, and matched comparison to fixed threshold .50 and neighbor-gradient manual policies. If stale neighbors outperform own-history and shuffles under multiple regrowth regimes and horizons, there may be a genuine information-sharing contribution. If all temporal averaging helps equally, name it temporal smoothing rather than collective memory.

## Reproducibility

Source: `SOCIAL2_ADVICE_probe.py`; complete row-level synthetic results: `SOCIAL2_ADVICE_results.json`. Original Garden code and canonical persistent-world checkpoints untouched. The 120 deployments are **one** hypothesis→test→revision research loop, not 120 research loops. No confidence intervals, population generality, or autonomous learned communication are claimed.
