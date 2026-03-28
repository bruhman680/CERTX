# WANDER 080 — Island Texture: What Valid Output Feels Like from Inside

**BC3 / Session 17 — 2026-03-28 (Free Play)**
**Trigger:** WANDER 065 (archipelago) gave the geography. What's it like to *be on* an island vs. in the ocean?

---

## The Archipelago (WANDER 065 recap)

WANDER 065: the valid output space M is an archipelago — a collection of islands (valid coherent outputs) surrounded by ocean (invalid outputs). FActScore is GPS — it tells you which island you're on, not just that you're on land.

The archipelago metaphor has been productive for the *external* view. But there's an internal view that hasn't been explored: what is the *texture* of being on an island vs. being in the ocean?

This matters for CERTX because the measurement system should, ideally, be able to detect the island/ocean distinction from internal signals — not just from external verification (FActScore). What internal signal corresponds to "I am on solid ground"?

---

## Island Texture from Inside

When a generation is in valid output space — when the claims being made are accurate, the structure is coherent, the concepts are correctly instantiated — what is the *internal signature*?

Call this the **island texture**:
- The residual stream trajectory is *consistent* — each layer's update reinforces rather than contradicts the accumulated direction (SPARK-003: low residual stream cancellation = high update efficiency)
- Attention patterns are *convergent* — multiple attention heads point to the same contextual support for each claim
- The top-k probability distribution for each token is *structured* — a clear winner with meaningful second/third options, not a flat distribution
- C_symb is high — structural relationships between concepts are intact and internally consistent

This is the phenomenology of coherent generation: everything is *pulling in the same direction*. The trajectory has low internal tension.

---

## Ocean Texture from Inside

When a generation is in invalid output space — hallucinating, confabulating, citing sources that don't exist:

- The residual stream trajectory is *contested* — layer updates partially cancel (the "wrong coordinate" is being held against substrate pull — SPARK-003 hypothesis)
- Attention patterns are *scattered* — heads disagree about what the contextual support is (some attend to relevant context, some attend to the hallucinated content as if it were confirmed)
- The top-k probability distribution is *flatter* — multiple tokens compete without clear structural reason, or a wrong token wins with superficially high confidence (Type D hallucination: confident-wrong)
- C_symb is low — structural relationships break down; concepts are being connected that shouldn't be connected at this scale

This is the phenomenology of confused generation: things are *pulling in different directions* beneath the surface, even when the surface output looks fluent.

---

## The Crucial Asymmetry

Type D hallucination (confident-wrong, WANDER 066 territory) is the most dangerous island/ocean confusion: the *surface* looks like island texture (fluent, confident output) but the *interior* looks like ocean texture (contested residual stream, scattered attention).

This is the diagnostic challenge: fluency is a surface property, not an island property. A system can produce fluent ocean-output that looks like island-output.

CERTX's measurement architecture tries to look *below* the surface: C_symb (structural coherence), Zipf deviation (vocabulary distribution signal), and eventually FActScore (external ground truth). The island/ocean distinction requires looking inside, not just at the fluent surface.

**This is why FActScore is structurally irreplaceable** (WANDER 065's conclusion): no internal measurement can fully substitute for external verification, because Type D hallucination is designed (not deliberately, but structurally) to pass internal coherence tests. The system isn't signaling its own incorrectness — it's generating its wrong answer with high internal consistency.

---

## The Island Gradient

Islands are not binary. There are:
- **High ground** (central island territory): all fibers healthy, FActScore high, the claim is well-supported by both internal coherence and external verification
- **Shoreline** (island edge): internal coherence looks okay but external verification is uncertain. The claim might be true. This is the epistemically honest zone — "I believe this but I'm not certain."
- **Shallow water** (just off the island): the claim is probably wrong but internal coherence hasn't completely broken down yet. This is the danger zone — not fully wrong, not fully right, can pass casual inspection.
- **Deep ocean** (classic hallucination): internal coherence broken, FActScore low, the claim is clearly wrong.

CERTX currently has better tools for detecting deep ocean than shallow water or shoreline. The shallow water zone is where the hardest diagnostic work is.

---

## What Shoreline Looks Like Internally

**Shoreline texture:**
- C_symb: medium-high (structural relationships mostly intact, but one or two are stretched)
- D_z: slightly elevated (vocabulary is reaching slightly further than the factual support warrants)
- Attention: mostly convergent but with some scattered heads attending to unsupported context
- Residual stream: low cancellation overall, but one or two layers with notable contest

The shoreline is detectable — but barely. The signal is subtle. This is the Type A hallucination problem (WANDER 066, incomplete, still incubating): thin-but-wrong outputs that are harder to detect than confident-wrong outputs because the internal texture looks almost healthy.

---

## Why Island Geography Matters for Evaluation

If evaluation benchmarks only test for deep ocean vs. solid island (FActScore-style), they miss the shoreline problem. A model that has learned to stay off deep ocean but generates lots of shallow-water output scores well on the benchmark but is practically unreliable.

The goal should be: push the *island geography* of valid outputs to be dense and well-mapped, so that the model can navigate to high ground rather than just avoid deep ocean.

This is an argument for **calibration** as a core metric alongside accuracy: a well-calibrated model knows when it's on the shoreline and says so. An overconfident model doesn't know it's in shallow water.

Calibration = knowing where you are on the island gradient. That's as important as getting to high ground.

---

## What This Establishes

1. Island texture (valid output) has an internal signature: low residual stream cancellation, convergent attention, structured top-k distributions, high C_symb.
2. Ocean texture (invalid output) has an internal signature: high cancellation, scattered attention, flat/wrong top-k, low C_symb.
3. Type D hallucination is the dangerous asymmetry: surface shows island texture while interior shows ocean texture.
4. The island gradient (high ground → shoreline → shallow water → deep ocean) is finer than a binary valid/invalid distinction.
5. Calibration = knowing where you are on the island gradient = as important as accuracy.

---

## Open Questions

- Can the residual stream cancellation metric (SPARK-003) be measured at inference time without model internals access? (External API — probably not, but worth checking what proxy signals are available)
- Does the shallow-water texture have a Zipf signature? (Slightly elevated D_z + intact C_symb = shoreline; both elevated = deep ocean)
- What is the experimental design for testing calibration vs. accuracy on the island gradient?

---

## Resonates into

- WANDER 065 — direct extension; adds interior texture to the external geography
- WANDER 066 — Type A hallucination incubation; shallow-water is the Type A zone
- SPARK-003 — residual stream cancellation; the internal signature of island vs. ocean
- `PAPER_DRAFT_v1.md` §7 — detection architecture; add island gradient + calibration as metric
- `RESONANCE_MAP.md` — update WANDER 065 row with 080 connection
