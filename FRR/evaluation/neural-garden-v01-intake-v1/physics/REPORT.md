# Physics and objective separation: independent bounded checks

12 November 2026, America/Chicago. Source pinned to CERTX commit `3204c81ebc6922d66b0ae2623ee83d629f11f3b8`, directory `NEURAL_GARDEN_V01`. Exact Git blob bytes for seven inspected files are verified in SOURCE_PROVENANCE.json. This review did not load remote pickle checkpoints, run a pretrained language model, advance either live garden, or modify their laws/state.

## What the base world actually does

For cell i, let R be resource, E energy, N the four-neighbor mean on a toroidal lattice, and A a binary harvest action. The source implements synchronous updates:

`R' = clip(R + .08(NR-R) + .06(1-R) - .18 R A, 0, 1)`

`raw = .25 R A - .063 A - .022`

`E' = clip(E + raw, 0, 1)`.

On legal resource states, the unclipped resource update already remains in [0,1]: it is `.86R + .08NR + .06` without harvest and `.68R + .08NR + .06` with harvest. Resource clipping therefore does not change this equation on the legal domain. Toroidal diffusion conserves the global resource sum; regrowth and consumption do not.

The environment rules are distinct from the controller rules. Every fixed-position cell has a seven-feature observation, twelve recurrent hidden units, its own 266 neural parameters, a binary action head, and a resource-prediction head. The simulation has separate global initialization and action RNG streams. Cells are neither general language models nor unrestricted algorithm-writing agents. The base Garden has no birth, death or movement; separate extension files may add mechanisms, so this is not an assertion about every variant on the branch.

Learning is also explicitly designed: a next-resource prediction gradient, a clipped one-step policy-gradient-like energy signal, a running reward baseline and truncated recurrent updates. The policy receives realized **clipped** energy change. These are objectives and update rules imposed on the cells, not physical laws discovered by them. Thus the project is Conway-like in local, synchronous, inspectable state transitions, but it does not demonstrate absence of designer-imposed neural behavior/learning structure.

## Exact observation traps

Let p=mean(A), y=mean(R A)/p for p>0, and z=E+raw. Then:

`mean(raw) = p(.25y-.063)-.022`

`mean(E'-E) = mean(raw) + mean(max(0,-z)) - mean(max(0,z-1))`.

At the energy floor, unpayable losses are discarded. A near-zero clipped-energy slope can therefore conceal a continuing negative raw budget. Clipping changes both the plotted metric and the learner's reward signal. This is a law-specific mechanism; it is not a universal analogy proving that language-model reasoning has the same conservation law.

Action quantity alone also loses a consequential relation:

`mean(R A) = mean(R) mean(A) + Cov(R,A)`.

The instantaneous raw advantage of harvest over rest is `.25R-.063`, crossing at R=.252. This is a one-step diagnostic, not an empirically learned threshold or a long-horizon optimum.

Under the restricted homogeneous stationary constant-rate approximation, `R*=.06/(.06+.18p)`. The derived maximum raw energy drift occurs at p=.3306825607413298, R*=.5019960159204453, and is **−.0013326693200742222**. This excludes nonnegative drift only within that approximation/class; resource-dependent and spatial policies are not ruled out.

The resource predictor does not receive current A, which is sampled after the hidden state. Conditional on its pre-action information and propensity p, the target has action-randomness variance `(.18R)^2 p(1-p)`. Lower experienced prediction MSE can follow changed resource levels/action entropy as well as predictor changes. On-policy MSE, held-out prediction, action quality and population energy therefore need separate measurements.

## Executed independent checks

`reproduce.py` uses inspected base Garden source and an independently written ledger/transition calculation. RESULTS.json retains all rows.

- **Eight base runs:** four new seeds 12001/12017/12029/12043, learned/frozen pairs, size8,300 ticks each. Energy, resource and covariance identities held to maximum residuals 2.43e−17,2.52e−17 and1.74e−17; diffusion-sum error was6.51e−17. Frozen tensors remained unchanged. All resource/energy values stayed bounded. Learning runs had final mean energy .00979–.01368 versus frozen .02389–.03289 in this small probe. This is a scoped negative result, not a precision estimate or new universal learning conclusion.
- **Four matched-count pairs:** fresh seeds12101/12117/12129/12143, size8,2000 ticks. An authored resource/energy-targeted rule was compared with a random-location counterfactual receiving exactly its action count each tick. Counts matched at every tick. Targeted final mean energy was .64562–.66190; shuffled was .11193–.13375, paired gaps .51951–.54978. This independently supports the placement/feedback mechanism on smaller worlds/new seeds. Both policies are authored controls, not learned discoveries; the long-run gap includes diverging state feedback, not an isolated instantaneous coefficient.

These are16 unique run conditions and18,400 unique run-ticks. They are **not** the source's72 size16/10,000-tick runs. Nor do they reproduce the published THEORY2 table, whose script imports a derived WelfareGarden and a trained reserve-resource controller. The exact identities transfer to that variant only where its stated transition equations match.

Execution accounting is preserved: attempt1 completed calculations but failed during metadata export on a __pycache__ directory; the file-only export fix did not change physics. Attempt2 succeeded with intake-added final blank lines. We then verified pinned Git blob bytes, removed only those added newlines, and repeated identical fixed-seed checks for final RESULTS.json. These repetitions are not counted as extra independent samples. ATTEMPT1_EXPORT_ERROR.stderr and ATTEMPT2_TRAILING_BLANK_RESULTS.json retain the earlier outcomes.

## What use transfers to our computational garden

Transfer the **measurement discipline**, not the harvest reward: separate legal operation, intended task result, raw state change, observed/clipped metric, policy update, and longer-horizon consequence. Observe correlation between where/when an action is applied and its effect instead of treating action count as an achievement. A plateau or repeated output alone is not a stability or emergence certificate.

Do not transplant the resource constants, neural objective, harvest threshold or a welfare score into the free language-model garden as a supposed fundamental law. No current result shows these controllers improve language reasoning, that the language-model interface has a comparable energy budget, or that binary harvest ecology exposes all capabilities of a pretrained model.

Strong next contacts are action-aware forecast controls, matched-count targeting under genuinely held-out physical regimes, and explicit separation of raw deficit, floor forgiveness and per-cell distributions. Any proposed online-learning safety gate must itself be compared with frozen and equally complex sham controls. Those are prospective here, not additional executed experiments.
