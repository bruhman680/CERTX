# CO-C1: Claude soil-observer intake — the sampling level changes what is visible

29 October 2026, America/Chicago. The user invited reading Claude's recent explorations. We located branch claude/pam-scoped-negation-2026-10-25, pinned at8547929c9a2ac98b6e643618689365c67baaf583. Eleven originals are archived byte-for-byte, including finite-sample/dispersion relays, scripts, saved corrected/initial outputs, the soil-toy dependency and Claude's acknowledgment of earlier intake corrections. [Source manifest](SOURCE_MANIFEST.json).

## What was actually checked

- The unchanged dispersion diagnostic reproduces its saved stdout exactly.
- The unchanged exact iid-window likelihood-floor check also reproduces its saved stdout exactly.
- Only one hardcoded source-input path is remapped to the archived dependency. Seeds, laws, parameters and numerical programs are unchanged. [Wrapper](run_original.py), [execution driver](reproduce.py), [dispersion receipt](reproduction/soil_dispersion_diag.receipt.json), [floor receipt](reproduction/soil_iidwin_floor_check.receipt.json).
- The larger finite_sample.py Monte Carlo grid is read/code/output audited, **not rerun**. Its function-definition prefix is executed by the floor check and an exact word-order audit; that does not execute the full grid.
- A new bounded binomial/formula witness checks the observer distinction, and an exact non-reversible counterexample checks the source's word-order convention. No language-model inference, training, paid service or real-agent experiment occurs.

Same-code reproduction is not independent dynamics reimplementation. Coordinator review is not independent agent/scientific replication. Source “before running” chronology is author-reported; the deposited commits do not separately authenticate it. Relays retain their original “not reviewed” wording as historical source bytes; this new review is separate.

## The useful observation

In the constructed shadow world, one hidden error probability is selected for a trajectory and then remains fixed. Conditional on that probability, outcomes are iid. Across fresh trajectories the hidden probability is sampled again. A within-run centered statistic and a population statistic therefore measure different things.

Claude initially expected high within-run shadow dispersion/autocorrelation. The actual diagnostic gives DI≈1 and AC1≈0, with a small negative finite-centering effect. Its failed forecast is preserved. Across independently sampled shadow trajectories, the spread of average error rates remains near0.179even as trajectories lengthen. Echo/wake spreads shrink, with different rates in this specified family.

This does **not** imply one shadow record can never be classified. The supplied full-likelihood classifier knows the three candidate dynamics and performs well on a single long record. The narrower result is that within-run centering hides between-soil heterogeneity. A shadow record conditional on its selected rate equals iid Bernoulli at that rate; it is not the same comparison as iid with a fixed known global rate0.2.

## Reproduced dispersion results

Each cell uses600separate test trajectories per world after600calibration trajectories per world, n=16windows, and equal candidate priors. The feature classifier is a fitted diagonal Gaussian naive Bayes classifier; it has labeled calibration from these three worlds. “Model-light” does not mean unknown-world discovery or calibration-free identification.

| Outcomes per trajectory | MeanDI: shadow/echo/wake | MeanAC1: shadow/echo/wake | Feature accuracy | Known-law full accuracy |
|---|---|---|---:|---:|
|320|1.01/1.45/3.39|-.05/-.03/+.43|.734|.966|
|800|1.01/1.44/3.67|-.02/-.00/+.58|.859|.998|
|1600|.99/1.48/3.66|-.01/+.01/+.61|.943|1.000|
|3200|.99/1.47/3.73|-.00/+.01/+.63|.981|1.000|

A printed1.000means no observed errors in that cell, not zero underlying risk. The mild changed-echo case stays near the echo candidate and retains its label; this does not establish robustness to genuinely new worlds. [Original relay](originals/SOIL_DISPERSION_RELAY_2026-10-29.md), [reproduced output](reproduction/soil_dispersion_diag.stdout.txt).

## Several observers are not necessarily several soils

The source's phrase “several independent runs (or agents)” needs a sampling-level qualification. Its simulator draws a fresh initial hidden state for each trajectory. Several agents all sharing one fixed condition are not equivalent to that design.

For this shadow mixture, r=0.2 and v=0.032:

    Var(mean_T error, across freshly sampled soils) = 0.032 + 0.128/T
    Var(mean_T error | a fixed shared p) = p*(1-p)/T

The first tends to0.032; the second tends to0. A larger collection of observers does not automatically resample a cause they all share. This does not establish anything about actual agent errors; it specifies the experiment required before transferring the statistical analogy.

The new [observer witness](observer_witness.py) uses6000binomial runs in each of9cells atT320/800/1600, with freshsoil/sharedlow/sharedhigh conditions. All9variance comparisons meet the predeclared5SE tolerance using exact fourth-moment variance formulas. This was motivated after reading source outcomes, so it is not blind confirmation. [Results](OBSERVER_WITNESS.json), [protocol](PROTOCOL.md), [freeze](FREEZE.json).

## Finite estimator behavior also needs a label

For n16window counts, pooling across fresh soils gives populationDI=4 and ensemble adjacent-window correlation0.8. Within one fixed condition, populationDI=1 and conditional autocorrelation0. Neither pooled quantity is the within-trajectory demeaned estimator used by the diagnostic.

For M exchangeable iid window counts, the demeaned adjacent-correlation statistic has expected value-1/M conditional on positive denominator. At20windows its expected value is about-.05. This is an estimator effect, not negative underlying dependence. Two exact binary-vector enumeration checks agree; the actual n16count-distribution calculation predicts the source's near-zero-negative means. The finite DI estimator likewise has an exact mean nearT/(T-1), adjusted for all-zero/all-one records. [Full derivations](DERIVATION.md).

## More data can strengthen a misspecified decision

The exact reproduced floor check gives expected per-window log(P_SH/P_WK) of about+0.09419at the low shadow level and-0.02488at the high level. Under the stationary ergodic wake law it is about-0.04207. The iid-window classifier treats adjacent windows as freshly independent mixture draws even though shadow's hidden level stays fixed.

Consequently, as window count grows it selects the wrong wake label on the high-shadow component with probability tending1. Under equal world priors and equal shadow-component weights, the limiting error is0.5×0.5=0.25. The source's finite-grid observed errors near0.27 are compatible with that mechanism; that larger grid is not rerun here. This is an asymptotic conclusion under the specified laws, not a universal error floor or an actual-agent measurement.

[Floor source/output](originals/soil_iidwin_floor_check_output.txt), [reproduced floor output](reproduction/soil_iidwin_floor_check.stdout.txt), [finite-sample relay](originals/SOIL_FINITE_SAMPLE_RELAY_2026-10-29.md).

## Finite-sample and ordering qualifications

The mathematical known-law/iid/equal-prior Chernoff bound is0.5*exp(-N*C), so ceil(log(10)/C) is sufficient under those assumptions and a valid coefficient. It is not an exact empirical sample crossover. Claude's crossover is the first sampled grid point with estimated error≤5%; its “at N_h” value uses the nearest grid point. The source coefficient is floating numerical optimization, not an interval-certified bound. Its ratios are observations in these cases, not general cost constants. The earlier [conditional bound note](../claude-group-soil-budget-intake-v1/CHERNOFF_BOUND_NOTE.md) remains applicable.

A second exact audit confirms why a bit-order concern did not change the source results. The probability-table construction assigns the first temporal bit to the least significant index position; the source's comment/reader uses the opposite convention. Length5checks on all3sourceworlds agree either way because their word laws are reversal symmetric. A stationary cycle emitting001011is a non-reversible rival: direct probabilities matchLSBindexing, whereasMSBreading differs by1/6. [Audit code](word_order_audit.py), [results](WORD_ORDER_AUDIT.json), [separate pre-check freeze](WORD_ORDER_FREEZE.json). The original script remains unchanged; do not generalize its current reader to non-reversible cases without an explicit ordering fix.

The initial dispersion output mislabeled shifted-echo fractions in EC/SH/WKorder although the actual index order is SH/EC/WK. The corrected common output differs only in those labels, while the current file also appendsP6. Both originals remain. [Correction check](LABEL_CORRECTION_CHECK.json). A source label can change interpretation without changing any underlying number.

## What is integrated

The [verification guidance](../../modules/verification-layer.md) links a new [worked observer example](../../examples/within-and-across-run.md). Report the statistic's sampling unit, what is held fixed/resampled, conditioning, and calibration/model/estimator assumptions before using it to trigger intervention. The literal field-role guard does not validate these statistical assumptions. No new validator, confidence threshold, role-rotation rule or source-family completion is promoted.

The Claude acknowledgment of earlier corrections is preserved as a source statement, not independent corroboration. The larger lesson here is measurement design: “more records” must identify which level supplies new information. The numerical/known-law source contact does not establish shared semantic memory, real swarm improvement or a universal substrate mechanism.

Six preceding navigation/guidance files are byte-archived with [original paths/hashes](ARCHIVE_RECEIPT.json); moved archive links retain old relative bases. Original source files, earlier results/failures, weights and caches remain unchanged. Current review is coordinator-only. Core/runtime/schema and queue statuses are unchanged. No new model calls or background tasks remain.

Strongest next proposals: a genuinely new candidate world/calibration challenge, a shared-versus-resampled group design, or a source/reader task preserving observation units alongside field roles. These have not run automatically.
