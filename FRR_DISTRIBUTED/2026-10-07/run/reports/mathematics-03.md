# Mathematics 03 — Approximate lumpability needs a stability bridge

**Status:** mathematical derivation and source-repair recommendation, not empirical validation. The surviving relationship is precise: a uniformly small one-step abstraction defect bounds finite-horizon predictive error; horizon-independent error additionally requires stability. An abstraction score alone supplies neither stability nor a causal location for its failure.

## Definitions and exact assumptions

Let X and S be finite sets, P an X-by-X row-stochastic micro-transition matrix, and q:X→S a surjection. Define the deterministic projection kernel Q(x,s)=1{q(x)=s}; distributions are row vectors. For probability measures μ,ν on a common finite space, TV(μ,ν)=½∑|μ−ν|. Select a row-stochastic macro kernel K on S. Its one-step intertwining residual is

ε = max_x TV((PQ)(x,·),(QK)(x,·)).

This compares two routes with common source X and target distributions on S: evolve then project, or project then evolve. It is a commuting-square defect, not a commutator on one space. The assumptions include the actual state being Markov in X, fixed P,Q,K, and uniform control over every microstate claimed admissible. A restricted set suffices only if transitions and interventions remain in that set.

The source's pairwise fiber defect is

δ = max_{q(x)=q(y)} TV((PQ)(x,·),(PQ)(y,·)).

For any K with residual ε, δ≤2ε. Conversely select one representative x_s per fiber and set K(s,·)=(PQ)(x_s,·); then ε≤δ. Any convex mixture of projected transition rows inside a fiber also yields ε≤δ, by convexity. Thus δ=0 is exactly strong lumpability, while an approximate δ must be connected to a specified K before it certifies a prediction. The optimal K may improve the constant; no optimality is assumed here.

## Finite-horizon guarantee and its proof

For initial micro law μ and initial macro law ν, put e₀=TV(μQ,ν). Then, for every integer n≥0,

TV(μPⁿQ,νKⁿ) ≤ min{1,e₀+nε}.

To see this, replace one projected micro step by K: for every micro law λ, convexity gives TV(λPQ,λQK)≤ε. Markov kernels do not increase TV. The triangle inequality therefore gives e_{n+1}≤ε+e_n, and induction completes the proof. This is a marginal-law guarantee, uniform over initial distributions under the stated global residual.

It also bounds a declared scalar observation f:S→R with finite range r=max f−min f: the expectation error is at most r·min{1,e₀+nε}. A small TV error does not control an unbounded reward or a relative error near zero. Micro rewards erased by q need a separate approximation assumption.

With matching initial projected laws, sequential maximal coupling gives a stronger *path* statement: the law of (q(X₀),…,q(X_n)) differs in TV from the K-chain path law by at most 1−(1−ε)ⁿ≤nε. Conditional on any positive-probability visible history, the next projected micro law is a mixture of rows in its current fiber; its discrepancy from K is ≤ε. At each still-matched coupling step, mismatch probability is therefore ≤ε. This supplies a path guarantee without assuming the projected process itself is Markov. Checking only one final marginal does not supply this premise.

## Contraction supplies a uniform error bound

Define the Dobrushin coefficient α(K)=max_{s,t} TV(K(s,·),K(t,·)). If α(K)<1, then TV(aK,bK)≤α(K)TV(a,b), so the same proof sharpens to

e_n ≤ αⁿe₀ + ε(1−αⁿ)/(1−α), capped at 1.

The denominator is essential. “Small residual” is meaningful relative to the contraction gap 1−α, not in isolation. If μ_*P=μ_* and πK=π, stationarity gives TV(μ_*Q,π)≤min{1,ε/(1−α)}. These are marginal and stationary guarantees, not uniform closeness of whole paths: repeated small discrepancies can remain detectable in long trajectories even when marginals mix.

One-step α=1 does not prove absence of stability. If α(Kᵐ)=β<1 for some m, apply the preceding finite-horizon argument to Pᵐ,Q,Kᵐ, whose residual is ≤min{1,mε}. At block times the recurrence is e_{(j+1)m}≤mε+βe_{jm}; intermediate steps add at most (m−1)ε. This is a sufficient, potentially loose repair. No contraction is inferred from a spectral threshold or an empirical entropy cutoff.

## Explicit failure witnesses

Even a uniform residual cannot provide an uncontrolled all-horizon guarantee. Take identity projection Q on {A,B}; K is identity; P moves A to absorbing B with probability ε each step. The uniform residual is ε, but from A the discrepancy at n is 1−(1−ε)ⁿ, tending to one. Here α(K)=1. With ε=.001 and n=1000 the error is about .6323. This witness concerns prediction of a selected approximate K, not loss caused by merging states; it cleanly isolates the missing stability assumption.

Sampled residuals are weaker still. Let q(a)=q(b)=A and q(c)=B. Let a stay at a, b move to c, and c stay at c. A fitted macro model K(A,A)=K(B,B)=1 has zero residual on trajectories initialized at a, yet unit one-step error after an admissible intervention setting b. The true uniform ε and δ both equal one. Training-distribution averaging can hide precisely the states needed by a counterfactual claim.

## Concrete source repair, rival, and evidence scope

Add a bounded guarantee box after the FRR v0.5 “Equivalence and Effective States” paragraph, and after FRR_FIBER_MEASUREMENT_PASS.md's d_i(t) definition: record P,Q,K, uniform ε or pairwise δ, admissible initial/intervention domain, fixed target, horizon H, and the bound Hε. Permit horizon-independent wording only with an explicit contraction certificate and denominator. Keep adequacy scores separate from their behavioral guarantees. Refining the grouping while holding the observation fixed is a possible repair; refining both changes the question.

A serious rival to “missing hidden memory” is ordinary macro-model miscalibration, changed intervention dynamics, or a rare untested state. Conversely a history-conditioned or state-plus-field model may be more appropriate than forcing a single Markov K. Those alternatives must be compared on the same declared prediction target. A failed square cannot choose among them.

Inspected sources: immutable NOW.md; recovered FRR v0.5 seed/equivalence/residual sections; CONTINUATION_HANDOFF.md and RECOVERED_CODEX_HISTORY.md; RECOVERY_NOTE.md; the October 5 field-wakes note; screenshot assembled record and inferred boundary README in bounded excerpts; FRR_FIBER_MEASUREMENT_PASS.md's definitions and refinement discussion. Their shared lineage is not independent evidence. No original scripts or external literature were executed/searched here; the witnesses and bounds above are explicit finite-state deductions. No historical source was edited, and these recommendations are not implemented.
