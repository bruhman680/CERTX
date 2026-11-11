# One Living Garden, seven futures: a controlled 3,000-tick continuation

**Status:** Executed; exact parent tick-100 checkpoint preserved and independently checked unchanged. Script: `LONGITUDINAL_fork_probe.py`; complete measured milestones, event records, fingerprints, platform/source provenance: `LONGITUDINAL_fork_results.json`.

This experiment answers a different question from the multi-seed sweeps. It follows the **same particular Garden** (seed37, 16×16, 256 independently weighted recurrent neural cells), starting at its canonical **tick100** checkpoint. Seven exact copies of that same state each continue to tick3000. The primary world was **not advanced, overwritten, or reset**: it remains safely paused at tick100 for subsequent observation. These seven paths are *matched counterfactual branches of one world*, not independent seed replications.

## Matched branches (all original v0.1 physics)

| Branch | Deliberate alteration | Energy at tick600 | Energy at tick3000 | Cell fraction at energy floor ≤.01, tick3000 |
| --- | --- | ---: | ---: | ---: |
| Original unchanged | Learning remains enabled | .00771 | **.00145** | **94.53%** |
| Freeze neural learning at tick100 | Same initial resource/energy, then no weight updates | .01869 | **.01655** | 51.56% |
| Freeze at tick500 | Learning on until tick500 | .00869 | **.00736** | 72.27% |
| Freeze at tick1000 | Learning on until tick1000 | .00771 | **.00377** | 87.89% |
| Graft non-neural threshold controller at tick100 | Replace action policy with `harvest iff resource>.55` | .10134 | **.03446** | 14.06% |
| Two scarcity shocks | Multiply resources ×.4 after ticks500 and1000; learning stays on | .00794 | **.00146** | 94.53% |
| One resource rescue | Multiply resources ×1.5 after tick500 (capped at 1); learning stays on | .00755 | **.00142** | 94.53% |

At tick100, before any forked intervention, this particular world had mean energy .24244, mean resource .36853 and 2.73% of cells near the energy floor. By tick200, unchanged learned energy had fallen to .01942 and approximately 50.8% of cells were at the floor. This early collapse is the dominant dynamic within this one seed and world-law choice.

## Findings that survived several passes

1. **The baseline is not ecologically viable over this measured horizon.** With learning enabled, 94.5% of cells have energy ≤.01 by tick3000, and mean energy is .00145. The raw, *pre-clipping*, energy budget over the final 500 ticks still averages −.01195 per step. The near-flat observed energy is therefore a *floor artifact*, not equilibrium.
2. **Freezing learning earlier limits damage in this trajectory.** Freeze at tick100 retains .01655 mean energy at tick3000, later freeze at500 retains .00736, later freeze at1000 retains .00377, and never freezing retains .00145. This monotonic timing pattern is suggestive, but **all values remain low and mean raw energy budget stays negative** (respectively about −.00498, −.00765, −.00936, −.01195 over the final 500 ticks). This does **not** show a sustainable frozen policy or proof that learning universally harms ecological health; it shows damage accumulation here.
3. **An explicit controller graft is a stronger intervention than merely freezing learning.** Replacing the action rule at tick100 with the fixed `.55` threshold preserves .03446 mean energy at tick3000 and only 14.06% energy-floor cells, outperforming both continued learning and freezing weight updates. However this is a **hand-coded transplant of behavior**, not a neural cell discovering the policy. Its energy declines from .10134 at tick600 to .03446 at tick3000, and its last-500-tick raw energy drift is still about −.000163 per tick. It is not an indefinite-health solution.
4. **One-off resource treatment does not repair the policy.** A resource injection at tick500 and two shocks at ticks500/1000 eventually converge back toward the baseline's low-energy region by tick3000. Resource stocks changing temporarily do not, by themselves, teach the cells to harvest conditionally or solve their incentive design.
5. **Exact continuity passed.** The branch states were verified identical before each intervention; uninterrupted 40-tick continuation and a 17-tick + save/load + 23-tick continuation yielded identical full-state fingerprints, including weights and RNG. The original tick100 checkpoint full-state fingerprint matched before and after all seven branches.

## Scope limits

- This is one selected canonical seed and seven dependent forks. It cannot estimate cross-world uncertainty or establish robustness to different initial conditions.
- Changing `.learning` is an explicit intervention. It switches off online updates, not activity, and uses the same environment equations. The fixed-threshold graft deliberately **replaces the neural policy implementation** while retaining state and physics; that branch cannot be interpreted as neural learning. Resource shock and rescue are likewise explicitly external, not adaptive agency or spontaneous healing.
- At a clipped energy floor, cells can still harvest and resource regrowth continues; the model lacks hard death in this version. Interpret "collapse" as depletion of the energy metric, **not biological extinction**.
- These are exact numerical experiments in a toy model. Their discovery significance lies in revealing the priority of **policy objective, timing and longitudinal trajectory**, not a universal law about neural learning.
- Future counterfactual comparisons should add the simple `.55` resource-aware policy and stronger adaptive controllers, but the current canonical learned state is already depleted by tick100; changing policy at that point may be too late without a separately logged rescue or reproduction mechanism.

**Next evidence-seeking loop:** Settle which long-lived world will be the canonical ecological experiment. Keep the saved v0.1 world as a negative reference lineage; create a *separate* more viable policy/world fork for long-term adaptation with a meaningful retained-energy metric and explicit inheritance/recovery hypotheses. Do not silently rewrite or rehabilitate the historical state.
