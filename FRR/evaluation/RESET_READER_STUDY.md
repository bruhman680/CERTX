# RR1: history, reset preparation, and a failed prediction

The first prospective research trial using our adopted bounded loop examined when more history helps a reader after a reset. It **failed one predicted source-kernel reversal** and exposed a confound in the older comparison. It also found a smaller controlled reversal in a different prespecified kernel. The failed prediction, all cells, and the original implementation are retained.

The [protocol, fixed tables and executable were committed before execution](https://github.com/bruhman680/CERTX/tree/c7d117d3ea6ccb3a1f51249746a79482cfa7b650/FRR/evaluation/reset-reader-study). This is prospective recording of this particular extension, not untouched discovery: earlier source-kernel results informed the question. The two additional tables were not independently authored or sampled from a task population, and no settings were tuned after inspecting their outputs.

## What ran

Three binary agent/environment kernel pairs, five h values each, five preparation protocols and nine prediction times produced **675 cells**. Each cell compares nine readers. All finite visible histories are enumerated; no stochastic sampling or LLM responses are involved. The main run took 7.61 seconds internally, within its external 60-second timeout. The timer excludes interpreter/import startup and output serialization. See [execution receipt](reset-reader-study/EXECUTION_RECEIPT.json), [full rows](reset-reader-study/RESULTS.json), [summary](reset-reader-study/SUMMARY.json), and [stdout](reset-reader-study/RUN_STDOUT.txt). Stderr was empty and exit code was zero.

State consists of visible y and hidden e. The visible transition uses K[e][y]; afterward, with probability h, e becomes the previous y. All preparations begin with y=0. They differ in whether e is naturally conditioned on y=0, independently retained from its stationary marginal, fixed at 0, fixed at 1, or freshly uniform. Some protocols coincide in particular cells. At h=0 the stationary environment mixture is explicitly equal-weighted because there is no unique joint stationary law.

Matched readers know the actual preparation. Assumed-natural readers always use the naturally conditioned preparation, even when it is wrong. In each family readers retain 1,2,4, or all available symbols. All know the elapsed time. A separate stationary one-symbol reader recreates the earlier baseline assumption. Giving a matched reader preparation metadata changes its available information; its advantage is not a free algorithmic improvement.

## Results against the recorded predictions

| Prediction | Result |
|---|---|
| Matched readers benefit or tie as retained information increases | Passed in every cell; this checks a conditional log-score relation, not FRR efficacy |
| Excess risk decomposes into an averaged KL between predictions | Passed; maximum numerical discrepancy 1.81e-16 nats |
| Assumed-natural full history loses to assumed-natural one-symbol history somewhere in the source grid | **Failed: zero such cells** |
| At h=1, full and two-symbol readers lose preparation dependence after the first transition | Passed exactly in these computations |

The direct joint-chain marginal cross-check agreed with the history enumeration to 1.23e-15. Probability mass and stationarity checks passed. The original scoring function and model tables were not repaired or changed after the results.

## Why the failed prediction matters

In the older source example at h=.2, fixed initial e=1 and t=1, the full reader has oracle-relative risk .0755444 nats while the stationary one-symbol reader has .0551770. Those numbers reproduce here. But when the one-symbol reader uses the **same elapsed-time/reset assumption** as the full reader, its risk is also .0755444. The apparent early benefit of shorter memory came from a different predictive assumption, not a clean change in history length. At this time y0 is fixed for everyone, so retaining it supplies no additional distinguishing information.

Across all 225 source cells, full assumed-natural history never loses to the age-aware one-symbol counterpart. It loses to the stationary one-symbol baseline in three cells. That comparison remains a valid example of reader misspecification; its interpretation as a pure history-length effect was too broad.

## A genuine, small controlled reversal

| Prespecified kernel | Cells where assumed-natural full loses to age-aware assumed-natural one-symbol | Total cells |
|---|---:|---:|
| Source | 0 | 225 |
| Additional A | 0 | 225 |
| Additional B | 3 | 225 |

These are correlated grid counts, not independent trials, effect probabilities, or estimates of how often this occurs in nature. All three reversals in B occur with h=0, fixed e=0, at t=4,5,6. At the largest, t=5, full-history risk is .0093166394 nats and one-symbol risk is .0092356848: full history is worse by **.0000809546 nats**. The difference is real in this toy but small. Correctly prepared readers have zero oracle-relative risk in this fixed-environment case.

A [post-run selected-witness check](../experiments/reset_reader_witness_check.py) recomputed those three cases by direct products of exact rational path weights and 60-digit Decimal logarithms, without importing the main filter. It agrees with the float gaps within 1.1e-16. [Check output](reset-reader-study/WITNESS_CHECK.json) is retained. This was selected after inspecting results, shares the model definitions, and does not constitute independent confirmation or an expanded search.

## What we understand more precisely

For full visible history H and any reader prediction q(H), oracle-relative expected KL risk decomposes as

`R(q) = R(q_matched_full) + E_H KL(q_matched_full(H) || q(H))`.

Matched suffix readers are conditional averages under the actual law; nested information therefore cannot worsen their expected log score. With the wrong law, that guarantee does not apply. More retained history can change how a misspecified model combines evidence, occasionally making its conditional performance worse. This is not a claim that additional available information is intrinsically harmful: an unrestricted reader could ignore it.

At h=1 the environment is overwritten with the previous visible symbol. From t=1 onward, two visible symbols identify the current e, so the initial-preparation mismatch no longer matters to those readers. This is exact within this update rule, not a general claim that memory vanishes after one step. The environment now carries a known recent trace instead of an unknown initial condition.

The useful connection to our field-of-view discussion is that the **circumstances under which a record was made** can matter alongside its length. More context does not calibrate its own interpretation. Conversely, limiting history is not a universal cure for wrong assumptions.

## Decision and next contact

Accept the algebraically checked toy results and narrow the earlier interpretation. Retain the failed source prediction, the small B counterexample, and every nonreversal. Runtime 0.2 and schema 0.1 remain unchanged; no actual-agent benefit or physical memory mechanism has been tested here.

Next: a reader that does not know the preparation, using a declared mixture over possible protocols or explicit metadata, compared at matched information/cost. Separately, real continuation agents can be tested on records with correct, missing or wrong provenance. Neither study has been executed by this trial, and the present tiny models do not establish transfer to those settings.
