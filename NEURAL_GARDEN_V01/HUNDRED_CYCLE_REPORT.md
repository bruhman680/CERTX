# Neural Garden — exactly 100 independent simulation runs

**Status:** Executed bounded synthetic factorial sweep (2026-11-11 UTC).  
**Code:** [`hundred_cycle_sweep.py`](hundred_cycle_sweep.py)  
**Raw:** [`hundred_cycle_results.json`](hundred_cycle_results.json) — 100 individual run records, full metrics at ticks 0/50/100/150/200, unique IDs, seeds, configuration hashes, model-state fingerprints, and SHA-256 source hashes.

This is a batch of **100 declared simulation experiments**, not 100 reasoning cycles, 100 generations of biological evolution, or 100 independent scientific discoveries. All runs use fixed grid 16×16 (256 distinct neural controllers), 200 ticks, and seeds 100–119. Five arms each receive twenty matched seeds.

## Fixed arms and conditions

| Arm | Learning? | World laws | Controller/reward |
| --- | --- | --- | --- |
| v01_learning | Yes | Original resource/energy laws | Original immediate energy reward |
| v01_frozen | No | Original laws | Same initialized neural weights, never updated |
| v02_stewardship_learning | Yes | **Same original laws** | Reward includes explicit local resource preservation term 0.65 × resource change |
| v03_viable_learning | Yes | **Changed law**: metabolism .03→.02 | v0.2 stewardship learning |
| v03_viable_frozen | No | Same changed v0.3 laws | Frozen v0.3 model |

The v0.3 world-law change is a deliberate intervention. It should never be interpreted as an emergent neural improvement. The v0.2 reward change is also designer-supplied, not spontaneously learned stewardship.

## Results at tick 200 (means across 20 runs per arm)

| Arm | Mean energy | Mean resource | Harvest rate | On-policy prediction MSE | Cells energy ≤0.01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original, learning | **0.01730** | 0.36457 | 58.34% | 0.00406 | 51.15% |
| Original, frozen | 0.06120 | — | 49.88% | 0.01579 | 22.5% |
| Stewardship reward, original world | **0.08025** | — | 47.48% | 0.00390 | 16.2% |
| Revised viable world, learning | **0.98263** | — | 42.64% | 0.00392 | 0% |
| Revised viable world, frozen | 0.98682 | — | 50.00% | 0.01703 | 0% |

Exact values, min/max and across-seed SD are in the JSON. Differences are measured at the final tick, with trajectories saved for earlier ticks. The v0.3 energy values are **near the upper clipping ceiling of 1.0**. This is not evidence of ongoing growth beyond capacity, and learned v0.3 mean energy was slightly lower than frozen v0.3 mean energy (paired difference −0.00419).

Paired mean v0.2 minus v0.1 learned energy is +0.06294; the reward modification reduces harvest frequency by 10.86 percentage points. This is a local outcome on the chosen world, and energy remains very low at tick 200. The measured v0.1 learned/frozen MSE difference is on-policy and must not be promoted to general forecasting competence; prior standardized off-policy tests gave conflicting results.

## Mean-field viability bound, and its limitation

For a spatially homogeneous constant harvest rate `p`, the original world has approximate steady resource `r*=.06/(.06+.18p)` and unclipped mean energy drift

`g(p)=.25*r* p - .03 - .055*p + .008*(1-p)`.

On `0<=p<=1`, its maximum is about **−0.00133** at `p≈0.331`. Thus no *homogeneous constant-rate* policy can maintain positive mean energy forever under that approximation. This is **not** an impossibility theorem for state-dependent spatial or temporal policies. Energy clipping at zero can also make measured post-collapse actual_delta deceptively near zero despite a negative pre-clipping budget. The sweep explicitly records the fraction of cells near the energy floor.

## Additional exploratory threshold-policy contact (outside 100 runs)

An independent, **posthoc-inspired** control uses the original world laws and a simple deterministic decision: harvest only if a cell's local resource exceeds 0.55. The threshold came from earlier results and was *not* preregistered. It was held fixed on **20 fresh seeds 600–619**, at 200 and 600 ticks. Script: [`heuristic_counterfactual.py`](heuristic_counterfactual.py); data: [`heuristic_counterfactual.json`](heuristic_counterfactual.json).

| Tick | Mean energy | Mean resource | Harvest rate at tick | Energy-floor fraction | Raw unclipped mean energy change |
| --- | ---: | ---: | ---: | ---: | ---: |
| 200 | 0.54556 | 0.52084 | 34.96% | 0 | +0.00488 |
| 600 | **0.48442** | 0.52051 | 32.46% | 0 | +0.00305 |

This *state-conditional* policy can select resource-rich moments and outperform the neural reward learners without changing the world's laws. It does not contradict the homogeneous constant-rate mean-field calculation, because action probability is correlated with resource availability. This is a powerful baseline and a reason to avoid interpreting sophisticated neural architecture as necessary for ecological viability. The 20 heuristic tests are **not counted** in the fixed 100-run sweep and are exploratory rather than confirmation of a frozen theory.

## Critical interpretation

1. Individual neural weight updates and improved on-policy prediction are reproducible, but **overall ecological viability does not follow**.
2. Designer reward shaping improves some energy metrics on the original laws but does not make the world self-sustaining by itself in the evaluated horizon.
3. A small change to world metabolism can create a positive viable region, yet both learned and frozen models benefit; this is not evidence that the neural controllers discovered resilience.
4. An elementary local threshold policy is a stringent comparator and shows that useful conditional behavior need not require learning.
5. These are fixed-grid cells, without births, deaths, mutation, heritable selection or natural-language reasoning. Calling the run “evolution” in a population-genetic sense would be premature.
6. The 20 matched seeds are not independent scientific replications of a natural phenomenon. Parameter settings and some baseline ideas arose through prior exploratory observation, and confidence claims require untouched confirmatory designs.

## Next discrimination

Keep v0.1 intact. Compare a fixed threshold policy with an action-conditioned neural controller on held-out seasonal/perturbed resource fields, matched access and compute. Test whether learning achieves a robust advantage across *unseen conditions* and resource costs, not just better behavior in the generator it already experienced. Then add reproduction and inherited weight mutation as a separate and independently controlled axis.
