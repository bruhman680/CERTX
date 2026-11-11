# Environmental physics research society — five distinct probes

**Status:** Executed five substantive conceptual research loops with **152 matched synthetic simulation records**, eight fresh seed worlds 9300–9307, 16×16 cells, 8,000 ticks each and final-1,500-tick measurements. Code: `NEXT_ECO_probe.py`; full per-run data, exact configurations, original-source hashes, versions and paired contrasts: `NEXT_ECO_results.json`.

This is an *independent exploratory mechanism investigation*, not a discovery of intelligent behavior. All successful decision rules here are hand-coded. Four studies use **unchanged original v0.1 world physics**. Only the explicitly labeled diffusion ablation changes the world equation. Full-state neural learning is disabled; the experimental policies replace action selection. The original living-world checkpoint is untouched.

## Analytical anchor

For resource `R∈[0,1]`, harvest action `A∈{0,1}`, baseline regrowth `α=.06`, consumption `β=.18`, diffusion `κ=.08` and no boundary clipping, the global mean update satisfies

`⟨ΔR⟩ = α(1−⟨R⟩) − β⟨RA⟩`.

Diffusion redistributes resources locally and cancels in its **global** mean. The raw, *pre-clipping* energy update is exactly

`⟨ΔE_raw⟩ = .25⟨RA⟩ − .063⟨A⟩ − .022`

`             = .25(⟨R⟩⟨A⟩+Cov(R,A)) − .063⟨A⟩ − .022`.

These are bookkeeping identities for the specified simulator, not conservation laws about organisms. Clipping makes realized energy different at the floor and ceiling. Positive instantaneous raw drift is not indefinite viability.

## Loop 1 — Match harvesting *quantity*, change the targets

We first replay the rescue policy to obtain an exact number `n_t` of harvesting cells **at each tick**. Three distinct policies then harvest exactly `n_t` cells in their own simulated worlds, selecting them using highest current resources, lowest current resources, or uniformly random positions. Thus **all four policies have precisely matched action counts every tick**. Count targets are externally supplied by the rescue reference and are not independently learnable behaviors.

| Action placement | Final mean energy | Cells at energy floor | Tail Cov(resource, action) | Mean resource per harvest |
| --- | ---: | ---: | ---: | ---: |
| Resource/energy rescue | **.6794** | 0.0% | +.010679 | .51618 |
| Current top-resource cells | .6792 | 0.0% | +.010679 | .51618 |
| Random cells, same counts | .1164 | 7.8% | +.000032 | — |
| Lowest-resource cells, same counts | .1444 | 85.0% | −.108176 | .33786 |

The energy-aware rescue and top-resource rules are practically tied under these conditions. Both beat the random and bottom-targeted controls in **8/8 paired seeds**. This isolates **where** actions occur rather than how many occur. The low-target strategy has high mean energy in a minority of cells while 85% occupy the floor: mean energy alone is misleading.

## Loop 2 — Does spatial diffusion help the targeted regime?

This is a **changed-physics counterfactual**, comparing normal κ=.08 against κ=0 for the same resource-aware and top-resource action policies.

| Policy | Diffusion .08 energy | No-diffusion energy | Tail raw drift with diffusion | Without diffusion |
| --- | ---: | ---: | ---: | ---: |
| Rescue | .6794 | .4622 | +.0000152 | −.0000181 |
| Top-resource count-matched | .6792 | .4648 | +.0000151 | −.0000183 |

Normal diffusion wins all 8 matched seed comparisons. The marginal raw budget changes sign; this strongly suggests spatial coupling affects the timing-dependent yield, but it does *not* show a globally stable world, nor can the across-world difference be attributed to neural cognition.

## Loop 3 — Delay the resource observation

The rescue rule was made to use its local resource value from **one or two ticks ago**, while its energy observation remained current. The action rates were allowed to change, so this study initially tests the *combined* effect of sensing delay, altered harvest frequency, and altered targeting—not a clean timing-only intervention.

| Resource observation | Final energy | Tail harvest rate | Resource per harvest | Tail raw drift |
| --- | ---: | ---: | ---: | ---: |
| Current | **.6794** | .3333 | .51618 | +.0000152 |
| One tick old | .0442 | .3636 | .48868 | −.0004833 |
| Two ticks old | .0529 | .3750 | .47643 | −.0009601 |

The delayed observations do badly in 8/8 paired seeds. This motivates a stronger control rather than claiming delay alone is causal.

## Loop 4 — Match *both* action count and stale targeting

Fix the `n_t` action count at each tick to the original rescue trajectory, then select the `n_t` top cells by their **current** resources, previous-tick resources, or resources from two ticks ago. This preserves the reference action count exactly for all three policies, making a sharper observation-age contrast. The external count sequence remains an artificial experimental control.

| Ranking observation | Final energy | Cells at floor | Tail Cov(resource, action) | Resource per harvest |
| --- | ---: | ---: | ---: | ---: |
| Current resource | **.6792** | 0.0% | +.010679 | .51618 |
| One tick old | .0453 | 11.7% | +.007975 | .51211 |
| Two ticks old | .0678 | 10.0% | +.003455 | .50539 |

All policies harvest the **same number of cells at each tick**; stale targeting loses across 8/8 seeds. Even the small change in resource captured per action crosses the narrow energy-balance boundary, with tail drift becoming negative. This directly demonstrates that temporal alignment of observations with actions matters in the toy Garden.

## Loop 5 — Collective mean versus the worst-off cells

All four policies use unchanged world physics, with no neural learning. An energy-aware rescue harvests at `R>.51`, but allows `R>.485` when `E<.12`. A reverse rescue instead requires `R>.535` when low on energy; a neighbor-gradient rule adjusts the local threshold using neighboring resource levels.

| Policy | Final mean energy | Cells near floor | Final poorest-decile energy |
| --- | ---: | ---: | ---: |
| Energy rescue | .6794 | **0.0%** | **.1969** |
| Fixed .50 | .6824 | **0.0%** | .1815 |
| Reverse rescue | .6872 | 0.63% | .1763 |
| Neighbor gradient | **.6942** | 0.05% | .1789 |

Neighbor gradient wins mean energy in this sample, but rescue protects the bottom-decile more. This is a **multi-objective tradeoff**, not an ordering of uniquely correct policies. In particular, optimizing average energy can sacrifice some lower-tail welfare.

## Confidence / falsification summary

1. **Strong within-model result:** Action placement matters at exactly matched per-tick harvest counts, and stale local observations lose at identical counts. Eight paired synthetic seeds, original laws.
2. **Mechanistic consistency:** Resource–action covariance and resource yield per harvest track the energy-budget differences. A near-neutral balance can tip with a small yield change.
3. **Spatial physics matters:** Removing diffusion changes the outcome, but this is explicitly a *different world* and does not prove universal viability.
4. **No single welfare optimum:** High mean energy, floor occupancy, lower-tail energy, and recovery after shock should be scored separately. Policy ranking changes with objective.
5. **Not established:** Autonomous learning, open-ended evolution, indefinite sustainability, environmental memory as cognition, or generality outside the chosen simulator.

**Next strongest pressure:** Use predeclared held-out world-law shifts and a genuinely learning two-input neural policy with *controlled action frequency* and *matched observation age*. Compare its worst-decile welfare and raw energy budgets against fixed, rescue and neighbor-gradient controls. Avoid tuning on the final holdout.
