# Complete verification path: source, state, calculation and conditional answer

CVP-C1/2/3,30October2026 America/Chicago. Parent `97227cda3a95c454e60c2785019b6c536876d213`.

**A usable complete path now exists.** The optional [source_calculation_path.py](../../tools/source_calculation_path.py) reads a byte-bound source record, binds identity and each count's role/state, checks a declared model and formula domain, computes exact variance, and returns a conditional criterion answer or a specific withholding reason. [The usage guide](README.md) provides actual runnable positive/missing/zero/proposal demos.

This is the larger integration step that the earlier reader failures motivated. It does not improve the135Mmodel's weights or general reasoning, and it does not authenticate source truth or empirical independence. Its useful scope is a small declared source grammar and one conditional model, with all input/decision stages inspectable.

## Cycle 1: build the connected component

[BUILD_PLAN.md](BUILD_PLAN.md) predates implementation. The246-line tool is standalone/optional and reuses the existing strict JSON loader from `evidence_threshold.py`. Existing field-role guard, threshold comparator, runtime/core/schema and their historic results are unchanged. No default source rewriter or model self-certification policy is installed.

The path is:

`source bytes + contract -> literal identity + role/state binding -> model/domain checks -> exact Fraction calculation -> at-most answer + receipt`

The caller supplies a source-relative path/SHA256, literal entity/scope, claim ID, named model/parameters/assumptions and criterion. The source has an identity header plus a complete supported count description. Known/missing/absent/planned states remain distinct. No field can silently absorb another field's number; extra unsupported text cannot be partially consumed. English number tokens0–99and bounded digit counts are supported within literal sentence templates, not as general NLP.

The model is an equal-cluster Bernoulli mixture. Under declared independent soil draws/equal observations per soil/conditional iid emissions and positive observed k,m:

`V = between/k + within/(k*m)`.

The checker enforces nonnegative bounded decimal parameters, mean in[0,1], and `between+within=mean*(1-mean)`. Those constraints ensure internal model arithmetic consistency; they do not establish the assumptions in a real population. Comparisons use exact fractions; displayed decimals are approximations with a recorded32digit display precision. A degenerate model can legitimately have zero variance with positive counts; zero sample count is a different domain issue.

Missing fields withhold at `source_missing`; a knownzero or planned/uncollected observations withhold at `outside_domain`. Unsupported language, malformed contracts, wrong identity/hash and wrong proposals have separate stages. The first blocking stage stops processing; later checks are not claimed to have run. Source/contract/tool/dependency fingerprints make the computation/source version reviewable, not authenticated empirical truth or hardened runtime attestation.

An optional typed proposal mode checks exact field roles, states, values and source clauses before proceeding. Direct deterministic mode needs no model. Thus a model's inability to produce the new interface does not make the tool unusable; no actual model witness-production capability is claimed. [The guide](README.md) specifies every grammar and interface boundary.

Twelve meaningful development test groups pass, including equality boundary, distinct count-role arithmetic, number words, missing/absent fields, zero/planned states, whole-source rejection, identity/hash/root bounds, numeric model invariants, adversarial proposals, bounded/UTF8input and fresh-process CLI/duplicate-JSON behavior. [Development stdout](DEVELOPMENT_TESTS.stdout), [stderr](DEVELOPMENT_TESTS.stderr), and [test code](test_path.py) are retained. No post-freeze code repair was needed.

## Cycle 2: evaluate the whole path

After code/development,20newauthored source-contract fixtures and independent expected keys,31old-source-body regressions,9curatedproposal fixtures and the evaluator were frozen before execution in [EVALUATION_FREEZE.json](EVALUATION_FREEZE.json). The [protocol](EVALUATION_PROTOCOL.md) distinguishes authored fixture acceptance from hidden independent validation. Neither these fixtures nor the exposed regressions establish population success rates or broad scientific superiority.

| Evaluation | Matched declared expectations |
|---|---:|
| New source-contract fixtures | 20/20 |
| Historical source-body regressions | 31/31 |
| Caller-authored typed proposals | 9/9 |
| Total | 60/60 |

Matching requires the stage, conditional answer, exact numerator/denominator when computed, bound role values/states and source quotation consistency. A coincidentally correct label with wrong fields or arithmetic fails. [Every receipt](checked_run/RECEIPTS.json) and the [summary](checked_run/SUMMARY.json) are saved; the evaluator does not supply expected keys to the path itself.

Among20newfixtures,8compute exact conditional answers and12withhold for their declared reason. This mix is deliberately adversarial, not a deployment coverage estimate. Six of the withholds are missing/domain cases; the others exercise unsupported content, wrong identity/hash and invalid model declarations. Approximation/correction language is refused because it exceeds the interface, not because its real-world meaning is universally unknowable.

Examples:

- k=4,m=16 yields exactV=1/100 andYESat the .01equality boundary.
- k=5,m=9 yields52/5625; k=9,m=5 yields4/625. Same total observations, different cluster role: the exact values matter even though both criterion labels areYES.
- Missing k with18observations/soil binds k as missing and refuses to invent18soils.
- Known k=0 with planned9observations retains0as recorded and stops at the estimator-domain boundary.
- Planned-but-uncollected observations remain planned even when the soil count is positive.
- A valid degenerate declared model with positive counts returns exact variance0, rather than treating every zero as missing/invalid.
- Extra correction/instruction clauses do not become ignored trailing text; wrong record identity/hash prevents reuse.

The31historical bodies come from FG/MF/SFcases. Their old body text is byte-preserved under an explicit caller-added record identity header; origin IDs/file/body hashes are retained in [REGRESSIONS.json](data/REGRESSIONS.json). The header is not claimed to be an original identity supplied by those experiments. Regression arithmetic keys are new conditional calculations over known source counts, not a relabeling of earlier model reasoning or arithmetic results. All prior failed outputs and the FG5/7gate remain failed.

The9proposal cases contain2faithful proposals and7invalid/false proposals. A faithful missing-state proposal binds but still withholds calculation. Swapped roles, invented values for unrecorded fields, zero-to-missing changes, planned-to-observed changes, wrong quote/hash and JSONnullallreject as declared. Proposals were caller-authored, not generated by a model; rejection rate alone is not evidence of useful LLM witness coverage. [PROPOSALS.json](data/PROPOSALS.json), [FIXTURES.json](data/FIXTURES.json) and [EXPECTED.json](data/EXPECTED.json) remain frozen.

A fresh-process CLI equality demo and four further CLI smoke examples (missing/zero/wrongproposal/faithfulmissingproposal) exercise the real entrypoint, not just the library. [Demo checks](DEMO_CHECKS.json) reference already frozen cases; these are not additional independent scientific trials. The guide links all runnable inputs and expected receipts.

## Cycle 3: keep the model's candidates separate from authority

Ten new direct source/formula/domain questions were frozen before actual local inference in [model_diagnostic/FREEZE.json](model_diagnostic/FREEZE.json). These use C01-C10:6validnumeric,2source-missing,2zero/domain tasks. The model receives original source/header and explicit formula/conditions, with no checked receipt or gold answer. Unsupported-language acceptance tests are separate, avoiding an unfair semantic penalty for a model understanding language outside our parser.

The model answers **YESonall10calls**, matching4/10labels, exactly the constant-YESbaseline. It matches4/6numeric task labels and0/4missing/domain task labels. All10reachEOS. Bare-label matches demonstrate neither extraction nor calculation; no reasoning or numeric values were shown. Case-insensitive formatting is10/10; exact uppercase formatting0/10and is not treated as a semantic defect.

[Raw outputs](model_diagnostic/RAW_OUTPUTS.jsonl), [scores](model_diagnostic/SCORES.json), [summary](model_diagnostic/SUMMARY.json), [protocol](model_diagnostic/PROTOCOL.md), [keys](model_diagnostic/KEYS.json), runtime/stderr and source/token/cache metadata preserve every answer. No retry, continuation, prompt optimization, examples, weight update or paid API occurred. Whole-response scoring was coordinator-only, not independent/masked; all completion outputs were viewed before structured scoring.

These outputs are untrusted candidate answers and never authorize the path's source fields, assumptions or receipts. This is a new deterministic path rather than reopening the old failed small-model extraction gate. Its integration advantage is a bounded executable route to a conditional answer despite weak candidate answers; it does not teach the model, establish autonomous model witness production, or validate arbitrary open-world source interpretation.

The program and model perform different work under different interfaces/costs. Their counts are component diagnostics, not a token-matched causal claim of broad superiority. No downstream claim about full reasoning quality, actual world variance, global memory or FRR efficacy follows.

## Working artifact and scope

Run from a CERTX checkout:

```sh
python FRR/tools/source_calculation_path.py FRR/evaluation/complete-verification-path-v1/demo/contract.json --root FRR/evaluation/complete-verification-path-v1/demo
```

[Guide](README.md), [working example](../../examples/complete-source-calculation-path.md), [positive receipt](checked_run/DEMO_RECEIPT.json), [missing receipt](demo_missing/RECEIPT.json), [zero receipt](demo_zero/RECEIPT.json), [rejected proposal receipt](demo_missing/wrong_proposal_RECEIPT.json).

This optional component can now be invoked explicitly in our work. Source hashes are byte identity, not authenticity; caller-declared model assumptions are not empirical evidence. Unsupported records withhold and need an explicitly reviewed adapter, not an invisible paraphrase. The grammar is small by design; actual deployment coverage is unknown. The model arm did not attempt typed proposals, so no real LLM witness coverage was measured. The existing broad queue statuses/core/runtime/schema remain unchanged; this is one usable conditional component, not completion of their larger questions.

The pressure/equalization intuition is preserved in [PRESSURE_LENS.md](PRESSURE_LENS.md) as an open research lens. A possible empirical version would identify a shared upstream assumption/representation, intervene on it in one task and measure effects on another with controls. This build links earlier failures to new engineering requirements; it does not test physical pressure, a conservation law, or a universal dynamics of understanding.

## Costs, preservation and next ecosystem step

The deterministic evaluator's60library calls total .0116seconds, excluding interpreter/import/startup/demo CLI and fixture preparation. This is an observed local instrument timing, not an end-to-end service benchmark. The10small-model calls use2,290inputtokens,20emittedtokens,7.2359secondsinference excluding load/serialization, and .0629secondscache serialization. No speed ratio is inferred from these different scopes/capabilities.

Small model: pinned `HuggingFaceTB/SmolLM2-135M-Instruct` at `12fd25f77366fa6b3b4b768ec3050bf629380bac`, CPUfloat32/eager,2threads,eval/inference,argmax,64-new-tokencap,freshcontexts. Python3.12.14,torch2.6.0+cpu,transformers4.57.1. No paid service or training. The main assistant remains separate; model candidates do not alter scientific/gating keys.

Ten new caches totaling106,033,040bytes remain in `/workspace/smollm_complete_path_states_v1`. Every cache's byte hash/sequence dimension/token prefix, full input/output IDs and decoded/rendered text was checked. The final emitted token may not have been forwarded; prefix counts preserve that boundary. Binaries stay local, with reconstruction IDs/model pin recorded; workspace persistence is not guaranteed. This does not provide main-assistant cache access or chat-storage improvement.

Before building,2,797oldFRRfiles were snapshotted. Before model inference,2,817preexistingfiles (including the new frozen code/data) and343recordedmodel/oldcachefiles were snapshotted and [checked unchanged](model_diagnostic/PRESERVATION_AFTER_GENERATION.json) before integration. Seven older current documents are byte-archived in [ARCHIVE_RECEIPT.json](ARCHIVE_RECEIPT.json). Moved relative links retain their original bases; use original paths at the parent commit for historical navigation. New code/data/reports, not historical rewrites, supply this component. [Final checks](FINAL_CHECKS.json) state exact preservation/source/link coverage. No independent or masked review is claimed.

**Next larger contact:** put one real stored experiment/research record through a reviewed typed adapter and an appropriate second recipe, carrying the same identity/role/state/assumption/receipt boundaries. Do not apply the soil-variance formula to an unrelated metric. That would test reusability of the workflow pattern beyond authored teaching records, with unknown/unsupported cases retained. Useful LLM witness production remains a separate measured interface question. No background task remains active.
