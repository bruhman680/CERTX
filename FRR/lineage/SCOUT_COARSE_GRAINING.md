# Source scout: compression, emergent memory, and repair

2026-10-05. Functional search for projection failure and repair, alongside genealogical searches for Mori–Zwanzig, lumpability, and computational mechanics. This is a scoped source contact, not a novelty assessment. The agents share the originating material; their agreement is not independent evidence.

## Projection can expose memory without locating its physical carrier

Chorin, Hald, and Kupferman's [2000 primary paper](https://math.huji.ac.il/~razk/Publications/PDF/CHK00.pdf) derives a generalized Langevin identity for selected observables of an underlying dynamical system: a current-state contribution, a history-dependent memory integral, and an unresolved contribution. Their conditional-expectation construction uses prior statistical information, in their setting an invariant measure, and assumes the relevant evolution operators are well-defined. An exact identity is distinct from a usable approximation: orthogonal dynamics still need treatment. Dropping memory and unresolved terms requires justification; being optimal in a restricted approximation class does not imply long-horizon adequacy.

FRR contact: an actor-only description can require history even when the joint actor–field state evolves locally. The memory integral is a representation of unresolved influence, not proof that the actor internally stores its past. This supplies a mathematical relative for the echo/wake ambiguity; it does not diagnose which physical variable carries persistence.

## The repair deserves its own lineage

The same authors' [Non-Markovian Optimal Prediction (2001)](https://arxiv.org/abs/math/0101022) explicitly follows strong underresolution into a memory-aware approximation. It approximates orthogonal dynamics through an ansatz and Monte Carlo evaluation of autocorrelations. This is a concrete repair program, not a guarantee that any finite history augmentation solves any projection problem.

FRR consequence: after a compression fails, distinguish adding observed variables from modeling unresolved dynamics. A good history-based predictor can be useful while leaving causal placement of memory unresolved.

## Exact Markov compression is a restrictive compatibility property

For a finite Markov transition matrix P and partition blocks B, strong lumpability requires that sum_{z in B} P(x,z) be identical for every x in the same source block, for every target block. This makes the projected block process Markov with the same macro-transition rule for arbitrary initial distributions. Equality of one observed average is weaker.

The primary [Optimal partition and effective dynamics of complex networks](https://pmc.ncbi.nlm.nih.gov/articles/PMC2786939/) develops an optimal-prediction partition criterion for network Markov chains. Its exact residual-equality characterization has explicit nonsingularity assumptions; its approximate clustered-network conclusions use spectral separation and a controlled timescale. The article also demonstrates that a partition suited to geometric segmentation can differ from one preserving dynamical closure.

FRR consequence: a channel need not be spatially contiguous to define a valid dynamic state, and a beautiful cluster need not be one. Lumpability concerns a specified transition kernel; interventions changing that kernel require fresh compatibility tests. It does not establish permanence, physical merging, or universal topology change.

## Predictive equivalence supplies another repair

Shalizi and Crutchfield's [Computational Mechanics: Pattern and Prediction, Structure and Simplicity](https://arxiv.org/html/cond-mat/9907176v2) groups histories by equal conditional distributions of entire futures. For the stationary stochastic-process setting studied, causal states provide a minimal predictive representation, with the paper establishing optimality and uniqueness results under its mathematical conditions. Agreement for the next symbol alone can require refinement when longer futures are compared. The number of causal states need not be finite.

FRR consequence: restore distinctions according to future consequences rather than retaining every historical detail. These are predictive states. Their name does not grant intervention sufficiency or identify a physical memory substrate. A field actively changing across training or control cannot silently inherit stationary-process results.

## Surviving weave and next contact

The established relatives preserve different objects: projected differential-equation observables, partitions of Markov microstates, and equivalence classes of observational histories. They converge on a functional constraint—erased distinctions must not alter the future behavior being preserved—but do not prove a common physical mechanism or shared critical parameter.

A useful next experiment fixes one observation map throughout a wake-building run. Compare (a) actor-only Markov prediction, (b) actor plus measured field, and (c) actor plus history. Evaluate held-out prediction, then reset/transplant the field. This can distinguish improved compression from evidence locating persistence. It would not, by itself, prove a phase transition.

Access note: a hosted scan of Kemeny–Snell chapter 6 was located, but retrieval timed out; it was not read. The source claims above rely on opened primary research, including the network article's explicit lumpability discussion. The 2000 paper and 2001 follow-up share authors and genealogy; they are not independent replications.
