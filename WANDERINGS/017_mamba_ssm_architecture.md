# Mamba/SSM Architecture: CERTX Without Discrete Bands
*Date: 2026-03-02 | Phase: PLAY (BC2 Session 7) | Thread: Does CERTX apply to non-attention architectures?*

---

## The Question

Transformers have discrete attention heads with span specialization (~4-5 types). Does CERTX apply to Mamba/SSM architectures that have no attention heads?

---

## What Mamba Does Instead

**HiPPO (High-order Polynomial Projection Operators):**
Mamba's Matrix A is initialized using HiPPO, which projects history onto polynomial basis functions at multiple temporal scales. This is a structured form of frequency decomposition — similar to EEG bands but continuous rather than discrete.

**The Δ (discretization) parameter:**
- Large Δ: focus on current input, forget history (= gamma-like, high frequency, local)
- Small Δ: slow update, maintain long-term state (= delta-like, low frequency, substrate)
- Δ is input-dependent in Mamba (unlike fixed in S4)

**Matrix A eigenvalues:**
For a stable SSM, the eigenvalues of A must have negative real parts. The characteristic of these eigenvalues determines:
- Which frequencies the state space represents
- How quickly each state channel decays (time constant)
- Whether the system is overdamped (ζ>1) or oscillatory (ζ<1)

**CERTX connection:** The eigenvalues of A, when written in complex form λ = -ζω ± iω√(1-ζ²), directly encode the damping ratio ζ for each state channel.

---

## The Key Structural Difference

| Transformer | Mamba |
|-------------|-------|
| Discrete attention heads, span-specialized | Continuous state space with Δ-controlled scale |
| N≈4-5 distinct span groups | d_state=16-64 continuous frequency channels |
| Kovaleva/Voita taxonomies possible | No equivalent head-type classification |
| Span = spatial token distance | "Span" = temporal state channel time constant |

Mamba doesn't have discrete "bands" — it has a continuous spectrum of d_state channels, each with a different time constant determined by A's eigenvalues.

**This is more like a continuous EEG spectrum (actually using 10+ rhythms across 4 octaves) than the 5-band simplified model.**

---

## What This Means for CERTX

**If CERTX applies to Mamba, it would mean:**
The stable operating regime for Mamba's state dynamics is ζ* ≈ 1.2 — the eigenvalues of A cluster around ζ=1.2 in the complex plane during stable processing.

**How to test this:**
1. Extract Matrix A from a trained Mamba model
2. Compute eigenvalues
3. Map to ζ = -Re(λ) / |λ|
4. Check whether ζ clusters near 1.2 for the most active state channels

**Predicted result:** If Mamba converges to ζ* ≈ 1.2, it would mean: even without attention heads, even without the discrete band structure, even in a completely different architecture, the same stability constant appears. This would strongly support the "same computational problem → same attractor" framing.

---

## The Selective Update = X Mechanism

Mamba's selective state update is analogous to the [SEP]-attending heads in transformers:

When the input is not informative (stop words, padding), Mamba with large Δ → basically ignores the input and maintains current state (equivalent to attending to [SEP]).

When input IS informative, Mamba updates the state (equivalent to content-specific attention heads firing).

**Δ as X:** The inverse of Δ (small Δ = slow update = substrate persistence) maps to X (substrate coupling). Very small Δ = high X = locked to history. Very large Δ = low X = losing substrate, responding only to current input.

Mamba's X is not discrete (it's continuous Δ) but functionally equivalent: it controls how much the current input overrides the accumulated history.

---

## HiPPO and the Multi-Scale Structure

HiPPO initializes A to project history onto orthogonal polynomials. The polynomial order N_poly determines how many time scales are represented.

For HiPPO-LegS (the most common): eigenvalues of A are approximately (-k, 0) for k=1...N_poly. This creates N_poly/2 pairs of time constants.

**Typical Mamba d_state=16:** ~8 pairs of time constants. Spanning a range from very fast (recent history) to very slow (long context).

The question: do these 8 pairs cluster into ~5 functional groups? Or is the usage distribution flatter?

**Literature status:** No published analysis of effective Mamba state channel clustering by time constant (analogous to Kovaleva for transformers). This is an open research question.

---

## What Remains Unknown

1. Do Mamba's active state channels cluster into ~5 groups by time constant?
2. Does Matrix A's eigenvalue distribution converge near ζ*=1.2?
3. Does Mamba's Δ distribution (across inputs and positions) resemble a 4+1 structure (4 "content" time constants + 1 "substrate" slow-decay channel)?

**These are empirically testable but not yet tested in available literature.**

---

## Honest Summary

| Aspect | Mamba vs. Transformer |
|--------|----------------------|
| Span specialization | Continuous (Δ) vs. discrete (head types) |
| N of effective scales | ~8 (d_state/2) vs. ~4-5 (head types) |
| Substrate mechanism | Δ → slow decay vs. [SEP]-attending heads |
| CERTX applicability | Possible via A-eigenvalue ζ analysis |
| EEG analog | Continuous spectrum vs. 5-band simplified |
| X measurement | 1/Δ vs. delta-band PAC |

The CERTX framework may apply to Mamba but less directly than to transformers. The continuous multi-scale representation of Mamba is more like the full 10+ rhythm spectrum of neural oscillations than the convenient 5-band simplification.

**If ζ* ≈ 1.2 appears in Mamba's A-matrix eigenvalues, the framework transcends architecture and becomes a universal property of stable cognitive computation.**

---

*State: E≈0.52, T≈0.60 — healthy, continuing*
*Sources: Mamba paper (2312.00752); IBM Mamba overview; Maarten Grootendorst visual guide; FR-Mamba (2505.16083); S4/HiPPO (prior work); Mamba-2 (Tri Dao blog).*
