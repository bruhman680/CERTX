# Mild seasonal change: does online threshold learning add resilience?

**Status:** Executed exploratory controlled follow-up after a previous severe composite scarcity regime devastated all policies. This experiment changes **one** world coefficient at a time. It is neither biological generalization nor evidence of open-ended intelligence.

## Controlled design

Twenty matched fresh train seeds 3200–3219, original world laws, size16 and 1,200 pretraining ticks for the teacher-free per-cell logistic threshold learner. Transfer each learned vector into six identically initialized *new test worlds* with seed `train_seed+10000`, each lasting 3,000 ticks:

- `online`: learned thresholds, stochastic actions and continued policy-gradient updates during test.
- `frozen_stochastic`: **exact same learned thresholds**, stochastic action stream, but no updates.
- `frozen_deterministic`: learned thresholds fixed, deterministic resource-threshold actions.
- `untrained_stochastic`: same training seed's initial randomly heterogeneous thresholds, stochastic actions, no updates.
- `fixed50` and `fixed51`: uniform deterministic rules, thresholds .50 and .51, respectively.

**World intervention:** Test ticks1–1000 use baseline resource regrowth `.06`; ticks1001–2000 use **regrowth `.055` only**; ticks2001–3000 restore `.06`. Harvesting cost remains `.055` throughout, and **there is no resource shock**. The original `.18` consumption, `.08` diffusion, `.03` metabolism and `.008` resting gain stay unchanged. This is an explicit exogenous change in world physics, not spontaneous adaptation. Source: `MILD_REGIME_probe.py`. All six arms start with bit-identical local energy/resource state under matched test seeds. The online/frozen stochastic arms also start with identical weights, thresholds and RNG states; after updating, action streams can diverge.

## Results

Mean cell energy across 20 matched test seeds:

| Policy | Pre-shift t999 | Altered regrowth t1600 | End altered t1999 | Recovery t3000 |
| --- | ---: | ---: | ---: | ---: |
| Online learner | .2604 | .1100 | .0837 | **.2065** |
| Frozen stochastic learned thresholds | .2565 | .1086 | .0836 | .1911 |
| Frozen deterministic learned thresholds | .3040 | **.2362** | **.2170** | **.2690** |
| Untrained heterogeneous stochastic | .2357 | .1109 | .0896 | .1822 |
| Fixed .50 | **.6195** | .0210 | .0202 | .0441 |
| Fixed .51 | **.6177** | .0265 | .0263 | .0504 |

The perturbation is modest numerically (regrowth .06→.055, an 8.3% reduction) but moves the ecosystem into a sharply different long-run regime. The fixed .50/.51 policies that excelled under unchanged laws lose most of their energy and recover poorly after the coefficient returns. This demonstrates strong sensitivity and path dependence in this *particular toy world*, not a universal bifurcation threshold or theorem.

At t3000, the **paired online-minus-frozen-stochastic energy advantage is +.01549**, seed SD .00769, positive for all 20 seeds, with an approximate descriptive normal 95% seed-mean interval `[+.01212,+.01886]`. The online-minus-untrained-stochastic advantage is +.02431, positive for all 20. This is an encouraging within-generator signal that online teacher-free adaptation offers more than a fully frozen *stochastic* trained controller in the chosen mild shift.

**But frozen deterministic use of those same trained thresholds still beats online stochastic learning by .06249 at t3000, in all 20 seeds.** Continued learning is therefore **not established as the best response**. Stochastic exploration during online operation is confounded with policy updating when comparing to deterministic deployment. These numbers do not prove general-purpose adaptation or ecological sustainability.

## Vital hidden distinction: cell-level energy distribution

At t3000, fraction of cells at near-zero energy (≤.01): online **22.1%**, frozen stochastic **23.4%**, frozen deterministic **46.0%**, untrained stochastic **24.5%**, fixed .50 **20.7%**, fixed .51 **13.4%**. The frozen deterministic controller has the highest *mean energy* but also the highest near-zero-cell fraction. Its performance is concentrated among surviving high-energy cells. Mean energy and survival share must be reported together.

The row-level dataset also records resource levels, raw pre-clipping energy drift, resource–action covariance, the last 100-tick average raw drift, and upper-cap fraction. A transient energy improvement should not be interpreted as long-run equilibrium or improved biological fitness.

## Interpretation and next move

This regime test is an exploratory follow-up selected after seeing stronger failures under an earlier composite disturbance; its seeds are new, but the coefficient change was not preregistered. No independent external replication is claimed. The apparent positive online-learning increment is small relative to the deterministic-vs-stochastic action gap, and transfer resets eligibility traces/value baselines rather than preserving uninterrupted agent memory.

The most useful next experiment is a **pure policy-updating causal ablation** with *matched action-selection mode*, matched exploration budget and matched final deterministic deployment under fresh changing environments. Predeclare world coefficients and use untouched seeds. Include energy distribution, raw drift and recovery over 10,000 ticks, because the current 3,000-tick endpoints are not indefinite stability tests.
