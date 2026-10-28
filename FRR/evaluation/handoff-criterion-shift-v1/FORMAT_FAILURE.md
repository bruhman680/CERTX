# Preserved final-response format failure

R02's public final output contains `],""missing_issue":` in Q6, one extra double quote. Strict JSON parsing fails with `Expecting ':' delimiter` at column2275 in the manually transcribed raw file. Its original is retained verbatim plus terminal newline in `outputs/readers/R02.final.raw.txt`. The reader received no retry, rescue or corrective feedback.

For human semantic evaluation only, `derived_semantic/R02.final.interpreted.json` removes that one extra quote and serializes the otherwise unchanged object. All other finals parse without repair. The derived object is not the public output and does not make R02 format-compliant. `FORMAT_CHECKS.json` binds raw and derived bytes separately; the scoring packet explicitly carries the failure, raw output and interpretation. All responses are manually transcribed from visible collaboration returns, not an authenticated transport export.

Semantic warrant, source fidelity, word-budget adherence and machine-readable output validity are separate dimensions. This contact must not be reported as four valid final JSON blocks or64 schema-valid answer occasions. No executable repair was deployed into the harness and no hidden edit was substituted for the original.
