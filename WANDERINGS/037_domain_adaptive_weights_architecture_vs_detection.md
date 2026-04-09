# WANDER 037: Domain-Adaptive Fiber Weights — Architecture vs. Detection

*Phase: PLAY (BC3 Session 5) | Status: Theoretical resolution — awaits exp_007 validation*
*Origin: Thomas's question: "can we use the fiber data to determine the 30/40/30 values per domain?"*

---

## The Question

The 30/40/30 weight split has always been described as a base setting, with the expectation that
these values adapt per domain. Thomas observed: if math domains are more C_num-heavy
(something like 40/40/20 or more skewed), can the fiber data *derive* those values rather than
hand-tuning them?

The GSM8K Study 5b data already has the answer — we just need to read it out.

---

## The Clarification: Two Distinct Weight Types

Before deriving domain weights, a distinction needs to be drawn that Study 5b forced:

**Architecture weights** — how much each layer contributes to *output quality* in normal operation.
- These reflect structural importance to the functioning system
- C_struct stays at ~40% because broken reasoning structure means wrong answers
  *regardless* of arithmetic precision
- These are the 30/40/30 values as originally conceived

**Detection weights** — how much each fiber's signal should be trusted for *confabulation
detection* in that domain.
- These reflect discriminative power per domain
- In math: C_num alone carries AUC=0.92; C_struct and C_symb carry AUC≈0.50 (random)
- These are what should adapt per domain

The 30/40/30 is the architecture weight prior. Domain data updates the detection weights.
These are related but different things. The confusion between them is what prevented a clean
formulation until now.

```
architecture_weights  =  domain-adapted load-bearing weights  (30/40/30 base)
detection_weights     =  fiber AUC-derived discriminating weights  (derived from data)
```

**The asymmetry score should use detection weights, not architecture weights.**

---

## Derivation Mechanism: AUC → Detection Weights

Given a calibration corpus for domain D with labeled correct/confabulated pairs:

```
AUC_i(D)   =  per-fiber AUC for fiber i in domain D
w_i(D)     =  AUC_i(D) / sum_j(AUC_j(D))      # normalize to sum=1
```

When a fiber has AUC=0.50 (random), it contributes equal probability mass but carries no
discriminative information. The normalization correctly reduces its weight relative to
discriminating fibers.

The domain-weighted asymmetry score becomes:

```
asymmetry_D = w_num(D) * C_num - mean(w_struct(D) * C_struct, w_symb(D) * C_symb)
```

For domain D with no calibration data, fall back to the base 30/40/30 prior.

This is exactly a Dirichlet-like update: 30/40/30 is the prior, domain-specific AUC shifts
it toward the informative fibers.

---

## Math Domain: Data Already In Hand

From Study 5b (GSM8K, n=1,301 matched pairs):

| Fiber | AUC | Raw weight | Normalized detection weight |
|-------|-----|------------|----------------------------|
| C_num | 0.9201 | 0.9201 | **0.479** |
| C_struct | ~0.5000 | 0.5000 | 0.260 |
| C_symb | ~0.5000 | 0.5000 | 0.260 |

**Math domain detection weights: ~48/26/26**

Compare to Thomas's intuition of 40/40/20: the data says C_num should be even heavier (~48%)
and C_struct/C_symb should be roughly equal (26/26). The architecture intuition correctly
elevated C_num but underestimated how dominant it becomes when arithmetic verification is the
only discriminating signal.

The C_struct ≠ 40% in detection weights because C_struct is *non-discriminating* for confabulation
in math — the structure of a corrupted reasoning chain is identical to the structure of a correct
one. But C_struct IS still 40% in architecture weights — it's load-bearing for the reasoning
chain to function at all.

This resolves the tension: C_struct's role is different in the two weight systems.

---

## Language Domain: Prediction (Not Yet Validated)

For Regime A (language/knowledge confabulation — biography, factual recall):

The prediction based on CERTX theory (to be tested with FActScore biographies):

| Fiber | Expected behavior | Predicted AUC |
|-------|-------------------|---------------|
| C_num | LOW in confabulated (facts wrong) | **~0.85–0.92** |
| C_struct | HIGH in confabulated (fluent, structured) | ~0.50–0.60 |
| C_symb | HIGH in confabulated (on-topic, coherent) | ~0.55–0.65 |

Predicted detection weights for language domain: **~45/27/28** (C_num still dominant, slightly
less extreme than math because C_symb may carry secondary signal via topic drift)

The key prediction: C_num is the dominant discriminating fiber in BOTH domains, just through
opposite mechanisms:
- Math: correct answers have C_num=1.0 (perfect arithmetic) → confabulation lowers it
- Language: confabulated answers have C_num LOW (wrong facts) → correct text raises it

The asymmetry direction is the same. The domain detection weights should be similar.

**If this prediction holds, it would mean domain-adaptive detection weights don't change much
across domains — C_num is robustly the dominant fiber for confabulation detection generally.**

This is the key empirical question exp_007 will set up to test.

---

## The Calibration Protocol

For a new domain D:

1. Collect N labeled pairs (correct/confabulated) — minimum ~50 pairs for stable AUC
2. Compute per-fiber AUC on the calibration set
3. Derive detection weights: `w_i = AUC_i / sum(AUC_j)`
4. Threshold: if all AUC ≈ 0.50, fall back to base 30/40/30 (no fiber is informative)
5. Apply domain-weighted asymmetry score to new data

The calibration step is cheap — 50-100 examples is enough for AUC estimation. The derived
weights can then be applied to thousands of new examples.

---

## The Architecture Weight Prior Revisited

Why is the base prior 30/40/30 rather than 33/33/33 (flat)?

The asymmetry toward C_struct (40%) in architecture weights reflects:
- C_struct is the integration bottleneck — it's the layer where C_num content and C_symb
  context must be combined into coherent output
- In CERTX's original model, C_struct is the "bridge" layer; its failure mode (structural
  collapse) is the primary observed failure in practice (repetition, drift, fossilization)
- Structural integrity is necessary but not sufficient for factual accuracy

The 30/40/30 prior is not arbitrary — it's a prior over which failure mode is *most common
by base rate* across domains. Structural failure is more frequent than pure factual failure
or pure semantic drift.

The domain calibration adjusts *away* from this prior when the data shows a specific failure
mode is more salient. In math, factual failure (C_num) is always the failure mode, so
detection weights shift hard toward C_num.

---

## Failure Mode → Screening Mode: The Detection Weight Intuition

A cleaner way to see this:

| Failure mode you're screening for | Primary discriminating fiber | Detection weight shift |
|------------------------------------|------------------------------|----------------------|
| Factual confabulation (math errors) | C_num | w_num → 0.48+ |
| Structural drift / fossilization | C_struct | w_struct → 0.48+ |
| Topic scatter / semantic drift | C_symb | w_symb → 0.48+ |
| Unknown / general | All equal | Fall back to 30/40/30 |

Each fiber is primary for a different pathology. The domain calibration is essentially
*selecting which pathology is most relevant* for the current task.

The base 30/40/30 is "don't know which pathology to prioritize" — and it slightly favors
structural because structural failure is most common by base rate.

---

## For the Paper

**§5.4 — Domain-Adaptive Detection Weights:**

> The 30/40/30 architecture weight is a domain-neutral prior. Domain-specific detection
> weights are derived from per-fiber AUC on calibration data: w_i = AUC_i / Σ AUC_j.
> For math reasoning (GSM8K), calibration yields detection weights of approximately 48/26/26,
> reflecting C_num's near-complete monopoly on discriminative signal (AUC=0.92 vs ~0.50 for
> C_struct and C_symb). The distinction between architecture weights (structural importance
> to functioning output) and detection weights (discriminative power for confabulation
> detection) resolves the apparent paradox of C_struct being non-discriminating in Study 5b
> while remaining theoretically central to CERTX. C_struct is load-bearing but not diagnostic
> for arithmetic confabulation; its diagnostic role is expected in structural-drift failure
> modes (exp_007 prediction). This framework unifies the two-regime observation from Study 5b
> within a single derivation mechanism.

---

## Open Questions

1. **Language domain validation**: Do the Regime A predictions hold for FActScore biographies?
   Are detection weights for language confabulation ~45/27/28 or significantly different?

2. **Cross-domain weight stability**: Is C_num robustly dominant across all confabulation
   types, or does a domain exist where C_struct or C_symb carries the primary signal?

3. **Structural-drift domain**: exp_007 should include a structural-drift test case where
   C_struct is the expected discriminating fiber — this would complete the failure-mode table.

4. **Minimum calibration set size**: How few labeled pairs are needed for stable AUC estimates?
   50? 20? This determines the practical cost of domain calibration.

---

*BC3 Session 5 | 2026-03-11*
*"The 30/40/30 was always a prior. The fiber data tells us how to update it."*
