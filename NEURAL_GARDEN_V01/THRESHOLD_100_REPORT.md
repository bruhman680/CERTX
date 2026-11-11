# Neural Garden — second, distinct 100-run threshold sweep

**Completed 2026-11-11 UTC.** Scripts and raw experiment rows: [`threshold_100_sweep.py`](threshold_100_sweep.py), [`threshold_100_results.json`](threshold_100_results.json). This is **100 independent simulation runs**, separate from the prior 100 neural-world runs and the earlier 20-run exploratory threshold baseline.

## Frozen design

Five candidate **fixed local resource thresholds** `0.35, 0.45, 0.55, 0.65, 0.75`, 20 matched fresh seeds `200..219` each, a total of exactly **5×20 = 100** simulations. In every simulation, the grid is 16×16 (256 cells), duration 600 ticks, action `harvest` iff pre-step local resource exceeds threshold. No neural model or learning is used. The original v0.1 resource and energy laws are unchanged. Record checkpoints 100, 200, 400, and 600; final 100-step averages; and 100-step harvest-frequency blocks. The raw JSON includes all 100 uniquely identified rows, source SHA-256, per-run configuration SHA-256, checkpoints and state fingerprints. Threshold candidates were fixed before running **this** sweep but chosen with awareness of earlier exploratory .55 outcomes; no claim of independent preregistration.

## Outcomes at tick 600 (20 seeds per threshold)

| Threshold | Mean energy | Mean resource | Harvest frequency | Fraction at energy floor (≤.01) | Raw unclipped energy drift/tick |
| --- | ---: | ---: | ---: | ---: | ---: |
| .35 | **.00769** | .35539 | 68.48% | 51.41% | −.00108 |
| .45 | **.30474** | .43515 | 48.77% | 0% | +.00378 |
| **.55** | **.48762** | .52033 | 31.93% | 0% | +.00261 |
| .65 | **.03721** | .60670 | 21.09% | 21.02% | −.00079 |
| .75 | **.02123** | .71677 | 15.45% | 64.32% | −.00276 |

Average energy over ticks 501–600 is `.00657, .32918, .49254, .03643, .03937` for thresholds `.35, .45, .55, .65, .75`, respectively. Thus .55 has the highest energy in this five-way comparison at tick 600 and across the final 100 ticks. It is **best among tested values** only, not mathematically optimal in the continuous threshold space.

Across matched seeds, differences in final mean energy relative to .55 are **−.47993** (.35), **−.18287** (.45), **−.45040** (.65), **−.46639** (.75). The raw JSON records descriptive paired standard deviations and approximate 95% intervals. These tight intervals reflect low variation in this deterministic simulation generator, not real-world generalization.

## Interpretation and limitations

The relationship is **nonmonotonic**: harvest too freely and the resource is depleted; harvest too rarely and cells fail to earn enough energy to offset metabolism. A simple *conditional* policy can sustain a substantially higher energy level without neural learning, suggesting a local ecological balance mechanism. The .55 threshold's resource-dependent action timing is consistent with its performance against fixed-rate neural baseline policies, but is no proof that fixed thresholds dominate all adaptive learners. No mutation, reproduction, environmental perturbation, external validity or emergent language competence was tested.

Importantly, the raw **pre-clipping** energy drift was recorded separately from the realized change of bounded energy. A cell at zero can show zero realized change despite having a negative underlying energy budget. Mean energy can also conceal divergence among cells; energy-floor fraction and ceiling fraction are therefore reported. A positive raw drift at tick 600 does **not** alone prove indefinite viability: energy is clipped at 1, and the simulated horizon was 600 steps.

The five candidates were chosen after seeing the previously good .55 baseline; these 100 runs are an honest **screening comparison**, not unbiased discovery or independent confirmation of an optimal threshold. Next tests should freeze .55 and its nearest challengers, vary costs and world seasons and evaluate on fresh untouched environments; compare with action-aware neural policies at matched information, and separately test long-horizon stability.
