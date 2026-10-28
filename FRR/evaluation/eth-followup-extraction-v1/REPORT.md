# ETH follow-up: fixed-program guarantees and precision interfaces

Accessed 28 October 2026 UTC, corresponding to the client's 27 October America/Chicago session. This is a selected static audit and small independent arithmetic illustration. It is not an independent Lean verification, full proof audit, or SAT benchmark.

## Current official status

[OpenAI's announcement](https://openai.com/index/building-scientific-understanding-with-academic-communities/), dated 26 October, explicitly announces that its system disproved ETH and reports subsequent Lean verification. It identifies the outputs as research material for further understanding and announces an independent examination organized by Impagliazzo, Paturi, and Williams. The wording is stronger than merely predicting a possible result. Its reported verification is distinct from a checker we executed and from completed community understanding; neither latter event was established here.

The GitHub connector's fresh [main-branch API read](https://api.github.com/repos/openai/math/branches/main) resolves to `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, committed `2026-10-26T21:18:03Z`, the same pin as the earlier scout. GitHub's signed-commit verification flag authenticates a commit signature; it is not Lean verification evidence. No community commentary was used as mathematical evidence, and no author was contacted.

## What the endpoint actually promises

The [configured endpoint](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean) has quantifier order

`for each k≥2, there exist one finite primitive machine and positive C,A,S,d,e; for every n and width≤k formula F, there exists a halting run ...`.

The machine and constants precede the input quantifiers. This excludes replacing the program or its constants separately for each formula or size. Its count tape contains the exact binary count, its answer tape contains whether the count is positive, and its halt state agrees. Time and every-prefix visited space concern that same run of that same machine. The compiled realization uses 1,220 tapes; count and answer outputs occupy tapes 256 and 1,216. These are formal statement contents, not observed executions.

The primitive machine scans one selected tape and makes a finite transition with a move/write action. Thus the endpoint is about primitive steps, rather than an uncharged arithmetic oracle. Inspecting this signature does not establish that all compilation lemmas and dependencies are sound.

The scale is

`g(n)=n [ln ln(n+16)]² / √ln(n+16)`

and the declared time is `C(L+1)^d 2^[A g(n)]`, with `L` the particular encoded formula length. This has **two** log-log factors. The manuscript's [main theorem](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex) claims a sharper single-log-log bound, and a still sharper fixed-density bound. The formal endpoint inspected here corresponds to its weaker rational-interpolation bound. A check of this endpoint would not by itself certify those appendix improvements. Both scales are sublinear in n and would suffice for the ETH consequence at fixed width.

## Consequential bridge: what is charged as input and space

The target uses finite sets of clauses and finite sets of literals on `Fin n`. Its count includes all declared variables, even unused ones: an empty formula has count `2^n`. Dropping unused variables without multiplying their contributions would change this counting target. Duplicate clauses are absent in the representation; their removal preserves ordinary CNF counting.

The input encoding is framed and uses unary natural-number fields. It should not be silently read as a standard compact binary DIMACS length. Nevertheless [EncodingBounds.lean](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/EncodingBounds.lean) supplies the explicit bridge, with `m=F.card`:

`L+1 ≤ (8k+7)(n+m+1)²`.

[Asymptotics.lean](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Asymptotics.lean) defines `ρ(n)=n [log₂ log₂ n]²/√log₂ n` and states `g(n)≤4ρ(n)` for `n≥20`. Consequently `exact_count_eth` transports the time constants as `C→C(8k+7)^d`, `A→4A`, and `d→2d`; space uses `S→S(8k+7)^e`, `e→2e`. This makes the theorem-to-input-size correspondence explicit. Fixed k is essential to treating these parameters as constants. For the finite-set input, the number of distinct width≤k clauses is polynomial in n at fixed k, so the polynomial input factor does not hide exponential dependence on n.

[VisitedTape.lean](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/VisitedTape.lean) instruments absolute head coordinates without changing machine transitions. Space sums the enclosing intervals on every tape, including the initial input interval. It tracks historical visits, not merely currently nonblank cells. The endpoint requires its polynomial bound at every prefix. The module explicitly distinguishes a bound derived from run length: substituting an exponential full runtime into that estimate would not establish polynomial space. The inspected final path instead obtains a separate space budget and handles small inputs by a fixed fallback program.

## Deeper appendix interface: precision changes the branch count

The sharpened [contraction appendix](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/quantitative-contraction.tex) works in a truncated polynomial ring modulo powers of two. Its precision is exact divisibility information. It is not numerical tolerance.

At a node of valuation i, the tapered Hermite recovery chooses jet multiplicity `q_t=h max(0,u−i)`, with `h=ceil(3M/u)` and `D_t=L/2^i`. It requests child precision `p_t=p+8hD_t+8M(a+1)`. The recovery proof charges denominator/evaluation losses before reducing back modulo `2^p`. Its quantitative gain comes from changing multiplicities gradually across valuation levels: the relevant loss is `O(MD_t/u)`, whereas a flat cutoff can lose `Θ(MD_t)` near its edge.

Cross-group interactions are expanded into modes of weight w whose coefficients are divisible by `2^w`. Only monomials with weighted exponent sum below `p_t` survive. With at most `6M/D_t` modes per weight, the partition bound gives `exp(O(√(Mp_t/D_t)))` possibilities; substituting `p_t=O(MD_t/u)` yields `exp(O(M/√u))`. The recovery precision bound therefore controls the interface's combinatorial cost. One cannot borrow the factorization identity while leaving its precision and enumeration costs uncharged.

A further obligation is immutable **creation precision**. Each tensor entry is canonically lifted from the precision at which that tensor was created; later calls retain that choice. Canonical lifting does not preserve ring operations. Recomputing an old defining expression at greater precision can select a different tensor. Descriptions are shared by reference to avoid accumulating nested entry routines, with separate entry-evaluation costs charged. These are manuscript mechanisms inspected statically; no correspondence of this sharpened appendix to the endpoint's complete Lean dependency graph was established.

The independent [arithmetic illustration](lift_witness.py) makes the creation-precision issue concrete. At precision two bits, `3+3` has representative 2 and `3·3` representative 1. Lifting those results to four bits retains 2 and 1, while evaluating the expressions directly at four bits gives 6 and 9. They agree modulo four and disagree modulo sixteen. [Recorded output](LIFT_WITNESS_RESULTS.json) has two successful exact cases. The first successful invocation printed to tools; a second identical successful invocation captured the receipt. No failed run was discarded. This checks elementary integer arithmetic only and neither validates nor challenges the ETH proof.

## Verification limits and useful next action

Neither `lean` nor `lake` is on PATH. No toolchain was installed; no Lean, Comparator, or Nanoda run occurred. The comparator configuration permits `propext`, `Quot.sound`, and `Classical.choice` and disables Nanoda. Those settings and the `#print axioms` source commands are not successful checker logs. The target file's placeholder `sorry` is a challenge specification, not by itself evidence of an admitted solution proof. Dependencies were not audited transitively.

The official result would invalidate ETH-based conditional barriers, while leaving unconditional lower bounds and the need for concrete algorithms intact. None of the inspected asymptotic statements supplies a measured crossover, a practical SAT implementation, or a polynomial-time algorithm. No change to FRR's core, navigation, or result status follows from this contact.

The useful transfer is a precise versioned-interface test: a handoff must say which representation, origin, and creation-time semantics its downstream reconstruction assumes. A reader should not recompute a frozen intermediate under a newer context and silently substitute it. [NEXT_CONTACT.md](NEXT_CONTACT.md) proposes a bounded fresh reader case; this is our application proposal, not an empirical FRR result.

Read scope, hashes, upstream blob identities, and access failures are in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) and [READ_SCOPE.json](READ_SCOPE.json). The browser rejected the GitHub commit-history URL; the GitHub branch connector succeeded. Existing source copies were read without edits and their selected hashes match the prior manifest.
