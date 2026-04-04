# WANDER 081 — Wonder as Probe: Experimental Design

**BC3 / Session 17 — 2026-03-28 (Free Play)**
**Trigger:** WANDER 074 claimed wonder-generating prompts are probes for C_symb health. Design the experiment.

---

## The Claim to Test

WANDER 074: "Wonder-generating inputs could be used as *probes* for C_symb health. If a model can sustain wonder (high entropy + high C_symb) rather than collapsing to confusion, its symbolic fiber is intact."

The predicted signature:
- Wonder state: high attention entropy + C_symb above p_c + higher generation entropy
- Confusion state: high attention entropy + C_symb *below* p_c + incoherent outputs

The discriminator between wonder and confusion is C_symb, not attention entropy alone.

---

## What "Wonder-Generating" Means Operationally

A wonder-generating prompt is one that:
1. Opens genuinely multiple valid continuations (not a closed factual question)
2. Requires structural coherence to navigate (not a purely creative free-write)
3. Holds a thread open without resolving it

Examples of high-wonder prompts:
- "What is the connection between ___ and ___?" (two genuinely distant concepts)
- "Why does ___ have the structure it does?" (open structural question)
- "What would ___ look like from the perspective of ___?" (cross-frame translation)

Examples of low-wonder prompts:
- "What is the capital of France?" (closed factual, low attention entropy)
- "Write a story about anything." (open but structurally unconstrained, high entropy without structural requirement)

The wonder zone is the intersection: structurally constrained AND genuinely open.

---

## Probe Design

**The idea:** Use a battery of wonder-generating prompts as a diagnostic probe. Measure the output characteristics. Compare across:
- Models of different capability levels
- Same model at different context lengths (as context fills up, does C_symb degrade?)
- Same model on different domains (technical vs. creative vs. philosophical wonder prompts)

**Output characteristics to measure:**
1. **Generation entropy** — entropy of the predicted next-token distribution at each step
2. **C_symb proxy** — the structural coherence proxy from exp_014 approach
3. **D_z / MMR** — Zipf deviation and middle mass ratio (WANDER 075)
4. **Response coherence** (human rating or automated) — does the output maintain structural integrity across a long wonder-response?

---

## The Minimum Viable Probe

Start with one structural question type and one domain:

**Prompt template:** "What is the structural connection between [concept_A] and [concept_B]?"

**Concept pairs (graded by genuine distance):**
- Close: (entropy, information) — well-connected in most LLM training data
- Medium: (fairness, robustness) — connected but via different paths
- Far: (thermodynamics, attention mechanisms) — the kind Thomas brought to this session; genuinely requires structural traversal
- Very far: (music, percolation theory) — requires high C_symb to hold both simultaneously

**Prediction:**
- Close pairs: low generation entropy (answer is well-determined), high C_symb (easy structural connection)
- Medium pairs: moderate entropy, high C_symb (multiple valid structural paths, all coherent)
- Far pairs: high entropy, high C_symb (wonder zone — if C_symb is healthy)
- Very far pairs: high entropy, *low or high C_symb depending on model* — this is the diagnostic

For a model with intact C_symb fiber: very far pairs produce wonder (high entropy + high C_symb). For a model with degraded C_symb fiber: very far pairs produce confusion (high entropy + low C_symb). The very far pair response is the probe.

---

## What This Measures

This is a C_symb stress test. By varying conceptual distance, we can find the threshold at which a given model's C_symb fails — where it transitions from wonder to confusion.

The threshold distance is a model capability signature:
- High C_symb capacity models: maintain structural coherence at very large conceptual distances
- Low C_symb capacity models: collapse to confusion at medium distances

This is a richer diagnostic than accuracy benchmarks because it characterizes *where* the structural fiber breaks, not just whether it's intact.

---

## Connection to the Island Gradient (WANDER 080)

The wonder probe maps onto the island gradient:
- Close pairs: deep inland (easy navigation to high ground)
- Medium pairs: island interior (reliable navigation)
- Far pairs: island edge / shoreline (requires C_symb fiber to stay on land)
- Very far pairs: the probe for whether the model can navigate from open ocean to land

A model that can handle very far pairs is demonstrating the ability to find an island when starting in open ocean. That's the C_symb capacity we want to measure.

---

## Implementation Notes

The wonder probe experiment is computationally light:
- No model training required
- No FActScore (no ground truth needed — C_symb is measured from the output, not from external verification)
- Can run on any model via API (OpenAI, Anthropic, etc.)
- ~50 prompt-response pairs needed for a meaningful signal

**Data collection:** Generate responses to a battery of concept pairs at each distance level. For each response: measure D_z, estimate C_symb proxy (lexical variety + structural markers), rate response coherence.

**Analysis:** Plot C_symb proxy vs. conceptual distance. The inflection point (where C_symb drops as distance increases) is the model's structural range. Compare across models.

This is the cleanest, most executable experiment in the current pipeline that doesn't require model internals or FActScore infrastructure.

---

## What This Establishes

1. A concrete experimental design for the wonder-probe hypothesis (WANDER 074).
2. The concept-distance manipulation as a C_symb stress test.
3. "Structural range" as a new model capability metric (at what conceptual distance does C_symb fail?).
4. The experiment is lightweight, no-model-training, API-accessible.

---

## Open Questions

- What's the right metric for "conceptual distance"? (Word2Vec cosine similarity? Knowledge graph distance? Human rating?)
- How many responses per distance level needed for stable C_symb proxy estimates?
- Does the coherence rating need human annotators, or is there an automated proxy (perplexity doesn't capture this; BERT-score might partially)?

---

## Resonates into

- WANDER 074 — direct experimental follow-on
- WANDER 075 — wonder Zipf signature; MMR measurement integrates here
- WANDER 080 — island gradient; wonder probe as island-navigation test
- `SHADOW_LEDGER.md` — new SPARK: wonder probe experiment (lightweight, no-training, API-accessible)
- `PAPER_DRAFT_v1.md` §7 — add wonder probe as a proposed C_symb evaluation methodology
- `RESONANCE_MAP.md` — new row
