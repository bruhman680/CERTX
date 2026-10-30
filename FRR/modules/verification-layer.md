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


## Check joined warrants and the full acceptance target

Before labeling a premise missing, identify it precisely and check the combined delivered evidence. One record can supply an assignment that another deliberately omits; a local limitation does not erase a valid exact-key join. Preserve genuinely missing scope, but do not invent an additional gap after the applicable premise is established.

For a decision over several components, distinguish a check that can reveal one violation from evidence sufficient to establish compliance across all remaining candidates. The largest raw reading need not have the largest physical upper bound when component errors can differ. Name what a proposed follow-up can settle and what would remain unresolved. [Worked example](../examples/joined-warrants-and-maxima.md) and [QR contact](../evaluation/quality-preview-reader-v1/REPORT.md) preserve the observed explanation defects and exact logical witnesses. This is a scoped guidance clarification, not a demonstrated behavioral improvement or new executable checker.


Before proposing a follow-up as sufficient, check whether its intended decisive outcome is feasible under the constraints already accepted. A logically sufficient condition can be unattainable through the proposed observation channel. Keep sufficiency for the named target separate from unnecessary reconstruction of every underlying value. [Task-relative summary and feasible-check example](../examples/task-relative-summaries-and-feasible-checks.md) records a prospective evaluation repair; behavioral benefit remains untested.


## Typed inference delegation — optional threshold instrument

[CD-C1](../evaluation/competence-decomposition-v1/REPORT.md) adds a separate [typed threshold helper](../tools/evidence_threshold.py) and [worked use](../examples/typed-threshold-inference.md). It accepts explicitly structured, byte-bound observations and an identified at-least criterion, validates literal entity/scope/unit, then compares finite decimal values exactly. This ruleset is separate from the verification adapters above and from core/runtime/schema versions.

Keep four obligations visible: extraction/source binding, input validity, formal computation, and the task's warranted conclusion. A correct computation over the wrong extracted field can produce a correct-looking answer without warrant. Output-format compliance alone satisfies none of the factual obligations. Domain-missing evidence, no supplied observations, failed access/parsing, identity mismatch and conflicting observations have different receipt stages; choose a repair from the actual reason rather than flattening them into failure or zero.

This helper is usable for its declared structured domain. It does not parse natural language, authenticate evidence, resolve conflicts or estimate model confidence. Caller-curated instrument tests and retrospective composition of model outputs are distinct evidence. No automatic model-routing policy, confidence threshold or general reasoning improvement is adopted.


## Refresh diagnostics without changing task acceptance

[FW-C1 source contact and guard](../evaluation/field-role-witness-v1/REPORT.md) adds a narrow source-role check after TP-C1 exposed loss of field roles. The optional [field-role witness guard](../tools/field_role_guard.py) checks typed proposals against exact quotations, roles and complete note coverage under a tiny declared source grammar. Only then may bound fields enter the existing comparator. A quoted criterion cannot become an observation merely because its number fits; equal numbers in different roles remain different claims.

Keep the task objective and historical keys/verdicts fixed while revising diagnostic questions from new failures. Record the new diagnostic's motivating trace, scope and a discriminating negative case. Inspect its evidence before task labels where feasible; preserve separate task acceptance. Candidate-selection evidence is not final confirmation, and exposed development fixtures cannot be renamed fresh held-out evidence. This optional guidance is informed by the source reading; automated rubric/harness co-evolution and improved agent behavior have not been established here.

The guard validates literal source binding, not source authenticity or empirical truth. Unsupported language withholds. The eight valid proposal fixtures were caller-authored; the guard did not teach a model to produce them. All seven old model-output pairs fail its new interface, giving zero usable coverage. A fallback UNKNOWN is infrastructure withholding, not demonstrated recognition of source uncertainty. This guard is an optional instrument, not a default model adapter or autonomous decision policy.


## Label the observation level before interpreting a statistic

[CO-C1](../evaluation/claude-soil-observer-intake-v1/REPORT.md) reproduces selected Claude soil diagnostics and separates conditioning within one run from averaging over freshly sampled hidden conditions. A statistic's label should preserve its sampling unit, what is held fixed or resampled, and the model/estimator assumptions. Several observers sharing a fixed cause do not create independent samples of that cause. More data under an incorrect independence model can strengthen a wrong decision in the constructed example.

[Worked observer example](../examples/within-and-across-run.md) distinguishes source-missing information, unobserved heterogeneity and an estimator's finite-sample behavior. These are optional measurement questions, not calibrated real-agent triggers or a new automatic policy. The literal field-role guard does not validate independence, ergodicity or population sampling. A hypothesis classifier among known candidates does not establish causal identification outside that family.


## Match the design and calibration to the question

[SD-C1/2/3](../evaluation/soil-design-three-cycle-v1/REPORT.md) extends the observer-level check with fixed-budget and reset witnesses. Label the intended target as well as the number of observations: population-average precision and within-condition structure can need different groupings. Moment agreement does not establish agreement of full laws or causal carriers. A closed-candidate comparison remains closed-candidate evidence.

For an intervention, state what changes, what stays fixed, and what establishes or bounds its effectiveness and cross-effects. An unchanged readout can reflect an ineffective intervention; the same attenuated readout can reflect different carrier allocations and efficacies. When the accepted model only identifies a feasible set, retain it. Do not withhold a point conclusion if the actual constraints do identify one. [Design-label example](../examples/soil-design-and-reset-calibration.md) provides the scoped arithmetic. These are optional design/reporting refinements, not a new validator, reset policy, confidence calibration, or demonstrated behavioral benefit.


## Test whether the reader can use the diagnostic

[SR-C1](../evaluation/soil-design-reader-v1/REPORT.md) exposes a gap between an exact toy diagnostic and a model using its supplied rules. Keep source reading, numerical computation/set reconstruction, and final conclusion as separate observed obligations. A label match from one query does not verify the extraction or computation elicited in other independent contexts. Preserve unfinished source echoes as unfinished readouts; do not infer their eventual answers from copied numerals.

Before adding control complexity, test a smaller prerequisite such as choosing the relevant source fact, with selection and its cost explicit. Retain the role of each number and the distinction between missing calibration, ineffective supplied calibration, and what the actual constraints identify. This is optional evaluation guidance, not a demonstrated model repair or an automatic reset/abstention rule.


## Keep excerpt scope and aggregate trade-offs visible

[CR-C1/2/3](../evaluation/clause-reader-three-cycle-v1/REPORT.md) records a supplied-clause benefit on exposed source-reading tasks and a question-wording change whose opposite task-family effects cancel in the overall total. Preserve source binding, the exact question, selection method and the excerpt's supported task; byte-correct selection is not autonomous relevance discovery or universal task sufficiency. Count completion separately from source-supported answers, and inspect prespecified families/paired changes rather than only the aggregate.

A changed question must be tested on the intended new sources before promoting it. An apparent transfer result under the original question does not establish transfer of a different question. Selected/clause evidence here does not validate arithmetic, causal identification, or a default prompt repair. These remain optional evaluation practices, not demonstrated broad behavioral gains.


## Countertest an upstream explanation before promoting a repair

[WC/NF/SF contacts](../evaluation/source-frame-role-v1/REPORT.md) distinguish a completed question-sensitivity comparison, an unsupported simple number-word explanation, and a source-frame contrast that changes generated number roles on two base pairs. Cross a suspected representation feature while preserving the task's intended value/role key, retain failed explanations, and keep later adaptive protocols distinct from an original confirmatory plan. A successful frame is a conditional readout aid, not evidence of model learning or a general source-normalization policy.

If a rewrite changes syntax, tense or other features together, state that package and which task-specific proposition is intended to stay fixed; do not claim universal semantic equivalence or isolate an internal mechanism. Preserve the original, source mapping and unresolved facts. Validate source roles before calculation, then test calculation separately. No automatic rewrite, new parser, runtime rule or broad FRR benefit is established here.


## Preserve source absence, known zero and the reason for withholding

[FG/MF/CP](../evaluation/count-presence-polarity-v1/REPORT.md) tests the negative cases after a source-frame success. The candidate frame gets new positive counts and knownzero, but replaces two unrecorded counts with another field's number; its predeclared readiness gate remains failed and no arithmetic follows. An empty source field, a recorded0, and a formula outside its domain are different states even when each can stop a calculation. [Worked example](../examples/missing-zero-and-complement-questions.md) preserves these roles and withholding reasons.

When a distinction can change the next action, include it in the source-state readiness check rather than infer it from positive examples. Declared complementary questions can expose answer inconsistency, but consistency alone does not verify either answer or make a model's self-judgment independent evidence. Preserve source/target identity and the actual reason for any withholding. Later correct labels from separate prompts do not retroactively repair a failed extraction/gate or demonstrate a joined workflow. No new parser, default prompt, automatic verifier or broad behavioral improvement is established by these optional refinements.
