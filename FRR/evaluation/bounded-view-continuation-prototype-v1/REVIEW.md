# Independent prototype review and artifact audit

13 November 2026, America/Chicago. Read-only source/record review and tokenizer audit. No model inference, world operation, canonical mutation or repeated runtime test was performed by this reviewer.

## Audit outcome

`audit.py` completed with **PASS** in `AUDIT.json`. The original main garden remains paused at1580. The three detached candidate replies are numbered1581–1583 in their own lineage; they are not new main-garden entries. The final detached world-store verifier passes at step8 and no pending marker or world lock remains.

The audit independently checks:

- Source archive and initial framing against the thirty actual main exchanges; exact parent1580 bundle and pinned source hashes.
- Unchanged original world entries except the explicitly declared `WORLD_RULES.txt` update, with new paths confined to the ordinary archive namespace during initialization.
- Exact seeded archive records and exact updated rule bytes in the initial candidate world.
- Each complete eight-pair chronological input, omitted/included entry IDs, exact role text and tokenizer IDs, raw decoding and unchanged greedy decoder metadata.
- Model batch and individual world-event copies, canonical action-receipt projection, archive-copy events, final combined feedback, record/raw/batch/archive-event hashes and before/after world links.
- Successful new entry files against their exact assistant/model-action receipt payloads, with exclusive new paths on the actual successful pilot.
- Final external authoritative archive, final read-operation linkage, clean pause and canonical candidate inventory preservation.

Weight equality and pointer preservation are the builder's successful before/after assertions, not an independently repeated model load. Current pointer/main state and the canonical file inventory remain consistent with the declared unchanged main lineage. There is no durability or hard-crash proof in this artifact audit.

## What the pilot demonstrates

The prototype combines a bounded input selector, a continuing copied world, ordinary readable archive files, actual feedback and per-turn exclusive copy operations. All three input sequences contain2,231 tokens. Each reply reaches256 generated tokens with an unfinished Python fence and no model-originated executable cell. The notebook appends and automatic copies succeed. The final operator read after reconstruction matches all33 records in this successful pilot.

These are working integration results for a small detached candidate. They do not demonstrate fifty-turn operation, reliable model retrieval, meaningful self-correction, acquired knowledge, an improved decoder or a new developmental phase. The copied archive is ordinary world data; its construction and verification are operator actions, not model discoveries.

The initial index is explicitly static for the imported records. Later entries are discoverable by listing the entries directory. The rules document that fact and distinguish source1551–1580 from the earlier pre1550 archive. The prototype does not silently claim to expose every earlier historical episode to the model.

## Exact input/output fixed point

The audit finds **one exact input-token sequence and one exact output-token sequence across all three pilot replies**. This is stronger and narrower than merely saying that the text looked repetitive. Human entry IDs change in external metadata, but they are not inserted into the selected chat messages. The last eight assistant texts are identical, and their delivered receipts are empty. A successful archive copy is deliberately silent in model-facing feedback.

Write B for the unchanged initial framing, x for this identical unfinished reply and ε for empty feedback. Under the observed conditions:

`I = B + eight copies of (x, ε)`

`G(I) = x`

Shifting out the oldest identical pair and appending another `(x, ε)` leaves the immediate input I unchanged. Fixed weights, greedy selection and fresh KV therefore reproduce the same tested I/O condition. The world still changes through notebook/archive growth, but this growth supplies no new perceptual text while writing and copying continue successfully.

This is a **conditional observation-level fixed point**, not a global claim that the model can never change or that the world stops evolving. An ordinary quota/write failure, a real code action and its output, a different observation, or a separately declared decoder/view change can alter the conditions. Physical resource growth may eventually produce a receipt; neither its timing nor a beneficial response is established by this three-turn pilot. The result should not be described as intrinsic maturation or spontaneous sophistication.

## Copy failures, writable files and the source refinement

The world files are model-writable. Exclusive creation protects existing entry paths from automatic overwrite; checks reject replaced symlink or missing parent directories without reconstructing them. Known copy failures are represented as actual `history_archive` receipts, while later lawful world actions remain possible.

The builder's separate no-inference fault tests report a file collision and a symlink-parent case. Both retained the affected model-created state, produced the expected failure receipt, allowed a following operator-written ordinary cell, survived reconstruction and passed store verification. They test copy/error mechanics; no model response to either injected copy fault was generated.

Review identified and the builder corrected an important policy issue **before launching the pilot**: a final archive-equality assertion would have treated legitimate edits/deletion of older ordinary archive files as an integrity failure whenever all new copies had succeeded. Equality and final read outcomes are now observations, not success gates. Model edits remain preserved; the authoritative observer history and actual world-store integrity are checked separately. The correction does not modify canonical source or history.

The per-turn file contains the assistant text and **model-action receipt**, not the receipt of copying itself. If copying fails, the final delivered/external feedback additionally includes that copy failure. A failed or partial world copy must not be claimed to equal the complete final model-facing conversation. The successful pilot's equality is a measured result, not an invariant requiring every future mutable copy to remain untouched.

## Operational boundaries before adoption

This is still a detached prototype. The main pointer was not activated, and no body/view changes were injected into the original garden. Adopting it would require a declared lineage and consistent version/pin/export/resume policy. The source refuses an existing STATUS and is not a general resumable job runner. `paused:true` between loops describes a closed world checkpoint, not proof that the entire job has finished; use the stage, pending state and completion artifacts together.

Pending records preserve unknown completion, but ordinary file writes for status/pending markers do not constitute a complete power-loss protocol. The tests do not cover process death at every copy/checkpoint boundary, shared-filesystem concurrency, indefinite quota growth or every Python/OS facility. Large newest receipts can still exceed the selector's mandatory-latest budget and pause honestly.

The strongest supported conclusion is that this candidate can maintain the tested bounded view and readable copy archive over three verified steps, while its exact input/output remains unchanged. Continuation can be an observation of that lawful state; behavioral success is not an admission criterion. It should not be promoted as a demonstrated solution to memory, retrieval or reasoning merely because the context-capacity pause has been mechanically avoided in this pilot.
