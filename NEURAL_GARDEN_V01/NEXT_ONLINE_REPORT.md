# Are online neural weight updates helpful when exploration is held constant?

**Status:** Executed predeclared causal study, awaiting independent audit. The protocol in `NEXT_ONLINE_PLAN.md` was written before any main-study results and given to an independent reviewer together with untouched audit seeds `9800–9811`. The only preceding smoke test used unrelated seeds `10600–10601`. Source `NEXT_ONLINE_probe.py`; all twelve per-seed runs, full checkpointed policy evaluations, source hashes and summaries in `NEXT_ONLINE_results.json`.

## The burden

Our earlier Garden investigations found a sharp difference between poor *online stochastic* neural ecology and much healthier *frozen deterministic* deployment. Two factors were confounded: whether the neural weights kept changing, and whether cells kept taking stochastic exploratory actions. We therefore tested these separately.

1. **Same-action-mode contrast:** `reserve_resource` teacher-free per-cell policy-gradient learner with penalty `.3`, trained 1000 stable ticks, then online learning ON vs exact trained clone with learning OFF. Both select stochastic actions, start with bit-identical physical state, neural threshold vectors and RNG state, and use the same mild regrowth schedule `.06→.055→.06` across 3000 ticks. Their actions are allowed to diverge after weights change—this is part of the treatment effect.
2. **Isolated learned-weight competence:** At test ticks0/1000/2000/3000, copy each arm's weights and deploy them as **frozen deterministic** controllers on *identical fresh evaluation worlds*, both stable and mildly shifting. The same evaluation-world seed is used for every checkpoint for each training seed. Thus no online stochastic exploration occurs during this secondary evaluation.

Twelve main train seeds `9600–9611`, grid10×10, fresh test worlds with seed+20000, fresh deterministic evaluation worlds seed+40000; original environmental laws except explicitly labeled regrowth change. Source and protocol frozen before outcomes. Independent audit seeds are separate and not used to choose the learner, reward or coefficients.

## Result 1: Continued stochastic online learning was harmful

| Policy mode, tick3000 | Mean cell energy | Near-floor cells ≤.01 | Late raw energy drift per tick |
| --- | ---: | ---: | ---: |
| Online weight updates, stochastic actions | .03778 | **17.83%** | −.001845 |
| **Same trained weights frozen, stochastic actions** | **.05283** | **13.83%** | −.001460 |

Paired online-minus-frozen mean energy = **−.01504**, seed SD `.00531`, online wins **0/12**. Both are ecologically unhealthy; the online branch harvests more frequently (`.4533` vs `.4308` at the endpoint) and depletes resources faster (`.4226` vs `.4381` mean resource). Reward shaping did not establish useful online adaptation. Floor-clipping can hide negative budgets, hence raw drift is reported separately.

## Result 2: The updated weights themselves degraded in deterministic evaluation

All policy evaluations below use *frozen deterministic* actions on fresh matched worlds, so exploratory action sampling is absent. Each frozen comparator retains its original trained weights through all checkpoints.

| Source-weight checkpoint | Stable eval: online-updated vs frozen weights | Mild eval: online-updated vs frozen weights |
| --- | ---: | ---: |
| t0 (exact same weights) | `.68084` vs `.68084` | `.22498` vs `.22498` |
| t1000 (before regrowth reduction) | `.68378` vs `.68084` | `.16853` vs `.22498` |
| t2000 (after reduced regrowth) | `.62656` vs `.68084` | `.10783` vs `.22498` |
| t3000 (after restoration) | **`.54951` vs `.68084`** | **`.04455` vs `.22498`** |

At the final checkpoint, the online-updated weights lost **every one of the 12 paired evaluation seeds** in both stable and mild regimes. In the mild evaluation the learned-weight penalty was `−.18043` energy. The updated controller also had *more* depleted cells in mild evaluation (`28.33%` vs `16.67%`). Under stable evaluation, updated weights had **fewer** near-floor cells (`.92%` vs `1.92%`) but substantially lower mean energy—another reminder that health has multiple axes.

This is stronger than merely observing that stochastic exploration is costly: **within this fixed setup, the online weight updates themselves moved the policy toward worse future deterministic competence.** The stable t1000 checkpoint showed a tiny temporary positive stable-evaluation change, but by t3000 the direction reversed.

## Scope and critiques

- This is evidence about one explicitly engineered `reserve_resource` objective, one policy architecture and a chosen synthetic Garden law/shift, **not a claim that online learning is generally harmful**.
- The learning setup had a positive resource-sensitive inductive bias and engineered reward penalties. It used no teacher demonstrations or direct action labels, but those designer choices shaped what the network could readily learn; this is not an emergent moral system.
- Different learner trajectories after t0 can produce different observations, reward baselines and stochastic action sequences. Our deterministic theta-transfer diagnostic isolates the quality of the *resulting policy weights*, not a mathematical decomposition of every causal pathway by which they developed.
- The deterministic evaluation worlds are fresh but from the same simulator generator; findings are within-model only. Tuning on the reserved audit seeds was explicitly prohibited.
- The same world state has 100 interacting cells and 3000 ticks, but replication is at the **12 independent seed** level, not `n=1200` or `n=36000`.
- No evidence of indefinite viability, beneficial adaptation across all environments, open-ended intelligence or globally optimal multiobjective policy.

## Next orientation

Investigate *why* the gradient direction degrades learned decision quality: examine advantage estimation with pre-clipping reward, baseline dynamics, eligibility traces and policy drift under environment changes. A conservative next test would freeze online updates during low-reward scarcity and resume learning only after recovery, using a predeclared switching rule and strong frozen controls; that is another designer intervention, not spontaneous solution.

**Crucial pending requirement:** Independent reviewer `/root/benchmark` must rerun this frozen protocol on untouched seeds `9800–9811` and check exact source/version identity before treating the negative result as confirmed. Do not modify the learner or this frozen burden in response to that review.
