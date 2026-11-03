# Cycle2 — joint class/noise candidates restore compatibility, with costs

2 November2026. CPU source-pipeline toy, no model calls. Two fit/calibration seeds and M400/1600; classes IND,DIFF,SHARED x noise .025/.05/.10. Independent800fit/800calibration samples per pair, empirical.99bands.300observations per36input cells,10,800observations evaluated under5paired arms =54,000arm decisions. These are reused paired records, not54,000independent observations.

At M1600, fixed-.05 rejection of off-assumption shared cases is repaired by the joint union: correct singleton rates .9767–.9967 across both seeds and the three grid noises. Gold filtering narrows ambiguity, but can exclude the true noise and introduce additional UNKNOWN. It does not uniformly improve correctness. At M400, mean UNRESOLVED over all known world/noise cells falls from .2426 for union to .1867 withG400gold; mean wrong-singleton rises .00222 -> .00444. Coverage/specificity costs must accompany error rates.

Gold counts are independent planted Bernoulli calibration information, G40 and nestedG400; Wilson1.96approximate intervals intersect the grid. This is a controlled additional information budget, not free external calibration or model self-discovery. Oracle arm knows the true noise and is privileged. Grid-aligned evaluation only; no arbitrary noise/unknown-world guarantee.

## Shared-world M1600 detail

Each row has300paired observations. All other classes/sample sizes, true-pair compatibility, ambiguity and wrong-label rates are in SUMMARY.json.

| Seed | Noise | Arm | Correct singleton | UNKNOWN | Calibration grid empty |
|---|---:|---|---:|---:|---:|
| 2026110311 | 0.0250 | fixed | 0.0000 | 1.0000 | 0.0000 |
| 2026110311 | 0.0250 | union | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0250 | oracle | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0250 | gold40 | 0.9100 | 0.0900 | 0.0000 |
| 2026110311 | 0.0250 | gold400 | 0.9633 | 0.0367 | 0.0067 |
| 2026110311 | 0.0500 | fixed | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0500 | union | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0500 | oracle | 0.9933 | 0.0067 | 0.0000 |
| 2026110311 | 0.0500 | gold40 | 0.9633 | 0.0367 | 0.0000 |
| 2026110311 | 0.0500 | gold400 | 0.9500 | 0.0500 | 0.0000 |
| 2026110311 | 0.1000 | fixed | 0.0000 | 1.0000 | 0.0000 |
| 2026110311 | 0.1000 | union | 0.9767 | 0.0233 | 0.0000 |
| 2026110311 | 0.1000 | oracle | 0.9767 | 0.0233 | 0.0000 |
| 2026110311 | 0.1000 | gold40 | 0.9167 | 0.0833 | 0.0533 |
| 2026110311 | 0.1000 | gold400 | 0.9100 | 0.0900 | 0.0367 |
| 2026110312 | 0.0250 | fixed | 0.0000 | 1.0000 | 0.0000 |
| 2026110312 | 0.0250 | union | 0.9900 | 0.0100 | 0.0000 |
| 2026110312 | 0.0250 | oracle | 0.9900 | 0.0100 | 0.0000 |
| 2026110312 | 0.0250 | gold40 | 0.9233 | 0.0767 | 0.0000 |
| 2026110312 | 0.0250 | gold400 | 0.9633 | 0.0367 | 0.0033 |
| 2026110312 | 0.0500 | fixed | 0.9967 | 0.0033 | 0.0000 |
| 2026110312 | 0.0500 | union | 0.9967 | 0.0033 | 0.0000 |
| 2026110312 | 0.0500 | oracle | 0.9967 | 0.0033 | 0.0000 |
| 2026110312 | 0.0500 | gold40 | 0.9567 | 0.0433 | 0.0033 |
| 2026110312 | 0.0500 | gold400 | 0.9500 | 0.0500 | 0.0000 |
| 2026110312 | 0.1000 | fixed | 0.0000 | 1.0000 | 0.0000 |
| 2026110312 | 0.1000 | union | 0.9967 | 0.0033 | 0.0000 |
| 2026110312 | 0.1000 | oracle | 0.9967 | 0.0033 | 0.0000 |
| 2026110312 | 0.1000 | gold40 | 0.9600 | 0.0400 | 0.0300 |
| 2026110312 | 0.1000 | gold400 | 0.9467 | 0.0533 | 0.0233 |

## Receipts and limits

PROTOCOL.md and FREEZE.json retain prospective design/source/code dependencies. PARAMETERS.json retains complete means/scales/thresholds. RAW.json preserves pair masks, per-arm class/noise masks and labels, gold counts, input hashes and regeneration seeds. AUDIT.json reconstructs54,000arm decisions, recalculates independent gold interval formulas and every summary metric, regenerates all36input hashes, and recomputes task pair masks from saved parameters. Cycle3 also checks exact preservation of parent coarse parameter values. No raw input backup or cross-version regeneration guarantee is claimed. Gold observations are simulated binomial counts; no paid tools/data or actual thousands of tool calls occurred.

These empirical bands/approximate intervals have no exact general coverage guarantee. Accepted singleton classes describe compatibility within supplied candidates, not causal route truth. Gold filtering can turn a correct broad union into UNKNOWN by excluding true settings. Noise families are authored symmetric independent flag flips; correlated/bias/drift channels, unknown task classes, interventions and shams remain untested. More candidate settings may increase class ambiguity. No general guard/default/teacher is adopted.
