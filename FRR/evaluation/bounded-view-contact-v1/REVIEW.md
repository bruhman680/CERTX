# Independent bounded-view review

13 November 2026, America/Chicago. Source review plus tokenizer-only boundary tests and retained-artifact audit. No weights were loaded, no model inference or generated code executed, and no canonical garden file was changed by this review.

## Supported result

The new selector implements a simple content-independent policy: preserve the exact two initial messages and a contiguous suffix of complete assistant/receipt pairs. The count limit is applied first; if the selected suffix is too large, only whole oldest pairs are omitted until it fits. The newest pair is mandatory. If initial framing plus that pair is too large, selection raises `ViewCapacity` instead of truncating or discarding the latest consequence.

No material implementation defect was found for the actual thirty-exchange source archive. The inputs at 4/8/12 retained pairs occupy 1,163 / 2,231 / 3,299 tokens, versus 8,104 for the full source conversation. All three outputs are capped unfinished writing and exactly match prior text. These are three selected deterministic conditions, not three independent replications, and they establish no improvement in reasoning or action.

## Boundary tests

`test_edge_cases.py` passed **12 of 12** tokenizer-only cases in `TEST_RESULTS.json`:

- Exact actual suffixes and entry ranges for all three declared views, preserving roles/text and original framing.
- No mutation of the source archive or aliasing of returned initial framing.
- Empty/small archives without unnecessary omissions.
- Token-budget fallback that omits whole old pairs while preserving literal newest receipts, including whitespace and fenced-looking text.
- Oversized mandatory receipt and oversized initial framing pause explicitly.
- Exact token boundary fits; one token less rejects the same mandatory input.
- Duplicate/out-of-order records are rejected even if they would have fallen outside the retained suffix.
- Missing receipts, nontext content, boolean identifiers, unexpected fields, invalid limits and malformed framing reject explicitly.

Synthetic receipt fixtures are tests of selection mechanics; they are not model behavior or new world events. A count-limited policy is not a guarantee of indefinite operation: an unusually large latest result can still exceed the input budget, and world storage/resource limits still exist.

## Independent artifact audit

`audit.py` uses the cached tokenizer and ordinary record reads. `AUDIT.json` verifies the complete source archive against current canonical entries, the exact retained role sequence and token IDs for each view, included and omitted entry IDs, raw text decoding, stop/cap metadata, parser output and final results rows. It checks that the canonical tree still matches the probe's pre-inference inventory and remains unchanged by the audit. It does not independently repeat the parent's inference or verify weights by reloading them; those are the parent runner's successful before/after assertions.

## Two important scope boundaries

First, this contact changes only the immediate input of detached inference. The live garden remains paused at1580. The inherited `WORLD_RULES.txt` describes the original full-history body/continuity condition. Before adopting a bounded view, create a declared consistent condition and reconcile that model-visible description. Do not silently patch the live pinned source or present the altered view as unchanged full-history token continuity. The model/world laws and decoding settings can remain stable while the view policy is explicitly versioned.

Second, **preservation of an observer-side archive is not automatic access by the model**. Host run/event files and `SOURCE_ARCHIVE.json` retain the complete history for review; the model's sandbox cannot read arbitrary host research paths. Its world notebook retains reply writing, but that is not necessarily a complete accessible log of all older receipts and metadata. This selector supplies no retrieval tool or world-side feedback archive. Omitted exchanges therefore leave the immediate input, and the model should not be claimed to remember or retrieve all of them. A future accessible retrieval mechanism would be an additional design condition with its own tests.

## Readiness interpretation

The mechanics are suitable as a transparent candidate input policy, with explicit included/omitted IDs and mandatory-latest capacity behavior. The source and full canonical history are intact. The data do not select 8 pairs as an empirically best reasoning setting: it is an engineering tradeoff among retained history, available capacity and compute. The smaller prompt alone did not change the observed repeated output in this contact.

These tests do not demonstrate sustained world continuity under the new view, fifty-reply operation, successful use of older files, acquired memory, behavioral improvement or emergence. Deployment, a multi-turn bounded-view world trial, source/version pinning and crash/recovery guarantees remain distinct follow-ups. No hidden summary, evaluator feedback, forced code closure or success gate is justified by these results.

## Addendum: detached readable-archive prototype

After the input-view review above, the parent executed a separately declared operator staging probe, `archive_probe.py`. I read its source, plan, initialization/read receipts and `ARCHIVE_RESULTS.json`; I did not repeat its execution or run a model.

The probe copied the source condition's exact initial messages and thirty assistant/receipt records (entries1551–1580) into ordinary files under `/world/conversation_archive_v1` on a **detached copy** of the current world. It created an index and one file per entry. The initialization receipt exited0 and printed30. Every original world path retained the same supported metadata/content entry; all new paths were inside the declared archive namespace.

The probe then closed the world, reopened its checkpoint and used an operator-written Python read program to reconstruct the payload from those files. That actual read exited0 and returned the expected SHA-256 digest, `cbd0d2dd4bfd3e7bdef7ec32acb77e8b7b428357e0532e542bebb0831e6bac55`. The read caused no captured path changes. The detached world-store verifier passed at step2, and the canonical candidate inventory stayed unchanged according to the completed probe assertion.

This narrows the earlier archive-access caveat: **a world-side, filesystem-readable archive of these thirty records has now been demonstrated on a copy**. It remains operator-staged data and operator-tested readability. The model did not choose to locate the index, write the read program, retrieve an older receipt, use it in reasoning, or successfully act on it. It does not include all pre1550 historical episodes merely because the broader repository preserves them elsewhere.

The archive files are ordinary model-writable files in this prototype. Their contents could later be changed within the world; the preserved observer originals remain the authoritative historical record. Future per-turn synchronization, namespace/conflict behavior, growth/quota handling and publication of readable receipts require an integrated declared policy. No such synchronizer or runnable wider-block runner was deployed by this probe, and the inherited world-rule declaration has not been updated for adoption. The live garden remains paused at1580.

The combined evidence therefore supports a tested selector and a tested readable-storage building block, while sustained bounded-view operation and actual model retrieval remain unobserved. These findings should not be compressed into a claim that the model already has reliable long-term retrieval or that fifty-turn continuation is ready unchanged.
