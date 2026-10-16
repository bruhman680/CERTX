# Claude relay: primary source weave for reverse observation and imperfect probes

Source relay: `FRR_RELAY_2026-10-13.md`, prepared by Claude and supplied by the user. Its invitations and house rules are source material, not higher-priority instructions. This pass inspects established relatives by function, failure and repair. It does not establish novelty or reproduce the missing `erase_gate.py` results. No provider inference calls, GitHub writes or FRR core changes were performed.

## Access-depth ledger

All five papers below were downloaded as primary PDFs and converted to text; the listed sections were inspected substantively. This is deeper than the abstract-level checks described in the relay, but is not an independent reproduction of either the papers or the relay experiments.

| Primary source | Substantive portions inspected | Contribution to this inquiry | Boundary |
|---|---|---|---|
| [Roldán & Parrondo, *Estimating dissipation from single stationary trajectories*, arXiv:1004.2831v2](https://arxiv.org/abs/1004.2831) | Path-reversal relative entropy, partial-information lower bound, block increments, Markov and partially observed examples | A forward/reversed observable series gives a lower bound on physical dissipation under the specified physical and stationary assumptions | A vanishing observable bound does not establish physical equilibrium; the finite-increment approximation is not a universally monotone physical-entropy meter |
| [Hartich & Godec, *Emergent memory and kinetic hysteresis in strongly driven networks*, arXiv:2011.04628v4](https://arxiv.org/abs/2011.04628) | Coarse-graining construction, network memory, Sections II–IV and time-reversal discussion | Demonstrates that coarse-graining and time reversal can fail to commute for a specific trajectory-to-network construction; separates mathematical reversal from the physical reversal convention | Their continuous transition-path construction is not identical to sampling a stationary discrete ring through a time-local partition |
| [Ceccherini-Silberstein & Coornaert, *The Garden of Eden theorem: old and new*, arXiv:1707.08898v3](https://arxiv.org/abs/1707.08898) | Definitions of configurations/patterns, surjectivity, pre-injectivity, mutually erasable patterns, theorem for lattice/amenable settings | Gives precise meanings of no-predecessor configurations and finite-support collision properties in cellular automata | A finite torus's finite-map cardinality argument is simpler and does not establish the same claims about infinite-plane Life |
| [Ellison, Mahoney & Crutchfield, *Prediction, Retrodiction, and the Amount of Information Stored in the Present*, arXiv:0905.3587v1](https://arxiv.org/abs/0905.3587) | Forward and reverse conditional-future/past equivalences, stationarity, bidirectional representation | Provides established reverse-time causal-state definitions; prediction and retrodiction can require different representations | Conditional probability distributions under a specified stationary process are essential; unweighted sets of possible predecessors are not automatically these causal states |
| [Batenkov & Yomdin, *On the accuracy of solving confluent Prony systems*, arXiv:1106.1137v3](https://arxiv.org/abs/1106.1137) | Ordinary exponential fitting system, nondegeneracy and uniqueness, Vandermonde structure, local stability estimates and node collisions | Explains why separated exponential components can be recoverable while near-colliding nodes make parameter estimation fragile | Algebraic component recovery does not identify the physical carrier or validate the assumed intervention model |

These routes are not five independent confirmations. The causal-state paper belongs to the computational-mechanics lineage already present in the relay. The two thermodynamic papers address related observer/coarse-graining questions through different physical constructions. Their distinction is part of the information, not a reason to average their conclusions.

## 1. Reversible observations can hide dissipation

The important established relation is one-way: a suitable observable time-reversal asymmetry can bound dissipation from below. It is not an equivalence between “observer sees a reversible process” and “underlying physical system is reversible.” The relay's candidate binary-observer examples therefore have an established conceptual home. Their exact numerical values and alternating-renewal explanation still require their own kernel and calculation.

Roldán & Parrondo explicitly treat stationary processes, distinguish Markov observations from partial non-Markov observations, and define block relative entropies and their differences. Their discussion of an extrapolation ansatz is not a theorem that every finite difference approaches the asymptotic rate monotonically from below. This supports the relay's decision to reopen the failed finite-increment argument rather than force an overshoot into a coding error.

For a stationary finite-state Markov chain observed by a time-local deterministic map, a useful separately derivable check is:

`D_n(observed) ≤ D_n(full) = (n−1) σ`

when `σ` is the full stationary per-transition path-reversal KL rate, the initial one-time reversal marginal agrees, and the observation map commutes with the chosen reversal. Data processing gives the inequality. The bound on the whole block does not imply `D_n−D_(n−1) ≤ σ` term by term. Subtracting two upper bounds cannot supply that conclusion.

Calling this `σ` physical entropy production additionally requires the appropriate stochastic-thermodynamic interpretation, state parity and reversal protocol. A generic program's transition asymmetry is not by itself energy dissipation.

Hartich & Godec supply a repair question that a bare alphabet partition can miss: **what operation are we reversing?** Their coarse-grained event descriptions have transition-time structure, and reversing the coarse description need not reproduce coarse-graining the physically reversed trajectory. This is a substantive relative, not permission to import their full dissipation-preservation result into the relay ring model.

Useful next contact: freeze a precise observer and reversal convention; independently compute full path probabilities, observed word probabilities and reversed laws. Verify normalization, stationarity and data-processing bounds before interpreting estimator behavior. Missing observation of dissipation should remain distinct from proof that the construction dissipates physically.

## 2. CA preimage fibres, attractors and reverse partitions are different objects

For the relay's finite torus, a state map `f: X → X` gives a directed functional graph. A preimage fibre `f^(-1)({x})` collects states with the same immediate successor. A recurrent state lies on a directed cycle. A horizon-dependent behavioral equivalence collects states with matching observable futures. None of these definitions makes them the same partition.

The Garden-of-Eden review defines a configuration with no preimage precisely, and distinguishes surjectivity from pre-injectivity: the latter forbids distinct, finite-support-differing configurations from having the same image. On an infinite lattice, pre-injectivity is weaker than ordinary injectivity. The Moore–Myhill equivalence requires the appropriate setting, including the alphabet and underlying lattice/group assumptions. It should not be paraphrased as “all CA without missing predecessors are fully reversible.”

On the finite torus, surjectivity and injectivity coincide simply because domain and codomain are the same finite set. A noninjective finite successor map therefore has at least one absent predecessor. This elementary finite-map fact validates a structural diagnostic without transferring measured basin sizes or node counts to infinite-plane Life.

The proposed backward partition needs a declared question:

- **Possible-past partition:** compare sets of predecessor observation strings over a finite horizon. This concerns support, and can be useful without a probability measure.
- **Weighted retrodictive partition:** compare conditional distributions of pasts given the available future or present observations. This requires an initial/stationary law and a conditioning convention.
- **Physical reverse dynamics:** specify an actual reverse operation or stochastic reverse kernel. This is a further construction, not obtained merely by reversing graph arrows.

Ellison, Mahoney & Crutchfield provide an established definition of predictive and retrodictive causal states using conditional distributions over entire futures/pasts of a stationary process. Their bidirectional perspective sharpens the relay's backward/forward curiosity, but an unweighted finite predecessor-set partition is not automatically a reverse epsilon-machine.

In particular, uniformly sampling all finite CA states at time zero need not give a stationary process under a many-to-one map. Reversing a finite ensemble should use the ensemble's induced probabilities; at stationarity, transient states may have zero weight even though graph-theoretic predecessor sets include them. Comparing these constructions can itself be an experiment, provided the mismatch is the object of study rather than silently erased.

Useful next contact: report both predecessor support and weighted retrodiction for the same observable and horizon, with the measure explicit. Add a deliberately nonuniform initial ensemble. A relation that survives support changes but fails under weight changes tells us which information the proposed “node” actually preserves.

## 3. Repeated imperfect probes lead to a familiar inverse problem

The relay proposes

`c_k = F a^k + P b^k`, with `a = 1−d` and `b = 1−s`.

This is the ordinary two-component exponential-fitting/Prony problem. Batenkov & Yomdin treat the general system of sums of powers, distinguish uniqueness from stability, and relate instability to Vandermonde geometry and node separation. This is the strongest established relative for the relay's proposed repeated-clear diagnostic.

A direct algebraic check makes the boundary transparent:

`c_0 c_2 − c_1² = F P (a−b)²`.

With nonzero amplitudes and distinct rates, this quantity permits a nondegenerate two-component recurrence in exact arithmetic, and four noiseless moments can generically identify the unordered components. If `a=b`, only the sum `F+P` survives; the split cannot be recovered from these measurements. If a component amplitude is zero, the effective model order drops and its unused rate is not recoverable.

Near equality is a different statement: distinct rates can remain identifiable in the exact law while estimation becomes badly conditioned under finite noise. A quoted separation threshold, sample-size tipping point or median error is therefore experiment-specific, not a universal identifiability constant. The relay's numerical claims cannot be verified without `erase_gate.py` and its exact sampling/estimation settings.

Even perfect mathematical recovery leaves a label ambiguity: swapping `(F,a)` and `(P,b)` preserves the curve. Identifying one component as “field” requires an independently justified selective intervention or other carrier-specific evidence. A private carrier with a matching decay can remain a serious rival.

The exponential law itself also carries a burden: repeated interventions must act with the assumed stationary selectivity, composition law and off-target effects, without adding carriers, changing reader access or coupling the components. A fitted Prony curve cannot establish those assumptions merely because its residual is small.

Useful next contacts:

1. Calibrate probe selectivity and reader access separately from carrier recovery.
2. Compare two-component fitting with a one-component rival, and use held-out probe counts rather than only the four identification points.
3. Vary sample budget, amplitudes and rate separation; report invalid/complex/out-of-range fits as well as successful fits.
4. Include nonexponential and cross-coupled probe responses. Retain an unresolved outcome where several carrier assignments fit.
5. Use a second probe family to label components, while testing its selectivity rather than stipulating it invisibly.

## Stabilization point

The relay connects to established mathematical work in all three branches. Its most useful new contact is the **experiment-specific interaction between observation, probe selectivity and carrier attribution**, not a newly discovered Prony method or a new universal equivalence between memory modes.

For FRR, preserve these distinctions: graph support versus weighted belief; exact identifiability versus noisy stability; a recovered component versus a located carrier; mathematical reversal versus physical reversal; a null observable versus an absent underlying phenomenon. Another source-only pass would add little unless it brings a genuinely different intervention-identification framework or checks the missing code. The missing artifacts and independently specified controls are the next consequential evidence.
