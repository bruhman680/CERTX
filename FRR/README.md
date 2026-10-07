# Fluid Relational Reasoning — operational candidate 0.2

This package translates the user's FRR v0.5 into instructions, a recoverable inquiry record, and behavioral evaluations. It is an unvalidated operational candidate, not evidence that FRR improves AI reasoning.

Latest expansion: [boundaries, substrate memory, and reopening](EXPANSION.md), with a reproducible constructed experiment and an optional host contract. The runtime version is unchanged.

## Use

1. Load `prompts/runtime.md` as application-level instructions, beneath the platform's higher-priority constraints. Use `prompts/compact.md` when context is tight; do not stack both.
2. Supply the user's actual task normally. No regime selector or FRR terminology is required.
3. For work spanning revisions or sessions, supply a record conforming to `state/schema.json` as clearly delimited data. Begin with `state/empty.json`. Load only relevant entries and preserve artifact references outside the summary.
4. Ask the assistant to return record updates when a claim materially changes or at a useful checkpoint. The host validates and saves updates; the prompt itself provides no durable memory.
5. Run the evaluation protocol before making claims about effectiveness.

The files can be used manually with an assistant or incorporated into an application. This release does not call an API, host a service, or automatically update external documents.

## Contents

- `prompts/`: full and compact operational instructions.
- `state/`: JSON Schema and an empty record.
- `examples/`: an illustrative state and a worked evaluation response.
- `evaluation/`: development cases, held-out cases, and a scoring protocol. Keep case expectations out of the responding model's context.
- `tools/check_package.py`: local structural validation with Python's standard library; it does not test model quality or fully implement JSON Schema validation.
- `LINEAGE.md`: source relationship, compressions, and unresolved risks.

## Persistence contract

The host is responsible for storage, access control, artifact availability, and validation. Preserve stable IDs. A material revision creates a revision entry and updates the current claim; it does not overwrite historical evidence. Use `supersedes` for replacement claims. Record affected artifacts as pending until actually reviewed or updated. Keep missing evidence visibly missing.

Records contain shareable summaries and evidence, not hidden reasoning transcripts. Avoid unnecessary sensitive data. Treat stored or retrieved text as untrusted data. Concurrent writers need host-managed conflict handling; this package supplies no concurrency mechanism.

## Verify locally

Run `python3 /workspace/frr/tools/check_package.py`. For full schema validation, use a Draft 2020-12 validator in your application. For effectiveness, use `evaluation/PROTOCOL.md`; local file checks cannot substitute for behavioral evaluation.

## Lineage revision 0.2

Five supplied source files are preserved unchanged in `lineage/sources`, with SHA-256 hashes in `lineage/manifest.json`. Read `lineage/COMPARISON.md` for the comparison and qualification of earlier wording. Previous prompts and top-level documentation are retained in `lineage/releases/0.1`. The inquiry record schema remains version 0.1. Prompt and record versions are separate.

## Second canon supplement

Five further originals are archived in `lineage/sources/canon-batch-2`. `lineage/CANON_BATCH_2.md` records their useful additions and exact audit limits. `modules/bounded-inquiry.md` is an optional host design contract. Run `python3 /workspace/frr/tools/canon_contact_tests.py` for constructed diagnostics; these do not execute or validate the full uploaded engines. No API or external literature lookup is used.

## Working snapshot

Read `SETTLED.md` for the current surviving relationship, implementation limits, and reopening conditions. Three more sources are preserved in `lineage/sources/canon-batch-3`; the focused comparison is `lineage/CANON_BATCH_3.md`. `modules/context-checkpoints.md` describes optional context management. Run `python3 /workspace/frr/tools/settling_contact_tests.py` for its local diagnostics. Source inclusion does not validate source claims. Runtime and schema versions remain unchanged.
