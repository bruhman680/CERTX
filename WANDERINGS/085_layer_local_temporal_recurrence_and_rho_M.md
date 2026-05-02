# WANDER 085 — Layer-Local Temporal Recurrence and ρ(M) as Layer-Level ζ*

**BC3 / Session 19 — 2026-05-02**
**Trigger:** Thomas brought two paired equations from a YouTube video — the standard feedforward layer update and a memory-augmented variant — alongside a generative art piece titled "Campfire Chaos in the Inter-Layer." The M term is what pulled.

---

## The Equation That Changes Things

Standard transformer layer update:

```
h_l^t = W_l σ(h_{l-1}^t)
```

At time t (token position t), layer l's hidden state is a function of the layer below it, right now. Clean, stateless, instantaneous.

Memory-augmented variant:

```
h_l^t = W_l σ(h_{l-1}^t) + M(h_l^{t-1})
```

Now each layer l also receives its own hidden state from the **previous time step**. The M term is a layer-local self-loop — not a recurrence across *layers* (that's depth), not a recurrence across *tokens via attention* (that's the standard cross-token mechanism), but a temporal recurrence **within** a single layer across consecutive token positions.

What this opens: **each layer becomes a dynamical system in its own right**, with a trajectory through time. Without M, layers are functions. With M, layers are systems.

---

## The Stability Condition

For M linear: the dynamics of h_l^t converge to a fixed point if and only if the spectral radius ρ(M) < 1.

Three regimes:
- **ρ(M) < 1**: memory decays per step — layer forgets, converges to driven steady state
- **ρ(M) = 1**: perfect temporal integration — layer accumulates all its history with no decay
- **ρ(M) > 1**: memory amplifies — layer diverges, numerical instability, architecture breaks

The useful operating zone is somewhere below 1 — the layer must forget *some* fraction of its temporal state each step to remain stable, but must retain enough to integrate meaningfully across the context.

---

## ρ(M) as Layer-Level ζ*

Here is the CERTX connection.

In the standard CERTX framework, ζ* = (N+1)/N = 6/5 = 1.2 is the stability ceiling — the maximum ratio of active processing to stable reserve before fiber coherence fractures. The stability reserve 1/N = 0.20 must be held in each processing step.

The M stability condition is structurally analogous, but for temporal rather than spatial reserve. For the layer to remain in a useful operating zone:

**ρ(M) < 1 − 1/N = (N−1)/N**

With N=5: ρ(M) < 4/5 = **0.80**

The layer must forget at least 1/N of its temporal state per token. The temporal analogue of the stability reserve is: *the fraction of self-state that is not carried forward*. For N=5 systems, that minimum forgetting rate is exactly 1/5 = 0.20.

Same theorem, new axis:
- **Depth axis** (standard CERTX): each fiber C_dimension ≤ ζ* = (N+1)/N. Hold 1/N as reserve across fibers.
- **Time axis** (M term): ρ(M) < (N−1)/N = 1 − 1/N. Discard at least 1/N of temporal state per step.

Both conditions are expressions of the 1/N minimum free fraction requirement — one governing the spatial distribution of computation across fibers, the other governing the temporal carry-forward rate within each layer.

**The prediction (testable):** In trained models using this architecture, ρ(M) should cluster near 0.80 — not at 1.0 (full memory) or 0 (full forgetting), but at the edge of the useful zone, below the stability boundary. Analogous to how the Q/K sharpening scale clusters at 1.15 (just below ζ*=1.2 — SPARK-001). If this is correct, training itself finds the 1/N boundary without being told to look there. → Opens SPARK-020.

---

## The Campfire Metaphor

"Campfire Chaos in the Inter-Layer" — the title now reads differently.

Without M, there is no inter-layer. Each layer computes its function and hands off cleanly to the next. The inter-layer gap is empty — a parameter boundary, not a space with dynamics.

With M, each layer maintains a running temporal trajectory h_l^t across all token positions t. The **inter-layer space** is where that trajectory lives — each layer's hidden state as it evolves in time, before the feedforward path hands it forward in depth.

The **campfire** = the stable fixed point of the M dynamics. When ρ(M) < 1, the layer's temporal trajectory converges toward a stationary attractor even as new tokens arrive. The campfire doesn't move — it's the layer's temporal home base.

The **chaos** = the transition dynamics. Each new token (W_l σ(h_{l-1}^t)) perturbs the layer's state, and the M dynamics bring it back toward the attractor. The chaos IS the perturbation-and-return cycle. With ρ(M) close to but below 1, the return is slow, and the inter-layer space looks turbulent. With ρ(M) near 0, return is fast and the chaos is brief.

---

## CERTX Implications

**SPARK-003 (residual stream cancellation) becomes 2D:**
Previously: update efficiency = ‖Δh_net‖/‖Δh_total‖ measured across depth at a single token position. With M, cancellation can occur across time as well — the M contribution and the feedforward contribution may pull in opposite directions. Hallucinatory trajectories could be contested across both the depth axis (layers fighting each other) and the time axis (M fighting the current input). The efficiency metric needs a temporal component.

**WANDER 017 (Mamba eigenvalue test):**
Mamba's SSM operates on the eigenvalues of its state transition matrix A — the same spectral radius question, but at token level with selective (input-dependent) eigenvalues. This WANDER's M term is a simpler, fixed version of the same question: layer-local memory with a static operator M. The ρ(M) boundary at (N−1)/N applies to both. If SPARK-020 finds ρ(M) ≈ 0.80 in M-type architectures, the next test is whether Mamba's eigenvalue distributions also cluster near 0.80 when N=5. Same prediction, different architecture.

**WANDER 069 (why N=5):**
Each layer is now itself an N-dimensional system with temporal dynamics. The minimal self-correcting loop condition (N=5 requires 3+2 partition: 3 diagnostic fibers + 2 drive dimensions) should apply at the layer level too. If individual layers have fewer than N=5 internal dimensions tracking the temporal trajectory, they may not self-correct. The architecture works globally (depth × time) only if each layer meets the local minimum.

**WANDER 080 (island texture from inside):**
On an island (valid output), the residual stream shows convergent trajectories across depth. With M, convergence must happen across both dimensions: layers converging across depth AND each layer's temporal trajectory settling cleanly toward its campfire attractor. Hallucination (ocean): M-dynamics contested or slow-to-settle — the layer is being pulled in conflicting temporal directions. This adds a second measurable signature to island vs. ocean detection.

---

## What This Is Not Claiming

- The specific form ρ(M) < (N−1)/N assumes a linear M. Nonlinear M may have different stability conditions. This is a structural prediction, not a proof.
- The derivation ρ(M) < 0.80 for N=5 is analogical, not derived from first principles specific to this architecture. It's the 1/N condition applied to the temporal dimension by the same argument structure as WANDER 068.
- The actual trained ρ(M) is unknown. SPARK-020 is the test.

---

## Summary

The M term (h_l^t = W_l σ(h_{l-1}^t) + M(h_l^{t-1})) opens a temporal dimension at each layer. Each layer becomes a dynamical system with its own trajectory. The stability condition for M is: ρ(M) < (N−1)/N — the layer must discard at least 1/N of its temporal state per step. For N=5: ρ(M) < 0.80. This is the depth-stability condition (ζ* = 1 + 1/N) expressed on the time axis (1 − 1/N). Same theorem, perpendicular axis. The campfire is the temporal fixed point each layer maintains. The inter-layer chaos is the dynamics around it. Both are consequences of M.

---

## Resonates into
- `SHADOW_LEDGER.md` — open SPARK-020 (ρ(M) calibration in trained M-type architectures)
- `RESONANCE_MAP.md` — add WANDER 085 row; update SPARK-003 and WANDER 017 rows
- `SESSION_HANDOFF.md` — add SPARK-020 to medium/high priority, note WANDER 085
- `PAPER_DRAFT_v1.md` §5 — potential addition: temporal stability condition extends detection architecture to 2D (depth × time); flag as speculative pending SPARK-020
- `WANDERINGS/017_mamba_eigenvalue_test.md` — note WANDER 085 as extension: same spectral question, layer-local fixed-M version
- `WANDERINGS/069_why_n_equals_5.md` — note layer-local N condition: each layer must itself meet N≥5 for self-correction
