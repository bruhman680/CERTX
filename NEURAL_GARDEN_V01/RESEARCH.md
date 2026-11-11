# Neural Garden v0.1 — Academic scout and comparison map

**Date:** 2026-11-11 UTC. **Scope:** primary-source research and experimental design guidance; no claim of novel biological intelligence or original neural-cell concept.

## The closest prior art

1. **Mordvintsev, Randazzo, Niklasson & Levin (2020), [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/).** Cells hold vector states and apply small learned local neural updates, ordinarily with *shared* weights. Their regeneration experiments train growth from seed, maintenance and recovery under damage. This is compelling prior art for local dynamics and ablations, but training a shared rule and training each cell independently are different questions. See also the [primary publication record](https://research.google/pubs/growing-neural-cellular-automata/).

2. **Bert Wang-Chak Chan (2019), [Lenia — Biology of Artificial Life](https://arxiv.org/abs/1812.05433), and [original implementation](https://github.com/Chakazul/Lenia).** Continuous cellular automata can exhibit richly structured traveling and persistent patterns without neural weight learning. Lenia is therefore a necessary *non-neural complexity control*. Do not label movement, longevity or recurring patterns as learning by themselves.

3. **[Self-Organizing Intelligent Matter: A blueprint for an AI generating algorithm](https://arxiv.org/abs/2101.07627) (2021).** A particularly direct precedent: separate recurrent neural networks at grid locations; local energy and chemistry; directional communication; survival and copy-with-mutation of weights. The manuscript explicitly separates ordinary recurrent activation updates from weight inheritance/mutation, and describes evolutionary selection instead of assuming an RL objective. Our core idea of an individual neural controller per cell is **not new**.

4. **[Biomaker CA: A Biome Maker project using Cellular Automata](https://arxiv.org/abs/2307.09320) (2023), with [author project](https://google-research.github.io/self-organising-systems/2023/biomaker-ca/).** Includes material and environmental constraints, reproduction, mutation and interactive evolution. It is useful for energy conservation, death/reproduction rule checks, lineage records and counterfactual interventions.

5. **Lana Sinapayen (2023), [Self-Replication, Spontaneous Mutations, and Exponential Genetic Drift in Neural Cellular Automata](https://arxiv.org/abs/2305.13043).** Shows that replication with mutation can generate inherited variation. This is *evolutionary drift*, not necessarily within-lifetime gradient learning or increasing predictive competence. Separate genotype variation from behavioral improvement.

6. **[Self-Replicating Neural Cellular Automata: Quantifying Emergent Phenotypic and Genotypic Diversity in an Open-Ended Substrate](https://pmc.ncbi.nlm.nih.gov/articles/PMC13705881/) (2026).** Especially close to Thomas's proposal: every pixel carries an individual 44-parameter neural controller, cloning with mutation; reports phenotype/genotype diversity measures across many small and long runs. This makes our per-cell premise well established as a research family. Study its controls and diversity metrics before claiming emergence or novelty.

7. **[Learning spatio-temporal patterns with Neural Cellular Automata](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078362/) (2024).** Shows that learned neural local dynamics can reproduce transient and stable patterns from reaction–diffusion-type systems. The distinction between *learning a transition model* and *producing interesting patterns* is important.

## Experimental design recommendations

### Separate mechanisms that can look the same

| Mechanism | What changes | Appropriate measurement | Essential comparator |
| --- | --- | --- | --- |
| Fixed neural cellular dynamics | Hidden activations and environmental states | Spatial patterns, persistence, resource flux | Fixed-rule non-neural CA or randomized neural rule |
| Online within-cell learning | Each cell's weights with feedback | Prediction error on future unseen transitions, temporal improvement | Identical garden with learning disabled |
| Heritable evolution | Cell weights through copy/mutate and survival | Genealogy, genotype diversity, replacement success | No-mutation, no-copy and neutral drift controls |
| Environmental memory | Fields, trails and neighbor structures | Intervention: erase/transplant field while holding cells and RNG fixed | Same agents with reset environment |
| Distributed memory | Information spread across several cells/edges | Selective multi-cell erasure versus matched single-cell erasure | Decentralized vs centralized/redundant storage controls |

### First reproducibility contract

- Make cell updates synchronous or state exactly which update schedule is used; order dependence can create accidental asymmetries.
- Use seeded RNG and save its state. Check resumed trajectories reproduce uninterrupted trajectories exactly, including cell weights and signals.
- Keep world laws stationary in initial trials. Allow tuning only at explicit versioned boundaries; never silently rewrite the original Garden.
- Record objective and training signal. A supervised prediction loss can establish predictive learning; it does not by itself demonstrate learned survival, cooperation or autonomy.
- Compare **same seeds and initial conditions** across learning-on/off arms where possible. Report diversity/complexity separately from predictive loss.
- Predefine liveness, persistence and improvement metrics, plus explicit failure criteria (collapse, saturation, no measurable learning, divergence).
- Save snapshots and logs at intervals, and bound CPU/memory/time. Do not claim continuous external operation unless a persistent runner/host is configured and observed.
- For reproduction later, trace ancestry and mutation; retain phenotype/genotype difference. A visually rich pattern can coexist with genotype collapse, or vice versa.

## Initial evaluation matrix

1. **Mechanics audit:** mass/resource balance, nonnegative bounded energy, no accidental out-of-grid reads; no NaNs or exploding weights.
2. **Operational audit:** seed determinism, checkpoint/resume identity, pause/restart, parameter variation as a new condition.
3. **Learning audit:** compare online prediction error with no-learning and shuffled-target controls, multiple seeds; avoid evaluating on the exact same transitions used for a gradient step.
4. **Ecology audit:** active fraction, energy distribution, per-cell weights variation, entropy, spatial clustering and mortality. Report descriptive dynamics; don't call diversity 'intelligence'.
5. **Intervention audit:** remove local signal/erase memory/transplant environmental state while holding initial agent weights and RNG matched, ask which future observable changes.

## Honest assessment

Building a per-cell neural world is tractable as a small CPU prototype and has strong published precedents. A **significant contribution** would not be the existence of neural cells; it would be a carefully instrumented, reproducible study of where information survives, whether individual learning improves a declared future task, and how local learning, heritable evolution and environmental structure interact. The first v0.1 should privilege credible measurements and pause/resume over complexity or anthropomorphic claims.
