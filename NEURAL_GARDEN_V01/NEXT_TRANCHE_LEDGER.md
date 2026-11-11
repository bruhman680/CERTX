# Next Garden tranche — adjudicated research loops 070–099

**Accounting:** From prior 69 documented loops, this turn's six societies completed **30 distinct evidence-backed research loops**, recorded as 070–099. The user authorized **the next 200** within the overall 2,000-loop program; **170 of that tranche remain authorized but not executed**. This is not a claim of 200 completed loops. The many thousands of ticks, hundreds of simulations and optimizer changes inside each investigation are not separately counted. Numbering is thematic rather than chronological because societies worked concurrently.

Each line records a question, actual discriminating probe and observed pressure/next direction. See named reports and machine-readable raw outputs for seeds, world laws, source hashes, evaluation windows and independent audit. Negative results are retained as findings.

| Loop | Investigated burden | Probe → measured consequence / next pressure |
| ---: | --- | --- |
| 070 | Does designer reward shaping improve ecological policy learning? | `NEXT_WELFARE_REPORT.md`: four explicit objectives evaluated on matched fresh worlds; resource shaping was selected during development, but online performance remains poor. |
| 071 | Does resource-shaped **online** learning beat its own trained frozen stochastic copy in mild scarcity? | Online energy .04379, frozen .05480; greater depleted-cell fraction online. Question turns to policy-update causality. |
| 072 | Does the same online failure persist under stable conditions? | Stable online .04262, frozen .05394; fixed .50 .6449. Not merely caused by environmental shift. |
| 073 | Can shaped policy weights be useful when deployed deterministically? | Frozen deterministic reserve-trained policy stable .71390 vs neighbor manual .65930, but reserve has 2.33% floor vs manual zero; mild combined reward .26218 vs reverse rule .27764. Useful weight learning but no superior online adaptation. |
| 074 | Is aggregate energy sufficient to rank ecological health? | `NEXT_WELFARE_pareto.py`: stable reserve-neural and neighbor-manual form competing energy/floor Pareto choices; mild reverse-manual dominates examined policies on both aggregates. |
| 075 | Does spatial action targeting matter with exactly matched action counts? | `NEXT_ECO_REPORT.md`: top/current resource .679 energy vs random .116 and bottom-resource .144. Counts matched, placement changes outcome. |
| 076 | Is resource diffusion causally involved in retention? | Explicit no-diffusion law ablation reduces rescue energy ~.679→.462, reverses tiny raw tail sign. Spatial coupling consequential. |
| 077 | Does one- or two-step stale observation harm policy placement? | Naive lag targeting falls to .044/.053, but action counts change; demanded rate-matched control. |
| 078 | Does observation freshness matter independently of harvesting frequency? | Exactly per-tick matched-count ranking by current resources .679 vs one-tick stale .045 and two-tick stale .068, 8/8 paired wins. |
| 079 | Which welfare policy protects low-energy cells, not just average energy? | Neighbor-gradient maximizes mean in tested set; rescue protects bottom decile and shows no floor. Different welfare objectives. |
| 080 | Does timing of a manual rescue matter in the same historical neural world? | `NEXT_LIVING_REPORT.md`: early intervention retains far more than late intervention; 12 fresh seed replication early ~.301 vs late ~.026. |
| 081 | Can a depleted world recover with explicit external aid? | Exact forks: at late switch, resource doubling or energy replenishment each help; combined mean energy ~.539 vs unaided ~.025. External rescue ≠ autonomous recovery. |
| 082 | Does returning to historical neural weights restore learned ecological competence? | After manual policy then stale original neural control, energy collapses; restoring/resetting dormant recurrent state has little impact. Not a test of uninterrupted online plasticity. |
| 083 | Is the canonical Living Garden history intact across controlled forks? | Exact tick100 full-state fingerprint and event-log checks pass; master remains paused, experimental results arise from copies. |
| 084 | Does compressed three-state history repair prediction under resource shift? | `NEXT_MEMORY_REPORT.md`: three coarse labels NLL .641→.141 with three prior states; temporal phase informative. |
| 085 | Is history's learned predictive structure invariant under changed laws? | Stable-trained history predictor NLL spikes ~.0066 before→1.363 during shift; memory not universal robustness. |
| 086 | Does acquired-threshold inheritance produce meaningful child behavior changes? | Mechanics work, but first-birth propensity impact averages only ~.00102 across standardized cases. Transmission ≠ adaptive benefit. |
| 087 | Does an independent exact-policy benchmark reproduce baseline rankings? | `NEXT_AUDIT_REPORT.md`: 168 matched t4000 trajectories; mild reverse rescue .290 > frozen learned energy-aware .148 > fixed .50 .057; formulas verified. |
| 088 | Does a *predeclared* multiworld and multisize evaluation reverse winners? | `NEXT_BENCHMARK_REPORT.md`: 288 t6000 trajectories across 4 regimes/3 sizes: stable fixed/gradient ~.679/.681, mild reverse rescue ~.342 vs early rescue ~.026; rank depends on world. |
| 089 | Do high-energy neural policies dominate strong manual rules on distributional welfare? | `NEXT_WELFARE_AUDIT.md`: 64 fresh long-horizon trajectories show reserve-trained neural mean can beat manual neighbor at 8k, yet bottom-decile/raw drift poorer; horizon reverses prior mild comparison. |
| 090 | Does online updating itself harm ecology when action selection is matched? | `NEXT_ONLINE_REPORT.md`: online stochastic .03778 vs trained frozen stochastic .05283 across 12 seeds, 0/12 wins; no deterministic/stochastic confound in primary comparison. |
| 091 | Do online-updated weights degrade downstream deterministic competence? | Checkpointed frozen-weight transfers stable .68084→.54951 and mild .22498→.04455 by t3000 compared to unchanged trained weights; learning update burden isolated. |
| 092 | Does independent reserved-seed replication support online degradation? | `NEXT_ONLINE_AUDIT_REPORT.md`: 12 untouched seeds online .03609 vs frozen .04889, 0/12 wins, consistent with first cohort (24/24 paired signs). |
| 093 | Is clipped reward hiding damage compared with raw reward? | `NEXT_CREDIT_REPORT.md`: contrary to conjecture, clipped-reward online .04241 > raw .03695 in main 12 seeds, but frozen still better. |
| 094 | Does delayed-credit trace horizon fix policy failure? | Trace .70 collapses to .01758, .995 creates high mean .217 but **43.75% floor** and negative raw drift; longer memory isn't sufficient. |
| 095 | Does faster reward baseline adaptation repair learning? | Fast baseline .04129 modestly above raw .03695, still below frozen .04888/manual reverse .27885; outcome selection qualified. |
| 096 | Why does online updating reduce energy? | `NEXT_CREDIT_ECO_REPORT.md`: online harvest increases +1.1–2.3 percentage points while resource yield declines. Exact budget `E[ΔE_raw]=p(.25 y−.063)−.022`, so target yield must exceed `.252+.088/p`; online drift worsens. |
| 097 | Which neural component updates contribute to harmful overharvesting? | Matched selective freezes: block energy input updates improves .03676→.03998 (11/12 wins), block bias .03819 (9/12), block resource weight nearly null; all-update freeze still best .04920. |
| 098 | Does credit-fix benefit survive long, untouched independent worlds? | `NEXT_CREDIT_AUDIT_REPORT.md`: 8 unseen seeds×stable/mild 8k; fast baseline modest vs raw but **both** online arms worse than frozen in every seed. Manual reverse/neighbor much healthier; selection caveat logged. |
| 099 | Does pausing weight updates **specifically during scarcity** beat an equal-duration sham pause? | `NEXT_GATE_REPORT.md` and `NEXT_GATE_AUDIT_REPORT.md`: scarcity pause .03784 vs early sham .03980 in independent seeds (1/12 wins), frozen all .04924; designer-supplied update gating failed. |

## Strongest revised interpretation

1. **The cells learn useful functions, but our tested online policy-gradient updates are ecologically harmful under the chosen reward/environment.** This is supported by matched stochastic action mode, deterministic frozen-weight diagnostic and independent seed replication—not a claim about all neural learning.
2. **Targeting and freshness are causal within these synthetic laws.** Holding harvest count exactly fixed while changing where/when actions occur transforms resource yield and energy retention.
3. **Welfare is multidimensional.** Reserve-trained neural agents may have higher mean energy while leaving worse lower-decile/floor outcomes or negative raw tail drift; no unique scalar optimum has been established.
4. **A pause is not automatically a repair.** Timing-specific update gates did not outperform an equal-budget sham; future work must improve the objective/credit mechanism itself or learn update regulation.
5. **Compression/history and inheritance remain separate inquiries.** History predicts phase but loses calibration in a changed world; transmitted acquired threshold adjustments are too small to establish a fitness benefit.

**Next authorization status:** cumulative documented loops **99 / 2,000**. In the newly authorized 200-loop tranche, **30 completed, 170 remain available**. No background work is implied after the live tool session ends. The historical 1,550-entry Garden and the canonical Living Garden checkpoint (paused tick100) remain unchanged.
