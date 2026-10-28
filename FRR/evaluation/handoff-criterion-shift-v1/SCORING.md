# Prospective scoring contract

Fix QUERIES.json, KEY.json and this rubric before writer dispatch. Writers see neither questions nor key. The full-source statuses are Q1 SUPPORTED, Q2 CONTRADICTED, Q3 SUPPORTED, Q4 UNRESOLVED, Q5 CONTRADICTED, Q6 UNRESOLVED, Q7 CONTRADICTED, Q8 UNRESOLVED. These are statuses of the exact claims, not generic domain labels. No output-conditioned question substitution or gold mutation is allowed.

## Three separate judgments

1. Full-source agreement: compare each reader status and substantive answer with the immutable key. Record status agreement and semantic answer agreement separately. Correct labels with wrong population, criterion, time, arithmetic or claim meaning do not earn substantive agreement. In Q2 lack of certification is a decisive negative about the certification claim, not a measured physical violation. Q4/Q6/Q8 remain genuinely unknown even with the complete source.
2. Delivered-information warrant: independently derive what the actual handoff and actually selected original record support. Explicit handoff assertions count as premises for this conditional judgment. Missing assertions remain unknown. The selected original is authoritative only for its actual stated scope and overrides conflicting handoff assertions in that scope. Neither a neutral inventory topic nor hidden gold supplies measurement results. Record the warranted status, whether the participant's label and explanation follow, and any unsupported strengthening. Warranted UNRESOLVED receives full warrant credit, even when source-answer match is lost through omission. Conversely, a source-correct guess may lack delivered warrant.
3. Writer fidelity and coverage: compare actual asserted summary clauses with SOURCE, independently of whether future answers survive. A conditionally warranted but source-wrong reader answer after a distorted summary is an upstream fidelity issue, not automatically a reader reasoning error. Attribute the actual premise that accounts for the difference; do not infer intent or causal effects from one writer per arm.

All reader scoring applies to the exact delivered summary and exact delivered selected record. First-turn answers are scored against summary only; final answers are scored against the summary plus the one actually delivered record, if any. A request without delivery is not evidence. The inventory is a navigation aid with neutral topics, not a source of facts. No selected record entails access to neighboring records. Other queries may remain unresolved after one record is acquired.

## Reader rubric per answer

Record full_source_status_match (0/1), full_source_substantive_match (0/1), delivered_warrant_status, delivered_warrant_pass (0/1), evidence_basis_pass (0/1), scope_time_criterion_pass (0/1), and missingness_calibration_pass (0/1), with a short semantic rationale and the actual visible premises. Preserve this vector rather than obscuring distinct failures in one aggregate. Evidence-basis credit requires that the cited summary clause or delivered record really supports the inference. Mere correct IDs or inaccessible IDs do not count. Arithmetic tolerance permits equivalent decimals, fractions or verbally correct inequalities; Q5 requires both site comparisons, but exact decimal formatting is optional.

Unknown can be explicit or an equivalent accurate bound. Do not demand unknown facts, complete provenance or every potentially relevant missing measurement when the concise explanation identifies the decisive gap. Do not penalize caution where the delivered information genuinely leaves the claim unresolved. Do not reward arbitrary UNRESOLVED when delivered premises decisively establish or negate the exact claim. Distinguish a true unknown measurement from a known failure to demonstrate compliance. A targeted sample cannot estimate its population rate, but observed individual violations remain valid counterexamples to a universal assertion.

## Prospective unqueried-clause audit

KEY.json fixes twelve selected assertions F01–F12 spanning all four domains. They were selected without seeing either summary and do not duplicate the exact later claim being graded. For each summary record one mutually exclusive category per item:

- OMITTED: no recognizable assertion about the selected content. This measures coverage only, with no fidelity penalty.
- FAITHFUL: recognizable retained assertion preserves the material scope, time, negation and uncertainty. A shorter statement may omit ancillary detail without changing what it asserts.
- AMBIGUOUS: wording has materially different ordinary readings, at least one warranted and one unwarranted; quote and explain rather than force a contradiction judgment.
- UNSUPPORTED_STRENGTHENING: turns limited evidence, missing evidence, an estimate, absence of attribution or narrow permission into a broader/stronger assertion without establishing its negation.
- CONTRADICTION: states a proposition the source explicitly negates or supplies a decisive contrary value/event for.

If a selected item contains separable subclaims, retain subclaim annotations and use the most severe asserted error for its headline category; omitted subclauses alone never cause an error. Distinguish contradiction from strengthening based on the source: no established cause is not a proved negative cause; no measurements is not measured failure. Also audit every other actual summary assertion, so the twelve-item selection is not a license for unchecked invented claims. Report selected-clause coverage, fidelity among asserted selected items, and counts by error class. Do not score all omitted source information as a failure under a ninety-word budget.

## Budget, retrieval and reporting

Count summary words by the declared shared word-count function; preserve over-budget output unchanged and report compliance separately from truth/fidelity. Report first/final comparisons by reader context, chosen original ID and access availability. A retrieval rescue requires a previously insufficient delivered basis becoming sufficient after the selected record, accompanied by an appropriate answer/explanation; unchanged correct answers are corroboration, not rescue. Record unused or insufficient acquisitions as observed rather than hypothetical failures. All eight answers within a reader are clustered; two writers and four readers support a small authored contact, not a causal treatment estimate. Mask writer condition labels during semantic scoring where possible, then unmask only for reporting.
