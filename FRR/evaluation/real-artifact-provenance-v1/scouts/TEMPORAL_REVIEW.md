# Independent bounded temporal-contact review

Accessed 2 November 2026 UTC; user session date 1 November America/Chicago. Reviewed `/workspace/frr/evaluation/real-artifact-provenance-v1/temporal.py` and `TEMPORAL_CONTACT.json` against the two-claim fixture proposed in `/workspace/causal-history-scout-2026-11-01.md`. No FRR edits.

**Verdict:** The implementation and saved result correctly demonstrate the proposed distinction for this fixture. No blocking bug or important overclaim was found in these two files.

The code first limits claims by receipt cutoff and effective start, then excludes a parent only when its eligible correction applies. Consequently `K3,V1` remains `ready/e1`, `K3,V2` becomes `blocked/e2`, and `K2,V2` remains `ready/e1` after the late claim arrives. The explicit before/after comparison checks the entire earlier receipt, not only its state label.

Verification: read both complete files; executed `contact()` with ambient stdlib Python using `-B`; compared all six state/witness/eligible-ID rows to a separately written explicit expected table; compared the generated object to saved JSON; and checked that `CLAIMS` remained unchanged. All checks passed. This is a second-agent functional review, not independent scientific replication, a model trial, or database-engine validation.

Two small boundaries deserve retention in downstream wording:

- The helper is correct for the fixed two-claim, open-ended effective-interval fixture. It does not validate source authority, parent existence, unique IDs, cycles, correction ancestry, finite interval ends, or arbitrary temporal histories. Its `len(heads)` guard does not by itself enforce all those assumptions. These omissions are outside the declared fixture, not demonstrated failures of it.
- The proposed receipt included an explicit applied-correction edge. Saved rows contain the answer, coordinates, eligible IDs, and witness; `e2 -> e1` is recoverable from the preserved claim list but is not duplicated in each receipt. That is a small receipt-format omission, not an answer error. Do not describe the rows as already containing a dedicated edge field.

The hard-coded `no_timestamps_inferred_from_git` flag accurately describes these ordinal authored inputs, but is a scope declaration rather than an executed test of all repository analysis. Likewise, `frozen_earlier_view_preserved` is supported by the specific comparison in `contact()`, not a general persistence guarantee.

The current scope text appropriately says authored functional example, no model calls, and no real effective dates inferred. Preserve that wording. No further experiment, fix, installation, or background work follows this review.
