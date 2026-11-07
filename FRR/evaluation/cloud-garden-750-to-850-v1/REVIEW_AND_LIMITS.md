# Preflight review and boundaries

7 November 2026. Independent reviewer cloud_boundary_review inspected the initial world/action design and the revised runtime/journal. It did not run model calls or edit source. Its independent dynamic check caught the failed cross-namespace bind; another confirmed Python user-site startup hooks were a genuine notebook-writing hazard. Main-agent development probes and failed test logs are retained separately from model evidence.

Repairs made before primary activation:

- Replaced failed namespace reattachment with a persistent trusted Python runtime inside one namespace; action child streams are separate pipes, child stdin is DEVNULL, extra FDs are closed, and guest /proc is absent.
- Explicitly unshared the user namespace and disabled nested user namespaces. Dropped capabilities. Root, /usr, runtime source and /dev are read-only; writable /world and /tmp each have an 8 MiB tmpfs data-block limit.
- Notebook appending uses isolated Python with site startup disabled (-I -S). A regression fixture first proved a .pth hook would execute in an ordinary Python action, then verified notebook appending did not execute it.
- Every notebook storage failure includes the actual result, including timeout when stderr is empty. Notebook contents themselves have no success/rejection test.
- Snapshot traversal is deterministic and fails on read errors instead of silently omitting inaccessible data. Hardlink identity, symlinks, FIFO modes and world-root mode are preserved. Directory permissions are restored after children, avoiding premature access loss. Unhandled special files or unreadable state cause an explicit integrity pause; no complete reconstruction claim is made for them.
- Restores reject traversal and symlink ancestors. The live world is compared to saved bundles and independently restored every ten committed entries.
- Journal checks compare raw hashes, manifest hashes, initial bundle hash, action kind derived independently from raw text, event parents, prompts/token IDs, decoded output, world bundle IDs and the state pointer.
- Runtime shutdown and pause/lock bookkeeping run even if the final snapshot fails. An interrupted or uncertain action is never automatically repeated. Earlier prior-stage files are hashed and preserved.

Thirteen host tests passed after the architecture change. Five additional tests check read-only mounts, clearing temporary storage, nested userns denial, Python startup-hook protection, and FIFO/hardlink restoration. The complete 18-case suite passed; the startup-hook fixture was then strengthened to assert its positive control and passed again independently. Tests are fixtures, not small-model discoveries or live-world artifacts.

## Exact resource scope

Child actions have 32 MiB address-space limits, 128 processes for the shared non-root user, 2 CPU seconds per process, a 3-second action wall limit, 256 KiB individual-file limits, 64 open FDs and 8192 captured output bytes. Shared UID process use can make the effective action process allowance smaller. Under non-root/no-capability/no-nested-userns conditions, 128 * 32 MiB is a conservative 4 GiB ceiling on summed action address spaces, not a measured aggregate cgroup memory cap. Runtime/model/observer memory and kernel allocations are separate. No writable cgroup controller is available here.

Tmpfs byte limits constrain data blocks, not every inode/directory metadata byte. The runtime also bounds how long actions can create metadata. This is a finite supervised experimental block, not a proof that arbitrary hostile workloads cannot exhaust any kernel resource. The host memory guard runs at generation boundaries. No perfect isolation or indefinitely autonomous-operation claim is made.

Processes and shell variables stop after every action. /tmp is cleared after each action and is not persistent state. /world files persist across entries and can be restored after pause from externally retained content-addressed objects and manifests. File contents, types represented by the checkpoint format, links and permission bits are observed; inode numbers, timestamps, open descriptors and running processes are not preserved as continuous state. These mechanics appear in the factual world notice where relevant.

A model that writes without acting is not prevented from continuing. A model that encounters a shell error is not prevented from continuing. Integrity failures concern our ability to retain and account for the world, not whether the model behaves as we wish.
