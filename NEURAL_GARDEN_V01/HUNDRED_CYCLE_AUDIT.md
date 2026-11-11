# Independent lineage audit — first 100-run Neural Garden sweep

**Scope.** This audit covers `hundred_cycle_results.json` produced by `hundred_cycle_sweep.py`, the v0.1/v0.2/v0.3 Python implementations, and the in-repository claims. It also independently checks a **second, separate 100-run threshold screen** in `threshold_100_results.json` below. This is a review of a *toy simulator*, not a claim of evolved consciousness, open-ended adaptation, or a validated biological model.

## Reproducibility and count verification

- **PASS: 100 distinct run records**, exactly 20 per arm, using seeds 100–119 in each arm, a 16×16 grid (256 cells), and 200 synchronous simulation steps each; total 20,000 grid steps across runs. These are **100 independent seeded simulation runs**, not 100 sequential design revisions or 100 biological generations.
- **PASS: 100 distinct run IDs and 100 distinct run-configuration SHA-256 digests.** Every run has five trajectory records at steps 0, 50, 100, 150, and 200.
- **PASS: source hash check.** The four SHA-256 digests embedded in the JSON matched the present bytes of `garden.py`, `stewardship_garden.py`, `viable_garden.py`, and `hundred_cycle_sweep.py` when audited. File contents may subsequently change; retain the hashed source with the archival result.
- **PASS: matched seed sets across arms**, allowing paired descriptive contrasts. A seed is the unit of replication; 256 cells within a run are interacting units and should **not** be counted as 256 independent replicates. Arm trajectories quickly diverge, so matching the seed does not give identical exogenous trajectories.
- **REMAINING REPRODUCIBILITY LIMIT:** the archival JSON contains final-state fingerprints and source hashes, but no captured package version, interpreter version, or commit ID. Stronger portability checks require replay under a pinned environment and comparison of per-run fingerprints.

## Actual interventions (do not mix up their lineages)

| Arm | Learning? | Reward for policy updates | Environment law |
| --- | --- | --- | --- |
| v0.1 learning | Yes | Realized energy change | Baseline metabolism 0.03 |
| v0.1 frozen | No | No policy updates | Same baseline law |
| v0.2 stewardship learning | Yes | Energy change + 0.65 × local resource change | **Same baseline law**, metabolism 0.03 |
| v0.3 viable learning | Yes | Stewardship shaping | **Changed law**, metabolism 0.02 |
| v0.3 viable frozen | No | No policy updates | Same altered law as v0.3 learning |

**Code-level finding:** `StewardshipGarden.step()` subtracts `self.METABOLISM`; v0.2 defaults to 0.03, `ViableGarden` overrides to 0.02. This distinction was verified after the implementation settled. v0.2 changes the agent's incentive; v0.3 changes the world's energy budget. Cross-version gains in energy **must not** be attributed solely to learned intelligence.

## Verified 200-step results

Values are means across the **20 independent seeds** for each arm, at step 200. MSE is measured on the action-dependent trajectories experienced by each arm.

| Arm | Mean cell energy | Mean resource | Harvest rate | Prediction MSE | Cells with energy ≤0.01 |
| --- | ---: | ---: | ---: | ---: | ---: |
| v0.1 learning | 0.01730 | 0.36457 | 0.58340 | 0.00406 | 51.15% |
| v0.1 frozen | 0.06120 | 0.39957 | 0.49883 | 0.01579 | 22.48% |
| v0.2 stewardship learning | 0.08025 | 0.41151 | 0.47480 | 0.00390 | 16.17% |
| v0.3 viable learning | 0.98263 | 0.43705 | 0.42637 | 0.00392 | 0.00% |
| v0.3 viable frozen | 0.98682 | 0.40067 | 0.50000 | 0.01703 | 0.00% |

Useful paired differences (left minus right), computed by matching seed:

- **v0.1 learning − v0.1 frozen:** energy −0.04390, MSE −0.01173, harvest +0.08457. The baseline neural learner predicts its experienced resource transitions better but depletes energy faster than its frozen comparator.
- **v0.2 stewardship learning − v0.1 learning:** energy +0.06294, MSE −0.00017, harvest −0.10859. Changing the reward signal substantially changes collective behavior without changing environmental laws.
- **v0.3 viable learning − v0.3 viable frozen:** energy **−0.00419**, MSE −0.01311, harvest −0.07363. Learning improves on-policy prediction and resource retention, **but the frozen control actually has slightly higher mean energy**. High v0.3 energy is therefore primarily an environmental-law result, not a demonstrated learning advantage.

Mean energy trajectories (steps 0 → 50 → 100 → 150 → 200) are: baseline learning 0.5503 → 0.4885 → 0.2674 → 0.0692 → 0.0173; stewardship 0.5503 → 0.4972 → 0.3262 → 0.1746 → 0.0802; viable learning 0.5503 → 0.9502 → 0.9852 → 0.9843 → 0.9826. These short horizons do not establish indefinite stability.

## Most useful inference

**The garden exposes the difference among *improving prediction*, *improving decision incentives*, and *changing physical feasibility*.** A cell can learn its local environment while its harvesting behavior harms the shared ecology; stewardship reward redirects collective behavior under the same environmental law; a separate reduction in maintenance cost makes high-energy states accessible even to a **frozen** policy. These three effects are experimentally distinguishable here, and their separation is the strongest defensible result.

## Important caution and future pressure tests

1. **Clipped energy distorts apparent health and reward.** Energy is clipped to [0,1]. At the floor, realized `next_energy − before_energy` can be zero even if the *unclipped* energy budget remains negative; at the ceiling, the converse can hide wasted positive energy. Do not equate near-zero observed change with ecological equilibrium. Add raw pre-clipping drift and floor/ceiling occupancy to future logs.
2. **Mean-field is not a proof of global impossibility.** For a spatially homogeneous constant harvest rate `p`, steady-state resource is `r*=0.06/(0.06+0.18p)`. The baseline mean-energy drift `0.25*r* p − 0.03 − 0.055p + 0.008(1−p)` has a negative maximum near `p≈0.33` (about −0.00133). Thus that *restricted policy family* cannot maintain energy in the unbounded model. Spatial, transient, or heterogeneous strategies require separate analysis; floor clipping complicates observed simulations.
3. **200 steps is short**, and v0.2 still loses substantial energy between steps 150 and 200. A 600-/2,000-step replay and recovery after resource shocks would clarify whether stewardship actually stabilizes rather than postpones collapse.
4. **On-policy prediction MSE is not a controlled generalization test.** A policy changes the difficulty and distribution of examples it sees. Use the existing standardized, nonmutating `prediction_probe()` across all arms, and record both learning and frozen performance on an independent held-out probe.
5. **No cellular reproduction or mutation yet.** The implementation has multiple independent recurrent neural controllers, local interaction, resource flow, and within-cell weight updates; it does **not** model reproduction, population selection, births/deaths, inherited genomes, or emergent societies. Call this a learning multi-cell automaton, not an evolving species.
6. **Design-selected toy world.** Baseline and viable coefficients, reward weight, metrics and comparator classes were chosen by designers following pilot runs, not preregistered and then validated on unseen real-world phenomena. The 20 seeds quantify **within-model seed variation**, not uncertainty about biological or social applicability. Explore robustness to grid size, perturbations, random seeds, coefficients, and alternative policies before assigning generality.
7. **Statistical interpretation.** Report raw paired differences and across-seed variability; these are descriptive simulator outcomes. If formal uncertainty intervals are used, base them on the 20 paired seeds, not on cells or time steps. The deterministic same-source simulation does not yield independent real-world evidence.

**Audit verdict:** count, arm separation, source lineage, and numerical summaries pass checks. The strongest insight is an incentive–feasibility separation, with **no** warrant yet for claims of autonomous ecological intelligence, perpetual viability, or significant new scientific discovery. Preserve both successful and failed interventions as evidence, and use this audit as the boundary for the next loop.

## Independent audit of second threshold screen: another 100 runs

**Count and provenance PASS:** `threshold_100_results.json` contains exactly 100 unique run IDs and 100 unique configuration SHA-256 hashes: **5 thresholds × 20 seeds**, grid 16×16, 600 steps each, seeds 200–219 in every threshold arm, with identical checkpoint layout `(100, 200, 400, 600)` across all records. Both archived source hashes (`garden.py`, `threshold_100_sweep.py`) match the local source bytes. Across both sweeps, there are **200 distinct archived simulation runs**, not 200 architecture generations; total simulated grid steps = 20,000 + 60,000 = **80,000**, excluding pilots.

Here the policy is **not neural and does not learn**: harvest iff pre-step local resource exceeds a constant threshold. Unlike v0.3, the world's energy and resource laws are the *original v0.1 laws*, including metabolism 0.03. This is a stronger baseline than a constant-probability frozen neural policy because its action reacts to local resource.

| Resource threshold | Mean energy at step 600 | Final 100-step mean energy | Harvest fraction at 600 | Raw unclipped energy drift at 600 |
| ---: | ---: | ---: | ---: | ---: |
| 0.35 | 0.00769 | 0.00657 | 0.68477 | −0.00108 |
| 0.45 | 0.30474 | 0.32918 | 0.4877 | +0.00378 |
| **0.55** | **0.48762** | **0.49254** | **0.3193** | **+0.00261** |
| 0.65 | 0.03721 | 0.03643 | 0.2109 | −0.00079 |
| 0.75 | 0.02123 | 0.03937 | 0.1545 | −0.00276 |

**Important revision to the interpretation:** the baseline homogeneous *constant-probability* policy's negative mean-field maximum **does not imply** that the original world is incompatible with every possible policy. This second experiment directly gives a counterexample at 600 steps for a simple *resource-conditional* policy under the original laws: threshold 0.55 maintains much more energy without a learned controller. The gap demonstrates the importance of policy class and timing; do **not** claim that changing metabolism was necessary for *all* sustained behavior. The result overturns the broader-sounding version of the feasibility story, while preserving its narrower constant-rate analysis.

This sweep is **candidate screening**, not unbiased model selection: candidate 0.55 had already looked promising in prior exploration, and the five candidates were deliberately chosen after that observation. It is best **among tested thresholds** and **at 600 steps**, not a proven optimum, global attractor, or perpetual equilibrium. Selection bias and world-specification dependence preclude a general discovery claim. Also avoid directly ranking this threshold arm against v0.1 neural arms as a controlled head-to-head: they have different seeds (200–219 vs 100–119) and horizons (600 vs 200). A valid head-to-head needs equal seeds, horizons, observations, metrics, and world law.

**Updated priority:** freeze the threshold baseline before the next test, run a fair same-law/same-seed neural-versus-threshold comparison, extend to long horizons and shocks, measure raw drifts and resource recovery, and test adaptation under changing local conditions. The richer question is whether neurons learn *conditional policies that respond to scarcity* better than hand-coded local rules, rather than whether the simulator can simply exhibit high energy after tweaking its physics.
