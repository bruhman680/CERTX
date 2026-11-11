# Resource timing, near-neutral thresholds, and diffusion: a dynamical research loop

**Status:** Analytic identity plus three *posthoc* controlled simulator probes. These experiments are intentionally separate from the preregistered-style 1,000-run matched policy comparison. The observations concern an artificial model, not biological ecology, intelligence, or infinite-time survival.

## 1. Why the early .55 threshold story changed

The prior .55 fixed-harvest rule retained high mean energy near tick 600, but its mean declined toward .269 by tick 2,000. Our new 8-seed, 5,000-tick probe found final mean energy **.0361** and average **raw, pre-clipping** energy drift −.0001526/tick in the last 1,500 ticks. Another 8-seed, 20,000-tick probe found .0354 and −.0001516/tick over its final 5,000 ticks. Thus .55 is not a stable high-energy long-horizon strategy in these conditions. A positive instantaneous drift at one earlier tick was misleading.

## 2. Exact global resource accounting, not just a mean-field guess

Let `R` be per-cell local resource *before* a synchronous step, `A` the binary harvest action, and angle brackets `⟨...⟩` denote means over all 256 cells (or over a subsequent time window). Under the original v0.1 laws:

`R' - R = .08*(neighbor_mean(R)-R) + .06*(1-R) - .18*R*A`.

The toroidal four-neighbor diffusion term **sums to zero exactly** across the grid; resource clipping is inactive for these admissible states and coefficients. Therefore

`⟨ΔR⟩ = .06*(1-⟨R⟩) - .18*⟨R*A⟩`.

The raw energy budget is exactly

`⟨ΔE_raw⟩ = .25*⟨R*A⟩ - .063*⟨A⟩ - .022`.

If the resource field is stationary *in time average*, `⟨ΔR⟩≈0`, substitution yields

`⟨ΔE_raw⟩ ≈ (1/12)*(1-⟨R⟩) - .063*⟨A⟩ - .022`.

These identities are about **unclipped energy**. Stored energy is capped in [0,1], so neither a zero net observed change at the floor nor a near-zero raw mean is a proof that every cell survives or the policy is globally stable. The numerical probe computes both balance residuals; errors are near floating-point rounding (<1e-17 per step on relevant identities).

## 3. New threshold screen: a near-neutral corridor

**Posthoc threshold choices:** `.45, .50, .525, .55, .575, .60`; 8 fresh seeds each (`930..937`), original world, 16×16 grid, 5,000 ticks, final 1,500-tick averages. All **48 individual simulations** and trajectories are stored in `DYNAMICS_results.json` from `DYNAMICS_probe.py`.

| Threshold | Final mean energy at t5,000 | Tail raw energy drift per tick | Tail harvest fraction |
| ---: | ---: | ---: | ---: |
| .45 | .02493 | −.00055709 | .40000 |
| **.50** | **.66879** | **+.00001555** | .33333 |
| .525 | .56461 | −.00000545 | .31069 |
| .55 | .03607 | −.00015262 | .28295 |
| .575 | .02973 | −.00057744 | .25000 |
| .60 | .02849 | −.00082271 | .23808 |

The response is strongly nonmonotonic and apparently discontinuous-looking at tested thresholds, consistent with recharge/harvest timing changes. This is *candidate discovery*, not a proven optimum or a universal near-critical law.

## 4. Independent longer-horizon check

We froze three candidates `.50,.525,.55` after the exploratory scan and ran **24 additional simulations** (8 fresh seeds `950..957`, 20,000 ticks). Data: `DYNAMICS_followup_results.json`, script `DYNAMICS_followup.py`.

| Threshold | Final mean energy t20,000 | Tail raw drift/tick | Average fraction at energy floor in final 5,000 ticks |
| ---: | ---: | ---: | ---: |
| **.50** | **.65656** | **+.00001624** | **.05338** |
| .525 | .47581 | −.00000571 | .0000083 |
| .55 | .03539 | −.00015163 | .15101 |

The `.50` threshold retains high **mean** energy and small positive raw drift over this horizon, but **some cells still reach the energy floor**. This is therefore neither all-cell sustainability nor mathematical proof of indefinite viability. The `.525` threshold is near-neutral by raw drift and retains energy in this finite window, with almost no floor occupancy. We should not select either candidate as the final Garden policy without a separate untouched validation set and perturbation tests.

## 5. A mechanism: a three-tick recharge–harvest cycle

With diffusion disabled, a single isolated cell obeys two affine resource maps:

- Rest: `f_0(r)=.94r+.06`.
- Harvest: `f_1(r)=.76r+.06`.

For a repeating pattern of **harvest, rest, rest**, the high resource just before harvest must solve `r_high=f_0(f_0(f_1(r_high)))`, yielding the exact candidate

`r_high = (.06*.94^2 + .06*(1+.94)) / (1-.76*.94^2) = .5157825515`.

The two intermediate resource levels are approximately `.4519947391` and `.4848750548`. They satisfy threshold `.50`: only the high state triggers a harvest. Its average raw energy drift is

`(.25*r_high - .085 - 2*.022)/3 = −.0000181207` per tick.

This very slightly negative isolated-cell budget contrasts with the **slightly positive** drift observed in the interacting spatial world. It suggests diffusion and phase relationships may alter resource availability at the moment of harvest.

## 6. Diffusion ablation: controlled mechanistic contact

At a frozen `.50` threshold, compared diffusion coefficient **0.00** versus original **0.08**, 12 fresh matched seeds `980..991`, 10,000 ticks and final 2,000-step drift averages (`DYNAMICS_diffusion.py`, `DYNAMICS_diffusion_results.json`). Note this is a deliberate **world-law intervention**, not a fair comparison of neural intelligence.

| Diffusion | Mean raw tail energy drift | Final mean energy | Final energy-floor fraction |
| ---: | ---: | ---: | ---: |
| 0.00 | −.00001739 | .42190 | 0.0 |
| **0.08** | **+.00001723** | **.67580** | .00651 |

The isolated population's negative drift closely matches the analytical three-cycle prediction. Restoring neighbor exchange changes the collective mean drift sign. This supports the mechanistic hypothesis that **spatial coupling changes harvesting phase and action–resource alignment**, even without neural learning. Yet the effect is tiny and likely sensitive to coefficients, thresholds, horizon, heterogeneity, and boundary rules. A positive average drift can coexist with a minority of energy-depleted cells.

### Phase diagnostic: the interharvest period did *not* change

A further 16-run probe (`DYNAMICS_phase.py`, `DYNAMICS_phase_results.json`) used 8 fresh seeds per diffusion condition, observed 2,000 late ticks, and counted the interval between each cell's harvests. **Every recorded interval was exactly three ticks**, with and without diffusion. Thus the hypothesis that a change in the *frequency* of harvesting caused the improvement was not supported in this regime.

However, mean **resource at the harvest moment** increased from `.5157825515` (no diffusion; exact homogeneous three-cycle high state) to `.5161932645` (diffusion .08). With ~1/3 harvests per tick, the predicted extra raw drift is approximately `.25*(.5161932645−.5157825515)/3 ≈ +.00003423/tick`, matching the observed tail-drift difference of about `+.00003462/tick` in the independent diffusion ablation.

The refined explanation is therefore **not** that diffusion causes more frequent harvesting. It is that spatial exchange changes the *amount of resource present at the fixed three-tick harvest moment* by a very small but consequential quantity. Neighbor phases and heterogeneous resource levels likely matter; isolating that causal detail requires a separate phase-pattern counterfactual. This refinement is more informative than simply saying coupling improves outcomes.

## 7. Research-loop accounting and next discrimination

Completed four substantive evidence-bearing movements: (A) exact resource-energy accounting plus 5k candidate sweep; (B) 20k fresh-seed follow-up and floor occupancy; (C) analytic three-cycle prediction followed by diffusion on/off ablation; (D) phase diagnostic contradicting the harvest-frequency hypothesis and refining it to harvest-resource amplitude. Simulation counts: **48+24+24+16=112 exploratory runs** in these four loops, not 112 conceptual research loops.

Promising next test: examine phase-locking and resource-action covariance **at the cell level** under controlled diffusion strengths and uneven topology, and perturb world-law coefficients in a separate labeled robustness study. More importantly, test whether a *learned* local neural controller can exploit this dynamic relationship on a held-out world rather than simply imitating a hand-coded threshold.
