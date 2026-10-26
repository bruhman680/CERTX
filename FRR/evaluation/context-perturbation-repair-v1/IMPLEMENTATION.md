# Implementation provenance and execution

Standalone NumPy plus Python standard library implementation; no predecessor implementation imports or predecessor executable-source inspection. Engineer inspected CR PROTOCOL, predecessor PC SCHEMA, SA/PC input/archive manifests, one source ledger record and the actual first source training pair/difference to verify the documented factor2 convention. This is source-data/schema inspection, not implementation independence from knowledge of the preceding design.

No experimental generation, fit, scoring or main execution performed during implementation. Allowed checks: Python syntax compilation and independent nonexperimental fixed-array fixtures of helper functions only; exact commands/results documented separately. Root alone executes main once after independent reviewer approval and completed freeze, single BLAS thread, timeout180seconds. Existing nonempty output directory causes failure; every failed attempt must be preserved. No output tuning or automatic rerun.

Code copies its initial executable, protocol/schema/implementation into run; source hashes and probes are saved before fit, and every fitted projector/centre is saved and hash-checkpointed before scoring. Original source task NPZ byte-copied; PC only selected source arrays copied with full-file/full-array hashes plus slice. No gigantic redundant PC archive copy. Actual source archives verified by SHA256. Outcome pool exact content addressing preserves all complete candidate arrays. This implementation explicitly changes the predecessor's fixed-rank estimator to the prospectively specified numerical-rank guard.

Before any main execution, root refined the protocol to add SOLVED coefficient-aware comparator. experiment_PRE_SOLVED.py preserves the complete preceding draft; experiment_INITIAL.py is the earlier initial source snapshot. This change is prospective and has no outcome contact.

Prospective reviewer correction before main: calibration means divide by valid sample counts, centres unavailable only if count0 or resultant<=tol. Initial pre-correction drafts preserved. No old implementation source inspected.

Further prospective review: unidentified SOLVED target comparisons are null, with explicit solved_available=false/solved_reason=unidentified_operator; numerical zero placeholder diagnostics are separate. Control source ledger file hash is verified against original PC archive manifest before reading. Additional predecessor ledger data-only inspection checked encoded_U metric definition, no executable source inspected.
