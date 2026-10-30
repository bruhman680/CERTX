# Optional read-only station registry, version 0.1

Frozen before the real four-receipt demonstration. This is an index over existing receipts, not another model evaluation, truth service, training run or tool-competence benchmark. Receipt construction and demonstration are by the station-registry subagent; subsequent coordinator review is separate and is not independent replication or masked review.

## Contract

`python tools/station_registry.py MANIFEST --root ROOT` prints JSON to stdout. The caller chooses where to save it. Exit 0 means every station was indexed; exit 2 means invalid manifest or one or more unresolved stations. No file writes, network, model calls, imports of training libraries or execution of referenced artifacts. Standard Python import caching may create normal interpreter `__pycache__` files; use `PYTHONDONTWRITEBYTECODE=1` when running.

Strict JSON uses the existing `evidence_threshold.load_json`: duplicate keys and nonfinite constants fail. Manifest and every referenced artifact are limited to one MiB; up to 64 stations, 32 ancestry references each. Relative file references resolve inside the supplied root, including symlink resolution. Local trusted workspace only: no protection against concurrent malicious filesystem mutation or authenticated runtime guarantee.

Manifest has exactly `registry_id` and `stations`. Each station has exactly `station_id`, `question`, `recipe`, `state`, `receipt`, `ancestry`. IDs must be unique. Question/recipe/state are nonempty caller text; they are not inferred from model outputs. Receipt reference is exactly `{path,sha256}`; ancestry references are exactly `{role,path,sha256}`. References use lowercase SHA256 over exact file bytes. Ancestry roles and links are caller declarations. Reading and hashing an ancestry file does not establish that a tool actually used it.

## Supported receipt projections

Two explicit receipt versions only: `source-calculation-path-0.1` computed deterministic conditional answers, and `stored-run-audit-0.1` computed cohort summaries. Unknown versions, extra top-level fields, unsupported states or malformed projections remain unresolved. The registry preserves parsed bound receipts in `reported_receipt`, including their own source hashes, assumptions, limitations, unresolved outputs and rows. The exact original byte hash remains in `receipt_reference`. Parsing preserves JSON values, not lexical whitespace or number spelling.

The source projection relays declared entity/scope, conditional answer, criterion, model assumptions, and variance. It does not redo source extraction, arithmetic or validate source truth. The audit projection checks envelope/identity/source-hash shape; exact row identities/labels/match booleans; uniqueness; row/summary counts, labels, constant-YES count, rational fraction, and stop totals. It retains all unresolved rows in the denominator. It does not rerun the auditor, tokenize/decode, authenticate keys, verify raw runs, or check token counts against raw bytes. Nested source arithmetic remains reported data rather than an independent calculation.

A station can retain a valid receipt projection while an unavailable ancestry file makes the station unresolved; consumers must inspect station `status`. Unsupported bound receipts are retained without `scoped_summary`. Invalid/unbound receipt bytes are not projected.

## Ancestry and interpretation

Collect identical hashes across station receipt bytes, reported source hashes and bound declared ancestry. Each shared hash produces `shared_hash_observed` with roles and stations. The warning identifies shared byte identity or a reported hash, not independent confirmation. No warning implies nothing about independence: different arm-specific key hashes may derive from the same keys. No inference of contradiction arises from different tasks, criteria, scopes or labels. No pooled fraction, majority vote, confidence or universal answer exists.

The real manifest binds four already-exposed receipts: source variance demo; ten-call full conditional-task direct-model audit; original 48-case narrow source-state audit; adapted 48-case narrow source-state audit. The last two bind shared EVAL_CASES, KEYS, TRAINING_MANIFEST and REPORT bytes while retaining distinct arm receipts/raw/key subsets. Their state declarations preserve one completed update, missing-class nonexposure, memory stop, exposed test status and no promotion. Different tasks and token caps prohibit treating their scores as one common measure.

## Freeze and acceptance

Before demonstration, run adversarial tests; freeze tool, loader, test, protocol, manifest and all referenced input bytes in `FREEZE.json`. Then run CLI once to `REGISTRY_RECEIPT.json`; compare every frozen file and source bytes afterward in `CHECKS.json`. Expected: four indexed stations; source conditional YES; separate 4/10, 4/48 and 16/48 summaries; 36 unresolved original-test outputs; shared input/key ancestry warnings; no pooled score. A repeat deterministic byte comparison is a replay consistency check, not an independent run. Preserve test output and hashes. Failures require a documented amendment before another demo.

Adversarial acceptance covers altered bytes, missing ancestry, duplicate JSON/nonfinite values, path traversal and symlink escape, unsupported versions/fields, forged/truncated summaries, bool-as-count, duplicate run IDs, impossible fractions, altered label counts, full unresolved denominator, shared dependencies, distinct declared questions, manifest extras/duplicates, size bounds, and read-only CLI behavior.
