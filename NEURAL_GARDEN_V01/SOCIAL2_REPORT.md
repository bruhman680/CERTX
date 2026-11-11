# Neural Garden social-learning investigation: two completed research loops

**Status:** Synthetic, controlled exploration. Two substantive hypothesis–test–revision movements; many simulation ticks are *not* research-loop counts. `SOCIAL2_PLAN.md` and `SOCIAL2_FOLLOWUP_PLAN.md` state the questions before their respective executed outcomes. Primary Living Garden and original dynamics were not modified.

## Loop 1: Does one-time neighbor copying aid changed conditions?

Every cell trained its own three-feature policy through 1,500 teacher-free steps at regrowth .06, then policy-gradient learning was frozen. At the fork, cells either kept weights or simultaneously received copies from a high-energy cardinal neighbor, a low-energy cardinal neighbor, random cardinal neighbor, globally shuffled cell, or the mean of cardinal neighbors. Deployment was deterministic over 3,000 ticks on either stable laws or mild regrowth reduction .06→.055. Twelve matched fresh seeds 10400–10411 per law, six arms per seed; **144 policy deployments** (same trained seed reused across arms).

| One-time intervention | Stable final mean energy | Stable floor share | Mild-shift final mean energy | Mild floor share | Shift wins over no-copy, /12 |
| --- | ---: | ---: | ---: | ---: | ---: |
| No transfer | .20470 | .1285 | .0172 | .382 | reference |
| Highest-energy local donor | .19483 | .135 | .0164 | .396 | 4 |
| Lowest-energy local donor | .1896 | .130 | .0174 | .376 | 6 |
| Random local donor | .2034 | .133 | .0173 | .375 | 6 |
| Globally shuffled donor | .2125 | .122 | .0168 | .394 | 4 |
| Local neighbor mean | .1121 | .112 | .0170 | .385 | 5 |

**Result:** Highest-energy-neighbor copying is *not* beneficial relative to no-copy, nor clearly better than randomly picking a neighbor. Under mild shift nearly every policy collapses toward the same low mean energy: relative changes are tiny. The apparent stable mean-energy gain from global shuffling cannot be called social learning; it is an arbitrary redistribution control and is not robust to the shifted regime. Mean energy and floor share also diverge for neighbor averaging, emphasizing multi-objective welfare.

**Revision:** One-time copying might merely be too brief to matter; test recurrent information exchange separately, with fresh seeds. Do not claim social learning occurs merely because externally specified copying is enabled.

## Loop 2: Does recurrent social copying rescue adaptation?

Follow-up predeclared repeated copying every 300 deployment ticks (initial copy plus nine later events), otherwise same training and laws. Twelve fresh matched seeds 10600–10611, **144 new deployments**. Frozen-own-policy control remains intact throughout.

| Recurrent intervention | Stable final mean energy | Stable floor share | Mild-shift final mean energy | Mild floor share | Shift wins over no-copy, /12 |
| --- | ---: | ---: | ---: | ---: | ---: |
| No transfer | .19931 | .126 | .0171 | .385 | reference |
| Highest-energy local donor | .0696 | .157 | .0176 | .390 | 9 |
| Lowest-energy local donor | .1092 | .045 | .0165 | .389 | 4 |
| Random local donor | .0892 | .106 | .0175 | .376 | 8 |
| Globally shuffled donor | .1125 | .091 | .0180 | .351 | 9 |
| Local neighbor mean | .0453 | .178 | .0175 | .381 | 11 |

**Result:** Frequent policy replacement strongly harms average energy in the stable world, even though some schemes reduce the share of depleted cells (the mean/floor tradeoff remains). Under mild shift, transfer arms differ by at most roughly .001 of energy after the long horizon; the apparent majority of paired wins over a low baseline does not establish meaningful rescue. The mechanism is *external repeated copying*, not evolved social learning or adaptive communication.

**Inference and next question:** These interventions can erase useful individual specialization without adding genuinely novel information. The stronger next test should distinguish social **signals** (neighbor’s recent outcomes or policy advice) from wholesale policy replacement, and let a receiving cell retain or reject advice based on a pre-specified validation period. Include donor-selection sham and an explicit no-communication counterfactual; evaluate a shorter post-shift recovery window to avoid floor saturation. Nothing here proves information sharing is inherently harmful or that social learning is impossible.

## Reproducibility and safeguards

- `SOCIAL2_probe.py` contains the complete deterministic evaluation and policy-copy arms; original `SOC_ENERGY_AWARE_policy.py` supplies teacher-free training and original toroidal environment physics.
- `SOCIAL2_results.json` and `SOCIAL2_followup_results.json` hold full per-seed/per-condition rows and outcome aggregates.
- Evaluation outcomes use 12 matched seeds per regime per experiment, not independent biological populations; no p-values or claims of generalization beyond these synthetic laws.
- We changed only policy coefficient *copies*, not environment laws, resources, or the historical Living Garden state. The same coefficient-copy schedule was applied independent of the actual future outcomes.
