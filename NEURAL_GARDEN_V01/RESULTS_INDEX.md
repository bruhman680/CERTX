# Neural Garden — experimental record and continuation point

**Branch:** `codex/frr-v05-explorations` in `bruhman680/CERTX`.

The Garden is a bounded, replayable cellular experiment with separate small recurrent neural controllers in each of 256 cells (at 16×16), original resource and energy rules, and checkpointable model state. This is a synthetic research testbed, not demonstrated open-ended evolution or intelligence. The original 1,550-entry historical Garden is untouched.

## What was actually completed

1. **Neural policy sweep:** 100 runs = 5 conditions × 20 matched seeds 100–119, 200 ticks each. `hundred_cycle_sweep.py`, `hundred_cycle_results.json`, `HUNDRED_CYCLE_REPORT.md`.
2. **Conditional harvesting sweep:** another 100 runs = 5 fixed thresholds × 20 matched fresh seeds 200–219, 600 ticks each. `threshold_100_sweep.py`, `threshold_100_results.json`, `THRESHOLD_100_REPORT.md`.

Both contain individual run IDs, parameters, checkpoints, numerical measurements, and SHA-256 source fingerprints. `HUNDRED_CYCLE_AUDIT.md` independently checks the counts, computations, and caveats. There were **200 simulation runs**, **80,000 summed run-ticks**, and **256 cells per run**. A run-tick is not a neural update count or an independent biological replicate. Exploratory pilots are separately recorded and excluded from the 200.

## Results that constrain the next design

| Condition | Final mean energy | Horizon | Caveat |
| --- | ---: | ---: | --- |
| Original neural learner | 0.01730 | 200 | Better on-policy prediction, worse ecology than frozen |
| Original frozen neural | 0.06120 | 200 | Same original world; no learning |
| Stewardship neural learner | 0.08025 | 200 | Reward modified, world unchanged |
| Easier-world neural learner | 0.98263 | 200 | Metabolism lowered from .03 to .02 |
| Easier-world frozen neural | 0.98682 | 200 | Also thrives; not evidence of neural learning |
| Fixed resource threshold .55 | 0.48762 | 600 | Original world, no neural learning, different sweep |

The threshold result is **not** a matched 200-tick head-to-head against neural variants; it uses different seeds and a longer horizon. The five thresholds screened at tick 600 were .35→.00769, .45→.30474, .55→.48762, .65→.03721, and .75→.02123. The best tested threshold is not a proven optimum and the settings were informed by exploratory pilots.

Analytically, all homogeneous constant-probability harvesting policies have negative long-run raw energy drift **under a restricted mean-field approximation**. Conditional policies preserve a resource–action covariance that this approximation erases. See `MEAN_FIELD_BOUND.md`; no general impossibility claim is made.

## How to continue

- Use `README.md` and `OPERATIONS.md` for finite-run, checkpoint, pause/resume, inspection, and replay instructions.
- Use `EVALUATION.md`, `STEWARDSHIP_EVALUATION.md`, `STEWARDSHIP_AUDIT.md`, `RESEARCH.md`, and `STEWARDSHIP_RESEARCH.md` for antecedents, controls, and interpretation.
- Use `heuristic_counterfactual.py` and `.json` for separately labeled exploratory pilot data.
- The privately archived demonstration checkpoint and HTML replay were intentionally **not** committed to the repository; the source and tabular raw experimental records were.

**Next experiment, before claiming adaptive intelligence:** Compare a genuinely action-aware neural cell with the frozen .55 threshold under **identical original-world seeds, durations, observations, and metrics**, then test both under held-out environmental shifts, scarcity shocks, and longer horizons. Track pre-clipping energy budgets, resource recovery, and lineage of any newly introduced mutations. Keep birth/death/reproduction as a separate, labeled extension.
