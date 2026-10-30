# FW-C1: source intake, diagnostic refresh and literal field-role witnesses

29 October 2026, America/Chicago. The user supplied two paper screenshots and a general harness diagram, authorized deeper extraction/integration and resumed work. The user then clarified that the diagram needed no additional investigation if its general structure was covered. We stopped that search. This contact makes no model calls, trains no weights and uses no separately billed service.

## Outcome

A new optional source-role guard now checks witnessed typed proposals before the existing arithmetic checker. Under a deliberately tiny literal source grammar, it requires the right source bytes, entity/unit, criterion quotation and every observation quotation. A matching number alone is insufficient: even an equal-valued criterion/measurement role swap is rejected.

All80frozen authored instrument cases have their expected status:8valid proposals bind,72adversarial proposals withhold. Eleven regression methods pass. The8caller-authored bound proposals chain through the unchanged exact comparator with expected conditional outcomes. None was produced by a model; this is tool behavior, not improved reasoning or benchmark generalization.

All7preserved TP-C1 output pairs fail the new witnessed-proposal interface. Usable coverage is0/7. Falling back toUNKNOWN matches4/7old keys, but recognizes no source-based reason and supplies no improvement. The old failure remains a failure. Strict abstention is not the same as helpful inference.

## What came from the supplied material

[Selected primary readings and source limits](SOURCES.md), [source access/version record](SOURCE_ACCESS.json). The RuHarness reading informs optional diagnostic-refresh guidance with fixed task acceptance; the PLM reading remains a deferred training/decoding lead. Neither paper is reproduced. No speed or accuracy claim transfers to our local CPU model, and no automatic rubric/harness optimizer is installed.

The initial handwritten reading of the RuHarness identifier transposed digits; matching title/authors located2610.36826v1. The unrelated page returned by the mistaken identifier is not evidence. The diagram remains a general reference: its visible proposal/execution/check/record loop does not establish a missing FRR module, and no unreadable numerical target is adopted.

## Why another guard was warranted

[TP-C1](../typed-pipeline-prospective-v1/REPORT.md) showed a specific representation failure. A generated source paragraph retained correctly labeled criterion and measurement sentences, but a surface parser harvested every number as a measurement. Natural-language absence also disappeared without a literalMISSING token. An exact checker then correctly assessed misrepresented inputs.

The new instrument does not broaden that parser. It asks a different, inspectable question: does this proposed typed field match the quotation and role it claims in this particular source, and are all relevant notes covered? This is a deterministic interpretation contract over recognized syntax, not an arbitrary natural-language entailment system.

## Guard contract

[Implementation](../../tools/field_role_guard.py), [frozen design](DESIGN.md), [pre-execution hashes](FREEZE.json), [fixture sources/proposals](RECORDS.json), [80case definitions](CASES.json), [runner](run_checks.py).

Supported sources contain exactly:

1. An entity's explicitly stated unsigned-integer minimum in cm or kg.
2. One or more uniquely lettered Note clauses stating that entity's unsigned-integer measurement or explicitly reporting no measurement.

The complete source must parse. Extra unsupported prose, unknown syntax or repeated note IDs withhold; nothing is silently skipped. The source is byte-bound by expectedSHA256. The caller supplies literal entity/unit context. The candidate supplies that same source identity, its minimum value with the exact criterion quotation, and all observation states/values with their exact source-note quotations. Candidate fields have a strict schema. Every source note must be covered once, including missing or conflicting observations; repeated equal measurements are distinct notes, not independent corroboration.

Our local acceptance predicate can be expressed as:

    Bind(candidate, source) =
        source_identity_matches
        AND complete_source_grammar_recognized
        AND criterion_quote_and_value_match_the_criterion_role
        AND every_observation_quote_and_value_match_its_note_role
        AND all_source_notes_are_covered

A bound receipt exposes validated fields; it does not itself declare a task verdict. Only the subsequent comparator evaluates the declared at-least relation under its own single-consistent-value policy. Literal role binding is also not empirical truth: a source may be wrong or inapplicable. SHA256 establishes byte identity, not authority. Another language/domain requires a separately justified interpretation method.

## Instrument results and discriminating controls

The8sources cover missing/below/equal/above, crossing conflict, same-side conflict, missing-plus-measured conflict and repeated equal observations. Each has10candidate types:

| Candidate type | Cases | Bound | Withheld |
|---|---:|---:|---:|
|Valid witnessed proposal|8|8|0|
|Criterion quotation used as observation|8|0|8|
|Observation quotation used as criterion|8|0|8|
|Omitted observation|8|0|8|
|Wrong criterion value|8|0|8|
|Fabricated note quotation|8|0|8|
|Wrong source hash|8|0|8|
|Wrong entity|8|0|8|
|Raw copied context instead of typed proposal|8|0|8|
|Extra proposal field|8|0|8|

At equality, a numeric-only check cannot distinguish the role swap; the quotation/role check does. Same-side conflict notes cannot be dropped merely because the resulting label might remain unchanged. This follows the explicit completeness contract, not a claim that every domain requires identical treatment of conflicts.

[Eleven regression methods](test_guard.py), [test output](TESTS.log) additionally exercise unsupported source prose, duplicate note IDs/quotations, malformed context, missing source access, duplicateJSONfields and unsupported numeric types. Rejection and unavailability remain separate stages. These authored/adversarial fixtures are exposed development checks, not independent held-out confirmation or a complete parser proof.

[Results](RESULTS.json), [summary](SUMMARY.json), [result freeze](RESULTS_FREEZE.json). Eight valid caller-authored proposals are handed to the unchanged exact threshold checker after binding; all8conditional actions match fixture expectations. This bypasses language-model proposal generation and cannot earn model-performance credit. The guard accepts unsigned-integer literal records only, whereas the existing comparator supports a broader numeric domain.

## Compatibility with the preserved model outputs

The7TP-C1 extraction pairs were originally requested as values/lists, not as the new quotation-witness schema. The fixed compatibility pass supplies their raw strings without coercion, extra quotations or gold repairs. All7returninvalid_proposal. No model is rerun or asked a new question. A fallbackUNKNOWN has4keymatches, just like the old always-UNKNOWN baseline, with0bound proposals and0source-reason recognition.

This is an interface/withholding observation. It does not establish that the model can or cannot generate faithful witnesses when actually prompted to do so. A prospective producer study is needed. It would be misleading to report this as seven model failures on a newly instructed task or as improved uncertainty understanding.

## Review and integration

A distinct coordinator saved-data pass recomputed193comparisons and inspected binding-call arguments for outcome/gold dependence. All pass. [Self-review receipt](SELF_REVIEW.json). The same coordinator authored design/code/fixtures/review; there was no independent agent or scientific replication. We retain that limitation rather than implying swarm corroboration.

The [optional verification module](../../modules/verification-layer.md) and [worked workflow](../../examples/typed-threshold-inference.md) now link the guard. Guidance separates fixed task acceptance from revisable diagnostics, with explicit development/selection/final-evaluation roles. Exposed fixtures remain exposed even if placed in a folder named heldout. No default model adapter, autonomous critic, confidence threshold or training behavior is promoted. Existing arithmetic checker/core/schema/queue statuses are unchanged.

A navigation assembly script missed an import after archiving originals; the unexecuted tail was completed separately without duplicate appends or scientific reruns. [Assembly note](ASSEMBLY_NOTE.md). Seven preceding navigation/guidance files are byte-archived with [original paths/hashes](ARCHIVE_RECEIPT.json); relative links inside moved archives retain their original base. Earlier model states, outputs, scientific keys and failures remain unchanged. No new tensor cache or model inference exists in this contact.

## Strongest next contact

Prospectively test whether a producer can supply correct witnessed fields, measuring schema validity, binding correctness, task outcomes, withholding reasons, usable coverage and total costs separately. Include field swaps at equality, omitted conflicts and changed source versions. A strict gate that rejects everything is not a useful reasoning result, even when it prevents false acceptance. Independently sourced records remain legitimate, but unsupported formats must not inherit this guard's tiny grammar guarantee.

No further automatic cycle or background task is left running.

[Final scoped checks](FINAL_CHECKS.json) verify frozen data/code, preserved historical files, the working example and package/link structure. They do not constitute independent scientific replication or empirical truth certification.
