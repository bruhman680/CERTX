# Field Persistence & Crystallization of Wakes — conversation record

Provenance: user message on 5 October 2026, after garden reproduction. The complete original remains in the conversation; this file records its seed, important formulations, and a scoped audit. It is not a verbatim archive of the entire message. No external literature lookup or PyTorch optimizer execution was performed.

## Preserved originating question

How can an actor without internal historical memory encounter and reinforce a persistent environment altered by earlier action? When does a transient mark become a durable constraint, and what interventions distinguish reduced responsiveness, erased persistence, and altered rules?

Important source formulations:

> “A law is simply a wake whose relaxation timescale ... is effectively infinite relative to the observation horizon.”

> “Both systems share the same critical persistence boundary gamma_c.”

These are preserved as proposed interpretations, not accepted universal results.

## What survives

A coupled actor–environment state can be Markovian while an actor-only description is history-dependent. Resetting the actor while retaining or transplanting the environment can locate a carrier of persistence. Local action laws can remain fixed while the conditions they read change. The supplied garden probes demonstrate this distinction within their implementation.

Persistence, symmetry breaking, metastability, inaccessible transitions, permanence, and physical law are distinct claims. A canyon can be an effective boundary at one scale and horizon while remaining alterable under geological or engineering interventions. It does not acquire a new fundamental law merely by becoming durable.

“Memory without storage” can mean without storage in the actor. If the environment retains a distinction, the coupled system has a storage carrier. “Amnesic” means no internal historical state beyond the declared current variables, not literally absence of all state.

## Graph threshold: argument failure and narrower valid boundary

For an undirected simple connected graph with M edges, stationary directed traversal probability pi_i*P_ij is 1/(2M). Its stationary recurrence interval is 2M when the event is defined as an oriented traversal. An undirected traversal event has probability 1/M and interval M. The displayed equality that inserts an additional 2M numerator into 1/pi(e) is algebraically inconsistent. These recurrence quantities are not automatically hitting times from arbitrary starting states.

The single-edge feedback calculation freezes the node distribution, omits softmax cross-edge derivatives and induced changes in visitation, and does not specify a complete equilibrium. Continuous deposition makes a zero field generally not an equilibrium. The proposed graph-wide formula obtained by appending alpha*lambda_max and a minimum degree factor is not derived from the coupled Jacobian. Undefined edge-Laplacian conventions add another ambiguity.

For a specified closed expected-field map with visitation functional r(E), a candidate linearization is J=gamma*I-alpha*L+w*Dr(E*). Discrete-time local stability is tested by its spectral radius under appropriate regularity and closure assumptions. A walker–field system may require linearizing the joint distribution/operator instead; an instantaneous stationary r(E) is itself a modeling assumption. Neither condition proves permanent freezing.

The earlier two-route expectation map has an actual local symmetry-breaking condition gamma+w*beta/2=1 at zero contrast. That specific condition explains its control and rebound. It cannot be promoted into an exact threshold for every graph or translated substrate.

## A counterexample to finite-persistence permanent freezing

Take the supplied alpha=0 case, zero initial field, 0<=gamma<1, finite beta, bounded deposit w, and a finite connected graph. Every edge field obeys 0<=E_t(e)<=w/(1-gamma). Therefore each available outgoing edge has probability at least exp(-beta*w/(1-gamma))/d_i. This lower bound is positive. No available edge becomes an exactly forbidden transition merely by reinforcement in this regime.

One can obtain severe finite-horizon channeling while retaining all transitions. This bound alone does not establish a unique stationary law or rapid mixing for the full coupled process. Exact removal needs additional conditions: an explicit topology-changing rule, a singular parameter limit, an absorbing state, or a separately established mechanism. Saturation at a finite value does not produce an infinite barrier. Gamma=1 can retain total deposited mass without proving divergent gradients; diffusion can erase contrasts while preserving a uniform mode.

The integrated geometric relaxation sum is 1/(1-gamma). An e-folding time is -1/log(gamma), and a half-life is log(1/2)/log(gamma). They have related asymptotics but are different quantities. Comparing a return interval with relaxation is a useful heuristic, not a sufficient bifurcation or permanence theorem.

## Defect and control

The quotient/transition discrepancy is an intertwining defect between different spaces, not an ordinary commutator [q,T]. Its value depends on q, the macro-model, discrepancy measure, horizon, interventions, and comparison set. If the macro-model is changed after crystallization, a lower defect is not an unchanged-measure comparison. No universal spike-and-drop order parameter has been established.

At beta=0, reinforcement loses its preferential routing, but deposits still occur. Under stationary uniform directed-edge traversal, expected field approaches w/[2M(1-gamma)] rather than zero. Individual field levels decay only when above the relevant balance; contrast can dissipate without all field mass vanishing.

Increasing explicit discrete diffusion is not unconditionally stabilizing: a field mode has multiplier gamma-alpha*lambda. For gamma=.9, alpha=1, lambda=2, this is -1.1 and grows in magnitude. A positivity-preserving discretization requires additional step-size conditions. A logarithmic beta schedule needs problem-specific conditions; its written form does not guarantee exploration, melting, or stability. Comparing a field magnitude with gamma_c also mixes different quantities.

## Optimizer translation: candidate, not inherited theorem

The scalar gradient-descent condition 0<eta*lambda<2 governs contraction of a positive-curvature quadratic mode. It is not a crystallization criterion, and Adam/AdamW with moments and preconditioning do not inherit it unchanged. Small learning rates need not imply sharp minima; stationary parameters need not imply topological partition.

Learning rate, sampling temperature, momentum, coordinate smoothing, SAM, and dropout perform different operations. SAM's local loss maximization is not Laplacian diffusion. Neighboring tensor channels need a justified geometry: arbitrary channel permutations can preserve a network function but change an adjacency-based smoothing operation.

For equal normalized averaging weights, mean-square <= second moment. Different beta1/beta2 kernels do not supply that inequality. With defaults .9/.999, 999 zero gradients followed by one gives bias-corrected S approximately 6.323, outside the claimed [0,1]. Alternating +/-1 gradients give S approximately .00277 after 1000 steps: oscillation need not make S approach one. The second raw moment v is not itself the gradient variance.

Even if S were clipped at one, the stated default learning-rate shrink is only about .756 of the base rate. Without a curvature measurement or bound, that cannot guarantee arbitrary-curvature stability. sqrt(v)/(|W|+eps) is not a Hessian spectral upper bound: gradients can vanish at a quadratic optimum with arbitrarily large Hessian. The supplied code does not implement that curvature proxy or an explicit target gamma*=.99 feedback check.

Both PyTorch snippets pass a tensor adaptive_lr as addcdiv_'s scalar value argument. As written, this conflicts with that method's scalar-value interface for nonscalar parameters; the code was not executed here. An elementwise update expression could repair execution without validating convergence, saddle escape rates, ravine escape, or SAM-like generalization. The diffused version smooths m_hat along a periodically wrapped tensor axis; it does not implement the stated two-dimensional gradient convolution.

## Transformer translation: already-separated operations must stay separate

Standard output sampling temperature rescales final output logits after the model forward pass. It does not directly set attention softmax temperature or alter existing keys and values for a fixed supplied prefix. It can change sampled tokens, which then change later context indirectly. The previously supplied context-swap protocol correctly separates these operations; this new seed's direct identification reintroduces the confusion that protocol could test.

Attention weights route values; they are not the final token distribution. A large attention weight, an attention sink, an in-context rule, and repetitive generation are not interchangeable observables. Finite output temperature with finite unmasked logits leaves positive support; hard top-k/top-p filtering is a different intervention. Cache eviction, context deletion, score soft-capping, repetition penalties, and diffusion require their own preservation/repair tests. Frozen weights define a fixed model function, not an unalterable physical law.

## Recorded contact and status

Six constructed checks are saved in `evaluation/results/wake-seed-checks-2026-10-05.json`. They test formulas and counterexamples, not optimizer performance or neural mechanisms. The strongest remaining candidate is horizon- and intervention-relative durability of environmental constraints. The graph-wide theorem, universal defect curve, optimizer guarantees, and exact substrate equivalences remain unsupported; individual counterexamples contradict specific unconditional claims without closing neighboring models.

Runtime 0.2 and inquiry schema 0.1 remain unchanged. Reopen the optimizer branch with corrected executable code, a declared workload, simple baselines, and separately held-out performance. Reopen hard crystallization with an explicit mechanism that changes accessibility, rather than naming a long-lived bias a permanent law.
