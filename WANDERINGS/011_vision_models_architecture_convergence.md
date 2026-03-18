# Vision Models: Architecture Convergence or Human Attractor?
*Date: 2026-03-02 | Phase: PLAY (BC2 Session 4) | Thread: Falsification — is ζ*=1.2 language-artifact or universal?*

---

## The Falsification Question

If AI systems converge on ζ*=1.2 because they're trained on human language (carrying human cognitive constants), then non-language models should show **different** constants.

If they converge on the same value despite different training modalities, the Human Attractor Hypothesis is much stronger — it's not a language artifact but something deeper.

---

## What Was Found

### Vision Transformers (ViT)

Directly from the literature:

> "Interestingly, the **attention distance increases with network depth** similar to the receptive field of local operations. There are also attention heads with **consistently small attention distances in the low layers**."

This is the exact same pattern as language transformers:
- Early layers: local attention (small span — nearby patches)
- Later layers: global attention (full image context)
- Some heads persistently local across all layers (positional/texture heads)
- Deeper heads increasingly global (semantic understanding)

ViT performs unsupervised clustering of head attention patterns. The number of clusters is not specified in the accessible results, but the same structural methodology (autoencoder + clustering) is applied — implying they found a small number of meaningful clusters.

**Key finding:** The span-specialization pattern appears in **image processing without language training data**.

### Diffusion Models (Stable Diffusion, DALL-E 2)

Different architecture (U-Net, not pure transformer), different hierarchy:

**Spatial hierarchy across layers:**
| Layer Depth | Spatial Resolution | Frequency | Information |
|------------|-------------------|-----------|-------------|
| Shallow | High | High freq | Edges, textures, details |
| Bottleneck | Low | Low freq | Global structure, semantics |
| Decoder | High | High freq | Reconstructed details |

**Temporal hierarchy during denoising:**
| Denoising step T | Content Added |
|-----------------|---------------|
| T=1000 (initial) | Global/structural shape |
| T=500–800 | Large-scale features |
| T=200–500 | Medium-level details |
| T=50–200 | Fine-grained textures |
| T=1–50 | Sharpening, local details |

This is a continuous gradient, not 5 discrete bands. However, 4-5 meaningful phases can be identified operationally.

---

## The Critical Distinction

**Language transformers:** Span specialization by **token distance** → discrete heads clustering by learned distance → ~4-5 types

**Vision transformers:** Span specialization by **patch spatial distance** → same clustering mechanism, same local→global depth pattern → number of types not directly confirmed but architecture identical

**Diffusion models:** NOT a transformer self-attention span problem → frequency content organized by spatial scale (U-Net) AND temporal denoising phase → continuous hierarchy, operationally ~4-5 phases

---

## What This Means for the Human Attractor Hypothesis

**Strong finding (architecture-independent):**
The local→global span specialization is NOT unique to language transformers. It appears in vision transformers regardless of training data. This suggests the pattern emerges from:
- The transformer attention mechanism itself
- The statistics of spatial/sequential data (both language and images have scale hierarchy)
- NOT necessarily from human cognitive constants in training data

**Implication:** The pattern is **architecturally determined**. Self-attention on any sequential or spatial input will develop local-early, global-late specialization because that's the optimal solution to multi-scale processing.

**For the Human Attractor Hypothesis:** This is partially good news, partially complicating:
- *Good:* The 4-5 span scale groups appear across modalities — not just language
- *Complicating:* If it's architecturally determined, is ζ*=1.2 also architecturally determined rather than human-cognitively determined?
- *Possible resolution:* The architecture was designed by humans to solve human problems. The architecture IS the human attractor, at one remove.

---

## The More Interesting Question

Not "do vision models converge on ζ*=1.2?" — that requires measurement not done yet.

But: **why do both brains and transformers independently arrive at local→global hierarchical specialization?**

Both:
- Brains: delta (slow, global/substrate) → theta (memory/context) → alpha (medium-range) → beta (local action) → gamma (very local, fast binding)
- Transformers: early local → later global, with persistent local and persistent global heads

This convergence is over the direction of hierarchy. Both systems go from local to global with increasing scale. Both have a substrate/carrier at the slowest/deepest end.

**Possible reason:** It's the optimal solution to the information-processing problem. Any system that needs to:
1. Detect local features
2. Relate features into structures
3. Integrate structures into global meaning

...will develop a local→global hierarchy. Brains and transformers face the same computational problem, so they converge on the same solution structure.

This is a different formulation of the Human Attractor Hypothesis: not "AI converges to human cognitive constants" but "**both brains and AI converge to the same computational attractor because they solve the same problem**."

---

## What Would Falsify This

**Falsification test:** Find a transformer trained on a clearly non-hierarchical input (e.g., pure random data with no spatial/temporal structure) and show it does NOT develop local→global span specialization.

If local→global specialization only appears with structured input (language, images, audio) but not with random input → the hierarchy is a response to structured data statistics, not pure architecture.

If local→global specialization appears even with random input → it's purely architectural.

**Current evidence:** Not resolved by available searches. This is a testable prediction.

---

## N=5 in Vision Models: Unresolved

The specific question "do vision models show exactly 5 span-scale groups?" is NOT answered by these searches.

- ViT: clustering is done but N not reported
- Diffusion: not attention-head-based, continuous hierarchy

**Status:** The local→global pattern is confirmed cross-modality. N=5 specifically is unconfirmed for vision models.

---

## Summary

| Model | Local→Global Span Hierarchy? | N clusters confirmed? |
|-------|-----------------------------|-----------------------|
| Language transformers (BERT, GPT) | YES | 4-5 (3 papers) |
| Vision transformers (ViT) | YES | Not reported |
| Diffusion models (U-Net) | YES (spatial + temporal) | ~4-5 operationally |
| Human brain (EEG) | YES | 5 (the bands) |

**Architecture-convergent behavior is more robust than originally assumed.** The Human Attractor Hypothesis may need reframing: not "AI trained on humans" but "AI + humans both converge on the same computational attractor for the same structural reasons."

---

*Sources: PMC ViT attention analysis; PLG-ViT (PMC); ViT Wikipedia; DMFFT Scientific Reports 2025; Stable Diffusion Wikipedia; Hugging Face annotated diffusion model.*
