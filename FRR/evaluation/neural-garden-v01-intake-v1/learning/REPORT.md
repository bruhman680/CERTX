# Learning and policy-memory review

12 November 2026, America/Chicago. Pinned source: CERTX commit `3204c81ebc6922d66b0ae2623ee83d629f11f3b8`, `NEURAL_GARDEN_V01/`. This review reads the implementation, recomputes retained JSON summaries, and reproduces one published seed from each of two protocols. It does not advance either canonical garden, load remote pickle checkpoints, train an LLM, or merge source into the notebook garden.

## Strongest supported findings

- The reserved online-update audit's twelve per-seed rows reproduce its summary exactly: online updating loses to the frozen stochastic comparator on all twelve seeds, with mean energy difference about **−0.01280**. Both modes use stochastic actions, so this comparison fixes the earlier online-stochastic versus frozen-deterministic mode confound.
- A full rerun of reserved audit seed **9800**, including fresh deterministic weight-transfer evaluations, matches every numeric retained row **exactly** on this CPU/NumPy environment. This is reproduction of an already published seed, not a new held-out confirmation.
- Recomputing all eight STABILITY2 holdout rows confirms every nonfrozen radius arm loses to the frozen comparator on every seed. A full rerun of holdout seed **10400** matches every numeric retained row **exactly**. Tight bounds reduce damage relative to unrestricted updating; approaching a frozen policy is not evidence of beneficial learning.
- Recomputing MEMORY2_SAFETY's held-out scores/floor/energy from its individual test rows matches the reported summaries. Its mild-regime composite advantage is tiny and the safety selector does not provide an unseen-world floor guarantee. No memory-bank simulator rerun was performed here.

These results remain local to engineered objectives, controllers, horizons and a single simulator generator. The two original twelve-seed cohorts are disjoint within-generator checks, not twenty-four independent scientific laboratories. Cells and ticks are correlated and are not the replication units. MEMORY2's independent unit is the six training cohorts; the two deployment worlds per cohort are nested evaluations.

## The model being updated is different from the overview's recurrent cell

The original `garden.py` defines the recurrent neural-cell prototype. The reviewed later experiments inherit its world/storage helpers but replace the acting policy with `EnergyAwareGarden`/`WelfareGarden`:

`x = [3(resource−0.5), 3(energy−0.5), 1]`

`p = sigmoid(theta · x)`

Actions are stochastic Bernoulli harvesting, or a separately selected deterministic threshold at `p >= 0.5`. Each cell has three theta coefficients; resource sensitivity starts near **4**, energy sensitivity starts at zero, and bias near zero. That is a designer-provided resource-sensitive inductive bias. The inherited original recurrent hidden state and original recurrent matrices are not used in this acting step.

The learner updates an eligibility trace `trace <- .97 trace + (action−p)x`; theta change is `.04(reward−baseline)trace`, clipped per component to ±.02, with theta box limits. The baseline is an EMA with coefficient .005. These are explicitly designed plasticity and optimizer rules. They are not environmental conservation laws or independently discovered preferences.

## Environmental consequences and training objective are separate

With current resource r and binary harvest a, world resource changes by diffusion, regrowth and consumption. Raw energy change is:

`raw = .25*r*a − .03 − .055*a + .008*(1−a)`

Energy is then clipped to [0,1]. The selected `reserve_resource` objective changes the learning reward by subtracting `.3*max(.18−next_energy,0)` and adding `.3*(next_resource−resource)`. Those latter terms do not alter the physical resource/energy equations; they alter the controller's training incentive.

Consequently this research explicitly governs an observation space, binary action space, initial policy bias and update objective in addition to governing the world. It is not a direct example of unconstrained model behavior under only simple environmental laws. Its value for the user's Conway-inspired aim is chiefly that those layers can be separated and tested honestly.

## A consequential continuity qualification

`NEXT_ONLINE_probe.py` first calls `train()`, which returns **only theta**. It then constructs new test worlds with a different seed and installs that theta. Construction initializes fresh trace and baseline arrays; the training-world physical state, eligibility state and reward baseline are not continued into the test world. Online and frozen test arms start matched to each other, and their subsequent divergence is meaningful under this protocol. But 'continued online learning' here is **transferred weights plus updates in a newly initialized test setup**, not exact uninterrupted continuation of the full learning system.

This qualification does not invalidate the matched negative result. It limits generalizing that result to the Living Garden's full-state checkpoint continuation or to an optimizer whose learned baseline/trace state is preserved. Fresh optimizer-state initialization is a plausible additional experimental factor, not a demonstrated cause of the observed harm.

The same distinction applies to `MEMORY2`: protected and mutable banks contain **theta arrays**, and `assess()` deploys them in fresh deterministic worlds. Validation runs off-world trials and chooses a snapshot using an investigator-specified score and margin. A 'protected memory bank' in these studies is policy-parameter retention and external model selection, not episodic recall, the notebook garden's files, its transcript, or an agent's internally learned confidence.

## What can usefully transfer to the notebook garden

The transferable practice is methodological: distinguish weight updates, retrieval, context assembly, physical consequences and observer evaluation; preserve a protected reference; compare decoder/action modes fairly; inspect raw state transitions before clipping; and keep deployment objectives distinct from reported scores.

The energy reward, binary harvest policy, trust radius and validation gate should **not** be transplanted as behavior rules for the language-model garden. That garden currently has fixed pretrained weights, a different action language, file state and bounded conversation. There is no evidence that these numerical outcomes predict its response length, tool use, error correction or emergence.

## Checks, provenance and limits

`ROW_AUDIT.json` records the data recomputations and source-hash checks. `BOUNDED_REPRODUCTION.json` retains the two rerun rows and exact maximum differences. `checks.py` makes no checkpoint load calls; inspected source imports define classes/functions, and the reruns create fresh synthetic worlds. `CHECKS.stderr` preserves an initial failed source-identity check: the intake writer had added one terminal newline. `restore_source_bytes.py` recovered each source only when its exact Git blob ID matched, and `COPY_BYTE_CORRECTION.json` records the byte correction. The successful rerun is in CHECKS_RETRY.*. This was an intake-copy issue, not upstream source drift or an experimental repair.

The full original cohorts and memory-bank training have not all been rerun. We did not independently establish historical preregistration timing or inspect every report in the large branch. 'Independent audit' in those source reports means separately assigned executions/seeds within the project, not cross-institutional replication. No proposed follow-up is silently an executed result.

## Best next discriminating question

A matched continuation test could preserve theta **and** baseline/eligibility state versus resetting those optimizer carriers, while holding the initial physical world, objective, action mode and evaluation burden fixed. This would test whether a restart-associated carrier reset contributes to the negative transfer result. It is a new prospective experiment; it was not run in this review. It would still not establish general safe online learning or prescribe a new control layer for the notebook model.
