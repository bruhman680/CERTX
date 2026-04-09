# WANDER 050: Thermodynamic Cost of Hallucination — Hypothesis and Open Derivation

*Phase: PLAY (BC3 Session 8) | Status: Hypothesis — derivation open*
*Origin: Thomas's cross-model exploration with Gemini/autonomous audit concept.
 Connects to: WANDER 008 (Landauer Conjecture, open), WANDER 049 (geometric fibers)*
*Honest flag: No specific number (e.g., 14.2%) has been derived here. Any such
 number from prior AI explorations is unverified and should not be cited.*

---

## The Question

WANDER 008 opened the Landauer Conjecture: if truth is thermodynamically cheaper than
lies, what does this mean for AI systems that hallucinate?

The claim surfaced again in this session from a cross-model audit: "Integrated Truth
requires 14.2% less internal energy than a fragmented lie." This number is not derived
in any of our prior work. It arrived without methodology.

This WANDER does not claim that number. What it does: restates the conjecture honestly,
identifies what an actual derivation would require, and sharpens the connection to the
fiber framework.

---

## What Landauer's Principle Actually Says

Landauer's principle (1961, verified experimentally by Bérut et al. 2012) states:

> The minimum energy dissipated to irreversibly erase one bit of information is
> kT ln(2) ≈ 2.85 × 10^{-21} J at room temperature.

This is a hard physical lower bound on information erasure in any classical or
quantum system. It's not about computational efficiency or software architecture.
It's about the thermodynamics of information at the bit level.

Applied to AI reasoning, the direct use of Landauer's principle requires:
1. Identifying which operations in forward-pass computation involve irreversible
   information erasure
2. Counting the number of such operations per token generated
3. Comparing that count between hallucinated and non-hallucinated outputs

None of these steps have been completed for transformer forward-pass computation.
The 14.2% figure in the cross-model exploration has no derivation attached.

---

## The Hypothesis That's Actually Worth Pursuing

Landauer's principle is the formal grounding, but the intuitive hypothesis is this:

**Hallucinations require more internal "correction work" than truthful outputs,
because they create conflicts that the residual stream continuously attempts to
resolve.**

This is not the same as claiming hallucinations cost more energy per se. It's a
claim about the *computational structure* of the forward pass during hallucination:

During a truthful generation trajectory:
- The residual stream accumulates corrections that all point in compatible directions
- Each layer's updates reinforce the previous ones
- The trajectory converges smoothly

During a hallucination trajectory (specifically Regime B — confident wrong):
- The residual stream has internalized an incorrect coordinate
- Subsequent layers may "see" the conflict between the trajectory and the broader
  contextual substrate (X)
- Some correction forces will point toward the correct answer, others toward the
  incorrect one already committed to
- The trajectory is internally contested

**The prediction:** in hallucination-generating forward passes, there is more
*cancellation* in the residual stream updates — more vectors that partially cancel
each other — compared to truthful passes. This is not an energy argument per se;
it's a computational efficiency argument. Contested trajectories waste update capacity.

This is measurable: compute the mean vector magnitude of residual stream updates
across layers, separately for hallucinated and non-hallucinated outputs. If hallucination
involves more cancellation, the effective magnitude (net update per layer) will be
lower relative to the Frobenius norm (total update magnitude). More computation for
less result.

---

## The Fiber Connection

From WANDER 049: hallucinations are trajectory failures at one of three geometric
constraints:
- C_symb failure: trajectory left the topic manifold
- C_struct failure: trajectory took an invalid edge
- C_num failure: trajectory landed at the wrong coordinate

Each failure type implies a different computational story:

**Type D (C_num failure — Regime B):**
The trajectory is on the correct manifold, following correct edges, but the coordinate
is wrong. This is where the thermodynamic argument is sharpest. The model has enough
correct context to "know" the right answer is nearby, but has committed to a wrong
coordinate. The substrate (X) pulls toward the correct answer; the current trajectory
is committed to the wrong one. This creates exactly the residual stream conflict
described above.

From a Landauer perspective: the model needs to "hold" a wrong coordinate against
the pull of its own substrate. This may require additional irreversible computation
relative to the case where the substrate and the trajectory agree.

**Type A (C_symb failure — Regime A):**
The trajectory has left the correct manifold. There is less conflict here because the
substrate in the wrong manifold may be internally consistent. A model generating
confident wrong output in the wrong semantic neighborhood may not experience internal
conflict — it's coherent in the wrong place. This would predict lower residual stream
cancellation for Type A, which makes it harder to detect thermodynamically even though
it produces qualitatively worse output (WANDER 048 confirmed Type A is worse quality).

**Prediction from this asymmetry:**
If the residual stream conflict hypothesis is right, Type D (Regime B, C_num failure)
should show more internal cancellation than Type A (Regime A, C_symb failure).
This matches the WANDER 048 finding that Type A is *worse quality* but perhaps *less
internally contested* — the model is confidently wrong in the wrong neighborhood.

---

## What "Truth is Cheaper" Would Mean if True

The intuitive claim: reasoning that arrives at a correct answer should, on average,
involve a more coherent residual stream trajectory — less cancellation, more
directional accumulation.

If this is true, it has a practical implication: the *magnitude efficiency* of the
residual stream (net update magnitude / total update magnitude, averaged across layers)
could be a proxy for output quality. A high-efficiency trajectory (updates reinforce
each other) would correlate with correct outputs. A low-efficiency trajectory (updates
cancel each other) would correlate with hallucination.

This is distinct from σ_fiber. σ_fiber is computed from the output text. Residual
stream magnitude efficiency is an internal measurement computed during the forward pass.
The two would be measuring the same underlying phenomenon from different observation
points: inside and outside.

If they correlate well, that is a significant result: it would show that the text-level
σ_fiber signal has an internal structural correlate, and that the geometric picture
(WANDER 049) is not just an analogy but a prediction about internal activation dynamics.

---

## What a Formal Derivation Would Require

To move from hypothesis to result, we need:

1. **A precise definition of "irreversible computation" in transformer forward passes.**
   Attention softmax is a many-to-one operation (irreversible). Layer normalization
   involves division by a value derived from the input (potentially irreversible).
   Linear projections are reversible when the weight matrix is full-rank. A careful
   accounting of which operations are irreversible is required.

2. **A count of irreversible operations per hallucinated vs. non-hallucinated token.**
   This requires access to intermediate activations during generation, not just outputs.

3. **A Landauer bound computation from that count.**
   Once irreversible operation counts are known, kT ln(2) per erasure gives a minimum
   dissipation. Comparing hallucinated vs. truthful sequences gives a ratio.

4. **Calibration against actual energy measurements.**
   The Landauer bound is a theoretical minimum. Real transformers dissipate far more
   energy due to non-ideal implementations. The ratio between hallucinated and
   non-hallucinated may be consistent across implementation scales even if the
   absolute numbers are not at the Landauer minimum.

None of these have been completed. The hypothesis is plausible and the experimental
path is clear, but no number belongs in the paper until step 3 is done.

---

## Connection to WANDER 008

WANDER 008 opened the Landauer Conjecture as an open question. This WANDER sharpens it:

**WANDER 008 (original conjecture):** Is truth thermodynamically cheaper than lies
for AI systems?

**WANDER 050 (sharpened form):** Specifically, does residual stream update cancellation
increase during hallucination, and if so, does this cancellation excess correspond to
a Landauer-measurable irreversibility cost?

The sharpened form is more falsifiable and more grounded in the mechanics of transformer
computation. It also connects to a measurable quantity (residual stream update
efficiency) that doesn't require full Landauer accounting — it's a proxy that could
be tested with existing interpretability tools.

---

## Shadow Ledger Addition

This WANDER opens a new experiment candidate:

**SPARK-003: Residual stream cancellation vs. hallucination**
- Track per-layer residual stream update magnitude and direction for matched
  hallucinated/non-hallucinated outputs from the same model
- Compute update efficiency = ‖Δh_net‖ / ‖Δh_total‖ across layers
  (net displacement / sum of all individual update magnitudes)
- Test: is update efficiency lower during hallucination-generating passes?
- Blocking dependency: open-weight model with residual stream access (Llama, Mistral)
- Note: shared blocking dependency with WANDER 049's trajectory curvature experiment —
  both require residual stream access. Can be run together.

---

## What Not to Claim

The following numbers have no derivation in our framework and should not be cited:
- "14.2% less energy for truthful outputs" — Gemini cross-model audit, no methodology
- "ζ* → 1.08 as N→∞" — limit of (N+1)/N as N→∞ is 1.0, not 1.08; the 1.08 is
  ungrounded (this appeared in the same session)

These have the same character as r = 0.989 before retraction. The concepts are
interesting. The specific numbers are not ours to use.

---

## Open Questions

1. **Residual stream cancellation:** Is there measurable difference in update
   efficiency between hallucinated and non-hallucinated forward passes?

2. **Type A vs. Type D:** Does the thermodynamic hypothesis predict that Regime B
   (C_num failure) is more "conflicted" internally than Regime A (C_symb failure)?
   This would be a novel prediction that follows from the geometric account but
   isn't directly testable with current surface-level tools.

3. **The efficiency ceiling:** Is there a maximum possible update efficiency in a
   transformer, and does it correspond to a known measure (e.g., the Frobenius norm
   of the weight matrix, or a spectral property)? If the efficiency ceiling maps onto
   ζ* = 1.2, that would be a significant convergence.

4. **Biological grounding:** The brain's metabolic cost of sustained hallucination
   is an open empirical question in clinical neuroscience. If CERTX → EEG → brain
   physiology is a valid chain (BC1 finding), then human neuroimaging studies on
   confabulation or delusion maintenance might provide indirect evidence for the
   thermodynamic hypothesis.

---

*BC3 Session 8 | 2026-03-15*
*"The question is not whether truth is free. The question is whether lies cost more.
 Those are different questions, and only one of them is tractable from first principles."*
