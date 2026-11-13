# Persistence and interruption review

12 November 2026, America/Chicago. Source commit3204c81ebc6922d66b0ae2623ee83d629f11f3b8. Only inspected source and newly created disposable worlds were executed. No remote pickle or canonical neural/LLM checkpoint was loaded or changed.

## Reproduced functionality

Using exact pinned source bytes, checkpoint save/load retained the full fingerprint and five subsequent stochastic/learning ticks reproduced identically. With learning disabled, all seven neural parameter tensors remained bit-for-bit fixed for30ticks. A fresh4x4world advanced5ticks, paused, forked, underwent a resource intervention, and restored the full pre-intervention checkpoint into a separate fork. The recovery fingerprint matched exactly, and the intervened parent's state remained intact. Full-state backups are materially stronger than visual snapshots.

## Reproduced same-tick commit gap

An intervention changes checkpoint state and manifest in separate writes. I injected a Python exception after saving state.pkl but before updating the manifest. Tick stayed5; actual learning became false while the manifest still said true; resource state and fingerprint changed. The last event was intervention_prepare, not intervention_applied. The original _open accepted the state because its tick matched the manifest. A separate confirmation actually advanced it to tick6 while retaining the inconsistent learning flag. See exact_run/RESULTS.json and GAP_CONTINUATION.json.

This is a bounded simulated process-interruption test, not an actual power-cut, filesystem-durability or exhaustive crash-matrix test. It identifies a gap specific to same-tick changes that a tick counter cannot detect. The pre-intervention backup still permits explicit recovery; a recovery mechanism existing does not mean interrupted state was automatically classified correctly.

## Separate proposed guard, not an upstream merge

OPERATOR_GUARD_PROPOSAL.diff records a minimal operator-side proposal: durably record INTERVENTION_PENDING.json before state mutation; clear it only after a completed applied-event record; refuse ordinary advance, intervention or fork while it remains. Explicit backup restore-fork and read-only inspection remain available. No learning equation or world physics changes.

The proposal was tested against the same injected gap in a new local world. It blocked continuation without changing partial state, allowed an exact pre-intervention recovery fork, retained the original pending source, and cleared its marker after an ordinary successful intervention. GUARD_PROPOSAL_RESULT.json records the result. It is not a complete storage-transaction solution or power-loss guarantee; file/directory durability, every interruption point and all CLI workflows would require further testing before deploying it as a general fix. Neither source branch nor active garden uses this proposal automatically.

## Source fidelity and artifacts

The initial apply_patch transport added one trailing newline to source copies. Initial executed-source hashes and outcomes are retained. Exact raw bytes were restored and verified against the pinned Git blob IDs; the independent bounded checks were rerun under exact_run with the same algorithm and seeds. Repeats are verification attempts, not extra independent samples. EXACT_SOURCE_CHECK.json and source_fidelity_initial/ preserve the correction. Disposable generated .pkl files are local test artifacts and are excluded from publication; reproduction scripts regenerate their own trusted checkpoints.

The practical transfer is to separate state identity, chronology and commit status. A plateau or unchanged tick is not evidence of unchanged state. Our notebook candidate's pending-operation and batch records already address this class of ambiguity under its own declared boundaries; no ecological reward or neural controller needs to be imported.
