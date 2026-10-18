# RR2 prospective protocol: unknown preparation, prediction and attribution

Save this protocol, settings, implementation and dependency hashes before execution. This is a finite-model extension of RR1, using its already-inspected kernels and five preparation protocols. It is not a held-out confirmation or an actual-agent efficacy test.

Question: can a reader predict adequately while remaining unable to identify which reset protocol generated its observations? When does averaging over protocols improve aggregate log risk, and who can lose in an individual subgroup?

## Fixed design

Retain RR1's (y,e) chain, three kernel tables and five h values per table. All histories start at y=0. Protocol label Z selects an initial e distribution; after that, K and h are identical across labels. Preparations are natural conditional, independently retained stationary marginal, fixed e=0, fixed e=1, and fresh uniform. At h=0 the equal-environment stationary mixture is explicitly selected, as in RR1.

SETTINGS.json fixes three population distributions over Z: balanced, natural-heavy, and fixed-e1-heavy. Enumerate all visible histories at times 0 through 8. No sampled trajectories or learned parameters. Reader variants:

- **Metadata:** knows actual Z and uses its matched full-history conditional prediction.
- **Population:** knows the population weights but not Z; averages with posterior weights after observing the history.
- **Uniform:** uses equal initial protocol weights, including when the population is skewed.
- **Natural:** always assumes the natural-conditional preparation, regardless of actual Z.

Metadata has extra information. Its advantage is not an equal-information algorithmic gain. All readers know K, h, elapsed time and visible history. A separate calculation collapses the population mixture to its single initial e marginal, testing equality of prediction laws. State support is fixed; no per-population tuning follows results.

There are 405 population/time cells and 2,025 conditional protocol/time cells. Retain all, including losses and ties. Report aggregate and per-protocol oracle-relative expected KL risk in nats. Identification is a different output: compute optimal Bayes classification accuracy for Z given the full visible prefix, not a verbal confidence score.

## Predictions and checks fixed before execution

1. Population-matched prediction has no worse aggregate log risk than Uniform or Natural. Metadata has no worse aggregate risk than Population. This is a conditional log-score relation, not evidence of FRR superiority.
2. Equal population weights make Population and Uniform identical. No universal per-protocol improvement is predicted: report every subgroup reversal. Report whether any occurs without changing parameters to obtain it.
3. A population mixture over initial e distributions predicts exactly as its collapsed initial e marginal. Compare complete finite-word joint weights, not just a scalar accuracy.
4. Two different mixtures—entirely fresh-uniform protocol versus equal fixed-e0/fixed-e1 protocols—have the same initial e marginal, hence the same visible law in this model. Verify the finite laws; give the separate linearity argument for all horizons.
5. Z influences future observations only through initial E0. Classification accuracy therefore cannot exceed `sum_e max_z w_z rho_z(e)`, the bound for a reader that sees E0 itself. Under balanced weights this bound is .4 because fixed-e0 and fixed-e1 attain its two maxima. This is construction-specific, not a universal memory-capacity number. Accuracy from growing full prefixes should not decrease.
6. At h=1, from t=1 the current e is the previous y. All four full-history predictive risks and the benefit of preparation metadata should be zero. Protocol identification can remain ambiguous; its accuracy should plateau after the first transition because later dynamics add no further Z information conditional on y1.

Acceptance tolerance is 1e-11 for probability, risk and identity checks. Check oracle-risk decomposition, population risk ordering, word-law collapse, identification bound/monotonicity and h=1 behavior. Save output before signaling a failed check. Classify any failure before modifying code; preserve the first result and register a later repair rather than silently overwrite.

## Resource and record contract

One primary local CPU run, external timeout 60 seconds; no GPU/provider API/agent calls. Save internal elapsed time, Python/NumPy/platform, dependency hashes, every result row and compact summary. Token, money and energy costs are not measured. Any post-run selected-witness calculation is a separate follow-up with its selection disclosed.

Run `python FRR/experiments/reset_reader_rr2.py`. Raw stdout/stderr and an execution receipt will accompany the results. The implementation imports RR1's helpers without executing its main routine; record that shared ancestry and dependency. The model has no protocol-specific dynamics after the reset. A result about nonidentifiability must keep that assumption; persistent protocol metadata or different update rules could change it.

Next contact: move from known population mixtures to uncertain mixture weights, or to actual continuation agents facing correct, missing or wrong provenance. Neither is automatically established by this model.
