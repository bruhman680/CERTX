# Eight-state coarse-graining transfers across ecological regimes

**Status:** Four new evidence-driven conceptual passes, with the earlier 13-loop source and results preserved. This report compares the SAME eight-category microscope and three-macro partition between a collapsing neural-policy world and a viable-looking fixed-threshold policy world. No cognitive-symbolic claim is made.

## Frozen measurement, distinct policies

- Eight microcategories are fixed: `(resource >= .48, energy >= .12, last harvest action)` as three binary bits, using the original `SOC_MACRO_probe.py` representation.
- Frozen macro mapping learned from an earlier independent v0.1 experiment: `[0,0,1,1,0,0,2,2]` (three labels).
- Policies: original learning `Garden`, versus no-learning deterministic `ThresholdGarden` with resource threshold `.50` and unchanged original world resource/energy laws.
- Eight matched training seeds 7200–7207 and eight fresh testing seeds 8200–8207, 100 cells per world, 420 steps. Same initial fields and source-defined rules across arms; subsequent trajectories necessarily differ because actions differ. Predictions target the original **eight-way next microcategory**, not a coarsened target.

| Comparison on heldout worlds | Original learned neural | Fixed threshold .50 |
| --- | ---: | ---: |
| Mean energy at tick420 | .00975 | .60827 |
| Share of observed states with high-energy bit | 31.55% | 100.0% |
| Full eight-state current-only next-micro NLL | .79081 | .47501 |
| Frozen three-label current-only NLL, aligned window | .82147 | .46501 |
| Frozen three-label + 3 prior labels NLL | **.79883** | **.00259** |
| Within-policy memory improvement (lower NLL) | .02264 | **.46242** |

**Critical caveat:** The two policies induce different state distributions and therefore different target entropies. Comparing absolute `.00259` and `.79883` does not show the threshold policy is a better *learning algorithm*; it is not learning at all. The meaningful within-policy contrast is current-only versus history-conditioned prediction using the same target and matched time window.

## Four successive conceptual passes

1. **State occupancy pressure:** Fixed `.50` keeps energy high, while v0.1 learned runs collapse. The fixed world occupies mainly categories `3` (~33.2%) and `6` (~66.4%) with very rare others. Thus the earlier finding that the energy bit alone was highly predictive arose partly from the collapsing world and cannot be carried over unchanged.
2. **Frozen macro representation transfer:** The earlier three-label mapping is *not* automatically an optimal sufficient state in the new policy. Even the full eight-state current-only view has nonzero prediction loss, because a single current symbol omits phase and continuous resource. A frozen three-label view has similar heldout next-micro loss (~.465) and is not a proof of Markov lumpability.
3. **Memory repair:** In the fixed-policy world, three previous macro symbols reduce prediction loss from `.46501` to `.00259` nats. This is a very strong regular pattern, plausibly because the fixed threshold produces a near-deterministic **three-tick resource/harvest cycle**. The memory is *in the observation history*, not acquired neural memory or intelligence. In the collapsed original neural world, history improves loss only `.02264` nats.
4. **Reoptimized partition control:** Greedy train-only merging gives a new three-label partition `[0,0,0,1,0,0,2,0]` for the fixed policy; current-only loss `.46502`, three-lag memory gain `.46341`. The frozen partition is already comparably predictive in this particular state distribution, so optimizing the mapping alone is not the source of the dramatic history benefit.

## An FRR-compatible interpretation

The same compression map can behave differently under different dynamics. A state that seems informationally irrelevant in one regime may become important when the environment settles into a periodic cycle. This is a concrete example of **representation, trajectory, and evidential burden changing together**.

The large memory gain has a mundane mechanistic explanation: missing the phase of a deterministic oscillation. It should **not** be described as a discovery of genuine cognitive memory, `C_num`, `C_struct`, or `C_symb`.

Next falsifying tests: (a) repeat on untouched seeds and a moderately shifted resource-regrowth law, (b) explicitly compare three-tick phase as a feature versus three-lag history, (c) test neighborhood information, and (d) measure whether prediction breaks under resource shocks. A phase-sensitive model may be accurate in the stationary world but fail catastrophically after perturbation.

**Artifacts:** `SOC_MACRO_TRANSFER_probe.py`, `SOC_MACRO_TRANSFER_results.json`. The original 13-loop script and result remain untouched. The new script records all seed sets and SHA-256 source fingerprints.

