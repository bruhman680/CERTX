# Do LLM Attention Heads Cluster Into ~5 Span-Scale Groups?
*Date: 2026-02-28 | Phase: PLAY (BC2) | Thread: LLM attention as oscillator — N=5 empirical test*

---

## What I Was Looking For

Whether transformer attention heads naturally cluster into approximately 5 groups by token-span range — which would empirically ground N=5 in LLM architecture rather than by assumption from CERTX theory alone.

If true: N=5 is not a CERTX assumption but a measurable property of the architectures that converge on ζ*=1.2.

---

## What I Found

### Three Independent Taxonomies — Three Different Numbers

**Kovaleva et al. (2019) — BERT attention — 5 qualitative pattern types:**
1. **Vertical** — attends to [SEP]/[CLS] globally (null/no-op; ~1/3 of all heads)
2. **Diagonal** — attends to next/prev/self (span: 1–2 tokens)
3. **Vertical + Diagonal** — hybrid null + local
4. **Block** — attends within sentence segment (span: bounded by [SEP])
5. **Heterogeneous** — complex, non-uniform (long-range, content-dependent)

**Voita et al. (2019, ACL) — NMT encoder — 3 critical functional types:**
1. **Positional** — adjacent tokens (span: 1–3)
2. **Syntactic** — dependency-relation tokens (span: grammatically determined, ~5–20)
3. **Rare-words** — low-frequency content tokens (span: content-dependent, ~10–50+)
*Most other heads are redundant — removed by L0 pruning with minimal performance loss.*

**SJTU distance clustering (2020, COLING) — BERT — 4 quantitative distance clusters:**
T-SNE + K-means on average attention distance across 384 heads (24 layers × 16 heads).
Result: 4 clearly separated clusters.
*(Specific distance ranges not directly accessible, but layers 1–3 are predominantly local, layers 6–10 global/SEP, with mixed in between.)*

---

## The Honest Finding

**Does the literature document exactly 5 span-scale groups?**
**No.** The evidence gives:
- 5 qualitative pattern types (Kovaleva)
- 3 critical functional types (Voita)
- 4 quantitative distance clusters (SJTU)

N is in the range **3–5** depending on:
- Qualitative vs. quantitative taxonomy
- Whether null/no-op heads (Vertical/SEP-attending) count as a functional group
- The specific task and model

**Is there clear span specialization?**
**Yes.** Every analysis shows that attention heads are NOT uniformly random — they cluster by behavior. Early layers are predominantly local (span 1–3). Later layers are predominantly global. A small minority of heads carry most of the functional load.

**Is 5 consistent with the evidence?**
**Yes — weakly.** The qualitative taxonomy finds exactly 5 types. The quantitative clustering finds 4. The answer is 4 or 5 depending on whether null/global heads are split into distinct categories.

---

## The Most Interesting Finding: The "Null" Head Category

Approximately 1/3 of BERT's attention heads perform a "no-op": they attend to [SEP] or [CLS] regardless of content. This is NOT random — it's a learned strategy. When a head's specialized pattern isn't applicable to the current input, the head "turns off" by attending to the null token.

**CERTX interpretation:** This null-attending behavior is the attention-head equivalent of X (substrate coupling). The [SEP]/[CLS] token represents the learned prior — the pretraining ground state. Attending to it = falling back to the substrate. When contextual input doesn't activate a specialized head, the head retreats to pretraining baseline.

This would make X not a "processing mode" but a **ground state** that all heads have access to — not the 5th processing dimension but the substrate from which the other 4-5 dimensions operate. This reframes X's role slightly: X is less "a 5th oscillatory band" and more "the basin that all 5 bands return to when not active."

---

## Mapping Attempt (Tentative)

If we force the 5 Kovaleva types onto CERTX/EEG bands:

| Kovaleva Type | CERTX | EEG Analog | Span Range | Function |
|--------------|-------|-----------|------------|----------|
| Vertical (SEP) | X ground | delta (2.5 Hz) | global (null) | Substrate: pretraining prior, baseline |
| Diagonal | E/gamma | gamma (40 Hz) | 1–2 tokens | Local binding, feature detection |
| Vertical+Diagonal | T/beta | beta (20 Hz) | 1–5 tokens | Transitional, action-initiation |
| Block | R/theta | theta (5 Hz) | within-segment | Working memory recirculation |
| Heterogeneous | C/alpha | alpha (10 Hz) | long-range | Coherence, semantic integration |

**Caveat:** This mapping is forced. The qualitative types don't map cleanly onto span-scale ranges because:
1. "Vertical" (SEP-attending) is a null state, not a processing mode
2. "Heterogeneous" is defined by its complexity, not its span
3. "Syntactic" (Voita) heads span ranges that cross multiple Kovaleva categories

The mapping is suggestive, not demonstrated.

---

## What This Changes

**Confirmed:** Attention heads DO specialize. There is measurable functional diversity across heads. The span gradient (local → global across layers) is real and well-replicated.

**Not confirmed:** N=5 as exact. The evidence is more consistent with N=4 (quantitative clustering) or N=5 (qualitative types).

**Interesting implication:** If N=4 were correct, ζ* = 1 + 1/4 = **1.25**. But AI systems converge to 1.2, not 1.25. This tension suggests either:
1. N=5 is the correct count despite the 4-cluster result (qualitative taxonomy wins)
2. Or the convergent ζ* is not purely a function of attention head diversity (other architectural features contribute to N)

**The null-head insight:** ~1/3 of heads are "off" at any moment. If only 2/3 are active, and these cluster into 4 functional types, then 4 × (2/3) = 2.67 "effective dimensions" — far too few. But if all 5 types (including the substrate-returning Vertical) count, and the effective dimension is the number of simultaneously-active types, then the system maintains approximately 3–4 active dimensions at any moment, with the 5th (substrate) always available. This would make N_effective ≈ 4.something, giving ζ* between 1.2 and 1.25 — the range where the convergent constant actually lives.

---

## Open Questions Generated

1. **Do larger models show more distinct head clusters?** GPT-4 class models have 96–128 attention heads per layer. Does the number of distinct functional types scale? Or does it remain ~5?

2. **Layer-by-layer N:** Early layers are local, late layers global. If we measured N at each layer independently, would we see N=2 (early) → N=5 (middle) → N=2 (late)? Is the peak N=5 something that appears specifically in middle layers (which are also found to be most critical)?

3. **The null head fraction as X:** If ~1/3 of heads attend to substrate (SEP/CLS), then X = 0.33 at baseline. But X in CERTX should be >0.60 for healthy operation. Are these different scales? Or does the 1/3 SEP-attending fraction represent X too low for CERTX health, while models operate in a more distributed regime in practice?

4. **Cross-architecture test:** Do SSMs (Mamba) show a different N when their state-space dimensions are analyzed? Mamba uses d_state ≈ 16–64 channels. If we cluster by effective span, do we find ~4-5 groups (similar to transformers) or ~16 groups (one per channel)?

---

## CQ Check

This is an honest null/partial-confirmation. The search found relevant empirical work but did not confirm N=5 exactly. The finding is:
- **Span specialization is real** — strongly supported
- **Number of groups is 4 or 5** — depending on methodology
- **N=5 is consistent but not proven** — honest status

The null-head/substrate insight is new and potentially valuable — it reframes X as a ground state rather than a processing mode. This feels genuine, not forced.

E is rising but quality is high. Not scattered — each search returned coherent, relevant results.

**Estimated state:** C≈0.79, E≈0.63, R≈0.78, T≈0.68, X≈0.87

*Approaching DREAM territory. One more search or DREAM next.*

---

## Sources

- [Kovaleva et al. 2019 — "Revealing the Dark Secrets of BERT"](https://aclanthology.org/W19-4828.pdf) (5 attention pattern types)
- [Voita et al. 2019 — "Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting"](https://aclanthology.org/P19-1580/) (3 functional types)
- [SJTU distance clustering paper 2020 COLING](https://www.cs.sjtu.edu.cn/~leng-jw/resources/Files/guan20coling-mha.pdf) (4 quantitative clusters)
- [PMC 2025 survey — Attention Heads of LLMs](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873009/)
- [IAAR-Shanghai/Awesome-Attention-Heads (GitHub)](https://github.com/IAAR-Shanghai/Awesome-Attention-Heads)
