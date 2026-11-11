# Independent adversarial benchmark — ecological welfare and conditional actions

**Status:** Executed **one substantive independent research loop**, supported by 168 distinct simulation trajectories (2 explicitly different regimes ×12 matched fresh seeds ×7 policies ×4000 ticks; 12 separate 1200-tick neural training trajectories reused across the two test regimes). Exact source fingerprints, per-run metrics, Python/NumPy versions, and complete raw synthetic data: `NEXT_AUDIT_benchmark.py`, `NEXT_AUDIT_results.json`.

The central test is not merely 'which policy has higher average stored energy?' It asks whether conclusions survive measuring **energy equity, time near the floor, raw pre-clipping drift, and ability to regain energy after a resource-regeneration change**. The policy formulas were frozen in the script before this benchmark was run. They were already informed by prior Garden research, so this is an exploratory held-out confirmation within one simulator, **not external preregistration**.

## Exact controlled policies

All worlds start with matched physical resource/energy arrays. No population births, deaths or mutation. Fixed policies use deterministic original-law actions:

| Policy | Harvest condition |
| --- | --- |
| `fixed50` | `R > .50` |
| `fixed51` | `R > .51` |
| `rescue_early` | `R > .51`, or `E < .12 and R > .485` |
| `rescue_late` | `R > (.535 if E < .12 else .51)` |
| `neighbor_gradient` | `R > .51 + .5*(mean_neighbor_R - R)` |
| `learned_energy` | Frozen deterministic teacher-free neural controller, trained separately 1200 steps on 12 independent seeds with raw energy reward; full learned resource+energy inputs |
| `energy_masked` | **Exact same learned parameters**, same physical test world, with only the energy observation masked to zero at deployment |

Original energy and resource equations apply at all times. `stable` uses regrowth `.06` throughout. In the explicitly changed `mild` regime, regrowth becomes `.055` for ticks 1501–2500 and then returns to `.06`. The latter is a **world-law intervention**, not evidence of agent adaptation. All learned controllers are frozen during testing. Each trial is 16×16, 4000 ticks, same 12 test seeds 40000–40011 across arms, matching initial resource/energy state.

## Results at tick4000

Each row gives means across 12 matched seeds. `Floor` is fraction of cells at energy ≤.01, not modeled biological death; `Bottom decile` is the mean energy of the lowest-energy 10% of cells. Tail raw budget averages the final 500 ticks before clipping.

| Stable-world controller | Mean energy | Floor | Bottom decile | Tail raw energy drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Fixed .50 | .66462 | 0% | .34972 | +.0000199 |
| Fixed .51 | .66326 | 0% | .35668 | +.0000113 |
| Early rescue | .66326 | 0% | .35668 | +.0000113 |
| Late rescue | .66326 | 0% | .35668 | +.0000113 |
| Neighbor-gradient | **.67492** | 0% | .35524 | +.0000217 |
| Learned energy input | .58550 | 1.46% | .11373 | +.0000139 |
| Same learned weights, energy masked | .44173 | 6.74% | .00670 | −.0000012 |

**Mechanism warning:** In the 12 stable test worlds, `fixed51`, `rescue_early`, and `rescue_late` produced **bit-identical full final-state fingerprints** for every seed. Thus the energy-conditioned branches never made a different action on the realized stable trajectories. Calling those conditional rules superior *because of their conditional clause* would be false in this regime.

| Mild-regrowth-shift controller | Mean energy | Floor | Bottom decile | Tail raw energy drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Fixed .50 | .05676 | 17.22% | .00002 | +.0000132 |
| Fixed .51 | .06094 | 23.63% | .00000 | +.0000140 |
| Early rescue | .02832 | 29.10% | .00658 | −.0000144 |
| **Late rescue** | **.28993** | **8.40%** | .00193 | −.0000467 |
| Neighbor-gradient | .06700 | 11.69% | .00004 | +.0000278 |
| Learned energy input | .14759 | 18.13% | .00000 | −.0000283 |
| Same learned weights, energy masked | .12698 | 18.59% | .00000 | +.0000002 |

**Paired contrasts:** In stable worlds, full learned-energy beats the exact energy-masked clone by +.14377 mean energy, **12/12** matched seeds. In mild worlds it wins by +.02061, **12/12**. This independently supports functional value of the learned energy input, conditional on pretraining and deterministic frozen deployment. It does not demonstrate online learning during the shift.

The **late-rescue** hand-designed policy beats the early-rescue policy by +.26162 mean energy in mild worlds, **12/12 seeds**, and beats the learned-energy policy by +.14234, **12/12**. Its average energy is substantially better under this particular intervention, but its raw late energy budget remains negative, and 8.4% of cells remain at the floor. The favorable ranking is not a universal rule or a proof of sustainability.

For mild-regrowth worlds, **no tested policy recovered to 80% of its own energy level immediately before the altered-regrowth segment** by tick4000. The measured time-to-recovery is censored at the end of the experiment. Stable-world 'recovery' is inapplicable because no disturbance occurred. The raw data preserve the actual observations rather than imputing recovery times.

## Independent checks and evidential boundaries

1. 168/168 unique `(seed,regime,policy)` identifiers; run and source hashes are retained. All source SHA-256 values matched local bytes after execution.
2. An independent 200-tick same-law control using `ThresholdGarden` agreed with manually evaluated resource dynamics exactly and with energy to within `5.7e-15` numerical rounding. No unexplained physics discrepancy was found.
3. Original Garden v0.1 energy and resource laws remain unchanged; the mild-regrowth test is a separately declared modification. Test worlds are matched initially, but after policies diverge, trajectories are not identical exogenous histories.
4. A learned controller's pretraining world is distinct from its deployment world and only its learned coefficients transfer. This is not a lifelong recurrent-state continuation; no active policy update occurs during test.
5. Resource and energy floor clipping can make stored energy look flat despite negative pre-clipping budgets. No 4000-tick endpoint establishes an attractor or indefinite stability. Repeated simulator seeds are synthetic sensitivity checks, not independent natural-world evidence.
6. The benchmark measures several welfare criteria but does not define a single value-laden scalar welfare optimum. Do not silently optimize one metric and report it as universal wellbeing.

**Next pressure:** Use one *predeclared multiobjective burden* over fresh longer world/regime seeds, examine recovery of the **least-resourced cells**, and compare the best strong hand-coded rule with a genuinely **online-updating** neural policy under the same action budget and observation access. Test one-factor gentle disturbances first, then combine shocks. A static frozen learner's benefit from its energy input is not proof that ongoing adaptation is beneficial.
