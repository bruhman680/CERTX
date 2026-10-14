# Wake reset scout — 2026-10-13

## Contact and surviving distinction

Read the Claude continuation and both source scripts directly. Their joint state is (visible y, hidden e). Calling e an environment does not distinguish its mechanism. A useful operational distinction is whether e can be retained, erased, or transplanted independently of the focal actor, and whether an independently initialized reader responds to it. The same variable can function as internal memory under one boundary and environmental memory under another. Passive trajectories alone cannot uniquely locate that boundary.

The edge interpolation changes an update kernel continuously. It supplies no actor-replacement or field-transplant test yet. The frozen e endpoint also retains its initial value without any actor-produced write: persistence alone is insufficient evidence of a wake. We need action-conditioned preparation versus a no-write rival.

## Small paired replay with exact predictions

Keep Claude's K table unchanged. Declare actor state y and independently owned field e, with separate constructors and reset methods. A writer uses an explicit action that sets e to its previous visible symbol, following the existing echo update; prepare writer symbols w=0 and w=1 by intervention. This is engineered writing, not spontaneous memory emergence. The writer action must precede reader generation, and order must be recorded.

Destroy the writer object and instantiate a new reader with y=0, no writer history, no treatment labels, and fresh random numbers. Freeze further field writing for the first read; subsequent write-enabled reads are a separate condition. Compare:

1. Retained prepared field e=w.
2. Cleared field: independently fair e in both writer conditions.
3. Sham reset: actor recreated but e unchanged.
4. Transplant: field from the opposite preparation, actor reset identically.
5. No-write: identical writer actions with the field-write operator disabled.
6. Reader-blind: replace K[e] with an e-independent kernel to test whether the read coupling is necessary.

For the first post-reset symbol, P(y_next=1|w=0,retain)=0.15 and P(y_next=1|w=1,retain)=0.45. The exact Bernoulli TV is 0.30. Under fair clearing, both probabilities equal 0.30; no-write must also remove w dependence given independent initialization. Opposite transplants reverse the effect. These values follow directly from construction and are unit targets, not independent empirical discoveries.

Use the same uniform draw for paired read branches, but separate independent draws for distinct stochastic mechanisms (visible generation, hidden refresh). This couples potential outcomes for variance reduction without changing either marginal kernel. Do not reuse one draw to create supposedly independent events. Report exact law plus sampled differences over independent seeds and an interval for the difference, not merely thresholded success.

Add delay d with symmetric field flips at probability epsilon and no writing. The predicted contrast is 0.30*(1-2*epsilon)^d for epsilon in [0,0.5]. This tests retention horizon and update implementation. A finite nonzero contrast is not permanent law. Changing the read kernel or coarse-graining can remove accessibility while e still persists.

## Stronger design and serious rivals

Factorial retained/cleared actor memory versus retained/cleared field identifies both possible carriers. Include a trajectory log as a separately controlled carrier, rather than accidentally passing it with the field. A payload-preserving sham erasure separates manipulation side effects from erasure. In a spatial substrate, also preserve total amplitude while shuffling positions to distinguish retained payload from generic resource or energy effects. A common field may alter action without encoding the relevant distinction; assess both decoding and subsequent action.

Serious rivals: initial-field confounding; retained RNG or actor state; hidden metadata labels; a reader trained on treatment IDs; action-independent field relaxation; generic surface changes; replay summaries that reconstruct deleted data; and projection-induced memory without an independently manipulable environmental carrier. A copied hidden bit implements an operational external-memory toy, but does not establish stigmergy, semantics, useful collective growth, or physical irreversibility. Erasure that reduces an effect identifies a necessary carrier relative to tested interventions, not a unique historical origin or globally sufficient mechanism.

## Sources and access depth

- Reid, Latty, Dussutour & Beekman (2012), *Slime mold uses an externalized spatial memory to navigate in complex environments*. https://pubmed.ncbi.nlm.nih.gov/23045640/ ; DOI https://doi.org/10.1073/pnas.1215037109 . Reopened primary bibliographic page, abstract, and figure captions this pass. The full PMC page was blocked by a browser challenge; earlier local SCOUT_SUBSTRATE.md records a prior full-text inspection. Figures compare blank agar with substrate-wide extracellular slime, and separate Y-maze avoidance tests. This supplies an experimentally manipulated environmental trace. Substrate-wide masking is not selective erasure, and brainless is not internally stateless. It is not the exact writer-destruction/read-transplant design above.
- Beckers & Halpern (2019), *Abstracting Causal Models*. https://arxiv.org/abs/1812.03789v4 . Primary abstract inspected this pass. It separates exact, uniform, and stronger abstraction requirements, including intervention scope and cases where distribution choice hides differences. Relevant discipline: an actor/field coarse description must declare which low-level interventions correspond to its reset and erase operators. No theorem from the paper is claimed proved for our toy here.
- Rubenstein et al. (2017), *Causal Consistency of Structural Equation Models*. Previously supplied PMLR URLs could not be opened in this pass; not counted as independently verified support. Beckers–Halpern explicitly identifies its exact-transformation ancestry. Related papers therefore share genealogy.
- Theraulaz & Bonabeau (1999), *A Brief History of Stigmergy*. https://doi.org/10.1162/106454699568700 . The PubMed retrieval returned no usable text this pass; prior SCOUT_SUBSTRATE.md records abstract-level access. Historical environmental mediation is a relevant relative, not fresh primary experimental verification.
- Reid's reference list identifies Chung & Choe (2009), *Emergence of memory-like behavior in reactive agents using external markers*, DOI 10.1109/ICTAI.2009.116. Located through the primary reference list only; not opened. This is a promising direct reactive-agent comparison, not evidence audited here.

## Next useful contact

Implement the first-read factorial and delay series before scaling swarm size. Then ask whether differently constructed readers can exploit a spatially distributed field without treatment-label access. Numerical agreement here would establish that the intended reset/write/read kernel executes; it would not independently validate an interpretation built into that kernel.
