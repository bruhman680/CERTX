# Neural Garden v0.1 — Stewardship and multi-agent ecology research

**Date:** 2026-11-11 UTC. **Scope:** primary-source research guidance and proposed discriminating experiments; not a claim that this Garden has evolved cooperation or ecological intelligence.

## Primary research contacts

1. **Leibo et al. (2017), [Multi-agent Reinforcement Learning in Sequential Social Dilemmas](https://arxiv.org/abs/1702.03037).** Spatial/temporal Harvest and Cleanup games show that cooperation versus competition depends on environmental dynamics, scarcity and interaction conditions. For our Garden, treat sustainability as an observable outcome, not a behavior that follows automatically from locally intelligent cells.
2. **[A Multi-agent Reinforcement Learning Model of Common-pool Resource Appropriation](https://proceedings.neurips.cc/paper_files/paper/2017/hash/2b0f658cbffd284984fb11d90254081f-Abstract.html) (NeurIPS 2017).** Explicit resource appropriation reveals conflict among individual benefit, long-run sustainability and inequality. Gives relevant metrics for regenerative supply, overharvest, distribution and survival.
3. **Nowak (2006), [Five Rules for the Evolution of Cooperation](https://pmc.ncbi.nlm.nih.gov/articles/PMC3279745/).** Relatedness, reciprocity, network structure and group-level mechanisms are distinct paths to cooperation. In a neural grid, compare outcomes against spatial mixing and no-communication controls before assigning any cooperative explanation.
4. **Ng, Harada & Russell (1999), [Policy Invariance under Reward Transformations](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf).** Potential-based shaping can preserve optimal policies under particular MDP assumptions. This is a warning that arbitrary extra 'cooperation rewards' may redefine success or cause gaming, not a blanket guarantee in multi-agent nonstationary learning.
5. **Jaques et al. (2019), [Social Influence as Intrinsic Motivation for Multi-Agent Deep Reinforcement Learning](https://proceedings.mlr.press/v97/jaques19a.html).** Influence-based intrinsic reward can facilitate interaction/coordination. But communication frequency or influence is not the same as ecological benefit; measure influence and resource outcomes independently.
6. **[A Game-Theoretic Analysis of Networked System Control for Common-Pool Resource Management Using MARL](https://proceedings.neurips.cc/paper_files/paper/2020/hash/71c1806ca28b555c76650f52bb0d2810-Abstract.html) (NeurIPS 2020).** Alternative incentives and common-resource control can change welfare under network constraints; suggests explicitly comparing decentralized policies to simple centrally prescribed harvest quotas.
7. **[Learning to Harvest Without Collapse in a Regenerative Commons](https://arxiv.org/abs/2609.36478) (2026 preprint).** A recent proposed constrained-learning approach for regenerative resource preservation. Treat as a primary contemporary candidate, not established proof that a particular controller is superior. Inspect its constraint definitions before importing a penalty term.

## Minimal stewardship mechanics to test (not pre-authorized claims)

Begin with measurable physical-like bookkeeping, not complex reward stories:

- Resource at grid location `r[i]` is bounded by a carrying capacity `K`; regeneration depends on currently available resource. An example law is `r_next = clip(r + g*r*(1-r/K) + diffusion - extraction, 0, K)`. The boundary value `r=0` is absorbing under pure logistic regrowth: if recovery from total depletion is intended, an explicit seed/influx term is needed. Do not silently invent new resource from zero.
- A cell's harvest cannot exceed its local available resource. Energy gain is linked to actual extracted resource, with a measurable conversion factor and cost. Report any external resource input independently.
- Communication, sensing, movement and updating weights consume declared resources *only if this is a tested design choice*. Avoid imposing hidden normative costs to force a pleasing outcome.
- Death/reproduction are ecological rules separate from reinforcement learning. A population increase can arise from inheritance, selection or imposed seeding without online individual learning.
- Keep an observation-action-receipt record. Reward is a measurement or explicit experimental objective, not an invisible guarantee that the world improves.

## Core experimental comparison matrix

| Arm | Cell policy | Resource law | Main diagnostic |
| --- | --- | --- | --- |
| A | Random/local reactive, no learning | Regenerative | Null ecology / survival baseline |
| B | Local neural, fixed weights | Identical | Complexity from fixed rules alone |
| C | Online predictor learning, no reproductive mutation | Identical | Predictive skill versus ecology; no inferred stewardship |
| D | Explicit stewardship constraint or penalty | Identical | Are resources protected? At what throughput/fairness cost? |
| E | Copy-and-mutate evolutionary ecology | Identical | Genealogical selection versus within-life learning |
| F | Local communication enabled/disabled | Identical | Coordination evidence versus incidental spatial clustering |

Compare matched seeds, initial resources, environmental laws and time horizon. When feedback is given, measure predictive skill separately from resource outcomes. Do not interpret one run with more living cells as superior ecological intelligence without accounting for regeneration, energy subsidies, reproduction and selection.

## Metrics to retain every checkpoint

- Total and spatial distribution of resource; influx/regeneration/extraction/outflow budget and any balance residual.
- Alive fraction, births/deaths, energy distribution and extinction risk across seeds.
- Sustained harvest `H` versus regeneration `G`; resource-collapse episodes and recovery time.
- Equity measures (e.g., variance or Gini of energy/resource access) with caution that equality can coexist with collapse.
- Predictive holdout error and weight change for each cell; learning must improve the declared task to earn that label.
- Spatial clustering and signal-flow strength as descriptive organization, not evidence of cooperation by itself.
- Robustness to supply reductions and perturbations, measured against fixed-rule and random baselines.

## Five high-value probes

1. **Overshoot and collapse:** vary demand and regeneration; locate empirical resource depletion boundary across seeds, with exact conservation checks. Don't interpret that threshold as a universal CERTX constant.
2. **Free rider:** introduce costly public resource regeneration/cleanup actions and compare individual vs group resource outcomes. A cell may benefit from others' costs while declining to contribute.
3. **Memory access:** erase selected cell recurrent states or local signals while holding environment/RNG fixed, then measure future harvest and prediction differences; this tests whether information is operationally relevant.
4. **Shaping sensitivity:** compare unshaped, explicit sustainability penalty, and potential-based shaping. Never proclaim ecological cooperation simply because the objective directly rewards it.
5. **Distribution shift:** lower regeneration mid-run without changing the neural architecture. Ask whether adaptation happens, how long it takes, whether old skill survives, and whether global resource budgets remain valid.

## Pitfalls and scoped interpretation

An attractive self-organizing pattern can be unsustainable; a sustainable population can be a scripted regulator; local prediction improvement need not improve the ecology; group persistence can coexist with unequal access or hidden subsidies. We should demand independent observables and negative controls before calling any of these 'learning', 'stewardship', 'cooperation', or 'emergence'.

This note offers design options for a later Neural Garden cycle. It does **not** instruct an automatic change to v0.1 world physics, controller objectives, or its frozen checkpoints. Version every environmental intervention as a new condition and preserve the baseline.
