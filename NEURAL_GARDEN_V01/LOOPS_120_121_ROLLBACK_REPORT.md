# Protected-policy rollback: research loops 120–121

Status: Two research hypotheses tested, not 50. November 11, 2026. Synthetic runs only; the canonical tick-100 Living Garden was not touched.

Standalone replication of WelfareGarden three-feature equations. Twelve paired seeds 12100–12111, 10x10 cells, 800 training ticks at regrowth 0.06, then 1,800 deployment ticks, 0.06 / 0.055 / 0.06 by thirds. All arms start with the same trained weights, energy, resource and state. Every arm uses the same uniform random draws per seed and tick, though different action probabilities yield different actions. Welfare is mean energy minus 0.5 times the fraction energy <=0.01. These are exploratory, not preregistered.

## Loop 120: Is ecological feedback triggered rollback beneficial?

| Arm | Final energy | Floor share | Welfare | Restores / 18 |
|---|---:|---:|---:|---:|
| Frozen | .051392 | .121667 | -.009441 | 0 |
| Online updates | .040283 | .147500 | -.033467 | 0 |
| Drift-triggered rollback | .051259 | .118333 | -.007908 | 18 |
| Half-rate schedule sham | .051281 | .137500 | -.017469 | 9 |

Drift trigger: every 100 ticks, restore trained weights and clear reward traces/baseline if 100-tick average RAW energy budget < -0.001. This rule was designed, not learned. It restored at all 18 windows. Therefore comparison against half-rate sham does not isolate feedback specificity; rates differ. Protected beat online on 10/12 matched seeds by welfare, but frozen on only 7/12.

## Loop 121: Does feedback add anything beyond periodic resets?

Replace the half-rate sham with restoring at every 100-tick boundary regardless of feedback. Outcomes of the drift-triggered arm and unconditional sham are EXACTLY IDENTICAL on all 12 matched seeds, including energy, floor, welfare and tail raw energy drift. Both restored all 18 times.

**Falsified for this regimen:** apparent protected-memory benefit is not due to successful identification of harmful updates. The rule collapses to unconditional resets under persistent negative raw energy drift. In-window updates and trace resets also distinguish both from a permanently frozen learner.

## Next pressure

Use independent new seeds, a changed schedule, and a decision signal that actually accepts some and rejects other candidate updates. Count-match rollback and update frequency, compare stronger fixed-rule baselines, and separately evaluate candidate-policy competence and whole-ecosystem welfare. Do not claim autonomous meta-learning.

Exact standalone Python and per-seed JSON were generated in the ChatGPT runtime as LOOP120.py / LOOP121.py and LOOP120_results.json / LOOP121_results.json. Those files are not committed by this report and must not be mistaken for branch-hosted raw artifacts. Code uses an independent recreation of recorded WelfareGarden equations, not an import of the repo module.

Accounting: documented completed loops 120–121. Cumulative 121. 48 of the newest 50 authorization remain unexecuted. Original 200-loop tranche has 178 remaining. No continuous background execution.