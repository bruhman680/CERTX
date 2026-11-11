# Sequential dynamics society: four physics hypotheses, 40 adaptive probes

**Status:** Executed numerical inquiry, **four distinct conceptual research questions, 40 adaptive probe decisions, one held-out calibration pass**—not 40 separate scientific discoveries or 40 substantive FRR research loops. Files: `SOC_DYNAMICS_active_scan.py` and `SOC_DYNAMICS_results.json` (complete ordered 40-step acquisition lineage, candidate-selection reasons, every seed's outcome, source SHA-256, interpreter/NumPy versions and fresh held-out evaluation). The raw JSON key `loop_count=40` is an algorithmic counter for acquisition iterations, **not the global FRR research-loop ledger**. No neural weights are trained in this study; the *experimenter* adaptively chooses the next rule to probe.

## Research question and actual probe definition

Can a simple harvesting threshold be tuned so a population maintains energy when resource physics shifts? **Each probe iteration** is an experimental decision: an untested threshold selected using the *previous* trials, a prediction that it may improve the incumbent, a probe on three matched seeded worlds, observed energy/resource/floor/raw-drift evidence, a clear accepted/rejected result, and an updated candidate choice. These are **40 adaptive probe iterations**, not 40 distinct conceptual hypotheses and not 40 independent external scientific replications. The substantive inquiry has four physics hypotheses—one per intervention regime—and a fifth calibration question about whether screening choices generalize to untouched seeds.

Four explicitly labeled law regimes received 10 sequential probe decisions each:

1. Original laws: regeneration `.06`, harvest consumption `.18`, diffusion `.08`.
2. No diffusion: set diffusion `.00`, otherwise unchanged.
3. Lower regeneration: `.055` instead of `.06`, otherwise unchanged.
4. Higher consumption: `.185` instead of `.18`, otherwise unchanged.

The experimental objective is **mean final energy − 0.25 × near-zero-energy-cell fraction**, measured at step 3,500. Each regime starts with thresholds `.475`, `.50`, `.525`. The remaining seven candidates are chosen by interpolation of measured scores plus distance-to-tested exploration; every candidate is distinct within its regime. Decisions are therefore *adaptive* and cannot be called preregistered threshold optima. Final candidates were assessed separately at tick 5,000 on **five untouched seeds (4500–4504)**, alongside fixed `.50`, `.51`, `.525`, `.55` comparators.

Total: `40 × 3 = 120` adaptive-screening runs and **100 separate held-out runs** (`4 regimes × 5 comparator thresholds ×5 seeds`), or **220 simulation runs** overall. Every run has a 16×16 world and explicit unchanged energy laws. The original fixed-rule simulator's local transitions were checked against the vectorized experimental implementation for 100 steps with absolute floating tolerance `1e−12` (only expression-association roundoff).

## What actually survived held-out probes

| World law | Best threshold chosen by 10-loop screening | Its held-out mean energy at tick 5,000 | Held-out floor fraction | Tail raw energy drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Original | `.50125` | `.67178` | `0` | `+0.0000160` |
| No diffusion | `.50125` | `.51054` | `0` | `−0.0000253` |
| Regrowth `.055` | `.49225` | `.01763` | `.352` | `−0.0019167` |
| Consumption `.185` | `.54225` | `.03451` | `.091` | `−0.0006001` |

Under the **original laws**, the fixed comparator `.51` actually did slightly *better* on the untouched holdout than our screened `.50125` (`.6743` vs `.6718`). This is an important **negative calibration result**: the adaptive search selected a plausible candidate but did **not** identify the best among these held-out comparator choices. The advantage of `.50125` over `.50` in mean energy was only ~`.0002`; no meaningful optimum claim follows.

Under the **no-diffusion** altered law, the harvested population still has fairly high bounded energy at t5,000, yet its raw tail energy budget is negative. This is a finite-horizon retention state, not a validated equilibrium.

Under **less regrowth**, all tested thresholds are near the energy floor by tick 5,000, despite selecting a new candidate. Under **more consumption**, the selected `.54225` yields only `.0345` mean energy, with negative raw drift. Neither change was compensated by merely tuning the threshold within the evaluated search range `.43–.56`.

## FRR synthesis and evidential boundary

The Garden's dynamics lie on a narrow coupling between regeneration, harvesting costs, and resource-conditioned timing. Merely adjusting the decision rule is insufficient when resource physics moves into an unfavorable energy budget. Even the *experimenter's* sequential search does not invent a viable strategy in these altered regimes. This strengthens the case for learning objectives or memory that can respond to changed circumstances, while also warning that some world regimes may genuinely make the tested policy family infeasible.

The test is posthoc design-space exploration with five holdout seeds **from the same toy generator**. It does not establish a mathematical optimum, biological intelligence, inevitability of collapse for all possible strategies, or long-term viability beyond 5,000 ticks. Three screening seeds and five holdout seeds limit statistical confidence. Future work should test richer conditional policies and long enough horizons, with each law change declared separately and severe/softer changes distinguished.

## Next explicit hypothesis

Can a *temporal* action policy that uses prior resource trajectory, local neighbor gradients, or reserve energy maintain viability when a memoryless threshold fails? The answer requires a matched original-vs-perturbed world comparison with frozen memoryless controls; merely adding recurrent cells without such evidence would not establish progress.
