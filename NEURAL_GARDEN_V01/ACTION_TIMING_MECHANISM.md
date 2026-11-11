# Action timing versus immediate reward: a local diagnostic

The v0.1 original cell's one-step **raw** energy change is

`delta_E = .25*resource*action - .03 - .055*action + .008*(1-action)`.

The instantaneous payoff difference, harvesting (`action=1`) minus resting (`action=0`), is therefore

`advantage_1step(resource) = .25*resource - .063`.

It crosses zero at `resource = .063/.25 = .252`. A policy that optimizes *only* this one-step raw energy budget would harvest whenever `resource > .252`. Such immediate gain ignores that harvesting simultaneously removes resource from future steps; this provides a plausible mechanism for over-extraction, not a claim that the actual neural network learned a crisp .252 threshold.

The v0.2 stewardship learner uses an explicitly hand-chosen reward augmentation `lambda * delta_resource`, where `lambda=.65` and one harvest consumes `.18*resource`. Holding the other world inputs fixed, this changes the immediate reward difference to

`advantage_stewardship(resource) = (.25 - lambda*.18)*resource - .063 = .133*resource - .063`,

with crossing near `resource=.47368`.

The tested non-neural threshold `.55` is stricter still. It was informed by exploratory results and is not a derived mathematical optimum. In both neural variants, state transitions, recurrent coupling, stochastic actions, clipping of realized energy rewards, resource diffusion, and temporally delayed effects mean these one-step values are **diagnostic comparisons**, not measured neural decision boundaries.

## What to measure in the 1,000-run matched test

Compare actual action–resource covariance, raw (pre-clipping) energy drift, resource levels, floor and ceiling occupancy, and long-horizon energy under identical seeds/world laws. If a learner's energy improves merely because it takes fewer actions, examine whether that action reduction is *appropriately targeted* to low-resource states. This makes the distinction between behavioral adaptation and mere caution observable.

Finally, a resource-state-conditioned hand rule may work without using a neural network. Showing the latter is beneficial requires an action-aware neural comparison and generalization under unseen perturbations; prediction MSE on each learner's own experienced trajectory is insufficient.
