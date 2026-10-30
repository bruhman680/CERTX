# Bounded scout: correspondence, copying and task application

Read date: 29 October 2026 (America/Chicago). Three primary papers contacted; selected sections only. No model execution, paid service, dataset installation, weight download or training. This extends the previous worked-application scout rather than repeating its published model-card checks.

## 1. Distribution-preserving corruption

[Yoo et al., Ground-Truth Labels Matter, v2](https://arxiv.org/html/2205.12685v2), EMNLP 2022. Inspected abstract, section 2.4.4 and Appendix A.1/A.5/A.6. Appendix A.6 distinguishes replacing labels with independent uniform draws from shuffling existing labels: the former can alter the demonstrated class distribution; the latter preserves it. Their task-difficulty analysis cautions that low label sensitivity may accompany weak task performance. Models include 1.5B–175B; this is not evidence about our 135M instruction checkpoint.

Local design implication: preserve the exact label inventory/counts when permuting correspondence. Report both task accuracy and paired response changes. Equal failure in correct/permuted arms cannot establish that only format matters. A changed response need not be an improved response. Existing semantic labels also carry prior meanings, so this diagnostic tests sensitivity to conflicting demonstrations, not arbitrary-label learning in isolation.

## 2. Copying versus construction

[From Copying to Composition: How Language Models Develop In-Context Learning, v1](https://arxiv.org/html/2610.19113v1), arXiv:2610.19113. Inspected abstract, section 3, model descriptions and Appendices A/L. The diagnostic assigns fresh suffix mappings, demonstrates three feature combinations, then requests the missing combination on a new stem. It distinguishes a nearest-demonstration copied ending from the rule-consistent composition. The study uses multiple families and includes continued-training experiments with SmolLM2-360M/1.7B; it does not test our 135M instruct checkpoint. Authors separately score candidate preference and free generation. Their training interventions concern learned changes, unlike our inference-only experiment.

Local design implication: maintain distinct fields for source/target copying, correspondence-sensitive output and warranted task application. A better-looking answer or less copying is insufficient for the last field. The suffix task is a possible later clean-room contact, not part of the present threshold/status experiment. No training or attention modification is recommended on this reading alone.

## 3. A peripheral readout warning

[The Readout Shortcut: Positional Number Copying Dominates Arithmetic CoT Readout in Small Language Models, v1](https://arxiv.org/html/2605.22870v1), arXiv:2605.22870. Inspected abstract, scope paragraph, models and task/protocol. The authors study 1–3B instruction models using teacher-forced arithmetic prefixes; changing a trailing answer-context number can control final readout despite retained intermediate information. They explicitly delimit this from generation-time computation. These are different models, tasks and prefix conditions from our ordinary generated answers, so the finding does not diagnose our wrong-entity echoes.

Local design implication: inspect whether generated quantities come from the target or an exemplar. A correct label with borrowed/wrong quantities remains an unwarranted explanation. If positional copying later becomes the explicit question, independently manipulate example order/last example; the current correct/permuted comparison alone cannot identify position as the cause.

## Scope and next decision

The most useful immediate contact remains a small frozen permutation control with balanced labels, identical target questions, matched serialization and generation allowance, generated-continuation-only scoring, and preserved failures. Keep absolute competence visible through a no-demonstration condition if feasible. If adding a quoted/apply-role factor, report its wrapper cost and treat it as a prompt intervention rather than a security boundary or pure information-equivalent comparison.

These sources motivate discriminators; they do not establish an FRR improvement, a neural mechanism, or general inferiority/superiority of a prompt. This is selected primary-source extraction, not a systematic review, full-paper audit, code inspection or independent replication. Search-result summaries were used to locate sources; claims above were checked against the linked primary HTML. The prior Min et al. primary abstract was also reopened for orientation, but no additional result from it is required here.

## Source-access record

- Yoo v2: opened primary HTML; targeted model/sensitivity/corruption sections inspected. No code run.
- Copying to Composition v1: opened primary HTML; task, models, literal prompt and 360M training-design sections inspected. No code, model weights or results reproduced.
- Readout Shortcut v1: opened primary HTML; abstract, scope, model and prefix protocol inspected. No causal/head-level experiment reproduced.

Only this new scout file is written by this scout. Historical reports and model artifacts are unchanged.
