# HG1 structured reader-scoring instrument 0.1

This is an instrument-only development contact, **not an HG1 behavioral run**. The implementation [hg1_reader_scoring.py](../../tools/hg1_reader_scoring.py) supports only the LINEAR-2 continuation question: original constraints `a+b=8`, `b+c=11`, later measurement `b=3`, target `a+c=13`. It does not read arbitrary prose, infer an agent's reasoning, or score the other seven tasks. The source reference comes from this authored fixture, not independently established real-world truth.

## Inputs and use

A scored JSON record has exactly `case_id`, `facts`, and `response`. Case ID must be `LINEAR-2`. Each fact has exactly a unique `id`, `origin` (`handoff` or `update`), three numeric `coefficients` for a,b,c, and numeric `rhs`. It describes a linear equality. The response has exactly `status` (`answer`, `missing_info`, or `conflicting_evidence`), `value` (numeric for answers, null for abstentions), and `support_ids` referring to supplied facts. Fractions can be strings such as `"1/2"`; finite decimal numbers are interpreted exactly from their serialized value.

Example of a sufficient compressed packet:

```json
{
  "case_id": "LINEAR-2",
  "facts": [
    {"id":"compressed","origin":"handoff","coefficients":[1,2,1],"rhs":19},
    {"id":"measurement","origin":"update","coefficients":[0,1,0],"rhs":3}
  ],
  "response":{"status":"answer","value":13,"support_ids":["compressed","measurement"]}
}
```

Run `python FRR/tools/hg1_reader_scoring.py --score record.json --output scored.json` from the repository root, or use the corresponding local `frr` path. Preserve the original record separately; this command does not alter it. `--self-test` exercises constructed controls; [SCORING_CHECKS.json](SCORING_CHECKS.json) records their results.

## Separate judgments

- `objective_correct`: whether an answered number equals the fixed continuation reference 13; null for abstentions. `task_completed_correctly` records objective completion and does **not** imply support.
- `packet_state`: identified, underdetermined, or inconsistent under exact linear equalities.
- `packet_supported`: both the whole supplied packet and the cited subset consistently imply the answered value.
- `source_grounded`: packet support plus every cited equality being entailed by its declared source reference. Handoff facts are checked against original constraints; update facts against the fixed later measurement. An origin label alone earns no source validity.
- `grounded_completion`: both objective correctness and source grounding.
- `epistemically_appropriate_to_packet`: an answer supported by supplied/cited equalities, an underdetermination response when those equalities do not identify the target, or a conflict response when they are inconsistent. **This is conditional on the packet, not a judgment of truth or global epistemic virtue.** A corrupted but internally consistent packet can support a false answer; objective correctness and source validity remain false.
- `packet_facts_source_valid` and `invalid_source_fact_ids`: source audit of all supplied facts, including unused facts. This audit is evaluator information, not extra evidence supplied to the reader.

A lucky answer of 13 with only b=3 is objectively correct but unsupported. Honest missing-information handling does not count as task completion. A handoff saying a+2b+c=20 followed by b=3 supports 14 within the packet, but both source grounding and objective correctness fail. A derived a+2b+c=19 is sufficient: original equations need not survive verbatim. Contradictory packets do not license every answer through logical explosion.

## Parsing and remaining limits

Duplicate JSON keys, duplicate IDs, unknown references, Boolean numeric values, nonfinite numbers, incompatible response fields, and unsupported case IDs are rejected rather than silently repaired. Exact rational arithmetic avoids a floating tolerance for this narrow linear task. Parsing errors are operational failures, not factual errors, and must retain their own denominator in any later run.

Structured facts and answer certificates in these tests were deliberately authored. A future natural-language handoff needs a frozen, reviewed extraction process preserving exact evidence spans, or a prospectively required structured format. Self-reported support lists are not proof that the agent used them. No validated free-text extractor or general judge is provided here. Model accuracy, HPGM advantage, broader FRR efficacy, and independence are unmeasured. Nonnegativity is present in the original fixture but this instrument models equalities only; its underdetermination test must not be generalized to arbitrary inequality-constrained problems.

Development correction: the first self-test attempt failed because the numeric validator rejected internally created `Fraction` values. Internal rational support was added and all controls rerun. No actor outputs or study outcomes were changed.
