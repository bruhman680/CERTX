# Adaptive-society study: one research loop with forty optimizer iterations

**Status:** Executed; same original Garden environmental laws throughout. This is **one substantive research loop** consisting of *forty* optimizer iterations. Each iteration records a changed controller parameter proposal, candidate configuration, matched seeded evidence, acceptance/rejection and next search orientation. These are engineering decisions within one hypothesis family, **not forty separate research loops, and not forty scientific discoveries**. The holdout is disjoint from developmental seeds but drawn from the same synthetic generator.

## Why this society pursued the question

Past runs showed (i) current neural controllers do not reliably discover sustainable harvesting, (ii) a simple fixed threshold near `.50` is formidable, and (iii) trained per-cell resource thresholds can modestly improve over their untrained starting values. We asked whether a deliberately evidence-guided search over a *teacher-free* learner could close the gap. This is optimizing the **learning setup**, not teaching correct harvest actions.

## Reproducible design

- Code: `SOC_ADAPTIVE_sequential.py`; raw: `SOC_ADAPTIVE_results.json`. The JSON field `optimizer_iterations` contains the **40 within-loop design probes**, not forty separate entries in the Garden's conceptual research ledger.
- 40 iterations, proposing one-at-a-time changes to trace decay, learning rate, slope and initial threshold distribution. Every iteration has a distinct stated candidate, a 4-seed matched developmental probe (seed6100–6103), 500 teacher-free learning ticks, and deterministic 800-tick transfer evaluation. A candidate is retained if developer-seed mean energy improves by >.0001; 16 accepted.
- After all 40, a separately reserved twelve-seed set 7100–7111 evaluated the final champion, unchanged default learner, and fixed `.50` policy, all in 8×8 worlds. These 12 seeds were not used by the search.
- Next, `SOC_ADAPTIVE_validation.py` checked the selected configuration **without further fitting** in larger 16×16 worlds and a 3,000-tick horizon, using twelve fresh seeds 8800–8811, matched test initial worlds, a frozen *untrained initial threshold* control, the original learner setup, and fixed `.50`/`.51` policies. This is a post-selection follow-up, not an independently preregistered field test.
- All cells have distinct teacher-free one-parameter stochastic neural thresholds while learning. Final evaluation uses deterministic decisions based on their learned threshold. This is not the original 12-hidden-unit recurrent controller; no births, deaths, or inheritance are involved.

## Selected policy

The sequential search ended with `trace_decay=.925`, `lr=.0031`, `slope=24.5`, and random initial thresholds in `[.5425,.6825]`. This altered **both** learning dynamics and the starting-state distribution. We cannot attribute the resulting gain solely to the optimization rule, delayed reward, or initial heterogeneity without further factorial ablations.

### First sealed holdout (12 seeds; size8; evaluation at tick800)

| Behavior | Mean final energy | Fraction near energy floor |
| --- | ---: | ---: |
| Optimized learned individual thresholds | **.64618** | **9.11%** |
| Same optimized init, not trained | .38989 | — |
| Original learning configuration | .30358 | 44.14% |
| Uniform fixed threshold `.50` | .61480 | **0%** |

The optimized learned policy exceeded the fixed `.50` *mean energy* at this limited 8×8/800-tick horizon, but the fixed rule protected every cell from the near-zero-energy floor. The optimized policy was not uniformly healthier.

### More demanding follow-up (12 new seeds; size16; evaluation at tick3000)

| Behavior | Mean final energy | Fraction near energy floor |
| --- | ---: | ---: |
| Optimized learned thresholds | **.64076** | 12.01% |
| Optimized init, untrained | .39559 | 18.10% |
| Original learner configuration | .28772 | 45.31% |
| Fixed threshold `.50` | **.64982** | **0%** |
| Fixed threshold `.51` | .64795 | **0%** |

The optimized policy's improvement over its frozen identical initial thresholds persisted (+.245 mean energy), but it **did not beat the simple fixed `.50` rule on the larger, longer follow-up**; and about 12% of its cells had nearly zero energy versus 0% under either fixed control. These are descriptive within-simulator outcomes, not real-world statistical confidence intervals.

## What this actually teaches us

1. A teacher-free local controller can acquire substantially better *resource-sensitive action behavior* after sequential design optimization; both trained and untrained variants were measured.
2. Mean ecological energy is insufficient as the sole objective. Different strategies can produce a high average while leaving a substantial minority of cells depleted.
3. Hyperparameter selection and initialization tuning are designer-mediated; the result is **not** spontaneous scientific self-discovery by neural cells.
4. Reusing just four developmental seeds for 40 choices invites strong optimization bias. The two disjoint evaluation sets help, but both came from the same world generator and were examined after the design was selected.
5. Fixed `.50` remains a strong baseline in stable laws; performance under changing laws and across very long horizons must be evaluated separately. The final learned policy has not shown indefinite viability.

**Next strong hypothesis:** replace mean-energy-only acquisition with a two-objective rule that penalizes *fraction of depleted cells*, preserve uncertainty with matched fresh seeds, and test whether a learned controller can generalize to held-out environmental changes where `.50` fails. Until then, the tuned policy is a useful experimental tool, not superior ecological intelligence.
