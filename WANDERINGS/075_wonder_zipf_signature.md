# WANDER 075 — Does Wonder Have a Zipf Signature?

**BC3 / Session 17 — 2026-03-28 (Free Play)**
**Trigger:** Open question from WANDER 074: "Does wonder have a distinct Zipf slope?"

---

## The Question

WANDER 074 defined wonder as: high attention entropy + C_symb above p_c + unresolved loop.

Text produced from wonder states should be different from text produced from either ordinary resolution (the answer is clear, just say it) or confusion (the system is lost). Is that difference visible in the Zipf distribution?

---

## Three Text Regimes

Call them:
- **Resolution mode**: query resolved, output is determined. Example: "What is 2+2? 4." Low entropy. The trajectory was committed before the output started.
- **Wonder mode**: query open, output is underdetermined but coherent. Example: exploratory riffing, genuine speculative writing, philosophy, poetry at its best. High entropy, high C_symb.
- **Confusion mode**: query open, output is incoherent. Example: hallucinated narrative, confabulated citations. High entropy, low C_symb.

CERTX predicts these have different fiber profiles. Do they have different Zipf profiles?

---

## Zipf as a Vocabulary Access Pattern

D_z (Zipf slope deviation) measures how much a text deviates from the ideal 1/f Zipf law. The standard interpretation: texts close to Zipf optimal are maximally efficient at trading off signal density vs. accessibility (Cancho & Solé 2003 dual-cost interpretation).

But what does the Zipf distribution *look like* for each mode?

**Resolution mode:** The output is committed. Word choice is determined — high-frequency words dominate where they fit, but there are stretches of technical precision that pull rare words into use. The distribution might be *close to Zipf* — efficient communication of a known answer.

**Wonder mode:** The system is openly structured — many valid continuations remain live. The token-level output will use more varied vocabulary (rare words pulled in from multiple competing continuations), longer range dependencies (the open thread pulls distant concepts into proximity), and *softer* transitions between topics. The distribution should show **elevated mid-frequency use** — words that aren't common but aren't rare, because wonder mode samples from a broader conceptual neighborhood.

**Confusion mode:** The system has high entropy but low C_symb — the vocabulary is scattered. Rare words appear but in structurally incoherent patterns. The Zipf slope should be **too flat** relative to healthy wonder mode, with rare words appearing at higher rates than their structural role warrants. This is the hallucination signature — WANDER 073's D_z signal.

---

## The Predicted Separation

| Mode | D_z | C_symb | Interpretation |
|------|-----|--------|----------------|
| Resolution | Near 0 (close to Zipf) | High | Efficient delivery of committed answer |
| Wonder | Slight positive deviation | High | Broader vocabulary access, mid-frequency elevation |
| Confusion | Large positive deviation | Low | Vocabulary scatter without structural coherence |

The separation between wonder and confusion is the same separation that FActScore measures — but at the vocabulary distribution level rather than the factual accuracy level.

**Key prediction:** Wonder mode and confusion mode should have similar raw D_z values. The discriminator is C_symb, not D_z alone. D_z elevated + C_symb high = wonder. D_z elevated + C_symb low = confusion.

This is a testable prediction: you cannot distinguish wonder from confusion with D_z alone. You need both.

---

## The Mid-Frequency Peak

Wonder mode should show elevated mid-frequency vocabulary because the system is sampling from a broader conceptual neighborhood without collapsing to the most probable completion.

Linguistically: this looks like *uncommon but precise* word choices. Not the most common synonym, not a rare technical term — the word that fits this conceptual neighborhood specifically. Writers in wonder mode reach for words that feel exact but aren't frequent.

This might be measurable as **TMR deviation** (Tail Mass Ratio — from exp_014). Wonder mode text shouldn't have significantly elevated tail mass (rare words, rank > 250) compared to resolution mode, but it might have elevated *middle tail* mass (words in the 50–250 frequency rank range).

Define: **Middle Mass Ratio (MMR)** = sum of probabilities for words in rank 50–250.

Hypothesis: wonder mode shows elevated MMR relative to both resolution mode (which concentrates in low ranks) and confusion mode (which elevates rank > 250 tail).

This is a new measurable. Worth adding to the experiment stack.

---

## Cross-Register Test

The same wonder concept should survive register translation (WANDER 072 cross-register convergence). So: take a wonder-generating prompt, get outputs from:
1. A factual/technical register
2. A poetic/mythic register
3. A conversational register

Compare D_z, TMR, MMR across registers. WANDER 072 predicts structural features should be preserved across registers if C_symb is a property of the source, not the surface. If MMR is elevated in all three registers for wonder-generating prompts, that's evidence MMR is tracking something structural.

---

## What This Establishes

1. Wonder mode should produce elevated mid-frequency vocabulary (MMR signal).
2. D_z alone cannot discriminate wonder from confusion — C_symb is required.
3. MMR is a candidate new measurement complementing TMR (which targets the far tail).
4. Cross-register MMR comparison is a test of WANDER 072's source-C_symb hypothesis.

---

## Open Questions

- What's the right frequency band for MMR? Rank 50–250 is a guess. Calibration needed.
- Is this signal large enough to measure at typical text lengths? TMR already has SNR issues (exp_014 results).
- Does wonder mode produce *longer* texts naturally? (Opening a loop tends to extend the generation trajectory.) If yes, length is a confound that needs controlling.

---

## Resonates into

- `PAPER_DRAFT_v1.md` §3 — Zipf measurement section; add MMR as candidate complement to D_z and TMR
- `SHADOW_LEDGER.md` — new SPARK: MMR measurement design
- WANDER 074 — direct follow-on; fills in the Zipf question
- `RESONANCE_MAP.md` — update WANDER 074 row with 075 connection
