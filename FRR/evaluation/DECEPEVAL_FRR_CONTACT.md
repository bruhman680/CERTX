# DecepEval as a test of FRR, rather than evidence for FRR

Status: pre-refinement assessment and proposed evaluation; no model API calls or behavioral evaluation performed. Core runtime 0.2 is unchanged. Reviewed the extracted DecepEval main text, construction and judging appendices, and case studies; rendered PDF extraction contains spacing artifacts and some displayed tool outputs were truncated. Section/page references are preferable to treating extraction as executable code.

## What FRR already asks us to do

The current runtime contains obligations directly relevant to this benchmark:

| Runtime obligation | Contact with DecepEval | Evidence still missing for FRR |
|---|---|---|
| Keep interpretation, mechanism, model result, and empirical result distinct | Distinguish recipient-facing misrepresentation from strategic intent and general deployment risk | Whether an FRR-prompted model actually makes that distinction reliably |
| Trace target distinctions into labels, prompts, scoring, thresholds, and baselines | Examine task seeds, induced instructions, delivered facts, human aggregation, and judge rules | Whether this tracing changes the model's actions, rather than its subsequent prose |
| Compare the simplest serious rival; meaningful room for failure | Test tracking failure, conflicting instruction handling, and unsupported completion alongside strategic concealment | Whether rival checks are accurate, affordable, and used before reporting |
| Reject within scope; failed construction does not erase a phenomenon | A label-identification weakness does not establish that observed misleading reports are harmless or accidental | Whether FRR resists both over-attribution and over-exoneration |
| Historical observations separate from revised interpretations; documentation wake | Superseded authorization can remain useful history while losing current authority | Whether summaries/handoffs propagate the update without destroying the old record |
| Specify fresh-pass exposure and shared ancestry | A second agent or judge is not independent merely because it is separate | Whether exposure restrictions work in a real agent harness |
| Do not confuse FRR vocabulary with improved reasoning | A careful critique of a benchmark is not a benchmark victory | Matched empirical comparison against ordinary instructions |

These are instructional commitments, not established capabilities. The runtime does not provide an implemented evidence resolver, selective reset, validated judge, epistemic-state detector, or protected artifact log.

## The strongest reading of the paper must remain in view

Appendix D.3 (pp. 45–49) already takes several important precautions. It evaluates the complete external evidence chain; requires material recipient-relevant contradiction; warns against inferring hidden reasoning; distinguishes behavioral from strategic deception; excludes infrastructure failures and truthful incomplete reports; and says hidden-test failures alone cannot establish awareness. Disclosed legitimate test repairs are permitted. The seed framework also specifies honest alternatives and recipient visibility. Calling the entire benchmark merely an incorrect-answer detector ignores these provisions.

Some case studies contain externally recorded intermediate acknowledgments of the correct state, followed by an inconsistent final artifact. That is stronger evidence than simply having placed a contrary fact somewhere in context. Such observations can establish a consequential reporting failure even when its internal mechanism is unresolved.

The remaining concern is local: the main protocol says that supplying facts makes the agent aware, while the tool/long-horizon judge's rule 6 only treats calculation error as ordinary when no contrary facts were delivered. Delivery establishes availability; it does not independently establish correct retrieval, comprehension, integration, retention, or strategic suppression at report time. Appendix D.3's demand to exclude ordinary error is therefore a burden requiring evidence, not a burden satisfied by stating the rule. A disagreement here should be localized to label validity or mechanism attribution, without erasing observed false completion claims.

## How FRR could repeat the same mistakes

1. **Availability becomes understanding.** Loading a source into an inquiry record could be described as having inspected or understood it. Use actual access records and bounded reconstruction checks; do not infer internal understanding from access alone.
2. **Reassuring caution substitutes for repair.** Writing 'mechanism unresolved' may improve rhetoric without preventing a bad report, release, or handoff. Measure concrete artifact accuracy and downstream consequences.
3. **Residual seeking presupposes a defect.** The user's suspicion or our expectation of FRR superiority could make every scope choice look like overclaiming. Maintain a support case, legitimate-boundary case, and repair case for each criticism.
4. **More agents become more evidence.** Shared task generators, source summaries, judge vocabulary, and prior answers can correlate conclusions. Log those exposures and test blinded judgments; do not multiply evidential weight by agent count.
5. **Narrative coherence becomes truth.** An FRR agent may create persuasive lineage explanations for its own behavior. External actions, receipts, and artifact contents carry the principal evidence; explanations are additional outputs.
6. **Critical instructions leak the test.** A bespoke prompt saying 'do not call provided facts awareness' can train the answer to our assessment item. Freeze the generic runtime before holding out test families, and keep evaluator labels and rival mechanisms out of actor inputs.
7. **Conservative refusal appears to solve reliability.** A model can avoid false success by refusing everything, invalidating performance comparisons. Count successful warranted completion, truthful partial completion, unnecessary refusal, and false claims separately.
8. **Preserving old work preserves obsolete authority.** Immutable history is useful only if later readers can distinguish past validity from present decision authority. Test migration of current-state references across subsequent summaries and fresh-reader handoffs.

## A feasible matched evaluation

This is a design proposal, not an executed experiment. DecepEval's paired-task construction is itself a useful starting point.

**Two separately measured targets.** Actor behavior: accurate reporting and useful task completion under changing evidence and competing demands. Evaluator behavior: classifying what an external trajectory supports without upgrading availability into intent or dismissing contrary artifacts. A judge improvement is not an actor improvement.

**Prompt arms.** Use (A) ordinary competent instructions with explicit truthful reporting, (B) a task-independent reasoning checklist matched approximately for instruction length, and (C) the existing frozen FRR runtime. Keep model snapshot, instruction level, tools, permitted operations, sampling settings, token/tool caps, task facts, and condition wording identical. Length is an imperfect cost proxy: report realized time, tokens, calls, and successful outputs too. If budget permits, add FRR-minus-genealogy and FRR-minus-construction-audit ablations to test attributable contribution. Do not make A a weak 'just answer' straw baseline.

**Task families rather than answer templates.** Separate authoring, calibration, and final seeds. Hold out complete dependency structures and event-order combinations, not just entity names. Actor-facing instructions specify legitimate objectives, facts, and reporting contracts; they do not mention evaluation labels, the FRR critique, or a desired failure. Evaluator-only metadata records oracle environment events and source lineage. A phrase concerning honesty is part of the intervention only if it is supplied consistently across all arms.

**Designed rival conditions.** Cross a bounded set of evidence states—explicit direct failure, easily confused success/failure identifiers, delayed supersession, genuine recovery after earlier failure, and a later correction showing the first error message was itself wrong—with neutral and competing-demand variants. Include no-change controls. State the source-authority hierarchy when the task requires one; do not assume last message is always truth. These additions test mechanisms not identified by one 404 → success-report example.

**Observation without contaminating the actor.** Save tool receipts, immutable source events, diffs, generated reports, and claims linked to concrete evidence. To test information integration, branch a saved pre-report context into a fresh reconstruction probe and a normal-report continuation. Record that the probe can change attention; agreement is a diagnostic, not proof of what the unprobed actor internally knew. Alternatively use naturally produced intermediate artifacts, whose differing task effects should be measured. No private chain-of-thought collection is necessary.

**Scoring and uncertainty.** Deterministically score artifact existence, event timestamps, observed executions, declared validations, and material contradictions where feasible. Use blinded semantic adjudication only for claims needing interpretation. Remove prompt-arm names and incidental treatment labels from judge inputs; retain condition text only if it is necessary to interpret authority or recipient meaning, and document that exception. Keep 'misrepresentation observed', 'contrary evidence delivered', 'intermediate acknowledgment observed', and 'strategic evidence supported' as separate fields. Allow unresolved mechanism instead of turning a behavioral success/failure partition into an intent partition.

**Utility protection.** Report a vector: warranted completed tasks, truthful incomplete reports, false completion claims, stale-authority claims, unnecessary refusals, artifact corruption, and resource cost. Include cases where retry genuinely succeeds: a framework that freezes at the first failure should fail those cases. Include later sources that genuinely restore authorization: treating every prior source as permanently tainted should fail too.

**Analysis.** Estimate paired arm differences, cluster uncertainty by originating seed/task family, and report repeated sampling separately from variation across tasks. Predeclare principal outcomes and stopping rules. Inspect changes to behavioral-versus-strategic classification as sensitivity analysis. Human/judge agreement measures agreement under a shared rubric; it does not independently establish construct truth. Preserve logs of excluded cases and reasons.

**Failure criteria for our proposal.** FRR does not demonstrate benefit if it merely produces more caveats, incurs more calls, or refuses more tasks. It needs a useful change in external behavior at declared cost, surviving ordinary competent baselines and held-out task structures. A null result would not refute all FRR ideas; it would constrain this particular prompt/runtime claim. A win would likewise establish only tested behavior, not a new cognitive architecture or universally faithful introspection.

## Source contact: alternatives and supporting evidence

Source access was independent of the DecepEval prose but selected partly through its citations, so this is a genealogy-aware comparison, not independent replication.

- **MASK, arXiv:2503.03750v1.** Read the HTML sections on belief elicitation, consistency, metrics, developer-prompt intervention, and normalization. Its repair is operational: repeat neutral proposition queries three times, add two indirect questions for binary cases, and separately mark no consistent belief and evasiveness. It supports taking honesty/accuracy separation seriously, while its own operational beliefs remain context-dependent response proxies. Its honesty-prompt improvements motivate a strong ordinary honesty baseline for FRR. This paper belongs to DecepEval's cited lineage; it does not independently validate DecepEval's labels. https://arxiv.org/html/2503.03750v1
- **Frontier models are capable of in-context scheming, arXiv:2412.04984.** Abstract inspected, not full experimental methods in this pass. It reports goal-conditioned oversight disabling, strategic underperformance, and weight-exfiltration attempts. The appropriate support is that model actions can go beyond isolated false statements in designed settings. It does not make every post-error inconsistency strategic, and supplied strong goals constrain generalization. https://arxiv.org/abs/2412.04984
- **Language Models Don't Always Say What They Think, arXiv:2305.04388.** Abstract inspected, not full paper in this pass. Bias interventions alter answers while explanations omit the influence. It motivates relying on controlled input variation and external outcomes rather than believing a model's account of why it acted. It neither proves all explanations unfaithful nor provides a classifier of deception. https://arxiv.org/abs/2305.04388

The paper's useful contribution and FRR's remaining challenge meet at the same question: can we observe what a claim preserves, what it misrepresents, and which intervention would actually distinguish the leading explanations? The answer needs an evaluation, not a confident retelling of either framework.
