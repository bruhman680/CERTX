# Cycle3 — precise calibration exposes an incomplete noise grid

2 November2026. Chosen after cycle2 revealed benefits and false rejections from gold filtering. CPU toy, no model calls. Reuse all coarse fitted class/noise pairs byte-for-value, then add .0375/.075noise fits to form [.025,.0375,.05,.075,.10]. Fresh evaluation at .0375/.05/.075, same two calibration identities and M400/1600.36input cells x300observations,5paired arms =54,000decisions on10,800observations.

At M1600 and true shared-process noise .075, coarse union already returns UNKNOWN .7333/.7967 across seeds. Coarse gold filtering withG4000has an empty calibration grid on300/300runs for each seed, hence UNKNOWN1.0. Adding the missing true-noise candidate gives dense-union correct singleton .9933/.9867, or .9233/.9267 with gold filtering. Gold interval error still costs compatibility. At .0375 coarse gold grid emptiness is .9800/.9733, also mostly repaired by dense candidates.

This is an authored diagnostic repair: we add the exact noise values chosen for the test, not values a learner autonomously discovers. The matched .05control, both seeds/sample sizes, all classes and failed cases remain saved. A precise interval can accurately fall between candidates; rejecting its grid is not evidence of a new latent process. Sampling error, wrong gold assumptions and missing candidates remain distinct possibilities.

## Shared-world M1600 detail

Each row has300paired observations. All other classes/sample sizes, true-pair compatibility, ambiguity and wrong-label rates are in SUMMARY.json.

| Seed | Noise | Arm | Correct singleton | UNKNOWN | Calibration grid empty |
|---|---:|---|---:|---:|---:|
| 2026110311 | 0.0375 | coarse_union | 0.7300 | 0.2700 | 0.0000 |
| 2026110311 | 0.0375 | dense_union | 1.0000 | 0.0000 | 0.0000 |
| 2026110311 | 0.0375 | coarse_gold4000 | 0.0100 | 0.9900 | 0.9800 |
| 2026110311 | 0.0375 | dense_gold4000 | 0.9733 | 0.0267 | 0.0167 |
| 2026110311 | 0.0375 | oracle | 1.0000 | 0.0000 | 0.0000 |
| 2026110311 | 0.0500 | coarse_union | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0500 | dense_union | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0500 | coarse_gold4000 | 0.9533 | 0.0467 | 0.0400 |
| 2026110311 | 0.0500 | dense_gold4000 | 0.9667 | 0.0333 | 0.0167 |
| 2026110311 | 0.0500 | oracle | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0750 | coarse_union | 0.2667 | 0.7333 | 0.0000 |
| 2026110311 | 0.0750 | dense_union | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0750 | coarse_gold4000 | 0.0000 | 1.0000 | 1.0000 |
| 2026110311 | 0.0750 | dense_gold4000 | 0.9233 | 0.0767 | 0.0700 |
| 2026110311 | 0.0750 | oracle | 0.9933 | 0.0067 | 0.0000 |
| 2026110312 | 0.0375 | coarse_union | 0.7567 | 0.2433 | 0.0000 |
| 2026110312 | 0.0375 | dense_union | 1.0000 | 0.0000 | 0.0000 |
| 2026110312 | 0.0375 | coarse_gold4000 | 0.0167 | 0.9833 | 0.9733 |
| 2026110312 | 0.0375 | dense_gold4000 | 0.9767 | 0.0233 | 0.0067 |
| 2026110312 | 0.0375 | oracle | 0.9933 | 0.0067 | 0.0000 |
| 2026110312 | 0.0500 | coarse_union | 0.9867 | 0.0133 | 0.0000 |
| 2026110312 | 0.0500 | dense_union | 0.9900 | 0.0100 | 0.0000 |
| 2026110312 | 0.0500 | coarse_gold4000 | 0.9300 | 0.0700 | 0.0567 |
| 2026110312 | 0.0500 | dense_gold4000 | 0.9467 | 0.0533 | 0.0167 |
| 2026110312 | 0.0500 | oracle | 0.9867 | 0.0133 | 0.0000 |
| 2026110312 | 0.0750 | coarse_union | 0.2033 | 0.7967 | 0.0000 |
| 2026110312 | 0.0750 | dense_union | 0.9867 | 0.0133 | 0.0000 |
| 2026110312 | 0.0750 | coarse_gold4000 | 0.0000 | 1.0000 | 1.0000 |
| 2026110312 | 0.0750 | dense_gold4000 | 0.9267 | 0.0733 | 0.0500 |
| 2026110312 | 0.0750 | oracle | 0.9767 | 0.0233 | 0.0000 |

## Receipts and limits

PROTOCOL.md and FREEZE.json retain prospective design/source/code dependencies. PARAMETERS.json retains complete means/scales/thresholds. RAW.json preserves pair masks, per-arm class/noise masks and labels, gold counts, input hashes and regeneration seeds. AUDIT.json reconstructs54,000arm decisions, recalculates independent gold interval formulas and every summary metric, regenerates all36input hashes, and recomputes task pair masks from saved parameters. Cycle3 also checks exact preservation of parent coarse parameter values. No raw input backup or cross-version regeneration guarantee is claimed. Gold observations are simulated binomial counts; no paid tools/data or actual thousands of tool calls occurred.

These empirical bands/approximate intervals have no exact general coverage guarantee. Accepted singleton classes describe compatibility within supplied candidates, not causal route truth. Gold filtering can turn a correct broad union into UNKNOWN by excluding true settings. Noise families are authored symmetric independent flag flips; correlated/bias/drift channels, unknown task classes, interventions and shams remain untested. More candidate settings may increase class ambiguity. No general guard/default/teacher is adopted.

Next strongest: compare a noise-range/profile method with discrete-grid membership, using independently calibrated range information and untouched intermediate noises. Preserve finite-sample false rejection and ambiguity. Avoid automatically widening every band until it accepts. The additional receipt helper distinguishes CALIBRATION_GRID_EMPTY from NO_COMPATIBLE_PAIR, AMBIGUOUS_CLASSES and COMPATIBLE_CLASS; those are bookkeeping locations, not proven causal diagnoses.
