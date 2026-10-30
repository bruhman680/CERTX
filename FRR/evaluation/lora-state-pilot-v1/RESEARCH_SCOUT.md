# Follow-up scout for the bounded LoRA pilot

2026-10-30. Read the prior [narrow-pilot report](/workspace/frr/evaluation/narrow-training-pilot-v1/REPORT.md). Its single full-weight update changed exact-label behavior to all-NO; that is not evidence of the positive/zero/missing distinction, and no unrelated-task measurement establishes catastrophic forgetting. The old test is exposed regression material. This note offers three distinct primary sources and design inferences for a separately frozen next pilot. No packages installed, training performed, or FRR/frozen-scout files edited by this scout.

## 1. Low-rank restriction is a learning–retention tradeoff

Biderman et al., [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673), [version 2 full text](https://arxiv.org/html/2405.09673v2).

**Read depth:** abstract; sections 2, 3.3, selected 4.1 passages, 4.7 and discussion/conclusion. Not an exhaustive audit of tables, learning-rate sweeps or appendices.

**Source finding:** in 7B code/math experiments, common low-rank settings learned less than full tuning while better retaining measured source-domain performance. Higher ranks could close instruction-tuning gaps in some settings. The study explicitly separates target-domain and source-domain evaluations and examines sensitivity to rank, scaling, learning rate and target modules.

**Pilot inference:** fit and semantic acquisition are separate outcomes. Log the actual rank, scaling convention, module names and trainable parameter count. Preserve the base model for paired evaluation. If retention matters, predeclare a small unrelated-behavior regression set; do not call frozen backbone weights proof of unchanged behavior while an adapter is active. One configuration’s failure does not diagnose LoRA generally.

**Limits:** these are much larger models, datasets and budgets. Neither their ranks nor their hyperparameters are validated recommendations for 135M CPU training. Their measured retention advantage does not guarantee this pilot avoids forgetting, and its all-NO predecessor does not demonstrate the same phenomenon.

## 2. Data order and early evaluation matter on small datasets

Dodge et al., [Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping](https://arxiv.org/abs/2002.06305), [version 1 full text](https://arxiv.org/html/2002.06305v1).

**Read depth:** abstract; methodology; section 4 including data-order/initialization separation and majority-baseline failures; beginning of section 5. Did not audit the full stopping-policy analysis or reproduce experiments.

**Source finding:** BERT experiments on four GLUE tasks found substantial variation with random seeds. Initialization of the task head and training-data order made comparable contributions to variation. Some runs performed near majority baselines; early validation could distinguish promising runs in their setting.

**Pilot inference:** a dataset balanced overall may be unbalanced in the few updates actually completed. Balance classes within each effective update, including accumulated microbatches, and retain the ordered IDs/labels actually applied. Declare development-evaluation checkpoints and stopping/selection rules before training. Keep final holdout results out of checkpoint selection; publish any partial schedule and its class exposures.

**Limits:** balancing every effective update is our proposal, not a tested result of this paper. Its model has a randomly initialized classification head, unlike this existing generative output head plus new LoRA factors. Its multi-run early-stop strategy does not authorize extra attempts or justify picking the best seed after looking at this test.

## 3. Parameter location matters; a tiny update can expose existing behavior

Ben Zaken, Ravfogel & Goldberg, [BitFit: Simple Parameter-efficient Fine-tuning for Transformer-based Masked Language-models](https://arxiv.org/abs/2106.10199), [version 2 full text](https://arxiv.org/html/2106.10199v2).

**Read depth:** abstract, sections 2–4, including the random-parameter comparison; optimization appendix A.2 skimmed. Not a complete task-table or implementation audit.

**Source finding:** freezing a BERT-family encoder while training bias terms and a task classifier was competitive on several small/medium GLUE tasks. Training a similarly sized random parameter subset performed worse. The authors discuss exposing pretrained capabilities versus acquiring new ones.

**Pilot inference:** “few trainable parameters” alone is an incomplete experimental description. Record precisely what can change. A valid short label after adaptation may reflect improved output selection or compliance; semantic target binding needs its own counterfactual tests.

**Limits:** this is masked-model classification with specific bias parameters, not decoder label generation or LoRA. Do not assume SmolLM2 has the same bias tensors or that bias-only tuning is a directly available fallback. Its results do not prove this pilot’s target distinction already exists in the base model, and its learning rates cannot be transferred as defaults.

## Proposed diagnostics for this run

The following are practical design inferences, not replications of any paper:

- Use the resource probe to measure a complete optimizer step at the declared maximum input length, and retain exact memory readings at each guard check. Static optimizer estimates do not capture peak working memory.
- For a custom LoRA implementation, verify initial forward equivalence to the base, one-random/one-zero factor initialization, finite gradients, and actual adapter updates. Both factors initialized to zero make BA’s parameter gradients zero. A zero first-step gradient for the random factor can be expected while the other factor starts at zero; it is not alone evidence of a broken implementation.
- Verify the backbone remains numerically unchanged and only the declared adapter parameters enter AdamW. Save adapter configuration and base revision together so the branch is reconstructible.
- Evaluate all examples in the denominator. Track valid exact-label output rate separately from confusion matrices and per-class recalls. Compare with every constant-label baseline. An all-NO model remains a constant predictor even if it completes cleanly.
- In the canonical development slice, use target-state minimal pairs while preserving distractor zero and missing fields. Track whether predictions change appropriately across the pair; label diversity alone is insufficient.
- Keep source-unavailable WITHHOLD as a semantic class, with invalid output separate. If scoring by label likelihood as a diagnostic, name it separately from the frozen free-generation interface.
- State that one bounded seed/configuration can establish a local outcome, not stability across seeds, LoRA superiority, broad retention or general FRR effectiveness. Do not expand the budget retrospectively because one observed result is promising.

All links are public primary-author arXiv text, checked 2026-10-30. Search results located the sources; claims above rely on the stated primary passages. Original LoRA mechanics were already covered in the separate memory scout; this follow-up does not apply GPU memory percentages to CPU.
