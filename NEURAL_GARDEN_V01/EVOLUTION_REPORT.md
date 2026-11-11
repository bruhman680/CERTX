# Experimental evolution extension — first pilot (not population-evolution evidence yet)

**Status:** Local exploratory prototype, tested on 20 fresh seeds per arm, 600 ticks, 10×10 grids. This work is independent of, and does not modify, Neural Garden v0.1–v0.3 or the matched 1,000-run sweep. Source: `EVOLUTION_garden.py`; test/runner: `EVOLUTION_pilot.py`; per-seed records and source digest: `EVOLUTION_pilot_results.json`.

## Mechanism and explicit intervention

- Each occupied cell owns separate recurrent-controller weights and a unique genome ID.
- A cell can die from low energy (≤.02) or a finite maximum lifespan (240 ticks).
- A living cell with energy >.62 can reproduce into one of its four empty neighboring grid sites, with probability .035 per tick when eligible.
- Child inherits all seven weight/bias tensors from parent, optionally with independent Gaussian mutation (`σ=.025` or `0`). The child has a unique ID, recorded parent ID, birth tick, location, generation and death tick.
- Parent pays **.24 energy**, newborn receives **.20**. The difference is reproduction overhead, and is not created from nowhere.
- Dead sites neither harvest nor pay metabolism. This changes the resource field relative to the *fixed-occupancy* v0.1 experiments. Do not compare energy directly across these different ecological worlds.
- In this extension there is **no gradient update**. Any possible adaptation would have to come from differential reproduction/survival of inherited controller weights; this has **not** yet been demonstrated.

## Smoke, replay, ancestry checks

PASS: seeded identical runs match full-state fingerprint after 48 ticks. PASS: saving/loading a trusted local checkpoint at tick 48 and continuing to tick 120 matches uninterrupted reference. PASS: offspring IDs uniquely identify parents, every parent ID precedes child ID, and `len(ancestry(uid)) == generation+1`. PASS: counts of founders plus recorded births equal total lineage entries.

These are software invariants, not evidence of a beneficial selection gradient. Future tests should explicitly test total energy accounting around reproduction and hold out evolved controllers on fresh environments.

## Pilot comparison (mean of 20 seeds, tick 600)

| Controller and inherited mutations | Living cells / 100 | Mean energy across all sites | Resource | Cumulative births | Max generation |
| --- | ---: | ---: | ---: | ---: | ---: |
| Neural weights, mutation σ=.025 | 45.75 | .2124 | .6427 | 155.35 | 6.00 |
| Neural weights, clonal σ=0 | 46.40 | .2192 | .6401 | 154.95 | 6.15 |
| Hand-coded resource threshold .55, genomes still mutate but **do not control actions** | **77.40** | **.3842** | .5734 | 151.75 | 8.00 |

The neural mutating condition did **not** outperform the clonal neural condition on these coarse measures. The rule-based controller supported a larger living population, although its inherited neural weights were behaviorally irrelevant. The third arm is an ecological positive control, **not a genetic selection experiment**. Small seed count, hand-picked world laws, and 600-step horizon limit any statistical inference.

## Audit questions before calling this evolution adaptive

1. **Phenotype link:** Does changing a weight causally change harvest decisions, lifetime reproduction and lineage persistence? Quantify genotype–phenotype mapping with controlled swaps.
2. **Selection pressure:** Does lineage survival or lifetime descendants predict heritable action timing, rather than initial resource luck or geographic position?
3. **Mutation counterfactual:** Compare σ=0, small σ and excessive σ on unseen seeds for far longer horizons, with multiple repeats and robust within-run diversity metrics.
4. **Genealogy:** Log allele/weight distributions, founder contributions, ancestor survival, and population bottlenecks. `max_generation` alone is not evidence of adaptive improvement.
5. **Energy accounting:** Reproduction redistributes energy; death removes stored energy, environmental harvest and regrowth are inputs. Distinguish changes due to altered occupancy/resource regime from genetic effects.
6. **Changed environment:** Test transfer after resource shocks only after the inherited phenotype shows a repeatable advantage. Keep any reset/selection intervention clearly labeled.

**Conclusion:** We now have an explicit, testable *evolution-capable mechanism* with actual inheritance and lineage tracking, but **no demonstrated adaptive evolution**. The negative comparison against clonal neural genomes is worth preserving. This is a separate exploratory direction, not a revision of previously completed results.
