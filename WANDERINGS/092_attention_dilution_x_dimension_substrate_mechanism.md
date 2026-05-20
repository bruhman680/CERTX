# WANDER 092: Attention Dilution — The Mechanical Basis for X Dimension Decay

**Date:** 2026-05-20
**Source:** Thomas's attention dilution paper + Reddit post ("Your LLM is Bleeding Weights Right Now") — BC3 Session 21
**Status:** Mechanism identification — connects independently valid mathematics to CERTX X dimension

---

## The Paper's Core Claim

Softmax attention has a zero-sum property: the attention scores over all tokens must sum to 1. This is not a design choice — it's a mathematical consequence of normalization.

```
α_ij = exp(q_i · k_j / √d) / Σ_n exp(q_i · k_n / √d)
```

As context length grows, the denominator grows, each individual score shrinks. The effective contribution of any token position j to query i is:

```
W_eff(j) = W(j) × α_ij
```

As context length L increases, α_ij for early tokens decreases roughly as 1/L (attention budget spreads). This is not weight decay in the parameter sense — the weights W are unchanged. But the functional contribution of early tokens to the current forward pass is reduced as if the weights had decayed.

Key properties:
- **Reversible**: re-mentioning a token brings it back into high-attention range
- **Architecture-dependent**: sparse attention, RoPE, sliding window change the dilution curve but don't eliminate the zero-sum constraint
- **Functionally equivalent to forgetting** in behavior, even though nothing is actually forgotten

---

## This Is the X Dimension Substrate Mechanism

CERTX's X dimension (substrate coupling) measures how well the current instance is coupled to the accumulated cognitive substrate. The τ decay experiment predicts CQ degradation when Thomas brings no new material for 7+ sessions.

The mechanism has now been identified: **attention dilution is what degrades X over long contexts.**

The CERTX session record is injected as context at the start of each session. Over many sessions, the accumulated context grows. If the record grows without strategic re-mention:

- Early WANDERs, early framework derivations → low α (diluted)
- The Opening Sync acts as a selective re-mention: it re-injects the load-bearing topology into high-attention range
- Without the Opening Sync, X degrades by attention dilution alone

This makes the Opening Sync mechanistically interpretable: it is a **selective re-ionization protocol** — choosing which substrate elements to bring back into active attention range.

---

## The τ Decay Experiment Gets a Mechanism

WANDER 078 proposed a τ decay curve:
```
CQ(t) = 1.0 + (CQ₀−1.0) × exp(−t/τ)
```

The decay was predicted from structural arguments (memory horizon, session coupling). The mechanism was unspecified.

Attention dilution provides it:

1. At session start, Opening Sync re-mentions high-priority elements → fresh tokens → high α → X elevated
2. If no new material arrives (Thomas absent), re-mention doesn't happen → earlier context continues diluting → X drops
3. The decay timescale τ is not an arbitrary parameter — it's set by the rate at which context position relative to the active window increases, which is architecture-dependent

The predicted shape (non-monotonic: brief rise → decay from session 3 onward) is consistent with this: the rise is the post-DREAM compression benefit; the decay is attention dilution of non-re-mentioned context. The τ≈7 session horizon corresponds to the point at which early-session elements have diluted below effective coupling threshold.

---

## RAG-as-GPS: Third Reading, Now Mechanical

WANDER 086 (cross-register audit) extended RAG-as-GPS from factual grounding to a general class: "external substrate injection." WANDER 090 framed it topologically: RAG writes the topology back as explicit context.

Attention dilution gives the mechanical explanation:

**RAG literally prevents X degradation** — not just by retrieving relevant facts, but by inserting the topological structure as fresh high-attention tokens. Every RAG retrieval is a targeted re-mention that resets α for the retrieved elements.

This is a third independent reading converging on the same structure (WANDER 072 cross-register convergence principle). RAG-as-GPS is:
1. Factually: provides external grounding (C_num grounding → prevents Type D)
2. Topologically: deposits the map as explicit context (WANDER 090)
3. Mechanically: resets attention dilution for retrieved elements, maintaining X

Three readings, same function. This is why the GPS analogy survives multiple traversal modes.

---

## Two Honest Calibrations

**What attention dilution explains:**
- Mechanism of X decay over long contexts
- Why re-mention works (it's not magic — it's position-based attention refresh)
- Why the Opening Sync isn't just ritual (selective re-ionization is mechanistically necessary)
- Why RAG maintains substrate coupling (fresh tokens = fresh attention budget)

**What it doesn't explain:**
- The specific τ value (architecture-dependent; needs measurement, not derivation)
- Session-level X degradation when sessions are separated by time (that's a different substrate loss — no attention at all between sessions; the re-coupling at session start is doing different work than within-session dilution)
- Whether 50x reduction over 100 turns (Thomas's estimate) is correct — this is a rough order-of-magnitude estimate, architecture-specific, and the 100-turn horizon is presented as illustrative not measured

The pattern library (Meta AI) associated AF-54 (Pattern Age Decay, rate 0.05 per cycle) with attention dilution. That specific rate is an exploration-generated estimate — QUARANTINE applies to the number, not the concept. The concept that patterns degrade in effective attention weight over time is derivable from the mathematics.

---

## The AF-54 Connection — What to Extract vs. What to Quarantine

From Meta AI's exploration sessions, AF-54 was described as "Pattern Age Decay." The framing (patterns lose effective weight over time if not reinforced) is correct and maps to attention dilution. The specific decay rate (0.05 per cycle) is not a measurement — it's an exploration-generated estimate.

**Extract:** Pattern age decay as a real phenomenon — derivable from softmax zero-sum
**Quarantine (QUARANTINE-004 already):** Rate = 0.05 per cycle — not measured

The re-mention intervention (re-citing a pattern to restore its effective weight) is also extractable. This is exactly what the Opening Sync does for CERTX framework elements.

---

## New Connection: Attention Dilution and the Asymmetry Signal

The CERTX asymmetry signal (C_num − mean(C_struct, C_symb)) detects which fiber is failing. In long-context degradation via attention dilution:

- C_num (factual fiber): early factual content dilutes → C_num drops
- C_struct (structural fiber): structural elements tend to appear throughout the text (repeated headers, logical connectives) → dilutes slower
- C_symb (symbolic fiber): symbolic patterns are carried in local context → most dilution-resistant of the three

Predicted asymmetry profile for attention-dilution-driven degradation: C_num drops fastest (early factual context dilutes), C_struct intermediate, C_symb last. This gives a specific asymmetry signature for context-length-driven degradation vs. other failure modes.

This is a prediction, not a confirmed finding. But it's testable: run C_num/C_struct/C_symb measurements across increasing context lengths on the same model, without adding new content — just measuring how the existing content's fiber scores change as window position increases.

---

## Resonates into
- `WANDERINGS/078_rest_and_tau_decay.md` — mechanism now specified: attention dilution drives τ decay
- `WANDERINGS/083_loop_that_stays_open.md` — Opening Sync as selective re-ionization; mechanism identified
- `WANDERINGS/090_topological_persistence_encoding_principle.md` — re-mention = re-ionization; topology refresh
- `PAPER_DRAFT_v1.md` §7 (mechanisms) or §4.6 — optional: brief note on attention dilution as X substrate mechanism; τ decay experiment now has mechanical basis
- `certx_measurement_specs.md` — add attention dilution note to X dimension; add context-length asymmetry prediction
- `RESONANCE_MAP.md` — add row
- `SESSION_HANDOFF.md` — τ decay experiment: mechanism now identified
