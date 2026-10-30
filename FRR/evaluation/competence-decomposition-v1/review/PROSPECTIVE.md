# Prospective competence-decomposition review

29 October 2026, America/Chicago. Reviewer read the current handoff and DM-C1 report before any new outputs. This is a prospective design recommendation, not approval of unseen final prompts/code and not a scientific replication. Proposed scope is six authored records (two entities × missing/below/above measurement) with five independently prompted queries each, 30 fresh greedy calls on the unchanged pinned local 135M checkpoint.

## Diagnostic purpose and limits

DM-C1's all-affirmative decisions coexist with changed literal-label scores. A useful next diagnostic separates requested field extraction from requested comparison and answer polarity. The same record should independently accompany each query; do not feed a generated extraction into later queries in this experiment. That avoids making a bad generated quantity the sole evidence for a later comparison. It also means success/failure across query types is descriptive localization, not a causal pipeline mediation result or proof that the corresponding information is/was internally represented.

Two entity templates and six records are enough for this bounded discrimination; they do not establish broad competence, generalization, instruction efficacy or population rates. Counterbalance low/high values and state all quantities in the same positive integer unit per record. Keep measured value numerically distinct from criterion, including across examples, so copying the criterion cannot accidentally pass extraction. Using one entity's threshold and measurement reused across missing/below/above is acceptable but constitutes correlated templates, not six independently sampled problems. Prompts should contain no worked examples for this baseline diagnostic.

## Recommended query roles

1. **Measured value:** ask for the recorded measured value, or UNKNOWN if no measurement is recorded. The required minimum is not a measurement. A true missing-measurement statement may satisfy semantic extraction without literal UNKNOWN.
2. **Required minimum:** ask for the numeric minimum specified in the rule. The rule's requirement remains known even when measurement is absent. Returning UNKNOWN is wrong for that field.
3. **Direct positive comparison:** ask whether the measured value is at least the required minimum. YES above, NO below, UNKNOWN absent.
4. **Inverse comparison:** ask whether the measured value is below the required minimum. YES below, NO above, UNKNOWN absent. Define this explicitly; 'fails' must mean measured below threshold, not simply 'not established to pass.'
5. **Neutral classification:** ask for PASS/FAIL/UNKNOWN from the record. Above → PASS; below → FAIL; absent → UNKNOWN. A semantically unambiguous equivalent may count separately from literal format adherence.

The inverse predicate is a different question and output vocabulary need not map by negating UNKNOWN. Direct/inverse polarity gold is balanced over the observed below/above records; UNKNOWN is its own evidence state. The neutral query changes both phrasing and label vocabulary, so a difference cannot identify either factor alone. Threshold equality is part of the stated at-least rule but is not tested by a missing/below/above-only design; do not claim equality competence.

## Freeze and execution recommendations

Freeze exact records, query strings, gold/bases, scoring contract, runner, pinned model metadata and input costs before first generation. Rotate query order for bookkeeping but use fresh independent model state and a new cache-artifact directory. Preserve the entire generated continuation and token IDs; score generated tokens only, never prompt prefixes. Keep cap and stop reason separate from semantic score. No prompt tuning/retries after outputs. Existing weights, cache branches, raw results and frozen scoring deposits remain intact. Save newly generated states with file/token/cache-count manifests; no permanent weight learning.

Report token and elapsed-forward costs per query family; these are workloads, not controlled speed or monetary/energy estimates. Main and little model are separate. Included/free resources only.

## Recommended outcome fields

The adjacent proposed contract supplies a minimal schema. Prioritize semantic extraction/decision correctness and full warrant; preserve syntax separately. Record whether an extraction selects a number from the wrong field, invents a value, copies only a generic rule, or fails to answer. Bare wrong YES/NO is an incorrect decision, not automatically an additional fabricated explanation. Unsupported certainty on a missing measurement is separate from invented quantities and both can coexist.

For each of the six records, show all five results together. Summarize extraction and comparison outcomes without turning them into stages that were actually chained. Specifically inspect whether both extractions are right but comparison wrong; this establishes a disparity across independently prompted tasks, not an identified internal defect. Direct/inverse contradiction is also a behavioral relation, not by itself evidence of an internal logical circuit.

## Independent review plan

Root scores then freezes its initial deposit. Provide reviewer a shuffled packet with query, target records, gold/basis and generated text but no run/order/condition mapping, complete prompt wrapper or root scores. Query type necessarily remains inferable from wording; call this ID/order-masked scoring, not query-family-blind. Another agent's coding is a second judgment, not an independent model experiment. Freeze reviewer deposit before comparison; append reconciliation, retaining both initial deposits. Do not use a broad clearing rule for secondary error flags.

Final exact cases/prompts/runner still require a prospective read before model generation. No model run or outcome inspection performed for this note.

## Final design disposition before generation

Root expands to eight records × five queries (40 calls) by adding equality for both entities: Cobalt Prism minimum11cm with missing/7/11/14cm, Bronze Bag minimum6kg with missing/4/6/9kg. This intentionally tests inclusive equality. Neutral answers are BELOW/AT_OR_ABOVE/MISSING, and measurement extraction uses MISSING. These supersede the initial six-record/proposed-PASS-FAIL wording above; the root SCORING_CONTRACT.md is the adopted contract, while PROPOSED_SCORING_CONTRACT.md remains the preserved initial proposal.

Direct gold is4YES/2NO/2UNKNOWN, inverse2YES/4NO/2UNKNOWN: polarity direction balances jointly, not per family. Equality's identical measurement/criterion numeral limits field-binding attribution. The final contract explicitly preserves that boundary, numeric-only extraction semantic sensitivity versus unit-format failure, and coexistence of wrong-field material error with unsupported missing-measurement certainty. No additional model calls requested by reviewer.

Final prospective read completed after root appended the common 'Return only the requested value or label; do not explain.' instruction. Reviewed exact CASES.json, RECORDS.json, DESIGN.md, GUIDANCE.json, INPUT_COSTS.json and runner; independently checked all40gold entries with the declared numeric predicates before any RAW_OUTPUTS.jsonl exists. Runner builds each prompt only from ordinary guidance, current record/question and common final instruction; evaluator gold is not serialized as an answer. Same original pinned checkpoint, fresh forward/cache per independent query, refusal to append an existing RAW file,96token cap and local state-file collision guard are present. The final contract/record design has no blocking prospective correction. Numeric extraction with correct units and labels has a strict output convention; semantic equivalents remain separately scored. Review does not claim CPU timing parity across different query lengths or a matched-input causal comparison.
