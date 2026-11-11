# Neural Garden stewardship intervention (v0.2) and viable-world control (v0.3)

**Status:** Separate experimental variants; v0.1 unchanged. These are design interventions, not spontaneous neural evolution.

## Versions

| Version | Class | What changes |
| --- | --- | --- |
| 0.1 baseline | `garden.Garden` | Original individual networks, immediate-energy policy reward, fixed environment |
| 0.2 same-law | `stewardship_garden.StewardshipGarden` | Changes only policy-learning reward to `delta_energy + 0.65*delta_local_resource` |
| 0.3 viable-world | `viable_garden.ViableGarden` | Same as 0.2 but changes baseline metabolism from 0.03 to 0.02 per tick |
| Threshold comparator | `threshold_policy.ThresholdGarden` | Non-neural harvest iff local resource > 0.55; original v0.1 world laws |

All other resource diffusion, regrowth, harvesting, cell architecture, prediction training, input and action APIs remain the same. All cells remain permanently present. No reproduction, mutation, birth/death, or movement yet.

## Why a world-law positive control is necessary

For a spatially homogeneous mean-field stationary harvest probability `p`, the v0.1/v0.2 resource equilibrium under the unchanged world laws is

`r*(p) = 0.06 / (0.06 + 0.18*p) = 1/(1+3p)`.

Ignoring energy clipping, the expected energy drift in v0.1/v0.2 is

`g_01(p) = p*(0.25*r*(p)-0.063)-0.022`.

Its maximum for p in [0,1] is approximately -0.00133, so no *homogeneous stationary* harvest policy can maintain strictly positive unbounded energy drift under this approximation. This is **not** a theorem forbidding heterogeneous spatial policies, oscillatory strategies, or boundary effects from maintaining some positive-energy cells. Because energy is clipped at zero, mean energy and mean energy drift require care.

The v0.3 single-law intervention lowers baseline metabolism by .01, giving

`g_03(p) = g_01(p)+0.01`,

which is positive near p=1/3 (approximately +.00867). Thus a viable homogeneous mean-field region now exists by construction. This does not make the learner intrinsically better: the world is easier.

## Selected diagnostic runs (seed 7)

At tick 500:

| Version | Mean energy | Mean resource | Harvest frequency |
| --- | ---: | ---: | ---: |
| v0.1 learned | 0.0078 | 0.3403 | 0.6680 |
| v0.2 stewardship learned | 0.0528 | 0.4341 | 0.4414 |
| v0.3 viable-world learned | 0.9737 | 0.5139 | 0.2852 |

v0.2 seed7 at tick5000 had mean energy 0.1137, resource 0.4893, harvest 0.3398. This longer run is one trajectory, not evidence of robust viability across seeds. v0.3 approaches the energy upper bound, making it a positive-viability control but arguably too easy for meaningful selection.

At tick 600, seed 7, the non-neural threshold comparator on original world laws has mean energy **0.4891**, whereas v0.2's neural stewardship has **0.0594**. This simple heuristic strongly outperforms our learned policy on viability in this case. It is not a fair claim of universally optimal threshold selection: 0.55 is an investigator-chosen baseline, and broad seed/threshold sweeps remain necessary. The performance gap warns against equating neural complexity with intelligent ecological regulation.

All variants passed finite-state execution and exact checkpoint/resume on tested seeds. Standardized off-policy prediction scoring and multi-seed controls are needed before claiming improved learning or ecological robustness. Short-sighted v0.1 harvesting remains a scientifically useful negative result.

## Next credible design

Specify ecological viability and diversity metrics *before* tuning, test policy reward sweeps with frozen initial seeds, compare heuristic fixed policies and learning-enabled cells, and include resource depletion/recovery periods. Only then consider a separate evolutionary population variant with explicit death, reproduction, heritable mutations, and lineage records. Do not conflate gradient-based learning with evolution by selection.
