# ST-C1: error-propensity soil toy intake

Three user-supplied originals—code, saved output and Claude relay—are [preserved unchanged](../../lineage/sources/claude-soil-intake-2026-10-21/manifest.json). The supplied script ran unchanged and its stdout matches the supplied output after trimming edge whitespace. [RUN.json](RUN.json) records exit code0 and about1.03seconds; stdout/stderr remain separate. This closes source/reproduction contact, not validation of real-agent error soil.

A separate [audit implementation](../../experiments/soil_intake_audit.py) rebuilds the transitions, computes stationary distributions analytically/directly, derives wake tuning without the source grid/fsolve, and decomposes the estimator score. [AUDIT.json](AUDIT.json) preserves results; all five audit checks passed. This shares the toy's definitions and parameters: it is not the proposed different-parameterization test or independent physical replication. No additional agents were spawned.

## What reproduces

All three selected worlds have stationary error rate0.2 and lag-one covariance0.032. Shadow covariance stays constant; echo covariance decays geometrically; wake covariance decays slowly. Forcing an error and conditioning on a naturally observed error produce the supplied curves. Perfect coordinate resets remove the respective echo/wake do-effects against the same reset without a probe. The relay correctly preserves and retracts its failed echo prediction: the do-effect is0.16*0.2^(k−1), not0.2 followed by zeros.

“Exact” here means finite enumeration without Monte Carlo sampling. The supplied tuning and stationarity use floating-point fsolve and a finite power method, rather than exact rational arithmetic. Shadow is reducible and uses the explicitly selected uniform hidden-soil mixture; the transition matrix does not determine that mixture uniquely. Echo has an unused frozen soil coordinate; the audit preserves its stated mixture too.

## Boundaries that matter

**Matched summaries are not matched passive laws.** Length-six passive TV distances reproduce as SH–EC0.2407791, SH–WK0.01219915 and EC–WK0.2425344, all positive. Longer passive observations can distinguish these three stipulated laws statistically. A shared rate and lag-one covariance alone cannot. Small TV at this word length is not a general passive impossibility result or sample-complexity theorem.

**The two-number signature is not necessary here.** The lag-one do-effects alone are0,0.16 and0.08421, already distinct. Adding observe-minus-do provides a useful decomposition, but its necessity does not follow from this example. The observe-effect is0.16 for all three because the marginal and lag-one covariance were matched. Neither do-effects nor their pair universally identify a physical memory location outside this family.

**Resets locate the model's response route under stipulated semantics.** Coordinate-selective perfect reset maps are part of the construction. Shadow's do-effect is already zero before any reset; that says the forced error did not alter its future propensity, not that shadow lacks a persistent environmental condition. In fact resetting shadow soil changes baseline propensity to its low level, approximately0.0211, for both probe and control. Comparing their difference removes that shared baseline change.

**Probe leakage needs a new derivation.** The earlier erase-gate linear-bias formula concerns an additive two-carrier decay model and specified independent interventions. The soil model has outcome-dependent state transitions and different reset targets. The same methodological controls are relevant, but “apply directly” requires mapping the actual reset operator and its interactions; the earlier scalar formula is not automatically its bias law. Leaky reset experiments are proposed, not executed by this intake.

**A finite exchangeability check is limited.** SH is a mixture of iid processes by construction. Equal-count word probabilities at one finite length alone do not prove an arbitrary process is an infinitely extendible iid mixture. The source comment's unqualified “iff” needs those additional conditions.

## An analytic tuning check

Let low propensity L=0.02, error target R=0.2, lag-one covariance C=0.032 and low-to-high deposition U=0.5. For the supplied wake mechanism,

`H = R + C / (R − L(1−U)) = 0.3684210526`,

`h = (R−L)/(H−L) = 0.5166163142`,

`d = LU(1−h) / [h(1−H)] = 0.01481481481`.

The soil transition rates per step are LU and(1−H)d. Its spectral gap is their sum,0.01935672515; its nontrivial eigenvalue is0.98064327485. Thus d is a conditional clearing probability, not by itself the soil relaxation rate. These values reproduce the source's numerical tuning without its search, within the same parameterization. The relay's earlier failed tuning is an authored account; its discarded source/run was not supplied and is not independently reproduced here.

## The estimator score mixes two quantities

For a history h, let p_s be error probability at hidden state s, p̄(h)=E[p_s|h] the posterior-predictive probability under the actual preparation/intervention, and q(h) the EWMA estimate. The Bernoulli identity is

`E[ KL(p_s || q(h)) | h ] = E[ KL(p_s || p̄(h)) | h ] + KL(p̄(h) || q(h))`.

The supplied score uses the left side, comparing the estimator with an oracle that sees the hidden state. The first term reflects information absent from that history; the second is predictive regret relative to what the history actually warrants. Interventions can change both. The audit sums both terms over every relevant history and verifies the identity numerically at every reported lag.

| Probe-minus-control excess, millinats | Supplied latent-oracle score, lag1→6 | Posterior-predictive regret, lag1→6 |
|---|---|---|
|SH|+127.648→+0.771|+127.648→+0.771|
|EC|−4.764→−19.726|+13.219→−19.726|
|WK|+12.592→+17.799|+51.473→+17.465|

Endpoints do not imply monotonicity for the entire echo curve; all six lags are in AUDIT.json. Wake predictive excess decreases at each tested lag even while the supplied combined excess rises from lag1 to6 (with an initial dip). Hence the relay's increasing score is not, by itself, evidence that predictor error grows because its forgetting outruns the soil. The hidden-information term also changes.

For SH the forced error changes no underlying propensity, so treating it as a naturally informative sample overreacts at lag1. That narrow finding survives the decomposition. For EC, the negative original lag-one excess combines positive predictive regret with eliminated hidden-state uncertainty; it is not evidence of improved lag-one prediction relative to the history-aware oracle.

The code implements an EWMA estimator, not a closed-loop PID controller with an actuator or saturation. “Windup” is a candidate analogy here, not an observed anti-windup mechanism. An actual estimator/controller comparison would need declared information access, preparation-aware predictors, effort/action outcomes and an explicit control objective.

## Preserved audit failures and remaining work

The first new audit failed because its source-isolation environment omitted alpha=0.3. The second completed calculations but could not serialize a NumPy boolean. Both pre-repair harnesses are retained, with [repair notes](AUDIT_REPAIR.md). The final harness supplies the original constant and converts check flags to ordinary booleans; no numerical model was retuned. Neither failed attempt wrote AUDIT.json. This separates audit-wiring failures from the source's preserved wrong prediction.

The relay proposes: different-parameterization rebuild, leaky resets, mixed worlds, estimator/timescale sweep and a real-data bridge. This intake tests none of those broader proposals. They remain candidate contacts, overlapping existing carrier/probe and feedback families. The estimator-score distinction should inform any next protocol before interpreting a persistence boundary. No core version, queue status or efficacy claim changes.
