# Snapshot packet instrument — NOT WIRED INTO PILOTS

This is a pure observer-side projection of an **already verified, committed supported-world snapshot**. **Completeness means all entries in that supported representation, not complete observation of native OS metadata or every environmental context dimension.** Verification of a bundle does not prove that its capture schema represents every such dimension. It does not start a model, open a sandbox, execute an action, alter a world, interpret a rule file, or activate M2. The existing M0/M1 inputs and results remain unchanged.

`snapshot_packet.py` accepts the captured bundle object and explicit timing/counters. It emits every current supported path in stable lexical order with its kind and logical regular-file payload size. It contains no task, suggested command, preferred file, score, reward, novelty threshold or selective ranking. Canonical ordering is a representation choice, not a claim of neutrality.

## Python API

```python
observation = make_snapshot(
    verified_bundle,
    timing="after_reply",       # or "initial"
    world_step=4,               # supplied actual committed operation counter
    reply_index=3,              # positive branch reply index; None for initial
    max_packet_bytes=8192,      # explicitly chosen observation-byte budget
)
model_text = observation.model_text
observer_record = observation.observer_record
```

`model_packet` and `model_text` contain only the path, timing, world step, reply index, and complete names/types/bytes list. Source bundle ID, root mode, provenance and instrument metadata are in the separate `observer_record`. That record must not be accidentally concatenated into model input.

This proposed schema adds explicit timing/step/reply fields to the earlier M1 packet. It is not a silently interchangeable M1 replacement. Any future live-versus-initial-only comparison needs the same new initial packet in both conditions; otherwise the initial schema change is another factor.

The step is a committed operation counter, not an autonomous tick or wall-clock timestamp. Initial/after-reply timing and reply indices are **caller-provided facts** whose types are checked, not independently established by this function. Calling it with an old snapshot and labeling it “after_reply” would remain false even if the JSON passes. A future controller must obtain the known after-effects checkpoint first, preserve actual runtime receipts separately, and never describe an unknown/pending action as a settled observation.

## Meaning of byte counts and links

- Regular file: captured payload-byte length.
- Hardlink: the target regular file's logical payload-byte length, not additional disk use.
- Directory, symbolic link or FIFO: `null`; no regular-file payload length is claimed. This is not the same as zero or empty.

Link targets and mode bits are validated as supported metadata, but are not added to the model packet. Symbolic-link text may be absolute or contain parent components; it is never followed. Captured entry paths must be relative, unique and have explicit directory ancestors. Hardlinks must name a captured regular file. No path appearing inside the bundle is opened by this projection.

Modes match the current source format: `final-garden-contract-v1/world.py` captures file/directory/FIFO/root modes using `st_mode & 0o777`. The instrument checks these nine permission bits. No model chmod action occurred in these pilots, and no such runtime fault was observed. This remains a future capture-fidelity audit question, not a reason to change current physics. The source bundle does **not** expose sticky/setuid/setgid bits; this instrument cannot recover them or claim complete native-filesystem mode fidelity. A future different capture schema needs a separately reviewed format update.

## Validation scope and capacity

Checks cover basic JSON/schema values, supported kinds, row shapes, modes, path relationships, hash *shape*, byte-count types and timing/counter types. They do **not** recompute source bundle identity, verify event ancestry, read content-addressed object bytes, validate storage quotas, or prove that a live world matches the snapshot. The existing world verifier remains responsible for those matters. There is no special requirement that WORLD_RULES.txt exist or contain approved text; the model can create, delete or change ordinary files under its world laws.

The complete JSON text is serialized first. If it exceeds `max_packet_bytes`, `PacketCapacityError` reports required bytes, limit and entry count. No partial packet is returned. Entries are never omitted to fit, selected for interestingness, or silently truncated. The caller's future protocol must decide what an observation-capacity pause means before running anything.

This is a **serialized UTF-8 byte limit**, not a tokenizer/context limit or a hard input-memory/CPU limit. The caller must separately measure the entire model input, including framing, FRR and history. A packet fitting8192 bytes does not establish that a7936-token conversation fits. `ensure_ascii=True` and JSON escaping keep literal newlines/quotes/control characters inside data strings escaped; that is syntactic handling, not semantic prompt-injection prevention. Filenames can still carry influential text.

## CLI separation

The CLI reads only its explicitly supplied bundle path. Standard output is the exact model-facing JSON text, without an extra newline. An optional `--observer-record PATH` writes provenance separately with exclusive creation; an existing path is not overwritten. No output directory is created automatically.

On metadata, capacity or file errors, stdout remains empty and a structured **observer error** goes to stderr with exit2. That error is not a fabricated world-action receipt and is not automatically passed to any model.

## Tests and current status

`test_snapshot_packet.py` reads the existing R&D control's prepared and final captured bundles, matches them to prior preparation/action records, and independently compares each regular-file length with decoded, hash-checked CAS bytes. It does not open a world or rerun model actions.

Separate synthetic metadata fixtures check six entries after addition, four after deletion, unusual filename JSON round-trip, directory/symlink/FIFO/hardlink projection, representative malformed metadata, and exact-budget/overflow behavior. These fixtures are explicitly not newly observed worlds and do not claim valid cryptographic ancestry. A CLI check verifies stdout/provenance separation and empty stdout on overflow. Temporary CLI files are confined to a test temporary directory.

The test command prints results without changing prior records; an explicit `--write-results NEW_PATH` saves a new record with exclusive creation. `TEST_RESULTS.json` records the passing outcome: **zero model calls, zero sandbox opens, no M2 run**. No existing pilot imports or invokes this instrument. The evidence supports this observer helper, not a claim that live sensing improves behavior or that the small model has learned.
