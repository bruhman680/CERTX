# Scheme computational world: blueprint and isolated host prototype

5 November 2026, America/Chicago; host UTC 6 November. **Built and host-tested in isolation. No model generation, training, primary migration or new continuing-garden entry.**

## Result

The user's clarification changed the language choice from a new Lisp-like dialect to a documented subset of an established language: **R7RS-small Scheme**. Three design/build agents worked on language, persistent execution, and independent interface tests. A fourth prepared an existing Scheme reference. Root integrated a process-bounded CLI, differential checks, integrity tests and a host-authored walkthrough.

The prototype supplies generic data and procedures, composition, own-name recursion, actual results/errors, durable artifacts and dependency versions. It does not prescribe a garden, workshop or domain-specific project. The small model has **not** used it yet. Host-authored success must not be described as model discovery or emergence.

## Established language, explicit restrictions

[R7RS-small](https://small.r7rs.org/attachment/r7rs.pdf) is the language reference. Supported expressions use standard Scheme syntax and behavior where admitted: `#t/#f`, quoted proper lists, `if`, a single-binding `let`, named definitions, arithmetic, list and text operations. The chosen left-to-right argument order is one permitted Scheme order. A custom bounded evaluator implements this subset; this is not full Scheme conformance or a claim to reuse Chibi as the world engine.

Notable omissions include first-class procedures, `lambda`, mutation, general `eval`, macros, imports/I/O, runtime symbols, improper/cyclic pairs, floats and mutually recursive groups. Resource exhaustion and immutable world-version binding are application rules. The [language contract](LANGUAGE.md) identifies these boundaries. Pinning a dependency when a definition is published is a world/module policy; it is not a claim about mutable Scheme top-level redefinition.

An independently built [Chibi Scheme](https://synthcode.com/scheme/chibi/) 0.12.0, pinned to commit `08e23be118e7de8cf29d606bc4793371c0ace680`, evaluates only trusted comparison fixtures. Its source/binary is outside the FRR tree. It has host capabilities and is **not** available as a model action or sandbox. [Setup, license, build and smoke evidence](REFERENCE_SETUP.md).

## What was built

| Component | Implemented behavior |
|---|---|
| [Scheme core](prototype/scheme_core.py) | Bounded reader, explicit evaluator/continuation stack, proper tail-call behavior in admitted forms, type errors, integer/text/list limits and versioned semantic costs |
| [World store](prototype/world_store.py) | SQLite durable immutable artifacts, aliases/snapshots, captured dependencies, atomic publication, exact retained request retry, conflict checks, hash/chain integrity and interrupted-request recovery |
| [Host CLI](prototype/world_cli.py) | Separate worker process with wall/CPU/memory/per-file limits, post-exit reconciliation without automatic rerun, compact observation projection with explicit omissions |
| Independent checks | World-contract tests, process/controller tests, corruption/owner/restart checks, existing-Scheme differential fixtures and a construction walkthrough |

The model-facing actions are host protocol commands around Scheme: `put`, `define`, `run`, `run-save`, `inspect`, `list`, `drop`, `help`. A pure run returns `COMPUTED`; a successfully stored result returns `PUBLISHED`. The host supplies request identity and expected snapshot. An old program continues to call its captured helper revision even if that helper's friendly name changes or is dropped. Failed runs publish no successful result artifact. Audit receipts are separate from guest world state.

The [state/execution blueprint](STATE_EXECUTION.md) and [interface/evaluation plan](INTERFACE_EVALUATION.md) describe the larger intended contract. The prototype does not implement every blueprint feature; the gaps below remain part of the record.

## Measured checks

[Combined checks](CHECKS.json) pin the actual source/profile hashes used in the final run:

- **31/31 host tests passed**, including type/truth rules, selected-branch evaluation, recursive composition, fuel exhaustion, save/reload, pinning, quotas, exact retries, stale snapshots, paging cursors, owner exclusion, corruption detection and a hard process exit after admission. [Per-test results](UNIT_CHECKS.json), [log](HOST_TEST_LOG.txt).
- **124/124 trusted expression fixtures matched Chibi Scheme**, covering positive/negative integer operations, Scheme truth (including zero and the empty list), strict Boolean/integer distinctions, Unicode text, lists, binding and recursive procedures. [Differential results](REFERENCE_CHECK.json). This checks those value semantics, not storage behavior, all Scheme forms or isolation.
- **19 host-authored actions, 10/10 walkthrough assertions passed**: compose a list transformation; revise/drop a helper while an old caller retains its behavior; observe and repair an empty-list error; save a checkpoint; reopen the same world; finish with a pinned procedure; refuse to publish a failed result. [Full host walkthrough](HOST_DEMO.json). The temporary world was disposable, not a new model season.
- Source files and fixture profile stayed unchanged during the final validation. No benchmark score or general correctness/security proof is inferred.

## Development failures and repairs

Independent checks found an SQL admission placeholder mismatch and a transaction-handling problem. Further review caught inconsistent quote diagnostics, unhandled surrogate input at a host boundary, and recovery paths that could return an old successful receipt for a conflicting request ID. Those paths were corrected and included in later checks. Owner locking was added so opening a second process cannot mistake a live request for abandoned work. Recovered process-abort counters remain null when unavailable; separately labeled conservative quota charges prevent confusing missing measurements with zero work. Existing diagnostics and tests were not relabeled as model performance.

The reference build's Makefile ignored an `ldconfig` failure; the private-prefix executable works through an explicit local library path. The upstream full Chibi test suite was not run. See its setup record. Failed development attempts are described here; the final check files report the final frozen sources, not a claim that all earlier versions passed.

## Remaining limits

1. **This is a host prototype, not full blueprint acceptance.** Host-work costs are explicitly unmetered/null rather than fabricated as zero. Process limits supplement semantic accounting, but exact CPU/memory cost and complete aggregate model-token/delivery accounting are not implemented. POSIX limits/owner locking make this version Linux-oriented; per-file limits do not bound total disk use.
2. **Long-artifact ergonomics remain incomplete.** Alias-list pagination works, and the CLI bounds its projection. Complete source/data slicing, useful recovery of omitted pure results through the model interface, and a portable complete export/import/rebuild path still need implementation and tests. Existing database close/reopen and integrity checks are not the same as independent reconstruction from an export.
3. **No security certification.** Trusted finite fixtures and a restricted interpreter do not prove resistance to every malformed input or implementation bug. The existing reference Scheme has broader authority and must remain outside the guest path.
4. **No model capability result.** The current 135M+LoRA's known context/arithmetic/control limitations remain unresolved. A correct interpreter does not grant the model programming ability, curiosity or weight learning. Numerical values in [constants.json](constants.json) are provisional host-fixture settings, not measured optimal limits.

## Strongest next steps

Finish compact source/data retrieval and portable export/reconstruction, and reconcile outstanding blueprint-versus-implementation obligations explicitly. Then run a short isolated fixed-model interface pilot using the same actual parser and receipts: basic command, definition, composition, feedback/repair, retrieval and checkpoint reuse. Preserve failed attempts, distinguish interface help from self-chosen work, and compare seed-free time with optional seeds. No long continuous season or original-garden replacement is scheduled by this report.

## Original garden preserved

The original `discovery-play-patch-v1` remains paused at **entry 500**, number **0**, current verifier **0096**, with its original model/adapter settings. All **1,504 non-bytecode primary-study files** remained identical during the recorded comparison. No primary verifier or projection was rerun. [Preservation](PRIMARY_PRESERVATION.json). The earlier interrupted-session unknown remains unknown.

Previous navigation bytes are preserved under `before/`. The prior research cycles remain historical; this report supersedes their proposed-only status for the isolated components actually built here. It does not supersede the original garden or activate the new world for it. [Reproduction instructions](RUNBOOK.md).
