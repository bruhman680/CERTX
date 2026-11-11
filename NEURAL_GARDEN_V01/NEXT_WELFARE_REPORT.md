# Learning a balance: three controlled welfare-objective probes

**Status:** Executed on synthetic neural-cell worlds, exploratory evidence. No claim that a value function equates to human welfare. All source code, individual seed outcomes, checkpoints, and source hashes are preserved in the accompanying files. Existing Garden physics was not edited.

## Hypothesis 1 — Can a different local learning objective preserve energy and prevent depletion?

We tested four teacher-free policy-gradient rewards with the same per-cell resource/energy logistic architecture and unchanged Garden environmental laws:

- `raw`: exact pre-clipping individual energy change.
- `reserve`: raw less an explicit penalty for ending below energy .18.
- `resource`: raw plus .3 times local resource change, an explicit ecological stewardship preference.
- `reserve_resource`: both penalties/rewards combined.

All coefficients and objective choices are **designer supplied**; success would show an engineered training improvement, not spontaneous moral reasoning. Four development seeds 9100–9103, grid8, 800 training and 1200 test ticks. The declared development score was `mean_energy − .5 × fraction_near_energy_floor`. `resource` ranked best and was frozen before the new test seeds. Its selection may be overfit to the small development set; no optimum is claimed.

## Hypothesis 2 — Does the selected reward produce useful ONLINE adaptation during mild changing conditions?

Twelve new matched test seeds 9200–9211, size10, 1000 pretraining ticks, then 3000 test ticks. **One explicit world-law change**: regrowth .06 for first 1000, .055 for middle 1000, return to .06 for last 1000. All other original laws remain identical. Same trained threshold weights, matched RNG states for online/frozen stochastic controls; actions diverge if policies update. Strong manual baselines use *exact* definitions:

- fixed `.50` threshold;
- original rescue `harvest iff R>.51 OR (E<.12 AND R>.485)`;
- reversed low-energy gate `harvest iff R>.51 if E>=.12, else R>.535`;
- neighbor-gradient `harvest iff R>.51+.5*(neighbor_resource−R)`.

| Arm | Final mean energy | Cells at energy floor | Welfare proxy `energy−.5 floor` |
| --- | ---: | ---: | ---: |
| Resource-shaped **online stochastic** | .04379 | 14.08% | −.02662 |
| Same resource-shaped pretrained, **frozen stochastic** | .05480 | 9.92% | +.00522 |
| Same resource-shaped pretrained, **frozen deterministic** | .09029 | 25.25% | −.03596 |
| Raw reward online stochastic | .04079 | 16.25% | −.04046 |
| Raw reward frozen stochastic | .05403 | 9.75% | +.00528 |
| Fixed .50 | .04499 | 19.42% | −.05209 |
| Hand-designed rescue | .03017 | 22.83% | −.08400 |
| Hand-designed **reverse rescue** | **.28482** | 9.75% | **+.23607** |
| Neighbor gradient | .05257 | 12.58% | −.01035 |

The selected objective slightly improves relative to raw online but **does not improve relative to its own frozen stochastic control**. This directly challenges the hoped-for online learning advantage under this mild regime. The hand-designed reverse low-energy gate is much stronger in this particular measured setting. Because the reverse rule was known from earlier explorations and this is the same simulator family, this is not independent confirmation of an optimum. The numerical value of the welfare proxy reflects an arbitrary designer choice; its ranking is not a biological fitness theorem.

## Hypothesis 3 — Is the failure caused by unstable-world selection alone?

On twelve further **fresh** stable-world seeds 9400–9411, grid10, 3000 ticks with *no world-law change*, the pretrained resource-shaped online stochastic policy still had low mean energy `.04262` and floor `16.0%`, versus its frozen stochastic clone energy `.05394`, floor `11.75%`. The **frozen deterministic** version scored energy `.58618`, floor `.25%`; fixed .50 had `.64490`, floor `0%`, and the manual `.51`-based rescue/reverse policy each `.64634`, floor `0%` (their low-energy rule seldom activated in this healthy stable environment). Thus stochastic deployment and ongoing updates remain strongly confounded; the selected online policy is not a viable long-horizon solution under either regime.

## Hypothesis 4 — Does reward engineering improve a policy under IDENTICAL deterministic action selection?

The earlier online-vs-deterministic comparisons confound stochastic exploration with weight updates. To isolate the *learned policy quality*, we trained each of the four candidate reward objectives for 1,000 ticks with exactly matched training seeds, then **froze every network and deployed deterministically** for 3,000 ticks. We did not reselect the development winner: all four reward objectives were evaluated on twelve new seeds 9500–9511, grid10, both unchanged-world and mild-regrowth worlds.

| Training reward (frozen deterministic test) | Stable energy / floor | Mild-regrowth energy / floor |
| --- | ---: | ---: |
| Raw immediate energy | .55784 / .58% | .10694 / 23.50% |
| **Explicit low-energy reserve shaping** | **.71390 / 2.33%** | .23723 / 16.58% |
| Resource preservation shaping | .56514 / .58% | .09439 / 23.08% |
| Combined reserve + resource shaping | .70950 / 2.33% | **.26218 / 16.75%** |
| Strong fixed .50 control | .65144 / 0% | .04511 / 18.92% |
| Hand-designed neighbor-gradient control | .65930 / 0% | .05200 / 12.33% |
| Hand-designed **reverse rescue** control | .65226 / 0% | **.27764 / 10.75%** |

These later data are in `NEXT_WELFARE_deterministic.py` / `_results.json` and exact same-seed manual controls `NEXT_WELFARE_rule_controls.py` / `_results.json`. Stable-world reserve-shaped learner beat the neighbor-gradient fixed rule in **10/12** matched seeds (mean +.05460 energy) but had *more depleted cells* (2.33% vs 0%). Under mild changing conditions, combined shaping recovered much more energy than fixed .50, but the stronger reverse-rescue manual rule still exceeded it in **8/12** seeds and left fewer cells depleted. The comparison is exploratory and the objective family was selected by designers; do not infer superior autonomous intelligence or general wellness.

**Crucial revision:** The development-selected `resource` objective was not the best for frozen deterministic deployment. In the new independent deterministic comparison, low-energy reserve shaping was superior for stable energy, while combined shaping performed better among the neural objectives under mild regrowth change. This exposes sensitivity to *which burden and action mode* is evaluated. The selected objective's earlier online failure remains intact, not erased by the separate successful frozen deployment.

### Limits particular to this fourth pass

Fixed deterministic deployment is **not online adaptation**. Reward shaping explicitly tells the learner which energy conditions we prefer; it can legitimately improve results without the system discovering the welfare criterion. Stable mean energy alone conceals a small but material number of depleted cells relative to fixed rules; a scalar `energy−.5 floor` is an *arbitrary* designer tradeoff. Comparators and objectives share the same simulator family, and four objectives plus four controls introduce posthoc selection opportunities.

## Hypothesis 5 — Does scalar welfare hide distinct defensible choices?

Using **the same previously measured** deterministic data (no new simulation seeds), we removed the arbitrary `.5` coefficient and calculated the two-dimensional Pareto frontier over: (i) **maximize mean energy**, (ii) **minimize fraction near energy floor**. The synthetic script `NEXT_WELFARE_pareto.py` and derived data `_pareto_results.json` preserve every dominance comparison.

- **Stable original laws:** the two nondominated aggregate choices were **neural reserve-shaped** (higher mean energy .7139, but 2.33% depleted) and **manual neighbor-gradient** (lower mean energy .6593, but 0% depleted). Neither dominates the other. Thus selecting a 'best' strategy requires a declared burden or safety constraint.
- **Mild regrowth shift:** the **manual reverse-rescue** rule (mean .2776, 10.75% depleted) dominated all other evaluated policy aggregates on both burden axes. The tested neural learner variants do not currently occupy the frontier in this regime.

This is an aggregate *descriptive* Pareto comparison, not proof of dominance for every seed, cell, or untested policy. It is a distinct conceptual clarification of why the one-number `energy−.5 floor` ranking is insufficient. It motivates explicit multiobjective design before further neural reward tuning.

## Verification and limitations (shared)

1. The world equations are preserved exactly in `NEXT_WELFARE_garden.py` and its `RuleGarden`; a changed regrowth coefficient is explicitly labeled in the changing test. No explicit teacher labels or hand-coded thresholds are used inside the neural learner, but neural resource dependence is initialized with a positive inductive bias.
   An independent three-seed ×200-tick numerical identity check against existing `ThresholdGarden(threshold=.50)` passed with **bit-identical resource and energy arrays** for the local `RuleGarden(fixed50)` comparator.
2. Each cell is an interacting unit within a world. **Independent replication unit is a seed** (12 per heldout), not the 100 cells or 3000 ticks.
3. The four training objectives, welfare proxy, and penalties were not preregistered outside this experiment. Testing many values on development seeds creates selection bias; the two holdouts are from the same simulator family.
4. No claim of indefinite ecological equilibrium, real biological viability, ethical welfare, or general AI intelligence. Abrupt energy clipping can hide negative raw budgets; row-level energy-floor rates were retained.
5. These results illustrate why average energy and all-cell survival must be reported together. They also support a negative result: changing a reward objective does not automatically make online learning beneficial.

## Next justified orientation

Separate **policy updates** from **stochastic exploration** through a controlled action-mode schedule, then evaluate deterministically with identical weights, observations, and heldout time windows. Test low-energy welfare as a true multiobjective burden, not a single convenient scalar. Independent review should inspect exact laws and source provenance before claims are promoted.

**Artifacts:** `NEXT_WELFARE_garden.py`, `NEXT_WELFARE_study.py`, `NEXT_WELFARE_results.json`, `NEXT_WELFARE_stable.py`, `NEXT_WELFARE_stable_results.json`, `NEXT_WELFARE_deterministic.py`, `NEXT_WELFARE_deterministic_results.json`, `NEXT_WELFARE_rule_controls.py`, `NEXT_WELFARE_rule_controls_results.json`, `NEXT_WELFARE_pareto.py`, `NEXT_WELFARE_pareto_results.json`. Quick smoke is separately held in `NEXT_WELFARE_smoke.json` and is NOT counted as an independent loop.
