# Independent stress audit — an environmental rank reversal

**One completed substantive research loop** (hypothesis → predeclared design → independent held-out experiment → adversarial interpretation). Source `AUDIT2_probe.py`, numerical rows `AUDIT2_results.json`, plan `AUDIT2_PLAN.md`; original checkpoint untouched.

The earlier claim "frozen trained weights outperform ongoing stochastic updating" was well supported for the tested stable/mild world. Does it survive larger shifts in regrowth? **No as an unconditional claim.** Eight independent held-out seeds per regime (11000–11007), matched initialized physics/action RNG, size10, 1,000 training +3,000 test ticks, resource regrowth fixed at .03/.06/.08:

| Fixed regrowth | Online final energy | Frozen final energy | Online final wins | Online integrated-energy wins | Interpretation |
|---|---:|---:|---:|---:|---|
| .03 severe scarcity | .00510 | .00503 | 5/8 | 2/8 | Both essentially collapse; terminal differences tiny and misleading. Frozen has higher cumulative energy (.01088 vs .01065) and lower average floor occupation (.7848 vs .8011). |
| .06 usual world | .03641 | .05864 | 0/8 | 0/8 | Reproduces strong harm from online updates. Online cumulative energy .10112 vs frozen .12102. |
| .08 abundance | .98177 | .97774 | 8/8 | 8/8 | **Rank reversal**: online updates modestly outperform frozen on clipped energy; both already near the upper-energy ceiling. |

Important adversarial qualification: Under abundance, online actions harvested more (final harvest proportion .5425 vs .4663) and depleted more environmental resources (final resource .4575 vs frozen .4849). Its average final energy advantage is just +.00404 near a ceiling of 1.0, *while frozen had slightly better raw energy drift* over the final 500 ticks (+.00637 vs online +.00603). Thus this does not show that ongoing learning is safer or more sustainable. It shows a valuable outcome-dependent reversal and why resource state, raw drift, and floor/ceiling saturation must accompany mean energy.

The model's learning mechanism is still poor in the reference world. The responsible claim is **regime-dependent online-vs-frozen competence**, not universal failure of online learning or demonstrated self-regulated lifelong adaptation.

Next pressure: test Pareto objectives and capped-energy saturation explicitly; compare online, frozen, and **equal-harvest-budget** policies under change points before attributing any advantage to adaptive control.
