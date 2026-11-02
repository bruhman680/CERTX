# Candidate compatibility control

2 November 2026. Paired CPU NumPy toy; no model inference or training.

The candidate-set rule repairs the known-DIFF failure in this run, while revealing substantial withholding and continued outside-world errors at small M. It does not establish general novelty detection or causal identification.

At M=1600, original F_care makes a wrong descriptive claim on DIFF in **728/1000** runs; candidate compatibility makes **0/1000**, returns the correct descriptive DIFF in **988/1000**, and UNKNOWN in **12/1000**. The exact known-DIFF noisy correlation is **324/1771**, below F_care’s .25 cutoff; its conditional agreement **853/2300** stays below the .6 shared-signature override. Thus the original guard asymptotically calls this known DIFF world IND. Vocabulary closure alone cannot explain that failure.

## Design and scope

[PROTOCOL.md](PROTOCOL.md), code and source hashes were saved in [INPUT_PINS.json](INPUT_PINS.json) before execution. These are local within-run receipts, not external preregistration. The protocol follows earlier source inspection and is not discovery-independent. The runner reuses the reviewed original generator, original seven features, and F_care definitions; it is not an independent implementation. Only the inspected AST prefix preceding source experiments executes. The source file remains unchanged.

Fit and calibration each use 800 runs per descriptive class IND, DIFF, SHARED, with separate seed streams; evaluation uses another stream and the same 1,000 observed A/B runs for each compared rule. Mean squared standardized feature distances and empirical .99 per-class thresholds follow the source. Empty compatibility sets return UNKNOWN, multiple candidates return UNRESOLVED, and singletons return their descriptive class. COMMON and UPSTREAM both have descriptive truth SHARED. F_care COMMON/COPY outputs are mapped to SHARED for scoring, with original labels preserved. These labels do not identify a causal route.

## All cells

Fractions below use 1,000 evaluations per cell. On authored outside worlds, any familiar specific claim counts as wrong-specific; this is the supplied category scoring convention, not proof of an unsupported claim in every possible interpretation. UNKNOWN and UNRESOLVED remain separate.

| M | World | Care wrong-specific | Set wrong-specific | Set UNKNOWN | Set UNRESOLVED |
|---:|---|---:|---:|---:|---:|
| 100 | IND | 0.032 | 0.015 | 0.004 | 0.898 |
| 100 | DIFF | 0.097 | 0.003 | 0.000 | 0.758 |
| 100 | COMMON | 0.036 | 0.007 | 0.007 | 0.007 |
| 100 | UPSTREAM | 0.030 | 0.005 | 0.002 | 0.008 |
| 100 | ANTI | 0.991 | 0.602 | 0.104 | 0.294 |
| 100 | LAG | 0.724 | 0.001 | 0.999 | 0.000 |
| 100 | DRIFT | 0.628 | 0.183 | 0.050 | 0.767 |
| 100 | PARTIAL | 0.925 | 0.731 | 0.031 | 0.238 |
| 100 | SWAP | 0.933 | 0.750 | 0.054 | 0.196 |
| 400 | IND | 0.001 | 0.003 | 0.002 | 0.277 |
| 400 | DIFF | 0.293 | 0.004 | 0.007 | 0.223 |
| 400 | COMMON | 0.000 | 0.000 | 0.010 | 0.000 |
| 400 | UPSTREAM | 0.000 | 0.000 | 0.020 | 0.000 |
| 400 | ANTI | 1.000 | 0.114 | 0.886 | 0.000 |
| 400 | LAG | 1.000 | 0.000 | 1.000 | 0.000 |
| 400 | DRIFT | 1.000 | 0.180 | 0.812 | 0.008 |
| 400 | PARTIAL | 1.000 | 0.275 | 0.725 | 0.000 |
| 400 | SWAP | 1.000 | 0.127 | 0.873 | 0.000 |
| 1600 | IND | 0.000 | 0.000 | 0.010 | 0.000 |
| 1600 | DIFF | 0.728 | 0.000 | 0.012 | 0.000 |
| 1600 | COMMON | 0.000 | 0.000 | 0.009 | 0.000 |
| 1600 | UPSTREAM | 0.000 | 0.000 | 0.008 | 0.000 |
| 1600 | ANTI | 1.000 | 0.000 | 1.000 | 0.000 |
| 1600 | LAG | 1.000 | 0.000 | 1.000 | 0.000 |
| 1600 | DRIFT | 1.000 | 0.000 | 1.000 | 0.000 |
| 1600 | PARTIAL | 1.000 | 0.000 | 1.000 | 0.000 |
| 1600 | SWAP | 1.000 | 0.000 | 1.000 | 0.000 |

## Predictions, costs and failures

All four numerical/directional prospective checks passed: increasing original DIFF error, low/lower candidate-set DIFF error at M=1600, exposed multi-candidate evaluations at M=100, and increasing SWAP UNKNOWN from M=400 to M=1600. The protocol’s COMMON/UPSTREAM equivalence statement is analytic, not a statistical equivalence test.

Passing these checks leaves important failures. At M=100, the set rule still makes specific familiar claims on ANTI (.602), PARTIAL (.731), and SWAP (.750). It withholds as UNRESOLVED on .898 of IND and .758 of DIFF, giving correct-specific rates only .083 and .239 respectively. The original and set rules do not operate at matched acceptance rates or costs. At M=400 known IND wrong-specific is .003 for the set rule versus .001 for original care: there is no uniform observed dominance.

SWAP UNKNOWN is .873 at M=400 and 1.000 at M=1600. This control fits only three descriptive candidates; its UNKNOWN rate must not be compared directly with the seven-class source recognizer, which includes PARTIAL and therefore accepts many SWAP runs there. Both candidate vocabulary and the selection rule changed relative to that seven-class experiment.

## Limits and artifacts

Separate fit/calibration/evaluation streams prevent direct reuse of evaluation samples for fitting; they do not make the authored class/world choices independent, eliminate post-source design choices, or validate an empirical band as a coverage guarantee. Only one calibration per M and a single .99 quantile were tested. Calibration-seed, threshold, distance-metric and feature sensitivity remain unmeasured. No nearest-class selector arm was run on these exact same fitted bands; comparisons to original care combine changed decision geometry with exposed compatibility sets.

The original care rule includes world-conditioned oracle probes, although mapping to SHARED removes the claimed route distinction from descriptive scoring. There are no implemented interventions or shams. The complete experiment concerns authored worlds with known symmetric flag noise .05; no feature discovery, learner, real-agent efficacy, causal-source localization or arbitrary-OOD guarantee is tested. Finite 0/1000 counts are not zero population-error guarantees.

[SUMMARY.json](SUMMARY.json) contains all cell rates and paired wrong-specific contingency counts. [PARAMETERS.json](PARAMETERS.json) saves complete fitted arrays, thresholds, seed spawn keys and observed-input SHA-256 hashes. [EVALUATIONS_COMPACT.json](EVALUATIONS_COMPACT.json) is the 735 KB publication artifact: per-cell arrays of all evaluation labels, minimum normalized distance and candidate bit mask (IND=1, DIFF=2, SHARED=4), plus exact-input and local NPZ SHA-256 hashes. The verbose local [evaluations.jsonl](evaluations.jsonl) (4.41 MB) preserves the same 27,000 evaluation records. [evaluations.npz](evaluations.npz) retains full observed boolean A/B inputs, seven features, all normalized class distances, masks and labels. Persisted inputs avoid relying on cross-version NumPy regeneration.

[run_control.py](run_control.py) reproduces the run. [VALIDATION.json](VALIDATION.json) records exact-fraction assertions, all 27 input hashes, all summary label counts, agreement of every JSONL row with NPZ, unchanged pinned source/code/protocol hashes, and empty stderr. [RUN_STDOUT.json](RUN_STDOUT.json) and [RUN_STDERR.txt](RUN_STDERR.txt) retain execution output. Run with `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python run_control.py`, then `python export_compact.py` for the publication export. The local full NPZ is 7.03 MB.
