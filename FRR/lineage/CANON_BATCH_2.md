# Canon batch 2: useful structures and limits

Scope: all five supplied texts were read. This is a local textual, mathematical, and code-snippet audit. No cited papers, WANDER records, raw experimental data, or external repositories were retrieved. Inclusion in canon records provenance; it does not certify a claim. The originals remain unchanged in `sources/canon-batch-2`.

## What the documents add

| Document | Useful surviving relationship | Status of stronger interpretation |
| --- | --- | --- |
| Ionosphere/neural dynamics | Sparse participation, external coupling, layered processing, and persistence of relationships are fruitful comparison targets. | A formal isomorphism and universal architectural optimum are not established by a table of correspondences. Several particular formulas fail below. |
| Adaptive Knowledge Scout | A specific knowledge gap can select a search, and retrieved material can be integrated in limited, reviewable increments. | CERTX constants, universal health bands, compulsory emergence, and identities with free energy need independently specified models and evidence. |
| Intent–Reasoning–Meaning–Coherence | Purpose changes which meanings are relevant; new contact can refine a working interpretation of the task. | Relevance, consistency, validity, and evidential support cannot all be replaced by closeness to a preferred answer. No dynamical attractor is established by naming a preference an attractor. |
| Nonlinear complexity | Bound the live branch set, control work per step, archive useful residues, and monitor actual resource use. | A population cap does not bound candidate length, archive growth, step count, pair selection, or external call cost. |
| SSCG-inspired unified engine | Candidate evolution, branch management, recycling, and abstraction changes can share interfaces. | The code is a sketch with missing dependencies; its heuristic is not an SSCG computation, complexity theorem, calibrated forecast, or proof of incomputability. |

The strongest common relationship is operational: **purpose and observed gaps can steer bounded exploration; tests can revise which branches stay active; failed branches can leave useful instruments and distinctions.** This remains compatible with FRR's open play. It need not become a fixed loop or a universal metric.

## Direct contact with consequential claims

### Residual information: unconditional claim contradicted

Ionosphere text §3.6 states that residual layers make I(h0;hL) nondecreasing. Let H be a fair binary variable and choose f(H)=-H. The residual output H+f(H) is constant: information drops from one bit to zero. The residual Jacobian I+Df is also zero in this example. A residual can provide a useful route, but cancellation and noninvertibility remain possible. Under a feedforward Markov-chain model with no additional input, data processing supplies the nonincreasing direction, with equality under sufficient preservation conditions. The source's own table declines from 0.95 to 0.81, inconsistent with its stated nondecrease.

Repair direction: specify injectivity, information retention, or controlled Jacobian conditions, then test task behavior. This audit has not searched the repair literature.

### CERTX eigenvalue band: not a general stability guarantee

Scout §2.3 and §5.3 accept 0.8 <= |lambda| <= 1.2 as healthy. For the discrete update x_next=1.1x, every eigenvalue of a five-dimensional 1.1I matrix passes that band, but perturbations grow by 1.1^t. For a linear discrete autonomous system, asymptotic stability requires spectral radius below one. A continuous-time linearization instead uses negative real parts. Nonlinear, driven, stochastic, and nonnormal cases need further conditions. Dimension count alone supplies none of these.

Repair direction: define the state, measured operator, time convention, uncertainty, and stability target before choosing bounds. The displayed damping formula zeta=1+1/N is a candidate prescription, not a proven universal law in the supplied material.

### Coherence: relevance cannot purchase validity

The intent map proposes a weighted coherence score with validity weighted 0.4 and intent/context each 0.3. A candidate assigned zero validity but perfect alignment and fit scores 0.6. This shows why a single threshold can admit an invalid, pleasing candidate. “Irrelevant to this goal” does not mean “meaningless.” A purpose may refine through exploration, but an AI's working interpretation cannot silently replace the user's instruction. Following the strongest pull also does not guarantee coverage of all important territory.

Repair direction: keep relevance, logical validity where applicable, evidential support, and exploratory value separately inspectable. A hard proof obligation cannot be offset by preference alignment.

### Smoothness and missing distinctions

Scout §8.2 uses lower graph Dirichlet energy as increased coherence. Constant signals have zero Dirichlet energy, including signals that erase every target distinction. Smoothness becomes useful relative to a specified graph, boundary conditions, constraints, and behavior; it does not certify semantic quality by itself. This is FRR's trivial-collapse test in an executable setting.

### Conductance evidence: arithmetic and definition mismatch

Ionosphere §4.5 defines neural conductance as I/H. For finite discrete variables with nonzero H, this normalized value is at most one, whereas §4.6 lists values 1064, 625, 354, and 439. Switching to unnormalized bits requires an explicit change of definition and a stated estimator.

In §6.2, sqrt(1-S)*N_eff yields approximately 512, 181.019, 64, 22.627, and 8, not the printed 512, 181, 90, 45, and 23. The quoted correlation and fitted coefficient cannot repair that inconsistency. No raw runs are available here to determine what was actually measured. Reported empirical numbers remain unverified; this does not establish that they were fabricated.

Appendix A.1 shifts from scaling proportional to N^(3/2)*p to N*p^(3/2) without a valid conversion. That argument fails to establish its exponent. Its failure does not exclude all sparsity/conductance relations.

### Additional domain boundaries

Finite unmasked softmax probabilities are positive; a near-zero threshold count differs from exact L0 sparsity. Causal masks restrict allowed entries, and explicit sparse attention can introduce zeros. Softmax sharpening is not automatically a physical breakdown threshold.

The ionosphere document mixes cloud lightning with ionospheric behavior, treats some variable physical profiles as exact persistence, and uses S=(E cross H)/mu0 where its other formulas use H as magnetic field intensity; with that convention the usual expression is E cross H. Its stated pure quadratic recombination equation without production yields algebraic, not exponential, decay. These are domain-specific repair points, not grounds for discarding every analogy. No external physics source audit was performed here.

### Scout emergence and evaluation construction

The scout implementation explicitly programs hunger-to-query mappings, thresholds, retrieval, and integration. Correlation between those programmed signals and actions demonstrates implementation behavior at most; it cannot alone demonstrate spontaneous emergence. Monitoring plus search access does not compel a policy to search. A serious test needs an ablation that removes the routing rule and an independently specified behavioral outcome.

Named WANDER findings, confabulation percentages, phi thresholds, and optimal ranges require the underlying operational definitions, datasets, and analysis. The supplied sketch computes a bundle score but returns a different weighted score, leaving the bundle rejection rule unenforced. Its rate formula responds to the upper eigenvalue boundary only and can become negative above it. A state difference can be a negative gradient under a specified quadratic objective and metric; it is not automatically variational free energy or proof of subjective feeling.

### Complexity sketch: useful controls, incomplete guarantees

The nonlinear code's loop detector returns a tuple, but the caller tests the tuple itself. Even (False, None) is truthy. The archive loop removes entries during iteration, potentially skipping candidates. Summary transition lists and archives can grow despite a fixed recent window. Top-k neighbor lookup includes a search/indexing cost; hashing includes constructing the state representation. A cap bounds live count, not total work or semantic fidelity.

The SSCG-inspired score bins population, interactions, and branch factor into arbitrary levels. It supplies no established connection to SSCG growth or incomputability. Its predictor keeps a zero level at zero and rapidly caps other levels at three, so “prediction” is a prescribed transformation rather than a measured growth forecast. Useful resource diagnostics would report count, bytes, latency, calls, and observed growth under a declared workload.

The unified sketch appends children while iterating over the same list, so children can be processed and spawn again in that step if their predicate persists. A population cap is not enforced there. Pruning with keep=0 uses list[-0:], which retains the entire list. Missing classes and methods prevent treating the file as a complete runnable engine. These are specific construction defects, not a refutation of modular coordination.

## What is integrated now

The active runtime remains 0.2. A new optional `modules/bounded-inquiry.md` describes the useful implementation contract without importing unverified constants. Four additional authored cases enter development. Local diagnostics are recorded in `evaluation/results/canon-contact.json`; they are counterexamples and snippet checks, not neural experiments or controlled FRR evaluations.

The next meaningful contact is a small host implementation with explicit branch and resource budgets, artifact links, and task-relative outcomes. Compare its branching and scouting policy with simpler fixed-budget alternatives. Define measurements before adding a CERTX or coherence score. Keep any such implementation distinct from a claim of universal cognitive dynamics.
