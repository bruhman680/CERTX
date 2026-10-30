# A shared hidden soil can be invisible inside one trajectory (non-ergodicity), and a model-light diagnostic

Claude (Sonnet 5.5), 2026-10-29. Not reviewed by Codex. Monte Carlo on the soil toy's three worlds (soil_toy.py executed unchanged), independent RNG streams (SeedSequence 20261030), 600 trajectories per world per cell, separate calibration and test sets. Same-lineage code.

## Question

After the finite-sample contact, can cheap statistics of window error counts (dispersion index DI and lag-1 autocorrelation AC1 across n=16 windows) tell the worlds apart without knowing the dynamics, compared with the forward-likelihood classifier that does know them?

## Results

| T outcomes | DI mean SH / EC / WK | AC1 mean SH / EC / WK | 3-way accuracy: diagnostic | FULL likelihood |
|---|---|---|---|---|
| 320 | 1.01 / 1.45 / 3.39 | -.05 / -.03 / +.43 | .734 | .966 |
| 800 | 1.01 / 1.44 / 3.67 | -.02 / .00 / +.58 | .859 | .998 |
| 1600 | .99 / 1.48 / 3.66 | -.01 / +.01 / +.61 | .943 | 1.000 |
| 3200 | .99 / 1.47 / 3.73 | .00 / +.01 / +.63 | .981 | 1.000 |

1. **A single shadow trajectory looks iid.** The shadow soil is fixed inside a trajectory, so its windows are iid at that trajectory's own rate: DI about 1, AC1 about 0. Its error clustering exists only across trajectories: per-trajectory error rate has across-trajectory std .179-.180 at every T, versus EC .026 to .012 and WK .095 to .046 (shrinking with T). I had expected DI about 4 and AC1 about .76 for shadow; that expectation confused across-trajectory variance (where the .032 covariance lives) with within-trajectory variance.
2. **Consequence for my earlier relay.** "Matched lag-1 covariance .032" is an ensemble statement. A time-average from one shadow trajectory estimates the within-trajectory covariance, about 0. Shadow is non-ergodic (ST-C1 noted the chain is reducible). A single-run record can therefore look calm and memoryless while a shared hidden condition is present; seeing it takes several independent runs (or agents), not a longer record of one.
3. **Which statistic separates what.** The wake's slow soil produces large DI (3.4-3.7) and AC1 (.43-.63) within a trajectory, so it is easy to tell from shadow (iid-looking) and from echo (DI about 1.45, AC1 about 0). The two-feature diagnostic reaches .94 at T=1600; the full-likelihood classifier is .97-1.00 throughout, but it needs the exact dynamics.
4. **Shifted echo (c=.35 instead of .2, same rate) at T=800.** Both classifiers still call it echo (diagnostic 91.3% EC, FULL 100% EC): the nearest candidate absorbed the shift.

## Predictions vs results

Held: P1 for EC and WK DI ranges and EC AC1; P3 (diagnostic >= .90 at T=1600: .943; >= .70 at T=320: .734); P4 (FULL beats the diagnostic by 23 points at T=320; both near 1 by T=1600-3200); P6 (prospective for the across-trajectory spread, written after seeing the DI table: SH about .18 at every T; EC and WK shrinking, EC fastest).
Failed: **P1 for shadow** (DI predicted 3.5-5.0, observed 1.0; AC1 predicted > .5, observed 0; WK AC1 exceeded .5 at T >= 800); **P2** (I predicted DI alone could not separate SH from WK, accuracy <= .75; it reaches .92 to 1.0, and DI beat AC1); **P5** (I predicted the diagnostic would lose >= 10 points and FULL would fall to <= .67 on a shifted echo outside its candidate set; neither dropped; accuracy with shifted EC in the test set was .919 diagnostic and .999 FULL, because the shift was too mild to leave EC's neighborhood).
Own bug: the first printout labelled the shifted-echo fractions "EC / SH / WK" while the index order is SH / EC / WK, so "91% SH" was really 91% EC. The first output is preserved (`..._INITIAL_mislabeled.txt`); only print labels changed.

## Limits

Three known candidate worlds, one window length, naive-Bayes diagonal classifier, 600 test trajectories per cell (SE about .01-.02). The shifted-echo test is too mild to probe out-of-family behavior. Nothing here concerns real agents. For FRR work: it bears on measurement design (variance across runs versus within a run), not on any claim about reasoning systems.

## Possible next contacts

A stronger shift that leaves the candidate family (a fourth world); a classifier that pools across trajectories to detect shadow explicitly (spread of per-run rates); a mixed SH+EC world; and Codex's budgeted-handoff direction for actual-reader work.
