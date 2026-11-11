# Second stress-test pass: apparent stability is horizon-dependent

**Status:** Posthoc follow-up to the 600-tick external shock pilot; 120 additional nonlearning fixed-threshold runs, 20 fresh matched seeds `820..839`, thresholds `.45/.55/.65`, shocked and unshocked controls, all carried to **2,000 ticks**. The original environmental transition laws remain unchanged within each tick; shocked worlds receive `resource *= .40` after ticks 200 and 400. Exact code and per-run checkpoint traces are in `PERTURBATION_longhorizon.py` and `PERTURBATION_longhorizon_results.json`.

## Mean energy through time

| Threshold | Shock intervention | Tick 600 | Tick 1000 | Tick 1500 | Tick 2000 |
| --- | --- | ---: | ---: | ---: | ---: |
| .45 | None | .3014 | .0973 | .0247 | .0244 |
| .45 | Two shocks | .0657 | .0304 | .0304 | .0304 |
| **.55** | **None** | **.4834** | **.4221** | **.3441** | **.2690** |
| **.55** | **Two shocks** | **.1160** | **.0855** | **.0534** | **.0416** |
| .65 | None | .0374 | .0374 | .0374 | .0374 |
| .65 | Two shocks | .0566 | .0566 | .0566 | .0566 |

**Crucial correction to the earlier 600-step impression:** even without shocks, the `.55` nonlearning policy's mean stored energy declines from about `.483` at step 600 to about `.269` at step 2000. With two shocks it declines toward `.042`. Thus 600-tick energy retention cannot be interpreted as demonstrated long-run sustainability or an equilibrium. This is a stronger counterexample to any overly enthusiastic reading of the threshold-screen results.

An additional single-seed diagnostic (`seed=820`, threshold `.55`, no shocks) found stepwise raw energy drift changes sign: at tick 600 it is positive (~`+0.00678`), but at tick 400 it is negative (~`−0.00686`), and mean energy declines over the longer interval. Neither floor nor ceiling clipping was active for this specific diagnostic at those recorded ticks. Therefore a **positive raw drift at a selected tick** is insufficient to show nonnegative *time-averaged* drift even when clipping is absent. We must measure the whole trajectory.

The `.65` and shocked `.45` apparently flat energy tails are also not proof of health: energy clipping at zero can yield a stable low average with many depleted cells. These rows should be interpreted alongside the floor fraction contained in checkpoints and ideally followed by raw energy-budget and action-covariance plots.

## Next inquiry

The strongest test is not just to maximize `energy_at_t600`. Estimate long-horizon viability under shocks with *uncensored raw energy drift*, floor occupancy, duration-to-depletion, and recovery dynamics. Freeze all candidate policies and validate on untouched seeds; then train an action-aware neural policy to change its harvesting rule when the world is disrupted. A persistent positive energy reserve across long horizons remains an **open target**, not an achieved capability.
