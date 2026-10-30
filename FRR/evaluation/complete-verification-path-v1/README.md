# A usable source-to-calculation path

This optional [246-line tool](../../tools/source_calculation_path.py) connects source bytes, record identity, count roles/states, formula-domain checks, exact calculation, and a conditional at-most answer. It runs with Python's standard library and the adjacent existing `evidence_threshold.py` JSON loader; no model or API is required. Python3.12was tested.

From a CERTX checkout containing this FRR directory:

```sh
python FRR/tools/source_calculation_path.py FRR/evaluation/complete-verification-path-v1/demo/contract.json --root FRR/evaluation/complete-verification-path-v1/demo
```

The [source](demo/source.txt) says4independentsoils and16observations/soil. The [contract](demo/contract.json) binds its bytes, literal identity and scope, declares the equal-cluster model, and asks whether variance is at most .01. The [checked receipt](checked_run/DEMO_RECEIPT.json) contains:

```json
{"status":"computed","stage":"conditional_answer","answer":"YES","variance":{"numerator":"1","denominator":"100"}}
```

The full receipt also contains exact source clauses, field states, source/contract/tool hashes, model assumptions and limitations. Decimal display is approximate; comparison uses exact fractions.

Run the missing-source and zero-data branches:

```sh
python FRR/tools/source_calculation_path.py FRR/evaluation/complete-verification-path-v1/demo_missing/contract.json --root FRR/evaluation/complete-verification-path-v1/demo_missing
python FRR/tools/source_calculation_path.py FRR/evaluation/complete-verification-path-v1/demo_zero/contract.json --root FRR/evaluation/complete-verification-path-v1/demo_zero
```

These return `source_missing` and `outside_domain`, respectively, with `answer:null`. They are different reasons for withholding. An observation count cannot fill a missing independent-soil count; known0remains recorded0even when the estimator is undefined.

Try a deliberately false proposal against the missing-count source:

```sh
python FRR/tools/source_calculation_path.py FRR/evaluation/complete-verification-path-v1/demo_missing/contract.json --root FRR/evaluation/complete-verification-path-v1/demo_missing --proposal FRR/evaluation/complete-verification-path-v1/demo_missing/wrong_proposal.json
```

It returns `proposal_binding_mismatch`. [The corresponding receipt](demo_missing/wrong_proposal_RECEIPT.json) shows that assigning18observations/soil to the unrecorded soil-count field is blocked. [A faithful missing-state proposal](demo_missing/correct_missing_proposal.json) binds but still withholds calculation for missing input. These proposal demos are caller-authored, not model-produced witnesses.

## Declared source format

A UTF8artifact, at most65,536bytes, starts with this literal identity header:

```text
Record Garden03 / Batch03.
There are 4 independently sampled soils. Each soil supplies 16 observations.
```

Entity/scope identifiers start with a letter, followed by up to63letters/digits/underscore/hyphen. They must match the contract. Source paths are relative and resolve inside the supplied artifact root. Source SHA256binds the exact file bytes before whitespace parsing; newline conversion is a byte change and requires a reviewed new source binding.

Supported first clauses:

- `There are N independently sampled soils.`
- `N soils were sampled independently.`
- `There are independently sampled soils, but their number was not recorded.`
- `Some soils were sampled independently, but their number was not recorded.`

Supported second clauses:

- `Each soil supplies M observations.` or `Each soil supplied M observations.`
- `Observations per soil were not recorded.`
- `M observations per soil were planned, but none were collected.`

The second clause may be omitted, producing an `absent` observation field rather than inventing one. All body text must be consumed; corrections, extra instructions, duplicate/extra claims, approximate counts and other unsupported language withhold. `N`/`M` are1–9digit integer strings or English number words0–99 (tens compounds use a hyphen), case-insensitive for the number token. Other prose is literal. This is a deliberately small grammar, not an arbitrary language reader. Valid complete source first/second clauses are separated by spaces/tabs on the body line; no information is silently skipped.

The tool labels an explicit soil value `known` and an observation claim `observed` within this declared grammar. Those are source-state tags, not proof the experiment really occurred. `missing` is an explicit unrecorded field; `absent` is an omitted observation clause; `planned` is not collected data. Bound quotes retain their original source text while numeric values are canonical integer strings.

## Model and contract

For a new artifact, review the complete source and its identity/scope, then compute its byte hash and place it in a copied contract together with the appropriate declared model/criterion. For example, from the repository root:

```sh
python -c "import hashlib; from pathlib import Path; print(hashlib.sha256(Path('FRR/evaluation/complete-verification-path-v1/demo/source.txt').read_bytes()).hexdigest())"
```

Hashing a file is a binding step, not approval of its claims or a way to bypass a failed source review. Keep the original and any reviewed adapter separate.

Inspect [the full contract](demo/contract.json). It names `equal_cluster_bernoulli_mixture`, mean/between/within decimal strings, the exact declared assumption list, and an `at_most` threshold. For positive observed counts k,m:

`V = between/k + within/(k*m)`.

The model requires `0<=mean<=1` and `between+within=mean*(1-mean)`. Assumptions are independent soil draws, equal observations per soil and conditional iid emissions. The program checks declarations and arithmetic consistency; it does not empirically establish those assumptions. Numeric contract values are bounded nonnegative ordinary decimal strings (no floats, exponent/NaN syntax); duplicate JSON fields reject. The operator is at-most, including equality.

Zero variance is possible under a valid degenerate declared model with positive counts. Zero sample counts or only planned observations are outside this estimator's domain. Missing fields stop at `source_missing`; known values/states remain in the receipt. Processing stops at the first blocking stage, so an unexecuted later check is not claimed to have passed.

A witnessed proposal, when supplied, requires exact entity/scope/source SHA and both fields, each with `state`,`value`,`quote`. It must equal the source-derived roles/states/values/quotes. A quote containing the right-looking number in the wrong role does not qualify. JSONnullis an invalid proposal, not a request for deterministic mode. Without `--proposal`, direct deterministic mode performs the same binding/computation without requiring any LLM formatting.

## Interpret the receipt

| Stage | Meaning |
|---|---|
| `conditional_answer` | Exact computedYES/NOunder the source grammar and declared model |
| `source_missing` | Explicitly unrecorded or omitted required input; no numeric result |
| `outside_domain` | Knownzero count or planned/uncollected observations invalidate this estimator |
| `unsupported_source` | Full input language/size/encoding is outside the declared grammar |
| `identity_mismatch` / `source_hash_mismatch` | Source context or bytes differ from the binding |
| `invalid_contract` / `invalid_model` | Required typed contract or model declaration is invalid |
| `invalid_proposal` / `proposal_binding_mismatch` | Supplied proposal is malformed or differs from source roles/states |
| `source_unavailable` / `implementation_changed` | Artifact access or loaded-source fingerprint check failed |

Read `status`,`stage`,`answer`,`reason_codes` together. CLI emits a JSON receipt for a withheld case; process exit0is not a proof of a computed or empirically true answer. The file fingerprints are not source authenticity, empirical truth or hardened runtime/bytecode attestation. Local trusted workspace only.

## Evidence and reproduction

[Report](REPORT.md):12development test groups;20newsource-contract fixtures,31historical body regressions and9curated proposal cases all match their60frozen expected stage/value/answer checks. The10small-model diagnostics all answeredYES(4/10labelmatches); they do not authorize the path and no model improvement is claimed.

Run development checks:

```sh
python FRR/evaluation/complete-verification-path-v1/test_path.py
```

Replay the frozen complete-path evaluation to a new output directory:

```sh
python FRR/evaluation/complete-verification-path-v1/evaluate_path.py --output-dir /tmp/cvp-review
```

That directory must not already exist; outputs are preserved rather than overwritten. The freeze binds exact tool/dependency/fixture bytes and intentionally rejects a different implementation. Use the pinned recorded commit for historical reproduction. The model runner also rejects silent reruns; this guide does not launch inference. No broad FRR efficacy, autonomous LLM extraction, universal memory or physical dynamics claim follows.
