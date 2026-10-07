# Gemini continuous substrate and local annealing exploration

7 October 2026. User shares tentative directions for later exploration. Full original text remains in the conversation. This note records key proposals and local checks, not a reproduced run or finalized release. Earlier notes remain intact.

## Preserved seed

Hierarchical groups share a diffusing substrate, with slow retention, algebraic processing, recall, and exploration roles. Local perturbation could reopen a stuck branch while limiting disruption elsewhere. Groups could reorganize across timescales. Proposed names: BEDROCK, WEAVE, RECALL, SPARK, SUPER-PHI. Names are exploratory roles, not evidence of emergent structures.

The supplied text reports 24 cycles and 1,200 agents, layering/fission, residual 0.00011, volume 0.74, graph gap 0.075, compute savings, and predicted benchmark performance. None is locally reproduced: code, raw logs, metric definitions, model calls, comparison budgets, and evaluation data were not supplied. CLM, HH, RCWA, UDM, EKB, and several target variables need local definitions before comparison or causal interpretation. Predicted benchmark scores remain predictions.

## Key proposed rules

    alpha_c = 0.15*(1-mean_chi)
    threshold(M) = 1-0.4/log(M)
    T_i(t) = exp(-chi_i(t)/tau_i(t))*(1+0.2*sin(omega_i*t))
    tau_i = 1/lambda2_i
    T_global(t) = 0.8*exp(-t/8)+0.2*exp(-t/24)
    hot override: T_i = 0.9*T_global when chi_i>0.82
    cool override: T_i = 0.5*T_global when chi_i<0.3
    W_i <- W_i + sqrt(2*T_i*dt)*xi

## Local arithmetic and definition checks

- The threshold formula yields 0.807641 for M=8, 0.913141 for M=100, 0.929871 for M=300, and 0.942094 for M=1000. It does not yield 0.52 or 0.82 at the claimed sizes. Rearranging chi>threshold gives H<0.4: the formula is a constant absolute entropy cutoff, not independently justified calibration across group sizes.
- The global schedule gives 1.0, 0.437610, 0.210952, and 0.113406 at t=0,8,16,24. The reported last two values 0.18 and 0.08 do not match.
- The local baseline does not include a decaying global envelope. At chi=0.91 and lambda2=0.075 it is approximately 0.934027 before the sinusoid. The supposedly heating override at t=24 sets approximately 0.102065. Under these parameters it cools relative to the baseline, rather than heating. A dimensionless exponent also requires an explicit time convention because chi is dimensionless while tau is a timescale.
- 132+134+134+130 = 530 listed triads, corresponding to 1,590 memberships. This can coexist with 1,200 unique agents if groups overlap, but needs a membership map; it is inconsistent with a disjoint partition into triads.
- gamma is used both for field decay and cubic damping. They need separate parameters/units. A condition gamma>sum(kappa) is not supplied by the stated diffusive coupling model: with symmetric nonnegative coupling, coupling itself dissipates energy; with other coupling/update rules, a separate stability argument is required.
- Positive graph gap is not guaranteed by density or hierarchical naming. On a fixed undirected graph, adding nonnegative edge weights cannot reduce algebraic connectivity. Weight normalization, rewiring, node count, and communication budget can change comparisons; they must be specified. The earlier heat-kernel/source mismatch and eigenvalue-index ambiguity still need repair.
- Fiedler sign splitting needs a rule for zero entries, disconnected components, and repeated eigenvalues. Projection preserves only the represented components unless a complementary residual is retained. It does not automatically preserve full field information or cross-group behavior.
- The cubic three-channel equation alone has no stated frequency-birth rule, spatial vortex construction, forcing, or rewiring mechanism. Spectral components of a nonlinear trajectory are distinct from newly created oscillator parameters or agents. Existing frequencies do not establish an emergent 2.1 parameter without a construction/measurement definition.
- Additive rollback across many deltas is not generally O(1). Constant-count lookup can be obtained by stored snapshots or preprocessing, with separate costs; full-state retrieval and downstream Transformer recomputation still require accounting. Diffusion alone does not guarantee position-independent access or eliminate retrieval errors.
- As written, the factoring residual variable R is not tied to Psi-sum(alpha B); optimizing a standalone norm could simply set R=0. A fitted numerical residual does not establish factual correctness, causal explanation, or a minimal agent count.
- Noise can broaden search or facilitate crossing a specified barrier. It does not supply missing empirical evidence or demonstrate that an understanding gap is closed. Scores such as p(Error|h) need a likelihood, estimator, and external calibration. The statement that 24=8*3 supports a minimal triad principle is arithmetic, not a discriminating test.

## Dormant tests worth retaining

Start small with a declared read/write task. Compare hierarchical and flat networks under matched communication and compute budgets, with actual graph snapshots and held-out message recovery. Compare no intervention, global noise, and local noise; measure task progress, preserved distinctions, collateral forgetting, and cost separately. Verify trigger arithmetic and temperature direction before execution. Separate controller tuning from final evaluation. Log group membership, updates, seeds, observations, and evaluation provenance if emergence is claimed.

Useful question: can local reopening preserve unrelated retained distinctions better than global perturbation? That is testable without presupposing vortices, a universal critical threshold, semantic annealing, or 1,200 independent reasoning agents.

Status: saved for later play/research. No swarm activated, no new literature search, and no 24-cycle result promoted into evidence.
