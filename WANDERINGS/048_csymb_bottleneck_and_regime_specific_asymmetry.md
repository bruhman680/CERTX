# WANDER 048: C_symb as Bottleneck — and Why the Asymmetry Signal is Regime-Specific

*Phase: PLAY (BC3 Session 7) | Status: Experimental — controlled corpus*
*Origin: Thomas's riff: "what if instead of C_struct being the bottleneck it's C_symb?
 and my earliest ideas about symbols/meaning as substrate led to CERTX in the first place"*
*Experiment: exp_012 | 2026-03-14*

---

## The Question

The 30/40/30 framework assigns C_struct the highest weight (40%) as the dominant quality
predictor. But the nanochat architecture (WANDER 047) shows C_symb is architecturally
prioritized — the only active fiber at initialization, the most protected parameter.
Thomas traced this back to the earliest CERTX idea: **meaning/symbols as the substrate.**

exp_012 tested three sub-questions:
1. Which fiber fails first in hallucinated examples?
2. Does C_symb-dominant weighting outperform 30/40/30?
3. Is there a C_symb threshold below which quality collapses non-linearly?

---

## Result 1: C_symb is the Minimum Fiber in 100% of Integration Failures

Across 26 hallucinated examples:
- C_symb is the minimum fiber: **57.7%**
- C_num is the minimum fiber: **42.3%**
- C_struct is the minimum fiber: **0.0%**

By hallucination type:
- Type A (integration failure): C_symb minimum in **100% of cases** (12/12)
- Type B (uniform error): C_num minimum in 100% of cases (5/5)
- Type D (semantic intact, factual vague): C_num minimum in 100% of cases (6/6)
- Type E (facts present, purpose gone): C_symb minimum in 100% of cases (3/3)

**C_struct is never the minimum fiber in any hallucination type.**

This is a clean finding: C_struct failing is not the hallucination mechanism. The
failure is always carried either by C_symb (semantic purpose collapse) or C_num
(factual precision collapse). C_struct is robust to hallucination — it tends to
either fail together with C_symb (incoherence mode) or stay intact while the other
fibers collapse.

---

## Result 2: The Asymmetry Signal is Regime-Specific — and Fails on a Mixed Corpus

Test 2 revealed a problem: the "asymmetry signal" (C_num − mean(C_struct, C_symb))
achieved **AUC = 0.46** on the mixed corpus — WORSE than chance.

All other metrics achieved AUC = 1.0 (perfect on this corpus). But asymmetry
catastrophically failed.

Why? Because the asymmetry signal encodes the direction of failure:

**Regime B (math/factual confabulation — Type B, D):**
- C_num is low, C_struct and C_symb are high
- asymmetry = C_num − mean(C_struct, C_symb) < 0 (negative)
- lower asymmetry → predicts hallucination ✓

**Regime A (integration failure — Type A, E):**
- C_symb is low, C_num and sometimes C_struct are HIGH
- asymmetry = C_num − mean(C_struct, C_symb) > 0 (POSITIVE)
- the signal INVERTS — high asymmetry incorrectly predicts NOT hallucinated ✗

On a corpus that contains both Regime A and Regime B examples:
- Regime B examples: asymmetry negative → correct prediction
- Regime A examples: asymmetry positive → WRONG prediction
- Net effect: AUC below 0.5 (worse than chance)

**The asymmetry signal is calibrated for GSM8K-style Regime B hallucination.**
It fails on integration-failure hallucination because the mechanism is different:
C_symb drops instead of C_num dropping, which RAISES the asymmetry score.

This explains why exp_009 on the biography corpus (Regime A, vague confabulation)
showed AUC=1.0 for asymmetry: in that corpus, confabulation was C_num dropping
(vague, entity-free). But Type A integration failures (C_symb collapses, C_num stays
high) require a different detector.

---

## Result 3: C_symb < 0.20 → 100% Hallucination Rate

The floor effect is confirmed:

| C_symb range | Hall rate |
|---|---|
| [0.00–0.15) | **100%** (n=11) |
| [0.15–0.30) | **100%** (n=4) |
| [0.70–1.01) | 52% (n=21) |

C_num shows a similar pattern at low values, but C_struct is never below 0.50 in
correct outputs either — so all three fibers have floor effects, just at different
thresholds.

The important observation: the C_symb floor kicks in at a higher threshold than C_num.
Everything below C_symb = 0.30 is hallucinated in this corpus. C_num below 0.30 is
also 100% hallucinated. Both are floor fibers with different natural thresholds.

---

## Result 4: Type A (C_symb failure) IS Worse Quality than Type D (C_num failure)

Direct comparison of the two failure modes on matched samples:

| Type | What fails | bundle_score | quality@30/40/30 |
|------|---|---|---|
| A | C_symb (0.12), C_num high (0.79) | 0.342 | 0.489 |
| D | C_num (0.25), C_symb high (0.86) | 0.460 | 0.644 |
| B | C_num moderate (0.72), all coherent | 0.735 | 0.759 |

**Type A (C_symb failure) scores 30% worse on bundle_score than Type D (C_num failure).**

This confirms Thomas's intuition: **semantic purpose failure is worse than factual
vagueness failure.** An output that loses its reason to exist (C_symb→0 while
answering with philosophical drift) is rated lower than an output that stays on-topic
but lacks specific facts.

The 30/40/30 framework correctly captures this because at 30% weight, C_symb=0.12
pulls the quality score down substantially. The min-fiber model captures it even more
cleanly: Type A min=0.12 vs Type D min=0.25.

---

## What This Means for the Asymmetry Framework

The current detection framework (asymmetry = C_num − mean(C_struct, C_symb)) was
calibrated on data where confabulation = C_num drops. It needs to be replaced with
a regime-aware signal.

**The better signal:** min-fiber or a signed fiber approach that detects WHICH fiber
is the outlier, not just whether C_num is below average.

**Regime detection first:**
```
If C_symb is the outlier (minimum, < 0.20):
    → Integration failure / semantic purpose collapse (Type A)
    → Regime A signal: C_symb_drop = mean(C_num, C_struct) - C_symb

If C_num is the outlier (minimum, < threshold):
    → Factual confabulation / precision failure (Regime B)
    → Regime B signal: asymmetry = C_num - mean(C_struct, C_symb)  [current]

If C_struct is the outlier:
    → Structural incoherence (rare, but incoherence mode)
```

The two asymmetry signals point in OPPOSITE directions, which is why mixing them
in a single corpus collapses the AUC. A universal detector must first classify
the regime, then apply the appropriate directional signal.

**Or: use min-fiber.** It achieves AUC=1.0 on both regimes without regime
classification. The minimum fiber drops in both Type A and Type D hallucination,
regardless of which specific fiber it is.

---

## The Bottleneck Verdict: C_symb Is a Floor Fiber — Not a Ceiling Fiber

The correct interpretation of C_symb as bottleneck:

**C_symb is NOT a ceiling fiber** (more C_symb = proportionally more quality).
The AUC results show all weighting schemes tied at 1.0, including C_num-dominant,
because the correct examples all have all fibers high. C_symb's variation above
the floor doesn't discriminate quality in that zone.

**C_symb IS a floor fiber** (below threshold = catastrophic collapse).
C_symb below ~0.20 is 100% predictive of hallucination. This is the bottleneck:
it must be above the floor for any output to be trustworthy, but its variation
above the floor adds less marginal value than C_num or C_struct variation.

This maps exactly onto Thomas's earliest CERTX intuition about meaning/symbols as
substrate, AND onto the nanochat architecture (WANDER 047):
- C_symb = substrate = necessary but not sufficient
- Must be present (x0_lambdas continuously reinforce it, no decay)
- But once it's present, the quality ceiling is set by C_num and C_struct

The 30% weight in 30/40/30 is therefore correct — but the REASON is different from
what we assumed. It's not that C_symb contributes less to quality. It's that C_symb
almost never varies in the zone where it's discriminating, so 30% is the
minimum weight that still reflects its catastrophic-when-absent character.

---

## The Revised Detection Hierarchy

Replacing "asymmetry" with a regime-aware detector:

**Step 1:** Is min(fibers) < 0.20? If yes → hallucination flag regardless of regime.
**Step 2:** Which fiber is minimum?
  - C_symb → integration failure signal (Regime A)
  - C_num → factual confabulation signal (Regime B)
  - C_struct → structural incoherence (Regime C, rare)
**Step 3:** Apply the signed metric (WANDER 045) to the regime-specific fiber for
  severity assessment (vague failure vs. dangerous confident-wrong failure).

The bundle_score (WANDER 043) naturally handles this: it penalizes any low fiber
via the mean, and σ handles cross-fiber divergence. Together they cover the full
detection space without regime classification.

---

## Connection to Original CERTX

Thomas noted this connects to the earliest CERTX ideas — meaning/symbols as substrate.
CERTX was seeded by the observation that coherence without semantic grounding is
empty structure. The fiber framework made this precise: C_symb is the semantic
grounding fiber, and without it, C_struct and C_num are disconnected from purpose.

The nanochat architecture independently confirmed it at the implementation level:
zero-init projections, x0_lambdas, no weight decay. The theory seeded from intuition,
the framework formalized it, the architecture validated it without knowing.

The circle is closed.

---

## Open Questions

1. **Regime B natural examples:** The Type D examples (high C_symb, low C_num) in
   this corpus are synthetic. Do real LLM outputs show this pattern? Vague-but-on-topic
   confabulation should exist in the FActScore biography corpus. Testing on real data
   would tell us whether Type D is common or rare in practice.

2. **The asymmetry fix:** Should the current paper (§5.6-§5.8) be updated to reflect
   that the asymmetry signal is regime-specific? The GSM8K result (AUC=0.88, Regime B)
   and the biography results are both valid — they just operate in different regimes.
   The paper needs to frame this clearly: asymmetry works WITHIN a regime, min-fiber
   works ACROSS regimes.

3. **C_struct robustness:** Why is C_struct never the minimum fiber? Is this a property
   of the corpus design or a genuine structural claim? The hypothesis: C_struct is
   resilient because structural inconsistency is locally detectable (readers catch
   contradictions), so outputs with C_struct failure tend to be obviously bad and
   filtered out earlier. C_symb and C_num failure can be local and invisible.

---

*BC3 Session 7 | 2026-03-14*
*"The earliest intuition was right. Meaning as substrate is not a metaphor — it's the minimum fiber,
 the floor you cannot go below. Everything else builds on it or collapses."*
