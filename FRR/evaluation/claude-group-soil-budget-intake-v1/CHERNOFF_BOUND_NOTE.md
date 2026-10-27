# A rate heuristic and a conditional finite-sample upper bound

Post-intake analytic clarification; not a reproduction of the soil model or a measured sample-size curve. The source correctly warns that its printed N values are not observed finite-sample thresholds. A stronger distinction is possible under idealized assumptions.

For two **known normalized** episode laws P,Q, equal priors and independent episodes, the optimal likelihood classifier has Bayes error

`Pe(N) = (1/2) sum_z min(P^N(z), Q^N(z))`.

For any s in[0,1], `min(a,b) <= a^s*b^(1-s)`; independence gives

`Pe(N) <= (1/2) [sum_w P(w)^s Q(w)^(1-s)]^N`.

Thus a rigorously justified coefficient yields a conservative finite-sample upper bound, not merely an asymptotic rate. With Chernoff information C, `Pe(N) <= (1/2) exp(-N*C)`. Consequently `N >= ln(10)/C` is sufficient for error<=.05 **under those assumptions and a valid bound on C**, but need not estimate the actual crossover accurately. It is not a universal cost prediction. Even a nonoptimal s gives a valid conservative coefficient if evaluated exactly.

The supplied scripts use approximate stationary distributions and floating numerical optimization, with law-normalization residuals. They do not produce interval-certified coefficients, a calibrated unknown-model guarantee, a finite-sample error curve, or a model-selection procedure with unknown candidates. We therefore do not certify their printed rounded N values as sample-size guarantees. Independently reset episodes, known laws, correct likelihood decisions, equal priors and counted intervention/startup costs must be specified before applying the ideal bound. Adjacent blocks from the same persistent soil are not automatically independent.

For fixed known counts N_a of independently sampled design arms, the coefficient product is `prod_a Z_a(s)^N_a`; its log is a weighted sum of log coefficients. For an arm freshly randomized and observed each episode, the one-episode coefficient is `sum_a f_a Z_a(s)`. The log sits outside that sum. These are different experiments; revealing random arm labels does not make their random counts deterministic.

A simple exact illustration: Bernoulli(.1) versus Bernoulli(.9) has coefficient .6 at s=.5. For odd N, majority classification is optimal and its error is the exact upper binomial tail under p=.1. At N=3 the actual error is .028, already below.05; the bound `.5*.6^3=.108` is conservative. At N=5 its bound is .03888. This illustrates bound versus crossover, without claiming the soil toy has that behavior. No assumptions about real agents follow.
