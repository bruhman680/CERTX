# Why continued online updates degrade this Garden policy — physical credit-assignment audit

**Status:** Two executed, distinct conceptual research loops. The first observes how a frozen-source online learner's action timing, resource yield and weights drift across an environmental change. The second intervenes on individual policy parameter updates to test a candidate mechanism. No original `Garden`, `WelfareGarden`, or `NEXT_ONLINE` source was edited.

**Artifacts:** `NEXT_CREDIT_ECO_probe.py`, `NEXT_CREDIT_ECO_results.json`; `NEXT_CREDIT_ECO_ablation.py`, `NEXT_CREDIT_ECO_ablation_results.json`. Each JSON records per-seed outcomes, configurations, platform/source SHA-256 fingerprints and explicit limitations. The independent `NEXT_ONLINE_AUDIT_REPORT.md` was read **before** this diagnostic; its reserved seeds9800–9811 were not reused. These probes instead use new seeds10080–10091 and10180–10191, respectively.

## Anchor: what raw energy gain actually requires

Under the *unchanged* original Garden energy laws, let `p=E[A]` be the fraction of cells harvesting at a tick and `y=E[R|A=1]` their **mean pre-harvest local resource**. Then the *unclipped* mean energy budget is exactly

`E[ΔE_raw] = .25 E[RA] - .063p - .022`

`           = p(.25 y - .063) - .022`.

For `p>0`, a nonnegative raw one-step mean budget therefore requires

`y >= .252 + .088/p`.

This is a **necessary and sufficient algebraic condition for the current tick's raw mean budget**, not a long-run equilibrium theorem. For harvest frequency around `.42`, resource yield must exceed about `.4615`. Merely increasing the harvest rate cannot repair a low yield if additional actions target scarce cells. Clipping at 0 or 1 changes realized energy; the inequality is explicitly *pre-clipping*.

The learner's unshaped immediate payoff from choosing harvest over rest is

`adv_raw(R)=.25R-.063`, positive above `R=.252`.

The selected designer reward is `raw_energy + .3 * Δresource − .3 * max(.18-next_energy,0)`. Ignoring the reserve penalty, its action difference is `.196R-.063`, positive above `R≈.3214`. The reserve term further depends on the cell's energy and on clipping. `NEXT_CREDIT_ECO_probe.py` computes the exact shaped counterfactual action advantage by evaluating **both** current-state actions. This immediate-shaped advantage can remain *positive* even when the long-run ecology runs a negative raw energy budget.

## Loop 1 — Is update-induced overharvesting phase-dependent?

Twelve new matched trained seeds 10080–10091, grid 10×10, 1000 baseline training ticks. Each pretrained threshold vector is placed into **identical new test worlds and identical RNG streams**, differing only in `learning=True` or `False`; both act stochastically. Test ticks1–1000 have regrowth `.06`, ticks1001–2000 have deliberately altered regrowth `.055`, and ticks2001–3000 return to `.06`. The changed regrowth is a **labeled world-law intervention**. All other physics are unchanged.

| Phase / window | Online harvest fraction | Frozen harvest fraction | Online resource per harvest | Frozen yield | Raw drift online | Raw drift frozen |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline t1–1000 | .4165 | .4059 | .4504 | .4574 | −.001370 | −.001160 |
| Early scarcity t1001–1200 | .4161 | .3954 | .4264 | .4406 | **−.003851** | −.003351 |
| Late scarcity t1201–2000 | .4151 | .3965 | .4272 | .4396 | −.003810 | −.003405 |
| Early recovery t2001–2200 | .4357 | .4169 | .4372 | .4484 | −.001825 | −.001522 |
| Late recovery t2201–3000 | .4402 | .4176 | .4354 | .4484 | −.001813 | −.001496 |

Across all windows, online updates harvested *more often* while obtaining *less resource per harvest*, and their raw budget was more negative. The relative harvest increase was already present before scarcity (about +1.1 percentage points), grew during its onset (+2.1), and reached +2.3 points late in recovery. Thus **scarcity amplified an existing drift**; it did not suddenly create it.

The online cell's mean bias parameter exceeded its frozen matched value by about `+.045` in baseline and `+.110` late in recovery. Its mean personal-energy coefficient became more negative (online `−.267` versus frozen `−.162` late), consistent with increased low-energy harvesting urgency. Resource–action covariance relative to frozen was usually lower during baseline/scarcity, though by late recovery it became slightly higher; increased action quantity and depleted resources remain important. The average exact shaped immediate action advantage remained positive (~`.029` to `.033`) while the ecological raw energy budget was strongly negative.

At tick3000, mean online-minus-frozen energy was **−.01122**, with **0/12 seed wins**. These observational mediators are consistent with harmful overextraction, but trajectories diverge after updating begins; covariance and coefficient correlations alone are **not a randomized causal decomposition**.

## Loop 2 — Which updates are causally contributing?

We ran a separate 12-seed trial (10180–10191), same original trained policy, stochastic action mode, initial physical state and RNG, same mild three-phase regrowth schedule. Every arm receives the original learning algorithm. A controlled intervention restores **one** class of weight coefficients after each update; comparator freezes all updates. Other traces/baselines remain active, so these are bounded update-component interventions rather than a mathematical gradient decomposition.

| Intervention | Final mean energy | Cells at floor | Harvest rate last 500 | Raw budget last 500 |
| --- | ---: | ---: | ---: | ---: |
| All online updates | .03676 | 20.42% | .44258 | −.001851 |
| **Freeze all updates** | **.04920** | **15.75%** | **.41670** | −.001473 |
| Freeze energy-input updates only | .03998 | 19.08% | .43145 | −.001650 |
| Freeze bias updates only | .03819 | 20.42% | .43598 | −.001717 |
| Freeze resource-input updates only | .03685 | 20.42% | .44229 | −.001843 |

Freezing energy-input updates improved energy relative to full online by **+.00322** (11/12 seeds). Freezing bias updates improved it by **+.00143** (9/12 seeds). Blocking resource-input updates had almost no average effect (~+.00009, 6/12 paired wins). Freezing *all* updates still performed best. This gives **causal experimental support** that energy-weight and bias updates contribute to the harmful drift *in this selected learner*, but their effects interact and neither individual ablation rescues the ecology.

## What FRR changed in our understanding

Our previous intuition was simply that online learning may encourage excessive harvesting. Here we can articulate the missing relationship more sharply:

1. The learner optimizes **an immediate shaped reward**, not the global finite-horizon resource–energy budget.
2. Continuing updates shifts its energy coefficient/bias and increases stochastic harvesting, even when each harvest has lower expected local resource yield.
3. Changing environmental resource regeneration makes the energy budget more negative while the reward's immediate action advantage remains positive.
4. Temporarily blocking the learned energy-input update or bias update reduces overharvesting and improves energy modestly, so those parameter changes are implicated—not merely random exploration.

The resulting hypothesis is narrower and testable: **in this simulator, low-energy urgency coupled to myopic shaped reinforcement can create an over-extraction feedback loop**. It is not a universal diagnosis of reinforcement learning, nor proof that the neural system has self-preservation intentions.

## Next discriminating experiment

Predeclare an alternative policy update that uses the **exact raw global resource/energy budget** as a *diagnostic gate*, e.g. defer harmful updates when the tail raw budget is negative, then compare it with a sham gate and unchanged learner on untouched seeds under identical stochastic action selection. This gate would be explicitly designer-imposed and would test the mechanism—not demonstrate autonomous discovery. A second, harder goal is to learn long-horizon credit assignment without hand-gating the solution. Preserve energy-floor rate and resource yield per harvest as primary metrics; do not optimize only average energy.
