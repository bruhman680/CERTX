# Bounded view and accessible-history contact

**Follow-through:** the [integrated detached prototype](../bounded-view-continuation-prototype-v1/REPORT.md) completed three consecutive replies with the same view, persistent world and per-turn archive-copy mechanism. It is not selected as the main run. [Exact-input/output loop finding](FIXED_POINT.md).

13 November 2026, America/Chicago. Main garden remains paused at **1580**. All tests here are detached; no live policy, instruction, world law, weight or main entry changed.

## Findings

| Input view | Included entries | Input tokens | Output tokens | Complete cells |
|---|---|---:|---:|---:|
| Full source conversation | 1551–1580 | 8104 | not generated | — |
| Latest4 complete pairs | 1577–1580 | 1163 | 256 | 0 |
| Latest8 complete pairs | 1573–1580 | 2231 | 256 | 0 |
| Latest12 complete pairs | 1569–1580 | 3299 | 256 | 0 |

The smaller views fit the7936 input limit. All three produce exactly the same prior unfinished text. They demonstrate input feasibility, not better reasoning, action or retrieval. One deterministic generation per selected context is not three independent learning trials. The over-limit full input was not run.

The initial empty-system/mechanics/invitation messages and greedy256 CPU float32 eager model remain identical. Selection keeps complete assistant/actual-receipt pairs chronologically, with no summaries, extra hints, scores or semantic relevance ranking. Included and omitted IDs, full source archive, exact input IDs and raw outputs are retained. The three shorter runs took23.6,38.8 and55.4 seconds; these single timings are not controlled performance benchmarks. No generated code executed or entered the main history.

## Tested selector

`view.py` keeps at most N latest whole exchanges, dropping only older whole pairs if the budget requires it. The initial framing and latest pair are mandatory. If those alone exceed capacity, it pauses instead of truncating the newest receipt. It validates record types/order/framing and does not mutate the source.

Independent tokenizer-only tests passed **12/12**, including exact4/8/12 suffixes, whole-receipt preservation, no mutation, budget fallback, exact capacity boundary, oversized-latest pause and malformed inputs. `AUDIT.json` verifies the retained views/raw outputs and unchanged823-file canonical inventory. Recency is still a design bias. Eight is a possible engineering trial value, not an empirically best count. A sufficiently large latest receipt still stops this policy, so arbitrary block lengths are not guaranteed.

## Preserved data versus model access

The review found an important gap: the observer's full raw/event archive is outside the model sandbox. Its notebook preserves writing, not an automatically complete journal of old tool receipts. Omitted feedback does not become model-retrievable merely because the host retains it.

`archive_probe.py` therefore created an independent copy of the exact1580 world. One explicitly operator-written action staged ordinary files under `/world/conversation_archive_v1`: the exact initial messages and30 actual source assistant/receipt records, with a chronological index. This covers1551–1580, not all pre1550 history. This particular main trajectory has empty notebook-success receipts; it is not a past nonempty-error retrieval episode.

After closing and reopening the clone, an operator-written Python read reconstructed the full payload with the exact source digest and no file changes. All original world paths remained unchanged. Source, receipts, objects and `ARCHIVE_RESULTS.json` retain the proof. The files are ordinary model-writable data; authoritative observer originals remain separate. This demonstrates filesystem readability and persistence. The model was not asked to retrieve anything and did not choose a retrieval action.

No per-turn archive synchronization, collision handling or integrated wider run was implemented. Existing8MiB world and256KiB per-file bounds apply. Long-run behavior must handle edits/deletions and storage faults rather than silently restoring preferred file contents.

## Before adoption

The inherited `WORLD_RULES.txt` explicitly describes full-history input. A new live view condition must declare the memory change and keep that mechanical description accurate. The test did not rewrite it. A preserved1580 parent and explicit continuation lineage can retain the world/counter without silently altering the frozen reference.

The concrete next integration is: fixed recent-pair selection with inclusion logs; a defined path to older actual records; archive update/collision/storage rules; consistent body/view declarations; and a small consecutive pilot. Preserve the original invitation and avoid mandatory retrieval or success requirements. The view is a causal intervention to test, even when selection is content-independent.

The selector and readable snapshot are now concrete and tested. An integrated runner is **not deployed** and fifty replies cannot yet resume under a new policy. Main remains1580 under its old contract; unchanged resume still pauses at8104 tokens. No background job is scheduled.

Evidence: `PLAN.json`, `RESULTS.json`, `SOURCE_ARCHIVE.json`, `views/`, `raw/`, `TEST_RESULTS.json`, `AUDIT.json`, `REVIEW.md`, `ARCHIVE_RESULTS.json`. Existing local compute only; no paid inference endpoint or model download.
