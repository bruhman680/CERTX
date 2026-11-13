# Independent reserved-seed audit: online policy updates versus frozen stochastic controller

**Result:** Online policy updates **harmed** the selected ecology relative to the exact trained, frozen stochastic controller on all 12 reserved audit seeds at tick3000. This is a within-simulator negative result, not a general claim that online learning is harmful.

The protocol (`NEXT_ONLINE_AUDIT_PLAN.md`) was frozen before observing the audit results. Source `NEXT_ONLINE_probe.py` was frozen by the welfare society before the separate audit seeds9800–9811 were evaluated. Audit code `NEXT_ONLINE_AUDIT_run.py` simply invoked the original protocol on those reserved seeds. Raw full rows and pretrained/frozen theta evaluations are in `NEXT_ONLINE_AUDIT_results.json`.

## Primary matched stochastic-policy comparison at test tick3000

| Metric | Online updating | Frozen learned weights | Paired online−frozen |
| --- | ---: | ---: | ---: |
| Mean cell energy | **.03609** | **.04889** | **−.01280** (seed SD .00442) |
| Cells at energy floor ≤.01 | **20.83%** | **17.33%** | **+3.50 percentage points** |
| Mean resource | .42395 | .44035 | −.01640 |
| Harvest rate at final tick | .43833 | .42167 | +.01667 |
| Mean raw energy drift (last 500 ticks) | −.001828 | −.001464 | −.000365 |
| Learned mean energy-feature coefficient | −.27952 | −.15394 | Difference associated with updates |

**All 12 held-out seed-paired energy differences were negative for online updates.** This meets the declared burden of comparing different update settings with the same initial physical state, trained theta, RNG stream and *stochastic* action-selection mode. Future action trajectories can diverge because learned propensities diverge; forcing actions to stay identical would suppress ecological consequences of policy learning.

After completing the reserved-seed audit, we inspected the independently executed main-study summary. Its disjoint twelve seeds9600–9611 also showed online updating worse than frozen stochastic controls (**mean difference −.01504, zero of twelve paired seed wins**). The independent audit's own difference was −.01280, zero of twelve wins. This agreement was checked *after* the audit run and did not influence the frozen test design or parameter choices. Together these are 24 within-generator seed runs across two predeclared cohorts, not twenty-four unrelated scientific replications.

The welfare objective `reserve_resource` with penalty .3 was explicitly designer-chosen using earlier experiments. During test, the world had baseline regrowth .06 for ticks1–1000, altered regrowth .055 for ticks1001–2000, and restored baseline for ticks2001–3000. The objective included reward terms for near-low energy and resource change. No unambiguous adaptive resilience emerged from continuing those updates on this schedule.

## Secondary deterministic frozen-theta diagnostics

To separate stochastic action costs from learned-policy competence, snapshots of each arm's theta at checkpoints 0,1000,2000,3000 were deployed as **frozen deterministic** controllers in entirely separate but matched test worlds under stable and mild regrowth. Each comparison used identical new initial worlds for online-derived versus frozen-derived theta. These diagnostic worlds do *not* establish uninterrupted online ecological survival.

| Theta checkpoint | Stable: online-derived − frozen-derived energy | Mild: online-derived − frozen-derived energy |
| ---: | ---: | ---: |
| 0 | 0 (exact weight equality) | 0 (exact weight equality) |
| 1000 | **+.00791** (8/12 seed wins) | **−.06293** (0/12 wins) |
| 2000 | **−.05002** (1/12 wins) | **−.11313** (0/12 wins) |
| 3000 | **−.13063** (0/12 wins) | **−.17253** (0/12 wins) |

This suggests a temporary stable-world improvement at an early checkpoint, followed by deterioration of transferable deterministic behavior as updates continued through scarcity. A plausible diagnostic mechanism is stronger low-energy urgency and higher harvest rates driving resource extraction, but the coefficient correlation is not by itself proof of that mechanism. The paired regime and theta evidence justify a new policy-gradient/eligibility causal ablation rather than a premature explanation.

## Verification and limitations

1. **PASS:** Twelve distinct reserved seeds, disjoint from the main 9600–9611 seeds; four theta checkpoints ×two evaluation regimes ×two arms yield **96 paired checkpoint/regime comparisons** (192 separate arm evaluations) across the twelve seeds. All twelve pairs began with exactly equal physical state, trained theta and RNG stream.
2. **PASS:** SHA-256 source hashes for `garden.py`, `NEXT_WELFARE_*`, both `NEXT_ONLINE` plans and scripts were checked against the executed local bytes. The frozen audit plan's checksum matches.
3. **PASS:** `next_online` executed without source or policy edits; no outcome-based retuning or cherry-picking. No cell-level pseudo-replication (seed is paired replication unit).
4. **LIMIT:** The reserve/resource reward was hand-chosen; it is not evidence of spontaneous normative preference. The study only tests one chosen objective and one moderate, finite-duration regrowth dip, across one synthetic world generator and size10.
5. **LIMIT:** A later change in stochastic action trajectory is an expected consequence of parameter updates; identical initial RNG does not imply identical realized actions for all time. Replaying identical actions while updating weights would test another mechanism, not the ecological consequences of a changed policy.
6. **LIMIT:** Energy is clipped at zero/one; report floor fraction and raw preclipping drift. Neither low mean energy nor flat observed energy at the floor imply stable equilibrium.

**Research-loop conclusion:** Under this specified learned reward and regime, online updating was worse than simply using the trained policy without further updates; even the trained controller itself was poor in absolute ecological energy. The next worthwhile question is how to train with delayed consequences and explicit external state without causing harmful overharvesting, using strong fixed and deterministic controls. This independent audit counts as **one substantive research loop**, supported by 12 fresh paired simulations and their nested policy-transfer evaluations.
