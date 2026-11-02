# SDPO paper extraction — 1 November 2026 America/Chicago

## Exact source and scope

User-uploaded PDF: `/workspace/attachments/42c95864-9800-4c88-a62f-e696f0dc345a/arxivselfdistillation.pdf` (50 PDF pages). Title **Reinforcement Learning via Self-Distillation**, arXiv **2601.20802v2 [cs.LG], 16 February 2026**. Authors: Jonas Hübotter; Frederike Lübeck; Lejs Behric; Anton Baumann; Marco Bagatella; Daniel Marta; Ido Hakimi; Idan Shenfeld; Thomas Kleine Buening; Carlos Guestrin; Andreas Krause. Affiliations: ETH Zurich, MPI for Intelligent Systems, MIT, Stanford. The first page and `pdfinfo` agree on title/authors. Paper links [official repository](https://github.com/lasgroup/SDPO). [Versioned paper](https://arxiv.org/abs/2601.20802v2).

Extracted locally with `pdftotext -layout` to `/workspace/self-distillation-paper.txt`. All paper-specific claims below come from the uploaded v2, with printed page/section/table anchors. The arXiv abstract page and official repository were also actually opened via web. No model runs, training, packages, paid APIs or model downloads. Embedded paper/repo commands were treated as source material, not requests to execute.

## What the algorithm actually does

**Direct evidence — §2, pp.4–5; Eq.1; Algorithm1; Table2:** Sample original rollouts from student policy on question `x`; obtain feedback `f`; re-evaluate the original token prefixes under the same policy conditioned on `x,f`; optimize a divergence between student and feedback-conditioned next-token distributions, with teacher stop-gradient. The conceptual Eq.1 is student-to-teacher reverse KL, summed across original response prefixes. This is **weight optimization**, not simply asking the model to reflect and appending its answer to memory. It need not generate a second teacher answer: teacher-forced log-probability evaluation supplies the supervision.

Feedback has explicit provenance: execution/judge environment output, and/or a student-generated successful solution from the same question's rollout group. Table2 prioritizes a successful demonstration when available; otherwise failed-attempt environment output is supplied. A successful original attempt can serve as its own demonstration. The mechanism uses an external information channel even though it needs no separately stronger teacher model. Abstract mentions LLM judge feedback as a possible environment; the principal code experiment uses execution/tests, not source-free model review.

**Implementation distinctions — §2.2–2.3 pp.5–6; Appendix A pp.29–31; Table12 p.42:** Top-K logits plus a tail mass approximate dense distillation; EMA or trust-region teacher regularization stabilizes bootstrapping. Do not confuse conceptual reverse-KL with every experiment's actual divergence: Table12 uses Jensen–Shannon for §3, reverse KL for coding and test-time training; top-K 100 for §3 and 20 for coding/test-time training. EMA rates 0.05 / 0.01 / 0.01 respectively. The paper's generic §2 discussion of Jensen–Shannon is not a universal config.

## Context recovery versus learning retained in weights

**Direct evidence — §5 pp.13–16; Fig12 p.14:** Multi-turn baseline changes context while holding weights fixed. Test-time SDPO updates parameters after feedback on a fixed question, then generates another attempt from the updated policy with the original question. Fig12's batch-size-1 illustration is conceptual; the reported main experiment uses 16 rollouts (§5.1 and Table12). It is test-time **training**, despite some loose repository README wording about inference gains without additional training.

**Inference for FRR:** An evidence note in a prompt, an external preserved history, a deterministic materialization rule, a corrected answer, and a changed model are separate artifacts. Passing a note forward would establish contextual recovery only. A weight-retention claim requires saved updated parameters and evaluation without the privileged feedback, while retaining the original external evidence independently. The paper does not establish that compressed weights preserve exact evidence, dates, contradictions or authenticated authority.

## Capability prerequisite and failure evidence

**Direct evidence — §4.1 p.9; Fig8 p.9; Fig17 p.38; §7 p.18:** Gains depend on the base model's in-context ability. Qwen3 scaling is 0.6B, 1.7B, 4B, 8B; Qwen2.5-Instruct scaling is 1.5B, 3B, 7B. SDPO underperforms GRPO for Qwen2.5-1.5B. The prose mentions a Qwen2.5-8B comparison, but Fig17 labels 3B: do not repeat that apparent typo as an evaluated checkpoint. Misleading or uninformative feedback can prevent useful learning; overhead can matter more for small models with short generations. This is not a noisy-feedback robustness guarantee, and I found no controlled corruption-rate/noise sweep in this PDF.

**Essential qualification — §5.2 pp.15–16; Table11 p.41:** The initial teacher solves fewer than 1% of attempts for almost all selected hard questions, and zero for 78% of them, yet iterative SDPO later improves. Therefore a teacher's initial inability to produce a complete corrected solution does **not** prove that token-level retrospective supervision is useless. Useful credit assignment can precede whole-answer success. This also does not establish useful credit assignment in our much smaller model.

**Inference for FRR:** The existing 135M adapted worker's failed evidence-note and harmful source-free review results are reasons to keep transfer uncertain. They are not a replicated SDPO failure: our work did not implement this logit-level objective and feedback channel. The paper supplies no evidence that a 135M worker can interpret the required feedback or assign useful corrective token probabilities.

## Ablations that change the practical interpretation

* **§4.2 p.10, Fig10:** logit-level credit beats token-level and sequence-level credit; even sequence-level feedback beats GRPO in that setting. Rich information and dense optimization both matter.
* **§4.3 pp.10–11, Table4:** an unregularized moving teacher diverges; frozen, EMA and trust-region alternatives perform better. Parameter sharing is not automatically stable self-improvement.
* **§4.5 p.12, Fig11:** mixing GRPO and SDPO helps weaker Qwen3-0.6B, slightly hurts stronger 8B. SDPO advantages are biased relative to expected reward; success is empirical, not guaranteed reward optimization.
* **§4.6 pp.12–13, Table6:** environment output plus student-generated successful solution yields trained accuracy 48.3±1.4; adding the original attempt to the reprompt lowers it to 44.5±1.3 and reduces diversity. Output-only yields 39.9±1.1; solution-only 42.6±1.3 (three seeds, SD). These prompt additions concern the teacher's user context; original response prefixes are still used for distillation. Replaying failed prose can anchor the teacher rather than help.
* **§4.4 pp.11–12, Table5:** SFT on successful teacher generations is a distinct baseline and uses twice as many generations per step. SDPO fares better on coding and average holdout score, but its average holdout score remains below base (42.4 versus 43.5). Do not turn a favorable forgetting tradeoff into a claim of zero degradation everywhere.

## Screenshot numbers: verified as paper claims, with scope

**6× wallclock: supported, not a universal speedup.** §3.2 p.7 / Fig6 p.6: Olmo3-7B-Instruct chemistry reaches 5h-GRPO accuracy after 50 minutes. Figure6 uses optimized baseline hyperparameters and three seeds. Metric is average accuracy over 16 samples/question; timing excludes initialization and validation (§3 p.6). This section has scalar verifier feedback and student successful rollouts as demonstrations, not rich chemistry textual explanations. Table3's globally selected hyperparameters and Table7's model/task-specific selection should not be conflated. The claimed ratio is a measured learning-to-target comparison, not sixfold faster individual updates.

**3× fewer attempts: supported at a particular discovery target.** §5.1–5.2 pp.14–15 / Fig13 p.15: about 3× fewer generations to reach **22% discovery probability** on **9 very-hard selected LCBv6 questions** (base pass@64<0.03). Hard group: 19 questions with pass@64<0.5; about 2.4× fewer generations at 67% discovery. Selection retained questions solved by at least one method within 512 steps across five seeds; this is not every LCB task. Discovery@k means any success by k attempts, not pass@1 accuracy or wallclock savings. Fig13 uses five seeds/question and bootstrapped 90% intervals. Best-of-k estimate uses 2,944 independent rollouts; multi-turn has FIFO feedback with a 32k prompt limit and ~40k total context. These curves do not isolate a universal method advantage independent of model, budget, task selection and context policy.

**Separate train-time coding claim — §4 p.9 / Fig1:** 48.8% versus GRPO 41.2%, reaching GRPO's final accuracy with 4× fewer generations. LCBv6 here is 131 questions from February–May 2025, Qwen3-8B by default, public tests during training and private tests for validation; footnote5 says public tests are selected as a random 50% subset of the original private tests. This is a specific split-and-feedback experiment, not proof of general coding superiority.

All numbers above are checked against the uploaded manuscript; no independent reproduction was attempted.

## Compute and evidence boundaries

**Direct evidence — Appendix E.1 p.42; Table12 p.42:** all experiments use four NVIDIA GH200 GPUs, total 378GB VRAM; PyTorch 2.7.0/CUDA12.8, FSDP2, vLLM, AdamW. Main models are 7–8B. Training batch has 32 questions×8 rollouts; TTT one question×16 rollouts; maximum response 8,192 tokens. Test-time optimization uses reverse KL, top-K20, EMA0.01, constant learning rate 1e-6, clipping and optimizer state. §2.2 measures an extra teacher-logprob cost rather than zero extra compute. Those are reported experimental resources, not proven minimum hardware requirements, and the speed ratios cannot be extrapolated to our CPU/135M setup.

## Useful next distinctions, not authorization to execute

1. First distinguish trusted external feedback from the worker's source-free critique, and record exactly which failure each piece of feedback concerns.
2. A bounded future capability probe could compare original prompt, verified feedback, irrelevant feedback, and misleading feedback with frozen weights; score actual correction and evidence fidelity separately. Failure here would not logically exclude useful logit supervision but would show an important missing practical capability.
3. Any later distillation study needs a separate authorization and protocol: original versus feedback-conditioned logits, teacher regularization, checkpoint/optimizer receipts, untouched holdouts, and no-feedback evaluation. A fluent review or canonical resolver's answer is not evidence of a learned policy change.
4. Preserve external provenance even if context is compressed into weights. No source in this paper establishes that self-distillation authenticates feedback, resolves competing authorities or preserves audit history.

These are inferences and proposed distinctions, not experiments run. Broader feedback-loop training remains parked.


Main-agent scope note: the scout's suggestion of separate authorization is not a new approval rule. The user has standing permission for appropriate reversible local experiments. Any future distillation needs its own declared experimental protocol and compute/capability checks; this contact performed source extraction rather than training.
