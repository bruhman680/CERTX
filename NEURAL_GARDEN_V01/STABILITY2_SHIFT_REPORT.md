# STABILITY2_SHIFT — abundance masks scarcity

**Evidence:** One new, separate predeclared research loop. Matched stochastic neural policies were evaluated under a rich–scarce–rich regrowth schedule. Initial conditions and action RNG identical within each seed. Eight development seeds 10500–10507, eight untouched holdout seeds 10600–10607; 10×10 cells, 1000 pretrain ticks, 3000 test ticks. **80 seeded policy trajectories** (five arms ×16 seeds); smoke runs excluded. Raw JSON stores each individual world, phase boundary, source SHA and summary.

| Policy | Development final energy | Holdout final energy | Holdout mean during scarcity | Holdout wins vs frozen (final) |
|:--|--:|--:|--:|--:|
| Frozen stochastic pretrained | .98029 | .98072 | .04783 | — |
| Unrestricted online | .98247 | .98159 | .04689 | 7/8 |
| Online radius .025 | .98044 | .98120 | .04772 | 6/8 |
| Online radius .10 | .98079 | .98159 | .04733 | 7/8 |
| Shuffled-gradient sham radius .10 | .98033 | .98166 | .04733 | 7/8 |

**Interpretive trap:** All five policies finish near the energy ceiling under strong recovered regrowth `.09`; the middle third's `.03` shock drives all policies near `.047` mean energy. Unrestricted online modestly exceeds frozen final energy in 7/8 heldout seeds, but its **average energy through the scarcity interval is lower than frozen**. The shuffled-gradient sham has slightly *higher* heldout final energy than the real radius-.10 local gradient and the **same** average scarcity energy to five significant figures. Thus the final endpoint advantage is not good evidence of useful learned adaptation: ceiling recovery and a direction-corrupting sham erase specificity.

This tests a different synthetic regime from STABILITY2, whose mild-shift 16-seed result found bounded updates prevented much harm but never surpassed freezing. The two results are compatible: apparent winners depend on the regime, phase, and metric, and rich-world ceilings conceal history. Next studies should prioritize *area under energy trajectory, time spent energy-starved, recovery time after shock* and a fixed-scarce comparator, not final state alone.

No autonomous confidence monitor or self-directed learning schedule was implemented. The shuffled-gradient control disrupts per-cell credit assignment but does not exactly equalize trajectories or downstream update magnitudes, so a nominal win over it alone would not prove credit assignment.
