# Training scout: positive counts, explicit zero, and missingness

Research checked 2026-10-30 using public primary paper pages. Scope: a first CPU fine-tuning pilot on SmolLM2-135M-Instruct, following an all-YES full-task baseline. No paper below reproduces that observation or tests this proposed task. Recommendations labelled **pilot inference** are proposed experimental choices, not published findings. No training was performed by this scout.

## Recommended use of this literature

Treat the pilot as a narrow semantic classification experiment: `POSITIVE` = a known count greater than zero; `ZERO` = an explicitly reported zero; `MISSING` = no reported target count. `MISSING` describes the source record. It is not model uncertainty. Define what counts as missing before generation: absent field, null marker and explicit “not reported” may be separate representation subtypes; ambiguous prose and contradictions can be excluded from the initial task.

Freeze the final test and its structural-family manifest before training. Select checkpoints and any thresholds using development data only. Compare the unchanged checkpoint and adapted checkpoint on exactly the same frozen examples. Preserve raw predictions, parsing failures, checkpoint identity, data hashes and seed. Report per-class recall, a confusion matrix, macro accuracy and breakdowns by structural family. An all-one-class predictor obtains one-third accuracy on a balanced three-class set; also report its actual score on each real split. These are **pilot inferences**, not numerical expectations supplied by the papers.

## 1. McCoy, Pavlick & Linzen (2019): controlled tests for shortcut learning

[Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference](https://arxiv.org/abs/1902.01007), ACL 2019. [Versioned full text](https://arxiv.org/html/1902.01007v4).

**Read depth:** abstract, introduction/heuristic examples, and section 7 including withheld-subcase transfer; not a full appendix audit.

**Finding:** HANS tests cases where lexical/structural heuristics fail. MNLI-trained systems, including BERT, struggled. Adding HANS-like training examples helped, but withholding subcases exposed incomplete transfer and replacement shortcuts.

**Pilot inference:** create minimal pairs in which the target field changes semantic state while irrelevant fields retain the same zero/NA/positive tokens. Include target selection, field order and distractor tests. Reserve whole structural families: merely generating fresh values in the same templates tests interpolation. Inspect whether adaptation replaces “always YES” with “any zero means ZERO” or “any missing marker means MISSING.”

**Limit:** this is NLI with different models and substantially larger datasets. It supplies diagnostic design, not a forecast of how many examples this 135M model needs.

## 2. Lake & Baroni (2018): random splits do not establish systematic composition

[Generalization without Systematicity](https://arxiv.org/abs/1711.00350), ICML 2018. [Versioned full text](https://arxiv.org/html/1711.00350v3).

**Read depth:** abstract, task definition, experiments 1–3 descriptions, and discussion passages; not all supplementary analyses.

**Finding:** SCAN recurrent sequence models could succeed on random recombinations while struggling with length extrapolation and applying known composition rules to a primitive seen only in isolation. The paper also reports successful generalizations, so its claim is conditional, not universal neural failure.

**Pilot inference:** separate held-out wording from held-out structure. A structural test can combine a familiar target-state rule with an unseen arrangement of records/distractors, while keeping all semantic operations individually represented in training. Keep longer-input extrapolation separate from semantic composition so a failure is interpretable.

**Limit:** these are recurrent seq2seq models trained on synthetic commands, not pretrained decoder transformers. A failure here does not establish an architectural limit of SmolLM2; a small pilot success does not establish universal composition.

## 3. Geifman & El-Yaniv (2019): abstention requires its own evaluation

[SelectiveNet: A Deep Neural Network with an Integrated Reject Option](https://arxiv.org/abs/1901.09192), ICML 2019. [Versioned full text](https://arxiv.org/html/1901.09192v4).

**Read depth:** abstract, sections 2, 5 and selected experimental passages; architecture/optimization skimmed, not reimplemented.

**Finding:** selective prediction pairs a predictor with a selection function. Performance trades off coverage (fraction accepted) against selective risk (error among accepted predictions). Its experiments use an integrated rejection architecture and discuss validation-based coverage calibration.

**Pilot inference:** do not use the semantic `MISSING` label as an abstention bucket. Initially score all three classes at full coverage, counting invalid generations as errors. If epistemic rejection is later added, retain a distinct `ABSTAIN`, choose its rule on development data and report both coverage and error among accepted outputs; report undefined risk when nothing is accepted.

**Limit:** its architecture and image/tabular experiments do not validate verbal confidence, maximum token probability, or rejection under the pilot’s structural shifts. A low accepted error rate alone may simply reflect heavy rejection.

## 4. Ben Allal et al. (2025): capacity-aware data curation in the actual model family

[SmolLM2: When Smol Goes Big—Data-Centric Training of a Small Language Model](https://arxiv.org/abs/2502.02737). [Versioned full text](https://arxiv.org/html/2502.02737v1).

**Read depth:** abstract, introduction, post-training sections 5.2–5.4, section 6; not a full audit of pretraining ablations or model cards.

**Finding:** most of the report concerns 1.7B. Section 6 explicitly covers 135M/360M, reruns data ablations at their scale, and filters post-training data to remove complex instruction tasks and difficult examples to suit capacity. The 135M model was pretrained on 2T tokens.

**Pilot inference:** a short, unambiguous task with verified labels and controlled output format is a defensible starting point. Treat data quality, target selection and generalization measurement as first-class variables. Record that this is additional adaptation of an already pretrained/instruction-tuned model: “no prior training” applies to our pilot, not the checkpoint.

**Limit:** this report does not establish a 135M fine-tuning ceiling, guarantee CPU feasibility for any proposed schedule, or identify an optimal learning rate for this task. Do not copy 1.7B training hyperparameters as evidence-based 135M pilot settings.

## 5. Geirhos et al. (2020): broader interpretation, secondary priority

[Shortcut Learning in Deep Neural Networks](https://arxiv.org/abs/2004.07780), Nature Machine Intelligence perspective; arXiv v5 revised 2023.

**Read depth:** primary author abstract/metadata only. This is a perspective rather than a new task-specific empirical study; included for framing, not as an independently audited experiment.

**Finding:** the authors describe shortcuts as rules that perform well in standard benchmark conditions yet fail under more challenging testing conditions.

**Pilot inference:** ordinary held-out accuracy is only one piece of evidence. Counterbalance conspicuous cues and inspect diagnostic cases before claiming the model learned the intended distinction.

**Limit:** neither a single all-YES baseline nor a later transfer failure diagnoses shortcut learning by itself. Parsing bugs, instruction interpretation, class bias and optimization failure remain alternatives. The HANS paper above offers the more directly actionable empirical design.

## Concrete additional controls

These are proposed controls informed by the papers, not their experimental results:

- Keep an easy canonical dev slice to distinguish failure to acquire the three labels from failure to transfer.
- Match lexical cues across labels where semantics allow. For instance, place an unrelated zero and an unrelated missing value in every record, and vary only the requested target.
- Split by generation family before rendering examples; deduplicate normalized examples across splits. Different random seeds alone do not prevent template leakage.
- Use a deterministic semantic oracle to generate/verify labels and inspect sampled records. Define explicit missing markers; avoid treating an unexplained dash as universally missing.
- Keep exact-label generation accuracy and any label-likelihood classification diagnostic separately named. Restricting decoding to labels can fix output formatting without proving semantic improvement.
- Use a fixed development stopping rule and modest predeclared compute budget. If the canonical slice cannot be learned, report that negative result before expanding to the full soil-variance task. No cited paper establishes the appropriate budget.

## Source receipt ledger

Public browser reads completed 2026-10-30. Relevant stable locations: HANS v4 sections 1 and 7 (especially “Transfer across HANS subcases”); SCAN v3 sections 2 and 4, experiments 1–3; SelectiveNet v4 sections 2 and 5; SmolLM2 v1 sections 5.2–5.4 and 6; Geirhos v5 abstract only. Search snippets were used to locate papers, not to support unverified numerical claims. No paid resources or APIs were used, and no existing FRR files were modified.
