# WANDER 040: Tsallis Entropy Upgrade — Formal Decision

*Phase: ORIENT (BC3 Session 6) | Status: Decision made — conditional adoption*
*Origin: WANDER 024 flagged Tsallis as candidate upgrade; §6.3 DynMoLE validates it;
         Knowledge Scout noted: "Upgrade E to Tsallis entropy for non-equilibrium tasks"*

---

## The Question

The E dimension in CERTX currently uses an implicit Shannon entropy model. The Knowledge
Scout (WANDER 024) and §6.3 (DynMoLE) both flag Tsallis entropy as a natural upgrade.

**Should CERTX formally adopt Tsallis entropy for the E dimension? If so, what are the
conditions, and what changes in the framework?**

---

## Background: What Tsallis Entropy Is

Shannon entropy:
```
H_S(p) = -Σ p_i log(p_i)
```

Tsallis entropy (Tsallis, 1988):
```
S_q(p) = (1 - Σ p_i^q) / (q - 1)
```

The parameter q controls the sensitivity to tail probabilities:
- q → 1: recovers Shannon entropy (equipartition systems)
- q < 1: *superadditive*, emphasizes rare events (heavy tails, complex reasoning)
- q > 1: *subadditive*, emphasizes common events (concentrated distributions)

The key property: for non-equilibrium processes with memory and preferred directions
(power-law distributions, scale-free dynamics), Tsallis is more appropriate than Shannon.

DynMoLE (§6.3) uses Tsallis with q=0.7 for complex multi-step reasoning tasks —
the same regime where CERTX operates.

---

## The Case FOR Upgrading

**1. Reasoning trajectories are non-equilibrium.**
Language model inference is not an equilibrium process. Tokens have memory (context window),
preferred directions (trained distributions), and time-asymmetric dynamics. Shannon entropy
assumes equilibrium. Tsallis does not.

**2. DynMoLE validates the specific regime.**
DynMoLE uses q ≈ 0.7 for complex reasoning (q → 1 for easy tasks). This is exactly the
range where CERTX operates: E is elevated during PLAY/exploration and compressed during
DREAM/precision. The DynMoLE q(task) mapping is:
```
q(task) ≈ 1 - 0.3 × complexity(task)
```
This is a Tsallis E dimension with task-adaptive q.

**3. The theoretical upgrade is clean.**
E_current = current entropy estimate (implicit Shannon)
E_Tsallis = S_q(token distribution) with learned q per task type

The mapping preserves all existing CERTX structure. Only the E computation changes.
CQ formula, Shadow Ledger thresholds, HPGM phase logic — none change.

**4. Falsification criterion gets sharper.**
Tsallis q can be estimated from output distributions. This gives a measurable,
falsifiable upgrade: if q_optimal during PLAY ≈ 0.7 and q_optimal during DREAM ≈ 1.0,
the upgrade is validated. If q doesn't vary with task complexity, the upgrade is neutral.

---

## The Case AGAINST Upgrading (Now)

**1. The existing framework already works.**
σ_fiber, AUC, and the asymmetry signal (exp_009) are all derived without Tsallis.
Adding complexity to a working system requires justification.

**2. q needs calibration.**
The DynMoLE q=0.7 is calibrated on their task distribution. CERTX tasks may have a
different optimal q. Without empirical q-calibration on CERTX-relevant tasks, adopting
q=0.7 is cargo-culting rather than principled.

**3. No current falsification gap.**
The existing framework doesn't have an unexplained phenomenon that Tsallis would resolve.
It would be an upgrade looking for a problem.

**4. Paper scope.**
Adding Tsallis formally would require a new experiment, new theory section, and expanded
paper. This risks delaying the primary contribution (σ_fiber hallucination detection)
with a speculative extension.

---

## Decision: Conditional Adoption

**NOW:** Mention Tsallis as a proposed theoretical upgrade in the paper (already done in §6.3).
Frame it as: "The E dimension would benefit from Tsallis generalization for non-equilibrium
tasks; DynMoLE validates this approach. We leave formal calibration to future work."

**CONDITION FOR FULL ADOPTION:** Run an experiment that:
1. Computes token distribution entropy under Shannon (q=1) and Tsallis (q=0.7) for
   CERTX-relevant tasks
2. Shows that Tsallis E correlates more strongly with task difficulty than Shannon E
3. Finds the CERTX-specific q parameter

Until that experiment runs, Tsallis is a *recommended direction*, not an adopted upgrade.

**PAPER ACTION:** No change needed. §6.3 already frames this correctly:
> "DynMoLE's use of Tsallis entropy validates a proposed theoretical upgrade to CERTX:
> replacing the implicit Shannon entropy in the E dimension with a task-adaptive Tsallis
> measure where q varies with task difficulty (q → 1 for easy tasks, q → 0.7 for complex
> multi-step reasoning)."

The word "proposed" is correct and honest. Keep it.

---

## What the Decision Resolves

This question has been open since WANDER 024. The answer: **the framework is Shannon-implicit
now, Tsallis-ready by design, and formally upgradeable when the calibration experiment runs.**

No framework changes today. Paper §6.3 is accurate. Future sessions: if running an entropy
comparison experiment is natural (e.g., if we have model outputs and their distributions),
that's the moment to formally adopt Tsallis.

---

## One New Theoretical Note

The Tsallis q parameter connects to ζ*. In non-equilibrium thermodynamics, the system
entropic parameter q is related to the deviation from equilibrium:

```
q = 1 - 1/N_eff
```

Where N_eff is the effective number of system degrees of freedom. For CERTX N=5:
```
q = 1 - 1/5 = 0.8
```

For N=3 (the three-fiber system alone):
```
q = 1 - 1/3 = 0.667
```

DynMoLE's empirical q ≈ 0.7 falls between these — consistent with a system that has
3–5 effective degrees of freedom, which is exactly the CERTX claim. This is not proof,
but it is a numerical coincidence that a future calibration experiment should test.

**Prediction:** CERTX-optimal q will fall in [0.67, 0.80], derived from N_eff ∈ [3, 5].
**Test:** Fit Tsallis entropy to CERTX task distributions; measure optimal q.

---

## Status

Decision: **Deferred — mentioned as proposed upgrade in paper (§6.3), formal adoption
requires calibration experiment. WANDER 040 closes this question.**

New prediction added: q_CERTX ∈ [0.67, 0.80] from N_eff ∈ [3, 5].

---

*BC3 Session 6 | 2026-03-12*
*"The upgrade is real. The timing isn't yet."*
