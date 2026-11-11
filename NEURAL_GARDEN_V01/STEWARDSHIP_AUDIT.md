# Neural Garden v0.2 — independent stewardship audit

**Date:** 2026-11-11 UTC. **Status:** Local adversarial development review; the thresholds below were explored after observing v0.2 outcomes and are **not** a prospectively validated policy ranking. No external publication. The canonical frozen CERTX Garden was untouched.

## Main finding

`stewardship_garden.py` does not change the world laws. It changes the *designer-supplied action reward* from immediate cell-energy change to

\[
R_{\mathrm{steward}}=\Delta E+0.65\,\Delta r.
\]

The resource transition contains an action-specific consumption term `-0.18*r*a`. Relative to resting, the expected incremental reward for harvesting at resource level `r` becomes

\[
(.25r-.063)-(.65\cdot .18r)=.133r-.063.
\]

This explicitly penalizes harvest-related resource depletion and changes the sign of the one-step incentive near `r=0.4737`. It is **hand-engineered restraint**, not evidence that neural cells spontaneously discovered sustainability. The exogenous parts of `Delta resource` (diffusion/regrowth) also enter the noisy learning signal but do not change this action-specific reward difference conditional on the observed state.

The v0.2 learner does change its individual network weights through actual local feedback; the *objective* guiding those changes was specified by the designer.

## Replicated outcomes under unchanged world laws

I independently ran size-12 worlds for 200 steps on seeds 7,17,29,43,61. v0.2 learned stewardship mean energies ranged `0.0543–0.0917`, v0.1 learned mean energies `0.0158–0.0190`, and frozen-policy energy `0.0427–0.0742`. Stewardship harvested less (~0.42–0.48) than the original neural policy (~0.55–0.59), leaving higher mean resources (~0.405–0.416 versus ~0.361–0.374).

At 600 steps on fresh seeds 83,97,101:

| Policy | Seed 83 energy | Seed 97 | Seed 101 | Mean |
| --- | ---: | ---: | ---: | ---: |
| v0.1 neural learning | 0.00816 | 0.00816 | 0.00879 | 0.00837 |
| v0.2 neural stewardship | 0.06026 | 0.06852 | 0.05539 | 0.06139 |
| v0.1 frozen neural policy | 0.03250 | 0.04057 | 0.03107 | 0.03471 |

Thus the shaped objective improves energy outcomes in the tested conditions, but the absolute energy level is still low and it does not prove long-term viability, open-ended evolution, or emergence of unprogrammed ecological understanding.

## Adversarial non-neural control: simple resource thresholds

I also implemented a fixed, **nonlearning** local rule directly against the same resource/energy transition equations:

`harvest = 1 if local_resource > threshold else 0`.

For each threshold, initial resource/energy fields used the same seeds 83/97/101, size 12, 600 synchronous world ticks. Neural weights were unused; no learned policy or reward shaping was involved.

| Fixed threshold | Seed 83 energy | Seed 97 | Seed 101 | Mean |
| --- | ---: | ---: | ---: | ---: |
| 0.35 | 0.00768 | 0.00893 | 0.00747 | 0.00803 |
| 0.45 | 0.29053 | 0.30475 | 0.29996 | 0.29841 |
| 0.55 | **0.48121** | **0.48579** | **0.48339** | **0.48346** |
| 0.65 | 0.03962 | 0.03715 | 0.04141 | 0.03939 |

The threshold-0.55 heuristic dramatically outperformed v0.2 stewardship (~0.483 versus ~0.061 energy), despite having no neural network or learning mechanism. This is a **post-hoc development counterexample**, not evidence that `0.55` is an optimal or universally transferable threshold. A follow-up must freeze candidate thresholds and test on unseen seeds, altered resource laws, and multiple grid sizes. This control is sufficiently strong to prevent interpreting v0.2's energy improvement as proof that neural adaptation is necessary or efficient.

**Fresh-seed check after freezing threshold 0.55:** I then evaluated three previously unused seeds 211,223,227, with the same size 12, 600 ticks, world equations and no extra tuning. The heuristic's mean energies were `0.48446, 0.48307, 0.48906` versus learned v0.2's `0.06292, 0.05900, 0.05852`. This independently replicates the **large gap within the same generator family**. It does not establish cross-environment superiority or a globally optimal threshold.

## Mathematical caveat: homogeneous mean-field sustainability

For spatially homogeneous constant harvest probability `p`, resource equilibrium from the unchanged world law is `r*=1/(1+3p)`, and expected energy drift away from clipping is

\[
\Delta E^*(p)=p\left(\frac{.25}{1+3p}-.063\right)-.022.
\]

This expression has a negative maximum (about `-0.00133` at `p≈0.331`). **It applies only to the homogeneous constant-p mean-field regime.** It does not rule out state-dependent, heterogeneous, cyclic harvesting policies, which the simple threshold control shows can fare much better. Clipping at energy bounds also changes boundary statistics. Do not claim the world is mathematically incapable of sustained energy or infer that v0.2 violated a theorem.

## Design and evidential risks

1. **Reward leakage by design:** The learner is *told* to value resource preservation through a direct weight on `Delta resource`. That is a policy objective, not emergent ecological ethics.
2. **One-step signal:** The action gradient uses immediate shaped advantage; long-horizon consequence sensitivity has not been learned or measured independently.
3. **No population evolution:** Cells do not reproduce, die, move, or inherit weights. Resource and behavior maps evolve, neural weights update, but there is no biological-style selection process.
4. **Policy comparisons:** Simple threshold policies can outperform the neural system by large margins. Future controls should include resource-conditioned logistics, random policies and action-matched controls, with held-out seeds and declared compute.
5. **Prediction vs stewardship:** Better resource prediction does not imply better resource management. Report predictor MSE, energy/resource stability, action diversity and policy cost separately.
6. **Long run:** At hundreds of steps, `mean_energy` is not the same as population viability; no death rule exists, and bounded energy clips at zero.

## Recommended next discriminating experiment

Freeze a small family of local heuristic policies on development seeds. Compare them against frozen neural controllers, v0.1, v0.2 shaping, and an explicitly resource-aware neural baseline on independent seeds and larger/changed worlds. Match initial fields, measure learning cost and threshold transfer, and expose policy uncertainty. Only after beating simple baselines on new conditions should we test whether learned recurrent memory or intercell communication adds value.

## Verdict

v0.2 is a legitimate **reward-shaping intervention** with positive energy effects relative to its original neural baseline. It does not demonstrate spontaneous stewardship or superiority over elementary fixed policies. The simple threshold control is a strong negative finding and should remain prominent in the experiment record.
