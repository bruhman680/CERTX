# THEORY2 — energy equilibrium, floor saturation, and action yield

Status: **executed synthetic experiment; three substantive research movements.**

## 1. The exact ledger (mathematical result)

For the actual source equations, with harvest fraction `p` and average resource `y` at harvested cells:

`raw_energy_mean = p*(0.25*y - 0.063) - 0.022`.

The raw break-even requirement is `y >= 0.252 + 0.088/p`, where `p>0`. If `p` is too small, this can require `y>1`, which is impossible. A policy that harvests often but badly placed food can therefore do worse than one that harvests less and more selectively. Crucially, this uses *resource at the harvested locations*, not average resource over the entire map.

For each cell, let `z=energy_before+raw`. The measured clipped energy change obeys exactly:

`mean(energy_after-energy_before) = mean(raw) + mean(max(0,-z)) - mean(max(0,z-1))`.

The second correction is excess energy discarded at the ceiling; the first is unpayable energy deficit erased by the imposed floor at zero. Neither represents gained energy or successful learning.

## 2. Fresh matched test (new empirical result)

`THEORY2_budget_probe.py`: eight seeds 10400–10407, size10, 600 training ticks, 3,000 evaluation ticks per online/frozen pair, mild regrowth scarcity ticks 1000–1999 then recovery. All 48,000 world ticks produce energy and resource identities with maximum absolute residuals **3.09e-16** and **3.23e-16** respectively.

| Phase | Learner | Mean clipped energy | Raw per-tick energy drift | Actual per-tick clipped change | Floor population | Mean floor correction |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Scarcity | Online | .0272 | −.00360 | −.00002 | 32.0% | +.00358 |
| Scarcity | Frozen | .0336 | −.00299 | −.00003 | 26.1% | +.00296 |
| Recovery | Online | .0396 | −.00170 | +.00001 | 17.8% | +.00171 |
| Recovery | Frozen | .0521 | −.00113 | +.00002 | 12.2% | +.00115 |

**Finding:** Near-zero change in the *clipped* average energy does not establish ecological equilibrium. In scarcity, almost every unit of negative underlying raw drift is offset by the simulator refusing to let empty cells become negative. Online learning is not shown to be helping: its raw deficit and floor incidence are worse than the matched frozen policy.

The same exact resource budget identity `Delta mean resource = regrowth*(1-mean resource) - .18*mean(resource*action)` held to floating-point precision, confirming that the spatial diffusion term conserved the global resource sum on the periodic lattice in these runs.

## Research lineage

- **Movement A — theoretical compression:** Replace ambiguous 'stable average energy' with separate raw flux, clipping corrections, and distributional floor measurements. Derive exact mathematical identities under the current Garden laws.
- **Movement B — empirical pressure:** Compare the identities on new matched worlds with online learning enabled/disabled. Observed systematic masking during scarcity and recovery. The raw conservation budget is the honest ecological objective; clipped average energy alone can be misleading.
- **Movement C — coupled systems conservation:** Eliminate the unobserved resource-at-harvest action term using the exact resource budget. For `alpha` regrowth and `delta_r` global resource change, `mean(raw)=(.25/.18)*(alpha*(1-r_before)-delta_r)-.063*p-.022`. `THEORY2_coupled_budget.py` validates all six held-out phase/cohort summaries with residual below `7.9e-18`. In a truly stationary resource world (`delta_r=0`), raw long-run nonnegative flow demands `(.25/.18)*alpha*(1-rbar) >= .063*p+.022`. This is a **necessary law-specific resource/energy balance condition**, not a guarantee of survival, and not evidence that any policy satisfies it.

Next strong test: evaluate a policy controller that monitors **unclipped viability margin** plus population floor, preserves competent frozen weights by default, and only performs bounded trial updates on cloned states. Compare against equally-complex sham/rollback controls on untouched seeds. This is a proposal, **not** an existing positive result.

No original Living Garden checkpoint was advanced or overwritten.
