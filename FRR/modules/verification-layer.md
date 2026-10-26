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


## Calibration and relationships — scoped follow-up

[Three-cycle contact](../evaluation/three-cycle-run-v1/REPORT.md) adds a measurement caution: a noisy matrix can be numerically invertible while the declared population design remains non-identifying. Separate that numerical property from the intervention/witness contract. When a readout depends on a relationship, marginal calibration alone may omit consequential joint effects. Check or bound those effects and use an out-of-fit operator where it can change the decision. Missing calibration warrants a scoped unresolved outcome rather than a forced allocation. These are optional measurement practices informed by constructed cases, not empirical validation of real instruments or improved agent reasoning.


The [second garden run](../evaluation/garden-three-cycle-v2/REPORT.md) sharpens this further: keep missingness distinct from zero, and ask whether readability selects the evidence in a consequential way. A restoration that changes content cannot by itself establish that the content survived earlier. If identification remains partial, retain the feasible set and ask whether the intended action stays warranted throughout it, under explicit task losses and constraints. A useful action does not verify the hidden-state explanation. Count the costs and state changes of further observation; a new measurement is not automatically a harmless improvement.


[UN-C1](../evaluation/upstream-numerics-v1/REPORT.md) adds a numerical boundary: distinguish intended equations, their finite-precision realization, and the information preserved in stored inputs. When consequential, use a higher-precision reference, stationary/equality cases and appropriate invariants before attributing an effect to dynamics. Representation loss can precede even a stable computation; conservation checks alone are not a full accuracy certificate. No historical result or training implementation is automatically revised by this source contact.


## Fit, intended structure and task outcome

[SA-C1/2/3](../evaluation/structural-access-three-cycle-v1/REPORT.md) distinguishes intact information from a readout that did not move with its representation. [PC-C1/2/3](../evaluation/paired-context-mismatch-v1/REPORT.md) adds a shared-assumption witness: a fitted subspace can preserve separate validation contrasts nearly exactly while missing the intended factor and failing downstream tasks. Fresh inputs from the same mechanism do not by themselves test that mechanism’s consequential assumptions. Where it matters, keep fit to observed data, recovery of the intended quantity and actual task acceptance separate; use a contrasting construction or independent criterion when the distinction can change the decision. These are optional checks motivated by synthetic examples, not demonstrated improvement in agent reasoning or a universal demand for additional validation.


## Reference authority and the quantity being guaranteed

[PW](../evaluation/probe-witness-calibration-v1/REPORT.md) and [RB](../evaluation/reference-bias-contact-v1/REPORT.md) separate agreement, valid measurement bounds, conditional identification and the intended task guarantee. When a decision depends on a bound or reference, name where its role, calibration and applicability to this target come from. Repeated readings or a new reference name do not authenticate a shared assumption. Count additional reference information and acquisition cost; leave unsupported authority unresolved. A common offset can preserve a difference while corrupting reconstructed values, whereas role-opposed offsets can counterfeit separation. Check the relevant error route rather than applying one generic bias correction.

State which quantity matters: raw values, recovered structure, normalized ranking or completed task. Invertibility alone is not an accuracy bound; normalized task agreement can hide gain error, and exact actual recovery can coexist with an uncertainty set too broad to warrant the requested guarantee. Use justified bounds or task margins for the needed quantity, with supplied geometry and transport assumptions explicit. If a check makes reuse unsafe without identifying a replacement, record “reopen / seek evidence” separately from “corrected and verified.” Apply this only when it can change the next action. These are conditional mathematical distinctions, not evidence that adopting the guidance improves real-agent behavior; executable rulesets remain unchanged.
