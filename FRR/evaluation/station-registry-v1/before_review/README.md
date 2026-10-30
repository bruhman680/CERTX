# Optional station registry

The registry makes four existing verification receipts inspectable together while preserving their separate questions, recipes, source hashes and states. It produces no shared truth verdict or pooled score. [Protocol](PROTOCOL.md), [real manifest](manifest.json), [registry receipt](REGISTRY_RECEIPT.json), [checks](CHECKS.json), and [report](REPORT.md).

Run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/station_registry.py evaluation/station-registry-v1/manifest.json --root "$PWD"
PYTHONDONTWRITEBYTECODE=1 python evaluation/station-registry-v1/test_registry.py
PYTHONDONTWRITEBYTECODE=1 python evaluation/station-registry-v1/check_results.py
```

The first command prints the JSON registry to stdout. Choose a new destination to preserve a later run; do not overwrite the frozen demo receipt. The final command verifies existing frozen/demo files and rewrites the reproducible post-demo `CHECKS.json`.

To add a station in a separate manifest, copy the explicit declaration schema:

```json
{
  "registry_id": "your-registry",
  "stations": [{
    "station_id": "unique-station",
    "question": "Exact scoped question this receipt addresses",
    "recipe": "Actual tool and relevant conditions",
    "state": "Actual completion, withholding, training and review state",
    "receipt": {"path": "relative/receipt.json", "sha256": "64 lowercase hexadecimal characters"},
    "ancestry": [{"role": "declared_input", "path": "relative/input.json", "sha256": "64 lowercase hexadecimal characters"}]
  }]
}
```

Use actual SHA256 file-byte hashes, not these placeholders. Root-relative paths and symlinks must remain inside the supplied root. No artifact may exceed one MiB. Ancestry may be empty. The tool supports only the two computed receipt schemas described in the protocol; other schemas or states remain unresolved. Existing source files are never modified by the tool.

Read `status` for both registry and station before using a summary. `reported_receipt` relays a byte-bound JSON value; it is not a fresh result of rerunning that receipt's producer. Source truth, key correctness and model assumptions remain external. `ancestry_warnings` surfaces shared hashes, including the narrow-training arms' shared parent inputs and keys despite different arm-key hashes. Shared hashes do not constitute independent witnesses, and absent warnings do not prove independence. Different answers from different declared questions are not contradictions.

`prepare_demo.py` constructed the frozen real manifest once and refuses to overwrite `FREEZE.json`. It is a preservation aid, not a general registry command. The prototype remains optional and separate from existing FRR core/schema and existing verifier tools.
