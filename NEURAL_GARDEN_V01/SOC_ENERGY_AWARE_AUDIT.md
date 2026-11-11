# Adversarial audit — does the *energy observation* actually help?

**Status:** Completed one new causal-ablation research loop; 24 matched synthetic train/test worlds (12 stable +12 mild), each with three policy deployments over 3,000 test ticks. Reproducible files: `SOC_ENERGY_AWARE_AUDIT_probe.py` and `SOC_ENERGY_AWARE_AUDIT_results.json`, with per-seed results, source SHA-256 and physical-state equality assertions. This is an independent same-generator test, not external validation or 24 conceptual loops.

## Why the published comparison needed another control

The original `SOC_ENERGY_AWARE_REPORT.md` compared two *separately trained* controllers: one with resource+energy observations and another with resource alone. That comparison allows other learned weights to differ, so it cannot isolate the causal influence of using the **energy input itself** at deployment.

I trained one energy-aware teacher-free controller per seed for 1,200 ticks, then copied its **exact same learned resource, energy and bias weights** into two new test controllers with bit-identical resource/energy initial states. Both used frozen, deterministic actions throughout testing. One used the learned energy feature; the other masked **only** the energy observation to zero in its action logit. A fixed threshold `.50` comparator started from the same physical test state. Tests used untouched seeds 19000–19011 (stable) and 20000–20011 (mild regrowth shift `.06→.055→.06` at test ticks1001–2000); no rescue teacher or extra physical-law changes.

## Result at test tick3,000

| Regime | Energy input **on** | Same learned weights, energy input **masked** | Fixed `.50` |
| --- | ---: | ---: | ---: |
| Stable mean energy | **.58845** | .48410 | **.65171** |
| Mild shift mean energy | **.11737** | .09324 | .04357 |
| Stable near-zero-energy cells | **0.49%** | 3.94% | **0%** |
| Mild near-zero-energy cells | **19.27%** | 26.86% | 22.75% |

Paired full-energy-minus-masked advantage was **+.10435** in stable worlds (12/12 wins, seed SD .01829) and **+.02413** in mild worlds (12/12 wins, SD .00397). This is stronger causal evidence that using *the learned energy channel* improves frozen deterministic policy performance, **conditional on that already trained parameter vector**.

The full energy-aware policy remains **worse than fixed .50 in stable worlds** (0/12 wins, mean −.06326). Under the selected mild shift it outperformed fixed .50 in 12/12 seeds (mean +.07380), but the environment choice was exploratory and final mean energy remained low. Importantly, this advantage was from a **frozen** pretrained policy, not evidence of learning during the shift.

## Learned coefficient interpretation

The energy coefficient started at exactly zero. After teacher-free training its mean absolute magnitude was ~`.0705`. Only ~0.2% of cells had a *positive* energy coefficient; almost all acquired a **negative** coefficient. Because the input is `3*(energy−.5)`, a negative coefficient generally raises harvest propensity when local energy is lower, all other features held fixed. This is a plausible learned urgency-dependent relationship, **not** proof that the policy learned an optimal energy-rescue threshold or discovered general ecological intelligence. Its original resource coefficient was already given a positive designer prior near `4`.

## Important remaining confounds

1. **Policy mode:** The earlier stochastic *online* learner performed poorly. The stronger result here arises from deterministic deployment with weights frozen. Do not conflate learned resource/energy dependency with demonstrated benefit of continued online updates.
2. **Learning objective:** The controller receives an explicitly chosen raw local energy reward and a `.97` eligibility trace; no teacher labels are supplied, but its reward and resource-sensitive initialization remain designed choices.
3. **Feature masking changes policy actions:** Holding weights fixed isolates the input's causal use, but the resulting rollout has different state distributions. This is an intervention estimate for the full closed-loop system, not a neuron-by-neuron causal theorem.
4. **Scale/horizon:** 12 seeds per regime, one generator, 3,000 ticks. Near-floor fractions and future long-horizon drift remain relevant. Neither stable-world dominance nor indefinite viability has been demonstrated.
5. **Training/test continuity:** Training and evaluation use distinct initial-world seeds and transfer only neural coefficients; eligibility traces and reward baselines are not carried over. This is transfer evaluation, not an uninterrupted single-world lifespan.

**Verdict:** The energy input *does matter*: the same learned controller with that observation masked consistently performed worse, under both tested environments. Nevertheless the strongest fixed rule is better in the stable regime, and the frozen-deployment success does not demonstrate online adaptability. This is **one substantive causal-ablation research loop**, with evidence preserved separately from the preceding optimization and deployment studies.
