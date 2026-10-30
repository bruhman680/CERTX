# Prospective generated-claim pipeline

29 October 2026, America/Chicago. This code is specified before the new model
outputs exist. It composes independent measurement/minimum extraction calls;
the baseline is one direct comparison call. The two-call acquisition cost is
reported and is not an equal-budget direct-answer comparison. Source entity,
unit and run association are caller question context, not model-established
ownership. No original numeric measurement, minimum, gold answer or correctness
flag enters `compute_pair`.

## Frozen surface representation

The new study-local parser accepts unsigned integer cm/kg quantities at clean
token boundaries. Simple sentence wrappers, lists separated by semicolon/comma
or “and”, and one or more literal MISSING tokens are syntactically accepted.
Every digit run must belong to a supported quantity. Signed quantities,
decimals/exponents, wrong or suffixed units and stray numeric fields are
unsupported. Minimum requires exactly one quantity with no MISSING token.
Measurement preserves all parsed quantities and MISSING tokens, including a
mixed missing/measured list; no aggregation, deduplication or precedence rule
is added. Duplicate equal values remain two observations but not independent
evidence.

This is surface parsing, not natural-language entailment. A wrapper such as
“not 7 cm” still becomes a 7 cm claim, and “not MISSING” still supplies a literal
MISSING token; quotation, hypothetical language, source
identity, omitted measurements and ownership are not understood. Tests expose
this boundary explicitly. In particular, if a model omits one conflicting
measurement, no oracle inserts it. Scoring source fidelity is separate from the
pipeline's action selection.

## Conditional computation and withholding reasons

`compute_pair(measurement_text, minimum_text, entity, unit, record_id,
artifactroot)` parses both generated responses. If either is unusable, it returns
UNKNOWN with `stage=extraction_unusable` and no checker receipt. This is an
implementation withholding policy, not proof of absent domain evidence. An
otherwise valid explicit MISSING observation reaches the unchanged exact
threshold helper and returns `missing_measurement`. Multiple distinct values,
or simultaneous explicit MISSING and measured observations, return
`conflicting_measurements`. Different values remain conflicting even if both
are on the same side of the threshold, as the declared task policy requires one
consistent measurement and supplies no precedence/aggregation.

The helper compares generated measured value >= generated minimum only when its
own structured-input conditions hold. The output exposes parsed fields,
contract, source-artifact hash, checker receipt, stage and action. A hash binds
generated claims to bytes, not their truth or applicability to the original
record. A correct action with a false extracted minimum is not fully warranted.
Actual source-field fidelity and task gold must be evaluated afterward, never
used to repair or gate the selected action.

## Preservation and scope

The source fingerprint of the unchanged checker is recorded at import and
checked before assessment. A changed file withholds as `checker_changed`.
Artifact files use exclusive creation; reruns cannot overwrite a previous
record artifact. An unsafe record identifier withholds before writing. The
scope remains a trusted local workspace, not a hardened arbitrary-input
service. No broad inference policy, confidence gate, natural-language parser or
FRR efficacy claim follows from these authored development tests.
