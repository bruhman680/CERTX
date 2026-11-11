# Exact-state intervention timing: repaired causal comparison

**Executed** after the seasonal report identified an unidentifiable early-switch comparison. Frozen `SEASONS2_SWITCH_PLAN.md`, 12 independent held-aside seeds, two fork times (after t3000 and t9000 scarcity), two policies from **identical arrays** at each fork, 3,000 subsequent normal regrowth ticks. Per-seed results and source hashes in `SEASONS2_SWITCH_results.json`.

## Loop S6 — Does emergency reverse-rescue improve recovery relative to fixed threshold when the starting state is exactly equal?

At t3000, mean starting energy **.01996**; after 3k normal ticks fixed `.51` reaches **.09686** mean energy, emergency reverse `.04726`. Reverse minus fixed is **−.04960**; reverse loses energy in **12/12** matched seeds, while reducing depleted fraction from **8.53%** to **5.47%**. The threshold difference activates on ~22.18% of cell–ticks of the *reverse-policy trajectory*, so this is an active treatment, unlike the earlier pre-scarcity equality.

At t9000, corresponding post-scarcity starting energy **.01963**; fixed reaches **.09552**, reverse **.04654** (difference **−.04898**, fixed wins all 12 seeds); reverse again reduces depleted fraction (fixed **8.76%**, reverse **6.48%**).

**Interpretation:** Policy acts as a genuine mean-energy vs depletion-floor tradeoff, not a clear net welfare win. The replicated sign across two matched intervention points supports context-specific causal comparison, but this hand rule is not an online neural learner and horizons are finite. The parent environmental regrowth schedules and histories differ before t3000 vs t9000, so comparing these times does not isolate history as a single parameter.
