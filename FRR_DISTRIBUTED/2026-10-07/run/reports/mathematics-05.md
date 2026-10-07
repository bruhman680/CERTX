# Predictive sufficiency versus intervention lifting

Worker mathematics-05, 2026-10-07. This is a mathematical clarification and source inspection, not a new empirical reproduction. The garden results cited below are inherited from experiments-03. No originals were edited or remote operations performed.

## What predictive sufficiency actually establishes

Let X be a finite microstate space, S a finite effective-state space, q:X→S a surjection, and P₀ a passive transition kernel. Write q_* for pushforward of distributions. Exact passive Markov closure means that a kernel K₀:S→Prob(S) exists with

q_*P₀(x,·)=K₀(q(x),·) for every x∈X.

This is equivalent to equality of projected one-step laws for every pair in each fibre. The kernel is then uniquely determined, and induction gives closure at every finite horizon for the projected Markov process. This implication requires the actual microprocess to be Markov on X and the criterion to compare transitions into every effective-state block. Equality of one observable at one horizon, or equality of conditional averages under a selected initial distribution, does not supply these premises.

For a weaker predictive target, define B_H(x) as the law of a specified observation sequence through horizon H. Sufficiency only requires B_H to be constant on q-fibres. It says nothing about changed transitions. This is the distinction the FRR candidate already makes at lines 882–894; the repair is to formalize the intervention family rather than strengthen the rhetoric of autonomy.

## Three separate conditions: descent, lifting, and availability

For each micro-action a, let D_a⊆X be its admissible domain and P_a its transition kernel on D_a. The deterministic case uses T_a:D_a→X. A fixed action has a well-defined effective consequence on an effective domain D̄_a precisely when:

1. D_a=q⁻¹(D̄_a), so applicability is constant within each fibre;
2. q_*P_a(x,·) is constant over x∈q⁻¹(s), for each s∈D̄_a.

These conditions are necessary and sufficient for an everywhere applicable effective kernel K_a on D̄_a together with fibre-invariant availability. If availability is deliberately ignored, condition 2 alone gives descent on the applicable representatives but conceals which microstates can execute the action. This is not a complete control abstraction.

The typed square is X —P_a→ Prob(X), with vertical maps q and q_*, and bottom map K_a:S→Prob(S). Its equality q_*P_a=K_aq is defined only on D_a. A defect in this square diagnoses inconsistent projected consequences; it does not identify the causal location of the missing distinction. No cube is needed here.

Conversely, prescribing a macro-action K:S→Prob(S) does not ensure a micro-implementation exists. A lifting selector λ_s∈Prob(q⁻¹(s)) chooses an initial representative; it does not by itself implement K. One must also specify an admissible micro-control policy π(a|x,s), supported on actions available at x. With that policy, the implemented macro law is

K^{λ,π}(s,·)=Σ_{x∈q⁻¹(s)}λ_s(x)Σ_aπ(a|x,s)q_*P_a(x,·).

Exact implementation means this law equals K(s,·). For finite spaces, if the selector and state-dependent randomized policy are both freely selectable, a solution exists exactly when K(s,·) lies in the convex hull of all available projected laws q_*P_a(x,·) in that fibre. If λ is prescribed, the attainable set instead is the weighted Minkowski sum of the convex hulls available at each x; a positive-weight representative with no legal action defeats implementation. Constraints on resetting, observing x, or policy dependence narrow these sets further. Existence in an unconstrained mathematical hull is not operational availability.

With π fixed, independence from every possible λ is equivalent to constancy of its induced projected law across the fibre. Restricting admissible λ weakens that condition: only their integrated laws need agree. Declaring one selector makes an intervention well-defined relative to that selector, but does not establish selector-independent causal standing. In the deterministic prescription m:S→S, robust implementation by one available micro-action requires q(T_a(x))=m(q(x)) for every representative, as well as fibre-invariant availability.

## A finite counterexample

Take X={(0,0),(0,1),(1,0),(1,1)}, S={0,1}, q(s,z)=s. Passive evolution is identity. Every pair with the same s has exactly the same projected future at every horizon; K₀ is identity. Yet define the everywhere available intervention T(s,z)=(s XOR z,z). In the fibre s=0, T(0,0) projects to 0 while T(0,1) projects to 1. No deterministic or stochastic effective kernel represents this fixed intervention for all microstates. Choosing λ₀=δ_(0,0) yields projected outcome 0; choosing λ₀=δ_(0,1) yields outcome 1. Passive prediction is perfect, and intervention invariance still fails.

For a separate availability obstruction on the same space, offer a flip action F(s,z)=(1−s,z) only when z=1. Where executable, its projected effect is perfectly uniform. However, an agent at (0,0) cannot execute “flip” without a separate permitted preparation operation. A lifting that selects z=1 implements the macro flip only if moving or resetting to that representative is itself authorized and physically available. Thus consistency of consequences, existence of a selected implementation, and universal executability are different claims.

## Garden contact, rival, and concrete repair

The transplant source independently assigns soil_field and soil to a common recipient. This is an explicit synthetic preparation operation, not evidence that arbitrary such carrier combinations naturally arise. Source inspection shows soil_richness returns zero when the archive is empty, while nonempty archives couple field total and archive length to controller updates. An intervention vocabulary of “transplant field” therefore needs to state the archive condition and subsequent horizon.

The inherited experiments-03 report supplies a local witness: removing B's target entry removes promotion at horizon three; retaining only that entry restores it. Promotion averages the virgin stored fitness plus three updates. This supports a specific carrier/read-path intervention, not global additivity. A manually synthesized numerically identical entry has the same consequence, so the numeric recipient state does not encode the entry's ancestry.

The serious rival is engineered additive fitness plus a selected threshold recipient. It explains the inherited observations without a uniquely historical causal semantics. History explains where the entry came from in the donor construction; it is not identified by the recipient's response.

Concrete recommended repair: attach an intervention contract to each compressed model containing X, q, passive kernel, observed target/horizon, legal preparation operations, D_a, admissible selectors and policies, and an outcome-distance tolerance. Test projected-law diameter across the reachable portion of each fibre and test availability separately. For garden, use independently selected recipients, record archive conditioning, compare donor-generated versus matched synthetic entries, and retain candidate fitness history when modeling promotion. These are recommendations, not implemented experiments. The broad agent–field relationship remains available for play; only the inference from predictive closure to robust intervention autonomy is ruled out without these additional conditions.

## Provenance

Inspected NOW.md; FRR v0.5 compact seed, equivalence/congruence and intervention sections; RECOVERY_NOTE.md; field_wakes_parallel_pass_2026-10-05.md; true_garden_field_transplant.py and engine read-path locations; CERTX-context/CONTINUATION_HANDOFF.md and RECOVERED_CODEX_HISTORY.md; reports/experiments-03.md. The mathematics is derived here from explicitly finite definitions. Garden numerical claims are inherited execution evidence sharing the supplied source lineage, not this worker's execution or independent confirmation. Historical intake pauses are superseded by NOW authorization.
