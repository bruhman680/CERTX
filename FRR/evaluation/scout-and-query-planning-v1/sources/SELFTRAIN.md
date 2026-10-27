# OPST bounded primary-source scout

Verified 2026-10-27: Leon Sick, Lukas Hoyer, Yannick Strümpler, Christian Reisswig, Timo Ropinski, Federico Tombari, **On-Policy Self-Training: Data-Free Self-Improvement in Large Language Models**, arXiv:2610.32770v1, submitted 2026-10-23. [Versioned metadata](https://arxiv.org/abs/2610.32770v1); [versioned full text](https://arxiv.org/html/2610.32770v1). The abstract page lists only v1. No official code link found in these pages or the bounded search; this does not establish that none exists.

## Paper-derived summary (175 words)

OPST generates questions, rationales and candidate answers from hand-chosen topic descriptors using pretrained weights. “Data-free” excludes curated training questions/answers, retrieval and an external stronger teacher; it includes existing parametric knowledge, human-written synthesis prompts and benchmark-domain labels. Visual OPST additionally uses unlabeled OpenImages images. The generator checks answers in fresh contexts and after paraphrasing; these are consistency checks, not independent correctness verification. A student consensus gate removes already-solved candidates. An EMA teacher receives generated rationale/answer context unavailable to the student, then supplies token distributions on student rollouts for gradient training. Evaluation uses the EMA model.

Gemma E2B non-thinking MMLU rises 37.5→47.7; thinking rises 69.9→71.1. Same-data SFT/GRPO comparisons and ablations support this setting, not autonomous discovery. Retention is mixed: all-domain training reduces MATH-500 by 4.9 points. Existing knowledge bounds improvement; consistent errors survive. Small models, chosen topics and benchmark-linked design constrain generalization. Pretraining contamination and held-out checkpoint selection are not resolved. Generation, fresh/paraphrase solves, consensus rollouts, teacher forwards and backpropagation incur compute; no end-to-end cost accounting is provided. Seven rounds outperform twelve/twenty in the reported MMLU ablation.

Support: §§3–6, Tables 1/3/5, Appendix A.1–A.7 in [v1](https://arxiv.org/html/2610.32770v1).

## Our proposed FRR transfer (not a paper result; 163 words)

Use synthetic queries to expose a planning uncertainty, then check the consequential claim against a task-relevant primary source. Record whether an answer came from source text, model memory, generated rationale, benchmark label or evaluator access. Same-model agreement can nominate a query or expose wording sensitivity; it cannot confer source authority. Rephrasing must preserve the disputed distinction; include a role-changing counterfactual as a separate sensitivity check.

Keep privileged training/evaluator context separate from ordinary reader inputs. An author can build a test using a hidden answer or source annotation, but the reader planner must choose sources and abstain using only its declared access. Score held-out reader success and unsupported confident answers separately from teacher-assisted or supplied-context performance. Freeze query budgets and test items before comparing planning procedures; include shared-error sources and cases where no authoritative answer is accessible. Stop when an external check changes the next action or the budget expires. No model training, index replacement or claim of learned improvement follows from this scout.

## Read scope and limits

Read versioned arXiv metadata and HTML §§1–6, Tables 1–8, Appendix A.1–A.8 (including evaluation protocol and prompt roles); no PDF figures were visually inspected. HTML has an apparent malformed mixture expression in §3.5; the loss was not implemented or independently validated. No repository, checkpoint, generated dataset or training logs inspected. No API training, installation or reproduction performed. Search budget: one malformed unsuccessful web call plus two successful search queries, three attempted query strings total; two selected primary resources, both manifestations of the same paper, not independent corroboration. Third-party search hits were discovery leads only. Detailed provenance and information-access trace: [SELFTRAIN_SOURCES.json](SELFTRAIN_SOURCES.json).
