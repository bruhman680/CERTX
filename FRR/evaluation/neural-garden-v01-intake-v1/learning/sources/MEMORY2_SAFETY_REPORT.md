# Safety-constrained memory consolidation: independent cohort replication

**Research loop:** one new substantive, predeclared replication and mechanism stress test with six entirely new training cohorts (`11200–11205`), independently selected checkpoints and held-out worlds. Full disaggregated outcomes `MEMORY2_SAFETY_results.json`, predeclared `MEMORY2_SAFETY_PLAN.md`. Synthetic environmental laws remain unchanged.

## Final scores on previously untouched held-out worlds

| Regime | Protected bank | Blind latest | Original composite gate | Safety-constrained gate |
| --- | ---: | ---: | ---: | ---: |
| Stable | **.68574** | .68510 | **.70666** | **.70274** |
| Mild shift | **.14868** | .00408 | **.14990** | **.14347** |

Score=`mean energy - .5 * fraction depleted`, 12 held-out deployment trajectories per regime (two worlds per training cohort). The original gate's stable advantage came from **one of six training cohorts**; none of the other five gained. In mild shifts, original gate won in **one of six**, while safety gate won in **zero of six**. Blind latest won mild in **zero of six**. These are not powerful significance estimates: `n=6` independent cohort units.

The floor-sensitive gate required validation depleted-cell fraction no more than `protected+0.01` **under both stable and mild validation laws**. Nevertheless, stable held-out floor rose from 2.08% to 2.21%, and mild held-out floor rose from 15.10% to **16.67%**. So the threshold did **not** transfer as a safety guarantee. The original composite gate's mild held-out floor was 16.28%.

## Adjudication

1. **Preserved:** Keeping a protected neural-policy bank prevents the severe harm observed from blindly replacing it with the latest online-updated policy in mildly shifted worlds.
2. **Not replicated robustly:** The larger mild composite improvement observed in `MEMORY2_REPORT.md` mostly vanished under new training cohorts; original validation selection produced only `.00122` additional held-out score over protected, and safety constraint slightly worsened it.
3. **Falsified for this implementation:** Validation depletion constraints do not bound unseen-world depletion; a safety gate is not a reliable adaptive welfare regulator here.
4. **Open:** An inexpensive local critic or contextual confidence mechanism might do better, but no evidence from these experiments supports that yet. Mechanistic follow-up should examine forecast calibration, avoiding ever equating a designer validation gate with the cell's own learned confidence.

No canonical Living Garden checkpoint was modified. Source and output retain independent seeds and entire individual outcome lineage.
