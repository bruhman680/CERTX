# Paged retrieval, portable reconstruction, and first Scheme interface pilot

6 November 2026, America/Chicago. **Host features implemented and checked; ten isolated fixed-model calls completed. Original garden remains paused at 500.** This is a new versioned study; the earlier blueprint/prototype and its evidence remain unchanged.

## Main result

The prototype now exposes bounded pages of retained procedure source, data and previously omitted pure-run results. It can export a data-only bundle and reconstruct a new database preserving state, history, dependency captures and request identity. Host checks passed.

The first small-model interface pilot produced **0/10 accepted actions**, with **0/8 requested outcomes achieved** and two unscored free-choice turns. This is a scoped interface failure under one syntax card and two fixed seeds, not evidence that the host machinery failed or that the model can never use Scheme. No longer model season was started.

## Engineering work

Implementation is isolated under [prototype/](prototype/), copied from the previous build before changes. Scheme value semantics and the deployed model/adapter were not changed. Shared limits are [provisional fixtures](constants.json), not measured optima.

### Retrieval

`(page target field cursor count)` returns a page of procedure `source` or data `value`. Target can be a current alias or retained immutable artifact ID. Source is literal saved Scheme text. Data pages contain the canonical tagged-JSON representation; join chunks before decoding. Offsets/counts are **Unicode scalar positions in that representation**, not UTF-8 bytes, grapheme clusters or list indices. Each page also reports actual chunk UTF-8 bytes.

`(page-run "request-id" cursor count)` reads a retained successful pure-run result without rerunning it or creating a guest artifact. Compact responses now expose the request ID and avoid duplicating the projection. Large pure results omitted from the initial view can therefore be recovered afterward.

The cursor binds current snapshot, immutable target, field and offset using a full digest. It is a consistency fingerprint, not a secret or authorization token. A changed snapshot, target, field or malformed offset invalidates it. Page size shrinks when escaping/Unicode would exceed the response budget. Reading appends a host audit receipt but leaves the guest snapshot unchanged. Retained revisions remain readable after their friendly name is dropped. Request/receipt bytes are retained; page projection byte counts are recorded. Complete aggregate model-token/transport delivery accounting remains outside this feature.

### Portable bundles

The host-only transport exports fixed-table records, canonical artifact/snapshot/capture/request/event bytes, profile/version declarations, per-table checksums and an overall checksum. The bundle is JSON data, not an SQL script or executable. No member selects an output path; the host chooses the destination. Export leaves the source world unchanged and does not overwrite an existing bundle.

Import validates bounded input, schema, versions, profile, table shapes/checksums and settled request status before reconstruction. It builds a separate temporary database, verifies hashes/relationships, recompiles procedure and captured-expression sources against their pinned bindings, checks quota counters/receipts, checkpoints the database and publishes it atomically without overwriting a target. Known malformed bundles, missing dependencies, incompatible versions/profile, forged receipt projections and counter changes are rejected. Checksums authenticate consistency with recorded bytes, not authorship or an external source of truth.

This reconstructs retained state and audit history; it is not re-execution of every historical action or infrastructure interruption. After import we tested new pinned calls, continued an explicit checkpoint, and obtained the exact original receipt for an exact prior request. Interrupted evaluator counters remain unknown when unavailable; conservative quota charges remain separate from measurements.

## Host validation

[Host checks](CHECKS.json) record **46/46 tests passed**, **124/124 Chibi Scheme value comparisons matched**, and the retained **19-action host walkthrough’s 10 assertions passed**. [Unit results](UNIT_CHECKS.json), [test log](HOST_TEST_LOG.txt), [reference results](REFERENCE_CHECK.json), [walkthrough](HOST_DEMO.json).

Fifteen new tests cover Unicode source/nested-list reconstruction, pure-result retrieval, escaped response limits, cursor binding, immutable access after alias removal, export/import state and exact retry identity, pinned behavior/checkpoint continuation, existing-destination preservation, checksums/dependencies/versions/profile, duplicate JSON keys, size limits, unsettled requests and resealed counter/receipt tampering. The prior 31 host checks remain included. The source/profile hashes used in these checks remain unchanged; pilot tooling added afterward is separately pinned by its pre-call plan.

Finite tests do not prove all Scheme semantics, arbitrary-data robustness or adversarial security. Limits remain POSIX/Linux-oriented. Exact host-work costs and comprehensive token/delivery accounting remain gaps. No production or primary activation is inferred.

## Ten-call model pilot

[Plan](pilot/PLAN.json) was saved with all prompts, input token IDs, seeds, initial setups, scoring rules, code/profile/model-file pins and predeclared host probes **before the first generation**. Used the existing cached **SmolLM2-135M-Instruct plus original canonical LoRA**, CPU float32/eager, two threads, temperature .8/top-p .9, max 96 output tokens/call. No training, model download, paid inference API, adapter ablation or retry. Each fresh context had its own disposable world. This is not a continuous run.

Five cases were each run with seeds 110601/110602. All received one compact syntax card with examples; no unassisted-versus-assisted causal comparison was performed. Raw generation was saved before passing its entire stripped text to the actual process-bounded dispatcher. No fence removal, command extraction, completion, heuristic repair or alternate candidate execution was allowed.

| Case | Calls | Accepted model actions | Requested outcome |
|---|---:|---:|---|
| Calculate 2+3 with a run command | 2 | 0 | 0/2 |
| Define double | 2 | 0 | 0/2, checked with a predeclared host call |
| Guard empty-list failure | 2 | 0 | 0/2, checked with empty/nonempty host calls |
| Retrieve seed value page | 2 | 0 | 0/2 |
| Free-choice action with numbers available | 2 | 0 | Not task-scored |

Examples retained: the calculation replies were `2 + 3`, definition replies `double`, one repair reply `EMPTY_LIST`; others were prose, malformed prefixes or multiple unsupported forms. These are not executed calculations, definitions or repairs. The free-choice replies also contained no accepted action. Descriptions of persistence were not treated as actual persistence. Scoring failures are preserved in [summary](pilot/SUMMARY.json), raw generations and dispatcher receipts.

The repair case supplied a real setup/error summary, not a full iterative model-feedback sequence. Host setup, post-reply scoring probes and observation aids are labeled as host contributions. None of the ten model replies changed its guest snapshot; audit records and host probes are separate activity. Two fixed seeds and one card do not identify whether the limiting factor is wording, syntax, context, adapter behavior or a broader skill limitation.

[Record verification](pilot/RECORD_CHECKS.json) reconstructed all 10 final worlds from their bundles, checked exact original model-request retry receipts, prompt/token/seed/stop/decode consistency and unchanged model assets/code. It generated no new model output and loaded no weights. Generation-time pre/post tensor digests also matched. The memory guard recorded 21 points, peak working estimate 1,284,259,840 bytes under a 5,153,960,755-byte limit. No interrupted generation or selective rerun occurred.

## Next strongest

Calibrate the smallest usable action expression before a longer exploration: a short exact-command copying condition versus the broader card, equal targets/budgets and preserved failures. Then test one expression/definition incrementally if actual execution becomes reliable. Any parsing assistance must be explicit; accepting a host-rewritten reply would be a different interface, not evidence that this one worked. Do not translate zero valid commands into a claim of zero possible reasoning, or proceed as though constructive free play occurred.

The persistent world can retain constructions and be transported, but productive model use is still unresolved. Further infrastructure breadth or longer seasons are not yet justified by this pilot alone.

## Preservation

All 1,504 protected non-bytecode original-garden files remain unchanged: entry 500, number 0, verifier 0096, PAUSE present. The prior prototype’s 26 non-bytecode files are also unchanged. Base/adapter file and tensor digests were checked; no weight updates. [Preservation](PRESERVATION.json). Old interrupted-session unknowns remain unknown. Prior navigation bytes are in `before/`; the earlier build and records were not overwritten. [Runbook](RUNBOOK.md).
