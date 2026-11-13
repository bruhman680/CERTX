# Optimizer-state carryover: bounded exploratory contact

13 November 2026, America/Chicago. This is a new detached numerical protocol, not a reproduction of the original 3,000-tick online audit. It does not run or modify the language-model garden, import remote checkpoints, or train an LLM.

## Question and result

The prior audit transferred policy coefficients (`theta`) into a fresh physical world while resetting the reward baseline and eligibility trace. We asked whether preserving those two additional learner-state carriers changes the direction of its online-versus-frozen comparison.

Across this four-seed, shorter-horizon probe, preserving both carriers did **not** reverse the mean energy disadvantage. Online updates lost to the matched frozen policy on three of four seeds in every arm. Carryover changed individual trajectories and sometimes helped a seed; it supplied no consistent rescue in this contact.

| Initial physical context | Baseline reset, trace reset | Baseline reset, trace retained | Baseline retained, trace reset | Both retained |
|---|---:|---:|---:|---:|
| Fresh test world | −0.001160 | −0.001418 | −0.000516 | −0.001794 |
| Trained physical continuation | −0.003630 | −0.004029 | −0.003530 | −0.005581 |

Entries are four-seed mean final energy differences, **online minus frozen**. Energy is clipped to [0,1]. Every cell in this table has one positive seed and three negative seeds. The table reports a bounded numerical observation, not statistical proof of generally harmful learning.

Keeping both carriers rather than resetting both changed online final energy by a mean −0.000634 in fresh worlds and −0.001952 in physical continuations. The corresponding per-seed effects have mixed signs. In particular, retained state helped seed 12400 but hurt seed 12401 in the fresh context. Those signs make a blanket “resetting the optimizer caused the harm” explanation unsupported here.

## Design and actual checks

The inspected `WelfareGarden` controller uses three policy coefficients per cell, stochastic Bernoulli actions, engineered `reserve_resource` reward with penalty 0.3, and the original numerical environmental equations. It is not the RNN controller described in the branch overview and is not the 135M language model.

Four explicit seeds, 12400–12403, each train a fresh 6×6 world for 300 ticks. We then create two contexts:

- **Fresh:** a new physical world at seed +20000, with trained theta installed.
- **Continuation:** a deep in-memory copy of the trained world, including its physical state and action-generator state.

Within each context we cross baseline retained/reset, trace retained/reset, and online/frozen. Retained values come from the same training endpoint; reset values are zero. The reset happens once at deployment. Online arms subsequently update both state carriers normally. Test length is 1,000 ticks, with regrowth 0.06 in the first/final thirds and 0.055 in the middle third. This totals **64 test worlds, 64,000 test ticks, and 1,200 training ticks**. Seeds, not cells, ticks, or eight factorial copies, are the independent replication units. The two physical contexts share each seed's training endpoint, so they are paired contexts rather than eight independent training replications.

Assertions passed for exact initial resource/energy/theta matching within context, identical initial action-generator state, identical first actions and first physical transitions, and identical final generator states. The latter verifies equal consumption of common random draws, **not** identical actions after policy divergence. Four frozen factorial copies produce identical final physical state and theta despite their different baseline/trace values; these learner carriers are inert while learning is disabled. Frozen theta remains equal to the training endpoint throughout the test. Source hashes match before and after.

`PLAN.json` was written before model execution. `probe.py`, `LOG.txt`, and `RESULTS.json` retain the implementation, all per-seed contrasts, checkpoints at test ticks 1/100/500/1000, source hashes, and platform versions. The plan and results should be read as an exploratory contact selected after the earlier audit, not an independently registered confirmatory study.

## What this narrows, and what remains open

Baseline and trace are real continuity carriers: retaining them changes later updates even with the same starting world, theta, and random draws. Their presence alone does not establish beneficial memory. This contact weakens a simple optimizer-reset-only explanation within this small protocol, while leaving the original longer-horizon cohort untouched.

The two physical contexts differ in initial resource, energy and random-stream position. They are matched **within** context; between-context differences cannot be attributed solely to one physical variable. We do not generalize the result to full-length 10×10 audits, other learning rates/objectives, arbitrary memory systems, or the notebook garden. No uncertainty interval or universal claim is inferred from four seeds.

A more expensive follow-up would preserve the original audit's dimensions and horizons, vary baseline and trace with the same matching checks, and reserve new seeds before reading outcomes. There is no basis here to transplant reward rules, reset policies, or behavioral gates into the language-model garden.
