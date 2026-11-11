# One Living Garden — continuity, intervention timing and memory

**Status:** Four distinct executed research loops from the *unchanged canonical Neural Garden tick-100 checkpoint*, each with an explicit hypothesis, probe, measured result and next pressure. Source/results in `NEXT_LIVING_*`. The canonical full fingerprint was verified stable before and after all exact-state forks. No baseline `garden.py` physics was modified.

This is a laboratory on the **same history and its matched counterfactuals**, not evidence of independent real-world replication. Fresh world seeds were added for relevant checks. Handwritten controller changes, energy injections and resource shocks are *interventions*, not learning or emergence.

## Loop A — Is it too late to change behavior after collapse begins?

Probe: 11 explicit policy/schedule forks from one canonical tick100 checkpoint to tick10,000 (`NEXT_LIVING_switch_probe.py`, `_results.json`), including fixed .50, hand-designed energy-aware rescue, reverse rescue, delayed switching, restored neural operation, shock and no-shock. All conserve original within-tick world laws. At t10,000:

| Historical policy path | Mean energy | Cells near floor |
| --- | ---: | ---: |
| Original neural learning throughout | .00019 | 99.61% |
| Fixed .50 from tick101 | .36523 | 1.95% |
| Energy-aware rescue from tick101 | .41859 | .39% |
| Reverse rescue from tick101 | **.60395** | 8.98% |
| Original neural to tick500, then rescue | .01785 | 50% |
| Original neural to tick1000, then rescue | .03985 | 0% |
| Rescue to tick5000, then original neural restored | .00114 | 95.70% |

The surprising nonmonotonic late-switch floor result (500 vs1000) should NOT be interpreted as a general monotone timing law; it is one historical state, and floor clamping can obscure raw budget. Reverse rescue raises mean energy but depletes more cells, confirming a welfare tradeoff. Crucially, **rescue to tick5000 then original neural restoration restarts a stale learner**: while the handwritten policy controlled actions, the recurrent hidden vector and neural weights were *not* advanced or trained. Its subsequent collapse tests restoring this dormant controller, not uninterrupted neural plasticity or continuous updating through the rescue period.

Two resource shocks at ticks5,000 and7,000 (resource×.7) left fixed .50 energy .0992, rescue-from-start .1764, and fixed-until-first-shock-then-rescue .1618 at tick10,000. The latter is a policy handoff after a shock, not spontaneous adaptation.

**Next pressure:** Replicate intervention-timing trends on independent initial histories.

## Loop B — Does early versus late intervention generalize across worlds?

Probe: 12 disjoint fresh seeds9000–9011, each initialized for 100 ticks under the original neural learner, then four paired intervention schedules to tick5,000 (`NEXT_LIVING_validation.py`, `_results.json`, size12). Results:

| Schedule | Mean energy | Fraction at floor |
| --- | ---: | ---: |
| Fixed .50 from tick101 | .28826 | 6.54% |
| Energy-aware rescue from tick101 | .30078 | **0%** |
| Reverse rescue from tick101 | **.64750** | 4.28% |
| Original neural until tick500, then rescue | .02562 | 26.74% |

Rescue beats fixed .50 on all 12 seeds by mean+.01252 but no claim of unique optimum. Reverse rescue yields higher mean energy than both but nonzero floor. Delaying a behavior change until the early neural learning ecology has depleted its reserves gives substantially worse outcomes on all 12 seeds. This is a delayed-intervention result for chosen model coefficients, not a permanent irreversibility theorem.

**Next pressure:** Distinguish resource scarcity from depleted energy itself as the obstacle to delayed rescue.

## Loop C — Can one-time resource or energy repair reverse a bad starting state?

Probe: 12 fresh seeds9100–9111 plus exact canonical world, each left under original neural learning until tick500 and then switched to energy-aware rescue (`NEXT_LIVING_repair_probe.py`, `_results.json`). A named one-time intervention at the switch does one of: none; resource multiplier×2; all cells energy raised to at least .3; both. All subsequent steps use unchanged original physics and same rescue action rule.

| Late rescue intervention | Mean energy t5,000 | Floor fraction |
| --- | ---: | ---: |
| No external repair | .02469 | 29.17% |
| Resource only | .26914 | .17% |
| Energy only | .28453 | .17% |
| Both | **.53870** | **0%** |

The two external injections make a large difference, and their cross-term is small: average combined interaction relative to simple additivity is ~+.00973 mean energy (range −.01978 to+.04116 across seeds). Thus post-collapse states can be rehabilitated by *external* changes without changing physics, but this says nothing about self-repair learned from experience. Replenishing the soil or replenishing the cell changes its reachable future.

**Next pressure:** Test whether existing neural weights/recurrent history are themselves useful when returning to neural action control.

## Loop D — Does recurrent-state continuity save the old policy after a healthy hiatus?

Probe: 12 fresh seeds9200–9211, start from tick100 learner state, use rescue policy through tick2,500, then either keep rescue, restore the original neural policy with the dormant recurrent hidden vector, or restore it with the hidden vector zeroed (`NEXT_LIVING_memory_probe.py`, `_results.json`). All original weights remain as they were; they do *not* train during rescue. At tick5,000:

| Controller route | Mean energy | Fraction near floor |
| --- | ---: | ---: |
| Keep rescue policy | **.30110** | **0%** |
| Restore neural policy, stale hidden state | .002053 | 92.01% |
| Restore neural policy, reset hidden state | .002066 | 91.96% |

The mean stale-hidden minus reset-hidden energy difference is about −.0000126. That tiny contrast is not evidence that recurrent memory is useless generally. This probe shows the **original harmful action weights dominate**; neither retaining nor resetting the stale recurrent state repairs them. It does not test a genuinely continuous learner operating alongside the manual controller, since recurrent neural state and weights were dormant throughout the policy handoff. A healthy history and a healthy *policy* are distinguishable objects.

## Bottom line / suggested next loop

The Garden has **state-dependent recovery basins and strong policy dependence**: intervention timing matters, a late policy change alone often fails after depletion, and either externally supplied resources or externally supplied energy can open new trajectories. Preserving hidden neural history is not equivalent to having useful policy weights. All results are finite-horizon synthetic measurements, with the original baseline still paused at tick100.

The strongest next test would give an actual online learner access to long-horizon consequences, then compare its pre-shock and post-shock behavior to exact-state handwritten and frozen controls—without supplying external repair or the target threshold as a teacher.
