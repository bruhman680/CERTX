# Prospective saved-array replay plan

Fixed before main outcomes on 2026-10-26 by the fresh independent replay auditor. Read `PROTOCOL.md` and `review/ANALYTIC_CHECK.md`; no main implementation or experimental outputs have been inspected at this point. This is an independent implementation review, not a claim of perpetual source blindness. Any later schema/source inspection will be disclosed.

## Fixed task sample

For every one of the 720 method conditions (seed × five arms × four fitting prefixes × two r × two query-noise values × three methods), select the first and last query in canonical source query order within that condition. Thus replay exactly 1,440 method records, including their entire 48-candidate readout vectors. Select by original source query index (minimum and maximum), never by outcomes, relevance, failure, score, or returned labels. Condition keys and chosen source query indices will be saved in the replay output.

Reconstruct projected query/candidate vectors from the copied frozen source arrays and saved projectors; normalize with the fixed 1e-10 threshold; compute all complex products, scores, angles, decoded labels and abstention reasons independently. Compare all candidate values to the compact saved readouts and compare returned top-three indices, predictions and reasons with the ledger. Exact-score ties use canonical candidate order. Report last-bit near-tie differences explicitly rather than treating every independently reordered exact/near tie as a semantic failure.

## Full structural replay

Reconstruct all 60 fitted projectors (three seeds × five arms × four prefixes) from saved raw/unit training banks and arm definitions, without importing experimental implementation. Verify raw/unit normalization, fixed prefix membership, difference identities, shared dense Q, all singular values, rank/cutoff diagnostics, and saved projector properties. Independently derive every arm's population moment and unique target and intended binding projector, then recompute empirical moments, operator deviation, normalized projector distances, principal cosines, eigengaps, and train/validation contrast residuals.

Reconstruct all 360 calibration-center method conditions (three seeds × five arms × four prefixes × two r × three methods) using only calibration entities and actual saved arrays. Verify per-status counts, circular means/resultants, and global availability; use the protocol's zero product, unavailable calibration, and ambiguous-center policies. The task sample will use these reconstructed centers.

The separate ledger auditor owns exhaustive ledger metrics, all 720 aggregates, repetition/availability counts, and control reuse comparisons. This replay owns array-level geometry/calibration and the fixed 1,440-record complete candidate replay. Share material failures directly; do not import predecessor or current experiment functions or invoke the main runner.

## Reporting

Save independent executable `review/replay.py`, a machine-readable check report, fixed sample identifiers, and a concise `review/REPLAY_REPORT.md`. Report actual tolerances, maxima, source/data hashes and source files read. Preserve all existing artifacts; write only new review artifacts. Any mismatches must remain visible, with exact-tie/numerical distinctions justified from values. No additional outcome-selected sample or tuning of protocol is authorized by this plan.
