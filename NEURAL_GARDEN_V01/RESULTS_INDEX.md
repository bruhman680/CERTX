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

## Subsequent research loops and living-world operations

**The user clarified that 1,000 means research *loops*, each containing as many reasoning passes, simulations, and tests as needed.** See `EXPLORATION_LEDGER.md` for actual completed loops, unanswered questions, and how evidence changed the plan. The 1,000-run batch below is only one experiment within that allowance.

- `THOUSAND_RUN_SWEEP.py`, `THOUSAND_RUN_META.json`, `THOUSAND_RUN_RESULTS.json`, `THOUSAND_RUN_REPORT.md`: **1,000 matched simulations** = four same-world conditions ×250 fresh seeds ×600 ticks. Final mean energy: original neural learned .00818, frozen .03211, stewardship learned .05884, fixed threshold .55 **.48557**. Crucially the .55 policy has slightly *negative* mean raw energy drift over the final 100 ticks; do not call it indefinitely viable. Original row-level data are privately retained and available on this branch as `THOUSAND_RUN_ROWS.jsonl.gz.b64`; decode with `base64 -d THOUSAND_RUN_ROWS.jsonl.gz.b64 | gzip -d > THOUSAND_RUN_ROWS.jsonl`. Archive SHA-256 and source provenance are in `THOUSAND_RUN_META.json`.
- `PERTURBATION_SHOCK_REPORT.md`, `PERTURBATION_LONGHORIZON_REPORT.md` and accompanying scripts/data: separate 200-run shocked/control test and 120-run 2,000-tick stability probe. Fixed threshold .55 without shocks declines from ~.483 energy at tick600 to ~.269 at tick2000, **disproving any inference of stability from the shorter horizon**. With shocks it falls toward .042. Resource recovery and energy recovery are distinct.
- `IMITATION_CAPACITY_REPORT.md`: teacher-supervised neural cells learn a useful resource-sensitive behavior; this is evidence of representational capacity, **not autonomous policy discovery**.
- `EVOLUTION_REPORT.md`: a separate explicitly demographic extension with birth, death, inheritance, and mutation; no demonstrated benefit from mutation over clonal neural controls.
- `LIVING_GARDEN.py`, `LIVING_GARDEN_GUIDE.md`: the new preferred **single persistent Garden**, with exact-state checkpoints, pause/resume, tick delay, logged interventions, and forks. Its canonical checkpoint is stored privately rather than publicly uploading neural weights and detailed history. This is an on-demand foreground process, not unattended hosting between sessions.

All new research is confined to `codex/frr-v05-explorations`; unrelated branches and the original historical Garden have not been changed.

## Next authorized research phase — longitudinal and adaptive probes

The user approved **the next 200 loops** within the existing 2,000-loop allowance. The ledger now documents **25 substantive loops completed overall**, not 200 loops performed or 2,000 loops exhausted. Only actual executed and interpreted work counts.

- `LONGITUDINAL_REPORT.md`, `LONGITUDINAL_fork_probe.py`, `LONGITUDINAL_fork_results.json`: seven exact-state futures of the one canonical living world out to 3,000 ticks. Continuous original learning has mean energy ~.00145 and 94.5% of cells near floor. Freezing learning earlier limits damage; grafting fixed .55 behavior helps more, but none of these counterfactuals proves viability. Original tick-100 checkpoint remains untouched.
- `LIVING_GARDEN.py`, `LIVING_GARDEN_GUIDE.md`, `AUDIT_NEXT_LOOPS.md`: corrected an earlier rollback gap. **Now** every intervention captures a verified full pre-intervention neural checkpoint, and `restore-fork` recovers it into a separate paused world. Abrupt power/process failure may still leave JSONL tick logs ahead of the latest checkpoint; reconcile before interpreting every log row as unique. `LIVING_GARDEN_replay_tick100.html` provides a portable read-only replay of 11 historical snapshots.
- `DYNAMICS_REPORT.md` and four paired scripts/datasets: threshold .50 can retain mean energy ~.657 at 20,000 ticks, whereas .55 falls to ~.035. Some cells still reach the energy floor, and near-zero drift at finite horizon is **not** indefinite stability. Diffusion changed the small energy budget despite the same three-tick harvest cadence; it slightly raises resource yield *per harvest*. Original-world and no-diffusion changed-world comparisons are clearly separated.
- `ADAPTIVE_RESEARCH_REPORT.md` and `ADAPTIVE_INDEPENDENT_AUDIT.md` plus scripts/raw records: individual teacher-free neural thresholds learn a modest advantage over their own untrained initialized controls. Yet a well-chosen **fixed .50** rule still substantially outperforms them at 5,000 ticks (~.671 vs ~.329 average energy in the specific held-out probe). Earlier superiority versus fixed .55 was a weak baseline choice for long horizons. No general advantage from the neural architecture has been established.

**Revised priority:** preserve the canonical living-world lineage, seek long-horizon policy stability under independent seeds, then ask whether adaptive controllers can generalize to perturbations where fixed thresholds fail. Keep environmental-law edits, teacher imitation, and mutation studies as separate interventions with matched controls.

## Additional approved continuation: loops 026–031

This is part of the user's **next 200 authorized research loops**, not evidence that 200 were completed. `EXPLORATION_LEDGER.md` now records **31 actual loops** overall. New local probes have been fully documented on this branch:

- `REGIME_DYNAMICS_REPORT.md`: 160 fresh matched fixed-rule trials on eight deliberately modified environment regimes. Fixed .50/.51 performance is highly fragile to resource regeneration and extraction costs; this is not a universal threshold.
- `REGIME_REPORT.md`, `AUDIT_REGIME.md`: 144 separate three-phase adaptive-regime runs. A combined resource shock, lower regrowth, and increased cost depleted nearly all cells; online learning's final matched advantage over trained frozen stochastic control was only ~+.0052 energy. The audit notes transferred thresholds but reset trace memory and meaningful floor-rate differences.
- `LONGITUDINAL_20K_REPORT.md`: nine 20,000-tick forks of the *same* canonical living-world checkpoint, without advancing the canonical state. At t20k fixed thresholds .49/.50/.51 retain ~.439/.459/.475 energy respectively; original neural learning is ~.00019. Two large shocks push .50 toward .029. These are dependent counterfactual branches of one world, not nine independent initial-world replications.
- `MILD_REGIME_REPORT.md`: 120 matched fresh simulations, only a mild regrowth .06→.055→.06 shift. Fixed .50/.51 rules collapse after the alteration (final energy .044/.050). A teacher-free online stochastic learner ends at .2065 versus identically trained frozen stochastic .1911, a **small paired advantage** across all 20 seeds. Frozen deterministic use of learned thresholds ends higher (.2690) but has ~46% near-zero-energy cells. This does **not** isolate policy updating from exploration mode nor establish long-term sustainability.
- `LIVING_GARDEN.py` now exposes a **read-only metric-log-health check**; the canonical paused t100 world has exactly 100 monotonic logged steps, zero entries ahead of the checkpoint, and unchanged full-state fingerprint. No automatic destructive log repair is attempted.

Next controlled question: can useful learning persist under **predeclared, mild held-out regime changes**, when both the learner and frozen controls use matched exploration budgets and deterministic evaluation? The 0.50 threshold remains a strong stable-world baseline but fails some perturbed-world tests.
