# Cycle1: finite noisy calibration and attribution

The [protocol](PROTOCOL.md) was saved before executing [run.py](run.py). This contact draws Bernoulli main outcomes from SR-C1's actual forced0/forced1 post-reset probabilities, with perfect-readout synthetic coordinate-survival witnesses. It is a new noisy study of the stipulated additive model, not validation of physical/agent resets. Four worlds, two designs, three sample budgets and200 replicates per world/design/budget yield4,800 stochastic groups and14,400 mode-assessments. The initial run took0.735seconds; no parameters or thresholds were retuned.

Each design has3 arms and uses6n outcome plus6n witness draws per replicate:12n total, including sham witness draws. Diverse arms are sham, agent-target(.8,.1), soil-target(.1,.8). Redundant arms are sham and two repetitions of the same shared(.6,.6) operator. Its repeated-arm witness estimates are pooled. Pooling alone does not prevent sampled coordinate differences from producing empirical rank2; the explicit structurally redundant design refusal prevents generic allocation. Different preparation/hardware costs are not modeled.

## Results

| Design and calibration | n/group | Fixed-candidate singleton fraction | Mean candidate count | Continuous interval mean width, a and b |
|---|---:|---:|---:|---|
|diverse, known|100|0|4.000|1.223,1.223|
|diverse, estimated|100|0|4.000|1.593,1.595|
|diverse, known|1000|0.00375|3.519|.387,.387|
|diverse, estimated|1000|0.00375|3.546|.503,.503|
|diverse, known|10000|1|1.000|.122,.122|
|diverse, estimated|10000|1|1.000|.159,.159|
|redundant, known or estimated|10000|.5|1.500|no generic allocation|

All true fixed candidates were retained and all constructed continuous intervals covered truth in these saved replicates. No positive-contribution false positives occurred under the conservative interval rule. These are observed frequencies, not evidence of100% general coverage or optimal efficiency. Hoeffding bounds were deliberately conservative; finite intervals are broad at low budgets. A null rejection is not proof the underlying contribution is absent.

The n10000 diverse design separates all four fixed contribution candidates here, although its estimated-calibration continuous interval width remains about.159. There is no contradiction: eliminating three fixed points is much easier than precisely locating an arbitrary continuous pair. Redundant design can discriminate some fixed candidates while remaining rank1 for generic allocation. In particular its .5 singleton fraction does not show that a second measurement direction appeared.

Absent calibration returns all labels and no continuous estimate. This is a deliberately conservative **unassessed candidate policy**, not a calculation proving all labels have identical observation laws. Absolute outcome baselines and the fully known family may contain additional discriminatory information; this procedure uses first-outcome contrasts only.

## Uncertainty contract

The same95% simultaneous Hoeffding radius over12 group means is used for known and estimated modes. Estimated-calibration candidate acceptance expands predicted contrast intervals using coefficient intervals; continuous bounds additionally use |a|<=.2, |b|<=.4. Calibration noise and outcome noise are independent by construction. The witness identifies survival only because its nonzero preparation, perfect readout, and reset-to-zero semantics are stipulated. No hidden gates, wrong witnesses, unknown target states, or witness backaction are included.

## Evidence and checks

[RESULTS.json.gz](RESULTS.json.gz) saves every mode-assessment; [SUMMARY.json](SUMMARY.json) is the compact summary. [DRAW_LEDGER.jsonl.gz](DRAW_LEDGER.jsonl.gz) exposes actual per-arm forced-group probabilities, same-reset no-probe baseline probabilities, sampled event counts, and witness survival counts. [check_draws.py](check_draws.py) deterministically replays the original PCG64 seed and matches all contrasts/witness values exactly. This is a bookkeeping replay of the same random stream, not an independent statistical replication. [CHECKS.json](CHECKS.json) binds the source and records the checks. Gzip files preserve the raw artifacts' exact bytes for transport; they do not replace the originals.

The raw outcomes and absolute group probabilities were added as a supplemental ledger after the first run because initial result rows stored contrasts/witnesses only. The frozen protocol and initial RESULTS.json were not changed; the supplemental replay used exactly the same source and seed. No selected trials, failures or false-positive outcomes were omitted. Empty stderr is preserved.

## Next decision

Cycle2 can investigate how an apparently valid witness can lose the same read access as the main observer, or how interaction misspecification survives naive calibration. The strongest present gap is not another precision tweak: the witness semantics are assumed. Keep model-checking/unknown calibration separate from inference within the correctly specified family. Do not promote generic carrier identification, real-agent benefit or broad queue completion from this contact.

## Post-run estimator edge

All2,400 estimated diverse matrices in the saved datasets had rank2; maximum condition number is recorded in [RANK_DIAGNOSTIC.json](RANK_DIAGNOSTIC.json). The original code nonetheless lacks a rank guard for a hypothetical singular estimated diverse matrix and would emit a pseudoinverse allocation there. No such event occurred in this run. The original source/results remain unchanged; a later cycle will exercise and repair this edge separately. Raw `point_identified` means a fixed-candidate singleton, not continuous point identification. The three calibration modes are offline views of the same4,800 datasets, not14,400 independent trials.

## Transport and execution accounting

Local originals remain unchanged. GitHub publication can retain their exact gzip archives; restore local inputs before running the draw check:

```bash
gzip -dk RESULTS.json.gz DRAW_LEDGER.jsonl.gz
python check_draws.py
```

Do not decompress over an existing original without first comparing hashes. The manifest binds compressed and original bytes; archive restoration is not another experiment. One stochastic analysis run and one deterministic draw replay were executed, plus diagnostic/packaging commands. There were no execution failures, retries, discarded stochastic trials, provider calls or hidden agent participants in Cycle1.

A correction to the frozen protocol's intended pooling rationale: repeated-arm pooling removes differences between duplicate arms, but does not enforce equality of independently sampled agent/soil rates. The redundant estimated matrices actually had rank2 in2,338 of2,400 cases, despite the true measurement design having rank1. The implementation's explicit design-based refusal, not numerical rank/pooling, protected continuous attribution. This is a useful observed example of calibration noise fabricating apparent measurement directions. Protocol and original results are preserved rather than rewritten.
