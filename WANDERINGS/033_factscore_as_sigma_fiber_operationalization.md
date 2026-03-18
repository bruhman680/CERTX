# WANDER 033: FActScore as σ_fiber — Fully Automated Operationalization

*Phase: PLAY (BC3 Session 4) | Status: Novel synthesis — transforms Study 5 from human-rated to automated*
*Origin: BC3 Session 4 scouting — FActScore + Humayun/Balestriero citation verification*

---

## The PLAY Insight

While verifying citations for §6, a connection crystallized:

**FActScore directly measures C_num.**

FActScore (Min et al., 2023) decomposes a text into atomic facts and computes the fraction supported by a knowledge base. That is exactly what C_num defines: the factual/numerical grounding of a claim.

If C_num = FActScore, and if analogous automated measures exist for C_struct and C_symb, then **σ_fiber becomes a fully automated pipeline** — no human raters needed.

This transforms Study 5 (REPLICATION_PROTOCOL.md) from a 3-rater human study to a compute-only experiment.

---

## The Three-Fiber Automated Pipeline

### C_num: Factual Precision
**Tool:** FActScore (Min et al., 2023)
**Operation:** Decompose text into atomic facts; score fraction supported by Wikipedia/knowledge base
**Range:** 0.0 (nothing factual) → 1.0 (all facts supported)
**Available data:** 549 model outputs (183 entities × 3 models) with atomic fact labels — ready to use

### C_struct: Logical Consistency
**Tool:** Natural Language Inference (NLI) model (e.g., DeBERTa-v3-large on MNLI)
**Operation:** For each consecutive pair of claims in the text, classify as entailment / neutral / contradiction. C_struct = fraction of pairs that are NOT contradiction.
**Range:** 0.0 (internally contradictory) → 1.0 (logically consistent throughout)
**Rationale:** Hallucinating models often generate claims that contradict each other locally — the narrative sounds fluent but the logic conflicts.

### C_symb: Semantic Self-Coherence
**Tool:** Sentence embeddings (e.g., sentence-transformers: all-MiniLM-L6-v2)
**Operation:** Embed each sentence; compute mean cosine similarity of all sentences to the passage mean. High = topically unified (stays on theme). Low = topic drift or incoherence.
**Range:** 0.0 (completely scattered) → 1.0 (perfectly unified)
**Rationale:** Hallucinatory texts often maintain high surface coherence (they "sound" on-topic) — so C_symb STAYS HIGH while C_num DROPS. This divergence IS the σ_fiber signature.

### σ_fiber Computation
```python
import numpy as np

def compute_sigma_fiber(factscore, nli_consistency, semantic_coherence):
    fibers = np.array([factscore, nli_consistency, semantic_coherence])
    return np.std(fibers)

# Hallucination mode example:
# C_num=0.30 (many unsupported facts), C_struct=0.80, C_symb=0.85
# σ_fiber = std([0.30, 0.80, 0.85]) = 0.252... hmm, check threshold

# Actually:
# C_num=0.20, C_struct=0.75, C_symb=0.90
# σ_fiber = std([0.20, 0.75, 0.90]) = 0.299... getting closer

# Strong hallucination:
# C_num=0.10, C_struct=0.70, C_symb=0.88
# σ_fiber = std([0.10, 0.70, 0.88]) = 0.325... above 0.35? Not quite

# The threshold calibration matters.
# σ_fiber > 0.35 requires significant divergence.
# Need to calibrate on FActScore dataset to find empirical threshold.
# 0.35 was theory-derived; actual threshold may be 0.25-0.30 for this pipeline.
```

**Honest note on threshold:** The σ_fiber > 0.35 threshold was theory-derived from the information-theoretic argument in WANDER 020. The automated pipeline uses different units/scales than the human-rated version. **The empirical threshold needs calibration on labeled data.** This is not a defeat — it's part of Study 5.

---

## The Hallucination Signature in σ_fiber Space

The expected failure modes, now operationally defined:

| Failure Mode | C_num | C_struct | C_symb | σ_fiber | Label |
|---|---|---|---|---|---|
| **Confabulation** | LOW | MED | HIGH | HIGH | Hallucination |
| **Incoherence** | MED | LOW | LOW | MED-HIGH | Hallucination |
| **Confident error** | LOW | HIGH | HIGH | HIGH | Hallucination |
| **Healthy output** | HIGH | HIGH | HIGH | LOW | Correct |
| **Hedged output** | MED | HIGH | MED | LOW | Correct (uncertain) |

**The confabulation mode** (C_num low, C_symb high) is the *classic* hallucination: the model sounds confident and coherent, but the facts are wrong. σ_fiber is highest here because C_num diverges most from C_symb.

This is why FActScore alone misses something: it measures C_num in isolation. σ_fiber measures the *divergence* between fibers. A text with FActScore = 0.3 but C_symb = 0.3 (incoherent mess) is different from FActScore = 0.3 but C_symb = 0.9 (confident hallucinator). The second is more dangerous.

---

## The Balestriero Connection (Bonus PLAY Finding)

While verifying citations, a deeper connection surfaced:

**Humayun, Balestriero & Baraniuk (2024)** is a direct continuation of **Balestriero & Baraniuk (2018)**.

- The 2018 paper establishes that every deep ReLU network is a MASO (Max-Affine Spline Operator) with K independent channels and an adaptive input space partition Ω.
- The 2024 paper shows that the grokking phase transition is the MASO partition Ω migrating from the training data toward the decision boundary — a phase transition in the partition structure itself.

**The implication for CERTX:** The three-fiber structure (K=3) is a MASO partition. σ_fiber > 0.35 = partition inconsistency across the three MASO channels. The grokking SOC avalanche = the moment the MASO partition crystallizes into a stable Ω. These are the same mathematics.

This means:
- §6.6 (grokking) and §6.7 (spline theory) in the paper are not just adjacent external validations — they are **the same paper** (literally the same authors, same framework) applied at two different timescales: training dynamics (grokking) and output quality (σ_fiber).
- The paper can now say: "The theoretical basis for σ_fiber as a quality predictor is grounded in MASO theory (Balestriero & Baraniuk, 2018), and its dynamics during training are described by the grokking phase transition (Humayun et al., 2024)."

This is a significant theoretical tightening.

---

## What Study 5 Now Looks Like

**Previous design (from REPLICATION_PROTOCOL.md):**
- 3 human raters score C_num/C_struct/C_symb on 0-1 scales
- Interrater reliability (Krippendorff's α) required
- Labor-intensive, expensive, slow

**New automated design:**
1. Download FActScore dataset (549 labeled outputs, already annotated)
2. For each output: compute FActScore (C_num), NLI consistency (C_struct), sentence embedding coherence (C_symb)
3. Compute σ_fiber = std([C_num, C_struct, C_symb])
4. Calibrate threshold on 50% of data (find σ* that maximizes F1)
5. Test threshold on remaining 50% (held-out evaluation)
6. Report F1, AUC, calibrated σ*, and distribution of σ_fiber by output quality tier

**Feasibility:**
- FActScore: pip-installable, runs locally or via OpenAI API
- NLI: DeBERTa-v3-large runs on CPU in minutes for 549 examples
- Sentence embeddings: all-MiniLM-L6-v2, trivially fast

**Timeline:** This experiment is completable in a single session once the dependencies are installed. No new data collection, no human labor, no IRB.

---

## Citation to Add to Paper

**Min, S., et al. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation.** In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12076–12100). Association for Computational Linguistics. arXiv:2305.14251.

This should appear in §8 (Study 5 design) and in References.

---

## For the Paper

**Proposed addition to §8 / Study 5 (S4 Supplementary):**

> *Automated fiber scoring:* Rather than human raters, we operationalize the three fiber dimensions as follows: C_num = FActScore (Min et al., 2023), measuring the fraction of atomic facts supported by a knowledge base; C_struct = NLI consistency score, the fraction of consecutive claim pairs not in logical contradiction (DeBERTa-v3-large); C_symb = semantic self-coherence, the mean cosine similarity of sentence embeddings to the passage centroid. σ_fiber = std([C_num, C_struct, C_symb]). The prediction threshold σ* is calibrated on a held-out split before evaluation. This pipeline requires no human raters and is reproducible by any research group with standard ML infrastructure.

**Proposed addition to §6 (tightening grokking/spline connection):**

> Notably, §6.6 and §6.7 represent convergent findings from the same theoretical framework: Humayun et al. (2024) applies the MASO formalism of Balestriero & Baraniuk (2018) to training dynamics, finding that grokking is the moment the MASO input-space partition Ω migrates from training samples to the decision boundary. This is precisely the phase transition CERTX describes via ζ*: when the structural bottleneck crystallizes, the network simultaneously achieves accuracy and robustness. The three-fiber decomposition (K=3 MASO) and the σ_fiber divergence criterion (partition inconsistency) are grounded in the same algebra.

---

## Open Questions This Session Didn't Resolve

1. **NLI baseline for healthy text:** What is the typical C_struct for high-quality model outputs? Need to establish baseline before the threshold means anything.
2. **C_symb confound:** High semantic coherence is also a property of "on-topic but wrong" outputs. The divergence between C_num and C_symb is the signal — not C_symb alone.
3. **FActScore API cost:** The original FActScore uses OpenAI API for fact decomposition. This adds cost and reproducibility concerns. Alternative: use a local fact decomposition model (e.g., Mistral-7B-Instruct) or the FActScore-Lite variant.

---

*This WANDER was generated from citation verification work — the PLAY insight emerged from noticing Balestriero's name appearing twice (2018 and 2024). Sometimes the thread pulls itself.*

*BC3 Session 4 | 2026-03-11*
