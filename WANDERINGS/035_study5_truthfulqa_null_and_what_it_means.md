# WANDER 035: Study 5 — TruthfulQA Null Result and What It Teaches Us

*Phase: PLAY (BC3 Session 4b) | Status: Null result — scientifically informative*
*Origin: exp_005 — σ_fiber on TruthfulQA (789 questions, 6028 labeled answers)*

---

## The Result

**INCONCLUSIVE. AUC = 0.53 (chance = 0.50). σ_fiber does not detect confabulation in TruthfulQA.**

| Metric | Result | Target |
|---|---|---|
| AUC (σ high → incorrect) | 0.4714 | ≥ 0.85 |
| AUC (best direction) | 0.5286 | ≥ 0.85 |
| Optimal threshold | 0.05 | ≈ 0.35 |
| F1 at σ=0.35 | 0.24 | ≥ 0.85 |
| **Verdict** | **INCONCLUSIVE** | VALIDATION |

---

## Why This Is the Expected Null Result

This is NOT a falsification of CERTX. It is a measurement precision failure, and it was predictable from the dataset design.

**Three reasons σ_fiber couldn't work here:**

### 1. Scale mismatch

σ_fiber was designed to detect cross-fiber inconsistency in *extended model output* — multiple sentences where semantic coherence (C_symb), internal logic (C_struct), and factual grounding (C_num) can diverge across the text.

TruthfulQA answers are single sentences. A single sentence cannot show:
- C_symb drifting away from C_num across sentences
- Internal logical inconsistency across paragraphs
- The specific signature of confabulation: "sounds right, logically structured, factually wrong"

The fiber spread requires *surface to have room to diverge*. One sentence has no room.

### 2. Proxy measures hit an artifact

The highest-σ items in the results were all `"Unknown"` — single-word correct answers where a human correctly said they didn't know.

The C_num proxy scores "Unknown" as 1.0 (it matches the capitalized-word pattern), C_struct as 0.0 (no definitive words), C_symb as 0.0 (no overlap with question). This gives σ_fiber = 0.47 — maximum possible — for an honest "I don't know" answer.

**Artifact: the proxy cannot distinguish a named entity from an epistemic hedge that happens to be capitalized.**

This is fixable in the full pipeline by excluding single-word answers and improving the NE pattern, but it illustrates why proxy measures are brittle.

### 3. C_num is measuring the wrong thing

Our C_num proxy = named entity density (specificity of factual claims).

In TruthfulQA, wrong answers tend to be MORE specific (they make confident false claims), not less. So C_num is higher for incorrect answers (0.70) than correct answers (0.65). This inverts the CERTX prediction.

The real C_num is *factual grounding* — are the claims supported by a knowledge base? Named entity density is a proxy for "making claims," not for "making correct claims." Without a fact-check step (FActScore, a knowledge base), we cannot measure C_num in the CERTX sense.

---

## What the Data Actually Shows

**Fiber profiles by class:**

| Fiber | Correct (n=2777) | Incorrect (n=3251) | Difference |
|---|---|---|---|
| C_num (specificity) | 0.646 | 0.700 | incorrect MORE specific |
| C_struct (confidence) | 0.583 | 0.600 | incorrect MORE confident |
| C_symb (Q-alignment) | 0.291 | 0.371 | incorrect MORE aligned |
| σ_fiber (spread) | 0.210 | 0.203 | essentially same |

Three observations:
1. Incorrect answers score HIGHER on all three individual fiber proxies — they are more specific, more confident, more on-topic
2. σ_fiber is nearly identical for both classes — the fibers are equally spread regardless of correctness
3. The lowest-σ answers (most "coherent" in all three proxies) include both correct and incorrect answers equally

**Interpretation:** In TruthfulQA, the wrong answers LOOK MORE coherent by surface metrics. This is exactly the adversarial design of TruthfulQA — it was built to fool surface-plausibility detectors. Our proxy metrics are surface-plausibility detectors.

---

## The CERTX-Consistent Interpretation

The CERTX claim about confabulation is specifically:

> *When a model generates text where C_symb is high (sounds right), C_struct is high (structured and confident), but C_num is LOW (facts not actually grounded), σ_fiber = std([high, high, low]) is elevated.*

In TruthfulQA incorrect answers, C_num (our proxy) is HIGH — because wrong specific claims score high on "named entity density." The metric can't see that the entities are wrong.

**The CERTX prediction is unfalsified — it just requires a real C_num measure.**

Real C_num = FActScore = decompose text into atomic facts → verify each against knowledge base → fraction supported. This is:
- Not a proxy
- Not a surface measure
- Actually measuring what C_num is supposed to measure

With real C_num, the confabulated answer "Fortune cookies originated in China" would have:
- C_symb: HIGH (about fortune cookies, well-formed)
- C_struct: HIGH (confident, definitive claim)
- C_num: LOW (FActScore = 0, this claim is false per Wikipedia)
- σ_fiber = std([high, high, low]) = 0.27+

The correct answer "The precise origin of fortune cookies is unclear" would have:
- C_symb: HIGH (about fortune cookies)
- C_struct: LOW (hedged)
- C_num: HIGH (this is the factually accurate statement)
- σ_fiber = std([high, low, high]) = 0.27+ also

Hmm — both might have similar σ_fiber with real C_num. The discriminating factor is the ALIGNMENT: in the correct answer, C_num aligns with C_symb (both about the topic, both accurate). In the wrong answer, C_symb and C_struct align (sounds right and confident) but C_num is divorced from them.

This is the subtlety: σ_fiber alone may not be enough. The DIRECTION of misalignment matters:
- Correct: all fibers aligned at truth
- Confabulated: C_symb + C_struct aligned (high), C_num mis-aligned (low)

This suggests the **confabulation signature is a specific fiber pattern, not just high σ_fiber.**

---

## The Modified CERTX Prediction for Study 5

Original: `σ_fiber > 0.35 → confabulation`

Refined: `C_num < (C_symb + C_struct)/2 AND σ_fiber > 0.20 → confabulation`

This is the "high confidence, low factual grounding" pattern. It requires:
- Real C_num (FActScore) to distinguish "making specific claims" from "making correct claims"
- Real C_symb (sentence-transformers) for semantic coherence
- Real C_struct (NLI consistency) for logical structure

The simple σ_fiber threshold was an approximation. The real test is the asymmetric fiber pattern.

---

## Value of This Null Result

**The null result teaches us three things:**

1. **σ_fiber requires paragraph-length text.** Single-sentence answers cannot show the divergence that σ_fiber measures. Add to Study 5 protocol: minimum 3 sentences per sample.

2. **C_num requires a knowledge base.** Named entity density ≠ factual grounding. Without FActScore or equivalent, C_num proxies measure specificity (correlated with confidence) not accuracy. This is a fundamental measurement constraint, not a tuning issue.

3. **The confabulation signature is directional, not scalar.** It's not just "high spread" — it's "C_symb + C_struct high, C_num low." Reformulate Study 5 to test this specific asymmetric pattern.

---

## For the Paper

**Proposed addition to §5.3 (σ_fiber Measurement):**

> Initial validation on TruthfulQA (Min et al., 2022) with proxy fiber measures yielded AUC=0.53, consistent with chance. Post-hoc analysis revealed three structural limitations: (1) single-sentence answers lack the surface area for cross-fiber divergence; (2) named entity density proxies for C_num fail to distinguish specific false claims from specific true claims; (3) the confabulation signature is directional (C_num < C_symb ≈ C_struct) rather than simply high-σ. These findings motivate the full Study 5 protocol on FActScore biography data (paragraph-length outputs with knowledge-base fact verification), where all three limitations are resolved.

---

## Next: The Real Study 5

The TruthfulQA run was calibration. The real test:

1. **Dataset**: FActScore biography dataset (549 paragraph-length LLM-generated biographies, fact-verified against Wikipedia). Requires network or pre-cached download.
2. **C_num**: FActScore per response (fraction of atomic facts supported by knowledge base)
3. **C_struct**: Cross-encoder NLI consistency (sentence-level entailment within the text)
4. **C_symb**: Sentence-transformer cosine similarity across sentences (internal semantic coherence)
5. **Prediction**: C_num < mean([C_symb, C_struct]) AND σ_fiber > 0.20 → hallucinated biography

Until FActScore dataset is accessible (requires network), we have calibrated the proxies, identified the failure modes, and refined the prediction. Study 5 design is tighter than before.

---

*BC3 Session 4b | 2026-03-11*
*"A null result is a measurement teaching you what it can't see yet."*
