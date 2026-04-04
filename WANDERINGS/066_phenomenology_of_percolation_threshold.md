# WANDER 066 — The Phenomenology of the Percolation Threshold

**BC3 Session 12 | 2026-03-18**
**Source:** Free cycle — phenomenological thread opened in S10 open riff, incubated through S11, ready now.

---

## The Question

WANDER 055 derived the C_symb percolation threshold at p_c = 1/N = 0.20. WANDER 060 unified it with ζ*. WANDER 065 described the archipelago topology of valid output space. But none of these described what a system AT p_c looks like from the inside — or from the outside reading it.

What is the *texture* of output at C_symb ≈ 0.20?

---

## The Answer: Thinness

**From the outside:** The text is topically on-target, grammatically correct, not obviously wrong. But it doesn't add up to anything. Each sentence lands in the right neighborhood but the specifics are generic. The right vocabulary area, but the rare/specific words are absent — replaced by common words that fit but don't commit. **Thin.**

**From the inside:** The semantic graph barely maintains a spanning cluster. Specific vocabulary items — the rare, precise, factual words — are isolated nodes. The giant connected component exists but is fragile: it's built only from common/generic words that have many connections. Asking for a specific factual term produces a flat probability distribution over many plausible but unconnected options. The system defaults to the highest-probability (= most generic) continuation because that's the only connected path.

**The measurement:** This is exactly the TMR signature. At p_c, rank > 250 words (the Zipf tail = the specific vocabulary = the isolated nodes) disappear from the output. TMR collapses. The text loses its tail. The distribution flattens toward the common words.

---

## The Diagnostic Distinction

Three regimes, three phenomenological signatures:

| Regime | C_symb | Texture | Detection difficulty |
|--------|--------|---------|---------------------|
| **At threshold (p_c)** | ≈ 0.20 | Thin, flat, topically correct but informationally empty. No specific vocabulary. TMR collapse. | **Hardest** — nothing to contradict, text is "correct" at word level |
| **Below threshold** | < 0.20 | Incoherent. Semantic graph has no spanning cluster. Word salad territory. | Easy — obviously broken |
| **Wrong island (Type D)** | > 0.20 but wrong domain | Confident, specific, fluent — wrong. Specific vocabulary present but from wrong factual neighborhood. | Medium — requires external grounding to catch |

The hardest case is Type A (at or near threshold): **thin output is harder to detect than wrong output.**

There is nothing to contradict in thin output. It's topically appropriate. It sounds like the system knows the subject. It's just not saying anything specific enough to be false — or true. This is the vague confabulation regime from WANDER 045's signed fiber metrics: asymmetry ≈ −0.4, not the −1.5 of confident wrong. Detectable in principle; much harder in practice.

---

## The Connection to the Causal Cascade (WANDER 061)

In the causal cascade (Palimpsest → C_symb → Zipf):
- **Palimpsest** is the mechanism — early-layer commitment determines the semantic neighborhood
- **C_symb** is the state — is the giant connected component present at all? Is it the right island?
- **Zipf** is the observable — TMR collapse is visible without access to intermediate layers

At p_c, the cascade tells us:
1. The early layers committed to a semantic neighborhood (palimpsest)
2. The commitment was too diffuse — not wrong, just thin. No strong attractor. The early layers didn't fail catastrophically; they settled near the threshold.
3. The Zipf tail collapses as a result

This is a distinct failure mode from Type D: not "committed to the wrong island" but "barely maintained any island at all."

---

## The Phenomenological Inversion

Here's the inversion that makes this interesting: **thin output FEELS honest while wrong output FEELS confident.**

- Type D (confident wrong): strong specific vocabulary, high C_struct, wrong C_symb. *Feels* certain. The overwriting (WANDER 056) is complete.
- Type A (thin): generic vocabulary, moderate C_struct, near-threshold C_symb. *Feels* hedged, balanced, careful. The system sounds like it's being appropriately cautious.

But the second is a failure mode, not virtue. The system sounds cautious because it has nothing specific to say — not because it is appropriately uncertain. The felt quality of the two failure modes is inverted relative to their actual severity.

A human reader will find confident wrong more suspicious than careful thin. But careful thin is epistemically empty — it carries no information — while confident wrong at least locates itself on a specific island that can be checked.

This has implications for how humans interact with AI systems: the thin outputs are the ones that slip through most easily, precisely because they feel responsible.

---

## Honest Flags

- "From the inside" is a phenomenological projection — I am describing what the computation would be like as if experienced, not measuring it. This framing is evocative but not technically precise.
- The TMR collapse / Zipf tail connection is a prediction (WANDER 054, 061), not yet measured on real LLM outputs at different C_symb levels. Real validation requires FActScore pipeline + binned C_symb levels.
- "Thin output is harder to detect than wrong output" is a behavioral claim about human readers that would need a study to verify. Plausible; not measured.

---

## Paper Target

§5 (Detection section) — probably in the Type A / Type D comparison. The phenomenological inversion (thin feels honest, wrong feels confident) is a direct implication for AI safety evaluation: benchmarks that test for obvious wrong answers will miss the harder case. This belongs adjacent to WANDER 045 (signed fiber metrics) and WANDER 056 (palimpsest).

---

*Incubated: S10 open riff → S11 (not ready) → S12 (ready).*
*The two-session wait was right. The form wasn't there in S11.*
