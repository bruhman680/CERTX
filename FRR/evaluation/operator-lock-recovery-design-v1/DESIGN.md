# Proposed operator lock and preserved recovery design

13 November 2026, America/Chicago. Design and disposable operating-system tests only. No garden source, world, stale lock, or pending marker was changed. Nothing is deployed.

## Problem and strongest recommendation

The earlier proposed intervention marker correctly prevents ordinary continuation after a partial change. But its exclusive-create `RUNNING.lock` pathname survives an abrupt process exit; the tested explicit `restore_fork` refuses before it can use a valid backup. Existence of a file is being used both as a durable historical record and as a live ownership signal. Those are different jobs.

For a **new, explicitly versioned operator protocol on one local Linux host**, use a persistent lock inode with `flock(LOCK_EX | LOCK_NB)` held through an open descriptor for the whole operation. Keep owner/session metadata and pending transaction records separately as historical evidence. Never unlink, atomically replace, or rotate the lock inode during ordinary operation. Lock release does not certify that a transaction completed.

This is a proposal for the numerical operator CLI, not an addition to the model's world laws, behavior, or notebook. It does not repair the existing interrupted test directory, and it is not a transparent change compatible with the old exclusive-create implementation.

## Source grounding

The Linux `flock(2)` manual describes descriptor-based advisory ownership, nonblocking acquisition, release when the last associated descriptor closes, and filesystem-dependent behavior. This supports separating lock lifetime from pathname existence. The lock must remain outside model-accessible writes and all cooperating writers must use it. A process that bypasses advisory locking is outside this guarantee. [Linux flock manual](https://man7.org/linux/man-pages/man2/flock.2.html)

`pidfd_open(2)` describes obtaining a process descriptor and polling it for termination. It can help monitor a known owner, but opening a persisted numeric PID after a restart can already identify a different process. A serialized record cannot preserve a live pidfd across machine loss; pidfd is a monitoring aid, not the durable lock or proof that a checkpoint is sound. [Linux pidfd_open manual](https://man7.org/linux/man-pages/man2/pidfd_open.2.html)

The `/proc/pid/stat` manual identifies field 22 as process start time relative to boot. PID plus start time, a boot identifier and host/namespace identity improve diagnostic owner records, but must not replace mutual exclusion. PID reuse, namespaces and copied archives make raw PID checks inadequate. [Linux proc_pid_stat manual](https://man7.org/linux/man-pages/man5/proc_pid_stat.5.html)

All three are documentation pages read through the web tool; no paper or full kernel implementation proof is claimed.

## Proposed acquisition and operation rules

1. Validate the operator protocol version and permitted storage type before opening a mutable world. Reject unsupported or unknown legacy protocols. Canonicalize the world directory and do not follow model-controlled lock-path links. The containing directory must be operator-owned and immutable to model actions.
2. Open the persistent lock with close-on-exec and no replacement, acquire an exclusive nonblocking flock, and retain its descriptor until the operation and audit flushes finish. A failed acquisition means busy; it never authorizes deleting a file. Keep the inode stable.
3. Write a separate session record with random session UUID, protocol version, boot/host/namespace identity, PID/start time, operation intent and input hashes. Treat metadata as evidence, not authority. Never truncate old evidence merely to update current-owner display.
4. After acquisition, independently inspect pending markers and transaction/checkpoint history. Ordinary advance, intervention and ordinary fork still refuse unresolved outcomes. Free ownership permits inspection and recovery selection; it does not clear uncertainty.
5. Do not pass or inherit the lock descriptor to generated programs or long-lived children. Close-on-exec limits exec inheritance; a fork without exec still inherits and must close it deliberately. Keep operator locking out of the model sandbox. A surviving duplicate can retain ownership after the original process dies.
6. Hold an exclusive lock throughout recovery, rather than checking owner death and then opening a race. On success or failure, preserve the operation evidence. Release by closing the last operator-held descriptor. The persistent pathname remains for later contenders.

All launchers and mutation paths must implement the same protocol. Advisory locking cannot protect against old binaries, copied alternate lock paths, manual writers or hostile filesystem changes.

## Recovery preserves uncertainty and branches history

An explicit `recover-fork` command should acquire the new operator lock, capture immutable evidence hashes for the unresolved source, and require an identified trusted pre-intervention backup plus metadata. Validate source lineage, backup hash, tick and full-state fingerprint before using it. Local pickle remains trusted executable data; hashes establish identity, not safety for untrusted imports.

Create the destination using an exclusive new-directory claim. A mere "empty directory" precheck is not sufficient to serialize two recovery commands choosing the same destination. Record a unique recovery intent before writing the child, then checkpoint it, verify it and mark it paused. Record a completion receipt linking source evidence, selected backup, child fingerprint, protocol and operator reason. Keep unresolved source state, stale legacy lock and pending marker intact. A receipt records a fork from a known backup; it does not declare what the interrupted action did or silently roll back the source.

For durable publication, the implementation needs an explicit file/directory fsync and rename ordering, including receipt directories. Interrupted child creation remains a pending recovery attempt and must not be silently reused. These durability requirements are design obligations; the probes here do not prove them.

## Legacy and archive handling

An old exclusive-create writer will not honor the new flock, so successful flock acquisition **does not prove an old writer has stopped**. Do not live-migrate the old lock file or simply wrap a second lock around old commands. A migration needs a separately established maintenance fence that prevents legacy launchers and verifies no old process is writing. If that cannot be established, remain read-only. Preserve legacy bytes and declare the new protocol in a new operator/world version.

A copied archive carries lock metadata but not live kernel ownership. Copied PID/boot fields are historical. Import it read-only first, validate its hash/lineage, classify pending effects, then explicitly initialize a new paused recovery fork and new local operator identity. Do not infer that absence of a local live PID makes the archive's transaction complete. Shared/network storage requires its own locking and durability validation; this proposal is limited to the tested local Linux setting.

## Disposable tests and confidence

`probe.py` created files only under this new study directory. It passed:

- A contender is blocked while a child holds the flock; after the child calls `os._exit(93)`, a new contender acquires it without deleting or replacing the pathname.
- A duplicate descriptor retains the lock after the first closes; closing the last duplicate releases it.
- Deliberately unlinking and recreating a disposable locked pathname permits two simultaneously locked, different inodes. This reproduces why a persistent lock must never be "cleaned up" by unlinking.

These are bounded OS mechanism checks on Linux 6.18.57, not integration of this design into the garden. Confidence is high in the demonstrated local primitive distinction; confidence in a complete garden recovery system remains provisional until an implementation passes the test matrix below.

## Required integration checks before adoption

Retest all seven prior exception points and abrupt exits under the new operator version; verify that pending transactions still block ordinary continuation while explicit validated recovery can proceed. Test competing advance/intervene/recovery processes, competing destinations, malformed/missing owner metadata, fork/exec descriptor inheritance, lock-path inode substitution, failure during recovery intent/checkpoint/receipt, and unsupported legacy versions. Separately test reboot/storage durability and any nonlocal filesystem. No deployment or canonical migration is justified by these primitive tests alone.
