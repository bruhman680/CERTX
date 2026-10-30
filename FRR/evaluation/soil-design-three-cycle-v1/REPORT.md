# Three soil-design cycles: what more observations can and cannot settle

Completed 30 October 2026 UTC. Parent: CO-C1 at `62bc87c84c6104292f9b2db4fb26d1f0237ea23d`. This is a local mathematical follow-up to the archived Claude explorations, not a new Claude result or real-agent trial.

The useful refinement is **label the target, independent cause draws, and intervention effectiveness alongside the fruit**. More observations can improve one target while leaving a different question unidentified.

## Scope and chronology

All three questions, parameters and primary checks were written in [PROTOCOL.md](PROTOCOL.md), then the [calculation code](experiment.py) and protocol were hash-frozen in [FREEZE.json](FREEZE.json) before execution. The three scoped cycles were evaluated sequentially in one local invocation; they are not three adaptive searches or independent replications. No generated data, Monte Carlo tuning, paid services, model calls, weight updates, cache deletion, or source-script edits were used.

[RESULTS.json](RESULTS.json) records seven budget designs, eight one-soil rival comparisons plus one four-soil design, and five reset scenarios. Its 200 passing assertions include repeated normalization checks: this is **not 200 independent experiments**. The subsequent [rational audit](rational_audit.py) checks selected identities in exact fractions; it is a post-result coordinator self-check, not independent agent review. Its [results](RATIONAL_AUDIT.json) preserve the distinction from the original floating-point run. No protocol deviation or failed prediction occurred in this narrow run. The protocol had identified the four-soil product comparison as conditional on tractability; all 83,521 count vectors were tractable and evaluated.

## Cycle 1 — same observation budget, different independent soils

A soil has a frozen rate `P = .2 +/- sqrt(.032)`, chosen with equal probability. Emissions are conditionally independent Bernoulli observations. Fix 64 observations; use k independent soil draws with n observations each, kn=64. For the **population mean .2**, the variance of the overall mean is

`Var(mean) = .032/k + .128/64`.

This follows from the between-soil variance plus the average conditional emission variance. We convolve the complete per-soil count distributions rather than simulating samples.

| Independent soils k | Observations per soil n | Mean variance | Inflation vs iid | Coverage of fixed iid-normal interval |
|---:|---:|---:|---:|---:|
| 64 | 1 | .0025 | 1.0x | 95.96% |
| 32 | 2 | .0030 | 1.2x | 93.85% |
| 16 | 4 | .0040 | 1.6x | 89.33% |
| 8 | 8 | .0060 | 2.4x | 80.71% |
| 4 | 16 | .0100 | 4.0x | 67.62% |
| 2 | 32 | .0180 | 7.2x | 51.66% |
| 1 | 64 | .0340 | 13.6x | 5.49% |

The interval is deliberately held fixed at `observed_mean +/- 1.96 sqrt(.16/64)` and checked against the true population mean. It is not a calibrated 95% interval for clustered observations, nor is even the independent finite-binomial coverage exactly 95%. The “effective iid sample size” in the raw results is variance-equivalent only, not a universal sample size.

**Garden reading:** 64 leaves from one plant are not 64 independent plants. Yet many leaves can be useful for estimating that particular plant's rate. This result targets a population average and omits reset/acquisition costs. It does not prescribe more agents, more resets, or shallower records for every task.

## Cycle 2 — a different soil can match the first two moments

The rival draws its frozen rate from `Beta(.8, 3.2)`. It has the same mean .2 and variance .032 as the two-point soil, but a continuous latent distribution. Thus both have the same binary one- and two-observation laws, not merely a matching estimated correlation. They differ on three or more observations sharing the same soil.

| Observations from one soil | Total variation | Equal-prior minimum classification error |
|---:|---:|---:|
| 1 | 0 exactly | 50% |
| 2 | 0 exactly | 50% |
| 3 | .025600 | 48.72% |
| 4 | .052992 | 47.35% |
| 8 | .153506 | 42.32% |
| 16 | .266343 | 36.68% |
| 32 | .383787 | 30.81% |
| 64 | .488373 | 25.58% |

The exact rational audit verifies the first five rows including the exact zeroes; the floating calculation has roundoff near 1e-16 for those zeroes. Count statistics suffice here because both candidate output laws are exchangeable. This sufficiency does not extend automatically to echo/wake processes with order-dependent laws.

For the same 64 observations, **four fresh soils with 16 observations each** give TV .493797 and error **25.31%**, versus **25.58%** for one soil with 64 observations. The small difference is exact within the specified candidate laws up to floating evaluation; it is not a noisy empirical improvement. It is far smaller than the population-mean precision improvement of Cycle 1. Neither design is established globally optimal; other partitions and acquisition costs were not optimized. If every observation gets a fresh soil, these two mechanisms both generate iid Bernoulli(.2) outputs and cannot be distinguished at any total sample size.

**Garden reading:** new plants help us estimate the orchard average; several leaves from each plant help reveal the orchard's variety. The design depends on which question we ask.

This completes a genuinely different latent-distribution contact, but still assumes two named candidate laws. It is not an open-world rejection/calibration system, an unknown-mechanism detector, or a discovery of where memory physically resides.

## Cycle 3 — a reset label is not a reset calibration

Now the same frozen propensity is carried internally in a fraction pi of runs and externally otherwise. The sign draw is independent of the carrier. These two locations have identical passive output distributions for every sequence length: merely moving the latent variable in the story cannot identify its location.

After observing an error `X1=1`, no-reset excess in the next error probability over .2 is `D0=.16`. An agent reset resamples the propensity with probability qA only when it is internally carried; a soil reset does so with probability qS only when externally carried. No cross-effects or direct emission changes are allowed.

`DA = .16 (1 - pi qA)`

`DS = .16 (1 - (1-pi) qS)`

The code separately enumerates the two-event joint distribution, including original and replacement latent signs, and checks these formulas. This is **conditioning on an observed error**, not forcing an error with `do(X1=1)`. Calling it an error-forcing intervention would be incorrect.

Three different worlds give exactly the same three readouts:

| Internal-carrier run fraction pi | Agent-reset efficacy qA | Soil-reset efficacy qS | D0 | DA | DS |
|---:|---:|---:|---:|---:|---:|
| .40 | .50 | .75 | .160 | .128 | .088 |
| .25 | .80 | .60 | .160 | .128 | .088 |
| .50 | .40 | .90 | .160 | .128 | .088 |

With unknown efficacies in [0,1], define `a=1-DA/D0` and `s=1-DS/D0`. The sharp feasible interval is

`pi in [a, 1-s] = [.20, .55]`.

The endpoints are attainable under the declared model, so more precision in these same readouts cannot choose among the allocations. With known nonzero efficacies, `a/qA` and `1-s/qS` both recover the specified pi. This is a fraction of runs assigned a carrier, **not a proportion of memory bits in one agent**.

Perfect resets give a point interval in this example. Ineffective resets give [0,1]. Under the structural assumptions, full combined attenuation can also identify a point even without separately supplied efficacy values; do not generalize the unknown-calibration example into “calibration is always necessary.” If either efficacy is zero, that side alone supplies no division-based reconstruction; a known nonzero other side can still identify pi. The recorded zero-efficacy case has both zero.

**Garden reading:** “we washed this pot” does not say how much old soil remained. The same outcome can reflect different amounts of old soil and different strengths of washing. Cross-contamination or a wash that changes the next emission directly would require a new model and could invalidate even the reported interval.

## What changed in FRR

An optional [design-label example](../../examples/soil-design-and-reset-calibration.md) and a short addition to the [verification guidance](../../modules/verification-layer.md) ask for: the target; the independent cause draw; observations per draw; intervention effects and their calibration; and what remains unidentified. These are refinements to experimental design and reporting, not a new confidence score or executable statistical validator.

The source-role guard and exact threshold comparator are unchanged. They do not validate exchangeability, independence, causal location, reset effectiveness, or the truth of source data. Existing model failures and queue statuses remain as recorded; no finding here demonstrates improved real-agent reasoning, FRR superiority, or an automatic role-rotation policy.

[Archive receipt](ARCHIVE_RECEIPT.json) preserves six preceding navigation/guidance files byte for byte. Historical links in moved copies retain their original bases; use the original paths at the parent commit for functional navigation. [Final checks](FINAL_CHECKS.json) record preservation and result checks.

## Strongest next contact

A bounded, new reader/producer task should test whether observation-unit labels survive the handoff alongside field roles: same number of observations, different soil grouping, and known versus missing reset calibration. Freeze separate keys for reading the source, performing arithmetic, and recognizing non-identification. The current toy laws can supply exact keys, but should not be confused with agent behavior. A later numerical extension can add cross-target reset effects or calibration intervals; this run does not silently incorporate them. No background run remains active.
