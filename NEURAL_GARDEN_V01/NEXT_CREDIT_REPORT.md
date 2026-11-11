# Neural Garden credit assignment — three falsifiable mechanism probes

**Status:** Executed predeclared main study, **independent audit pending**. The plan `NEXT_CREDIT_PLAN.md` and source `NEXT_CREDIT_garden.py`, `NEXT_CREDIT_probe.py` were frozen before the outcome-bearing run. A smoke test used disjoint seeds 10700–10701. Main study used twelve fresh matched seeds 9700–9711, size10, 1000 stable pretraining ticks, then 3000 test ticks with explicit regrowth `.06→.055→.06`. Source hashes, per-seed trajectories, full final metrics and deterministic learned-weight transfer evaluations are in `NEXT_CREDIT_results.json`.

The fixed training objective is the earlier explicitly **engineered** `reserve_resource` reward, penalty `.3`, no teacher labels. Each neural test arm starts with identical trained weights, physical conditions and action RNG, and all select stochastic actions, so the one-factor learning-rule difference precedes any change in trajectories.

## Hypothesis 1 — Does clipping the energy feedback cause collapse?

Our hypothesis predicted that clipped realized rewards might hide raw energy deficits and harm online learning.

**Counterexample within our chosen setup:** The clipped-reward learner actually improved over the raw-reward learner in **12/12 matched seeds**: final mean energy `.04241` versus `.03695`, floor fraction **18.00%** versus **19.75%**, and raw late drift `−.001660` versus `−.001800`. It did not beat the frozen stochastic control (`.04888` energy, `16.92%` floor). The simple intuition “raw rewards must be superior because clipping erases gradients” was not supported here; baseline and action-policy interactions likely matter.

## Hypothesis 2 — Does eligibility-trace horizon alter delayed credit?

| Trace decay | Final mean energy | Cells near energy floor | Final 500-tick raw drift |
| --- | ---: | ---: | ---: |
| Short `.70` | **.01758** | **41.83%** | −.003583 |
| Baseline `.97` | .03695 | 19.75% | −.001800 |
| Long `.995` | **.21703** | **43.75%** | **−.005549** |

The short trace worsened energy and floor health, losing to baseline in all twelve matched seeds. The long trace substantially increased **average** energy in all twelve seeds, but also **more than doubled** the fraction of depleted cells. Many cells accumulated energy while many others remained at the energy floor. The long trace's strongly negative *raw* energy budget was hidden partly by floor clipping. This is not an unqualified success; it exposes an energy–equity tradeoff. Long-trace updated weights, deployed frozen and deterministically under a mild shift, retained `.41815` mean energy but left **40.67%** of cells depleted, compared with the original frozen weights `.21756` energy and **15.25%** depleted.

This does not establish a universal optimal credit horizon: `.70/.97/.995` were preselected contrasts in one simulator and reward objective.

## Hypothesis 3 — Does a faster moving reward baseline help changing conditions?

Faster baseline smoothing `.90` (compared with baseline `.995`) modestly improved online mean energy to `.04129` and reduced floor occupancy to `17.58%` (baseline `.03695`, `19.75%`). It won the energy comparison in all twelve matched seeds, but still underperformed the frozen stochastic policy (`.04888`, `16.92%`). The beneficial change is small and does not demonstrate robust adaptation.

## Strong controls and deterministic weight competence

| Controller at test tick3000 | Mean energy | Floor fraction |
| --- | ---: | ---: |
| Online raw reward | .03695 | 19.75% |
| Online clipped reward | .04241 | 18.00% |
| Online short trace | .01758 | 41.83% |
| Online long trace | .21703 | **43.75%** |
| Online fast baseline | .04129 | 17.58% |
| **Frozen stochastic trained neural controller** | .04888 | 16.92% |
| Fixed threshold `.50` | .04401 | 22.00% |
| Hand-designed **reverse rescue** | **.27885** | **8.83%** |

All arms shared the same unchanged energy/consumption/diffusion laws; the mild resource-regrowth change was explicit. The reverse-rescue controller uses exactly `R>.51` when energy is not low and `R>.535` when `E<.12`. It is **hand-coded**, not learned; among this tested set it exceeds every neural variant on both mean energy and floor fraction. This remains within a finite horizon and chosen environment.

The frozen deterministic diagnostic separately evaluates each arm's final theta on **the same fresh initial worlds** under stable and mild conditions (1500 ticks each), distinguishing learned-weight competence from ongoing stochastic deployment. The numerical results reveal that an apparent gain in average energy (long traces) can accompany an unacceptable increase in depleted cells. See complete source and row-level metrics rather than interpreting only the highest mean.

## Interpretation and confidence

1. The first conjecture was falsified in this setup: clipped rewards outperformed raw rewards locally, albeit weakly.
2. Trace length is consequential, but **higher energy does not imply a healthier population**. Long eligibility traces create a polarized state with many depleted cells.
3. Faster reward-baseline tracking helps slightly but does not solve online ecological control.
4. Strong manual welfare-sensitive controls remain superior on both reported axes under this regime. None of these results validates consciousness, biological evolution, or a general learning law.
5. Replication unit is **seed (n=12)**, not 100 interacting cells or 3000 ticks. All source, parameters and metrics are archived; independent audit should replay with untouched seeds and verify raw/floor accounting before any broader claims.

**Next pressure:** A genuinely multiobjective online learner should explicitly track all-cell depletion, raw resource budgets and long-horizon recovery, with stochastic policy updates decoupled from exploratory action risk. Designing such rewards is engineering, not automatic discovery of welfare.

**Artifacts:** `NEXT_CREDIT_PLAN.md`, `NEXT_CREDIT_garden.py`, `NEXT_CREDIT_probe.py`, `NEXT_CREDIT_results.json`, `NEXT_CREDIT_REPORT.md`. Quick smoke (`NEXT_CREDIT_smoke.json`) is non-independent and excluded from the substantive loop count. This study comprises three distinct causal hypothesis probes (clipping, trace, baseline), with several variants *inside* the trace probe.
