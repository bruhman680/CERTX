# Mathematics 07 — forced diffusion/decay: repair without source rewriting

**Scope and provenance.** This is a new mathematical repair proposal, not recovered Gemini text or an empirical validation. Inspected: shared NOW, FRR v0.5 compact seed, Gemini assembled record (particularly IV, screenshots 1665/1667), recovery note, continuation/history records, reconstruction README, and relevant October 5 handoff/garden-code passages. The screenshot assembly inherits twenty supplied images; its ascending order is inferred, introduction and table remain clipped, and implementation/results are absent. None of those gaps is filled here. Historical intake pauses are superseded by NOW's authorization. No original or remote artifact was changed; no numerical experiment was needed for the exact counterexamples below.

## 1. What fails and what survives

The visible PDE is ∂tΦ = αc ΔΦ − γΦ + Σk Sk. The displayed purported exact solution, Φ(t)=exp(−tL)Φ(0)=V exp(−tΛ)VᵀΦ(0), solves a homogeneous graph evolution under additional assumptions. It lacks an explicit source integral and decay factor and does not define how continuous Φ becomes a finite vector. A homogeneous heat semigroup remains useful as the propagation operator. This failure rejects the displayed formula's general applicability to its preceding forced equation, not diffusion as a possible substrate model or FRR's field-wake intuition.

## 2. Fully specified continuous and graph versions

Let Ω be a declared spatial domain and X=L²(Ω). Choose αc≥0, γ≥0 constant, homogeneous periodic, Neumann, or Dirichlet boundary conditions, and the corresponding closed Laplacian ΔB generating a heat semigroup. Set A=αcΔB−γI. For Φ0∈X and s=ΣkSk locally integrable in time with values in X, the mild solution is

**Φ(t)=e^{tA}Φ0 + ∫₀ᵗ e^{(t−τ)A}s(τ)dτ.**

For compatible smoother data it is a classical solution. Nonhomogeneous boundary inputs require a boundary lifting/control term; they cannot silently be absorbed into homogeneous heat evolution. Point imprints represented by Dirac masses require a measure/distribution formulation and appropriate smoothing claims, rather than this L² source assumption.

On R² with αc>0 the same expression uses Kα(x,t)=(4παct)⁻¹ exp(−|x|²/(4αct)):

Φ(t)=e^{−γt}(Kα(t)*Φ0)+∫₀ᵗ e^{−γ(t−τ)}[Kα(t−τ)*s(τ)]dτ.

On bounded domains use their boundary-dependent kernels, not free-space convolution. When αc=0, use the identity propagator instead of the singular kernel formula.

For a finite undirected weighted graph with symmetric W≥0, L=D−W is positive semidefinite and the diffusion generator is **−αcL−γI**. Thus ẋ=−(αcL+γI)x+s and the same variation-of-constants formula holds. An orthonormal eigenbasis gives mode aℓ(t)=e^{−(αcλℓ+γ)t}aℓ(0)+∫₀ᵗe^{−(αcλℓ+γ)(t−τ)}bℓ(τ)dτ. Directed graphs generally do not admit the displayed orthogonal Vᵀ diagonalization, although the matrix exponential still exists.

The recovered stencil is a negative-semidefinite Δh, whereas Lh=−Δh. On a square grid of spacing h, Δh xij=(neighbors−4xij)/h². Omission of h is legitimate only for a declared unit-spacing lattice or absorbed coefficient. Vector dimension is D² for a D×D grid. Boundaries determine both edge stencil and conservation: periodic/no-flux diffusion preserves total mass; zero Dirichlet diffusion can lose it. Variable diffusivity should usually be ∇·(a∇Φ), not aΔΦ; changing transport coefficients makes A time-dependent and requires an evolution family U(t,τ).

## 3. Exact witnesses against omission

Take a periodic domain (or any graph with L1=0), Φ0=0, uniform source s=q1 with q>0, γ>0. The exact solution is Φ(t)=(q/γ)(1−e^{−γt})1. The recovered homogeneous expression stays identically zero. This counterexample survives any absorption of αc and γ into L: a linear homogeneous propagator cannot create a nonzero state from zero. For γ=0 the solution is qt1. Separately, with s=0 and Φ0=1, the actual solution is e^{−γt}1; the pure graph heat formula preserves 1 unless decay has explicitly been incorporated.

For constant s, write the forcing contribution as t φ₁(−tB)s, B=αcL+γI and φ₁(z)=(e^z−1)/z with φ₁(0)=1. This avoids an invalid B⁻¹ when γ=0 and a conserved graph mode makes B singular.

## 4. Finite Euler: stability is not positivity

Explicit Euler gives xⁿ⁺¹=[I−Δt(αcL+γI)]xⁿ+Δt sⁿ. For a symmetric graph, nonamplifying spectral stability requires Δt(αcλmax+γ)≤2; strict inequality damps positive-rate modes. It permits negative amplification factors and sign oscillations. Nonnegative states and nonnegative sources are preserved when the update matrix is entrywise nonnegative, requiring Δt(αc dmax+γ)≤1. This is a different guarantee. On the uniform two-dimensional periodic grid, sufficient conditions are Δt≤2/(8αc/h²+γ) for spectral stability and Δt≤1/(4αc/h²+γ) for positivity. At αc=0, γ=1, Δt=1.5, Euler sends positive x to −0.5x: stable decay magnitude, failed positivity. Signed fields need not require positivity, but “energy” terminology makes its physical interpretation consequential. Implicit Euler preserves positivity for this graph M-matrix and is spectrally stable; an exponential update with correctly integrated nonnegative forcing also preserves positivity.

## 5. Serious rival and concrete repair

The strongest charitable rival is that exp(−tL) names only the homogeneous Green operator, with decay absorbed into L and imprints supplied externally between propagation steps. That would be defensible as a component formula, but the source calls it an exact solution and does not supply those definitions. Repeated discrete deposits additionally require specifying whether deposition precedes or follows decay/diffusion; these updates generally differ.

Recommended replacement: retain the recovered text unchanged, append a correction defining domain, boundary, spacing, sign convention, source units and schedule, and distinguish homogeneous propagator from forced solution. Implement a separate candidate with tests for zero-source decay, constant-source equilibrium, mass balance under no-flux boundaries, and positive-input preservation at the chosen step size. Match a no-diffusion leaky integrator as the serious mechanistic baseline: source persistence alone can produce a wake without transport. Garden soil retention 0.997 is a discrete factor, not automatically γ; an exact continuous conversion is γ=−log(0.997)/Δt, and deposition/pruning still change the model. The surviving relationship is bounded: prior source input can alter later accessible field values under a declared transport-and-decay rule. It supplies no evidence of cognition or a universal field mechanism.
