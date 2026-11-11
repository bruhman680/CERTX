# Adversarial rescue-policy audit — energy-conditioned gating is not a free lunch

**One substantive research loop, 156 simulation runs.** The question was whether the hand-coded `energy_rescue` rule's advantage is genuinely due to energy-conditioning, or merely to comparing it against an inferior fixed threshold or too-short horizon. Script `SOC_RESCUE_AUDIT_probe.py`; complete results `SOC_RESCUE_AUDIT_results.json`, containing original-source fingerprints, Python/NumPy versions, all 12 fresh matched seeds `36000..36011`, 16×16 world, 20,000 ticks, checkpoints, floor/ceiling occupancy and tail raw drift. Every arm uses **unchanged** v0.1 resource and energy physics. A separate 300-step direct equality check against `SOC_LONGITUDINAL_explore.PolicyFork` passed exactly for the reference rescue policy.

This is a **posthoc adversarial simulator test**, not independent preregistration or proof of indefinite viability. It contains 13 distinct policy arms ×12 seeds; those are **not 156 research loops**.

## Hypothesis and counterfactual design

Historical rescue policy: harvest when resource `R>.51`, except when energy `E<.12`, when harvest if `R>.485` (lower threshold by `.025`). It explicitly uses energy; the original fixed rule sees resource only.

There are two plausible opposite mechanisms:

1. **Immediate-payoff rescue:** When a cell is energy-depleted, harvesting earlier earns energy instead of resting, at the risk of depleting future resources.
2. **Conservation rescue:** When depleted, harvest *less* often to give local resource time to regrow; this can protect the world but may starve the needy cell immediately.

Under original raw energy laws, harvesting vs resting has one-step advantage `.25*R-.063`. At all thresholds in this study, that instantaneous advantage is positive, but it says nothing about future resource depletion. Thus a higher *or* lower urgency-dependent threshold could win over 20,000 ticks through delayed effects.

Fixed controls cover `.475,.485,.49,.495,.50,.505,.51,.515,.525`. Conditional controls lower the depleted-cell threshold by `.010,.025,.040`; one adversarial **reverse-rescue** arm *raises* it by `.025` for `E<.12`.

## Long-horizon results — four-seed claims do not suffice

The matched 12-seed means at tick20,000:

| Policy | Mean energy | Cells near floor ≤.01 | Cells near ceiling ≥.99 | Raw tail drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Fixed .485 | .36281 | .03% | 0% | −.0000157 |
| Fixed .500 | .64894 | 7.85% | 12.76% | +.0000125 |
| Fixed .505 | .65527 | 6.58% | 15.56% | +.0000152 |
| Fixed .510 | .65022 | 5.27% | 16.93% | +.0000165 |
| Fixed .525 | .47825 | 0% | 0% | −.0000056 |
| Energy rescue, discount .010 | .65022 | 5.27% | 16.93% | +.0000165 |
| **Energy rescue, discount .025** | **.72356** | **.07%** | 12.27% | +.0000242 |
| Energy rescue, discount .040 | .72752 | 0% | 12.14% | +.0000250 |
| **Reverse-rescue: raise threshold .025** | **.82695** | **3.32%** | **26.63%** | +.0000078 |

Other fixed thresholds and exact per-seed trajectories are archived in the JSON. These means are at a finite selected horizon; near-zero raw drift or high stored energy is not proof that a regime can persist indefinitely.

**A stronger result than the prior one-world claim:** energy rescue .025 outperformed fixed .50 in **12/12 fresh seeds**, by +.07462 mean energy at tick20,000. It also beat fixed .505 and fixed .51 in all 12. On another earlier 10,000-tick fresh-seed study, rescue won only 13/24 against .50. The ranking therefore depends on horizon, initial distribution and simulation selection, not a universal policy theorem.

**A genuine adversarial surprise:** raising the threshold for depleted cells (reverse-rescue) performed *better by mean energy* than the original lower-threshold rescue in **12/12** fresh seeds, mean +.10338. However, it also left **3.32% of cells depleted** versus .07% for original rescue, and accumulated far more cells at the energy ceiling (26.6% versus 12.3%). Thus the policy optimizing mean stored energy is not automatically the policy maximizing equitable or all-cell ecological health.

The tiny `.010` rescue discount produced the exact same aggregate outcomes as fixed .51 in this 12-seed screen despite the nominal conditional policy; this suggests its decision boundary rarely changes actions at relevant resource states. By contrast `.025` and `.040` discounts materially changed harvest timing. This is another example of why a parameter value is not evidence of a changed causal mechanism unless action patterns also differ.

## Decision lineage and caveats

- **Initial conjecture:** Low-energy action urgency explains earlier advantage. The results support usefulness of energy-conditioning but **contradict any unique causal claim that harvesting sooner when depleted is the optimal intervention**; an opposite urgency rule produced even higher mean energy at the cost of more depleted cells.
- **Evidence preserved:** Same physics and matched starting states, alternative constant thresholds, positive and negative urgency sign tests, 12 independent synthetic seeds, raw tail budgets and energy distribution. No neural controller learned these rules.
- **Remaining gap:** We have not controlled for equal harvest rates or equal action-distribution access across policies, nor tested representative milder shocks, different regrowth/consumption regimes, exact cell-age lineage, or external systems. Reverse-rescue could fail by other welfare criteria or horizons. The `E<.12` cut and discounts were hand-selected and tested posthoc.
- **Next decisive test:** Freeze three competing conditional policies (low-energy earlier, low-energy later, neighbor-gradient) and compare **longitudinal cumulative shortage, worst-decile energy, floor-duration, and shock recovery** on untouched seed sets. Do not optimize only final mean energy. Require an adaptive neural candidate to beat those hand-coded controls under the **same information budget** before attributing value to its learning architecture.

**Adjudication:** This was **one** substantial adversarial research loop that falsified the simple “low-energy cells should always harvest sooner” story. It did not yield a universal rescue law or automatically confer adaptive intelligence on the Garden. Its primary value is revealing the importance of delayed feedback and competing welfare objectives.
