# Neural Garden v0.1 — First independent evaluation

**Status:** Executed bounded synthetic tests, 2026-11-11 UTC. Not evidence of general intelligence, evolutionary improvement, or a viable ecosystem.  
**Source:** `evaluate.py`, complete raw data `evaluation_results.json`.  
**Command:** `.venv/bin/python NEURAL_GARDEN_V01/evaluate.py --size 12 --steps 200 --seeds 7 17 29 43 61 --output NEURAL_GARDEN_V01/evaluation_results.json` (from repository scratch root).

## Construction and independent controls

Compare learning-enabled and weight-frozen worlds for five distinct starting seeds. Each is a 12×12 toroidal grid with 144 independent neural cells, run for 200 synchronous ticks. Initial conditions and RNG seeds are paired, but **the world trajectories diverge after actions and updates differ**. Consequently, on-policy prediction errors do not measure performance on identical data. All values below are descriptive five-seed means, not generalization claims.

| Metric after 200 ticks | Learned | Frozen | Reading |
| --- | ---: | ---: | --- |
| On-policy next-resource MSE | 0.003882 | 0.016113 | Learned cells fit their experienced outcome distribution better |
| Average cell energy | 0.017753 | 0.054849 | **Learned cells have lower energy**; no viability improvement |
| Harvest-action frequency | 0.568056 | 0.493056 | Learned policy harvests more frequently |
| Mean resource | ~0.365 | ~0.398 | The world distributions differ |

Energy is low in both arms; agents remain present and active even at zero energy in this v0.1 model. It has no reproduction, death, migration, species selection, or population evolution. `learning=True` changes weights through local prediction error and a policy-gradient-like energy reward; it does not imply better survival.

## Two independent prediction probes disagree constructively

The first probe is a **standardized off-policy expectation** implemented by `Garden.prediction_probe()`. It uses independent synthetic resource/energy fields, zero prior recurrent state, and a fixed 50% reference harvest-action expectation, then compares each cell's prediction with the expected next resource under that reference. Same cases and target for learned and frozen models.

| Seed | Initial/frozen MSE | Learned MSE at tick 200 |
| --- | ---: | ---: |
| 7 | 0.015364 | 0.020518 |
| 17 | 0.015660 | 0.022265 |
| 29 | 0.015152 | 0.021215 |
| 43 | 0.014821 | 0.020667 |
| 61 | 0.015218 | 0.020286 |

**Learning worsens this standardized probe in every seed.** This shows that lower on-policy error does not imply improvement under a different fixed action distribution and input regime. Note its target is a conditional expectation for a reference policy, not a sampled realized transition; that is a distinct question.

The second probe, `heldout_common_world_probe()`, runs a new independent *frozen reference Garden* for 80 steps and scores both trained/frozen predictor weights against the **same actual reference-world consequences**, carrying probe-specific hidden states from zero without changing weights. It asks for transfer to a concrete policy-induced observational trajectory rather than the 50% fixed synthetic expectation.

| Seed | Learned MSE | Frozen MSE |
| --- | ---: | ---: |
| 7 | 0.005282 | 0.016296 |
| 17 | 0.005348 | 0.014603 |
| 29 | 0.005168 | 0.016093 |
| 43 | 0.004683 | 0.014543 |
| 61 | 0.005073 | 0.015097 |

Here the learned weights are better across five seeds. This **does not cancel the standardized probe failure**: the reference trajectory occupies a different part of state/action space, and predictive sufficiency is explicitly target-distribution-relative. Neither test covers all possible worlds. These probes were developed and analyzed during the same pilot, so results are development evidence, not prospective blinded confirmation.

## Reproducibility and checkpoint integrity

Three independent seeds (7,17,29) passed exact full-state fingerprint comparisons:

- Two equal-seed, equal-policy worlds at tick 17 have equal full-state fingerprints.
- Saving and reloading preserves all state, weights, memory and RNG fingerprint.
- 13 resumed ticks exactly match an uninterrupted run at **each step**.

This tests deterministic continuation for the recorded configuration. It does not establish recovery from arbitrary process crashes or corrupt storage.

## Fresh-seed extended follow-up (not used to tune model)

After the first pilot, an additional **three different seeds** (83,97,101) were run for 600 ticks at the same grid size. Raw results are `evaluation_followup_600.json`.

| Metric at tick 600 | Learned (range) | Frozen (range) |
| --- | ---: | ---: |
| On-policy resource prediction MSE | 0.00176–0.00193 | 0.01395–0.01606 |
| Mean cell energy | 0.00816–0.00879 | 0.03107–0.04057 |
| Standardized reference-action probe MSE | 0.03131–0.03183 | 0.01537–0.01580 |

This reinforces the warning: on-policy predictions continue improving **while energy and standardized prediction transfer deteriorate**. It is a confirmatory *directional* follow-up on fresh seeds for these exact settings, not proof of failure under all learning rates or world rules. No parameter adjustment was made between these runs.

## What remains open

1. **Why energy falls:** The learning policy increased harvest but did not maintain energy. Diagnose reward scales, end-of-resource effects, and lower-bound clamping rather than silently rewriting the model after seeing these seeds.
2. **World semantics:** At zero energy cells still act; this is an abstract dynamical grid with neural learners, not yet an ecosystem subject to genuine survival selection.
3. **Generalization:** Register fixed test distributions *before* tuning a next model. Both held-out probes ask different questions and need broader regimes, capacities, independent seeds, and uncertainty intervals.
4. **Baseline fairness:** Compare fixed neural controllers, a simple deterministic heuristic policy, shuffled-target learner, and shared-weight cells. Current frozen comparator is one useful control, not a complete ablation.
5. **Population and memory:** Future cell reproduction/inheritance, spatially explicit signal channels, migration, mutation and selection would require their own independently tested laws. Do not label their absence an emergence failure.

**Research interpretation:** Neural weights changed and task-specific predictions improved in some regimes, while energy and one standardized probe deteriorated. The evidence supports **local adaptation**, not general improvement. The ability to pause, resume, audit and compare is already real and reproducible.
