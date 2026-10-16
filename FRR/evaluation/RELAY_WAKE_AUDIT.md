# Wake relay: reproduction and reset preparation

Original `wake.py` is preserved under [the source archive](../lineage/sources/claude-relay-2026-10-15/). It ran unchanged; [original output](results/relay-wake-original.txt), [extension](../experiments/relay_wake_audit.py), and [extension results](results/relay-wake-audit.json) distinguish reproduction from new tests. This is a four-state stochastic toy, not a physical or transformer-memory experiment.

## What reproduces and what changes

The first post-reset visible total-variation difference is .30 for every tested h. Retaining different hidden environments changes future visible laws after resetting the visible coordinate. That is a concrete environmental-persistence contact.

The source header's proposed decay rate `max(1-h,.45)` is not a general coupled-chain rate. At h=1, the joint chain's subdominant eigenvalue is .6438251502, rather than .45. The latter comes from a naively averaged visible chain and misses feedback. The computed spectra and full propagation are saved in the results.

At h=0, the signed visible difference at times 1,2,4,8,16,32 is .30,.255,.1189875,-.01052062,-.06457468,-.07052796. Consequently visible TV can fall and then rise. Joint TV stays one: the frozen environments have disjoint support. This does not violate data processing. A later visible read can expose information that remained in the joint state. Every tested joint-TV sequence is nonincreasing.

Both h=0 and h=1 have rank four for the finite 15-by-15 word Hankel matrix using prefixes/suffixes through depth three. Exact rational elimination with the intended decimal kernel confirms the numerical rank. Rank alone does not separate these endpoints. It also must not be equated with predictive-state cardinality.

The source's full-history B and M10 coincide throughout its displayed horizons because the available word never exceeds M10's history capacity and both use the same initial belief. Their agreement is not independent corroboration. More history need not reduce risk under a mismatched reset prior: the source's selected fixed-environment preparation can favor a shorter, differently mismatched predictor.

## Observing zero versus setting zero

A naturally observed `y=0` implies the stationary conditional prior `pi(e|y=0)`. Independently forcing y to zero while retaining a stationary field marginal implies `pi(e)`. These are different preparations. The original fixed-e experiments are defined experiments; their reader prior must be stated before calling the reader Bayes-optimal.

The extension explicitly tests the second preparation. At h=1, the conditional prior is [.7857143,.2142857], while the retained marginal is [.5894737,.4105263]. Using the conditional rather than interventional prior adds .00969694 nats of one-step expected oracle KL risk. The excess agrees with `KL(q_do || q_cond)`. Across h=.02,.05,.2,.5,1 the tested excesses are all nonnegative. These values concern this declared preparation, not every reset protocol.

## Next discriminating contact

Compare natural conditioning, independent visible resets, fixed-environment resets and joint resets under explicitly matched reader priors. Record both full joint distinguishability and visible distinguishability. This separates persistent information, observer access and prior mismatch without requiring a new universal memory metric.

## Later controlled contact

[RR1](RESET_READER_STUDY.md) subsequently compared five preparations, age-aware suffix/full readers and the older stationary one-symbol baseline. The source-kernel reversal against the stationary baseline does not survive as a pure history-length effect when the assumed preparation and elapsed-time law are held fixed. A small controlled reversal occurs in another prespecified kernel. This narrows the old comparison without changing its numerical output or establishing actual-agent transfer.
