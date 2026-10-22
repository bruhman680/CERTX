# Garden v2 separate review

This review uses the same authored models and shared platform/context as the coordinator, with separate scalar/rational checks. It is a practical inspection, not independent laboratory replication or an attempt to establish FRR superiority. [Review contract](REVIEW_CONTRACT.md) records the criteria before the audits. No new agents, provider calls or external experiments were used.

## Cycle1: access, survival and observation semantics

[audit_cycle1.py](audit_cycle1.py) reconstructs216 joint/observation laws without importing the experiment implementation. It checks each reported sharp interval and101 constructed survival values per cell. [CYCLE1_AUDIT.json](CYCLE1_AUDIT.json) reports maximum error2.23e-16, correct protocol binding and all checks passing.

The population ternary observation probabilities p1,p0 imply the sharp survival set[p1,1-p0]. Every intermediate v has admissible gate probabilities a1=p1/v and a0=p0/(1-v), with irrelevant zero-mass endpoint coordinates handled explicitly. The formula, rather than the finite dense replay alone, supplies the general attainability argument. Zero-coding missingness instead gives[p1,1].

Selection-dependent access can make two different survival levels have identical ternary laws. Treating complete cases as representative would then be wrong. The conditional-readable mean equals population survival under the declared MCAR assumption and positive readability; it does not follow merely from having a missing-value label. The216cell grid contains30 readable MCAR cases and6 fully closed MCAR cases, not216 MCAR cases. [Method note](CYCLE1_METHOD_REVIEW.md) preserves that protocol wording clarification.

Restoration is informative about the original state only under a state-conservation contract. Both preserving and rewriting matrices are valid; one reveals original survival while the other reveals the rewritten state. A successful subsequent read does not by itself establish preservation. Perfect direct external access is stipulated, not empirically authenticated. These are population identified sets, not finite-sample confidence intervals or evidence that real memory obeys this model.

## Cycle2: actions can need less identification, but require an objective

[audit_cycle2.py](audit_cycle2.py) independently derives the policy results with rational arithmetic, then enumerates state/damage outcomes. [CYCLE2_AUDIT.json](CYCLE2_AUDIT.json) records maximum floating difference1.12e-16 and successful source/protocol binding. A full replay of the final source in an owned sandbox exits0 and produces byte-identical RESULTS.json. [Replay stdout](SOURCE_REPLAY.stdout.txt) and [stderr](SOURCE_REPLAY.stderr.txt) are saved. The sandbox's source/input copies are reproducible transport duplicates, not new scientific data.

Under the specified state losses, pure-action threshold is17/28. Intervals entirely on one side can support a single action without identifying v. For straddling intervals, minimax expected loss uses fallback probability5/7, while minimax regret uses19/28 on[.2,.8] and8/21 on[.55,.7]. Those differences arise from different declared criteria. They do not mean the data are contradictory or that one criterion is universally correct. Randomized improvement is in expected criteria across the population, not a safety guarantee for a single realized decision.

The probe reveals the individual's post-intervention state S', not simply the population parameter v. That distinction makes its prospective information different from knowing v. With declared damage and cost, direct enumeration supports the probe-loss formula and all12 interval/probe evaluations. For[.2,.8], worst expected losses are .15 for the cheap preserving probe, .62 for the costly preserving probe and .796 for the damaging probe. Ignoring damage would report .15 for the last case and select an action incorrectly under this objective.

The damaging probe combines information and state intervention. Its benefit/cost is not pure value of information or an unconditional ordering of experiments. The oracle knowing S' is also richer than the fixed-policy regret comparator knowing only v; these benchmarks should remain separate. Loss weights, costs, damage law and perfect post-state access are authored inputs. Empirical measurement or another task could change the preferred action.

## Failures, preservation and useful revision

Cycle2's first NumPy-boolean serialization failure is preserved in INITIAL_FAILED source/streams, with repair notes. The final serializer rejects unsupported values rather than silently replacing them. Independent final-source replay agrees exactly; no objective or scientific parameter was changed in the repair. Both reviewer audits completed without failures or new stochastic sampling. No unrecorded repeated trial or selection of successful samples is involved.

A justified small practice is to separate three questions: what information survives, what the observer can access, and which action is warranted under the stated consequences. Missing output should retain its missingness semantics. An unresolved parameter can coexist with a stable action, while an apparently informative intervention may destroy what the task values. Preserve the uncertainty set, criterion and intervention-conservation assumptions when recording that decision.

These cycles are useful discovery/re-discovery contacts. They support the scoped calculations and refinement above, not general physical-memory identification, actual-agent performance or a universal optimum. No broader efficacy comparison or automatic fourth cycle is needed to close the requested run.
