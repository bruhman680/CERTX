# A small inference boundary: extract, bind, compare, check the task

This optional workflow links to [CD-C1](../evaluation/competence-decomposition-v1/REPORT.md) and its [primary-source scout](../evaluation/competence-decomposition-v1/review/INFERENCE_SCOUT.md). Use it when an actual question reduces to an identified at-least comparison. It is a narrow tool, not a universal reasoning controller.

1. Identify the required field and the criterion in the applicable source. A generated extraction is a claim to check; the criterion is not a substitute for an absent measurement.
2. Keep entity, scope, unit and source version explicit. Construct a typed record only when its origin and meaning are inspectable. A hash binds bytes, not truth or semantic applicability.
3. Let the fixed comparator perform the arithmetic. It does not need a language model to decide whether 6.00 is at least 6.
4. Inspect both the receipt stage and the original task warrant. Correct arithmetic and valid JSON cannot repair a wrong extracted value or wrong criterion.

From a CERTX checkout:

```bash
python FRR/tools/evidence_threshold.py FRR/evaluation/competence-decomposition-v1/threshold_example/contract.json --root FRR/evaluation/competence-decomposition-v1/threshold_example
```

This supplied curated example measures Parcel Elm at 6.00 kg under a minimum of 6 kg. It should yield `verdict=supported`, `stage=compared`. The receipt exposes the actual decimal values and source/checker hashes. This example bypasses language extraction and therefore earns no small-model performance credit. Zero CLI exit means a receipt was produced; read its verdict/stage.

The strict contract names claim ID, entity, scope, criterion ID/operator/unit/minimum and a relative evidence path/SHA256. The artifact names entity/scope/unit and observations. Use explicit `state=missing` when that is the supplied source state. Decimal strings and integers are supported; booleans, binary floats, exponent notation, nonfinite values and implicit unit conversion are not. See [instrument design](../evaluation/competence-decomposition-v1/review/INTEGRATION_DESIGN.md).

Different unresolved causes need different actions:

| Receipt stage | What it establishes | Possible next contact |
|---|---|---|
|`no_observations`|No observation was supplied to this checker|Find or supply the relevant record|
|`missing_measurement`|The bound structured source explicitly reports no measurement|Collect a measurement if the task needs one|
|`evidence_unavailable`|The named file could not be read|Repair access/path, then reassess|
|`invalid_contract` / `invalid_evidence`|Inputs are unsupported or malformed|Repair representation; do not invent a value|
|`artifact_mismatch` / `identity_mismatch`|The declared binding does not hold|Find the applicable version/entity/unit|
|`conflicting_measurements`|The supplied values conflict under this contract|Investigate precedence or source differences explicitly|

Repeated equal observations do not become independent evidence. Different measured values remain conflicting even if both lie on the same side of the threshold; this helper does not silently invent an aggregation rule. A caller can still supply false structured facts with valid hashes. Neither the helper nor its tests certify empirical truth.

CD-C1 separately evaluates saved model extractions, comparisons and a retrospective extraction-plus-computation replay. Those results motivate checking boundaries; they do not establish that this workflow improves arbitrary agents. The original module is preserved in the study's [archive receipt](../evaluation/competence-decomposition-v1/MODULE_ARCHIVE.json).
