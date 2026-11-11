# Long-lived seasonal Garden: state-history and intervention audit

**Status:** executed, predeclared `SEASONS2_PLAN.md`, frozen-source `SEASONS2_probe.py`, complete 72 trajectory × 12,000 tick row-level `SEASONS2_results.json`. All worlds are synthetic *counterfactual forks* and do not touch the canonical paused Living Garden. There is no neural-weight learning or social behavior in these six deliberately simple hand-coded policy controls.

## Loop S1 — Does a seasonal Garden recover promptly when conditions become favorable?

**No.** Each seed experiences repeated 1,500-tick mild seasonal scarcity at regrowth .048 and 1,500-tick standard regrowth .06; final recovery is 3,000 ticks. Under the fixed .51 rule, mean energy changes across boundaries: t1500 **.6244**, t3000 **.0194**, t4500 **.0622**, t6000 **.0194**, t7500 **.0618**, t9000 **.0200**, t12000 **.0951**. Recovery regrowth is restored, but population energy has long historical deficits. These numbers are means across 12 initialized 256-cell worlds, not independent tick samples. Finite recovery, not universal irreversibility.

## Loop S2 — Does policy-switch timing identify a causal benefit?

**The proposed early-switch comparison is *not identified*.** The predeclared `early` switch at t1400 is exactly equal to the `reverse` policy from t1 across all 12 seeds and recorded milestones: the conditional emergency branch was not activated before t1400. A delayed t5500 switch differs, but changing both timing and depleted world state prevents a claim that *early* always beats *late*. Outcome at t12000: fixed .51 **.0951**, reverse/early **.0385**, late **.0400**, reactive **.0373**, oracle seasonal **.0375**. All 12 seeds favor fixed vs every switching rule. Critically, the season oracle is *worse* than fixed because foreknowledge does not imply correct action policy. We must not convert this result into an argument that history-sensitive policy switching is adaptive.

## Loop S3 — Does adding state-reactive or oracle timing solve the ecology?

**No.** The reactive policy (permanently switch once >10% cells at energy ≤.01) has t12000 mean energy **.0373** and depleted fraction **.095**. Oracle seasonal switching has t12000 mean energy **.0375** but depleted fraction **.614**, compared with fixed t12000 **.0951** depleted fraction **.086**. Matching policy actuation schedules to known seasons can induce harmful energy distribution, and a mean alone hides inequity. This oracle has privileged access to regrowth and is not an autonomous learner.

## Implications and limitations

The world retains environmental and bodily history, but this is *stored state*, not evidence of a learned structural memory mechanism. Some world-state histories differ even when current regrowth is the same. The predeclared timing hypothesis failed to identify a clean effect. For future work, clone an exact state at an intervention point and change **only one** rule or intervention variable; evaluate energy floor and tail distribution alongside mean. The held-out `SEASONS2_RECOVERY_PLAN.md` is that follow-up design.
