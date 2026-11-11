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

## Verification and limitations

1. The world equations are preserved exactly in `NEXT_WELFARE_garden.py` and its `RuleGarden`; a changed regrowth coefficient is explicitly labeled in the changing test. No explicit teacher labels or hand-coded thresholds are used inside the neural learner, but neural resource dependence is initialized with a positive inductive bias.
2. Each cell is an interacting unit within a world. **Independent replication unit is a seed** (12 per heldout), not the 100 cells or 3000 ticks.
3. The four training objectives, welfare proxy, and penalties were not preregistered outside this experiment. Testing many values on development seeds creates selection bias; the two holdouts are from the same simulator family.
4. No claim of indefinite ecological equilibrium, real biological viability, ethical welfare, or general AI intelligence. Abrupt energy clipping can hide negative raw budgets; row-level energy-floor rates were retained.
5. These results illustrate why average energy and all-cell survival must be reported together. They also support a negative result: changing a reward objective does not automatically make online learning beneficial.

## Next justified orientation

Separate **policy updates** from **stochastic exploration** through a controlled action-mode schedule, then evaluate deterministically with identical weights, observations, and heldout time windows. Test low-energy welfare as a true multiobjective burden, not a single convenient scalar. Independent review should inspect exact laws and source provenance before claims are promoted.

**Artifacts:** `NEXT_WELFARE_garden.py`, `NEXT_WELFARE_study.py`, `NEXT_WELFARE_results.json`, `NEXT_WELFARE_stable.py`, `NEXT_WELFARE_stable_results.json`. Quick smoke is separately held in `NEXT_WELFARE_smoke.json` and is NOT counted as an independent loop.
