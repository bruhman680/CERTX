# Next Garden research — macro-history transfer and inherited action sensitivity

**Status:** Three substantive experimental questions completed, each with an independent analytical/executable burden. The 8-state categories are simple observable projections, **not** measurements of `C_num`, `C_struct`, or `C_symb`. This is a synthetic simulator study, not proof of cognitive memory or beneficial Lamarckian inheritance.

## Question 1: Does macro-history still help if resource regeneration changes?

We keep the previously frozen 8→3 label map `[0,0,1,1,0,0,2,2]`, constructed from resource≥.48, energy≥.12, and last harvesting action. Test the same next-**eight**-state target on eight new baseline and eight changed-regrowth seed worlds, size 10, 420 ticks. The changed world follows the original physics except regrowth .06→.055 for ticks161–320, then returns to .06.

**Separately fitted on the relevant condition** (not a transfer test), held-out prediction errors in nats/category:

| Policy law | Current 3-label NLL | Current plus 3 prior labels | Difference |
| --- | ---: | ---: | ---: |
| Baseline .06 regrowth | .46493 | **.00262** | .46231 |
| Temporary .055 regrowth | .64098 | **.14149** | .49949 |

History helps under both environments, but the changed world's absolute difficulty is much greater. Its final cell energy averaged .306 versus .603 in baseline. We did not optimize the label map on these test worlds.

## Question 2: Does *baseline-trained* compressed memory transfer through a law change?

For a stricter burden, train the three predictors **only on original-law training worlds**, freeze them, then test on untouched baseline or temporarily changed-law worlds. This tests distribution shift without retraining.

| Predictor | Baseline test NLL | Shifted test NLL | During changed law |
| --- | ---: | ---: | ---: |
| Full current eight-state observation | .47463 | 1.12378 | 2.04627 |
| Current three-label macrostate | .47996 | 1.00186 | 1.72112 |
| Three-label plus three previous states | **.00262** | **.54652** | **1.36318** |

The memory-assisted predictor substantially outperforms the others under this specific shift, yet its NLL grows dramatically during the altered period: from about .0066 before the change to 1.3632 during it, recovering to .0774 after the world returns. The learned temporal regularity is useful but **not invariant** under changing physics.

**Important caution:** The eight-state current-only predictor loses its favorable training distribution under the shift; its worse shifted result does *not* imply that observing more information is harmful in general. These are finite-sample smoothed conditional-frequency estimators with different state-conditioned row counts and fixed training laws. Their performance depends on model class, training coverage, phase occupancy, and sample size.

## Question 3: Is mechanically inherited information large enough to affect actions?

The earlier first-birth test established that acquired neural threshold changes are copied to offspring. We repeated that exact paired first-birth comparison on 20 additional fresh seeds, with mutation disabled and bit-identical prebirth environments, then evaluated newborn action propensities over a standardized resource range [.25,.75] at the model's slope of 14.

The **mean maximum absolute action-propensity difference** between acquired-threshold and germline-only newborns was approximately **0.00102**. This small expected behavior change helps explain why successful mechanical transmission had not produced a robust population-level fitness difference in earlier tests. It does not prove the inheritance cannot matter over generations, nor does it estimate actual selection under ecological stress.

## FRR reading / next orientation

1. **Compression preserves a lineage of lost distinctions.** Some distinctions become predictable again when history restores a phase trajectory. The same history can become less reliable under changed world dynamics.
2. **Storage is not sufficient for utility.** An acquired threshold can cross a parent–child boundary faithfully while having only a tiny immediate effect on the child's action distribution.
3. **A stronger inheritance challenge:** explicitly test when acquired policy changes are large enough to alter descendants' actual harvesting decisions, then compare inherited benefit against clonal/no-learning controls with the same ecology. A stronger memory challenge tests state-dependent adaptation of the coarse predictor *online* during changing conditions, rather than freezing a baseline-trained model.

## Reproducibility and limitations

- `NEXT_MEMORY_probe.py` and `NEXT_MEMORY_results.json` contain macro-regime and inherited propensity data.
- `NEXT_MEMORY_transfer.py` and `NEXT_MEMORY_transfer_results.json` contain frozen training-to-shift tests, including time windows and individual seed scores.
- Source SHA-256, seed lists, law interventions, model categories and exact trained/frozen conditions appear in both data files.
- Eight macro labels are not complete microstates: continuous values, neighboring resources, personal neural weights and recurrent hidden state are suppressed from this representation. The resulting process need not be first-order Markov even before coarse compression.
- All numerical results are synthetic within a single designed world family, selected exploratory questions; no preregistered external replication is claimed.
