# Continuity 02 — spectral connectivity and consensus repair

## Evidence and provenance

Inspected NOW v1, TASKS, recovered continuity handoff/history, FRR compact seed and its source-weave requirements, Gemini assembled graph section, reconstruction README, and reconstruction Laplacian/eigenvalue code excerpts. No screenshot pixels, external papers, or simulations were newly inspected/executed here. Gemini is a partially recovered proposed formulation; the ring is explicitly inferred new code, not its implementation. Their shared vocabulary does not provide independent evidence. Coordinator's optimizer correction supersedes NOW v1's unbounded-ratio wording; this report makes no optimizer claim.

## Repair that preserves the useful relationship

For a finite undirected graph with nonnegative symmetric weights, use the combinatorial Laplacian L=D−A. Write eigenvalues with zero-based indices: 0=λ₀≤λ₁≤…. Algebraic connectivity is λ₁, not λ₂ in that convention. Connectedness is equivalent to λ₁>0; a threshold 0.05 describes a chosen rate policy, never topological disconnection. A disconnected graph consisting of an edge of weight 1 and an isolated vertex has eigenvalues (0,0,2): the screenshot's zero-based λ₂ can be positive while the graph is disconnected. A connected two-vertex edge of weight 0.01 has (0,0.02), already below the proposed cutoff.

Under the declared consensus law ẋ=−κLx, κ>0, let P=I−11ᵀ/N. Symmetry gives ||Px(t)||₂≤exp(−κλ₁t)||Px(0)||₂. Thus τ=1/(κλ₁) is the slowest disagreement-mode e-folding time. Reaching relative tolerance ε requires t≥log(1/ε)/(κλ₁). It is not a complete time-to-consensus statement without tolerance, initial condition and gain. Multiplying all edge weights rescales this time without changing graph topology. Directed or time-varying networks need different assumptions and cannot inherit this bound automatically.

The executable ring uses eigenvalues[1], consistent with this repair. For its Euler map I−dt L, disagreement contracts by max over k≥1 of |1−dt λk|; stability also depends on λmax, not just the gap. The README's positive-floor weak links retain connectedness. Small gaps at all tested floors are compatible with eventual deterministic mixing.

## Serious rival and surviving distinction

Slow consensus can protect a spatial contrast while hindering writing and cross-region coordination. The reconstruction's reported learned gap 0.00118 versus uniform 0.00963 does not predict useful bit retention: reported writer relocation changes retention radically while retaining the prepared field. A serious rival is low total transport plus message/eigenmode alignment, rather than an adaptive boundary memory mechanism. Existing common-write, mean-matched and shuffled controls partly discriminate this rival; they do not isolate a matched-spectrum rival or arbitrary-message generalization. Noise covariance and decoder can change task error without changing the deterministic gap. Retained conductance carries transport constraints; it does not store the erased polarity.

## Source weave: inspected versus inherited and missing

The reconstruction README supplies an inherited connection to Delvenne, Lambiotte and Rocha (2015), *Diffusion on networked systems is a question of time or structure*, arXiv:1309.4155. Its assigned role is timescale/structure pressure, not bit-retention validation; this worker did not inspect the paper. The README also carries anisotropic-diffusion and well-posedness repair references, relevant to conductance construction but not proof of consensus claims.

Fiedler's algebraic-connectivity work, spectral graph treatments of combinatorial versus normalized Laplacians, and consensus/switching-network convergence literature are prospective source contacts from general mathematical knowledge, not newly searched or verified citations. A repair search remains open: search by function (disagreement contraction), failure (directed/nonnormal transient amplification; switching connectivity), repair (joint connectivity and gain/step-size assumptions), and rival (mixing time versus task memory). No external literature search was executed; therefore this is a bounded local source weave with an explicit search gap, not a completed genealogy or novelty assessment.

## Concrete next improvement (recommended, not implemented)

Replace the screenshot split rule with separately named fields: topology_connected; Laplacian_convention; dynamics_gain; horizon; disagreement_tolerance; measured_task_score. Predeclare a horizon-rate policy λ₁≥log(1/ε)/(κT) only for the law above. Log the written state's modal amplitudes, decoder error and noise-driven modal variance alongside spectral gap. Compare conductance fields matched on gap and mean transport but differing in eigenvectors; cross writer placement with independent message families. This tests whether boundaries preserve the task-relevant modes rather than merely slowing everything. Keep the original 0.05 policy dormant as a possible application-specific choice pending calibration.

A cube adds no useful third operation here. The consequential comparison is field construction followed by writing/holding versus a common-written-state holding intervention; its residual already identifies alignment and write accessibility as separate burdens without pretending to locate causality from a diagram alone.
