# Dual memory: protected neural policies and validation-gated consolidation

**Status:** One substantive completed research loop (hypothesis → predeclared protocol → matched simulated controls → held-out judgment); six independent training cohorts, twelve independent held-out synthetic worlds per regime. Full individual rows and exact source fingerprint: `MEMORY2_results.json`. Protocol: `MEMORY2_PLAN.md`. No edits to canonical Living Garden.

## What the predeclared trial showed

The mutable policy learned during 1,600 further ticks; the protected bank retained its original weights. Four candidate snapshots were validated independently, and a gate admitted only a candidate better than the protected policy by >.005 on validation reward. The selected checkpoint was the 800-tick snapshot in four of six training cohorts; two remained protected.

| Deployment regime | Protected score | Blind latest score | Validation-selected score | Hindsight oracle score |
| --- | ---: | ---: | ---: | ---: |
| Stable regrowth | .66282 | .64951 | **.66953** | .68081 |
| Mild changed regrowth | .15080 | .03486 | **.19214** | .19277 |

Scores are `final mean energy - .5 * fraction with energy <=.01`, averaged across 12 independently seeded deployment worlds (two for each of six training cohorts). The hindsight oracle chooses on held-out scores and is **not** a fair deployable comparator. It bounds the best option among snapshots after outcomes are known.

Average final mean energies: stable protected .67064, blind latest .66123, selected .68450; mild protected .22306, latest .14619, selected .26506. Stable floors were protected 1.56%, latest 2.34%, selected **2.99%**; mild floors protected 14.45%, latest 22.27%, selected 14.58%. Thus better average energy does **not** imply uniformly healthier cells. The selected policy improves the combined score but worsens stable floor and does not clearly improve mild floor.

## Interpretation

This is encouraging for a **protected memory bank plus external validation-based consolidation**, not a demonstration that neural cells autonomously know when to learn. A direct blind replacement with the latest trained weights is worse, especially across changing resource laws. An engineered selector can preserve and sometimes improve average policy competence at these horizons.

## Pressures / unresolved

1. Gate requires running multiple *off-world validation worlds* and is expensive designer infrastructure. Test cheaper or local per-cell critics without claiming equivalence.
2. Six training cohorts are small; request an independently frozen replication with wholly new training and validation seeds before treating score gain as robust.
3. Selection objective tolerates worsened depleted-cell fraction. Predeclare safety-constrained validation and inspect Pareto tradeoff.
4. These are independently initialized evaluations of a frozen policy bank, not uninterrupted training/deployment in a common world; checkpointability and migration to canonical Living Garden remain separate open questions.
