# Continuity 06 — optimizer geometry and serious rivals

## Evidence boundary

Inspected on 2026-10-07: NOW.md, TASKS.json, FRR v0.5 Compact Runtime Seed, the October 5 field-wakes optimizer section, and reports/experiments-01.md. The scalar results below are inherited from experiments-01, not re-executed or independently replicated here. Bounded primary-source contact inspected author/venue abstract pages for Adam, AdamW, AdaBelief, and Reddi–Kale–Kumar. OpenReview returned a browser challenge; Google Research's author publication page supplied the convergence abstract instead. No full proof, tensor implementation, training experiment, prior transcript, or original Gemini optimizer was inspected. This report is the sole local mutation.

## What survives, and what must change

The defensible seed is that gradient history alters subsequent motion through optimizer state. With full state x=(theta,m,v,t), this is an ordinary state-dependent recurrence; calling moments an external field is relative to the boundary that excludes them. The existing scalar witness shows S=mhat²/(vhat+eps) exceeds its asserted [0,1] range, and the proposed decay component can flip and amplify a nonzero weight. It does not show an entire training trajectory diverges.

Inherit the corrected calculation explicitly: for beta1=.9, beta2=.999 and nonnegative epsilon, weighted Cauchy–Schwarz gives S<=sum_i a_i²/b_i. The limiting envelope is 52.8571428571428, not infinity and not 1; finite-horizon bias corrections must remain in the expression. The reproduced spike S≈9.99945 and retention≈-455.555 still invalidate the claimed universal shrinkage guarantee. Do not retain NOW's older broad phrase “unbounded moment ratio.”

Ordinary EMA lag mismatch is the serious rival to crystallization. Constant gradients produce S≈1 on a linear loss with zero curvature; gradients at a single weight can agree across shifted quadratics with drastically different Hessians. Gradient coherence therefore does not certify local curvature. These inherited witnesses support a measurement distinction, not a rejection of all adaptive controllers.

## Primary-source weave

[Adam, Kingma and Ba](https://arxiv.org/abs/1412.6980) explicitly uses adaptive lower-order moment estimates and reports diagonal gradient-rescaling invariance. That establishes neighboring precedent for historical conditioning; it does not establish arbitrary coordinate or neuron-permutation geometry for an added diffusion operator. [Reddi, Kale and Kumar](https://research.google/pubs/on-the-convergence-of-adam-and-beyond/) supplies a serious theoretical rival: EMA-based adaptive scaling can fail even in a simple convex setting, motivating longer-term gradient memory. Its abstract does not transfer a convergence theorem to GammaCAdam or to nonconvex training under new control laws.

[AdamW, Loshchilov and Hutter](https://arxiv.org/abs/1711.05101) distinguishes adaptive L2 regularization from decoupled weight decay. This pressures any interpretation that merges moments and shrinkage into one persistence mechanism. [AdaBelief, Zhuang et al.](https://proceedings.neurips.cc/paper/2020/hash/d9d4f495e875a2e075a1a4a6e1b9770f-Abstract.html) adjusts step size according to agreement between observed gradients and an EMA prediction. It is a direct functional comparison for an alignment controller, not evidence for the proposed crystallization semantics. All four contacts concern distinct published methods, while the local audit reports share recovered-source ancestry.

## Geometry pressure: a typed square suffices

An axis-roll Laplacian assumes index adjacency. Hidden units can often be relabeled with coordinated permutations of incident weights while preserving network function; optimizer moments must be relabeled too. Arbitrary relabeling need not preserve an index ring. Some special permutations do preserve the ring, so testing only cyclic shifts would conceal the problem.

For a single channel block let G=R^n, P:G→G be a permissible unit permutation, L:G→G a fixed index Laplacian, and D_L=I-alpha L. Compare P D_L g with D_L P g. The defect is alpha(LP-PL)g. A new analytical witness, not an executed test: on the three-node path with L=D-A, g=e1, and P swapping coordinates 1 and 2, LPg=(-1,2,-1) while PLg=(-1,1,0). The routes differ by alpha(0,1,-1). This is a geometry defect, not automatically worse loss or a causal explanation of instability.

If geometry is carried with the state, L'=PLP^T and D_L' Pg=P D_L g exactly. That repairs coordinate equivariance algebraically; it does not establish that the transported adjacency is functionally meaningful. An activation-similarity graph could be a candidate, provided its construction is itself permutation equivariant, calibrated separately, and compared with graph-free controls. Function-preserving rescalings pose additional pressure beyond permutations. A cube adds no useful third operation to this immediate question, so no cube is asserted.

## Concrete next step, not implemented

Keep a separate exploratory controller branch. Define a bounded coherence signal using the same positive averaging weights for numerator and denominator: (sum_i w_i g_i)²/(sum_i w_i g_i²+eps)<=1 when sum_i w_i=1. Alternatively clip the existing signal but disclose that this changes the controller. Independently constrain 0<=eta*decay<1, and test the full moment/parameter recurrence rather than borrowing the plain-GD Hessian threshold.

Use matched tuning/compute budgets for AdamW, AdaBelief, learning-rate-only control, decay-only control, joint control, diffusion, and a distribution-matched randomized signal. Repeat identical minibatches after a coordinated function-preserving permutation of parameters and moments; verify initial outputs agree, then measure both parameter-route defect and function-output defect. Compare fixed index adjacency with transported and function-derived adjacency. This separates an index artifact from useful relational coupling. Held-out performance remains a separate burden from safety and equivariance.

Leave alignment, field-wake, and playful cross-domain interpretations available as hypotheses. Their survival here is generative; the repaired range bound, explicit decay guard, and typed geometry comparison are the immediate claim improvements. No claimed repair or benchmark is implemented by this source weave.
