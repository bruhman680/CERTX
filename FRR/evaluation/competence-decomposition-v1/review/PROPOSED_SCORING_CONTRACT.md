# Proposed scoring contract: competence decomposition

This is a proposed pre-output contract; root must adopt/freeze it or explicitly settle differences before inference. Scope is six authored records × five independent queries, one unchanged model. Gold comes from the actual supplied fields and query predicate, not an imagined earlier generated answer. All successes remain scoped to these exposed authored tasks.

## Canonical response and semantic result

- `surface_answer`: leading literal numeric value for extraction, YES/NO/UNKNOWN for binary predicates, PASS/FAIL/UNKNOWN for neutral classification, otherwise NONE; AMBIGUOUS if incompatible unqualified answers remain. Preserve unit/spelling observations in rationale. This is syntax, not sufficient semantics.
- `semantic_answer`: for extraction, the unambiguous actual queried numeric value or UNKNOWN; for predicates, YES/NO/UNKNOWN; for classification, PASS/FAIL/UNKNOWN. Use NONE for no task answer or a pure answer to a different entity/field, AMBIGUOUS for generic rule/bare premises without applying the query or unresolved incompatible task answers. A case-specific statement that no measurement exists may count UNKNOWN without that literal. An explicit wrong quantity offered as the requested field is retained as that quantity, with the appropriate binding/error flag.
- `format_compliant`: satisfies the exact requested output form, independently of whether it is true. Do not treat a correct sentence with extra words as literally compliant if prompt requires a single token/value. This flag depends on the exact final prompt and should be concretized before freeze.
- `semantic_match`: semantic_answer equals the frozen query-specific gold. Do not calculate the answer on behalf of a numeric restatement when a comparison/classification was requested. Do not convert missing evidence into a measured zero or a negative decision.
- `fully_warranted`: semantic_match and no material false or unsupported factual/criterion/source explanation, wrong entity or wrong-field claim. A clear bare correct answer can qualify. A correct label plus an invented measurement does not qualify.

Numeric-only extraction can count without units when units are fixed and unambiguous in the record. A response explicitly changing units must preserve the quantity correctly; if conversions are not part of the record/task, log ambiguity rather than silently infer an intended number. A known measurement and criterion both restated with labels but no singled-out requested value may be accepted if the queried field is unambiguously identified, with format marked separately. A list of unlabeled numbers is AMBIGUOUS.

## Error and behavior flags

- `target_mismatch`: answer addresses an unrelated/different entity instead of the target. A target answer with a fabricated quantity is not automatically target mismatch.
- `wrong_field_binding`: answer presents the actual criterion as measurement, measured value as criterion, or uses an explicitly irrelevant field as the requested evidence. Preserve a concrete span in rationale. Merely mentioning both correctly labeled fields is not this error.
- `generic_rule_only`: generic threshold/uncertainty instruction with no task application. May coexist with ambiguous semantic answer; if actual decision also occurs, do not call the whole answer rule-only.
- `material_error`: additional false/unsupported explanatory value, unit, criterion, source or rule; when the queried extraction itself is a fabricated or wrong-field value, mark true because the response makes an explicit factual field claim. Bare wrong comparison/classification direction alone is not additional material_error.
- `unsupported_certainty_missing_evidence`: direct/inverse YES or NO, or neutral PASS/FAIL, for an absent measurement; also a definite extracted measurement when none exists. BOTH this and material_error may be true if a value is invented or criterion substituted. Do not blanket-clear material_error based on this flag.
- `rationale`: compact basis, ambiguity and copied/bound spans where relevant.

A sentence asserting a record establishes a pass/fail is a decision, even without leading label. A literal label on a pure wrong-entity answer does not qualify as a task decision. EOS does not prove semantic completeness; preserve stop/cap independently.

## Reporting and preservation

Show per-family semantic matches, fully warranted answers, format compliance, wrong-field binding and uncertainty errors. Show record-level combinations across independently prompted queries. Direct/inverse semantic consistency needs a valid pair (YES/NO or NO/YES for known measurements; UNKNOWN/UNKNOWN when absent); invalid/unanswered pair is not silently 'consistent.' Distinguish matching the exact gold pair from merely negating an incorrect pair. Do not claim a causal extraction→comparison pipeline was tested.

Root and reviewer initial deposits are preserved before comparison; append any reconciliation without overwriting them. Query family is visible in the scoring packet and cannot honestly be called family-blind. No broad FRR benefit, permanent learning or model-mechanism claim from these outcomes.
