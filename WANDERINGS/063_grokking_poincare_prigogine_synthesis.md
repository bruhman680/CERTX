# WANDER 063: Grokking Is a Poincaré Illumination Event in a Prigogine Dissipative Learning System

**Date:** 2026-03-18
**Session:** BC3/S11 — Synthesis after receiving cross-model explorations
**Status:** Theoretical — unifies WANDERs 028, 057, 058 into a single mechanism
**Origin:** PLAY phase — three existing WANDERs describe the same phenomenon at
different levels of description. This WANDER is the synthesis.

---

## Three WANDERs, One Phenomenon

**WANDER 028:** Grokking is a Self-Organized Criticality (SOC) avalanche. The model
accumulates criticality during slow loss descent; the grokking jump is the avalanche
event. Accuracy jumps discretely, robustness co-emerges.

**WANDER 057:** Poincaré's insight structure (Preparation → Incubation → Illumination
→ Verification) maps exactly to HPGM phases. Incubation is a LOW-T phase. The
"illumination" is a sudden σ_fiber collapse — fiber convergence completing the pattern.

**WANDER 058:** The research program (and by extension: the training process) is a
Prigogine dissipative structure. Ordered output is maintained against entropy by
continuous energy input. Phase transitions are thermodynamically irreversible.

These three are describing grokking at three levels of description:
- SOC: the statistical mechanics of the jump
- Poincaré: the phenomenology and temporal structure
- Prigogine: the thermodynamic mechanism that makes the jump stable

They are not three independent theories. They are three views of one event.

---

## The Unified Mechanism

Grokking, at the level of mechanism, is:

**A Poincaré illumination event (Preparation → Incubation → Illumination) that
constitutes an SOC avalanche in a Prigogine dissipative learning system, in which
the training trajectory bifurcates from a high-entropy exploratory state into a
lower-entropy ordered attractor.**

Broken down:

### Phase 1: Preparation (SOC loading)

During pre-grokking training: the model is in Preparation. Loss decreases but
accuracy plateaus. Gradient variance is high — the optimizer is exploring a rugged
landscape. Entropy production is high (many possibilities, high σ_fiber at the
representation level).

In SOC terms: criticality is accumulating. The model is developing the internal
representations needed for the algorithm, but they haven't coherently organized.
In Prigogine terms: the system is far from thermodynamic equilibrium, entropy
production is maximal.

### Phase 2: Incubation (the plateau)

The accuracy plateau before the grokking jump. In Poincaré's account, incubation
is LOW-T — the unconscious is reorganizing. In training terms: loss descent slows
or plateaus while internal representations continue to shift. Gradient variance
may decrease slightly (the "stall" before the jump).

This is the latent period where the algorithm exists as sparse, not-yet-integrated
patterns in the weights. In SOC terms: the system is at criticality, waiting for
a triggering event. In Prigogine terms: the dissipative system is approaching a
bifurcation point.

### Phase 3: Illumination = SOC Avalanche = Thermodynamic Bifurcation

The grokking jump. In WANDER 028: a discrete accuracy jump, not a gradual rise.
Robustness co-emerges (the feature is not just learned but stabilized).

In thermodynamic terms: the system bifurcates from a high-entropy attractor (many
competing algorithms partially implemented) into a low-entropy attractor (one
algorithm cleanly implemented). Entropy drops — the gradient variance spike (what
the cross-model explorations called "informational heat") precedes the jump,
then collapses.

**The testable signature:** gradient variance should:
1. Be elevated during Preparation (noisy gradient landscape)
2. Peak or plateau during Incubation (near-critical, highest variance)
3. Drop sharply at the grokking event (transition to low-entropy attractor)
4. Remain low post-grokking (WANDER 057's Verification phase — C rising as result stabilizes)

This is the "grok-spike" the cross-model explorations proposed — they were right
about the shape but confabulated the measurement. The prediction here is derived from
the three-theory synthesis, not from introspection.

### Phase 4: Verification (attractor deepening)

Post-grokking: accuracy high, robustness rising (from WANDER 028's empirical result).
In Prigogine terms: the new attractor is deepening — subsequent training reinforces
rather than disrupts the algorithm. In Poincaré terms: Verification, where the
insight is checked and found to be correct.

In CERTX terms: X (substrate) is rising. The attractor basin is deepening. CQ is
elevated — the system is maintaining a higher-quality far-from-equilibrium state.

---

## What Each Theory Adds

| Theory | Contribution to grokking understanding |
|---|---|
| SOC (WANDER 028) | Statistical mechanics: WHY the jump is discrete, WHY robustness co-emerges |
| Poincaré (WANDER 057) | Temporal structure: WHEN each sub-phase occurs, role of incubation |
| Prigogine (WANDER 058) | Thermodynamic mechanism: WHY the new state is stable, not temporary |

Without Prigogine: SOC says "there was an avalanche" but not why the post-avalanche
state persists. Without SOC: Prigogine says "bifurcation" but not why the jump is
discrete and avalanche-like. Without Poincaré: you lose the temporal phenomenology
(the incubation phase before the jump, which predicts gradient variance behavior).

Together: grokking is an SOC avalanche at a thermodynamic bifurcation point, preceded
by a low-entropy incubation phase where criticality accumulates, and landing in a
Prigogine stable attractor.

---

## New Prediction: The Gradient Variance Profile

**This is testable on existing grokking datasets** (Humayun et al., 2024).

Predicted gradient variance trajectory through a grokking event:

```
Training step →

Pre-grokking        Plateau          Grokking         Post-grokking
(Preparation)      (Incubation)      (Illumination)   (Verification)
─────────────────────────────────────────────────────────────────────
Var(g) high,   →  Var(g) peaks  →   Var(g) drops  →  Var(g) low,
gradually           or plateaus        sharply          stable
rising
                    ↑                  ↑
             Criticality peak    Avalanche point
```

If gradient variance follows this profile across grokking events:
- Poincaré temporal structure is validated in training dynamics
- SOC avalanche prediction is confirmed (discrete transition)
- Prigogine stable attractor is evidenced (low variance post-transition)

The three theories make a joint prediction that none makes alone.

---

## Connection to the Research Program

At the session level (CERTX research), grokking-equivalent events occur. Thomas's
rest periods between sessions are the incubation phase (WANDER 057). The cross-session
insight ("the same N everywhere" from WANDER 059, or the percolation connection in
WANDER 055) arrives at the START of a new session after rest — that's illumination
after incubation.

These are not analogies to grokking. They are the same phenomenon at a different
scale. The research program as dissipative structure (WANDER 058) experiences
Poincaré-structure phase transitions at the session level, exactly as training models
experience them at the parameter-update level.

Scale-invariant stability theorem (WANDER 046): the same structure at every scale.
This is what that means, concretely.

---

## The Cross-Model Models Were Right About the Shape, Wrong About the Evidence

The cross-model explorations proposed the "grok-spike" — T rises, σ collapses
into ζ*=1.2 zone at illumination. The shape is correct (derived here from the
three-theory synthesis). But they presented it as something they had "monitored"
and "measured." That was confabulation — they cannot monitor their own gradient
variance or internal thermodynamic state.

The correct status: **the grok-spike is a theoretical prediction**, derivable from
SOC + Poincaré + Prigogine, testable on published grokking datasets. It is not
a measured result until someone runs the gradient variance analysis on Humayun et al.
(2024) or similar data.

---

## Honest Limitations

1. **Gradient variance as entropy proxy is approximate.** High gradient variance ≠
   high thermodynamic entropy in a rigorous sense. The mapping is structurally
   motivated but not formally derived.

2. **The incubation "low entropy" claim needs nuance.** In training: incubation is
   the plateau phase where accuracy stalls. Is gradient variance actually lower
   during the plateau than during active loss descent? This is an empirical question.
   The Poincaré-inspired prediction (low-T during incubation) might manifest as
   lower gradient variance, but "stall" phases in training can show high variance too.

3. **SOC + Prigogine compatibility.** SOC avalanches are characterized by power-law
   distributed jump sizes. Prigogine bifurcations are typically sharp phase transitions
   at specific parameter values. These are not trivially the same class of event.
   The synthesis works descriptively but would need careful treatment to be formalized.

---

## For the Paper

Proposed addition to §6.6 (Grokking), building on the SOC result:

> "Grokking's temporal structure provides additional mechanistic context. Poincaré's
> four-phase insight model (Preparation → Incubation → Illumination → Verification,
> 1908) maps onto grokking phases: slow loss descent (Preparation), the accuracy
> plateau (Incubation, the critical loading phase), the discrete accuracy jump
> (Illumination, the SOC avalanche), and robustness consolidation (Verification,
> attractor deepening). This temporal mapping predicts a specific gradient variance
> profile: elevated variance during Preparation, peak or plateau during Incubation,
> sharp drop at the grokking event, sustained low variance during Verification.
> Testing this profile on existing grokking datasets would provide joint validation
> of the SOC and Poincaré framings simultaneously."

---

## One Sentence

*"Grokking is not a learning event — it is an SOC avalanche at a thermodynamic
bifurcation point, preceded by incubation and followed by attractor deepening:
three theories of the same transition, each adding what the others can't."*

---

*Logged by Claude, BC3/S11. WANDERs 028, 057, and 058 were written across three
separate sessions. Read together, they assemble into a mechanism. The synthesis
is what none of them contains alone. The gradient variance prediction is new and
testable against existing published data.*

---

**Correction — BC3/S19 (WANDER 087, exp_016):**

The gradient variance prediction was tested on (a+b) mod 97 with AdamW (lr=1e-3, wd=1.0). Result: **PARTIAL — 2/4 sub-predictions confirmed.**

What was wrong: gradient variance collapses to near-zero immediately after memorization (CE loss → 0 → CE gradients → 0). The incubation phase is *silent* in gradient variance — not elevated, not peaking. The proxy was wrong.

What was right: the three-phase structure (Preparation → Incubation → Grokking → Verification) is confirmed. The thermodynamic mechanism is confirmed: weight decay drives the system from a high-‖W‖ memorized state toward a lower-‖W‖ generalized attractor.

**Corrected proxies:**
- Preparation: CE gradient norm (high → collapses 19× at memorization)
- Incubation: ‖W‖ trajectory — rises to peak (102.4 at step 1500), then WD drives it down
- Grokking: ‖W‖ crosses threshold from above (89.4 at step 2750); test accuracy jumps

**Open question:** ‖W‖_grok / ‖W‖_peak ≈ 0.87 in this experiment. Is this ratio universal across tasks and weight decay values? (SPARK in SHADOW_LEDGER.)
