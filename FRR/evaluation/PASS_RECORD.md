# Optional exposure and stopping record

Use when an evaluation or evidential comparison relies on multiple passes. This is host metadata, not a required conversational form and not an extension of inquiry schema 0.1.

```json
{
  "pass_id": "P1",
  "prompt_version": "0.2",
  "task_reference": "case or task ID",
  "accessible": ["task statement", "raw observations"],
  "withheld": ["prior proposed answer", "expected behavior", "ratings"],
  "shared_dependencies": ["model version", "source dataset"],
  "exposure_violations": [],
  "rating_method": null,
  "stopping_basis": "Available tests completed within the declared scope"
}
```

Withholding a prior answer can reduce anchoring; it does not remove shared model training or dataset confounds. If material is already in the responding model's context, a request to ignore it does not establish withholding. Use a fresh context with host-enforced access boundaries. Record unavailable information as unavailable rather than inventing a complete dependency inventory.
