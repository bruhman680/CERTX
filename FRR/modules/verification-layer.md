# Optional verification layer — scoped, revisable, versioned

Adopted as an optional working practice and narrow executable prototype following [VL-C1](../evaluation/verification-layer-v1/REPORT.md). It extends the [bounded experiment loop](bounded-experiment-loop.md) and [evidence-gated feedback procedure](evidence-gated-feedback.md); it does not change core FRR prompts/schema, implement an autonomous semantic judge, or establish improved model reasoning.

Use a lightweight record when a claim becomes consequential for an answer, experiment, build or later agent. Open play can remain exploratory. Do not turn every passing idea into a mandatory checklist. Existing protocols/receipts can supply these fields without duplicate forms.

## The working contract

Before calling something verified, name:

- **Claim and scope:** stable claim ID/revision, exact assertion, population/context/horizon and dependent assumptions. Distinguish a literal calculation, factual claim, inference, prediction and preference.
- **Criterion:** what observation/check would support, contradict or leave it unresolved? Record tolerances and constraints, plus which failure matters. Mark a changed goal as a new criterion/version, rather than making the old failure disappear.
- **Evidence:** source/artifact location, version and content hash where applicable; what it actually measures; known missing input. Hash integrity is not source authenticity, reliability or independence.
- **Check and limitations:** checker/method version, inputs, result, meaningful rival/negative control where appropriate, cost/budget and remaining blind spots. Do not count copied/shared-source evidence as independently generated corroboration.
- **Verdict and next consequence:** supported for this scope under stated assumptions, contradicted for this scope, or unresolved with a reason. Preserve disagreement across dimensions. Reopen if the evidence, criterion or a consequential assumption changes.

A failed or unavailable verification attempt is not automatically a false claim. A satisfied obligation is not automatically a completed task. A failed prediction is not automatically an invalid probabilistic forecast. Keep observation, inference, decision, execution and outcome status separate when they matter.

## Feedback and acceptance do different work

PID supplies useful scheduling analogies. Present unmet obligations can trigger a check; persistent consequential uncertainty can remain visible; a stable measured trend can change effort. None is evidence of truth by itself. Accumulated concern must not accumulate belief confidence. Budget caps, unavailable evidence and repeated unchanged checks should pause intervention rather than build urgency indefinitely. Rebase effort/trend bookkeeping when the goal or metric changes, preserving the old record.

A check accepts a claim only through its relevant evidence/criterion. There is no master coherence, entropy, confidence or success score. Numeric PID gains are appropriate only for a defined measurable process with justified response assumptions; this prototype implements no PID scheduler or automatic role rotation.

## Executable subset

[verification_layer.py](../tools/verification_layer.py) produces receipts for two adapter configurations:

- **Ruleset 0.1:** exact equality for a restricted literal rational-arithmetic expression.
- **Ruleset 0.2:** the same adapter plus interval assessment of whether a true state is within a target band, conditional on an additive sensor model and supplied bias bounds. It does not authenticate a sensor or establish those bounds empirically.

Ruleset versions are separate from FRR runtime0.2. Exact checker source hash distinguishes revisions, including the disclosed parser repair. The adapters bind a local artifact's bytes, require matching explicit scope and a recognized criterion, and retain unresolved status for unsupported or invalid inputs. Scope matching is literal, not semantic scope understanding. Domain support is conditional, not universal certification.

From a repository checkout:

```bash
python FRR/tools/verification_layer.py FRR/evaluation/verification-layer-v1/examples/literal_correct.json --root FRR/evaluation/verification-layer-v1 --version 0.2
```

The corresponding literal_incorrect.json yields contradicted. A zero process exit means a receipt was produced; callers must read verdict. The examples' roots and evidence paths are deliberately explicit. Supply `--ledger path/to/receipts.jsonl` to append; to revise a claim, also supply `--supersedes EVENT_SHA --revision-note 'reason'`. Preserve the original contract and artifact bytes alongside receipts; a contract hash alone does not recover their content.

The local log uses a writer lock and hash-linked events. It can detect changed payloads against the recorded chain and preserves an existing prefix during ordinary appends. A privileged writer can rewrite the file and all hashes; it is not signed or tamper-proof. Git commit anchors and separately controlled originals can strengthen history. This is a local trusted-workspace utility, not a hardened arbitrary-input service, automatic source retriever or networked multiwriter database.

Other domains need appropriate domain tools, experiments or explicit human/agent review records. The arithmetic adapter cannot certify empirical premises, scientific generalization, ethical priorities, causal identification or AI output truth. Do not retrofit arbitrary tasks into its literal proof label.

## How it evolves

1. Preserve a concrete failure, gap or new domain need with its evidence and affected claims. A low score alone does not diagnose the cause.
2. Propose a candidate checker/criterion change and state intended verdict changes. Keep the old checker, contracts, outputs and known failures.
3. Replay earlier applicable cases and add discriminating new cases. Unintended regressions block adoption; intended corrections require explicit justification, not silent relabeling. Authored development fixtures are not held-out confirmation.
4. For broader deployment/efficacy claims, use separately prepared evidence/tasks and meaningful simpler comparators, report false support and needless withholding separately, and include cost. Admit unresolved results.
5. Publish the version, reason, exact evidence and affected scope. Reassess consequential dependent claims as needed; a new verifier does not automatically relabel every old result. Keep original and revised verdicts linked.

VL-C1 exercises this process with a real post-run parser-limit correction, separate manifests and preserved initial receipts. It demonstrates a repair/replay workflow locally, not autonomous learning. Adoption remains provisional and optional. A future discovery can revise the verifier, its assumptions, or the problem definition; the historical record must show which changed.

Later [VA-C1 live adoption](../evaluation/verification-adoption-v1/REPORT.md) adds execution-entry checkpoints, real saved-claim contacts and a second disclosed source-binding repair. The checker now records an import-time source snapshot and leaves a verdict unresolved if its file changes before evaluation; fresh-process checks remain preferable. This does not authenticate bytecode or prevent runtime monkeypatching. [VP-L1](../evaluation/verification-practice-pilot-v1/REPORT.md) demonstrates fresh-context use on three authored tasks, with ordinary and simpler provenance guidance tying. Use the lighter procedure when sufficient; consistent long-term habits remain untested.

For a material revision, the separate [reopening helper](../tools/reopen_assessment.py) can compare an original contract/receipt with a proposed contract and suggest reuse or a new assessment after binding checks. [PG-C1](../evaluation/practice-growth-v1/REPORT.md) supplies a working command, explicit limits and a peer-found exact-binding repair. It does not authenticate sources or silently change historical verdicts.
