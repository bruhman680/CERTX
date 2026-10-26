# Independent raw-array replay audit

The audit validates fixed record-ID values and returned-set membership, with ordered differences. **The original strict ordered replay remains FAIL (`strict_original_pass=false`).** Its 1,170 comparison flags, code, selection and log remain unchanged and are copied with hashes into `REPLAY_ORIGINAL_FAILURE/`. This report supplements that result; it does not replace its criterion or claim an original pass.

## Coverage and independence

The initial three-method plan was written before outcomes and preserved as `REPLAY_PLAN_INITIAL.md`. Root's pre-outcome addition of coefficient-aware SOLVED expanded the prospective plan to four methods, recorded in `REPLAY_PLAN.md` before main execution. The fixed sample remained source ordinals 0 and 31 in every condition. Actual audit coverage is all 60 structural configurations, all 480 calibration configurations, all 960 method conditions, 1,920 selected method records and 92,160 candidate readouts. The audit also independently hashed all 1,207 exact content-addressed output arrays and checked 7,680 complete logical array references.

Inspected sources: initial protocol, root's prospective revision instructions, initial and updated declarative `SCHEMA.md`, raw task/training/probe/structure/outcome NPZ files, structural/calibration JSON, complete output map and selected ledger records. No `experiment.py`, predecessor implementation, implementation imports, or main reruns. Auditor code independently reconstructed actual privileged probes, coefficient solutions, rank-guarded projectors, analytic targets, clean circular calibration, noisy normalized complex products, fixed-ID decoding, stable sorting and returned records. The separate reviewer reconstructed all ledger metrics/aggregates and independently corroborated the resumed ordering classification.

Numerical comparisons retain original `atol=rtol=2e-12`; all validity, label, reason, membership and identity comparisons are exact. The decision threshold remains 1e-10. No sample, threshold, main artifact or original audit code/result changed during diagnosis.

## Original result and classification

All structural/projector/spectrum/rank comparisons and all calibration comparisons pass the original arithmetic tolerance. The largest projector entry difference is 1.234e-14, largest calibration product difference 1.066e-14, and largest selected evaluation product/score difference 1.186e-14. First/second/average/coefficient-solved raw contrasts match exactly. All selected per-candidate fixed-ID validity, decoded label and reason arrays match exactly: 92,160 readouts each. Abstention and boundary flags match exactly.

The 1,170 original flags comprise 223 condition-level top-array flags, 341 returned-index flags, 341 returned-record-ID flags and 265 returned-label-sequence flags. They arise in 341 of 1,920 selected rows. **Every affected row retains the identical three-member returned set.** There are zero candidate label/reason/validity differences and zero returned-set membership changes. Sequence-label differences follow the changed positions of the same record IDs.

`REPLAY_ERROR_CLASSIFICATION.json` classifies every original flag by index, links affected rows and records exact fixed-ID checks, independent/saved top IDs, exchanged or reversed ID pairs, and their score gaps. Across all reversed pairs the maximum saved-score gap is 2.054e-15 and the maximum independent-score gap is 1.555e-14. These are measured differences rather than a tolerance-based ranking repair. Neither sorting algorithm changes scores or introduces ties. The independent SVD reconstruction produces projectors within arithmetic tolerance but changes floating order among these returned records.

Every saved top three is exactly the stable descending sort of the saved scores. The supplemental saved-projector replay reconstructs calibration and all selected raw readouts from the saved numerical projectors and matches all discrete outputs exactly, with zero comparison errors. This localizes the ordering discrepancy to refit numerical representation rather than stored-score ranking, candidate decoding or membership. That supplemental success does not satisfy the original independent-refit ordered requirement.

Boundary diagnostics are preserved: 288 selected rows have saved third/fourth gaps at most 1e-10; the independent replay produces exactly the saved near-boundary flags, and no selected row crosses the returned-set boundary. The machine result retains these counts independently of the ordering classification.

## Failure preservation and artifacts

Audit attempt01 had an audit-reader key parsing error: `_r` was split inside `repaired`. Its code and diagnosis are retained as `replay_audit_attempt01.py` and `REPLAY_ATTEMPT01_FAILURE.txt`. Correcting key construction produced the original strict FAIL, retained as `REPLAY_RESULT.json` and `REPLAY_ATTEMPT02.log`. All 1,170 original flags were subsequently reproduced identically. Main's earlier source-hash failure is outside this audit's code and remains root's preserved execution record.

`REPLAY_FINAL_RESULT.json` is the scoped final machine summary. `REPLAY_ERROR_CLASSIFICATION.json` contains all 1,170 classifications and all 1,920 per-row fixed-ID/membership checks. `REPLAY_SAVED_PROJECTOR_RESULT.json` and its log contain the diagnostic saved-projector replay. `REPLAY_SELECTION.json` is the unchanged prospective sample realization. `PRESERVATION_HASHES.json` inside `REPLAY_ORIGINAL_FAILURE/` binds the original files; the final machine summary verifies their current bytes still match.

The original strict ordered criterion is unmet. Fixed-ID arithmetic/categorical behavior, calibration, structural reconstruction, saved-score sorting and selected returned-set membership are validated at the coverage above. No confidence interval, general perturbation detector, external causal selectivity, or out-of-fixture behavior is established.
