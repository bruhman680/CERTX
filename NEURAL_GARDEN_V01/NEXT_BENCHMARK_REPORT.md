# Frozen-design Garden benchmark — stable and changing worlds

**Status:** Executed complete 288-trajectory preregistered-*design* benchmark; the underlying six policies were selected before this benchmark through earlier exploration, so this is NOT a preregistered discovery of any policy. No policy was modified after observing these results. The frozen design lives in `NEXT_BENCHMARK_PLAN.md`, experiment code `NEXT_BENCHMARK_run.py`, full per-run evidence `NEXT_BENCHMARK_results.json`.

## Design, units and checks

- Six policy arms ×four explicitly labeled environments ×three grid sizes (8,12,16) ×four held-out test seeds = **288 distinct trajectories**, each 6,000 ticks, with nested checkpoints t1000, t3000 and t6000 (**864 observations**, NOT independent replications).
- Fresh test seeds 33000–33003 and disjoint teacher-free neural training seeds 25000–25003. Each matched arm began from exactly identical physical resource and energy arrays. Frozen deterministic neural policy used 1,200 earlier raw-reward training ticks, then **no test-time learning**.
- Original resource/energy equations were preserved except declared modifications: mild regrowth .06→.055 during test ticks501–1500, no diffusion throughout, or one exogenous resource×.70 shock after tick600.
- A one-step fixed .50 implementation check matched `ThresholdGarden`'s physical update within maximum 1.2×10⁻¹⁶ floating-point rounding error. The raw record carries source hashes, plan hash, platform, training-weight fingerprints, distinct IDs and all checkpoint metrics.

## Mean energy at tick 6000

| Policy (frozen design) | Stable | Mild regrowth dip | No diffusion | One resource shock |
| --- | ---: | ---: | ---: | ---: |
| Fixed .50 | **.6790** | .1283 | .4938 | .4539 |
| Fixed .51 | .6705 | .1416 | .4945 | .5069 |
| Earlier-harvest energy rescue (`E<.12` → threshold .485) | .6708 | **.0262** | .4945 | .5075 |
| Later-harvest reverse rescue (`E<.12` → threshold .535) | .6728 | **.3416** | .4945 | .5133 |
| Neighbor-gradient gate | **.6813** | .1543 | .4940 | **.5221** |
| Learned two-input energy policy, frozen deterministic | .5684 | .2259 | .4346 | .4598 |

These figures average the 12 size×seed pairs (four seeds per size). Size-specific results are archived; combining sizes does **not** yield 12 statistically independent replications of a fixed architecture because the same seed IDs recur across sizes. Each policy has different outcome distributions, and the exact ranking changes across regimes.

## Distribution matters (t6000 floor fraction)

| Policy | Stable | Mild regrowth | No diffusion | Shock |
| --- | ---: | ---: | ---: | ---: |
| Fixed .50 | 0% | 13.7% | 0% | 0% |
| Fixed .51 | 0% | 12.3% | 0% | 0% |
| Earlier rescue | 0% | **31.8%** | 0% | 0% |
| Reverse rescue | 0.4% | **8.8%** | 0% | 0.1% |
| Neighbor-gradient | 0% | 11.2% | 0% | 0% |
| Learned energy-aware policy | 2.2% | 14.1% | 3.3% | 0.9% |

The earlier-rescue policy previously looked impressive under stable long horizons, yet here it is **worst** under the specific mild regrowth dip. That is an important cross-regime falsification of any claim that urging depleted cells to harvest sooner is generally protective. The reverse rule is dramatically better on energy and floor fraction in this particular dip, but the reverse design is itself a prior, hand-tuned exploratory candidate and not proven globally optimal.

## Paired and temporal observations

- Under **mild regrowth**, reverse rescue minus earlier rescue mean energy was **+.31538**, positive for all 12 size×seed pairs. Learned-energy minus fixed .50 was **+.09766**, positive for all 12 pairs; this is consistent with useful trained state-dependence but not online learning during the dip. Against reverse rescue, learned-energy remains lower on the reported mean.
- Under **stable** laws, fixed .50 minus learned-energy mean energy was **+.11065** (12/12 pairs), a strong simple-rule negative control.
- After a one-time **resource shock**, neighbor-gradient minus fixed .50 mean energy was **+.06826** (12/12), but this says nothing about indefinite stability or more severe repeated shocks.
- At t1000 during the mild dip, all policies were already substantially depleted; early rescue .0182 mean energy with 33.3% floor while reverse rescue .0849 with 27.9% floor. At t3000 after recovery, the former reached only .0301 and the latter .2865. These histories illustrate regime dependence and path effects, not instantaneous causal rescue from one action.
- The stable learned policy itself declines from .6024 energy at t1000 to .5684 at t6000 and has 2.2% floor occupancy. Good transfer in one regime does not certify stable viability.

## Interpretation, in FRR terms

This controlled contact reveals **policy–environment interaction**: no universally best strategy appears among these six. A rule's response to energy scarcity can be beneficial or destructive depending on resource regeneration and spatial dynamics. State, history, and objective need to stay linked to the environment that gives them meaning.

The comparison also distinguishes *learned representation* from *online adaptation*. The teacher-free energy-aware network learned weights in separate normal worlds, then was frozen. Its mild-regime advantage over fixed .50 is **static transfer** of learned behavior, not measured continued learning through environmental change. The stronger reverse-rescue control shows it has not surpassed hand-designed alternatives in that regime.

**Next specific burden:** predeclare and test policies under a held-out family of *mild varying regrowth durations and magnitudes*, with exactly matched frozen/online policy action mode and an individual-survival objective. A high mean with many floor cells is not a healthy Garden. Extend to longer horizons and more independent seeds before inferring an attractor, universal crossover, or adaptive intelligence.
