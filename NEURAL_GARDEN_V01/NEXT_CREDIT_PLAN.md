# Frozen causal plan — why do online policy updates degrade?

Written **before** execution of `NEXT_CREDIT_*` outcome-bearing tests. Follows `NEXT_ONLINE_PLAN.md` but uses **fresh seeds** and distinct, one-factor causal contrasts. No new objective or parameter value will be selected based on its results.

## Motivation

In the matched online/frozen stochastic experiment, continued updates of the per-cell energy-aware policy harmed both live ecological state and the deterministic competence of its later learned weights. Which learning-rule component is responsible?

Predeclare the baseline reward-shape `reserve_resource` (penalty .3, explicitly designer engineered), one-neuron resource+energy logistic cells, original Garden resource/energy laws, fixed stochastic action selection, pretrained initial threshold weights. Baseline hyperparameters: learning rate `.04`, eligibility trace decay `.97`, reward-baseline smoothing `.995`. No teacher labels.

## Three conceptual pressures and one common control

1. **Reward observation:** compare pre-clipping raw energy reward versus post-clipping *actual* energy reward, with otherwise identical reserve/resource shaping. Hypothesis: clipped reward hides failure at energy floor and degrades response; this is conjecture, not outcome.
2. **Delayed credit horizon:** compare trace decays `.70`, `.97` (baseline), and `.995` keeping raw reward and baseline fixed. Hypothesis: shortening credit might prevent harmful attribution in a rapidly changing environment; longer credit is an adversarial alternative.
3. **Reward baseline adaptation:** compare `.995` baseline update (baseline) with faster `.90` smoothing, holding all else equal. Hypothesis: fast baseline may track changing regimes, reducing gradient miscalibration.

Common **no-update frozen stochastic** comparator uses exactly the same trained initial theta, initial world, and RNG/action-selection mode. A strong **manual reverse-rescue** rule (`R>.51`, or if `E<.12` require `R>.535`) is included as non-neural reference, not as a teacher.

## Fixed experimental burden

- **Main test seeds 9700–9711** (12 independent matched training worlds, size10×10). These are separate from `NEXT_ONLINE` seeds9600–9611 and untouched benchmark seeds9800–9811.
- Each seed: 1000 stable pretraining ticks under original baseline combined reward, then seven arms from exact equal fresh test-world seed+20000 (all neural arms share theta/RNG/physical state at test t0).
- Test horizon **3000 ticks**. Regrowth `.06` first1000, `.055` middle1000, `.06` final1000, with the original consumption/harvest/metabolism/diffusion equations unchanged.
- Record checkpoints t1000/2000/3000, mean energy, fraction near zero, resource, harvest frequency, raw pre-clipping energy drift, trace/gradient metrics and paired seed contrasts. Do not treat cells/ticks as independent replicas.
- After each arm reaches t3000, copy its learned theta into a **frozen deterministic** controller in a fresh evaluation world seed+40000, 1500 ticks stable and mild. This evaluates weight quality without stochastic action sampling. All diagnostic evals use identical initial world state and seeds.
- Primary scientific contrasts are each neural ablation minus raw baseline and frozen stochastic at t3000. Secondary weight-quality comparisons against frozen trained theta. Do not optimize based on these test seeds.

## Limitations

Changing clipped-vs-raw reward observation changes the learning signal but not physics. Changing trace and smoothing values is designed training engineering, not spontaneous adaptation. Paired outputs can diverge through induced action changes and reward histories; do not claim exact isolation of every downstream path. Synthetic-world results and finite horizons cannot prove general intelligence, indefinite viability, or general learning-theory laws.

The canonical Living Garden and all prior experiments remain untouched. New artifacts are `NEXT_CREDIT_*`. Any independent replication should use seeds outside 9700–9711 and 9800–9811, with protocol and source frozen beforehand.
