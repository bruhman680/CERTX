# Can a learned per-cell harvesting policy handle unfamiliar scarcity?

**Status:** Executed exploratory nonstationary-world stress test. All trials are synthetic. The goal is to test transfer and online adaptation, not to claim intelligence, stable ecosystems, or biological generality.

## Design: 144 matched worlds with a shared, declared disturbance

Twenty-four independent pretraining seeds 2500–2523, size16; each policy trains for 1,200 ticks on the **original** v0.1 world using the teacher-free REINFORCE/eligibility-trace threshold learner. For each seed, transfer the trained per-cell threshold vector to a fresh world with test seed `train_seed + 10000`, then run **six** matched arms for 3,000 ticks (**24×6=144 trajectories**):

1. `online`: trained thresholds, stochastic actions and continued teacher-free policy-gradient updates during test.
2. `frozen_stochastic`: exactly the same trained thresholds, same initial world/action RNG streams, stochastic actions with learning disabled.
3. `frozen_deterministic`: same trained thresholds frozen, action iff resource exceeds local threshold.
4. `untrained_stochastic`: the same pretraining seed's original untrained heterogeneous thresholds; stochastic, no updates.
5. `fixed50`: deterministic fixed resource threshold `.50`, no learning.
6. `fixed51`: deterministic fixed resource threshold `.51`, no learning.

**World change explicitly distinguished from learner change:** Test ticks 1–1000 (internal tick0–999) use original v0.1 physics: resource regrowth `.06` and harvesting cost `.055`; before decision on test tick1001, every resource is multiplied by `.70`. For ticks1001–2000, regrowth falls to `.025` and harvesting cost rises to `.070`; for ticks2001–3000, world laws revert to original values. This combines a sudden resource shock with *two* concurrent physical-law changes. It does **not** isolate which perturbation caused any effect. `REGIME_garden.py` holds the explicit intervention; original `garden.py` is unchanged.

Starting resource and energy are exactly matched for all six arms within each test seed. The online/frozen stochastic arms start with identical thresholds and action RNG streams; their action trajectories can diverge as online thresholds update. We record checkpoints at ticks 500, 999, 1200, 1600, 1999, 2200, 2600, and 3000, including resource, energy, raw pre-clipping drift, energy-floor occupancy, action-resource covariance, and preceding 100-tick average.

Only trained **threshold parameters** transfer; the online arm starts its eligibility trace and reward baseline fresh in the test world. This is a transfer-and-relearning intervention, not uninterrupted within-world autobiographical memory.

## Results: all arms suffered acute collapse during scarcity

Mean cell energy (24 matched seed worlds per arm):

| Arm | Baseline tick999 | Scarcity tick1200 | Scarcity tick1999 | Recovery tick3000 |
| --- | ---: | ---: | ---: | ---: |
| Online trained stochastic learner | .2651 | **.0010** | .0011 | .1995 |
| Frozen trained stochastic | .2626 | .0011 | .0012 | .1943 |
| Frozen trained deterministic | .3112 | .0015 | .0015 | **.2702** |
| Untrained heterogeneous stochastic | .2421 | .0012 | .0013 | .1861 |
| Fixed threshold .50 | **.6178** | .0017 | .0125 | .0219 |
| Fixed threshold .51 | **.6169** | .0000 | .0015 | .0469 |

The scarcity intervention is *very severe*: at tick1200 approximately 94–100% of cells in each arm are near the energy floor. By tick1999 the frozen fixed `.50` arm retains some energy (~.0125), but all arms are ecologically devastated by this phase. This is not a benign seasonal fluctuation.

At recovery tick3000, online minus frozen-stochastic energy is **+.00519** (seed-level SD .00699, 18/24 paired seeds positive). Online minus untrained-stochastic is +.01340 (22/24 pairs positive). These are small toy-world effects relative to the much bigger trained-deterministic advantage: the frozen deterministic learned-threshold arm is **+.07073** above the *online stochastic* arm, in every one of the 24 matched pairs. At baseline before scarcity, the fixed .50/.51 policies were strongest; after shock and recovery, their mean energy is low. The policy class, stochastic exploration, learned threshold heterogeneity, and time horizon jointly alter the ordering.

## Critical audit of mean energy

Mean energy can hide very uneven cell populations. At tick3000:

| Arm | Mean energy | Fraction near energy zero (≤.01) | Final 100-tick raw drift |
| --- | ---: | ---: | ---: |
| Online learning | .1995 | **22.3%** | −.00260 |
| Frozen trained stochastic | .1943 | 22.8% | −.00271 |
| Frozen trained deterministic | .2702 | **43.0%** | −.00480 |
| Untrained stochastic | .1861 | 23.8% | −.00280 |
| Fixed .50 | .0219 | **0%** | −.00024 |
| Fixed .51 | .0469 | **0%** | +.00039 |

The frozen deterministic learned-threshold arm has the highest mean energy at tick3000 but **43% of its cells are near the floor**, while both fixed-policy arms have low mean energy but **zero cells near the floor** at that instant. Neither metric alone is an honest ecological-health score. The very different fractions reflect clipping and spatial heterogeneity, not a declaration that one strategy truly survives indefinitely.

The learned stochastic arms exhibit slightly *negative* resource–action covariance in baseline and recovery phases, whereas the fixed `.50` policy has positive covariance in baseline but near zero immediately following the shock. Thus the existing adaptive learner has not discovered resource-preserving timing comparable to the strongest fixed rule.

## Interpretation and next pressure tests

- **No demonstrated robust adaptive advantage:** Online policy updating buys only ~.005 energy relative to a matched frozen stochastic pretrained controller, while a frozen deterministic deployment of those learned thresholds does substantially better. The difference is confounded by continuing stochastic exploration versus deterministic action, so this is not a clean causal decomposition of adaptation.
- **The world was made hostile by design:** Lower regrowth, higher cost, and shock act simultaneously. Failure is not proof that adaptation is impossible; success after physical laws revert is not proof of learned generalization.
- **History and hysteresis matter:** Fixed `.50/.51` dominate the unchanged baseline but recover poorly from the depleted state here. Earlier intact-world strength does not guarantee shock recovery. However the scarcity intervention nearly zeroed all arms, creating a floor-saturation regime where clipping can obscure ongoing damage and suppress learning signals.
- **Independence:** 24 seeds are the experimental replication units, not 256 cells ×3,000 ticks. The probe settings and arms were chosen during exploratory research; test seeds were new, but this is not preregistered external confirmation.

**Next strongest experiment:** Isolate **one** environmental perturbation at a time (shock-only vs altered regrowth-only vs altered cost-only), use milder perturbations so substantial live signal survives the scarcity phase, compare stochastic online vs frozen stochastic using matched action streams and *also* separate deterministic evaluation. Prefer full 10,000-tick replay and raw energy budget over single-tick mean snapshots. Only then can we know whether these cells truly adapt to changing conditions rather than simply endure or fail under forced regime shifts.
