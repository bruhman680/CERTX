# Fluid Relational Reasoning — operational candidate 0.1

This package translates the user's FRR v0.5 into instructions, a recoverable inquiry record, and behavioral evaluations. It is an unvalidated operational candidate, not evidence that FRR improves AI reasoning.

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
