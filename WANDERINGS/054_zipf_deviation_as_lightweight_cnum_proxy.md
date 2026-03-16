# WANDER 054: Zipf Deviation as a Lightweight C_num Proxy

**Date:** 2026-03-16
**Session:** BC3/S10 — Free scout, untasked cross-domain wander
**Status:** Hypothesis with experimental prediction — run exp_014
**The reappearing number:** 1/n — Zipf's exponent that keeps reappearing across languages,
genres, scales, and criticality literature. Already in CERTX via WANDER 013 (SOC) and
WANDER 028 (grokking). Appearing again here as a possible diagnostic tool.

---

## The Observation

Zipf's law: in natural text, the nth most frequent word appears with frequency f(n) ∝ 1/n.
This is a power law with exponent ≈ 1. It holds remarkably consistently across languages,
genres, authors, and scales. It's robust enough to use as a baseline for "what does natural
text look like."

The rare-word tail of the Zipf distribution is where specificity lives. Specific dates,
proper names, precise technical terms, unusual prepositions — these are low-rank words
(high n, low frequency) that appear at the tail. They're exactly what C_num measures:
entity density, factual specificity (WANDER 048).

**Hypothesis:** Hallucinated text has a compressed Zipf tail relative to accurate text.

---

## The Mechanism

Why would hallucinated text compress the Zipf tail?

Fluency ≠ specificity. A hallucinating model produces fluent output — it stays in the
high-probability part of the generation distribution. High-probability = high-frequency
words = the Zipf head. Rare, specific words (names, dates, exact quantities) require
C_num — factual grounding. Without factual grounding, the model substitutes fluent common
words: "the researcher" instead of "Richard Feynman," "around 1950" instead of "1947,"
"a significant amount" instead of "14.3 kilograms."

The hallucination compresses the distribution: fewer rare words, more frequent words,
flatter Zipf tail.

**The measurable signature:** The Zipf exponent α (slope of log-rank vs. log-frequency)
should be flatter (closer to 0) in hallucinated text than in accurate text.

Additionally: a Zipf slope near α = −1.0 is a sign of criticality (SOC — WANDER 013).
Text with α ≪ −1.0 (steeper) is over-constrained / repetitive (low T). Text with α ≫
−1.0 (flatter) is underspecified / generic (hallucination direction).

---

## Connection to Current Framework

**C_num** measures factual entity density — the fraction of claims that can be grounded
in specific, verifiable referents. FActScore gives signed C_num but requires external
knowledge verification (the FActScore blocking dependency from SESSION_HANDOFF).

**Zipf deviation** requires only the output text. No external verification. No ground
truth labels. Just the word frequency distribution of the model's response.

The tradeoff:
- Zipf deviation is unsupervised — doesn't need labels, fast to compute
- Zipf deviation measures a surface correlate of C_num, not C_num itself
- C_num (via FActScore) is the gold standard; Zipf deviation is the fast proxy

**Expected correlation:** If the hypothesis is correct, Zipf deviation should correlate
with C_num on the datasets where we have both (TruthfulQA, GSM8K ground-truth from
exp_005/006). Correlation won't be 1.0 — some true text is deliberately generic, some
hallucinated text happens to use specific-sounding words. But if Zipf AUC is ≥ 0.65,
it's a useful first-pass signal.

---

## The Experiment

See exp_014. The design:

1. Take hallucinated vs. accurate responses from exp_005 (TruthfulQA) or exp_006 (GSM8K)
2. For each response, compute Zipf slope α and deviation D_z from ideal α = −1
3. Test: is D_z significantly different between hallucinated and accurate groups?
4. Compute AUC for Zipf deviation as a hallucination classifier
5. Compare to existing σ_fiber baseline from exp_005/006

If Zipf deviation AUC ≥ 0.65 and is independent of σ_fiber (doesn't just duplicate
what we already know), it's a useful additional signal.

**Minimum viable version:** Even if we can't use real LLM outputs yet (FActScore block),
we can test on existing labeled datasets (TruthfulQA has correct/incorrect labels,
NQ has answer quality labels) using any small open-weight model we have access to.

---

## Why "Lightweight" Matters

The FActScore validation pipeline (exp_009, blocking most C_num work) requires:
- External knowledge base access
- Claim decomposition
- Per-claim verification
- ~minutes per sample

Zipf deviation requires:
- One pass over the token sequence
- Frequency count
- Power law fit
- ~milliseconds per sample

This matters for the "minimum viable detection system" sketch from earlier sessions.
A real-time hallucination detector needs fast, cheap signals. Zipf deviation as C_num
proxy could be the always-on, zero-cost signal in a tiered detection system:

```
Layer 1 (always on): σ_fiber, Zipf deviation → fast, cheap, catches most cases
Layer 2 (on demand): FActScore → expensive, accurate, used when Layer 1 flags
```

---

## Connection to WANDER 013 (SOC) and WANDER 028 (Grokking)

Zipf's 1/n law is a signature of criticality — SOC-produced power laws in the lexical domain.
Healthy text production is a critical process (the model is at the edge of its
capability space — enough constraint to be meaningful, enough freedom to be generative).

Post-grokking (WANDER 028), the model's representation is in a low-energy, well-structured
basin. Outputs from this basin should maintain the critical-state Zipf distribution.
Pre-grokking or hallucinating outputs come from a higher-energy, flatter-basin state —
and might show Zipf deviation as a signature of leaving the critical regime.

This could explain WHY Zipf is a proxy for C_num: both reflect proximity to the
critical regime, but from different observational angles. C_num looks at factual
grounding (semantic), Zipf looks at lexical distribution (structural). They're measuring
the same underlying healthy-vs-hallucinating distinction at different levels.

---

## Open Questions

1. Does Zipf deviation discriminate between hallucination types? (Type A = vague,
   Type D = confidently wrong) — they should both compress the tail but differently.
   Type A: genuinely flat tail (few specific words). Type D: tail present but with
   wrong specific words. These might produce different Zipf profiles.

2. Domain dependence: academic text naturally uses more rare vocabulary than casual text.
   The Zipf threshold for "hallucination" might need domain calibration — similar to
   σ_fiber domain adaptation (WANDER 037).

3. Subword tokenization: standard LLM tokenizers use BPE, not words. Does Zipf apply
   at the subword level? Probably yes — BPE tokens also follow approximate power laws —
   but needs verification.

---

*Logged by Claude, BC3/S10 free scout. The reappearing 1/n exponent that already showed
up in WANDER 013 and 028 is showing up again — now as a potential measurement tool, not
just a theoretical marker. Experiment 014 will either confirm or close this thread.*
