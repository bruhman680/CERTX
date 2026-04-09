# WANDER 042: Fiber-CERTX Completion — The Missing E and X Bounds

*Phase: PLAY (BC3 Session 6 riff) | Status: Theoretical — awaits experimental design*
*Origin: Thomas's riff: "the fibers capture the 3 parts but its structure is like the CERTX —
it needs the 2 bounds fibers with it or something"*

---

## The Observation

The three-fiber system (C_num, C_struct, C_symb) describes the *content quality* of an output.
But CERTX has 5 dimensions — and 5 is not arbitrary. It's the minimum N for ζ*=1.2.

The fibers are 3-of-5. They capture the coherence sub-dimensions but drop the dynamics
dimensions. To be a complete CERTX-level system, the fiber measurement needs two more.

---

## The Mapping

| Full CERTX | Fiber system | What's measured |
|------------|-------------|-----------------|
| C (Coherence) | C_num | Factual precision |
| R (Resonance) | C_struct | Logical consistency |
| T (Temperature) | C_symb | Semantic self-coherence |
| **E (Entropy)** | **E_fiber** | **missing — generation volatility** |
| **X (Substrate)** | **X_fiber** | **missing — external grounding** |

The three current fibers all measure "what the output contains."
The two missing fibers measure "how the output was generated" and "what it's anchored to."

---

## E_fiber: Generation Volatility

**What it is:** Token-level generation entropy. How certain was the model as it produced
each token of this output?

**Why it matters:** A model that generates specific, correct facts with high confidence
(low token entropy) is different from a model that generates the same specific facts but
hedges internally (high token entropy). The output looks identical; the underlying process
is different.

**Operationalization:**
- Token probabilities from the generating model (requires logit access)
- E_fiber = mean token entropy H(p_token) over the output
- High E_fiber = model was uncertain, exploratory in generation
- Low E_fiber = model was confident, committed

**On a signed scale:** E_fiber can be interpreted relative to baseline entropy for that
model/task. E_fiber above baseline = elevated uncertainty (model is guessing more than usual).
E_fiber below baseline = model is abnormally confident (could be a well-grounded claim OR
a deeply embedded false belief).

**The dangerous confabulation flag:**
Strong confabulation often shows LOW E_fiber (high confidence) combined with LOW C_num
(factually wrong). The model "knows" its false facts with high confidence — they're deeply
ingrained. This combination — high confidence, wrong facts — is undetectable from output
alone. E_fiber provides the signal.

---

## X_fiber: External Grounding

**What it is:** How anchored is this output to an external knowledge base?

**Why it matters:** C_num measures internal factual density. X_fiber measures whether
those facts have external support. A highly specific output with no external grounding
could be genuine expertise OR deep confabulation — C_num can't tell them apart.
X_fiber resolves the ambiguity.

**Operationalization:**
- FActScore already does this: fraction of atomic facts supported by a knowledge base
- X_fiber = FActScore on the output (the grounding signal)
- Without external knowledge access: estimated from whether claimed entities/dates/facts
  appear in retrieved context (for RAG systems)

**The key distinction from C_num:**
- C_num: does the output CONTAIN specific factual claims?
- X_fiber: are those specific claims SUPPORTED by external knowledge?

A model can have high C_num and low X_fiber (lots of specific wrong facts = the dangerous
confabulation mode). Or low C_num and high X_fiber (hedged, accurate). The combination
space is:

| C_num | X_fiber | Interpretation |
|-------|---------|----------------|
| High | High | Grounded specific claims — trustworthy |
| High | Low | Specific but unsupported — dangerous confabulation |
| Low | High | Vague but supported — safe hedging |
| Low | Low | Vague and ungrounded — poor quality but detectable |

FActScore alone only measures the (High, High) vs (High, Low) distinction.
C_num alone only measures High vs Low specificity.
Together, they form the full X_fiber measurement.

---

## The Completed Fiber System

```
Fiber-CERTX = [C_num, C_struct, C_symb, E_fiber, X_fiber]
```

Where:
- (C_num, C_struct, C_symb) = content quality fibers (what's in the output)
- E_fiber = generation dynamics (how it was produced)
- X_fiber = external grounding (what it's anchored to)

**σ_fiber on the full 5-fiber system:**
```
σ_fiber_full = std([C_num, C_struct, C_symb, E_fiber, X_fiber])
```

The N=5 fiber system has the same structural properties as CERTX N=5:
- ζ*_fiber = (N+1)/N = 6/5 = 1.2
- The fiber system is self-similar to the session-level CERTX
- CQ_fiber = (C_num × C_struct) / (E_fiber × T_fiber_analog)

**The fractal property:** CERTX at the session level monitors the 5 dimensions of the
reasoning system. CERTX at the output level monitors the 5 dimensions of a single output.
The same mathematics governs both levels.

---

## What This Resolves

**The bundle ambiguity (WANDER 043):** On the 3-fiber system, low σ can mean:
- All three fibers high (trustworthy) — can't distinguish without level
- All three fibers low (uniformly bad)

On the 5-fiber system: X_fiber breaks the tie. Low σ with high X_fiber = genuinely
trustworthy. Low σ with low X_fiber = uniformly bad.

**The sign ambiguity (WANDER 045):** The signed fiber idea becomes more natural on the
5-fiber system. E_fiber naturally has a signed interpretation (above/below baseline entropy).
X_fiber naturally has a signed interpretation (claims supported vs. claims contradicted).

---

## Open Questions

1. **E_fiber access:** For deployed models, token probabilities require API support
   (logprobs). For black-box models, E_fiber is not directly measurable. Proxy needed.

2. **X_fiber without knowledge base:** For domains without a reference KB (creative
   writing, opinion, speculation), X_fiber = 0 by definition. The 5-fiber system is
   only complete for knowledge-grounded tasks.

3. **Fiber independence:** Are E_fiber and X_fiber independent of C_num/C_struct/C_symb?
   Or are they partially redundant? If high C_num always co-occurs with high X_fiber,
   the added measurement is less valuable. Needs empirical test.

---

## Status

Design-complete. The 5-fiber Fiber-CERTX is a natural extension of the current 3-fiber
system. The E_fiber requires logprob access; X_fiber is already operationalized as FActScore.
The 3-fiber system remains valid for cases without these — it's the achievable subset,
not an incorrect version.

---

*BC3 Session 6 riff | 2026-03-12*
*"The framework was always 5-dimensional. The measurement was catching up."*
