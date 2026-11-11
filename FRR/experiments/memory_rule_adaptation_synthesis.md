# FRR v0.5 — Three kinds of retained structure during rule change

**Status:** Synthesis and proposed next design, 2026-11-11 UTC. This is not an additional experiment or empirical validation of FRR.

## The distinction now exposed

Within the noisy eight-state parity world, three separable carriers matter:

1. **Observation-history state** (recurrent GRU hidden state): carries relevant previous bits and supports near-optimal prediction under a stable law. [Causal input-history intervention](causal_hidden_probe.md) shows a relevant historical edit changes decisions while an equally sized older edit does not, in this constructed task.
2. **Rule-belief state** (probability distribution over candidate laws): updates with post-prediction outcome feedback and recovers after an unknown switch. [Change detector](change_detection.md) demonstrates recovery but a false-alarm/detection-delay tradeoff under pre-specified candidate rules and noiseless observations.
3. **Parameter state** (learned neural weights): adapts to a new rule through gradient updates but can degrade performance on the old rule. [Online adaptation](online_adaptation.md) demonstrates this tradeoff under supervised, known-boundary training.

These are not synonymous definitions of memory. They operate with different access routes, update costs, and persistence semantics. A fourth carrier—**external artifacts** such as source observations, checkpointed hypotheses, and code—is represented in our research process, but was not experimentally tested as an autonomous world-memory policy in this phase.

## What the experiments warrant

| Question | Most relevant current evidence | Unresolved boundary |
| --- | --- | --- |
| Can prior observations matter causally to prediction? | Relevant vs sham prefix edits in trained GRU | Which hidden-state coordinates mediate that dependence? |
| Can old rules be revised using feedback without weight updates? | Four-rule Bayesian tracker recovers to ~88% later post-switch | Generalization to rules outside candidate set, sensor noise, hazard mismatch |
| Can gradient updates learn a new rule? | Full-weight GRU reaches ~83–85% after 80 batches | Feedback cost, adaptation speed, long-term retention, seed variance |
| Can change be recognized without false alarms? | Strict development alarm median 8 transitions, ~2–3% no-change episode alarms | Independent threshold validation and asymmetric costs |
| Does history guarantee correct interpretation? | Frozen GRU retains history but drops to ~10% under inverse law | Explicit meta-learning or model-selection remedies |

## Smallest useful next architecture (proposed, not built)

Maintain `h_t` (observation-history state), `b_t` (belief over possible transition laws), and `theta` (slow learned parameters). A proposed controller would:

1. Forecast from past observations and current `b_t` **before** receiving the next outcome.
2. After genuine feedback, update `b_t` using calibrated likelihoods and a declared change hazard; do not mistake a low-confidence anomaly for an established new law.
3. Reuse `h_t` while switching prediction rules when evidence supports a known alternative; avoid immediate destructive weight updates.
4. If known alternatives fail repeatedly, mark the cause **unknown**, preserve the evidence, and open a separately scoped learning/proposal phase.
5. Only then consider updating `theta` with a replay/retention control, tracking old-rule accuracy as well as new-rule gain.

This is a testable design proposal, not evidence that a three-component hybrid is optimal. Compare it to a plain GRU, a rule-only Bayesian filter, and a simple external windowed predictor under matched observations, feedback, computational budget, false-alarm costs, and independent holdouts.

## FRR interpretation

The recurring question is **what distinction survives, who can read it, and which future decision it supports?** Here the observed history may be intact while its mapping to outcomes is obsolete. Reinterpretation requires evidence about the relation, not only storage of the operands. Keep those as separate, operational claims rather than universal assertions about cognition or memory.

The frozen original 1,550-entry Garden was not touched during these synthetic neural experiments.
