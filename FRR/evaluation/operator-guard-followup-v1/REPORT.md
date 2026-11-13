# Detached operator-guard follow-up

13 November 2026, America/Chicago.

The existing proposed guard was copied unchanged from `neural-garden-v01-intake-v1/operations/guard_proposal`. Its learning equations and original physics remain unchanged. All executed checkpoints were freshly generated locally. Neither the canonical neural world nor the continuing notebook garden was opened or mutated by these tests. No deployment occurred.

## Seven injected exception boundaries

`probe.py` generated seven independent 4×4 worlds, advanced each three ticks, paused, and injected an exception at one distinct intervention boundary. These are software-failure cases, not repeated independent evidence about ecology.

| Interruption boundary | Pending marker | Checkpoint changed | State/manifest learning agree |
|---|---|---|---|
| Before marker write | No | No | Yes |
| After marker write | Yes | No | Yes |
| After checkpoint state only | Yes | Yes | No |
| After full checkpoint helper | Yes | Yes | No |
| After snapshot | Yes | Yes | No |
| After final manifest | Yes | Yes | Yes |
| After applied event, before marker removal | Yes | Yes | Yes |

All six pending-marker cases blocked ordinary advance, further intervention, and ordinary fork, with unchanged physical fingerprint during the blocked attempts. Read-only inspection remained possible. All seven allowed an explicit exact pre-intervention recovery fork while retaining the original source and marker status. A subsequent successful intervention cleared its marker normally. `RESULTS.json` contains these assertions and copied-source hashes.

The guard intentionally treats an interruption after the applied event as unresolved even though state and manifest agree: it does not automatically infer that the marker may be deleted. This preserves uncertainty but requires operator reconciliation. Before-marker interruption leaves the original state unchanged yet leaves an already-created backup; retrying intervention refuses to overwrite it. Explicit recovery still works under the exception-test conditions.

## Actual abrupt process exit: a remaining recovery gap

`abrupt_exit.py` generated an eighth independent world and ran its intervention in a child process. Immediately after saving the changed checkpoint, the child called `os._exit(93)`, bypassing Python `finally` cleanup. This is an actual abrupt process exit, not a power-loss or storage-durability test.

The pending marker and `RUNNING.lock` both survived. The checkpoint changed while the manifest learning flag remained stale. Read-only `_open` inspection remained possible. The ordinary explicit `restore_fork` command refused because the stale run lock was still present, before it could use the preserved backup.

This qualifies the earlier recovery result: the proposed marker guard handles the tested exception paths, but it does not itself supply a complete recovery workflow after abrupt death of the lock owner. Manual lock removal was not performed, and no pending record was deleted. The disposable interrupted state remains available for inspection. See `ABRUPT_EXIT_RESULT.json`.

The next operator-only design question is how to establish that a lock owner is dead and permit an explicitly recorded recovery without trusting PID reuse, confusing concurrent ownership, or silently replaying partial actions. This is separate from changing neural/world dynamics. No proposed fix is adopted here.

## Limits and reproduction

No hard-kill signal matrix, host reboot, power loss, directory fsync proof, concurrent-operator race test, or canonical deployment is claimed. The seven exception cases release locks normally and must not be counted as abrupt-death tests. The eighth case does bypass cleanup, but process exit does not establish stable-storage durability.

Use the existing local environment to run `probe.py` and then `abrupt_exit.py` in a fresh output directory. Both scripts intentionally refuse existing initialized worlds rather than rewriting their history. The copied `source/` files are exact bytes of the prior proposal. Generated pickle files are trusted local reproduction outputs and should be excluded from publication.
