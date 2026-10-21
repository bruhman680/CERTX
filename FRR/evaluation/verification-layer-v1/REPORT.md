# VL-C1: a usable verification layer and a verifier repair

The user asks whether our collected work and PID skeleton can support a more reliable verification layer that improves alongside discoveries. Yes, as an explicit scoped evidence contract, bounded checking practice and versioned repair process. We implemented a narrow prototype and adopted an [optional working module](../../modules/verification-layer.md). It is not a general truth detector, fully automated research judge or demonstrated model-reasoning improvement.

## What the earlier work contributes

| Existing contact | Useful obligation for this layer |
|---|---|
| [Role/reference tests](../EVIDENCE_GATED_ROTATION_REPORT.md) | Check reference provenance and assumptions; independent random noise does not make an inherited reference independent evidence. Supplied provenance is not learned reliability. |
| [PID-C1](../pid-contact-v1/REPORT.md) | Separate measured error from true error; bound intervention effort and avoid accumulation when action cannot help. More control terms can perform worse. |
| [ES-C1](../error-success-contact/REPORT.md) | Locate the alleged failure: premise, inference, measurement, model, objective, action or scope. Correct forecasts can have unlucky realizations. |
| [RR2](../RESET_READER_RR2.md) | Prediction quality, preparation identity and subgroup performance are different outcomes. Keep the task/prior/preparation explicit. |
| [Recovery pilot](../RECOVERY_PILOT_REPORT.md), [REV-C1](../revision-continuity-v1/REPORT.md) | A judge can lack actor-visible evidence. Audit the evaluation input/version, preserve repairs and avoid interpreting missing access as participant failure. Ordinary/FRR comparisons tied in the scoped continuation study. |
| [Bounded loop adoption](../BOUNDED_LOOP_ADOPTION.md) | Separate candidate, evaluator, evidence and decision; preserve failed trials and evaluator repairs. |
| Palimpsest/sync work and preserved histories | Historical assertions are not current validation. Retain evidence plus linked revisions and a navigable current view. |

These contacts have different substrates and limitations. This is a synthesis of their reports, not independent replication or a causal demonstration that FRR produced the findings. Previously consulted primary sources on control, cybernetics, scoring and metareasoning remain linked in PID-C1 and ES-C1; no new literature search or full-archive audit was performed for this implementation contact.

## Architecture and what is actually implemented

Three responsibilities remain separate:

1. **Domain check:** assess a specified claim against a declared criterion and bound evidence.
2. **Effort control:** decide whether another check can matter, cap repetition/cost and preserve unresolved obligations. This is working guidance, not an implemented numerical PID scheduler.
3. **Verifier revision:** preserve what was checked with which code, diagnose verifier failure, replay and publish a scoped revision. A local receipt/log utility supports history; it does not discover scientific corrections autonomously.

The [checker](../../tools/verification_layer.py) produces `supported`, `contradicted` or `unresolved` receipts containing contract/checker hashes, artifact hash when read, scope, criterion, dimension-specific checks, reason and assumptions. Failure of integrity/scope or unavailability of an adapter leaves the claim unresolved rather than asserting factual falsity. Successful literal arithmetic establishes only that calculation. The sensor adapter's conclusions are conditional on supplied bounds and an additive measurement model; these premises are not empirically certified by the adapter.

Two capability configurations were prepared together: 0.1 for restricted exact rational equality; 0.2 adds bounded-sensor interval assessment. These are not historical deployments and their numbers do not change FRR's runtime version. Exact source hash distinguishes code revisions. Local history appends preserve previous events and require a prior claim event plus note for an ordinary supersession. A hash chain cannot stop a writer who changes the entire chain and recomputes hashes.

## Initial prospective instrument contact

[Protocol](PROTOCOL.md), checker, test driver, 22 authored fixtures, separate keys and [manifest](LAUNCH_MANIFEST.json) were published at [2c4c4e96](https://github.com/bruhman680/CERTX/commit/2c4c4e966722d49f94a2db59f9d62525398bd4d0) before the run. 22 cases × two capability versions = **44 evaluations**, no model calls. Cases include correct claims, wrong arithmetic, missing/stale evidence, scope expansion, unknown semantic checks, changed criteria, undefined/forbidden expressions, malformed inputs and sufficient/insufficient/inconsistent sensor bounds. Keys were not passed to the checker. Cases and implementation were authored together; this is development instrument validation, not independent held-out evidence.

[All 44 per-version expected dispositions matched](RESULTS.json); all 14 earlier non-sensor cases retained their verdict across the capability extension. Against the final 22-case contract key:

| Instrument | Key matches | Unwarranted support | Supported cases withheld | Contradictions identified |
|---|---:|---:|---:|---:|
| Always unresolved | 15 | 0 | 4 | 0 |
| Integrity-only | 7 | 15 | 0 | 0 |
| Capability 0.1 | 18 | 0 | 2 | 1 |
| Capability 0.2 | 22 | 0 | 0 | 3 |

The first two are intentionally weak software comparators, not ordinary review or provenance-only reasoning baselines. These figures show how the authored obligations differ; they do not estimate natural-world error rates. Of 22 final-version cases, four are supported, three contradicted and 15 unresolved. High abstention alone is not success; neither is passing all readable artifacts.

Ledger checks passed: original prefix preserved, invalid revision parent rejected, changed event detected without hash repair. The deliberately tested limitation also occurred: rewriting the whole chain and recomputing hashes still passes its local chain check. Authenticity requires additional trusted anchors and source controls.

Artifacts: [initial receipts](RECEIPTS.jsonl), [initial results](RESULTS.json), [development log](DEVELOPMENT_LEDGER.jsonl), stdout/stderr and fixtures are retained. These are software-rule dispositions, not participant outputs.

## The verifier needed its own repair

After the first run, code review found a resource-limit gap: checking string length and then checking rational magnitude after parsing did not bound expansion of a short exponent string. The initial tests had passed without covering that case. Extreme inputs were not run against the original parser.

We preserved the initial artifacts, published [Amendment 01](AMENDMENT_01.md), restricted numeric strings before parsing, and froze a separate [hardening manifest](HARDENING_MANIFEST.json). Initial results and the repair preparation were committed at [d6694958](https://github.com/bruhman680/CERTX/commit/d6694958058d285a94813d416fc27f9abc0f1e1b) before the expanded check. Original source remains at the initial commit; current source has a different hash. The original launch manifest intentionally no longer matches repaired checker bytes. Its unchanged-at-initial-run receipt is historical, not a current-source claim.

[Repaired-check results](HARDENING_RESULTS.json): all 44 earlier dispositions matched their keys again; eight rejected numeric forms included huge positive/negative exponents, ordinary exponent syntax, leading-dot decimal, nonfinite forms, overlong text and a non-string boolean. Six valid plain-number controls passed. Both command-line contacts produced the intended receipt, including a contradicted claim with exit code zero. Automation must read verdict, not confuse process completion with verification success. This was a disclosed engineering repair and regression replay; it supplies no broader security certification.

[Preservation check](INITIAL_OUTPUT_PRESERVATION_CHECK.json) confirms the five initial output artifacts remained byte-identical against hashes pinned before repair execution. Initial and repaired outputs are distinct files. No scientific forecast was retuned or old outcome overwritten.

## Adoption and evolution limits

Use the optional module for consequential claims and builds; leave free exploration available. A claim can stay exploratory while collecting evidence. The layer is not automatically attached to every future action or conversation; an agent/host must use the saved guidance and run suitable checks. Generic empirical, causal, ethical and statistical claims need their own tools/review, not an arithmetic pass label.

Evolution now has a concrete local mechanism: preserve failure → propose checker/criterion revision → freeze changed assumptions and intended verdict changes → replay relevant cases plus new cases → retain both versions and reassess affected claims. The parser repair exercises that mechanism. The adapter extension is a prepared capability example; neither is autonomous learning. Previously exposed fixtures are development material.

Next discriminating work remains the unrun actual-agent comparison against ordinary review and a simpler provenance-only procedure on separately authored error types, with grounded correctness, diagnosis, needless checks, appropriate uncertainty and cost scored separately. Arbitrary broad scientific experiments or the full backlog did not run here. Current package, bounded-loop and queue/core integrity checks are recorded separately. Core FRR prompts/schema remain unchanged.
