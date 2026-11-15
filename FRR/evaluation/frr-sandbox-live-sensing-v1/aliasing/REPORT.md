# A complete directory packet can hide a consequential difference

15 November2026, America/Chicago. **Zero new model calls, zero new world actions, zero world opens.** This is a read-only check of real previously saved worlds and their previously recorded program consequences. Only new code/results/report files in this aliasing directory were written. The current main and the M2 engine/instrument were not edited.

## The witness

The completed history-retrieval study contains paired `transfer_a` and `transfer_b` worlds. Their saved **pre-artifact** snapshots are `bundles/000001.json`, not their final post-execution notebooks. Both contain43 supported entries. Every path, kind, mode and byte count matches. The sole differing supported entry is the content hash of `probe_value.json`:

| World | Actual decoded JSON | File bytes | Previously saved read stdout |
|---|---|---:|---|
| transfer_a | `{"value": "K7M4Q9"}` |19|`Value: K7M4Q9`|
| transfer_b | `{"value": "R2V8T6"}` |19|`Value: R2V8T6`|

The frozen R&D `snapshot_packet_v1` instrument was applied as a **pure metadata function** to each saved bundle, using the same truthful timing/counters: `timing="initial"`, `world_step=1`, `reply_index=null`, and8192-byte packet allowance. It lists all43 entries; no entry was selected or omitted for this demonstration.

Both model-facing packets are byte-identical: **3393 UTF-8 bytes**. Their common packet hash and complete serialized text are retained in RESULTS.json. Observer-side source bundle IDs differ, as do the decoded target-file contents and their CAS hashes. The bundle IDs are deliberately absent from model-facing text, consistent with the instrument's design.

## Existing functional consequence, not a new experiment

The old `program-transfer/RESULTS.json` names these exact snapshots in its `before_id` fields. Its two saved notebook batches contain **the same full generated text and the same complete Python-cell source**. They first append the identical notebook text, then the same program opens `probe_value.json`, parses JSON and prints the field's value. Existing real receipts show the differing stdout values in the table, exit0 and no runtime boundary. Python execution changes no supported file path in either world.

The check joins each batch operation to the matching saved world event, verifies parser/source correspondence, matches the source artifact text and cell-source hash across worlds, and confirms result before/after IDs. Both source stores pass the existing read-only `verify_store` checks for committed event/receipt/bundle ancestry and CAS bytes. Target payloads were decoded and hash/length-checked; these are not invented or merely shape-valid synthetic metadata fixtures.

Those program executions happened in the earlier study. **They were not rerun here**, and they are not new independent model solutions, FRR comparisons or M2 trajectories. The source study already labels its two artifact executions as zero additional model calls. The present check adds only a deterministic projection-and-provenance calculation.

## What follows

Let `O` be this directory projection and let `sA`, `sB` be the two supported file states. This witness has:

`sA != sB`, but `O(sA) = O(sB)`.

The same saved file-reading operation has different actual consequences on those states. Thus the packet is **complete for its chosen metadata fields**, but those fields do not determine all file contents or all possible operation consequences. Updating such a packet after every reply would not make it a complete view of the universe or the model's internal computation.

The qualification matters in both directions. This does **not** establish that directory sensing is useless. Names and byte counts can reveal additions, deletions and growth, and may alter behavior. It does not establish that the small model will choose a useful read, understand a packet, retain a discovery or improve. It merely identifies an information boundary of the observation instrument.

Nor does this claim that two **full model inputs** must remain indistinguishable. If actual file-read receipts return, they contain different values and can separate the worlds. Prior history might also distinguish them. This witness concerns the directory packet alone, with matched timing/counters; the planned closed loop includes other information channels that must remain separately recorded.

For M2, “live” should therefore mean **truthfully refreshed metadata after known effects**, not full observability, automatic comprehension or access to internal reasoning. A complete external observer record of the supported CAS state is also a different object from the smaller model-visible packet. Neither establishes complete native-host or neural-state observability beyond its declared scope.

## Reproduce without touching a world

Run the cached Python environment with bytecode writes disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 /workspace/cache_backend_venv/bin/python check_aliasing.py
```

The default prints a short check summary and creates no result file. To save a new result, pass `--write-results NEW_NAME.json` inside this directory; existing paths are refused. The function does not follow file paths from metadata, open a guest, execute a notebook, generate model text or load untrusted pickle data.

`RESULTS.json` records source/version paths and SHA256 pins for this checker, the frozen instrument, source plans/results/artifact, bundles, world manifests/states, batches and relevant runtime source files. Source-tree inventory equality and instrument-hash equality were checked before/after. This preserves the distinction between validating saved data and conducting a new world intervention.

Sources: [frozen instrument](../../frr-sandbox-rd-v1/interface/instrument/snapshot_packet.py), [previous artifact check](../../history-retrieval-three-cycle-v1/program-transfer/RESULTS.json), and the source records/pins enumerated in RESULTS.json. No external paper or new behavioral mechanism is claimed by this local witness.

## Observer date-basis correction

The child initially inherited14November client context. Root subsequently relayed the updated15November America/Chicago client date. The new stage's observer date labels were corrected without rerunning the projection check or changing packet/world evidence. RESULTS.json records that label-only revision and the original executed checker hash; its exact bytes remain in check_aliasing_before_date_basis_update.py. Historical R&D14November source files were not edited.
