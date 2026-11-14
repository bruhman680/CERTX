# Detached bounded-view continuation prototype

13 November 2026, America/Chicago. Main garden remains **1580** under its original full-history contract. This new detached candidate inherits that exact world, declares an eight-pair input policy and readable history copies, then makes three actual model calls labeled **candidate1581–1583**. No main activation or canonical counter change occurred.

## What was built and observed

- Fixed latest-eight complete assistant/receipt pairs, exact initial framing retained, oldest whole-pair fallback to7936, latest pair never silently truncated. Full authoritative external history continues to accumulate.
- Same cached135M model, CPU float32 eager/two threads, original greedy256 generation function, fresh KV per reply. No training, adapter, endpoint, seed revision, coaching or imposed success target.
- Exact parent1580 filesystem copied into a new store; initial operator actions add ordinary history files and update only the cloned WORLD_RULES body/view declaration. All other parent paths remain unchanged at initialization. Original rule bytes are retained externally.
- Three consecutive replies through one persistent world, closed/reopened between turns. Every reply is passed unchanged through the existing notebook parser and gets actual feedback. Three new history records were copied successfully. Final operator read after reopen reproduces all33 authoritative records exactly in this actual no-copy-error pilot.

| Candidate entry | Input tokens | Output tokens | Complete cells | Archive-copy exit |
|---|---:|---:|---:|---:|
|1581|2231|256|0|0|
|1582|2231|256|0|0|
|1583|2231|256|0|0|

The three exact input-token sequences are identical. Recent exchanges contain repeated identical text and empty actual receipts; silent successful copying changes files but adds no prompt content. With the fixed model and greedy decoder, all three outputs also repeat the prior unfinished text. This is an observed deterministic input/output fixed point for this block, not evidence of maturation or useful new memory. File growth is not automatically information in the immediate input. No model-originated archive retrieval was observed.

## Readable history and error semantics

`/world/conversation_archive_v1` holds the source condition's initial messages and entries1551–1580, followed by files1581–1583. Its initial index is explicitly static; `entries/` can be listed for later files. It does not claim all pre1550 conversation coverage. Ordinary files are model-writable: edits and deletions are allowed, while authoritative observer originals stay outside the world.

Each world file stores the assistant reply and its **model-action feedback**. A copy cannot contain the receipt about its own creation without self-reference. Successful copy adds no model-facing receipt, so the stored action receipt then equals final feedback. On a known copy failure, the actual `history_archive` receipt is appended to final model-facing feedback and retained externally. The in-world record may be absent, collided, partial or edited; it is never silently rewritten to fix that. Final archive equality/read errors are observations, not a gate or reason to restore model files.

Copying uses exclusive creation in existing ordinary archive directories. Existing final paths are not overwritten; replaced symlink parents or missing parents return an actual error rather than being repaired. Existing finite world/file/output limits apply. A large latest receipt can still cause a capacity pause. No unbounded storage, unlimited generation, general recovery or power-loss durability is claimed.

## Actual failure-path tests

Two separate operator-created fault worlds, with zero model inference, tested file collision and symlink-parent replacement. Both produced known copy errors without overwriting or repairing the existing file/link. The exact failure entered combined feedback, a following ordinary Python cell succeeded, and close/reopen checks preserved both the fixture and the later cell's effect. Full initialization/setup/copy/read receipts and store verifications are retained under `faults/` and `FAULT_TEST_RESULTS.json`. These are specific sandbox mechanism tests, not all possible archive/storage faults.

## Integrity and scope

Source pins and model parameter digests matched before/after. The823-file non-cache canonical inventory and ACTIVE pointer remained unchanged. The candidate world verifies cleanly at its final paused checkpoint, with no pending marker. Every selected view, full authoritative history, raw token sequence, model batch, operator copy event, before/after world ID and record hash is retained. `AUDIT.json`/`REVIEW.md` contain the independent artifact audit when complete.

This is a narrow fixed-three-loop prototype, not an activated or general-purpose long-run resume service. Wider blocks and automatic sessions are not demonstrated. The existing source intentionally refuses an already initialized STATUS rather than replaying the same entries. During execution, a between-loop STATUS paused flag means the physical world checkpoint is closed; only completed stage plus absent pending/locks identifies this settled pilot. See RESUME.md before any next work.

The prototype shows one integrated way to bound input while maintaining readable copies and exact external records. It does not show improved reasoning, successful self-repair, voluntary retrieval or that eight is an optimal window. No result or candidate history is silently promoted to the main trajectory.
