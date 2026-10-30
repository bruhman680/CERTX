# Observer units and conditional versus ensemble statistics

These derivations concern the specified two-level shadow toy. They were motivated after reading Claude's outputs; they are not blind forecasts about real agents.

Let P be chosen once per trajectory with equal probability from r±sqrt(v), r=0.2 and v=0.032. Conditional on P, X_t are iid Bernoulli(P).

    E[P] = r
    Var(P) = v
    E[P(1-P)] = r(1-r)-v = 0.128
    Cov(X_s,X_t) = v                 (s != t, ensemble over fresh P)
    Cov(X_s,X_t | P) = 0             (within a fixed condition)
    Var(mean_T X) = v + 0.128/T      (fresh independently resampled P per run)

For repeated runs all sharing a single fixed p:

    Var(mean_T X | P=p) = p(1-p)/T

The first variance tends to0.032; the second tends to0. Several observers of one fixed soil do not thereby create independent soil draws. Detecting population heterogeneity requires variation at the relevant sampling level. A known-model likelihood test can still distinguish the specified SH candidate from EC/WK using one long run; “within-run centering hides between-soil variance” does not mean the candidate can never be recognized from one record. SH conditional-on-P is identical to iid Bernoulli at that selected rate; that is a different comparison from iid with a fixed known global rate0.2.

## Window dispersion

For n=16 outcomes per window, population variance pooled across fresh soils is:

    Var(K) = n*r*(1-r) + (n*n-n)*v = 10.24
    DI_pooled = Var(K)/(n*r*(1-r)) = 4

Within fixed p, population variance is n*p*(1-p), giving DI_conditioned=1. Ensemble adjacent-window correlation sharing the same latent P is n*n*v/Var(K)=0.8. These ensemble quantities are not the within-trajectory sample variance and demeaned correlation used in the diagnostic.

The sample DI in Claude's code uses an estimated rate and ddof=1. Under iid Bernoulli(p), conditioning on total errors gives an exact mean T/(T-1) when the total is neither0norT, and DI=0 for those degenerate totals. Therefore:

    E[DI | p] = T/(T-1) * (1 - p^T - (1-p)^T)

Its near1value is expected here. The original header's high-DI shadow forecast is preserved as a failed prediction; its pooled counterfactual is not the statistic actually calculated.

## Negative finite-sample autocorrelation

For M exchangeable iid window counts, the code subtracts the observed mean before computing adjacent products divided by the total squared residual. Conditional on a positive denominator, symmetry plus sum(z)=0 gives:

    E[AC1 | denominator>0] = -1/M

The code returns0 for zero denominator, so the unconditional mean is -(1-Pr(allcounts equal))/M. For n16, that probability is the sum over k of BinomialPMF(16,k;p)^M. At M20 the expected AC1 is about-0.05; this estimator effect is not negative underlying conditional dependence. The new exact enumeration checks the same identity on binary windows of length8; the saved formulas also calculate the mean for the actual n16counts.

## Misspecified independence and an asymptotic floor

The reproduced floor script gives expected per-window log(P_SH/P_WK) under low/high SH soils of about+0.09419/-0.02488. Under stationary ergodic WK, the expected same log ratio is about-0.04207. Nonoverlapping windows are iid conditional on the frozen SH rate, so their average log ratio converges to its conditional expectation. The misspecified iid-window rule therefore selects WK on high-soil SH trajectories with probability tending1. It selects correctly on low-soil SH and on ergodic WK. With equal world priors and equal SH-soil weights, the limiting error is0.5*0.5=0.25. More data strengthens the wrong selection on that SH component. This conclusion uses the constructed laws and strict signs; it is not a general real-agent error floor.

## Finite-sample count wording

For known pair laws and iid independent episodes with equal priors, the conditional Chernoff upper bound is:

    Bayes_error_N <= 0.5 * exp(-N*C)

Thus ceil(log(10)/C) is a sufficient bound-based count for error at most0.05 under those assumptions; it is not the exact minimum empirical sample count. Claude's “crossover” is the first estimated <=5% point on a60-point sampled grid, with2500trials per truth, and its “at N_h” value uses the nearest grid point. Reported ratios are measurements in these cases, not universal conversion factors or exact confidence guarantees. The floating numerical coefficient is not interval-certified, so the source's rounded printed counts are not certified guarantees. The full finite-sample Monte Carlo grid was read/audited, not rerun here. Its zero-error printouts mean zero observed errors, not zero underlying risk.

## Word order

The concatenate-zero-block/one-block construction assigns the FIRST temporal outcome to the LEAST significant index bit. The source's MSB comment/reader uses the opposite convention. Exact length5checks agree either way in SH/EC/WK because their observed word laws are reversal symmetric. A stationary deterministic six-state cycle emitting001011 is a non-reversible rival: LSB indexing matches direct probabilities, while MSB interpretation differs by1/6. Preserve original code/results; do not transfer that reader unexamined to non-reversible worlds.
