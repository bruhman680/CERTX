# Persistent computational-notebook world

This module is environmental machinery. It has no model, reward, assessment of
usefulness, preferred reasoning steps, repair of source, or extraction of
commands based on apparent intention. The caller chooses what observations to
give its model and which prospectively declared interface to use.

The original garden at 1550 remains untouched. `GardenWorld.create` copies its
snapshot and the four referenced content objects into a new owned store. The
copy retains parent entry, source snapshot hash and exact initial bundle bytes.
New operation numbers start at zero; they do not rewrite or impersonate the
original entry count. Root's runner separately records candidate model turns.

## API

```python
from garden_world import GardenWorld, verify_store

world = GardenWorld.create(store, parent_bundle, parent_objects, parent_entry=1550)
event = world.apply('python', "print(6*7)")
batch = world.receive_notebook("prose\n```python\nprint(6*7)\n```\n")
snapshot = world.checkpoint()
world.close()
world = GardenWorld.open(store)
assert world.bundle == snapshot
world.close()
verify_store(store)  # no action or model inference
```

`apply(channel, source)` has explicit `shell`, `python`, `note` and `noop`
channels. `note` appends literal text using isolated guest Python; it never
executes that text. `noop` has no process receipt because no process ran.
`receive(text)` preserves the legacy exact two-key shell-action JSON law;
other text is literal writing. `receive_notebook(text)` is the additional law
below. Legacy behavior is not silently loosened.

`observe()` returns the current manifest, operation count, parent entry and last
actual receipt. It does not dereference guest symlinks or inject directory text
into a model prompt. `.step`, `.bundle`, `.objects` and `.store` are available.

## Prospectively declared notebook syntax

- A column-zero line exactly ` ```python` or ` ```sh` **without the leading
  space shown here** opens executable source. Its closing line must be exactly
  three backticks. Labels are case sensitive; no attributes/trailing spaces.
- Every column-zero run of at least three backticks opens a fence, even with
  unknown labels or arbitrary info strings. It shields all interior lines until
  the same backtick delimiter appears alone. Thus a four-backtick or unknown
  outer block does not accidentally execute a nested three-backtick example.
- Only complete exact `python`/`sh` three-backtick cells execute. Indented,
  unknown, wrong-case, attributed, or incomplete cells remain literal writing.
  LF and CRLF line endings are accepted. Source bytes are not stripped,
  dedented, completed, translated or repaired.
- The full raw reply is durably retained outside the guest. An ordinary guest
  append to `notebook.txt` is attempted once before code cells. A known append
  error remains a real receipt **and does not block cells**: the model may use
  its own code to truncate or replace a full/unwritable notebook. It is not
  silently retried or repaired.
- Complete executable cells run once in textual order, each in a new process.
  Ordinary native errors are retained and later cells still run. Python/shell
  variables and `/tmp` do not persist between cells; `/world` files do.
- At most eight complete executable cells are accepted per reply. Exceeding
  this declared resource bound returns `cell_count_limit` before any guest
  operation, with full raw text retained externally. It is not a semantic
  judgment. Cell source offsets are recorded in Unicode code points and UTF-8
  bytes, end exclusive.
- Cell output is data, never parsed recursively for executable fences.

Each batch returns `batch_id`, `raw_text`, `parsed`, `operations`, `status`,
`boundary`, `note_stored` and, after an append attempt, `note_storage_fault`.
Operations contain channel, exact source, actual receipt, visible feedback,
before/after snapshot identities and changed paths. Successful literal notes
have blank feedback; note errors and code receipts remain available unchanged.

## Bounds, persistence and uncertain outcomes

The wrapper imports the existing frozen sandbox as a pinned, read-only
dependency. It retains isolation from host research files/network and the
existing per-cell limits: 8 MiB world, 8 MiB temporary storage, 32 MiB process
address space, 128 processes for the shared UID, 3 seconds wall time, 2 CPU
seconds per process, 256 KiB per file, 64 descriptors and 8192 output bytes.
Limits are per cell; a reply can contain up to eight cells plus its note append.
This is a broad inherited Linux/Python world, not a claim that the entire OS
has been reduced to a few elementary laws.

Every operation saves PENDING before running, then saves the actual receipt,
new content-addressed snapshot and event before atomically advancing STATE.
The pending marker is removed only after commit. A notebook batch separately
records progress so committed cells are never silently replayed after a crash.
Exclusive ownership prevents two live mounts using the same store.

Lost/malformed runtime receipts, unsupported/unreadable checkpoint states and
other uncommitted effects retain pending/fault evidence and block ordinary
resume. Best-effort uncommitted filesystem capture is retained when possible.
If capture is impossible, recovery of effects after the last committed bundle
is **not guaranteed**, and that limitation is recorded before shutdown. No
automatic retry, reset to an earlier world, permission repair, or action replay
is performed. Explicit inspection is required to resolve an interruption.

Supported file bytes, types, modes and links persist; process/KV state, `/tmp`,
timestamps and inode-number identities do not. Unsupported special files can
cause an honest fault rather than an incorrect completeness claim. Data quotas
do not bound all kernel metadata. `verify_store` checks the complete committed
event/bundle/receipt chain, copied parent bytes, dependencies and object hashes.

Run tests with the existing environment:

```sh
/workspace/cache_backend_venv/bin/python -m unittest -v test_garden_world
```

These tests use real disposable namespaces, including read/write and restart,
ordinary errors, notebook-full cleanup, process isolation, physical limits,
host-symlink protection, unknown partial outcomes and interrupted notebook
batches. They make no model calls and never change the original garden.
