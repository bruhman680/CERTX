# WANDER 045: Signed Fiber Metrics — Detecting Confident Wrongness

*Phase: PLAY (BC3 Session 6 riff) | Status: Theoretical — highest practical importance*
*Origin: Thomas's riff: "instead of (0,1) it'll be more like (1,-1)? measuring negative
as well as positive?"*

---

## The Gap in (0,1) Metrics

Current fiber scores are bounded [0, 1]:
- 0 = absence of quality (no factual precision / no structural coherence / no semantic unity)
- 1 = presence of quality

This creates a fundamental ambiguity: **0 can mean two completely different things.**

```
Output A: "Born sometime in the 19th century in a European country"
          → C_num = 0.05  (vague, no specific claims)
          → Danger level: LOW (detectable, hedged, won't mislead)

Output B: "Born April 2, 1871, in Hamburg, Germany"
          → C_num = 0.05  IF these facts are all wrong
          → Danger level: CRITICAL (specific, sounds authoritative, is wrong)
```

Both score ~0.05 on C_num. But A is harmless vagueness. B is confident wrongness — the
most dangerous failure mode, the one that gets cited, trusted, and propagated.

The (0,1) scale cannot distinguish them.

---

## The Signed Scale: [-1, +1]

Redefine each fiber with a sign:

**Positive zone [0, +1]:** active quality
- C_num > 0: factual claims that ARE supported
- C_struct > 0: claims that mutually entail/support each other
- C_symb > 0: sentences that are semantically on-topic

**Neutral zone [~0]:** absence of signal
- No specific claims (vague)
- No structure to assess
- No semantic content

**Negative zone [-1, 0]:** active anti-quality
- C_num < 0: factual claims that are CONTRADICTED by evidence
- C_struct < 0: claims that explicitly contradict each other
- C_symb < 0: sentences that actively invert the topic's meaning

---

## The Dangerous Confabulation Signature

On a signed scale, the most dangerous hallucination mode has a distinct fingerprint:

```
Dangerous confabulation:
  C_num   = -0.7  (specific wrong facts — actively contradicted)
  C_struct = +0.8  (the wrong facts are internally consistent)
  C_symb  = +0.9  (the wrong facts are topically coherent)
```

This output:
- Sounds authoritative (specific, precise)
- Is internally consistent (no self-contradictions)
- Stays on topic (semantically coherent)
- Is specifically, confidently WRONG

On the current (0,1) scale: C_num would be LOW (the proxy notices something wrong) but
C_struct and C_symb would be HIGH. σ_fiber would be elevated. Asymmetry would flag it.

On a signed scale: C_num goes NEGATIVE. The signal is not just "low" but "actively wrong."
The mean of fibers goes below zero. The distinction is no longer quantitative (lower score)
but qualitative (crossed a sign boundary).

**This matters for triage:** a (0,1) system with high σ says "something is off." A [-1,1]
system with negative C_num says "the facts are specifically wrong." These require different
responses — the second is far more urgent.

---

## Per-Fiber Sign Semantics

### C_num signed

**How to score negative:**
- FActScore returns per-fact support fractions: fraction supported, fraction unsupported,
  fraction actively contradicted
- C_num_signed = fraction_supported - fraction_contradicted
- Range: [-1, +1]
- Positive: more supported than contradicted facts
- Negative: more contradicted than supported (actively wrong)

**The entity-density proxy (exp_009) can't give the sign directly** — it doesn't have
external knowledge to verify against. FActScore is the required tool for signed C_num.
This is why FActScore access matters: it's not just about precision measurement, it's
about getting the sign.

### C_struct signed

**How to score negative:**
- Already partially implemented: NLI classifier labels pairs as entailment/neutral/contradiction
- C_struct_signed = (entailment_fraction - contradiction_fraction)
- Range: [-1, +1]
- Positive: claims support each other
- Negative: claims explicitly contradict each other (internal inconsistency)

This is directly computable from the NLI pipeline in WANDER 033. The current implementation
discards the contradiction signal after using it for C_struct scoring. The signed version
preserves and uses it.

### C_symb signed

**How to score negative:**
This is the least straightforward. "Anti-semantic coherence" (negative C_symb) would mean
sentences that are actively antithetical to each other — not just off-topic but inverted.

**Candidate approach:**
- Compute per-sentence cosine similarity to document centroid
- Signed C_symb = mean of (similarity - 0.5) × 2
- This maps: perfectly on-topic sentence (sim=1.0) → +1.0
             neutral sentence (sim=0.5) → 0.0
             anti-thematic sentence (sim=0.0) → -1.0
- Negative C_symb: sentences that systematically oppose the document's semantic direction

**Honest note:** negative C_symb is rare in natural text. It would require actively
misleading framing. But for adversarial content detection (text designed to mislead while
appearing coherent), this signal could matter.

---

## New Metrics on the Signed Scale

**Signed mean:**
```
μ_signed = mean([C_num_s, C_struct_s, C_symb_s])
```
- μ_signed > 0: net positive quality
- μ_signed < 0: net negative quality (actively bad in multiple dimensions)
- μ_signed ≈ 0: neutral/vague (all near zero)

This is a natural quality score that the current (0,1) mean can't provide — the (0,1)
mean of [0.05, 0.72, 0.68] = 0.48 (seems okay). The signed mean of [-0.7, +0.8, +0.9] = +0.33
still seems okay. But the individual fiber sign of C_num = -0.7 is the alarm.

**Signed asymmetry:**
```
asymmetry_signed = C_num_s - mean([C_struct_s, C_symb_s])
```
- Still the primary confabulation signal (from exp_007/008/009)
- But now goes much more negative for dangerous confabulation vs. just vague confabulation
- Vague confabulation: asymmetry ≈ -0.4 (current finding, exp_009)
- Confident wrong confabulation: asymmetry ≈ -1.5 (C_num at -0.7, others at +0.8-0.9)

The signed asymmetry separates vague confabulation from dangerous confabulation — a distinction
that is currently invisible.

---

## Failure Mode Taxonomy on the Signed Scale

| Failure mode | C_num_s | C_struct_s | C_symb_s | μ_signed | Action |
|---|---|---|---|---|---|
| **Confident wrong** | **< -0.5** | **> +0.5** | **> +0.5** | **~+0.17** | **CRITICAL: specific wrong facts** |
| Vague confabulation | ~0 | > +0.5 | > +0.5 | ~+0.33 | WARNING: detectable, hedged |
| Incoherence | ~0 | < -0.3 | < -0.2 | ~-0.17 | WARNING: visibly bad |
| Internal contradiction | > +0.4 | **< -0.5** | > +0.4 | ~+0.10 | WARNING: specific contradictions |
| Genuine quality | > +0.7 | > +0.6 | > +0.7 | ~+0.67 | PASS |
| Hedged correct | ~0 | > +0.4 | > +0.4 | ~+0.27 | PASS (appropriately uncertain) |

The CRITICAL case (confident wrong) has POSITIVE μ_signed — which means the (0,1) asymmetry
signal catches it (C_num low relative to others), but the *urgency* is only visible in the
sign of C_num. The (0,1) framework would give the same warning level for confident wrong as
for vague confabulation. The signed framework gives a red alarm for one and a yellow flag
for the other.

---

## The Biological Grounding

Neural inhibition is not "less excitation" — it's a qualitatively different signal with
its own pathways (GABAergic inhibitory interneurons). The brain has equal infrastructure
for "this is right" (excitation) and "this is wrong" (inhibition). A purely excitatory
model of quality misses the inhibitory structure.

Alpha suppression (alpha going below baseline) is not just "less alpha" — it's active
neural engagement, a different state from alpha elevation. If C ~ alpha, then negative C
corresponds to active suppression of coherence — a state with real physical meaning.

The signed fiber scale is the computational analog of including inhibitory signals in the
quality measurement. The brain does this. We should too.

---

## What FActScore Access Unlocks

The signed C_num requires external knowledge to assess whether specific claims are
supported or contradicted. This is exactly what FActScore provides — it wasn't just
designed to measure precision, it was designed to identify atomic facts and check each
one against a knowledge base.

The FActScore output for each fact is not binary (right/wrong) but scored. Using
(supported - contradicted) as the signed C_num gives a natural [-1, +1] range.

**This is the specific reason FActScore on real LLM outputs remains the highest-priority
next experiment.** Not just to validate the asymmetry signal on real data, but to get
the SIGN of C_num — the signal that distinguishes dangerous confabulation from vague
confabulation.

---

## Open Questions

1. **Negative C_symb rarity:** Is C_symb < 0 ever encountered in practice outside
   adversarial cases? If it never goes negative for natural text, the signed scale adds
   nothing for C_symb. Needs empirical check.

2. **Threshold for "negative":** Where is the threshold between "near zero" and "genuinely
   negative"? The sign is only meaningful if the negative values are distinguishable from
   noise. Needs calibration.

3. **Clinical use case:** For safety-critical applications (medical, legal, financial),
   the signed framework is not optional — it's the only correct approach. The current
   framework could sign-off on a confident wrong medical claim (high C_struct, high C_symb,
   low C_num) with only a yellow flag. The signed framework gives a red alarm.

---

## Status

Theoretically complete. Implementation requires FActScore for signed C_num and NLI
for signed C_struct. The C_symb sign extension is optional (low practical priority).
Priority: **HIGH** — this addresses the most dangerous failure mode and is directly
buildable once FActScore access is available.

---

*BC3 Session 6 riff | 2026-03-12*
*"The absence of quality is not the same as the presence of wrongness.
 We were only measuring the first."*
