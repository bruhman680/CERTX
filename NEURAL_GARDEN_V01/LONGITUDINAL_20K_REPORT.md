# Twenty-thousand-tick Garden: narrow harvest-timing window and shock fragility

**Status:** Executed from the same paused canonical Living Garden checkpoint, seed37, 16×16, tick100. Every scenario begins as an *exact copy* of that checkpoint, with matching source and RNG histories until its explicit controller intervention. The parent world is unchanged. See `LONGITUDINAL_20K_probe.py` for the runnable implementation and `LONGITUDINAL_20K_results.json` for per-branch milestones, energy/resource/floor/covariance, tail raw budgets, intervention events and fingerprints.

## Main outcome at tick20,000

| Scenario from one historical world | Mean energy at t20,000 | Fraction at energy floor (≤.01) | Average raw energy drift over final 1,000 ticks |
| --- | ---: | ---: | ---: |
| Original learned neural controller | 0.00019 | 99.22% | −0.015958 |
| Fixed threshold 0.49 grafted at t100 | 0.43858 | 17.19% | +0.0000059 |
| Fixed threshold 0.50 grafted at t100 | **0.45875** | 13.28% | +0.0000052 |
| Fixed threshold 0.51 grafted at t100 | **0.47533** | 12.11% | +0.0000124 |
| Fixed threshold 0.52 grafted at t100 | 0.30409 | 0% | +0.0000059 |
| Fixed threshold 0.53 grafted at t100 | 0.17742 | 3.52% | −0.0000397 |
| Fixed threshold 0.54 grafted at t100 | 0.02377 | 50.39% | −0.0001470 |
| Fixed threshold 0.55 grafted at t100 | 0.03747 | 14.06% | −0.0001509 |
| Threshold 0.50 + resource ×.4 shocks after ticks5,000 and10,000 | 0.02867 | 0% | −0.0000401 |

**Interpretation:** On this single existing world, harvesting above a threshold near **0.49–0.51** maintains far more energy through twenty thousand ticks than the previous `.55` standard. The pattern appears very sensitive around `.52–.54`. This suggests a potential **harvest timing regime boundary**, but it is a *posthoc observed feature of this simulator*, not a demonstrated mathematical bifurcation, universal critical constant, or optimal parameter.

The most revealing trajectory is threshold `.50`: mean energy initially declines from .242 at tick100 to about .203 at tick2000, then climbs to .260 at tick5000, .365 at tick10000, and .459 at tick20000. Its final 1,000-tick raw energy drift is nearly zero and slightly positive. This is evidence of **20,000-tick retention and partial recovery**, not proof of an infinite-time stationary distribution or genuinely learned adaptation. No weights learned this policy: the controller was hand-coded and grafted at tick100.

## Fragility under exogenous disturbances

When the same `.50` graft experiences two large deliberate resource shocks (multiply all available resources by .4 after ticks5,000 and10,000), its t20,000 mean energy is **.0287** rather than .4588. Resources recover under the fixed regrowth law but the population's energy trajectory does not recover to the control level within the observation window. A policy that works over 20,000 quiet ticks may be brittle under shocks. This is the first directly relevant reason for an *adaptive neural policy*: perhaps cells can change harvesting thresholds when world conditions change.

## Evidence and lineage cautions

1. **One seed only.** Nine outcomes are dependent counterfactuals from a single selected historical world. They cannot quantify uncertainty across random initial conditions. The thresholds were selected after observing earlier results, so no independent holdout claim is justified.
2. **Finite-horizon numerics.** Twenty thousand simulation ticks are a long diagnostic relative to earlier 200–2,000 tick tests, but cannot establish indefinite stability. Near-zero tail raw drift may hide oscillations or very slow dynamics; inspect full trajectories, recoveries and resource-action covariance.
3. **No spontaneous policy learning.** Threshold action rules are externally specified and deployed by explicit `__class__` controller substitution on a deep-copied Garden checkpoint. All world resource/energy equations are the original v0.1 laws. Original neural-controller failure remains real for this world but is not a universal verdict against reinforcement learning.
4. **Energy clipping.** `Garden.energy` is bounded [0,1]. Floor occupation is a resource-budget diagnostic, not cell death in this simulator, and zero observed change at the floor is not viability. Raw pre-clipping energy drift is recorded separately.
5. **Preserved anchor.** The source run's full-state fingerprint is verified identical before and after all counterfactuals. No canonical state, archive, or unrelated branch was overwritten.

## Strongest next confidence

Do **not** simply declare `.51` globally best. Freeze a small, preregistered threshold set around `.49–.54`, test on *fresh independent seeds* for 20,000 steps, and test controlled shocks/seasonality at matched seeds. Then attempt to train genuinely action-aware neural cells to learn conditional thresholds without teacher labels and assess transfer to unseen environments. We have evidence of an exploitable resource-timing mechanism, and equally strong evidence that its resilience is not automatic.
