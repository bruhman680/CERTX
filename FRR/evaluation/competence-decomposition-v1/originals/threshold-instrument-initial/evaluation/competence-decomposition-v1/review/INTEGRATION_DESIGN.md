# Optional typed threshold instrument

29 October 2026 America/Chicago. Root approved this design before implementation. Inspecting the previous demonstration-mapping run showed that changed literal-label scores and a correct-looking answer vocabulary do not establish task application. Existing verification guidance already separates evidence, acceptance and action; this instrument supplies a deliberately narrow deterministic execution boundary.

## Inputs and scope

New optional `tools/evidence_threshold.py`, separate from existing verification adapters/core/schema. A caller contract names claim, exact entity/scope, criterion ID/operator/unit/minimum and a relative JSON evidence path with SHA256. Operator is exactly `at_least`. A bound JSON artifact names the same entity/scope/unit and a list of observations. Each is either a finite measured decimal value or an explicit missing observation.

The instrument checks artifact bytes before JSON interpretation, exact literal identity and units, then performs an exact decimal comparison. Booleans, all Python floats (including NaN/infinity), exponent notation, nonnumeric strings, extra schema fields and implicit unit conversions are unsupported. Decimal strings and integers are accepted under bounded length. Negative values and equality are legitimate. Conflicting measured values, or simultaneous missing/measured declarations, remain unresolved; no timestamp/priority rule is invented. Repeated identical values remain usable but do not count as independent evidence.

Malformed contracts are rejected as `stage=invalid_contract`, with unresolved verdict and no artifact assessment. Bound evidence that is missing/invalid/mismatched/conflicting is separately reported at an evidence stage. Empty/all-missing observations remain `stage=missing_measurement`, distinct from contradiction. A valid comparison returns `supported` for the stated at-least claim or `contradicted` otherwise.

## Boundary

This is a local trusted-workspace utility, not a hardened arbitrary-input service. Path traversal outside the supplied root is rejected; artifact size is bounded. A byte/checker hash records identity, not source authority or runtime integrity. Natural-language parsing, model extraction, source truth, calibration, interventions and probabilistic confidence are not implemented. Caller-curated JSON bypasses extraction: any comparator success must be recorded separately from small-model performance. Model-produced valid JSON could still contain a fabricated measurement and would not thereby become evidence.

The proposed integration is tool delegation to an explicit arithmetic checker with provenance/identity boundaries, not an FRR efficacy claim or automatic default. PAL's parsing-versus-execution distinction and the scout's syntax-versus-correctness cautions motivate this separation; no paper is reproduced by the tool. Tests use curated development fixtures and adversarial schema/binding cases, not held-out natural data. The preceding model outputs and historical verdicts remain unchanged.
