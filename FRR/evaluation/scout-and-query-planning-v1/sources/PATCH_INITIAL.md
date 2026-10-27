# PATCH — bounded primary-source scout

## Paper-derived summary (under 180 words)

The verified paper is **Scalable Patch-Level Self-Supervised Learning**, arXiv **2610.10013v1** (7 October 2026), introducing JEM. The supplied 2610.01031 resolves to an unrelated microwave-modeling tutorial. [Identity](https://arxiv.org/abs/2610.10013v1), [mismatched ID](https://arxiv.org/abs/2610.01031v3).

JEM assumes each view preserves downstream-task information; the authors explicitly call this task/view-dependent and idealized. An EMA teacher supplies categorical patch targets. KL alignment matches corresponding overlapping patches, including visible and masked patches. Per-position marginal-minus-conditional entropy prevents global/positional collapse; a separate structural proxy reconstructs teacher-layer pairwise cosine similarities, because individually informative patches can still repeat one image-level code. Independent photometric augmentation matters substantially in ablations.

Evaluation uses frozen-backbone probes across classification, segmentation and depth. Controlled DINOv2 comparisons are stronger evidence than the unmatched DINOv3 comparison; classification retains a gap. Scaling is expensive: 300M–7B models, 500k steps; 7B uses batch 4096 and about 1.851 trillion student tokens on A140M. Smaller dataset size does not establish low compute cost. GPU-hours, wall-clock expense and verified JEM code were not established. [Methods, evaluation and configurations](https://arxiv.org/html/2610.10013v1).

## Original proposed transfers — not paper claims (under 200 words)

For paired contrasts, first distinguish nuisance changes from semantic interventions. Positive pairs may share lexical material while reversing agent/patient roles; forcing their whole representations together would destroy the signal we need. Audit a small, manually checked set of each proposed view transformation for role preservation before applying consistency.

Use two diagnostics separately: diversity across examples, and sensitivity within each example to role-bearing spans or edges. A varied embedding collection can still map every local element of an example to its topic. Test role swaps, negation, argument deletion and harmless paraphrases; report invariance to the last alongside sensitivity to the others.

For unknown roles, retain abstention and alternatives instead of treating agreement as truth. Ask whether a second view preserves independent evidence or merely repeats the same model's guess. Rank scout queries by which disputed role a result could resolve. Begin with an offline evaluation of existing representations and bounded queries; this paper supplies no evidence that retraining our system or importing its image augmentations will help.

## Source scope and access limits

- [Correct arXiv record](https://arxiv.org/abs/2610.10013v1): version/date/title/author metadata and abstract checked.
- [Versioned primary full text](https://arxiv.org/html/2610.10013v1): read §§3–4 and selected Appendix A.1/A.6 and training-token table; no complete proof audit, reproduction, training or installation. HTML equations/figures may omit rendering details. No standalone limitations section was identified; limitations above distinguish author caveats from scout inference.
- [Incorrect-ID record](https://arxiv.org/abs/2610.01031v3): metadata only, to resolve mismatch.

Search budget: three queries total (title/MetaJEM; GitHub organization/title; title/code/Meta). No verified author JEM repository surfaced in that bounded search or paper links; this is an access/discovery limit, not a claim that code does not exist. Only primary sources support the summary. No complete document or PDF was saved.
