# Prospective independent raw-array replay plan

Written before main execution on 2026-10-26 UTC by fresh array auditor `/root/perturb_replay` after reading `PROTOCOL.md` only. No outcomes, implementation source, or implementation imports have been inspected. This plan fixes selection before outcomes; later schema/source inspection will be disclosed in the audit record. The audit will neither run the main experiment nor modify historical artifacts. Audit code and records will live under `review/`.

## Prospective revision before outcomes

The root notified the auditor before main execution or outcomes of the fourth-method SOLVED comparator. The initial plan is preserved verbatim as `REPLAY_PLAN_INITIAL.md`. This revised plan expands the same ordinal selection rule to four methods; it does not claim the expanded count was in the initial plan. No draft audit code existed at revision. The auditor has still read no implementation or outcomes.

SOLVED reconstructs the signal contrast as `(Dprobe - alpha * D) / (beta - alpha)` for nonzero denominator and fits the same rank guard. COPY and GLOBAL_FLIP have zero denominator: reconstruct the explicit unidentified-operator flag and zero-projector placeholder, and never interpret this as identified signal recovery. Check SOLVED binding recovery for the three identified operators and all its saved structural fields. The coefficients are supplied trusted interface information.

## Frozen selection and coverage

For **each of all 960 method conditions**, select the **first and last source query in the saved canonical source-query order** (ordinal positions 0 and 31, never selected by scores, failures, or labels). Preserve each condition's full identity: seed, delta, probe, m, r, query noise, and method. This gives **1,920 method records** and **92,160 candidate readouts** (48 candidates per record). Check that the selected query identities match the source order and that every method condition appears exactly twice. Repeated controls remain separate logical conditions even when arrays are deduplicated.

Reconstruct **all 60 structural configurations** (3 seeds × 2 deltas × 5 probes × 2 m values) and **all 480 calibration configurations** (structural configurations × 2 r values × 4 methods). Query noise does not produce a new clean calibration configuration. Also inspect full source-query identity/reuse and exact output mapping cardinalities to establish that replay selection is complete.

## Independent reconstruction

Read the engineer's declarative artifact schema when available, and disclose that read. Access saved raw task inputs, selected actual training rows, saved rotations, explicit five-arm probe definition, and condition identities. Reconstruct probe contrasts from source contrasts by applying context/binding block scales before the saved Q; check the supplied pre-fit probe and average arrays. Independently compute rank-guarded SVD projectors with absolute cutoff 1e-10 and rank ceiling 12, including the empty/zero average guard. Reconstruct analytic transported targets and all saved structural diagnostics, singular values, numerical/retained ranks, and residuals. Check CONTEXT_FLIP/SIGNAL_FLIP equal probe spans, GLOBAL_FLIP unchanged probe span and zero average, and the rank-zero binding distance 1/sqrt(2).

Independently reconstruct all clean calibration products and circular centres using the saved raw calibration entities/queries, supplied labels, canonical candidate order, complex arithmetic, column action expressed as x @ P.T, and the protocol's 1e-10 validity/resultant policy. Compare every calibration configuration, including validity, centre angles, resultants, and global availability.

For each selected noisy raw query and all 48 raw candidate records, independently apply FULL, ORACLE, the independently reconstructed average REPAIRED projector, or the independently reconstructed coefficient SOLVED projector; normalize projections, form complex products, take modulus scores, apply stable descending ranking with canonical ties, decode using independently reconstructed calibration centres and the exact abstention policy, and reconstruct returned top three and oracle-relevant predictions/reasons. Compare saved products, validity, scores, decoded labels/reasons, indices/record IDs, and boundary ties. The separate reviewer owns exhaustive ledger metrics/aggregates/control comparison; any overlap is a cross-check, not a substitution.

## Artifact resolution and comparisons

A declarative complete condition/field map may point to exact content-addressed arrays in NPZ storage. Resolve each logical output through this map; independently verify content hashes over dtype, shape, and bytes and mapping cardinalities. Do not infer outputs from an implementation function, rounded proxy, aggregate, or selected saved rows. Exact discrete outputs and hashes must match; floating comparisons will report maximum absolute/relative residuals, with explicit tolerances justified by arithmetic precision and the fixed decision threshold. Threshold/tie disagreements are failures even when nearby floating values pass an arithmetic tolerance. Angular comparisons use wrapped circular distance. Preserve rank diagnostics when singular values are near threshold.

## Independence, failures, and final record

No predecessor or main implementation imports. Record every file/source/schema actually inspected, commands, audit code hashes, selected condition/query IDs, counts, comparison tolerances, discrepancies, and limitations. Preserve the first failing audit output and code before any fix; record diagnosis and any later audit-only correction separately. A main-artifact defect is reported without silent repair, parameter change, or rerun. Wait for the root's notification of completed main execution before reading outcome artifacts or performing outcome replay. Completion requires a saved replay report containing actual reconstructed coverage and comparison results, not merely checks that saved outputs agree with one another.
