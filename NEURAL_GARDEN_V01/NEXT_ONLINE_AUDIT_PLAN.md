# Independent prospective audit — online learning versus frozen exploration

**Frozen before the audit seeds are evaluated.** This audit follows the parent welfare society's pre-outcome `NEXT_ONLINE_PLAN.md`; it does not introduce a new reward setting, change a policy, or select a result-dependent baseline.

## Main reserved cohort

**Twelve audit seeds 9800–9811 are reserved and disjoint from main study seeds 9600–9611.** Use the identical implementation (once finalized), size10, 1000 stable training ticks, then 3000-tick paired test, resource regrowth `.06` for ticks1–1000 and2001–3000 and `.055` for ticks1001–2000. Compare online stochastic training to frozen stochastic with matching initial physical state, trained theta, action-selection mode, and RNG stream. Running the same code on new seeds is a generalization check within one generator—not external replication or 12 new intellectual loops.

The independent audit must check:

1. `NEXT_ONLINE_PLAN.md`, finalized source and actual audit result source SHA256 fingerprints.
2. The two test arms start at equal full physical and theta state; any `learning` difference alone must be accounted for.
3. Primary outcomes at t3000: seed-paired mean energy, floor share, raw tail drift, and wins. A small positive mean without improved floor is not a general welfare gain.
4. Secondary frozen deterministic deployment from each captured theta at t0,t1000,t2000,t3000 under both stable and mild test laws, using validation seed `train_seed+40000`, matching the parent's protocol. This isolates learned policy competence from stochastic sampling during deployment but is not uninterrupted online-world adaptation.
5. If a source or protocol mismatch is found, mark the audit invalid and report the discrepancy; do not silently reconfigure the run.

The primary and diagnostic metrics are predeclared, so the auditor must report negative/null outcomes and avoid selecting the strongest checkpoint after observing results. The audit is **one independent conceptual test**, regardless of its seeded simulations and nested checkpoint evaluations.
