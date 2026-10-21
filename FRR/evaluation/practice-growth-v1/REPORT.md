# PG-C1: practicing useful inquiry through an audit, build and repair

The user clarified the objective: useful reasoning/behavioral habits for our learning and growth, not advantage over other labs or people. We changed the work accordingly. Six engineering collaborators convened; no new guidance-ranking study was run. We followed a concrete premise question into saved data, built a reopening tool, accepted peer criticism, repaired an uncovered binding bug, and improved current navigation while preserving its history.

[Practice record](PRACTICE_RECORD.md) captures the actual short pulse: what changed, which distinction mattered, what contact could change the next move, and what followed. This is an example of use, not proof of a durable best habit.

## 1. Current source, wrong kind of support

A current authentic record can report a valid statistic without supporting the broader claim someone needs. We examined saved PID-C1 noisy-sensor data, distinguishing signed mean error, average magnitude and an all-readings bound. [Protocol](PROTOCOL.md), source/tool hashes and analysis code were pinned at [6f4401c4](https://github.com/bruhman680/CERTX/commit/6f4401c4ff7b687cd4b0e44e11dc16f669465f20) before this new analysis. Original data had already been observed, so this is a retrospective illustrative audit, not fresh confirmatory measurement. Thresholds .01 for absolute signed mean and .08 for pointwise error were fixed for this contact, not fitted universal limits.

One PI residual stream per each of30seeds,400rows each:12,000 selected saved readings. Residual is measured minus known simulated true state.

| Quantity | Saved-data result |
|---|---:|
| Mean signed error | −0.0002798957500694042 |
| Mean absolute error | 0.059835331096037614 |
| Largest absolute error | 0.13544550312245474 |
| Absolute signed mean ≤ .01 | yes |
| Readings with absolute error > .08 | 1,855 / 12,000 (15.4583%) |

Thus small signed average does not establish small individual errors; even MAE below .08 coexists with many pointwise exceedances. Neither the valid mean nor the stored source needs to be called false. The unsupported step would be promoting its mean result into a pointwise guarantee.

Seven controller variants reused the same sensor-noise stream per seed; measured-minus-true residuals agree to2.22e−16 across them. The archive has84,000 controller rows for this scenario but not84,000 independently generated sensor observations. We used12,000 selected rows from30 seeded streams. No claim that these are independent physical measurements. Future incomplete archives would need actual row-count checks rather than relying on configured controller counts.

[Results](RESULTS.json) retain per-seed statistics; [RESIDUALS.json](RESIDUALS.json) deposits the extracted streams for inspection/reanalysis. The original PID RESULTS.json is a large workspace-retained artifact, not part of that earlier GitHub deposit; its hash is pinned here. No original simulation rerun or new sensor measurement was performed.

The finite maximum is not a deterministic future bound. The mathematical Gaussian noise model does not supply bounded support; a real sensor also needs its own model/calibration evidence. We did not compute a confidence/tolerance interval from unjustified sampling assumptions. [NIST's official distinction](https://www.itl.nist.gov/div898/handbook/prc/section2/prc263.htm) separates confidence for parameters such as means, population coverage and engineering acceptability; see [source contact](SOURCE_CONTACT.md).

## 2. A usable reopening tool

[reopen_assessment.py](../../tools/reopen_assessment.py) takes the old contract, its saved receipt and a proposed contract. It checks declared historical binding, classifies explicit changes, optionally checks proposed live artifact bytes and current checker source identity, and suggests the next action. It never rewrites a historical verdict or issues a new domain verdict.

Recorded change dimensions include question/criterion parameters, assertion, scope, claim identity, evidence hash/location, checker revision and unclassified metadata. Live evidence/method binding is required before suggesting reuse. Canonical formatting-only changes do not change contract identity. A changed description is not automatically changed scientific evidence.

On actual MS-L1-style Q7 data100.040±.001, old tolerance.1 yields supported and new tolerance.01 yields contradicted. Same evidence and computed interval, different criterion. Both are correct scoped assessments; this is not discovery that old support was false. The [working example](reopening/reopening_plan.json) selects a new scoped assessment and preserves old support. The append-only-by-normal-use [history example](reopening/history.jsonl) retains both receipts and the original prefix.

From a checkout, in the current POSIX/Python workspace:

```bash
python FRR/tools/reopen_assessment.py FRR/evaluation/practice-growth-v1/reopening/old_contract.json FRR/evaluation/practice-growth-v1/reopening/old_receipt.json FRR/evaluation/practice-growth-v1/reopening/proposed_contract.json --root FRR/evaluation/practice-growth-v1
```

This helper classifies explicit recorded fields, not semantic equivalence or source reliability. Matching hashes do not authenticate a receipt or prove execution. Reuse preserves the old receipt's stated method/ruleset; it is not an implicit upgrade to another checker configuration. Hidden changes outside supplied records are not discovered. The underlying verifier remains unchanged; its old source/repair history remains intact.

## 3. Peer review found what the first checks missed

Eleven initial checks passed, covering changed criteria/assertions, formatting/notes, wrong/missing historical binding, missing live checking, checker changes and changed evidence bytes. Initial outputs and extracted data were preserved at [bb6b3345](https://github.com/bruhman680/CERTX/commit/bb6b33456525d04d053c64bcde6e0d6ab1f289f7) before repair.

A colleague then reproduced an absent-versus-null bug: adding expected_value:null to the sensor contract left the classified changes empty due to Python .get() equality, so the helper suggested reuse although exact contract hashes differed. This was not a demonstrated false sensor verdict, but it violated exact-contract reuse. Numeric metadata1 versus boolean true exposes a related equality collapse.

[Amendment 01](AMENDMENT_01.md) records the miss. Direct reuse now requires identical canonical contract hashes. Unclassified hash differences require review/new binding. Repaired source/driver were frozen at [8f5eeee5](https://github.com/bruhman680/CERTX/commit/8f5eeee55c6d2ec04c03486737e6fbd8689e7604) before expanded execution.

[Repair results](REPAIR_RESULTS.json): all11 original behavior cases replayed in temporary copies, both new equality controls passed, CLI produced the intended reopening plan, and all12 initial output files remained byte-identical. Original launch manifest now intentionally differs at the reopening-helper source; its earlier unchanged-at-run receipt is historical. The separate repair manifest identifies current code. Sensor-audit outputs were not retuned or rerun.

This is a concrete useful practice: execute, allow a different perspective to challenge the result, reproduce the miss, repair the relevant mechanism, and preserve both versions. It is not a claim that a six-agent collective guarantees correctness.

## 4. Better continuation without erasing the palimpsest

The current handoff had accumulated11,611bytes of repeated latest-checkpoint paragraphs and old episode limits. We preserved it exactly at [HANDOFF_BEFORE_PRACTICE_GROWTH.md](../../sync/checkpoints/HANDOFF_BEFORE_PRACTICE_GROWTH.md), with [hash receipt](HANDOFF_ARCHIVE_RECEIPT.json), before replacing the current view with a concise orientation.

The new view names the user's growth goal, useful working artifacts and current next moves. Earlier45%-window/stopping notes remain historical rather than silently controlling the user's newly authorized run. This does not implement automatic context loading or prove the shorter handoff improves an agent. It is a concrete navigation repair consistent with preserving old tracks while making the current path readable.

## What we retain

- Ask what kind of claim a statistic supports before strengthening confidence.
- Count distinct generating streams, not repeated representations.
- Ask what changed before calling a revised verdict an earlier error.
- Use disagreement/review as a source of testable noticings, then act on them.
- Preserve historical evidence while keeping current orientation concise.
- State why the next action is warranted; unresolved nonconsequential detail need not block useful work.

These are optional habits already related to FRR, strengthened through actual use. [Platt and Russell source notes](SOURCE_CONTACT.md) motivate discriminating inquiry and proportionate stopping, without adopting universal rhetoric or inventing calibrated information-gain scores. There is no newly validated universal reasoning algorithm, and no need to win a benchmark for this work to be useful.

Scoped closure: the saved-data questions are answered, a working command is available, the peer-found bug is repaired, and the initial history is preserved. Remaining leads—current read-only health command, semantic revision-link validation, actual source-reliability estimation and harder memory tasks—are retained as options, not automatically launched to manufacture more progress. Core FRR prompts/schema remain unchanged.
