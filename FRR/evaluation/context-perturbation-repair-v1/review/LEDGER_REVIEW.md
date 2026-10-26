# Independent exhaustive ledger review

All30,720 method records,7,680 paired rows and960 condition aggregates passed the independent audit in `audit_ledger.py`; results in `LEDGER_CHECKS.json`. Every record was reconstructed from complete saved candidate field arrays and fixed source claim/status truth, without importing implementation code. The audit checked record IDs, exact ranking, returned products/scores/angles, predictions/reasons, oracle-relevant diagnostics, all task metrics, boundary ties, pair links, query identities/reuse and every aggregate. All15,360 FULL/ORACLE predecessor comparisons and14,592 repeated-control comparisons matched exactly. There are384 source-query IDs,288 unique base arrays,80 method uses per query ID. These are reused controls, not independent observations.

Source inspection was disclosed prospectively: protocol, schema and new implementation source were read; old implementation code was not imported or inspected. Actual source arrays were inspected only for digest verification and this audit. Independent raw arithmetic/subspace/calibration replay belongs to the separate replay auditor; this exhaustive ledger audit does not substitute for that work.

## Preserved audit-only correction

The initial audit completed all record checks then rejected aggregate floating sums: Python's compensated built-in sum gave30.0 where the implementation's sequential additions gave30.000000000000007. Initial audit code/logs remain as `audit_ledger_INITIAL.py` and `LEDGER_AUDIT_INITIAL.*`. The corrected audit permits1e-11 arithmetic error for floating aggregate sums/means; all integer/discrete values remain exact. Maximum actual difference was7.105427357601002e-15. No main artifact or scientific parameter changed.

## Outcome interpretation

Pooled joint-label recall (correct scope and status among the actual top3) across all frozen seeds/deltas/m/r/noise/query rows:

| Probe | Averaged REPAIRED | Coefficient-aware SOLVED |
|---|---:|---:|
| COPY | .3828125 | unavailable |
| CONTEXT_FLIP | .8046875 | .8046875 |
| PARTIAL_CONTEXT | .7378472 | .8046875 |
| SIGNAL_FLIP | 0 | .8046875 |
| GLOBAL_FLIP | 0 | unavailable |

FULL=.5130208 and ORACLE=.8046875 in every probe group. These are descriptive equal-weight pooled outcomes with repeated controls. Coefficient-aware availability is a mathematical identification condition supplied by trusted role coefficients, not a probability estimate. All3,072 unavailable SOLVED records explicitly retain their unavailable flag/reason. Their zero-projector downstream evidence recall .0625 arises from canonical first3 ranking of all-zero scores; it is a placeholder consequence, not evidence recovered by an unidentified operator.

CONTEXT_FLIP and SIGNAL_FLIP have identical probe subspaces yet averaging yields sharply different task outcomes. SIGNAL_FLIP averaging has evidence recall .7473958 but joint-label recall0 and all three returned items abstain: preservation/retrieval of records does not guarantee usable status information. GLOBAL_FLIP supplies maximal ambient response while its average is zero. PARTIAL_CONTEXT averaging improves over COPY but retains some context; known coefficients permit exact conditional signal reconstruction instead. These observations support separating response, identification assumptions, reconstruction rule and task outcome.

ORACLE recall is below1 in the pooled noisy task; successful subspace recovery does not remove query noise or guarantee every retrieval. No result validates real-language probe selectivity, autonomous semantic diagnosis, physical fault analogy or a calibrated mismatch detector. The local source/provenance pre-fit failed attempt and diagnosed repair remain part of the execution record; one repaired main experiment completed.
