# Initial candidate-world code review

9 November 2026, America/Chicago. Review of the first written `minimal-garden-candidate-v1/world/garden_world.py`. Findings were sent to the builder/root before activation. This is a development review, not a final pass or an assertion that these issues remain in the final code.

## Confirmed useful properties

- Imports the existing frozen sandbox dependency without modifying it. Records source and guest executable dependencies for candidate stores.
- Creates its own store and copies the supported entry-1550 bundle/objects rather than replacing the old phase.
- Notebook writing occurs via guest Python using literal repr and shell quoting, avoiding host writes through model-controlled symlinks.
- Snapshot observation returns manifests and actual receipts, without following arbitrary guest paths on the host.
- Preserves the exact raw reply and parser source offsets; applies a prospectively defined notebook grammar rather than repairing arbitrary fragments.
- Declares note-append-before-cells, eight-cell preflight, separate-process variable lifetime, and continuation after known cell errors.
- Each operation uses pending evidence before execution; uncertain execution/capture failure retains recovery evidence and does not automatically replay. Multi-cell batches retain an additional pending marker.

## Findings requiring resolution or explicit scope

**High: close failure cleanup.** In the initial close implementation, `checkpoint()` can raise before `_guest.close()`, while the outer finally still removes the owned lock and sets `_closed`. A live namespace can remain with no clean pause. Required: terminate the guest in a guaranteed finally, preserve the mismatch or uncertain-state evidence, and do not claim a clean pause. The builder was asked to add an injected-checkpoint-failure test.

**Medium: record-chain verification.** Opening checks dependencies and restores/captures the latest bundle, but initially did not verify STATE.last_event_sha256 against the event file or replay the event/bundle linkage. This does not establish corruption under normal operation; it is a missing verification step for a durable-record integrity claim. Either the world wrapper or root's owning runner must verify committed history before resume, and tests should demonstrate tampered state/event detection without model calls.

**Grammar scope: unsupported outer fences.** The first parser recognizes only exactly three backticks followed by an ASCII alphanumeric/underscore/hyphen label or no label. An outer fence with an unsupported info string or longer marker is ignored, so an inner recognized `python` cell can execute. This is predictable under that narrow dialect but conflicts with a broad promise that unknown fences shield their contents. Resolve by shielding a clearly defined broader set of outer fence markers, or narrow the public law precisely and test examples. Do not describe it as unrestricted Markdown or semantic intent recognition.

**High: ordinary notebook-write failure became an action gate.** The initial notebook route appended the whole reply to notebook.txt before executing cells, then skipped every cell when that append failed. At the per-file limit, this would also block a valid cell deleting or truncating the notebook, unlike the legacy action path. External raw evidence already preserves the model reply. Root and builder agreed that a known note-write failure must return its actual receipt while leaving declared code cells able to execute; no silent retry or repair is needed. A concrete full-notebook cleanup test is required. Unknown effects or uncheckpointable state still pause separately.

The review does not propose executing code based on estimated intention. Supported cell boundaries must remain explicit, mechanical, declared and retained. Incomplete or unknown regions should remain inert under the final declared law.

## Acceptance still pending

Runtime tests, model-generated read/write, actual error receipt followup, exact pause/resume reconstruction, and an open invitation pilot are separate evidence categories. The code review alone does not confer working-foundation status. A completed build should report them separately, preserving ordinary free writing and model failures rather than inventing success.
