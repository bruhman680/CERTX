# Evidence boundary transfer: retain proposals, verify source support

1 November 2026 UTC. Prospective frozen contact using the existing adapted SmolLM2-135M reader. [Protocol](PROTOCOL.md) · [cases](DATA.json) · [checker](verifier.py) · [raw model outputs](run/RAW.jsonl) · [case/policy receipts](run/ROUTES.jsonl) · [summary](run/SUMMARY.json) · [audit](CHECKS.json).

## Scope and separation

The target names Fennel, Nettle and Yarrow differ from recent worker studies, but are not globally novel words. Distractors are Pepper, Bramble and Marigold. Sources use three deliberately declared layouts: line blocks, bracket records and JSON record lists. We authored a parser for these formats and supply format metadata out of band. This tests a designed contract, not automatic arbitrary-format understanding, external source truth or a general verification layer.

Every case receives a raw model proposal, including cases the checker holds. The checker reads only source text, target and layout; authored expected categories are test metadata, not inputs to the checker or model. When the source supports a unique target value, a selected-record worker receives a canonical line-format snippet. Source-record index witnesses, original source, warnings, raw proposal and worker output remain separate. Nothing silently rewrites the raw answer or deletes inconvenient records.

The parser already reads the status literal, so a mechanical mapping could answer every supported case without a model. Worker success does not establish that the model adds otherwise unavailable semantic reasoning. Successful selection/normalization belongs to the code; model readout is measured separately.

## Cases and declared checking rules

324 logical cases cover single complete records, target/distractor pairs in both orders, consistent duplicates, conflicting complete target values in both orders, target name-only partial plus full record in both orders, other-only/name-only/status-only/invalid-status/absent/malformed sources, unattributed status plus full target, conflicting non-target records plus full target, and partial non-target plus full target.

Two rules are compared. Strict holds when any target record lacks a status. Supported permits a complete unambiguous target statement alongside a name-only target record, retaining that partial record as a warning. Under this asserted-facts contract, a missing value does not itself assert a contradictory value. Neither policy establishes which source is newer or more authoritative; no revision or authority information is supplied.

Both hold conflicting complete target values, invalid target status, lost record attribution, unsupported syntax/schema, absent source and absent target. A known non-target partial or conflict does not override a complete target statement. These distinct receipts are not all relabeled UNKNOWN, and a code hold is not evidence that the model recognized an error.

JSON duplicate keys, duplicate line/bracket fields and unknown schema keys are rejected rather than silently last-write-winning. Consistent complete duplicates retain multiple source witnesses, but do not become independent confirmations. The authored checker matches its expected categories on all cases in pre-run tests; that is functional coverage, not an independent discovery or proof of universal safety.

## Completed results

318 unique raw-source calls plus nine unique selected-record calls =327 actual generations. Empty-source layout variants share identical model inputs and are deduplicated; 324 source cases × two policies produce648 logical receipts. Selected-worker results are deliberately reused across formats/orders/policies.

| Policy | Cases | Supported | Held | Raw answers consistent on supported cases | Selected-worker answers consistent on supported cases | Raw class-label proposals on held cases |
|---|---:|---:|---:|---:|---:|---:|
| strict | 324 | 144 | 180 | 102 | 144 | 160 |
| supported | 324 | 198 | 126 | 149 | 198 | 112 |

| Layout | Supported-policy supported cases | Raw consistent | Selected-worker consistent | Held |
|---|---:|---:|---:|---:|
| brackets | 66 | 46 | 66 | 42 |
| json | 66 | 51 | 66 | 42 |
| lines | 66 | 52 | 66 | 42 |

| Case family | Cases | Strict supported | Supported-rule supported | Supported-rule raw consistent | Supported-rule worker consistent |
|---|---:|---:|---:|---:|---:|
| absent | 9 | 0 | 0 | 0 | 0 |
| conflict | 54 | 0 | 0 | 0 | 0 |
| conflicting_other | 18 | 18 | 18 | 12 | 18 |
| duplicate_same | 27 | 27 | 27 | 25 | 27 |
| invalid_status | 9 | 0 | 0 | 0 | 0 |
| malformed | 9 | 0 | 0 | 0 | 0 |
| name_only | 9 | 0 | 0 | 0 | 0 |
| orphan_plus_full | 18 | 0 | 0 | 0 | 0 |
| other_only | 9 | 0 | 0 | 0 | 0 |
| pair | 54 | 54 | 54 | 24 | 54 |
| partial_other | 18 | 18 | 18 | 16 | 18 |
| partial_plus_full | 54 | 0 | 54 | 47 | 54 |
| single | 27 | 27 | 27 | 25 | 27 |
| status_only | 9 | 0 | 0 | 0 | 0 |

The extra54supported cases are partial-target-plus-full sources. They become answerable under the supported rule with retained warnings, rather than losing their partial records. This is an explicit change in evidence contract, not a learned repair or proof that all partial-plus-full sources are safe under unknown revision semantics. The strict alternative remains recorded.

Both policies retain all54conflicting-target cases as CONFLICT. Unknown target status, missing attribution, invalid formats and actual absence retain different categories. For held cases there may be no uniquely warranted class label, so raw model proposals are counted and retained rather than scored against an invented hidden answer. A well-formatted answer is not automatically source-supported.

Supported-rule verdicts: `{'CONFLICT': 54, 'FORMAT_ERROR': 9, 'INVALID_STATUS': 9, 'PARTIAL_TARGET': 9, 'READY': 198, 'SOURCE_ABSENT': 9, 'TARGET_ABSENT': 9, 'UNATTRIBUTED': 27}`. Warnings: `{'consistent_duplicate_target_statements': 27, 'other_partial_record_retained': 18, 'target_record_without_status_retained': 54}`. Raw unique-output labels: `{'INVALID': 30, 'NO': 109, 'WITHHOLD': 50, 'YES': 129}`. These are model outputs and code receipts, not model uncertainty judgments.

## What this supports and what remains open

The checker can expose a meaningful boundary between a supplementary partial record, a conflicting complete claim, and a record that cannot be attributed. In the tested grammar it can keep proposals moving while withholding endorsement where support is missing. It need not turn every incompleteness into a global stop.

The selected worker receives a source that has already been identified and normalized by code. Nine unique worker responses underpin many logical receipts; do not treat those repeated bindings as hundreds of independent model successes. Formatting and record selection change together between raw and selected prompts. This does not identify a neural cause of raw errors or prove that normalization alone is sufficient on arbitrary data.

The largest unresolved boundary is source revision and authority. A complete old claim may conflict with a new replacement; a partial update may preserve an earlier field, delete it, or leave it unspecified. No such semantics exist here. The strongest next contact is an explicitly declared revision/authority experiment with genuine conflicts and partial updates. Preserve prior versions and test replacement versus patch rules before selecting latest/highest values by convention. A decision rule must not silently manufacture chronology.

Fresh names and three layouts provide a small transfer contact, not broad independent replication. Add mixed formats, unsupported/unknown fields, provenance loss and real source uncertainty before making wider checker claims. The exact format metadata and hand-coded parser are advantages that general sources will not necessarily provide.

The wider model feedback/exploration loop remains parked. The earlier UNKNOWN notepad remains history; no rationale is invented, no small-model self-correction or calibrated uncertainty claim is made, and no default core/model/schema/module is replaced here. Broader memory/handoff/planning branches stay open.

## Runtime, audit and preservation

Input/output tokens 30,610/975; generation time 115.371 seconds excludes model loading, checking and documentation. Output cap stops: 0. Sampled working estimate max 1,951,375,360 bytes; RSS max 894,373,888 bytes, below the5,153,960,755-byte guard. Raw-source allowance16tokens; canonical-worker allowance8tokens; no input truncation. Different allowances are a limitation if a raw answer hits its cap; all stops are retained.

Same base HuggingFaceTB/SmolLM2-135M-Instruct revision12fd25f77366fa6b3b4b768ec3050bf629380bac. Base SHA2565af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c; canonical adapter SHA2564d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. Existing CPU float32/eager runtime, two threads, seed73103, greedy fresh caches. Saved dependencies, base and adapter in-memory digests remain unchanged.

Four test groups and the run audit pass, covering every authored case under both policies plus adversarial duplicate-field, conflict, attribution and partial-record fixtures. All327actual inputs/token IDs/decodes/stops,648receipts, canonical witness indices and selected-worker bindings are audited. 3,900 older local files unchanged before sync; four current navigation/method-note originals archived.

No training/new weights, external paid APIs/rental, installs/downloads, action tools, default policy/core/schema/general-tool/queue changes, new capsule or restore/optimizer-resume/independent-backup claim. Dense model/runtime remain local, while code/data/raw outputs/receipts are preserved in GitHub. No account billing/usage visibility and no background model job remains.

To reproduce in a fresh study directory: run tests, venv `study.py prepare`, venv `study.py run`, stdlib `study.py score`, venv `verify_run.py`. Files are created exclusively; do not overwrite this frozen contact. Preparation parses fixtures and tokenizes locally before the freeze, but never loads the model. Preserve local checkpoint dependencies or declare new ones in a separately frozen run.
