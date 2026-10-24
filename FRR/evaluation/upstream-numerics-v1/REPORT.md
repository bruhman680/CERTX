# UN-C1: upstream numerics before downstream interpretation

User authorized resumption and confident refinements, asking whether source weaving includes upstream dynamics. The existing three-angle scout already names underlying challenges. This contact makes the implementation/representation path explicit and tests one concrete source lead before proposing changes to training code.

## Source and actual access

[Barron, Gnanapragasam and Tschannen,2610.31642v1](https://arxiv.org/html/2610.31642v1) proposes stable expressions for hard-target and teacher/student gradients. Primary methods/examples and selected experimental passages were read in the prior intake; this contact uses explicit algebra from those methods. No new literature sweep. Its reported optimizer/training outcomes are not reproduced here.

Workspace inspection found NumPy and mpmath available, but neither JAX nor PyTorch installed. No packages were installed. [Protocol](PROTOCOL.md) explicitly limits this to evaluated formulas and high-precision reference checks, not actual framework backward kernels, training speed, optimizer trajectories or all dtype/platform combinations.

## Recorded observations

Six hard-target cases cross float32/float64 and gaps10,18,40 on[m,0,0]. At float32 gap18, the usual target-gradient subtraction is0 while the stable form is−3.0459962e−8, matching the reference within about1.02e−7 relative error. Both non-target components remain positive in the usual expression, so its gradient sum is nonzero. At float64 gap40, the usual target subtraction also becomes0 while the reference is−8.4967085e−18. Higher precision moves a boundary; it does not abolish it.

Six soft-target cases cross those dtypes with zero and two small student/teacher differences. Separate normalized-exponential and exponentiated-logsoftmax operation paths give residual gradients at equal logits: max magnitude about1.49e−8 in float32 and2.78e−17 in float64. The stable expression gives exactly0 for equality. For the tested nonzero float32 differences, maximum absolute reference errors are at most2.28e−13 for the stable expression versus about4.60e−8 for the usual two-path subtraction. These are our NumPy formula-path results, not claims about every library implementation.

A separate representation stress starts with unequal float64 student/teacher logits, adds a common1e5 shift, then casts to float32. The stored arrays become identical. The intended reference gradient is nonzero, while both the stored-input reference and stable gradient are0. This is a correct answer for the altered inputs; it cannot recover a difference erased before computation. Mathematical shift invariance alone does not guarantee invariance after destructive representation changes.

## Checks and warranted refinement

All six declared checks pass. A separate100-decimal differentiation check exactly matches the saved hard-target reference gradients and verifies real-arithmetic common-shift invariance for those cases. Source/protocol hashes and execution streams are retained in [CHECKS.json](CHECKS.json). One model/formula run and one independent-formula check; no failed execution, random draws or omitted cases. This is same-assumption numerical review, not independent empirical validation.

The optional [three-angle scout](../../modules/three-angle-scout.md) now asks where the consequential distinction first enters, changes or disappears: source generation/access, representation, numerical operations, observation/calibration, objective/evaluator, inference and action/feedback. This is a candidate dependency path, not a universal linear theory or mandatory checklist. Trace back only as far as the next useful decision requires; feedback can alter earlier stages.

The [verification guidance](../../modules/verification-layer.md) now distinguishes intended mathematics, actual computation on stored inputs, and preservation of the intended input information. Invariants and stationary cases are useful diagnostics; passing them alone does not establish all numerical accuracy, mechanism truth or good downstream outcomes.

## Existing results and next useful boundary

Targeted source inspection found a moderate-logit softmax-support check and direct probability/KL arithmetic in older tools/audits. They are different paths; no training-loop dependence was identified in this targeted read. No historical source/result is patched or retroactively invalidated. No claim is made that all CERTX numerical code has been audited. A future material use of near-zero KL, clipping or gradients deserves its own precision/conditioning contact.

We have not adopted a replacement training loss or inferred that numerical error explains our reasoning, memory or swarm behavior. Actual-agent record-access work remains a separate pending bridge. The readable-code/history idea remains deferred. Core/runtime/schema and scientific queue statuses stay unchanged; this contact refines a working practice and preserves a runnable small numerical instrument.
