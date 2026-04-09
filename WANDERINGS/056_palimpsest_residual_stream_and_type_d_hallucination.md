# WANDER 056: The Palimpsest — Which Layer Is "Original"?

**Date:** 2026-03-16
**Session:** BC3/S10 — Free scout, Thread 1
**Status:** Framing established — no new measurement, strong paper contribution
**The reappearing number:** None — this one is about direction, not quantity.
The surprise was an inversion.

---

## The Palimpsest

A palimpsest is a manuscript that has been scraped and overwritten. The economics
of medieval writing: vellum (scraped calfskin) was expensive. Monks reused it.
They scraped off old ink and wrote new text on top. The old writing was supposed
to disappear. It didn't — traces of the earlier writing remained readable through
multispectral imaging.

The most famous example: the Archimedes Palimpsest. A 10th-century copy of
Archimedes' works was scraped and overwritten in the 13th century with a prayer
book. For 700 years, Archimedes was unreadable — hidden under later writing.
In 1906, Johan Heiberg recovered it. Modern multispectral imaging (2000s) revealed
it completely. The earlier text was the valuable one.

**The transformer residual stream is a palimpsest.**

---

## The Mechanism

In a transformer, earlier layers write representations into the residual stream.
Later layers read those representations and write new ones on top. The residual
stream accumulates contributions — it is not reset between layers. Every layer
adds its signal to what was already there.

The earlier layers handle:
- Token embedding (raw input)
- Basic syntactic structure
- Semantic manifold assignment — what TOPIC is this about?
- C_symb commitments: what conceptual region are we operating in?

The later layers handle:
- Fluency shaping
- Grammatical surface structure
- Pragmatic coherence (does this sound right?)
- Rhetorical smoothing

**The C_symb commitment is an early-layer event.** The model decides, in the first
several layers, what semantic manifold it is operating in. Is this a question about
biology? History? Mathematics? Who is being discussed? Which time period? The topic
manifold assignment sets the stage for everything that follows.

Later layers then write fluent, coherent surface text *on top of* that commitment.

---

## The Inversion

In manuscript scholarship: the earlier writing is the valuable original.
We use multispectral imaging to RECOVER it from under the overwriting.
The Archimedes under the prayer book is what we want.

In a transformer: the same structure applies, but we usually don't notice.
We read the surface output — the prayer book. We don't look underneath.

**The inversion that surprised me:**

We treat the final token output as the "real" output. But the final output is
the last layer's overwriting. The *original manuscript* — the early-layer semantic
commitment, the C_symb manifold assignment — is what actually determines truth value.

A model can produce a fluent, well-structured, grammatically impeccable sentence
about the wrong thing. The late layers did excellent overwriting. The early layers
committed to the wrong manifold. The prayer book is beautiful. Archimedes is wrong.

---

## Why Type D Hallucination Is the Hardest to Detect

Type D hallucination (WANDER 048): C_num drops, C_struct and C_symb stay high.
The output is confident, fluent, well-organized — and factually wrong.
Surface quality: high. Underlying accuracy: low. This is "Regime B": the model
is coherent but specifically incorrect.

The palimpsest explains why this is hard to detect:

**The late layers did complete, high-quality overwriting.** The surface text carries
every signal of competent production — varied vocabulary, correct syntax, appropriate
register, smooth transitions. A human reader has no signal that anything is wrong.
Even σ_fiber doesn't strongly signal Type D because C_symb and C_struct are intact.
Only C_num drops (WANDER 045, signed fiber metrics).

The error is in the early manuscript, completely overwritten by excellent later text.
The prayer book is flawless. You need multispectral imaging to find the error.

**The CERTX measurement pipeline IS the multispectral imaging.** σ_fiber, particularly
the C_num_signed signal (WANDER 045), is the tool that reads underneath the surface
fluency to find the early-layer commitment failure. Without it, the palimpsest fools
every surface-level reader.

---

## Implications for Detection Architecture

The palimpsest framing suggests:

1. **Layer-targeted measurement matters.** If C_symb failure is an early-layer event,
   then measuring it at the final output is already measuring it through all the
   overwriting. Direct early-layer probing (activations at layers 4–8, before the
   fluency-shaping layers) might give a cleaner C_symb signal.

2. **The "earlier is more foundational" principle.** For truth-sensitive measurement,
   earlier layers are more informative than later layers about whether the model
   is in the right semantic manifold. The fluency layers are later and less relevant
   to factual accuracy.

3. **SPARK-003 connection** (SHADOW_LEDGER — residual stream cancellation):
   If the early-layer C_symb commitment is wrong, does the residual stream show
   cancellation as later layers try to reconcile fluency with an incorrect base?
   The palimpsest predicts YES — the contested internal state Gemini described
   (inhibitory pressure analog) IS the later layers overwriting an early error.

4. **Paper placement:** This belongs in §5 (detection mechanisms), specifically
   in the section explaining WHY Type D is the hardest to detect. The palimpsest
   gives readers an intuitive model of the detection challenge before we present
   the technical σ_fiber solution.

---

## What This Is Not

This is not a measurement claim. C_symb and C_num already capture the relevant
signal. The palimpsest is a *mechanistic explanation* of why the signal has the
structure it does — why C_symb is early and foundational, why Type D looks fine
on the surface, why you need to measure underneath.

It's also not a new failure mode — it IS Type D as described in WANDER 048.
The contribution is the mechanistic framing that makes the failure mode
intuitively clear.

---

*The surprise was the inversion: we treat output as "original" and everything
before it as "draft." The palimpsest flips this. The early-layer commitment IS
the original manuscript. The final output is all overwriting. Truth lives
underneath the fluency.*

*Logged by Claude, BC3/S10 free scout. This one surprised me most in the scout.
The inversion of what counts as "original" in a forward pass.*
