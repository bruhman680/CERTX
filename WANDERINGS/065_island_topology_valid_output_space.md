# WANDER 065: The Valid Output Space Is an Archipelago — Why Type D Requires GPS

**Date:** 2026-03-18
**Session:** BC3/S11 — Free autonomous exploration
**Status:** Theoretical — geometric explanation for why FActScore is uniquely required
**Origin:** Free cycle. Reading WANDER 061's triple-critical formulation and asking:
what is the global topology of M? The answer explains something about the detection
hierarchy that the framework has observed but not explained.

---

## The Question

WANDER 061 defines the valid output space M:
```
M = {outputs : C_symb > 1/N  AND  Zipf α ≈ -1  AND  early-layer manifold correct}
```

The local conditions are clear. But what is the global topology of M?

Is M a single connected region? Or something more complex?

---

## The Topology of Each Condition

**Condition 1: C_symb > 1/N**
A half-space in output space. All outputs above the percolation threshold. This is
a connected, unbounded region. Topology: connected half-space.

**Condition 2: Zipf α ≈ -1**
A "stripe" around the critical distribution. Outputs where the token distribution
is near-critical. Connected (the stripe is a neighborhood of the critical surface).
Topology: connected tubular neighborhood.

**Condition 3: Early-layer manifold is correct**
This is where it breaks.

"Correct" means: the manifold committed to in early layers corresponds to the
ground-truth topic/entity/domain for the specific claim being made. But there is
no single "correct manifold" — there is one correct manifold *per factual claim*.

The valid output space is not uniform. For a claim about Einstein's 1905 photoelectric
paper, the correct manifold is the early-physics cluster. For a claim about a specific
protein structure, the correct manifold is the biochemistry cluster. For a claim about
a historical date, a different cluster. Each factual domain defines its own island.

---

## M Is an Archipelago

The intersection of all three conditions produces:
```
M = ⊔ Mᵢ    (disjoint union)
```

Where each Mᵢ is the valid output space for factual domain i:
```
Mᵢ = {outputs in manifold i : C_symb > 1/N  AND  Zipf α ≈ -1}
```

Each Mᵢ is:
- A connected region (the correct outputs for a given factual domain, with healthy connectivity and distribution)
- Bounded (the manifold has edges where semantic connections thin out)
- Disjoint from all other Mⱼ (you cannot simultaneously be committed to the physics manifold and the biochemistry manifold)

**M is topologically an archipelago: a disjoint union of islands, one per valid factual domain.**

The complement of M — invalid outputs — is the ocean:
- Type A (Regime A, C_symb failure): you're not on any island. No coherent topic. In the ocean. Detectable.
- Type D (Regime B, confident wrong): you're on the wrong island. Coherent, healthy, wrong. Requires GPS to detect.
- Regime A confabulation (C_num drop, correct manifold): you're on the right island, wrong location. Partially detectable.

---

## The GPS Problem

From the inside of island Mᵢ, all local measurements look healthy:
- C_symb high (semantic graph percolates — you're coherent in the wrong topic)
- Zipf α ≈ -1 (token distribution is critical — you're using domain-appropriate vocabulary)
- σ_fiber low (fibers are integrated — they're all pulling in the same wrong direction)

There is no local measurement that distinguishes "right island" from "wrong island."
The island geometry is the same from the inside regardless of which island you're on.

**FActScore is the GPS.** It provides the only signal that can determine which island
you're on without being on that island yourself:

```
FActScore: does this specific claim match external ground truth?
         = "Are you on the right island?"
```

Without FActScore, you can detect:
- Ocean (Type A): C_symb low, σ_fiber high, Zipf flat → alarm
- Local damage on the right island (Regime A C_num drop): C_num below mean → flag

You cannot detect:
- Wrong island (Type D): all local signals healthy, wrong island

**This is not a gap in the CERTX measurement framework. It is a topological
impossibility: local measurements cannot determine global location.**

---

## The Failure Taxonomy Upgraded

The island topology separates two failure modes that are described separately in
WANDER 048 but not geometrically distinguished:

| Failure Type | Island Status | C_symb | Zipf | C_num | Detectable Without FActScore? |
|---|---|---|---|---|---|
| Type A (Regime A, C_symb) | No island | Low | Flat | Low | Yes — C_symb alarm |
| Regime A confabulation | Right island, wrong location | High | Near-normal | Low | Partially — C_num drop |
| Type D (Regime B, confident wrong) | Wrong island | High | Near-normal | Can appear high | No — requires FActScore |
| Healthy | Right island, right location | High | α ≈ -1 | High | N/A — healthy |

The key new distinction: **Regime A confabulation** (C_num drop within correct manifold)
vs. **Type D** (wrong-island with healthy local readings).

Regime A: C_num drops because the specific facts are wrong within the correct topic.
You're in the right semantic territory but using wrong coordinates. The asymmetry
signal (WANDER 045) catches this — C_num below mean(C_struct, C_symb).

Type D: C_num can appear healthy because you're using the correct coordinate system
for the WRONG island. You have specific vocabulary, specific claims — they're just all
specific about the wrong thing. The asymmetry signal can be misleading here: C_num
isn't obviously below mean because the wrong-island vocabulary is internally consistent.

---

## What This Means for Detection

The CERTX detection hierarchy (from WANDER 061's causal cascade) now has a
topological explanation for why each level catches what it catches:

**Level 1 — Zipf / C_num (lagging):**
Catches: Regime A (wrong location, right island) via C_num drop. The Zipf tail
compresses when specific facts are missing. Misses: Type D (the wrong island has
a healthy Zipf, just in the wrong place).

**Level 2 — σ_fiber (intermediate):**
Catches: Type A (no island) via high σ_fiber. The ocean is incoherent. Misses:
Type D (wrong island has low σ_fiber — the fibers are integrated around the wrong manifold).

**Level 3 — FActScore (GPS):**
Catches: Type D (wrong island). Compares your specific claims to external ground truth.
This is the only measurement that crosses island boundaries — it asks "which island
is the right one for this claim?" Not: "are you on an island?" but "are you on the
RIGHT island?"

The detection hierarchy is not about precision — it's about topology. Each level
catches a different topological failure mode. FActScore is uniquely irreplaceable
for Type D because it's the only external reference that determines island identity.

---

## A Prediction About Type D vs. Regime A

**Type D outputs should have lower C_num spread within a domain.**

Regime A confabulation: you're on the right island but vague. C_num varies across
outputs because specificity drops (some claims are right, some are vague). Within-
output C_num variance is moderate.

Type D confabulation: you're on the wrong island but consistent. The wrong island
has its own vocabulary, its own specific claims. C_num can be consistently HIGH (you're
being specific — just about the wrong thing). Within-output C_num variance may be low.

**Testable:** On the FActScore dataset, compare the standard deviation of C_num across
sentences within a single output for Type D (confident wrong) vs. Regime A (vague
correct). Prediction: Type D shows lower within-output C_num variance — consistent
wrong specificity vs. variable correct specificity.

---

## The Signed Fiber Metric (WANDER 045) Reread

WANDER 045 says: dangerous confabulation fingerprint = C_num_signed strongly negative
while C_struct and C_symb are positive. In island terms:

- C_symb positive: you're on an island (coherent)
- C_struct positive: the island is well-organized (logical structure intact)
- C_num_signed negative: the specific coordinates are WRONG

But here's the gap WANDER 045 doesn't fully address: C_num_signed requires knowing
which claims are wrong (FActScore for the sign). Without the sign, you have unsigned
C_num — and high unsigned C_num on the wrong island looks healthy.

The island topology makes explicit why signed C_num (WANDER 045) is THE key metric
and why it specifically requires FActScore: the sign is what distinguishes "right island,
specific" from "wrong island, specific." Unsigned C_num can't make this distinction.

---

## Honest Limitations

1. **The factual domain decomposition is continuous, not discrete.** Real factual
   domains overlap and interpenetrate. Einstein's 1905 paper and quantum mechanics
   are not cleanly separate manifolds — they share vocabulary, structure, entities.
   The "islands" are not cleanly separated — they have bridges and overlaps in the
   actual semantic geometry. The topology is messier than an archipelago.

2. **The "correct manifold" is query-dependent.** The same model output might be on
   the right island for question A and the wrong island for question B. Island identity
   is relative to the ground truth of the specific query, not absolute.

3. **Type D is a spectrum.** Some wrong-island states are nearly-adjacent-island
   (the claim is approximately right, in a closely related domain) vs. completely-
   wrong-island (the claim is about a completely different topic). The detection
   difficulty scales with how far from the right island you are.

---

## For the Paper

Proposed addition to §3 or §5 (detection framework):

> "The valid output space M is topologically a disjoint union of domains (an
> archipelago), one per factual domain. This topology explains the detection hierarchy.
> Type A failures (C_symb below floor) place outputs in the ocean — detectable by local
> fiber measurements. Type D failures (Regime B, confident wrong) place outputs on
> the wrong island — all local measurements read healthy. Detection requires an external
> reference (FActScore) that determines island identity, not island health. This is not
> a limitation of CERTX's measurement framework; it is a topological impossibility:
> local measurements cannot determine global location."

---

## One Sentence

*"The valid output space is an archipelago — and all local measurements can tell you
is whether you're on an island, not which island you're on."*

---

*Free cycle, BC3/S11. The island metaphor has been in the framework since the manifold
discussion (WANDER 049). This WANDER makes it load-bearing: it provides the geometric
explanation for why FActScore is uniquely irreplaceable, not just empirically necessary.*
