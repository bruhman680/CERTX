# Neural Garden temporal update gates — negative causal probe

**Status:** Predeclared and run on twelve fresh matched seeds 10100–10111, 100 cells per world, 1000 initial training ticks and 3000 deployment ticks. The protocol `NEXT_GATE_PLAN.md` was written before source and before main outcomes; source was frozen after unrelated two-seed smoke. All five neural arms used identical initial trained theta, world state, stochastic action mode and action RNG. Full per-seed, checkpoint, diagnostic and hashes in `NEXT_GATE_results.json`; `NEXT_GATE_probe.py`, `NEXT_GATE_garden.py` are frozen. Fresh seeds 10200–10211 are reserved for independent audit and were not used by us.

**Hypothesis:** Suppress neural policy-weight updates specifically during mild scarcity (t1001–2000, regrowth .055) and improve final energy *without* worsening cell depletion compared with a same-duration sham gate suppressing updates during the stable first third. This is an explicitly designer-imposed scheduler, not learned breathing.

| Deployment controller at t3000 | Mean energy | Near-floor cells | Final 500-tick unclipped energy drift |
| --- | ---: | ---: | ---: |
| Online continuously | .03797 | 17.92% | −.001807 |
| **Freeze theta only during scarcity** | **.03811** | **18.50%** | **−.001891** |
| Sham gate, freeze theta in first third | .03965 | 17.50% | −.001639 |
| Gate theta during recovery (third third) | .04113 | 16.92% | −.001785 |
| **Freeze theta throughout** | **.05119** | **12.67%** | **−.001468** |
| Hand-designed reverse-rescue threshold | **.27838** | **10.25%** | Not recorded |

**Result: the preregistered scarcity-specific gate fails.** Relative to equal-duration sham, it has lower mean energy by `.00154`, *higher* floor exposure by 1.00 percentage point, and more negative raw late drift; scarcity gate wins only 3/12 paired seed energy comparisons. Recovery-stage gate improves energy over sham in 9/12 seeds, but frozen-all still beats every online update schedule on both aggregate energy and floor. None repairs the negative raw budget. The manual rescue remains far superior on aggregate ecology.

Frozen deterministic deployments into identical fresh mild-shift environments reveal learned-weight quality separately from live stochastic trajectories: stable original theta `.22579` mean energy with 17.08% floor; scarcity-gated final theta `.07128` with 26.50% floor; sham-gated `.05205` with 25.17%; recovery-gated `.10584` with 25.92%; continuously online `.04184` with 28.33%. Scarcity-gated weights are *less degraded* than continuously online here, but they remain worse than original frozen weights; there is no evidence they positively adapt.

## Interpretation and limits

- Withholding updates at known scarcity onset does **not** confer ecological benefit over an equal-budget early gate in this setting. This falsifies a narrow causal hypothesis; it does not disprove future condition-triggered learned gating under other worlds.
- Gates keep eligibility trace and reward baseline running while freezing **only theta**, so skipped rewards still influence later updates via the trace. A genuine learned metacontroller or a reset-on-pause protocol was not tested.
- `gate_recovery` hints later updates can be harmful, but it was one of three predeclared scheduling contrasts; treat the suggestive 9/12 energy wins as a follow-up hypothesis, not discovered universal timing law.
- Equal skipped tick counts do not guarantee equal *number or amplitude of consequential updates*, and actions/world states diverge causally following first differences. Contrasts are legitimate scheduled interventions but cannot identify one-step credit effects or generalize beyond this synthetic regime.
- Study units are **twelve world seeds**, not 1200 independent cells. Source includes no transformer, long-term autonomous multi-agent scientist, consciousness assay, or evidence of spontaneous evolutionary learning.

**Next warranted probe:** Try a bounded, externally measured *viability guard* with a preregistered objective requiring both energy gain and non-increase in floor fraction and negative raw drift. If protective gating is hand-designed, label it explicitly as control engineering. Audit the timing-gate hypothesis first on reserved 10200–10211 before making stronger claims.
