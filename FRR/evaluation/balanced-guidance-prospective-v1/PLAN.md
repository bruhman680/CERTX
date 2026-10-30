# Balanced prospective guidance contact

2026-10-30, coordinator-only. New experiment, 12 authored source cases and 2 paired instruction conditions =24 actual local model calls. Three stages: freeze/build, run/challenge/read, integrate/sync. No independent review or population-performance inference.

Question: on a balanced YES/NO/WITHHOLD conditional soil-variance task, does compact role/domain/comparison guidance improve exact normalized-label matches over ordinary guidance? This tests this particular instruction package, not general FRR, training or universal reasoning.

Primary endpoint: full-denominator exact normalized label matches per arm using stored_run_audit.py. Secondary: per-key class outcomes, paired changes, unresolved responses, stop distribution, token usage, measured inference time. Compare constant-label baseline (4/12 each). Unsupported phrases remain unresolved; no post-hoc extraction. No output-dependent retries, continuations, case selection, prompt revisions or default promotion. Existing cache branches preserved; new branch percall.

Keys are specified separately from outputs and independently cross-checked with exact rational algebra before inference. They are coordinator-authored, not independently reviewed. Sources and keys are not sent together to the runner. Caller-declared independence/equal-cluster/conditional-iid assumptions define a math exercise, not empirical soil data.

Arms share cases, rules, model, deterministic decoding and64token cap; instruction length/content differs and token costs are reported. Each call has a fresh context. Alternate within-pair execution order to avoid making one arm always first; this is not randomized sampling or a multi-seed evaluation.12cases are authored diagnostic probes, not independent draws.

Acceptance is faithful execution and inspectable receipts, regardless of which arm wins or whether all outputs repeat YES. New instruction patterns are not adopted from a single pilot. Included local CPU only, no API, training or paid resources.
