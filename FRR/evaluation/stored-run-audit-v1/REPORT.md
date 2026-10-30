# Stored-run audit: a second complete verification recipe

30 October 2026. Three stages completed: build, adversarial challenge, record/sync. Coordinator-only; no new model inference, training, paid services or swarm run.

## What now works

The optional [stored_run_audit.py](../../tools/stored_run_audit.py) carries an actual stored experimental artifact through a typed source contract to an exact summary receipt. The first complete path calculated a declared soil-model variance. This second path counts label matches in a declared model-run cohort. Different questions require different recipes; shared binding practices can carry across them.

This is a retrospective engineering audit of existing data, not new evidence that the small model improved. All ten outputs and the previous summary were already known when the plan was written.

## Source → binding → checks → calculation → receipt

[contract.json](contract.json) selects the ten CVP3 run IDs, literal family/facet/cycle/arm metadata, raw JSONL and separate key JSON, both by relative path and SHA256. Sources are the existing [raw log](../complete-verification-path-v1/model_diagnostic/RAW_OUTPUTS.jsonl) and [keys](../complete-verification-path-v1/model_diagnostic/KEYS.json). Originals remain unchanged.

The adapter checks byte identity before parsing, root containment including resolved symlinks, strict JSON syntax, expected cohort membership and cardinality, key/run uniqueness, row identity, text/stop types, and positive integer token counts matching token-array lengths. Booleans and negative token IDs are rejected. Each bound artifact is limited to 8 MiB; cohort size is limited to 1000. Blank JSONL records and unsupported stop values withhold the receipt.

The declared parser strips leading/trailing whitespace and uppercases the complete response. Only exact YES, NO and WITHHOLD are accepted. Explanations, echoed prompts and empty strings become UNRESOLVED; they remain in the denominator. Case normalization is a scoring convention, not proof of understanding. A token-limit completion with an exact label can count as a label match; its stop remains reported separately. This tool does not interpret whole-response reasoning.

For declared cohort I and provided keys g_i:

    L_i = normalized exact label, or UNRESOLVED
    M = sum_i 1[L_i = g_i]
    match fraction = M / |I|, reduced exactly using Fraction
    constant-YES baseline = sum_i 1[g_i = YES]

No independence assumption or statistical interval is needed to count these stored outcomes. The count does not estimate generalization accuracy. Cohort completeness is checked against the caller's explicit list, not an external guarantee that the caller selected every relevant experiment.

## Observed result

[RECEIPT.json](RECEIPT.json) recomputes 10 calls, 4 label matches, exact fraction 2/5, and 4 matches for constant YES. All ten recorded texts normalize to YES; all ten stop metadata values are EOS. Token metadata sums to 2290 input and 20 output tokens. These agree with the earlier published aggregate after treating omitted zero-count stop categories as zero.

This makes the limitations visible: four correct labels tie a constant answer. It provides no evidence of arithmetic skill, missingness understanding or useful source authorization. It does not reopen the earlier failed source-reading readiness gate.

## Challenge result

[15 test groups](test_audit.py) pass on disposable copies: reordered rows, removed/added/duplicated runs, missing/duplicated/invalid keys, byte tampering, wrong identity with a recomputed hash, Boolean/mismatched/negative token metadata, unrecognized and empty responses, casing/whitespace and token-limit policy, unsupported stop/text types, absolute/escaping/symlink paths, unsupported contract parser/cohort, duplicate JSON/nonfinite/blank/invalid UTF8 records, and unavailable files.

A changed response from a previously correct YES to an explanatory phrase yields 3/10, not 3/9. This specifically guards against improving apparent accuracy by dropping unresolved responses. These are engineering challenge groups, not 15 model experiments or independently sampled cohorts.

[FREEZE.json](FREEZE.json) records code, dependency, plan, contract, tests and expected result after development tests but before the retained receipt/challenge run. Historical data and expectations were already known. [CHECKS.json](CHECKS.json) records retained checks. [REVIEW_NOTE.md](REVIEW_NOTE.md) preserves an initial comparison assertion failure and its narrow repair; frozen code/results did not change.

## Use

From the repository root:

```sh
python FRR/tools/stored_run_audit.py \
  FRR/evaluation/stored-run-audit-v1/contract.json --root FRR
python FRR/evaluation/stored-run-audit-v1/test_audit.py
python FRR/evaluation/stored-run-audit-v1/check_results.py
```

Receipt status/stage must be inspected; CLI exit zero by itself is not acceptance. Withheld stages distinguish invalid contract, unavailable source, bad source hash, invalid source, cohort mismatch and identity mismatch. Unexpected programmer errors are not evidence of successful verification.

Changing a source requires a reviewed new binding. The local contract is trusted configuration. Keys, metadata, source authorship, actual inference and empirical correctness are not authenticated by a hash. Token arrays are structurally checked but not decoded; cache files are not reopened. Earlier cache/token reconstruction checks remain separate evidence in the original study. The tool is a local research CLI, not a hardened service.

## What carries forward

We now have two useful calculation paths sharing a pattern: declare the question and input roles, bind sources, refuse invalid inputs, compute the appropriate quantity, retain an inspectable receipt. This is cross-task engineering reuse; it does not establish a universal truth-verification layer or FRR benefit.

Strong next contact: use the run-audit interface prospectively for a small new, balanced task with a frozen cohort and independently specified keys. Keep raw output, parser policy, unresolved cases and baseline visible before interpreting any model improvement. Add another metric or adapter only when a real task needs it. A three-stage cadence is useful when each stage resolves a distinct uncertainty; it is not a quota requiring three runs on every turn.
