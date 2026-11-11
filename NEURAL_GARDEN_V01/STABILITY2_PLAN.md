# STABILITY2 — predeclared bounded-update stability probe

## Question
Does restricting how far each neural controller can drift away from its competent pre-trained weights improve **continued stochastic online learning** under a mild reversible resource shift? This specifically tests parameter stability, not an endogenous learned decision about when to learn.

## Paired conditions
- Frozen stochastic weights (radius 0; no updates).
- Unrestricted stochastic online update (current algorithm).
- Online update with per-cell Euclidean radius from initial transferred weights of 0.025, 0.10, 0.40, 1.00.
- A sham restriction: project per-cell weights onto same-radius sphere around **zero** instead of transferred initial weights, only as supplementary mechanical control; it may harm competence by construction and is not a matched-benefit comparator.

Train all identically with `train('reserve_resource',seed,10,1000)`; test each on equal physical state and action RNG at seed+20000, for 3000 steps, same .06/.055/.06 regrowth schedule. Fresh development seeds 10300–10307. Preserve frozen weights, neural state, baseline and RNG matching at initialization. Scalar metrics end energy, floor, tail raw drift, fraction harvest, theta distance; paired wins against frozen and unrestricted. Compare radius behavior rather than claim automatic learning. Independent holdout seeds 10400–10407 not used to select radius.

## Interpretation burden
A bounded optimizer can win against unrestricted online updating by limiting catastrophic drift; it cannot establish autonomous learning, environmental awareness or advantage over doing no updating. A useful online adaptation claim requires an advantage over the strong same-mode frozen controller on held-out seeds and preferably a changed-world regime where freezing is weak. Predeclare no global winner; negative outcomes remain in report.
