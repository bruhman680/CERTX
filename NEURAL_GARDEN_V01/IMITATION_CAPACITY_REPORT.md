# Distinguishing neural representation from autonomous ecological learning

**Status:** Exploratory supervised-control probe, not a new independently validated neural-learning result. These pilots are *not* part of either 100-run batch or the separate 1,000-run matched experiment.

## Hypothesis

Our original cells may have an adequate local neural architecture but a poor *teaching signal*: current action selection is optimized with immediate clipped energy rewards, which can encourage resource depletion. Test whether the **same per-cell hidden network** can learn conditional decisions when an external teacher explicitly supplies the known `resource > .55` action target.

## Intervention

`imitation_garden.py` preserves the v0.1 world transition constants exactly and retains independent neural weights for each cell. It changes **two learning details**:

1. Prediction becomes **action-conditioned** on the *current* sampled harvest action via a learned per-cell coefficient.
2. Policy learning uses the external label `harvest iff current resource > .55` rather than self-discovered reward maximization.

This is a capacity probe, not autonomous reinforcement learning or discovery of the .55 threshold. The label comes from the earlier non-neural pilot. Cells may still stochastically deviate from the teacher during training and ordinary deployment.

## Pilot A: continuously supervised, stochastic actions

Script: `evaluate_imitation.py`; raw: `imitation_pilot_results.json`. Five exploratory seeds 740–744, size 16, 600 ticks, original world laws and matched seed sets for three arms.

| Arm | Average energy at tick 600 |
| --- | ---: |
| Original neural learner | **0.00884** |
| Supervised neural imitation | **0.22783** |
| Fixed deterministic resource threshold .55 | **0.48047** |

The supervised learner's **policy classification accuracy** on the teacher's binary target reached an average **0.8656** at tick 600, yet realized energy remained well below the deterministic teacher. Its classification accuracy does **not** mean its *sampled* actions follow the teacher exactly; residual stochastic exploration can still lead to many off-target harvests.

## Pilot B: teach for 250 ticks, freeze, deploy for 600

Script: `imitation_training_probe.py`; raw: `imitation_training_probe.json`. Five **different** exploratory seeds 760–764 per learning-rate setting. During training, actions remain sampled. At deployment, network learning is frozen and actions are deterministic (`propensity>=.5`), so there is no ongoing teacher access in the 600 deployment ticks.

| Imitation learning rate | Mean deployed energy at tick 600 | Mean contemporaneous classification accuracy |
| ---: | ---: | ---: |
| .22 | 0.46123 | 0.30859 |
| .50 | 0.49510 | 0.42031 |
| 1.00 | 0.50465 | 0.38984 |

Here observed classification accuracy **fell sharply** during deterministic deployment even as energy remained high, indicating that teacher imitation accuracy alone is not a reliable indicator of ecological success. The deployment scores cannot be directly compared with Pilot A's fixed-threshold result because their seeds and training/deployment timelines differ. The three rates were explored posthoc; these are descriptive pilots without fresh independent confirmation.

## What follows—and what does not

The existing neural architecture appears **capable of learning useful resource-sensitive behavior from supplied labels**, and switching to action-conditioned prediction closes an identified information gap. The pilots do **not** isolate which of these changes causes which effect, prove representational sufficiency in all conditions, or show autonomous discovery. The deployment accuracy drift suggests policy behavior, state distribution, and evaluation metrics need further disentangling.

The next *confirmatory* study should freeze one candidate learner, add a genuine same-seed .55 baseline with identical timeline, and separately ablate: (a) action conditioning, (b) teacher supervision, and (c) deterministic versus stochastic deployment. Long-horizon and unseen-environment tests should follow before claiming learned adaptive ecology.
