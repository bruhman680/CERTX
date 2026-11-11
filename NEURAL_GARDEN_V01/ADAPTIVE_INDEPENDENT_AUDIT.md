# Independent audit: adaptive thresholds and the omitted fixed-policy comparator

**Status:** Executed additional exploratory counterfactual experiments. Audited the source and published raw results in this working tree. This is a synthetic, designer-defined model; none of these experiments establishes emergent intelligence, open-ended evolution, or indefinite sustainability.

## What the adaptive learner is

`ADAPTIVE_threshold.py` has **one learnable scalar resource threshold per cell**, expressed by logistic harvest propensity `sigmoid(14*(resource-threshold))`. This is not the original twelve-hidden-unit recurrent neural controller: its `Garden` superclass allocates those weights, but the adaptive threshold policy does not use them for action. The learning rule uses a policy-gradient score `-14*(action-p)` and an exponentially decayed eligibility trace (decay `.97`). That derivative sign is consistent with the logistic Bernoulli policy and threshold parameter; no teacher threshold is supplied. Training rewards use **clipped realized energy changes**, and learned thresholds are deployed deterministically in a **new test world** with learning off.

The original adaptive report's paired comparison **learned vs the same randomly initialized thresholds without learning** is meaningful within this simulator. In its fresh 15-seed, size16, 1,200-train/2,000-test experiment, mean energy was learned `.31764` vs untrained `.29118`, a `.02647` mean uplift (15/15 positive pairwise differences). A separate size12 validation batch (30 seeds, 900-train/1,000-test) had `.30494` learned vs `.27924` untrained (30/30 positive). This supports a **small learning-related improvement over that specific heterogeneous untrained initialization**, not generalized superiority.

## Counterfactual that changes the interpretation

I independently tested a stronger posthoc comparator. In **10 fresh size16 training seeds 1800..1809** (1,200 train ticks) each learned policy's thresholds were evaluated on the **same new test-world seed** (seed+9000) over 2,000 ticks in four ways:

| Deterministic test controller | Final mean energy, 10 paired seeds |
| --- | ---: |
| Learned heterogeneous thresholds at original cell positions | **.30979** |
| The same learned threshold multiset, spatial positions shuffled | .29967 |
| Uniform threshold equal to that trained world's **mean** learned threshold (~.498) | **.62649** |
| Original untrained heterogeneous thresholds | .27631 |

Artifacts: `ADAPTIVE_AUDIT_SHUFFLE.py` and `ADAPTIVE_AUDIT_SHUFFLE.json`. The uniform threshold is a deliberately posthoc ablation prompted by seeing the earlier result; it was **not** part of an independently frozen model-selection protocol.

In another **20 fresh held-out test seeds 10800..10819**, no learning or neural policy involved, original environmental laws, size16, 2,000 ticks, the following *posthoc candidate screen* was run:

| Fixed resource threshold | Mean energy at tick2000 |
| ---: | ---: |
| .450 | .02434 |
| .475 | .30842 |
| .490 | .63161 |
| .500 | .63701 |
| **.510** | **.63912** |
| .525 | .58143 |
| .550 | .27177 |

Artifacts: `ADAPTIVE_AUDIT_FIXED_GRID.py` and `ADAPTIVE_AUDIT_FIXED_GRID.json`. The .51 result is best **only among these posthoc candidates at this horizon**; it is not a global optimum, not an independent confirmation, and not proof of infinite-horizon viability. The sharp sensitivity also warns that small threshold parameter changes can outweigh architecture complexity.

**Key correction:** The early adaptive prototype did exceed the previously selected fixed `.55` control in its 2,000-tick comparison, but `.55` had been selected from a **600-tick** screen. That is not a robust long-horizon standard. Fixed `.50`/`.51` controls perform roughly **twice** as well as the adaptive learner at tick2000 in comparable simulation settings. Thus do **not** claim neural adaptive behavior outperforms simple hand-coded rules. The most defensible claim remains a modest, reproducible improvement over the matched initial heterogeneous-threshold distribution.

## Limitations and next controls

1. **Policy class:** This is per-cell scalar-threshold reinforcement learning, not trained recurrent cognition. Initial spatial **heterogeneity** itself changes performance; use shuffled and uniform-threshold comparisons by design.
2. **Horizon selection:** A fixed rule favored at t600 can perform poorly at t2000. Predeclare horizons (e.g., 600/2000/5000), optimize training settings on a separate development set, and evaluate on genuinely untouched seeds and environment coefficients.
3. **Short-run learning signal:** The reward uses clipped actual energy changes; floor occupancy weakens incentive gradients. For ecological sustainability, track the pre-clipping raw energy budget, tail means, and boundary occupancy.
4. **Teacher-free but simple:** No teacher supplies the answer, but architecture and reward explicitly encode resource and energy. A small paired gain over a random baseline is not proof of open-ended adaptation or evolving intelligence.
5. **Same-world equality:** Baseline and learned variants are evaluated on identical test seeds, world laws and horizon, but training and testing distributions are generated by the same code family; generalization to new physics or real biology is untested.
6. **Experimental dependence:** All ablations and candidate thresholds here were suggested by observing earlier results. Treat confidence intervals across seeds as within-model sampling variability only, not independent real-world replication.

## Provenance

Python 3.12 and NumPy 2.5.4 in this environment; the adaptive source SHA256 at audit was `ad5003aee67640efc831b35865dd506d4212236b0af9dda5ed62fed30e8ac59b`, original environment `garden.py` was `ab49fddf1a61744e3f2e11d9eca95ac4f73b774446ee17480bd13237a24e7ea1`, and fixed-threshold implementation was `93230b8f5c3bb6a0ec28eca5e69f7fe99d3450905e8db9045e788216aaef2e12`. The raw row-level outputs and short scripts are archived alongside this report.

**Conclusion:** Interesting progress inside the limited policy-gradient mechanism, but the stronger finding is a comparison correction: *horizon-matched fixed rules, especially near `.50–.51`, remain substantially stronger at 2,000 steps*. Keep the negative result and upgrade the controls before deciding what truly learned.
