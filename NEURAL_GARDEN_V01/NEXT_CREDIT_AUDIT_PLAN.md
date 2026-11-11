# Independent audit precommit — credit assignment versus ecology

**Frozen before reviewing any NEXT_CREDIT outcome table.** This is an adversarial follow-up to `NEXT_CREDIT_PLAN.md`, not a replacement for its predeclared 9700–9711 experiment.

## Primary evaluation burden

- Inspect code and recorded SHA-256 hashes before interpreting effects. Look for train/test world overlap, information transferred other than initial theta, changed physics, changed action-selection mode, and baseline mismatches.
- Validate seven neural arms against the *same* initial learned theta and test-world state for each seed, with stochastic action RNG matched at test start. Observe that later RNG streams can diverge from model decisions; count seed/world as unit of replication.
- Treat the **frozen stochastic original-weight** controller as the primary no-learning control. Evaluate online-minus-frozen outcomes, never mistake online stochastic versus frozen deterministic for a learning effect. Independently evaluate learned weights in identical frozen deterministic evaluation worlds.
- Manual reverse-rescue is a non-learning ecological comparator and cannot be described as a matched learning ablation. Inspect its exact threshold equation.
- Check final mean energy, near-floor occupancy, tail raw energy drift, lower-decile energy, and checkpoint trajectories. A policy winning only on mean energy but losing equity or energy budget does not demonstrate unambiguous garden health.
- Distinguish learning-rule alterations (reward observation, eligibility decay, baseline smoothing) from changes to physical world laws. An effect from changing regrowth schedule is environmental, not a credit-assignment fix.

## Fresh long-horizon challenge reserved before results

If implementation is available and fixed, execute **8 distinct training seeds 9900..9907**, test seeds `training+20000`, an 8,000-tick test horizon and diagnostic frozen evaluation worlds `training+40000`; use unchanged initial parameters and the same perturbation window **tick1001–2000** across arms, unlike a length-scaled perturbation that would make horizon confounded with environmental exposure. Include online baseline, best predeclared credit variation selected exclusively from *9700–9711 development* and a frozen stochastic twin, with manual reverse-rescue and neighbor-gradient controls. Freeze selection before using 9900..9907 outcomes. Also evaluate against a stable no-shift 8,000-tick environment. Any seeds or arms not actually run must be explicitly reported.

**No guarantee of improvement:** A learning rule may create temporary gains, reduce worst-case cell viability, or improve weight-quality diagnostics without ecological improvement. Report such splits, confidence limitations, and do not claim an indefinitely sustainable autonomous learner.
