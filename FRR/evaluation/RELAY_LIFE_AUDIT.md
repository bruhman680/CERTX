# Life relay: reproduction, observable-specific nodes, and possible pasts

Status: exhaustive finite-model reproduction and extension. No inference about real AI memory, physical dissipation, or infinite-lattice Life is made. The supplied script is retained unchanged under `lineage/sources/claude-relay-2026-10-15/life_nodes.py`.

Run: `python experiments/relay-life-audit.py` from the FRR root. Results: `evaluation/results/relay-life-audit.json`, including original stdout, numeric tables, cross-check outcomes, and concrete witnesses.

## What reproduced

The successor map covers all 65,536 configurations of a 4×4 periodic torus. An independently coded per-cell bitwise neighbor enumeration agrees on every successor; it avoids the source's array-roll implementation. Kahn peeling independently recovers the same recurrent set. These checks share the mathematical Life rules and input space, so they establish implementation agreement rather than independent physical evidence.

| Quantity | Exact result |
|---|---:|
| States with no immediate predecessor | 47,657 |
| States with at least two immediate predecessors | 6,927 |
| Maximum immediate predecessor count | 9,628 |
| Recurrent states | 1,245 |
| Cycles | 345 |
| Cycle counts at lengths 1, 2, 4, 8 | 53, 180, 16, 96 |
| Largest basin | 49,116 states |
| Maximum transient length | 9 |

Forward classes group states with identical observation strings `(O(x), O(f(x)), ..., O(f^t(x)))`. Their counts reproduce: constant 1, full state 65,536, population count 249, left-window population count 1,085. Equal consecutive class counts first occur at horizons 1, 1, 5, and 9, respectively. Since these forward partitions provably refine their predecessors, that equality implies a stable partition. It is not a general rule about equal counts in arbitrary evolving partitions.

Merge states, recurrent states, and forward observational equivalence classes answer different questions. None alone supplies a universal meaning of information node. A successor fibre is a preimage set; it is not automatically a fibre bundle with uniform fibres and local trivializations.

## A relay correction: this defect does not grow monotonically

The relay says the popcount macro-model defect grows with horizon. The supplied script instead prints average defects **0.7069, 0.6577, 0.5791** at horizons 1, 2, and 3. Worst values are 0.9975, 0.9967, 0.9977. The general claim of growth is contradicted by its own output.

Its metric is `1 - predicted_probability(actual_macro_outcome)`, averaged over uniformly selected microstates. Equivalently, at each state it is TV between the deterministic actual macro outcome and the fibre-averaged Markov prediction. The chosen uniform-in-fibre reset is built into the one-step macro transition matrix. Iterating that matrix is an additional closure assumption: projected microstate distributions need not remain uniform within each fibre. This score is not physical entropy production, and its horizon behavior need not be monotonic.

## Separating abstraction A from observable O

For deterministic Life, define the exact pairwise target defect

`d(A,O,t) = max{ TV(delta[O(f^t(u))], delta[O(f^t(v))]) : A(u)=A(v) }`.

TV is 0 or 1 here. The audit also reports the fraction of uniformly weighted microstates lying in an A-fibre with multiple target outcomes. That latter fraction is a prevalence measure under a declared initial-state weighting, not the probability that any particular predictor will err.

With fixed O and t, refining A cannot increase either maximum defect or the ambiguous-state share. The script verifies this on the refinement chain constant → population count → joint population/window count → full state for all four observables and horizons 0–12.

The 249-class stable population-count abstraction preserves its own target exactly for every future time, by construction. But with the target changed to left-window count, it has maximum defect 1: 84.87% of states lie in ambiguous fibres at horizon 1 and 23.86% at horizon 9. Conversely, the stable left-window abstraction is not exact for total population. More classes do not automatically make an abstraction universally better: partitions can preserve different distinctions and need not refine one another.

This is the substantive A/O contact: an abstraction can be a complete behavioral description for one declared observable while hiding a distinction important to another. Changing O changes the question, not merely the accuracy score.

## Two meanings of a backward partition

### Literal full-state predecessor sets

Let `B_k(v) = {u : f^k(u)=v}`. For distinct target states v and w, nonempty sets B_k(v) and B_k(w) are disjoint, so they cannot be equal. Grouping targets by equality of these sets therefore yields one singleton class per depth-k reachable target, plus one class containing all targets with empty pasts.

The class counts at depths 1–9 are 17,880, 7,726, 4,554, 2,790, 1,854, 1,398, 1,310, 1,262, and 1,246. At depth 9 only the 1,245 recurrent targets remain reachable. This definition is exact but nearly trivial: it uses the identities of complete predecessor microstates.

### Sets of possible observable past words

For a nontrivial observation-relative version, define

`L_k(v) = {(O(u), O(f(u)), ..., O(f^(k-1)(u))) : f^k(u)=v}`.

The present observation O(v) is deliberately excluded. Targets are grouped by exact equality of their L_k sets. There is no initial probability law and no multiplicity weighting: one and a thousand predecessors yielding the same word count as the same possibility. This is a possibility-support partition, not a reverse-time predictive distribution or a computational-mechanics reverse causal state.

| Past depth | Population-count past classes | Left-window past classes |
|---|---:|---:|
| 1 | 33 | 69 |
| 2 | 67 | 250 |
| 3 | 70 | 278 |
| 5 | 41 | 161 |
| 8 | 24 | 93 |
| 9 | 23 | 91 |
| 10 | 23 | 91 |
| 12 | 23 | 91 |

These partitions are not a forward-style monotonic refinement: possible prefixes may disappear when they cannot be extended further into the past. In particular, even a constant observable produces two backward classes—targets with any depth-k past and targets with none. Their membership changes through depth 9. A passive constant observer cannot discover which actual full state it occupies; the grouping is a property of the oracle finite-state model, not an observational capability bestowed by the constant output.

An important extra warning: the left-window class count stays 91 at depths 9–12 **while membership still changes between each adjacent depth**. Equal counts alone therefore do not establish backward stabilization. The JSON stores partition-equivalence checks and a concrete pair of states witnessing this change. The stable-count claim used for forward refinement cannot be transplanted without its refinement premise.

Forward and backward partitions differ in both directions. At depth 12, population-count past classes fail to determine forward classes, while some equal-forward-class states have unequal possible pasts. Thus neither grouping is generally a refinement of the other. Retrodictive ambiguity and future observational equivalence are distinct relational questions.

## Scope and next contact

Finite-torus predecessor-free states are sometimes called Gardens of Eden, but enumeration on this fixed periodic domain is not a proof or test of the Moore–Myhill equivalence for infinite cellular automata. A separate source pass is needed for that theorem and its precise assumptions.

The natural next theoretical choice is what a backward observer should preserve: possibilities, multiplicities, probabilities under an initial ensemble, or stationary reverse-time predictions. The present experiment exposes that choice rather than selecting it universally. Under a stationary deterministic finite-system ensemble, transient states have zero probability; that would remove the large class of impossible long pasts and materially change the inquiry.

These findings support a narrow FRR refinement in use: declare the direction, target, ensemble, and horizon before calling a partition a node or a count stable. No core prompt change is needed to adopt that discipline here.
