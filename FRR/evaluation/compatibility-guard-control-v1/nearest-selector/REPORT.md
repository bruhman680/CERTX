# Nearest-selector comparison: post hoc

This analysis reuses the existing 27,000 evaluation runs and their three class-normalized distances. It draws no new samples and performs no model calls. It was requested after inspecting the frozen control results; it is explicitly post hoc. The parent protocol, runner and output artifacts remain untouched.

The nearest rule returns UNKNOWN when every normalized distance exceeds one; otherwise it selects the lowest normalized-distance candidate. Compatibility uses the identical fitted bands and distances, but withholds as UNRESOLVED when more than one candidate is accepted. Thus every difference between these two arms is precisely one of those multiple-candidate cases. This selector rule minimizes distance divided by its class threshold, matching the source’s normalized selection convention.

## All cells

Rates use 1,000 evaluations per cell. For outside worlds any familiar specific claim is scored wrong under the parent authored-category convention; COMMON and UPSTREAM are descriptively SHARED.

| M | World | Multiple count | Nearest wrong | Set wrong | Nearest correct | Set correct | Shared UNKNOWN |
|---:|---|---:|---:|---:|---:|---:|---:|
| 100 | IND | 898 | 0.233 | 0.015 | 0.763 | 0.083 | 0.004 |
| 100 | DIFF | 758 | 0.165 | 0.003 | 0.835 | 0.239 | 0.000 |
| 100 | COMMON | 7 | 0.010 | 0.007 | 0.983 | 0.979 | 0.007 |
| 100 | UPSTREAM | 8 | 0.009 | 0.005 | 0.989 | 0.985 | 0.002 |
| 100 | ANTI | 294 | 0.896 | 0.602 | — | — | 0.104 |
| 100 | LAG | 0 | 0.001 | 0.001 | — | — | 0.999 |
| 100 | DRIFT | 767 | 0.950 | 0.183 | — | — | 0.050 |
| 100 | PARTIAL | 238 | 0.969 | 0.731 | — | — | 0.031 |
| 100 | SWAP | 196 | 0.946 | 0.750 | — | — | 0.054 |
| 400 | IND | 277 | 0.045 | 0.003 | 0.953 | 0.718 | 0.002 |
| 400 | DIFF | 223 | 0.053 | 0.004 | 0.940 | 0.766 | 0.007 |
| 400 | COMMON | 0 | 0.000 | 0.000 | 0.990 | 0.990 | 0.010 |
| 400 | UPSTREAM | 0 | 0.000 | 0.000 | 0.980 | 0.980 | 0.020 |
| 400 | ANTI | 0 | 0.114 | 0.114 | — | — | 0.886 |
| 400 | LAG | 0 | 0.000 | 0.000 | — | — | 1.000 |
| 400 | DRIFT | 8 | 0.188 | 0.180 | — | — | 0.812 |
| 400 | PARTIAL | 0 | 0.275 | 0.275 | — | — | 0.725 |
| 400 | SWAP | 0 | 0.127 | 0.127 | — | — | 0.873 |
| 1600 | IND | 0 | 0.000 | 0.000 | 0.990 | 0.990 | 0.010 |
| 1600 | DIFF | 0 | 0.000 | 0.000 | 0.988 | 0.988 | 0.012 |
| 1600 | COMMON | 0 | 0.000 | 0.000 | 0.991 | 0.991 | 0.009 |
| 1600 | UPSTREAM | 0 | 0.000 | 0.000 | 0.992 | 0.992 | 0.008 |
| 1600 | ANTI | 0 | 0.000 | 0.000 | — | — | 1.000 |
| 1600 | LAG | 0 | 0.000 | 0.000 | — | — | 1.000 |
| 1600 | DRIFT | 0 | 0.000 | 0.000 | — | — | 1.000 |
| 1600 | PARTIAL | 0 | 0.000 | 0.000 | — | — | 1.000 |
| 1600 | SWAP | 0 | 0.000 | 0.000 | — | — | 1.000 |

## Interpretation and limits

At M=1600 every world has zero multiple-candidate cases. On known DIFF both selectors make zero wrong-specific claims, return correct DIFF .988, and UNKNOWN .012. Original F_care made wrong-specific claims .728 on these same runs. The DIFF repair at this M therefore comes from replacing the original decision geometry with the calibrated feature-distance bands; it cannot be attributed to withholding multiple candidates. This does not isolate which component of that geometric replacement is responsible.

At smaller M withholding can remove both correct and wrong nearest selections. The per-cell correct rates quantify that cost. On the authored outside worlds, every withheld familiar label mechanically reduces the wrong-specific rate, so that reduction alone does not validate useful recognition. Neither selector identifies a causal route.

Specifically, M=100 IND nearest selects correctly .763 and wrongly .233; the set rule retains correct .083 and wrong .015 while withholding .898. Those withheld cases include 680 correct and 218 wrong nearest selections. DIFF nearest correct/wrong is .835/.165, versus set .239/.003; withholding removes 596 correct and 162 wrong nearest selections. The calibrated nearest arm also has more wrong-specific claims than original F_care at M=100 on IND (.233 versus .032) and DIFF (.165 versus .097). Geometry replacement is therefore not a uniform improvement across sample sizes.

The analysis fixes the earlier fitted means, scales, empirical thresholds, seeds, worlds and feature choices. It isolates selector behavior conditional on those artifacts, not calibration-seed sensitivity, metric choice, independent scientific replication, coverage guarantees, or population performance. The two rules have identical UNKNOWN by construction; zero observed errors are not zero-risk guarantees.

[INPUTS.json](INPUTS.json) records the exact NPZ, parent summary and analysis-script hashes. [SUMMARY.json](SUMMARY.json) includes all cell rates and the nearest labels, correct counts and wrong counts among cases withheld by the set rule. The script asserts that changed labels equal precisely the multiple-candidate mask and that all UNKNOWN masks match. Run `python analyze.py` from this directory to reproduce.
