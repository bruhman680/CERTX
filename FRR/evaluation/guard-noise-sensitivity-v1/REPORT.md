# Noise-sensitive guards: the measurement model is part of the soil

2 November 2026, client date. CPU NumPy toy; no model inference or training. Source generator/features reused, two independently seeded calibrations, not an independent reconstruction of the whole design.

## Main finding

The candidate guard is calibrated to flag-flip noise .05. At M=1600 and empirical .99 bands, the known shared-error world remains compatible in .982/.986 of matched-noise runs across the two calibrations. Changing only flag noise to .025 **or** .10 makes that same underlying shared process return UNKNOWN on all500 sampled runs in each of the four cells. Cleaner observation as well as noisier observation can trigger rejection of a model fitted to a fixed noise level.

These alarms do not establish a new underlying error mechanism. The guard measures compatibility with a combination of a latent pattern and an assumed observation channel. A changed observation channel can look like a changed world.

## Design

Two frozen calibration seeds; M400/1600; three descriptive candidates IND, DIFF, SHARED;800fit and800calibration samples per class. Training noise always .05. Empirical .95/.99 quantiles use the same fitted/calibration samples.500evaluation runs per known world at noise .025/.05/.10. All noise levels share the same latent sequence and nested flip sets via reset evaluation seeds; the audit verifies this coupling. No probes, shams, causal route labels, or external datasets.

There are18,000noise-evaluation records, scored under two thresholds for36,000threshold evaluations in72cells. These are paired and reused observations, not36,000independent worlds. Complete cell results remain below and in SUMMARY.json; no threshold is selected as a new default.

## Shared-world mechanism

For latent error probability p=.2 and independent symmetric flag flips epsilon, observed marginal q=epsilon+(1-2epsilon)*p and observed shared correlation is

`phi = (1-2epsilon)^2 * p*(1-p) / (q*(1-q))`.

- epsilon=0.025: q=0.215, shared phi=0.855577.
- epsilon=0.050: q=0.230, shared phi=0.731790.
- epsilon=0.100: q=0.260, shared phi=0.532225.

The latent shared relation stays fixed, while the measured signature moves. Narrower high-M bands can make the channel mismatch more evident. This is rejection of the assumed observation model, not evidence that less noisy sensing intrinsically harms knowledge.

## All .99-band cells

Each row has500evaluation runs. Compatibility of the true class is distinct from a unique correct label. UNRESOLVED retains multiple candidates; UNKNOWN rejects all candidates.

| Seed | M | World | Noise | True class compatible | Correct singleton | Wrong singleton | UNKNOWN | UNRESOLVED |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| 2026110301 | 400 | IND | 0.025 | 0.982 | 0.766 | 0.008 | 0.010 | 0.216 |
| 2026110301 | 400 | IND | 0.050 | 0.986 | 0.680 | 0.008 | 0.006 | 0.306 |
| 2026110301 | 400 | IND | 0.100 | 0.980 | 0.542 | 0.016 | 0.004 | 0.438 |
| 2026110301 | 400 | DIFF | 0.025 | 0.990 | 0.860 | 0.002 | 0.008 | 0.130 |
| 2026110301 | 400 | DIFF | 0.050 | 0.994 | 0.774 | 0.004 | 0.002 | 0.220 |
| 2026110301 | 400 | DIFF | 0.100 | 0.988 | 0.626 | 0.012 | 0.000 | 0.362 |
| 2026110301 | 400 | COMMON | 0.025 | 0.506 | 0.506 | 0.000 | 0.494 | 0.000 |
| 2026110301 | 400 | COMMON | 0.050 | 0.988 | 0.988 | 0.000 | 0.012 | 0.000 |
| 2026110301 | 400 | COMMON | 0.100 | 0.090 | 0.090 | 0.000 | 0.910 | 0.000 |
| 2026110301 | 1600 | IND | 0.025 | 0.986 | 0.986 | 0.000 | 0.014 | 0.000 |
| 2026110301 | 1600 | IND | 0.050 | 0.982 | 0.982 | 0.000 | 0.018 | 0.000 |
| 2026110301 | 1600 | IND | 0.100 | 0.944 | 0.944 | 0.000 | 0.056 | 0.000 |
| 2026110301 | 1600 | DIFF | 0.025 | 0.956 | 0.956 | 0.000 | 0.044 | 0.000 |
| 2026110301 | 1600 | DIFF | 0.050 | 0.996 | 0.996 | 0.000 | 0.004 | 0.000 |
| 2026110301 | 1600 | DIFF | 0.100 | 0.968 | 0.968 | 0.000 | 0.032 | 0.000 |
| 2026110301 | 1600 | COMMON | 0.025 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| 2026110301 | 1600 | COMMON | 0.050 | 0.982 | 0.982 | 0.000 | 0.018 | 0.000 |
| 2026110301 | 1600 | COMMON | 0.100 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| 2026110302 | 400 | IND | 0.025 | 0.988 | 0.756 | 0.002 | 0.010 | 0.232 |
| 2026110302 | 400 | IND | 0.050 | 0.984 | 0.710 | 0.008 | 0.008 | 0.274 |
| 2026110302 | 400 | IND | 0.100 | 0.972 | 0.530 | 0.022 | 0.006 | 0.442 |
| 2026110302 | 400 | DIFF | 0.025 | 0.994 | 0.884 | 0.000 | 0.006 | 0.110 |
| 2026110302 | 400 | DIFF | 0.050 | 0.998 | 0.844 | 0.002 | 0.000 | 0.154 |
| 2026110302 | 400 | DIFF | 0.100 | 0.994 | 0.690 | 0.006 | 0.000 | 0.304 |
| 2026110302 | 400 | COMMON | 0.025 | 0.540 | 0.540 | 0.000 | 0.460 | 0.000 |
| 2026110302 | 400 | COMMON | 0.050 | 0.992 | 0.992 | 0.000 | 0.008 | 0.000 |
| 2026110302 | 400 | COMMON | 0.100 | 0.086 | 0.086 | 0.000 | 0.914 | 0.000 |
| 2026110302 | 1600 | IND | 0.025 | 0.994 | 0.994 | 0.000 | 0.006 | 0.000 |
| 2026110302 | 1600 | IND | 0.050 | 0.998 | 0.998 | 0.000 | 0.002 | 0.000 |
| 2026110302 | 1600 | IND | 0.100 | 0.950 | 0.950 | 0.000 | 0.050 | 0.000 |
| 2026110302 | 1600 | DIFF | 0.025 | 0.964 | 0.964 | 0.000 | 0.036 | 0.000 |
| 2026110302 | 1600 | DIFF | 0.050 | 0.988 | 0.988 | 0.000 | 0.012 | 0.000 |
| 2026110302 | 1600 | DIFF | 0.100 | 0.940 | 0.940 | 0.004 | 0.056 | 0.000 |
| 2026110302 | 1600 | COMMON | 0.025 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| 2026110302 | 1600 | COMMON | 0.050 | 0.986 | 0.986 | 0.000 | 0.014 | 0.000 |
| 2026110302 | 1600 | COMMON | 0.100 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |

## Checks, limitations and next contact

[FREEZE.json](FREEZE.json) pins source/code/protocol before new samples. [PARAMETERS.json](PARAMETERS.json) retains fitted means/scales/quantiles. [AUDIT.json](AUDIT.json) independently reconstructs all36,000mask/label/rate decisions, regenerates36observed-input hashes in the recorded NumPy runtime, and checks nested flip sets for all12latent cell groups. Generation stderr and audit stderr are empty. Calibration targets are empirical, not coverage guarantees; matched-noise acceptance itself varies across seeds/classes.

[PUBLICATION_COMPACT.json](PUBLICATION_COMPACT.json) preserves every label, candidate mask, all three normalized distances, seed and input hash. It is a lossless minified representation of the larger local RAW_COMPACT.json; [PUBLICATION.json](PUBLICATION.json) verifies exact reconstruction of its original bytes with the specified Python formatting. Full A/B arrays are not stored in either file; source+seeds+input hashes support regeneration checks, not an independent input backup or cross-version guarantee.

Only two calibration seeds, two quantiles, two sample sizes and one symmetric-noise family were tested. Results do not cover biased, correlated or state-dependent sensing errors, arbitrary unknown worlds, or real agents. More data does not inevitably worsen detection; here it sharpens a specifically misspecified known-noise model. No general gate/controller is adopted.

Practical refinement: every UNKNOWN report should state the assumed measurement channel and plausible calibration mismatch. Keep 'observation model rejected' separate from 'new causal mechanism discovered.' The prior Claude relay's estimated-noise gold-set costs are directly relevant, but are not replicated by this experiment.

Next, prospectively compare joint candidate sets over both descriptive class and a noise range, with independent gold-label calibration observations. Measure how allowing unknown noise increases ambiguity; do not repair every alarm simply by widening bands. Actual intervention and sham-source localization remain separate unexecuted work.
