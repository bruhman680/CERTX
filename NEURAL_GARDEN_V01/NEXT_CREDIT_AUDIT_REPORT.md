# Independent credit-assignment audit — why better reward engineering is not yet ecological learning

**Audit status:** One independent conceptual audit loop, 80 new full trajectories (8 pre-reserved seeds × 2 environments × 5 matched controls), each 8,000 ticks. Experimental source `NEXT_CREDIT_AUDIT_probe.py`, complete per-seed checkpoints and SHA-256 source record `NEXT_CREDIT_AUDIT_results.json`. Original 12-seed study also checked. The audit introduced **no changes to Garden physics** or the authored credit-learning mechanisms.

## Source and leakage audit

The original `NEXT_CREDIT_PLAN.md` was written before the original 12-seed run. The main recorded source hashes for `garden.py`, `NEXT_WELFARE_garden.py`, `NEXT_CREDIT_garden.py`, `NEXT_CREDIT_probe.py` match present file bytes. The primary 9700–9711 worlds use independent 1000-tick training seed and test physical world `seed+20000`, with all online/frozen arms starting from exactly equal learned theta, resource, energy and action RNG. No coded train/test world leakage was observed. `frozen_stochastic` is the relevant same-policy, same-stochastic-action comparator; manual reverse rescue is only an ecological reference, not a learned-model counterfactual.

`NEXT_CREDIT_garden.py` alters **credit assignment alone**: `raw` versus post-clipping observed energy reward, eligibility decay `.70/.97/.995`, baseline smoothing `.90/.995`. It retains the same resource diffusion/regrowth/harvest/metabolism/energy clipping laws across all arms. Every neural controller samples actions stochastically, including frozen. Tests therefore isolate intended learning-rule interventions, though resulting action histories and state distributions naturally diverge.

The original mean-energy `.21703` for long trace `.995` is **not a success without qualification**: 43.75% of cells are near the energy floor at t3000, compared with manual reverse mean `.27885`, floor 8.83%. Short trace `.70` has energy `.01758`, floor 41.83%. The modest `online_clipped` (`.04241`, floor18.0%) and `online_fast_baseline` (`.04129`, floor17.58%) improve on baseline online (`.03695`, floor19.75%) but remain below frozen stochastic (`.04888`, floor16.92%). Clipped reward's small paired gain occurs 12/12 times; none of these prove long-run repair.

## Untouched-seed, long-horizon replication

The audit plan `NEXT_CREDIT_AUDIT_PLAN.md` reserved eight new training seeds **9900–9907** and 8,000-tick tests before seeing main results. After the main results, we selected `online_fast_baseline` using only 9700–9711, because it reduced depleted-cell exposure without substantially sacrificing mean energy. **Selection caveat:** This is an explicitly *post hoc* equity-safety constraint, not the audit plan's unconstrained scalar `energy − 0.5×floor` maximizer: that scalar would choose long-trace (≈−.00172), despite its 43.75%-floor exposure. Fast-baseline scored ≈−.04663 versus clipped ≈−.04759. Thus this comparison is exploratory and must not be described as a strictly preregistered arm-selection contest. The untouched seeds remain valid independent tests of the tested controllers.

Regime `stable` has constant regrowth `.06`; `mild` has `.055` on ticks1001–2000, then `.06` again. All neural arms start with exact equal theta/action-RNG/world within each seed/regime. The same manual policies start from the same physical state. Every cell has three learned logistic policy weights, **not a transformer**. Policy weights update online in the two online arms and remain frozen in the `frozen_stochastic` arm.

| Stable world, tick8000 | Mean energy | Final floor | Bottom-decile energy | Tail raw drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Online fast reward baseline | .03705 | 19.625% | .000059 | −.0017804 |
| Online original raw updater | .03472 | 21.250% | .000025 | −.0019240 |
| Same neural weights, frozen stochastic | **.04820** | **16.375%** | .000588 | −.0014971 |
| Manual reverse rescue | .69169 | 1.000% | .18814 | +.0000251 |
| Manual neighbor gradient | **.69760** | **.250%** | .18182 | +.0000244 |

| Mild-shift world, tick8000 | Mean energy | Final floor | Tail raw drift/tick |
| --- | ---: | ---: | ---: |
| Online fast reward baseline | .03749 | 19.50% | −.0017624 |
| Online original raw updater | .03431 | 22.50% | −.0019227 |
| Same neural weights, frozen stochastic | **.04817** | **16.375%** | −.0014972 |
| Manual reverse rescue | **.36840** | **10.750%** | −.0000450 |
| Manual neighbor gradient | .19975 | 11.750% | +.0000265 |

At tick8000 **frozen stochastic wins mean energy against both online variants on all eight seeds in both environments**; it also has lower final floor fractions. All three neural policies exhibit negative raw late energy drift, while simple manual policies retain far higher energy. This strongly rejects the hypothesis that changing only the reward baseline smoothing has *already* repaired continued online learning.

From the same mild-shift test, t3000 mean energies were fast baseline `.0413`, raw online `.0377`, frozen `.0466`, reverse `.2870`, neighbor `.0520`. By t8000, manual neighbor recovers to `.19975` while reverse reaches `.36840`; neural arms remain close to the floor. The fixed mild perturbation was **not length-scaled**: it lasted precisely ticks1001–2000 in both audit regimes, making recovery horizon interpretable.

## Weight-quality cross-check and limitations

Online-tuned final weights were transferred to identical fresh worlds using **frozen stochastic action mode** for 1,500 ticks. Their stable mean energies were fast `.0376`, raw `.0356`, initial frozen `.0540`; mild-trained weight transfers gave fast `.0383`, raw `.0355`, frozen `.0540`. This agrees directionally with ecological degradation and rules out the claim that only adverse live-state inheritance masks better learned policies. **Protocol deviation:** audit plan called for deterministic frozen transfer; implemented transfer was frozen **stochastic**. It is a mode-matched independent-weight test, but must not be mislabeled deterministic. The original authors' deterministic transfer test remains separate.

The original signed `raw_tail` budget is a *pre-clipping* local energy increment, not the delta of clipped stored mean energy. Its negativity warns of drain, without proving an infinite-horizon trajectory. Eight world seeds, one synthetic resource-law family, and a deliberately weak 0.005 regrowth perturbation do not establish general failure of policy-gradient learning or the limits of memory systems. No tested arm includes an independently constructed multistep delayed reward, learned world model, or inter-cell communication; varying eligibility decay is only a **trace horizon** test, not a demonstration of cognitive memory.

## Verdict and next pressure

1. The current fast-baseline credit change slightly improves the failing online baseline, but **does not beat freezing the original trained network**, nor strong fixed rules, over 8,000 ticks in untouched synthetic worlds.
2. Extending eligibility trace may inflate *average* stored energy at the cost of a greatly depleted subpopulation. Mean energy alone can mistake unequal survival for healthy learning.
3. A substantive next candidate would separate training-time exploration from deployed control, explicitly learn the **resource externality** of harvesting, and use a future-return critic or a bounded energy-preservation constraint. The burden should require improved energy **and** floor occupancy **and** raw late budget on untouched long-horizon seeds, with a predeclared selection rule that excludes post hoc welfare weights.

**Count:** One independent reasoning-and-experiment loop; 80 newly computed trajectories, not 80 autonomous research loops.
