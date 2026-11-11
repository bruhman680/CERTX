# Preregistered update-gating experiment (freeze before results)

Question: Does suppressing *policy updates* specifically during a predeclared mild-scarcity interval improve subsequent energy and learned-weight competence, rather than merely benefiting from fewer updates?

Fixed policy: `CreditGarden` `reserve_resource` objective, `.3` reserve/resource penalty, raw realized energy reward, eligibility `.97`, baseline smoothing `.995`, learning rate `.04`; stable theta pretraining 1000 ticks. Every test arm uses stochastic action mode with identical pretrained weights, initial physical state and action RNG. World size 10 (100 cells), same spatial world laws and regrowth `.06` ticks1-1000, `.055` ticks1001-2000, `.06` ticks2001-3000. Each cell retains its own weights; no teacher action targets. No mechanism will be retuned on results.

Interventions (all with 3000 test ticks):

* `online_all`: update weights on every tick.
* `gate_scarcity`: suspend policy-weight updates **only** t1001–2000, resume afterwards.
* `gate_sham`: suspend updates t1–1000 only (same duration, different phase); resume throughout scarcity/recovery. This matched update budget is an imperfect time-placebo, as update opportunities and world histories are intrinsically different.
* `gate_recovery`: suspend updates t2001–3000, further timing negative control.
* `frozen_all`: suspend updates throughout; reports no-learning boundary.
* `manual_reverse`: explicit non-neural rule (harvest iff R>.51, except under energy .12 require R>.535).

When disabled, policy theta remains frozen while the same state transition and action-sampling proceed; eligibility trace and reward baseline **continue to update** on every step so the arm tests withholding theta steps rather than removing the signal observation (the trace may store skipped-period information). This design isolates timing imperfectly because trajectories naturally diverge after first update difference.

Primary: final mean energy (no exclusive scalar optimization); co-primary depleted-cell fraction E<=.01 and final500-tick **unclipped** raw energy drift; secondary resource and harvest. Evaluate final theta from every neural arm deterministically on the same fresh stable/mild 1500-tick worlds. Report paired seed contrasts and 1000/2000/3000 checkpoints.

Fresh primary seeds **10100–10111**. Fresh reserved audit seeds **10200–10211** untouched by primary study. Smoke seeds **11100–11101** never included in main estimate. Independent audit may execute frozen source on reserved seeds. Hypothesis is testable and can fail: scarcity-specific gate should beat the sham energy **and** not worsen floor occupancy; if not, we reject claims of targeted improvement. A gating gain must not be claimed as autonomous learned breathing: schedule is explicitly imposed by designer with privileged knowledge of shift timing.
