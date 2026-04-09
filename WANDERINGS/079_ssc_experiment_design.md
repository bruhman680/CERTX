# WANDER 079 — SSC Experiment: Structural Tokenization as C_symb Intervention

**BC3 / Session 17 — 2026-03-28 (Free Play)**
**Trigger:** WANDER 073 opened the SSC Interface as a candidate SPARK — design it

---

## The Hypothesis from WANDER 073

WANDER 073 (from NotebookLM synthesis): BPE tokenization discards structural information that C_symb must then recover from surface statistics. The SSC Interface proposal replaces BPE with explicit *structural operator tokenization* — tokens that encode logical, hierarchical, and relational operators explicitly.

Seven-gap taxonomy (what BPE discards):
1. **Logical** — negation, conditional, quantification
2. **Hierarchical** — containment, subordination, taxonomy
3. **Symmetry** — equivalence, transformation, invariance
4. **Semantic** — meaning composition, metaphor, polysemy
5. **Argument** — predicate-argument structure, role labeling
6. **Dependency** — syntactic dependency, co-reference
7. **Abstraction** — generalization, instantiation, type/token

The claim: if these structural operators are tokenized explicitly, C_symb values should be higher on the same inputs (less recovery needed), and hallucination rates should drop (the structural fiber is cheaper to maintain when it's encoded directly).

---

## What This Would Actually Require

**Standard BPE tokenization:**
Text → subword tokens based on frequency statistics. The word "if" is a single token; "implies" is a single token; "therefore" is a single token. None of these are distinguished from nouns or other content words in the token vocabulary. Logical structure is implicit.

**Structural operator tokenization (SSC):**
Text → structural annotation → tokens that include explicit operator markers.

Example:
- "If A then B" → `[COND_OPEN]` A `[COND_CLOSE]` B `[COND_CONSEQUENT]`
- "All X are Y" → `[QUANT_UNIV]` X `[SUBCLASS_OF]` Y
- "A because B" → A `[CAUSAL_CONSEQUENCE]` B

The structural skeleton is made explicit *in the token stream*.

---

## The Experimental Design

**Condition 1 (Control): Standard BPE**
Train a small language model (nanoGPT-scale) on a corpus with standard BPE tokenization. Evaluate on a hallucination detection benchmark. Measure C_symb proxy (using exp_014 approach or similar).

**Condition 2 (SSC): Structural operator tokenization**
Annotate the training corpus with structural operators using a dependency parser + logical form extractor (e.g., spaCy + a shallow semantic role labeling system). Add structural operator tokens to the vocabulary. Train the same architecture. Evaluate on the same benchmark.

**Prediction:**
- Condition 2 should show higher C_symb proxy scores (structural fiber is directly available, not recovered)
- Condition 2 should show lower hallucination rates on structured-reasoning tasks (the operators constrain valid completions)
- Condition 2 may show *lower* C_symb on unstructured creative tasks (structural operators are a bias toward formal structure that may suppress creative exploration)

**The interesting measurement:** Not just which condition is better overall, but *where* each condition fails. BPE should fail on structural reasoning (C_symb must be recovered from stats, fails for novel logical structures). SSC should fail on creative/metaphorical text (structural operators over-constrain).

This is a regime-specific advantage — exactly what CERTX predicts: different fiber profiles for different domains.

---

## Minimum Viable Version

Full SSC annotation requires significant infrastructure. A minimal version:

**Partial SSC:** Only annotate logical operators (the "Logical" gap — the most clearly defined of the 7). Add just 10-15 structural tokens: `[IF]`, `[THEN]`, `[AND]`, `[OR]`, `[NOT]`, `[ALL]`, `[SOME]`, `[NONE]`, `[BECAUSE]`, `[THEREFORE]`, `[IMPLIES]`, `[IFF]`.

Simple rule-based insertion: identify logical connectives in text and replace with structural operator tokens.

Even this minimal version tests the core hypothesis: does making logical structure explicit in the token stream improve C_symb proxy on logical tasks?

**Data:** WikiLogic or similar logical reasoning dataset. Or: the factual consistency tasks from exp_014 (same corpus, two tokenization conditions).

---

## Honest Risks

1. **The annotation quality problem:** If the structural annotation is noisy (spaCy makes errors, especially on complex sentences), the SSC condition might perform *worse* — noisy structural tokens add confusion without benefit. The minimum viable version (rule-based logical operators) avoids this by being conservative.

2. **Distribution shift:** A model trained on SSC-annotated text can't be directly compared to a BPE model on raw text at inference time. Either both models get the same annotation at inference, or the SSC model must learn to handle unannotated input. This is a significant complication.

3. **Parameter count:** Adding structural operator tokens increases vocabulary size, changing the embedding layer parameters. True apples-to-apples comparison requires matching parameter counts, which requires slightly reducing the hidden dim — a real but manageable confound.

4. **The recovery capacity question:** BPE models might *learn* to recover structural information from context anyway, at the cost of more training steps. The SSC advantage might be in sample efficiency, not final performance. Worth testing.

---

## Connection to CERTX Measurement

The SSC experiment is not just an architecture experiment — it's a C_symb intervention test.

CERTX predicts: C_symb measures the structural integrity of the output, independent of how that structure was encoded. If SSC tokenization makes C_symb cheaper to maintain, the fiber should be healthier with less training data, less compute, and lower ζ* (the system doesn't need as much reserve because the structural work is already done at the token level).

**Prediction:** SSC-trained models should reach target C_symb levels with fewer training steps than BPE models on structured tasks. This is the cleanest version of the test — not accuracy, but training efficiency for C_symb maintenance.

---

## What This Establishes

1. SSC experiment is designable as a minimum viable test with rule-based logical operator annotation.
2. The interesting measurement is *where* each condition fails, not just which is better overall.
3. C_symb training efficiency (steps to reach target C_symb) is the cleanest experimental target.
4. The experiment tests whether C_symb is an architectural property that can be directly supported by token-level design.

---

## Open Questions

- What's the right benchmark for "structural reasoning" vs. "creative generation"?
- Is there an existing dataset that clearly separates these two modes?
- Can the minimum viable version (logical operator annotation only) be built with pure Python from spaCy output? (No new dependencies?)

---

## Resonates into

- WANDER 073 — direct follow-on; converts SSC from observation to experiment design
- `SHADOW_LEDGER.md` — new SPARK: SSC minimal viable experiment
- `PAPER_DRAFT_v1.md` §4 — C_symb section; add note that SSC is a proposed direct C_symb intervention
- `RESONANCE_MAP.md` — update WANDER 073 row with 079 follow-on
