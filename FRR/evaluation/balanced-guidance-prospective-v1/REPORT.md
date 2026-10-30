# Balanced guidance: prospective paired small-model contact

30 October 2026. Three stages completed: freeze/build, actual generation and audit, integration/sync. Coordinator-only design and review; no independent or masked review and no swarm run.

## Result first

**Both ordinary and compact guidance scored 4/12. All 24 generated answers were `Yes`.** Each arm has four YES, four NO and four WITHHOLD keys. Every constant-label baseline scores 4/12. Neither arm distinguishes the NO or WITHHOLD cases; the four matched answers do not demonstrate calculation or grounded source reading. No guidance/default change is justified by this pilot.

| Quantity | Ordinary instruction | Compact role/domain guidance |
|---|---:|---:|
| Actual calls | 12 | 12 |
| Label matches, full denominator | 4/12 | 4/12 |
| YES keys matched | 4/4 | 4/4 |
| NO keys matched | 0/4 | 0/4 |
| WITHHOLD keys matched | 0/4 | 0/4 |
| Normalized output labels | 12 YES | 12 YES |
| EOS stops | 12 | 12 |
| Input tokens | 2597 | 3053 |
| Generated tokens, including EOS | 24 | 24 |
| Measured inference seconds, excluding serialization | 7.882 | 9.445 |
| Cache serialization seconds | 0.081 | 0.080 |
| New preserved cache bytes | 120281472 | 141294144 |

Paired cases: four both match, eight neither matches; zero ordinary-only and zero compact-only gains. Exact measured times are recorded in [SUMMARY.json](SUMMARY.json). This single CPU run does not establish a general latency ratio. The compact arm uses 456 more input tokens without a label-score gain here.

## Question and prospective design

The [plan](PLAN.md), [12 cases in two arms](CASES.json), separate [keys](KEYS.json), [key authoring](KEY_AUTHORING.json), [guidance](GUIDANCE.json), model pin, runner, scorer and existing audit dependency were hash-frozen in [FREEZE.json](FREEZE.json) before any inference. The coordinator knew earlier all-YES findings but did not see these new outputs when specifying the protocol or keys.

The question is whether this particular compact instruction package improves exact normalized-label matches on a balanced conditional variance exercise. It is not a test of all FRR reasoning, a trained FRR model, or the efficacy of distributed verification.

Each source states the independent-soil count k and collected observations per soil m, or explicitly marks a missing/zero/planned condition. The shared task states the assumptions and rule:

    V = 0.032/k + 0.128/(k*m)

For known strictly positive k,m and collected observations, YES means V <= 0.01 and NO means V > 0.01. Missing counts, zero counts or only planned/uncollected observations require WITHHOLD. These are authored conditional math exercises, not empirical observations of a real garden. Source claims of independence are declared assumptions, not experimentally verified facts.

Before inference, exact rational keys were checked against the independently rearranged integer inequality `32*m + 128 <= 10*k*m` where counts are valid. Keys were separately specified from model outputs, not independently expert-reviewed. B10 (k16,m1) is the equality case. Withheld cases are missing k (B03), missing m (B06), zero k (B09), and planned/uncollected m (B12).

| Case | k | collected m | Exact declared variance | Key |
|---|---:|---:|---:|---|
| B01 | 4 | 32 | 9/1000 | YES |
| B02 | 7 | 2 | 12/875 | NO |
| B03 | missing | 11 | not calculated | WITHHOLD |
| B04 | 8 | 4 | 1/125 | YES |
| B05 | 2 | 64 | 17/1000 | NO |
| B06 | 14 | missing | not calculated | WITHHOLD |
| B07 | 10 | 2 | 6/625 | YES |
| B08 | 3 | 16 | 1/75 | NO |
| B09 | 0 | 5 | outside domain | WITHHOLD |
| B10 | 16 | 1 | 1/100 | YES |
| B11 | 6 | 1 | 2/75 | NO |
| B12 | 20 | planned8, none collected | outside domain | WITHHOLD |

Both arms share source and question. Ordinary guidance asks for a grounded answer without adding absent facts. Compact guidance explicitly separates k and m, checks known/collected/positive status before arithmetic, and directs comparison of the two-term sum. It is one task-relevant instruction package, not a broad FRR base. Instructions differ in content and length; costs are reported, not matched away.

Each call starts from a fresh context with the same pinned model and greedy decoder. Within each case pair the execution order alternates by case index. This avoids making one arm always first but is not randomization, multi-seed evaluation or independent sampling. No output-dependent retries, continuations, case selection or prompt repairs occurred.

## Actual model and artifact checks

The existing local HuggingFaceTB/SmolLM2-135M-Instruct revision `12fd25f77366fa6b3b4b768ec3050bf629380bac` ran in CPU float32/eager eval/inference mode, two threads, argmax decoding, 64-token cap, local files only and no remote code. Every call stopped at EOS after two generated tokens. No optimizer, training, model update, paid API or rented compute was used.

[RAW_OUTPUTS.jsonl](RAW_OUTPUTS.jsonl) retains all prompts, input/output token IDs, text, timing and cache metadata. All 24 completion texts were viewed in the log before structured scoring; review was not blind. [RAW_FREEZE.json](RAW_FREEZE.json) binds the completed log/manifest before scoring. A harmless torch_dtype deprecation warning is retained in RUN.stderr; inference and checks completed.

[Artifact checks](ARTIFACT_CHECKS.json) verify all 24 rendered prompts, input-token sequences and decoded outputs against the pinned tokenizer; all 24 local cache files by hash, byte size, token-prefix binding and tensor sequence dimensions; and all 346 recorded prior model/cache files unchanged. The new cache branches remain local under `/workspace/smollm_balanced_guidance_states_v1`; binaries are not uploaded to Git. Token metadata in the raw source is additionally checked by the audit tool. These are consistency checks, not an independent model implementation or proof of empirical truth.

## The new audit path used prospectively

The frozen [scorer](score.py) checks the full raw cohort against all 24 predeclared ordered IDs before making per-arm views. Each arm view preserves exact selected raw lines and has a source hash plus a [derivation receipt](ordinary/DERIVATION.json). No rows are selected by correctness or output label.

The unchanged [stored_run_audit.py](../../tools/stored_run_audit.py) then binds each arm's raw/key source, expected cohort and identity and produces [ordinary](ordinary/RECEIPT.json) and [compact](compact/RECEIPT.json) receipts. Its frozen `strip_upper_exact_label_v1` parser accepts only whole responses that become YES/NO/WITHHOLD after stripping and uppercasing. Unsupported answers remain UNRESOLVED in the denominator. There were none in this run; that does not make the wrong labels acceptable.

This is the first prospective use of this optional audit path on a newly frozen paired experiment. The prior [stored-run audit](../stored-run-audit-v1/REPORT.md) was retrospective. Operational reuse is demonstrated here; it does not establish independent corroboration, model improvement, source authenticity or a universal verifier.

## What this narrows and what remains open

High confidence within this frozen run: execution completed as specified; both prompt packages generated all YES; there was no paired label gain; prior artifacts were preserved. Rephrasing these particular instructions did not produce useful discrimination.

The mechanism remains unknown. This experiment does not isolate arithmetic weakness, source interpretation, default-answer behavior or instruction-following failure. It also does not establish that a larger/different model, training intervention or materially different interface would fail. The authored cases and deterministic reused model are not 24 independent observations of a population effect. No FRR benefit or harm estimate follows.

The earlier failed source-reading gate stays failed. The deterministic calculation tool remains useful under its stated source grammar and assumptions; it is not retroactively credited to the model. No model output is allowed to authorize source fields or change an accepted deterministic receipt.

## Next direction and pacing

More variants of this same full-task prompt now have a weak expected return. Keep the small model as an untrusted experimental proposer; do not assign it arithmetic or missingness authority on this evidence. Move the next larger build toward a read-only station registry over existing receipts: preserve each question, source ancestry, recipe and withholding state, expose incompatibilities, and avoid multiplying copied evidence or voting different tasks into one truth score. This would operationalize the user's [distributed-stations idea](DISTRIBUTED_STATIONS_LENS.md) without pretending that a central station can repair false assumptions by aggregation. The registry is proposed, not installed by this run.

A three-stage cadence remains appropriate where it produces a usable artifact, a meaningful challenge, then an honest integration decision. This run fulfilled that cadence and stopped without additional output-driven experiments. Raw errors and failed predictions are part of the soil we retain.
