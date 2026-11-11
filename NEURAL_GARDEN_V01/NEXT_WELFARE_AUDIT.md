# Independent welfare-objective audit — reward shaping, Pareto tradeoffs and horizon sensitivity

**Status:** One independently executed adversarial research loop with a new 64-trajectory, 8,000-tick untouched-seed follow-up. Source: `NEXT_WELFARE_AUDIT.py`, `NEXT_WELFARE_AUDIT_results.json`. This audit also inspected original deterministic welfare training, matched manual controls and the derived Pareto analysis. It is not evidence of biological welfare, human values or general intelligence.

## Original findings verified against source and archived data

`NEXT_WELFARE_deterministic.py` trains four different per-cell policy-gradient reward objectives on matched training seeds, transfers each learned threshold vector to a separate seeded world, **freezes all weights**, and uses **deterministic** action selection for each arm. The training seed and test-world seed differ (`seed` versus `seed+20,000`). Manual controls use the same test-world seeds and starting physical resource/energy arrays. They also use deterministic actions, so unlike the earlier stochastic-online comparison, the action-selection mode is matched.

Recorded source SHA-256 digests for `garden.py`, `NEXT_WELFARE_garden.py`, `NEXT_WELFARE_study.py`, `NEXT_WELFARE_deterministic.py` and the manual controls all matched the current local bytes. The `RuleGarden(fixed50)` implementation was previously checked against `ThresholdGarden` for exact same-world transitions over 3×200 ticks. The original data's 12 paired fresh seeds9500–9511 gave:

| Original 3,000-tick stable-policy outcome | Mean energy | Near-energy-floor cells |
| --- | ---: | ---: |
| Reserve-shaped learned neural, frozen deterministic | **.71390** | 2.33% |
| Manually designed neighbor-gradient deterministic | .65930 | **0%** |

The paired reserve-minus-neighbor mean-energy difference was `+.05460`, paired SD `.04027`, with **10/12** seed wins. This is evidence of reward-engineered policy quality in the synthetic world, not an online-adaptation advantage; the reserve penalty `-.3 × max(.18-next_energy,0)` explicitly encodes the designer's preferred low-energy condition. A resource-sensitive initial neural coefficient is also designer supplied. The four reward objectives are separately trained, so any advantage compares *trained policies under different selected rewards*, not a causal ablation of an individual learned feature.

The original aggregate Pareto analysis is numerically correct for its **two specified axes**: maximize mean energy, minimize near-floor fraction. Under original stable conditions, `neural/reserve` and `manual/neighbor` were nondominated; under the original 3,000-tick mild regrowth schedule, manual `reverse` dominated the tested aggregates (mean energy `.27764`, floor `10.75%`) versus reserve-resource learned `.26218`, floor `16.75%`. Importantly these are **means across seeds**, not per-seed dominance or a theorem that one rule wins at all horizons. The study's old designer scalar score `energy-.5*floor` is arbitrary and should not be called natural welfare.

## Newly run independent longer-horizon follow-up

I froze the already-designed reserve reward shape and three strong manual policies **before** running new probes. New training seeds `9600..9607`; matched but separate physical test seeds `29600..29607`; 10×10 cells; 1,000 teacher-free training ticks; 8,000 frozen deterministic test ticks. Original physics in `stable`; in `mild`, only resource regrowth changes `.06→.055` at test ticks1001–2000, then returns. No online updates occur during either test. Every policy sees the same physical initial state for a given seed/regime. The raw record also tracks checkpoints at ticks1000,2000,3000,5000,8000, cumulative floor occupancy, lower-decile energy, and unclipped raw energy drift in the final 500 ticks.

| Stable world, tick8,000 | Mean energy | Floor fraction | Bottom-decile energy | Tail raw drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Reserve-shaped neural, frozen | **.73903** | 3.125% | **.03235** | **−.00003495** |
| Neighbor-gradient manual | .70107 | .25% | .21057 | +.00002503 |
| Reverse-rescue manual | .70601 | 1.00% | .18239 | +.00002262 |
| Fixed .50 manual | .68159 | **0%** | .16532 | +.00002057 |

Here the reserve learner still has the highest *mean* energy, but it has markedly worse worst-decile energy and a **negative late unclipped energy budget**. In this new eight-seed test it beat neighbor-gradient on only **6/8** seeds, paired mean +.03797 (SD .06069). At tick3,000 of the same runs it had .70839 versus neighbor .65796. This is promising engineering under one environment, but its aggregate stored energy advantage does not establish resilience or indefinitely positive budgets.

| Mild regrowth, tick8,000 | Mean energy | Floor fraction | Bottom-decile energy | Tail raw drift/tick |
| --- | ---: | ---: | ---: | ---: |
| Reserve-shaped neural, frozen | **.54410** | **9.63%** | .00608 | **−.00024423** |
| Neighbor-gradient manual | .20037 | 11.63% | .00192 | +.00002554 |
| Reverse-rescue manual | .36969 | 13.25% | .00066 | −.00004980 |
| Fixed .50 manual | .16227 | 14.88% | .00082 | +.00001460 |

The reserve learner in this particular mild-shift horizon now has higher mean energy and lower final floor fraction than the three manual controls, beating reverse rescue in **7/8** matched seeds (paired +.17441, SD .14384). But its raw final energy budget is **substantially negative** and its worst decile remains near zero; that means it may be spending down accumulated reserves. These are finite-horizon observations and do not prove eventual survival.

At **tick3,000** of these same mild-shift runs, reserve neural energy was `.25428` and reverse rescue `.28517`. By **tick8,000**, the ranking had reversed (`.54410` vs `.36969`). Thus which policy appears 'best' depends materially on the chosen time horizon and on how energy and floor occupancy are weighted. An aggregate Pareto frontier should be recomputed for each horizon *and* raw budget, not carried forward unchanged from an earlier endpoint.

## Why the apparently strong result is not a broad intelligence claim

1. **Designer-supplied objective:** The reserve penalty instructs the network to avoid a low-energy region. Improved behavior is legitimate reward engineering, not independently discovered ethics.
2. **No ongoing learning:** Neural weights were frozen during the 8,000 test ticks. This supports *quality of an acquired policy*, not capacity to update during changing conditions.
3. **No universal rule:** There are only eight untouched synthetic test seeds, all generated by the same toy world's laws. The reward family and models were informed by previous exploration; this is exploratory holdout, not pristine independent preregistration.
4. **Equity and budget conflict:** At stable tick8,000, reserve neural stores more average energy but has more depleted cells, lower bottom decile and negative raw late drift. The manual fixed .50 has lower mean but no depleted cells and positive raw drift in this short tail. Which outcome is preferable requires a declared burden.
5. **Horizon sensitivity:** Mild-shift rank changes between tick3,000 and tick8,000. No observed endpoint proves an attractor or indefinite viability.
6. **Clipping:** Observed stored energy can diverge from the pre-clipping resource budget near floor/ceiling. Report both.

## Verification

- Exactly **64 unique** `(seed,regime,policy)` records; source hashes match their final files; Python/NumPy environment recorded.
- All displayed paired comparisons use world seeds as units, never cells or ticks as independent replicates.
- Original Garden energy/resource equations unchanged; only mild-regrowth interval explicitly modifies a law.
- The initial physical test-world resource/energy state is matched for all policies using identical test seeds; neural weight differences originate in controlled training objectives.

**Verdict:** Reserve-shaped deterministic learned behavior can exceed strong manual rules on aggregate mean energy in selected conditions, but its increased depleted-cell exposure and negative raw late drift weaken any broad 'healthier Garden' conclusion. The next decisive experiment should use an explicitly fixed multiobjective criterion (including worst-decile and raw-budget constraints), and compare a *continuously updating* learner against its otherwise identical frozen counterpart under matched action-selection mode, untouched regime seeds, and long-horizon evaluation.
