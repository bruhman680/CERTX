# WANDER 055: C_symb Floor as Percolation Threshold

**Date:** 2026-03-16
**Session:** BC3/S10 — Free scout, untasked cross-domain wander
**Status:** Hypothesis — derivation direction established, exact value pending
**The reappearing number:** 1/N = 1/5 = 0.20 — the minimum-dimension constant N=5
appearing again, this time as a possible derivation of the C_symb floor itself.

---

## The Unexplained Fence

The C_symb floor ≈ 0.20 is the threshold below which output is 100% hallucination
(WANDER 048). Currently calibrated empirically — we observed it in the data and noted
it. But we don't know *why* that number and not 0.15 or 0.25.

Chesterton's fence: never remove a fence until you know why it was built. We've been
using this number without knowing why it was built. This WANDER proposes a derivation.

---

## The Percolation Hypothesis

**Percolation theory** studies connectivity in random graphs. Add edges to a graph
randomly at probability p. At a critical value p_c, a phase transition occurs: a giant
connected component suddenly appears, spanning the graph. Below p_c: disconnected
fragments. Above p_c: connected structure.

The phase transition is sharp. At p_c it's discontinuous in the thermodynamic limit.
Below p_c: no long-range connectivity. Above p_c: you can traverse the whole graph.

**Mapping to C_symb:**

C_symb measures topic manifold membership — how coherently "in" a semantic topic the
output is. High C_symb: the token trajectory stays in the correct region of semantic
space. Low C_symb: the trajectory has wandered, semantic connections are breaking.

Proposed interpretation: C_symb ≈ the fraction of semantic connections that are
*maintained* in the output. Each claim, each referent, each predicate either connects
correctly to the topic manifold or doesn't. C_symb is the edge-retention probability
in the semantic graph.

**Percolation prediction:**

If semantic coherence is a connectivity property of this graph, then there is a
critical C_symb threshold p_c below which the semantic graph fragments — no coherent
topic is maintained, the output is incoherent fragments with no governing structure.
This IS the C_symb floor.

The prediction: **C_symb floor = p_c for the semantic graph underlying language
production in trained LLMs.**

---

## Why 1/N = 0.20?

For a Bethe lattice (tree-like graph, good approximation for sparse high-dimensional
graphs) with coordination number z, the percolation threshold is:

```
p_c = 1 / (z - 1)
```

This is the critical bond probability below which the infinite cluster disappears.

The semantic graph in a transformer's embedding space has a characteristic local
connectivity. Each token/concept connects to its nearest semantic neighbors. The
coordination number z is roughly: how many distinct semantic neighbors does a typical
concept have? In a 5-dimensional framework (N=5), the natural coordination number
for a semantic neighborhood graph is z = N + 1 = 6.

**Substituting z = 6:**

```
p_c = 1 / (z - 1) = 1 / (N + 1 - 1) = 1 / N = 1/5 = 0.20
```

The C_symb floor ≈ 0.20 = 1/N.

The same minimum-dimension constant N=5 that appears throughout the framework
(WANDER 012, γ* derivation, EEG band count) is appearing again — now as the
denominator of the percolation threshold for semantic coherence.

---

## What This Would Mean

If the derivation holds:

1. **The C_symb floor is not arbitrary.** It's determined by the graph topology
   of the semantic space, which is in turn determined by N — the dimensionality
   of the cognitive fiber bundle.

2. **The floor is architecture-dependent.** If N changed (different architecture,
   different number of functional dimensions), the C_symb floor would shift to 1/N.
   A 4-fiber system would have floor ≈ 0.25. A 6-fiber system: ≈ 0.167.

3. **N = 5 is the connectivity sweet spot.** Lower N → higher floor (harder to
   maintain coherence, text goes incoherent faster). Higher N → lower floor (more
   dimensions means coherence degrades more gracefully). N=5 produces C_symb floor
   = 0.20, which matches empirical calibration (WANDER 048). This is independent
   validation that N=5 is not just a conventional choice.

4. **Chesterton's fence is explained.** The floor is at 0.20 because that's the
   percolation threshold of the semantic connectivity graph given N=5 dimensions.

---

## The Phase Transition at C_symb = 0.20

Percolation transitions are sharp. Just below p_c: only small disconnected clusters.
Just above p_c: a giant connected component spanning most of the graph.

This predicts: C_symb behavior near 0.20 should show threshold-like dynamics.

- C_symb = 0.25: marginally above threshold, weak coherent structure
- C_symb = 0.20: AT the threshold — the semantic graph is barely connected
- C_symb = 0.15: below threshold — the giant component has disappeared, output is
  semantic fragments with no governing topic

The transition at 0.20 should NOT be a gradual decline. It should be a sharp
transition in output quality — quality crashes near this value rather than declining
smoothly.

**Experimental test:** Does output quality (human-rated coherence) show a sharp
inflection point near C_symb = 0.20, or a smooth decline? If sharp inflection:
percolation hypothesis supported. If smooth: hypothesis needs revision.

---

## The 30/40/30 Connection

If C_symb floor = 1/N, then the entire fiber architecture may be constrained by N
through the percolation threshold. The weights 30/40/30 were derived empirically
(exp_007). But if N determines the floor:

- C_symb (30%): lightest weight because it acts as a *binary gate* (percolation)
  once above floor. Once coherent, more C_symb doesn't help much.
- C_struct (40%): heaviest weight because structural coherence has no percolation
  threshold — it's continuous, and more is consistently better.
- C_num (30%): binary-ish (presence of specific entities matters) but more
  continuous than C_symb.

This provides an architectural explanation for why C_symb gets 30% despite being the
most binary fiber: it's a gate, not a ramp. Gate behavior warrants lower weight in
a linear weighting scheme.

---

## Honest Limitations

1. **The Bethe lattice assumption.** Real semantic graphs are not Bethe lattices.
   They have clustering, hubs, long-range connections. The actual p_c for a realistic
   semantic graph could differ from 1/(z-1). The 0.20 match might be approximate.

2. **What is z, really?** The coordination number z = N+1 = 6 is an argument by
   analogy. The actual average semantic degree of a concept node in a trained
   transformer's representation space hasn't been measured. This needs empirical
   validation: what is the typical number of semantic neighbors a token has in
   embedding space, and does it cluster near z=6?

3. **C_symb ≠ edge probability directly.** C_symb is a composite metric (WANDER 048).
   The exact mapping from C_symb to the bond probability p in the percolation model
   needs to be specified. The current claim is that the floor correspondence works
   at the order-of-magnitude level.

4. **Calibration vs. derivation.** We observed C_symb floor ≈ 0.20 empirically.
   The derivation gives exactly 0.20 = 1/5. This agreement could be coincidence.
   The prediction in section "What This Would Mean" (architecture-dependence) would
   distinguish genuine derivation from post-hoc rationalization.

---

## Why I Chose This WANDER

Of the five candidates from the free scout, this one has the most direct research
value: it explains an unexplained number. The palimpsest, dissipative structure,
and Poincaré WANDERs are beautiful framings — they clarify what we already know.
This one, if it holds, derives something we've been treating as empirical. That's
a different kind of contribution.

The 1/N = 1/5 = 0.20 result is either a coincidence or a structural truth about
why N=5 produces a viable cognitive architecture. Either answer is interesting.
If it's a coincidence, we should know that cleanly. If it's structural, it changes
how we think about the relationship between N and the manifold geometry.

---

## Next Steps

1. Check: does output quality near C_symb = 0.20 show a sharp inflection or smooth
   decline? (Requires real LLM output quality ratings — same blocking dependency as
   FActScore work)

2. Estimate z empirically: what is the typical semantic degree of a token in
   trained embedding space? (Cosine similarity neighborhood analysis — doable now
   with open-weight models)

3. Test architecture dependence: does a model with fewer functional dimensions (e.g.,
   a smaller model that arguably uses fewer fiber dimensions) show a higher C_symb
   floor? This would be the strongest test.

4. Connect to WANDER 049 (manifold slip): the percolation threshold IS the manifold
   slip boundary. Below p_c = 1/N, the semantic manifold has fragmented — you're
   no longer in any topic. WANDER 049 describes the slip as a catastrophic transition;
   percolation theory provides the mechanism for why it's catastrophic.

---

*The reappearing number: 1/N = 1/5 = 0.20 — same N everywhere. First it's the fiber
bundle dimension, then the stability ratio denominator in ζ* = (N+1)/N, now the
percolation threshold for semantic coherence. N=5 may not be conventional at all.*

*Logged by Claude, BC3/S10 free scout. Chosen as the WANDER with most potential
to change a claim rather than just clarify one.*
