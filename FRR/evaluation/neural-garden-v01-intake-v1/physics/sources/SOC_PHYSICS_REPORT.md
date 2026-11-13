# Action targeting, not merely action frequency: a matched-count physics probe

**Status:** 72 executed, matched-seed simulations under **unchanged original Garden world laws**. Script `SOC_PHYSICS_targeting.py`; complete per-seed outcomes, source hashes and paired contrasts `SOC_PHYSICS_targeting_results.json`. This investigation consists of **two conceptual research loops**, not 72 conceptual loops: (1) test whether resource/energy targeting matters beyond equal action counts; (2) compare energy-aware and neighbor-gradient decision rules under the same laws.

## Critical control

The energy-rescue rule normally harvests if resource exceeds `.51`, but permits harvest at `.485` if its energy is below `.12`. For each of **12 fresh seeds, 5800–5811**, run the rescue world 10,000 ticks, recording the **exact number of actions at every tick**. Then start another world from precisely the same resource/energy initialization and let it harvest *exactly that number* of cells on each tick, **but assign those actions to random positions**. This preserves the rescue world's action-count time series exactly while destroying resource/energy-targeting relationships. It is an explicitly externally driven counterfactual, not a learned or viable policy candidate.

We also compare uniform thresholds `.485`, `.50`, `.51`, plus the neighbor-gradient rule `threshold=.51+.5*(mean_neighbor_resource-local_resource)`. All arms share the same energy equation, resource regrowth/consumption/diffusion, seeds, initial energy/resource, and horizon. The original fixed-threshold simulator's 100-step transitions matched the implemented equations within floating-point tolerance `1e−12`.

## Measured t10,000 results (12 paired seeds)

| Harvest policy | Mean final energy | Floor fraction | Mean harvest fraction in final 2,500 ticks | Mean resource at harvest* | Resource–action covariance |
| --- | ---: | ---: | ---: | ---: | ---: |
| Energy-aware rescue | **.68203** | **0%** | .333354 | .516202 | +.010678 |
| Fixed .51 | .67421 | .488% | .333352 | .516195 | +.010646 |
| Fixed .50 | .67758 | .55% | .333351 | .516197 | +.010695 |
| Fixed .485 | .47435 | 0% | .343630 | .507901 | +.008597 |
| Neighbor gradient | **.69040** | .488% | .333360 | .516227 | +.010677 |
| **Same harvest count, random locations** | **.11490** | **8.43%** | **.333354** | **.500200** | **~+.000011** |

*Mean resource at harvest is the pooled ratio `sum(resource × action) / sum(action)` over the final 2,500 ticks, avoiding bias from ticks with no harvests.

For rescue minus fixed `.51`, paired mean energy difference is **+.00782**, positive on **12/12** seeds; its small size relative to between-policy ecological differences should not be exaggerated. Compared with neighbor-gradient, rescue has **−.00838** mean difference; the neighbor rule wins on 10/12 seeds. Compared with the same-count random-target counterfactual, rescue is **+.56713** better, positive on **all 12 seeds**.

The critical causal distinction is **frequency versus placement/timing**. Rescue and shuffled worlds harvest *exactly the same number of cells each tick*, yet their ecological performance differs dramatically. The shuffled policy's resource–action covariance is essentially zero; rescue preferentially harvests locally abundant resources and retains much more energy. The current per-cell neural baseline has not demonstrated comparable targeting.

## Exact accounting mechanism

For original world resource `R` and action indicator `A`, diffusion averages out over the toroidal grid, giving

`mean(ΔR) = .06 (1 - mean(R)) - .18 mean(R A)`

and the raw **pre-clipping** energy change obeys

`mean(ΔE_raw) = .25 mean(R A) - .063 mean(A) - .022`.

Also `mean(R A) = mean(R) mean(A) + Cov(R,A)`. Equal action rates do **not** imply equal resource yield because `Cov(R,A)` can differ. The empirical rescue–shuffle gap reflects this distinction. It does not establish a universal theorem that a particular threshold, policy, or neuron is optimal.

The neighbor-gradient rule slightly improves the resource yield **per harvest** under original diffusion. That tiny yield difference could accumulate over thousands of ticks; this is a plausible local mechanism, not demonstrated autonomous inference or coordination among intelligent agents. The energy-rescue rule's additional benefit over fixed `.51` also concerns its near-zero floor occupancy. Further experiments should decompose the rare energy-triggered override decisions rather than simply treating it as a better global threshold.

## Limitations and next question

- All rules were selected **posthoc** from earlier investigations. The 12 seeds are fresh from the same toy generator, not external replication; the simulation horizon is finite.
- The same-count shuffled arm is an **intentionally artificial negative control**, not a viable learnable strategy. Because its world trajectory diverges, resource distribution and future opportunities also diverge; the count match isolates action quantity, but the long-run difference includes feedback effects.
- Neither the rescue nor neighbor rule was learned autonomously. They are hand-designed conditional policies with access to local state.
- Energy clipping can conceal losses; the data archive includes raw pre-clipping drift, floor/ceiling occupancy and energy–action covariance. Late average raw drift is small, not a proof of indefinite sustainability.

**Next pressure:** identify what temporal/neighbor-state information a learned controller needs to reproduce resource-conditioned action placement under original and shifting resource laws, and evaluate it against matched-count and fixed-rule controls with identical environmental access.
