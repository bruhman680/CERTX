# Longitudinal Garden Society — four substantive research loops

**Status:** Executed. Four evidence-driven research loops, not 25 research loops. The first loop made 25 logged policy-level *optimization/probe decisions* on one exact historical Garden; they are nested experiments, not separate conceptual loops. The other three loops asked materially different questions using fresh held-out worlds and stronger controls.

**Canonical world:** 16×16 seed37 at tick100, complete neural weights and RNG preserved. Its full-state fingerprint was verified unchanged by the exploratory script. All tested controllers below are explicitly **hand-coded, non-neural harvesting rules** grafted onto copies; this is not evidence of neural learning, mutation, or evolving intelligence.

## Loop 1 — Which ecological feedback might prevent energy-floor collapse?

Run `SOC_LONGITUDINAL_explore.py` and inspect `SOC_LONGITUDINAL_results.json`. Starting from the identical historical tick100 checkpoint, compare 25 sequential policy hypotheses/measurements: near-threshold bracketing, energy-at-cap rest, energy-rescue gates, neighborhood gradients, resource-trend gates, periodic phase gates, hysteresis, and stochastic action uncertainty. A 300-tick physics-equivalence check confirms the forked baseline matches `ThresholdGarden` exactly.

The highest t5000 mean energy on this **selected single world** was a simple local emergency rule:

> Harvest if local resource exceeds 0.51. But if cell energy is below 0.12, allow harvesting already at resource 0.485.

This rule is **designer-supplied** from exploration, not learned independently. At t5000 it retained mean energy 0.27893 and zero cells near the floor, versus fixed .50 energy 0.25980 and ~10.2% near floor. When extended to t20000 on the same historical world, the rescue rule kept ~0.6271 energy/floor0 versus fixed .50 ~0.4588/floor13.3%. Under two exogenous resource reductions (×.7 at ticks5000/7500), rescue t10000 energy .1999 versus fixed .50 .0989. These follow-ups share the *same historical world* and are not independent replication.

**Pressure:** Could this be a selection accident or merely equivalent to choosing a different constant threshold?

## Loop 2 — Fresh-seed validation, not same-world confirmation

`SOC_LONGITUDINAL_validation.py`, `SOC_LONGITUDINAL_validation.json`: 120 matched runs, **five policies ×24 fresh seeds** (20,300–20,323), size16, 10,000 ticks, identical initial resource/energy laws. Candidate policies were frozen before these fresh seeds, but they were chosen posthoc from loop 1.

| Non-neural policy | Mean energy t10000 | Energy-floor fraction | Late raw drift/tick |
| --- | ---: | ---: | ---: |
| Fixed .50 | .67662 | .0060 | +.0000190 |
| Fixed .51 | .67459 | .0073 | +.0000199 |
| Fixed .515 | .67313 | .0052 | +.0000195 |
| **Energy rescue (.51/.485)** | **.68295** | **0** | +.0000207 |
| Neighbor-gradient (.51, coupling +.5) | **.69120** | .0057 | +.0000236 |

Energy rescue minus fixed .50 is only +.00633 across seeds (13/24 positive; SD .01487), so it was **not** reliably better than fixed .50 at this horizon. It exceeded fixed .51 on 24/24 seeds (mean +.00835). Neighbor gradient had higher *average* energy but nonzero floor occupancy. These are small, mechanism-sensitive synthetic differences.

**Pressure:** Does the rescue advantage grow over longer histories and after disturbances?

## Loop 3 — Long horizon and two shocks

`SOC_LONGITUDINAL_stress.py`, `SOC_LONGITUDINAL_stress_results.json`: **72 runs**, three frozen policies ×12 fresh seeds ×two declared scenarios:

| Scenario | Fixed .50 energy | Energy rescue | Neighbor gradient |
| --- | ---: | ---: | ---: |
| Unchanged original laws, tick20,000 | .64308 | **.72053** | .66177 |
| Two resource×.7 shocks at ticks3,000/6,000, tick10,000 | .39938 | **.50035** | .49975 |

Rescue-minus-fixed .50 mean energy differences were **+.07745** (12/12 seed wins, SD .01708) at t20000 and **+.10097** (12/12 wins, SD .01731) after two shocks at t10000. In unchanged 20k runs rescue's floor fraction averaged .00033 versus fixed .50's .08105; near-zero floors after shocks were observed in both arms at the stated endpoint, not proof every cell was healthy during the shock. These are matched *within-generator* differences only. Tail raw drift stayed small (~+2.5×10⁻⁵ for rescue), so no infinite-horizon viability claim is justified.

**Pressure:** The rescue policy may have lower effective threshold than fixed .50. A stronger fixed-threshold comparison is required.

## Loop 4 — Adversarial lower-threshold grid

`SOC_LONGITUDINAL_counterfactual.py`, `SOC_LONGITUDINAL_counterfactual_results.json`: **128 runs**, eight policies ×16 fresh seeds (20,800–20,815), size16, 20,000 ticks, original world laws. Fixed thresholds .48/.485/.49/.495/.50/.505/.51 were frozen alongside rescue.

| Controller | Mean energy at tick20,000 |
| --- | ---: |
| Fixed .48 | .03032 |
| Fixed .485 | .35510 |
| Fixed .49 | .62519 |
| Fixed .495 | .63689 |
| Fixed .50 | .64625 |
| Fixed .505 | .65178 |
| Fixed .51 | .65619 |
| **Energy rescue .51/.485** | **.72906** |

Rescue exceeded every one of these fixed thresholds across **all 16 paired seeds**; versus the best tested fixed .51, mean +.07287 energy (seed SD .00958). This supports a local **state-conditional harvesting benefit**, but neither proves the rule optimal nor excludes untested fixed thresholds (.512, .516, etc.), more sophisticated non-neural baselines, or failure under different world laws. Candidate selection remains posthoc from one canonical world. No neural architecture learned this rescue behavior.

## Mechanistic interpretation and next research pressure

The rescue policy preserves a useful distinction erased by a single scalar threshold: a cell's **local energy reserve** changes when harvesting is worth the long-term resource cost. It harvests conservatively in normal conditions and temporarily lowers the threshold when a cell is depleted. This can protect lower-energy cells even when mean energy is not maximized, but every mechanism assertion remains model-bound and testable.

Next: test the frozen rescue rule under **predeclared changes to regrowth/cost and entirely untouched seed ranges**, with severe and mild shocks, record time-to-recovery and cell-level energy distributions. Only then compare an action-aware *learned* policy to this stronger interpretable benchmark with identical observations and environmental laws. More tests do not transform a hand-designed rule into independent intelligence.

**Reproducibility:** Every raw result file records exact policies, seed and horizon, final measurements, source hashes, and methodological limits. No canonical checkpoint was modified. `SOC_LONGITUDINAL_explore.py` also records the precise parent fingerprint and proves same-world state conservation.
