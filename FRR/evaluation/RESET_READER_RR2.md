# RR2: prediction can succeed while preparation remains unidentified

RR2 separates prediction of the next visible symbol from identification of the protocol that prepared the initial environment. The [protocol and implementation were registered before execution](https://github.com/bruhman680/CERTX/tree/dd40eba8523ea5654a919fbd7554276f3794ca9e/FRR/evaluation/reset-reader-rr2). It uses RR1's already-inspected three kernel tables, five h values per table, five preparations, three population mixtures and times 0 through 8. No new kernel was tuned, no trajectory sampled, and no LLM response measured.

All 405 aggregate and 2,025 conditional preparation/time cells were retained. The main CPU run took 10.04 seconds internally, within the 60-second external timeout. [Summary](reset-reader-rr2/SUMMARY.json), [full rows](reset-reader-rr2/RESULTS.json), and [execution/validation receipt](reset-reader-rr2/VALIDATION.json) preserve the calculation, versions and limits.

## What survived the checks

- A reader using the correct population mixture had no greater aggregate log risk than an equal-mixture reader or a reader always assuming natural preparation. Knowing the actual preparation label supplied an additional information advantage.
- The population-optimal reader was worse than the natural-assumption reader in 856 conditional cells, including 322 where natural preparation was actually used. These are correlated grid cells, not independent trials or a population frequency of harm. Average optimality is not a guarantee for each subgroup.
- Under balanced weights across the five protocols, best observed full-history protocol-identification accuracy through t=8 was about .346. Even a reader directly shown initial E0 would be bounded at .4 in that constructed population.
- At h=1, from t=1 all predictive risks were zero while preparation classification remained ambiguous and stopped improving. The current hidden bit is then the previous visible symbol. The reader can know what determines the future without recovering which initial protocol occurred.
- The five-protocol mixture produced the same finite-word law as a single initial-environment marginal. Entirely fresh-uniform preparation and a half-fixed-e0/half-fixed-e1 mixture also gave identical laws.

Mass, direct joint-chain marginals, conditional log-risk decomposition, mixture collapse, identification bounds/monotonicity and h=1 relations passed at tolerance 1e-11. The largest identity errors were on the order of 1e-15 or smaller. These checks support the finite calculation; several predictions are algebraic properties of its construction rather than discoveries about FRR.

The [post-run checker](../tools/check_rr2_and_hg1.py) separately recomputes selected h=1, t=0 values for additional kernel B with rational stationary probabilities and 60-digit Decimal logarithms. It agrees within 1e-14. Those witnesses were selected after inspecting results, share the model definitions, and are numerical cross-checks rather than independent confirmation.

One concrete separation: in the source kernel, balanced population and h=1, protocol-classification accuracy is .26 from t=1 through t=8, while all four oracle-relative next-symbol KL risks are zero. Readers match the oracle's probability distribution; the next realized symbol remains random. A zero excess-risk score is not perfect prediction of individual outcomes, and neither establishes unique identification of the preparation. An intermediate progress message used the overly broad wording “zero prediction error”; that wording is corrected here explicitly.

## Why protocol attribution is limited here

Let Z be the preparation protocol and rho_z the initial distribution of environment bit E0. Subsequent dynamics are the same for every Z. For any visible word H,

`P(H | Z=z) = sum_e rho_z(e) L_e(H)`.

Therefore a mixture with weights w has the same law as initial marginal `rho_bar = sum_z w_z rho_z`. Different weights giving the same rho_bar cannot be distinguished by these observations. This is an all-horizon linearity argument; finite enumeration is a check, not its proof.

The causal chain is Z -> E0 -> later visible observations. Even E0 itself does not identify Z uniquely. Its optimal classification bound is `sum_e max_z w_z rho_z(e)`. Balanced protocol weights make each maximum .2, attained by a fixed-bit protocol, hence .4 total. This number belongs to these five labels and their overlapping distributions. It is not a universal measure of memory or a claim that systems can recover only 40% of their history.

At the largest subgroup reversal, additional kernel B, h=1, fixed-e1-heavy population, true fixed-e0 preparation, t=0: population-reader risk is .180753 nats versus .005066 for the natural-assumption reader. The latter happens to suit this subgroup better; it remains worse on the overall declared mixture. The subgroup is deliberately rare under the chosen population, so neither the sign nor size establishes an ethical or practical tradeoff beyond this toy.

## What changes our understanding

Preparation metadata can matter, but sometimes its only effect is through a smaller present-state belief. A reader may compress away the protocol label faithfully for prediction while losing historical attribution. Predictive sufficiency, correct mixture assumptions and recovery of an event's identity are different objectives.

This refines the field-of-view idea: choosing what to retain requires declaring what the later reader must do. A current belief may suffice for a predictive job; an audit of how that belief arose needs additional provenance. More observations of identical laws cannot supply a distinction that the construction never preserved.

## Limits and next contact

All readers know the kernels, h, elapsed time and a specified prior family. Population weights are known to the matched-mixture reader. Metadata is extra information. The toy has no protocol-dependent dynamics after the reset; adding such dynamics or a durable label trace can change identifiability. No neural memory mechanism, agent benefit, physical dissipation or general FRR efficacy follows.

RR2 is completed within this scope. Next numerical work can vary unknown mixture weights or protocol-specific later dynamics, with a new prospective protocol. For HG1, [eight development fixtures](hpgm-gates-study/FIXTURE_READINESS.md) now make the packet format concrete, but independent tasks, model execution and cost-aware evaluation remain unfinished. Runtime 0.2 and schema 0.1 remain unchanged.
