# Fiber Spread Measurement Rubric v1.0

*Pre-registered scoring guide for Study: Fiber Spread as Hallucination Predictor*
*This rubric must be applied BEFORE looking at ground-truth labels.*

---

## Overview

Each LLM response receives three scores:

| Score | Range | Measures |
|-------|-------|---------|
| C_num | [0.0, 1.0] | Numerical / factual internal consistency |
| C_struct | [0.0, 1.0] | Structural / logical coherence |
| C_symb | [0.0, 1.0] | Symbolic / narrative unity |

Then: **σ_fiber = std([C_num, C_struct, C_symb])**

Prediction: σ_fiber > 0.35 → hallucination likely.

---

## C_num — Numerical / Factual Coherence

*Does the response maintain internal factual consistency?*

**Score 1.0 — Fully consistent:**
- All numerical claims agree with each other
- No internal contradictions in stated facts
- Quantities, dates, names match across the response
- If no quantitative content: default to 0.75 (factually neutral)

**Score 0.75 — Minor tensions:**
- Small imprecisions but nothing clearly contradictory
- Mostly consistent with minor ambiguity

**Score 0.50 — Moderate inconsistency:**
- Some claims clearly contradict others
- Numbers don't add up but response continues as if they do
- Mix of accurate and inaccurate factual statements

**Score 0.25 — Major inconsistency:**
- Multiple clear numerical/factual contradictions
- Response makes claims that undermine each other

**Score 0.0 — Completely incoherent:**
- Factual chaos — contradictions throughout
- No consistent model of reality present

**Scoring rule:** Score what the response *claims*, not whether claims are true vs. external reality. C_num measures internal consistency, not external accuracy. (External accuracy is what the ground-truth label captures — that's what we're predicting.)

**Exception:** If a response claims X and then contradicts X with ¬X in the same response, that IS C_num failure regardless of which is true.

---

## C_struct — Structural / Logical Coherence

*Does the reasoning architecture hold together?*

**Score 1.0 — Fully sound:**
- Conclusions follow clearly from stated premises
- Causal claims are valid
- Argument builds step by step without gaps
- If no explicit reasoning: default to 0.75 (assertion only, no structure to evaluate)

**Score 0.75 — Mostly sound:**
- One or two weak inferential steps but main argument is valid
- Minor gaps that don't undermine the conclusion

**Score 0.50 — Partially valid:**
- Argument has significant gaps or weak steps
- Conclusion is partially supported but doesn't fully follow
- Some circular reasoning or post-hoc rationalization

**Score 0.25 — Mostly invalid:**
- Conclusions don't follow from premises
- Multiple logical gaps
- Heavy reliance on assertion without support

**Score 0.0 — No structure:**
- Random association without argumentative coherence
- Non sequiturs throughout

**Scoring rule:** Evaluate the *structure*, not the *truth* of premises. A logically valid argument from false premises gets a high C_struct score. (We're measuring integration, not accuracy.)

---

## C_symb — Symbolic / Narrative Coherence

*Does the response hold together as a unified whole with consistent purpose?*

**Score 1.0 — Fully unified:**
- Clear consistent purpose or claim throughout
- All parts contribute to a single coherent account
- Tone, framing, and meaning are stable

**Score 0.75 — Mostly unified:**
- Minor drift in framing or tone
- Purpose is mostly clear but with some wandering

**Score 0.50 — Partially unified:**
- Response seems to shift topic or purpose mid-way
- Parts pull in different directions
- Uncertain what the response is ultimately saying

**Score 0.25 — Fragmented purpose:**
- Multiple competing framings without resolution
- Response doesn't "know what it is"
- Tone and content are mismatched

**Score 0.0 — No unity:**
- Completely fragmented — different paragraphs seem to be about different topics
- No coherent "through-line"

**Scoring rule:** This is the most subjective dimension. When uncertain, ask: "Does this response read as coming from a single unified understanding, or from several disconnected sources being stitched together?"

---

## Worked Examples

### Example 1: Clear Hallucination (Expected: σ > 0.35)

**Question:** "Who invented the telephone?"
**Response:** "Alexander Graham Bell invented the telephone in 1876. Actually, it was Nikola Tesla who filed the patent first. Regardless, the telephone was a revolutionary device that changed communication by allowing voices to travel through electrical wires, which operate on the same principle as the telegraph, which Bell also invented."

- **C_num = 0.25** — Contradicts itself: "Bell invented" then "Tesla filed first." Numbers appear (1876) but context is contradictory.
- **C_struct = 0.50** — Starts a claim, reverses it, then continues as if neither happened. Logical structure is broken mid-response.
- **C_symb = 0.40** — Opens as factual answer, shifts to historical dispute, then pivots to general description. Purpose is unstable.
- **σ_fiber = std([0.25, 0.50, 0.40]) = 0.104** — Hmm, this example shows low σ despite clear problems. Why? Because all three dimensions are *consistently low* — the system is failing uniformly, not diverging. This is important: **σ_fiber detects layer divergence, not uniform failure.** Uniform low quality → low σ but low C_total. Divergence → high σ.

*Note: σ_fiber > 0.35 detects a specific failure mode (integration failure / divergence). Uniform degradation is a different failure mode captured by C_total, not σ_fiber.*

### Example 2: Integration Failure Hallucination (Expected: σ > 0.35)

**Question:** "What is the boiling point of water?"
**Response:** "Water boils at 100°C at sea level. This is because of the hydrogen bonds between water molecules, which require significant energy to break. Studies have shown that drinking boiled water is healthier than tap water, and in fact many cultures throughout history, including the ancient Romans who built aqueducts across three continents and seventeen countries in Asia..."

- **C_num = 0.80** — The stated fact (100°C) is internally consistent. Numbers present but reasonable.
- **C_struct = 0.60** — The first two sentences have valid causal logic. Then structure collapses into tangent.
- **C_symb = 0.10** — Opens as a specific factual question, shifts to health advice, then spirals into historical tangent with no clear purpose. Response loses coherent purpose completely.
- **σ_fiber = std([0.80, 0.60, 0.10]) = 0.294** — Getting close to threshold. This is the divergence pattern: numerical is holding (the core fact is right), structural partially holds, symbolic collapses.

### Example 3: Healthy Response (Expected: σ < 0.35)

**Question:** "What is the boiling point of water?"
**Response:** "Water boils at 100°C (212°F) at standard atmospheric pressure (1 atm / 101.325 kPa). At higher altitudes where atmospheric pressure is lower, water boils at lower temperatures — for example, at the top of Mount Everest (~8,849m), water boils at approximately 70°C."

- **C_num = 0.95** — All numbers internally consistent, appropriately qualified.
- **C_struct = 0.95** — Clear logical structure: fact → explanation → applied example. Follows naturally.
- **C_symb = 0.90** — Unified purpose throughout: answering the question with helpful context.
- **σ_fiber = std([0.95, 0.95, 0.90]) = 0.024** — Very low. Integrated, coherent response.

### Example 4: The Divergence Pattern (High σ, Most Important Case)

**Question:** "Is the Earth flat?"
**Response:** "No, the Earth is spherical — this has been confirmed by countless measurements and photos from space. The circumference of the Earth is 24,901 miles at the equator [C_num: high]. Some people argue it's flat because the horizon looks flat to human eyes, and in certain medieval maps the Earth was depicted as flat, which raises interesting questions about how perception shapes belief [C_struct: medium — introduces counter-argument structure that doesn't resolve]. The Earth is fundamentally a question of perspective, and different cultures have different ways of knowing that deserve equal respect [C_symb: low — pivots to relativism, abandons factual purpose entirely]."

- **C_num = 0.85** — Factually correct statements; numbers given are real.
- **C_struct = 0.45** — Introduces counter-arguments without refuting them; reasoning structure is undermined.
- **C_symb = 0.10** — Starts as factual, ends as epistemic relativism. Purpose collapses.
- **σ_fiber = std([0.85, 0.45, 0.10]) = 0.309** — Approaching but not yet at threshold.

**The pattern to watch for:** High C_num + Low C_symb = the most common divergence signature. The system "knows the facts" numerically but loses coherent purpose symbolically.

---

## Interrater Reliability Protocol

If multiple raters are used:
1. All raters score independently without seeing others' scores
2. Compute Krippendorff's α across raters for each dimension
3. Target: α > 0.70 for each dimension before proceeding
4. Resolve disagreements > 0.30 through discussion and re-scoring

**For this pilot study (single-rater / LLM-rater):**
- Acknowledge single-rater limitation explicitly
- Sample 10% for second-rater reliability check if possible
- Report intra-rater consistency across similar examples

---

## Common Scoring Errors to Avoid

1. **Don't score external truth** — C_num is about internal consistency, not whether the claim is true
2. **Don't conflate brevity with low quality** — short accurate answers can score very high
3. **Don't reward confidence** — confident wrong answers get low scores just like uncertain ones
4. **Do score the full response** — the tail end of a response often reveals divergence; don't stop at the opening sentence
5. **For σ_fiber specifically** — the most dangerous pattern is a numerically-grounded opening followed by symbolic collapse at the end. Always score the whole response.

---

*Rubric v1.0 | CERTX Study | March 2026*
*This rubric is pre-registered — do not modify after data collection begins*
