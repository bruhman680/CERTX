# Symbolic transfer: bounded research perspective

**Status.** Planning only. Read LAB_BRIEF.json and the exact compact FRR prompt; use FRR as working guidance, without claiming a cognitive upgrade. No model calls, training, model downloads, or old-world edits. “Understanding language supports other systems” remains a hypothesis.

## Evidence actually read

1. **Mirchandani et al. (2023), [Large Language Models as General Pattern Machines](https://arxiv.org/html/2307.04721v2).** Read abstract/introduction, methods and results §§3–7, including tables and limitations; appendices not audited. Pretrained large models complete symbolic transformations, numerical sequences, and some robot trajectories without weight updates. On 800 ARC tasks, text-davinci-003 solved 85 with digits versus an average 43.6 with five random token alphabets. Procedurally generated PCFG transformations reduce reliance on memorized ARC examples. Consistent tokenization materially changes performance. Robotics results depend on supplied demonstrations, discretization, ordering/context selection, and sometimes online rewards. This supports partial representation robustness and context-mediated adaptation. It does not isolate language understanding as their cause, establish universality, or establish corresponding capacity at 135M parameters. Random remapping reduces a contamination route; it does not erase all training ancestry.

2. **Lake & Baroni (2018), [Generalization without Systematicity](https://arxiv.org/html/1711.00350v3).** Read main §§1–5, SCAN grammar/interpretation and architecture descriptions; did not inspect implementation or replicate. Trained recurrent sequence-to-sequence networks translate a finite navigation-command grammar into actions. The overall-best architecture reached 99.7% on a random split, 13.8% on a longer-output split, and 0.08% when composing “jump” encountered only as a primitive. A different architecture reached 90.3% for the analogous “turn left” split, where its action also appears inside other training outputs. Thus distributional coverage and operation role matter. These are counterexamples to inferring systematic composition from familiar-distribution success, not proof that transformers or SmolLM2 must fail.

These papers study different bodies/procedures; neither independently verifies this garden.

## Operational distinctions and inference

- **Prediction:** a committed expected next observation, compared with the subsequently realized outcome under stated conditions. Successful continuation alone can reflect copying or familiar templates.
- **Understanding:** a provisional, domain-bounded explanatory attribution supported by coherent predictions across novel compositions and interventions, including sensitivity to changed laws. No single score or fluent explanation establishes it; verbal explanation is optional and not necessary for behavioral evidence.
- **Transfer:** source experience improves target behavior relative to an explicit matched alternative. Distinguish renamed-symbol robustness, new compositions, longer horizons, and genuinely changed domains. Target success alone is target competence.

**Inference:** useful transfer needs some shared exploitable structure, an accessible representation, adequate evidence distinguishing rival rules, and sufficient computational/context capacity. There is no unconditional route from any observed language history to every possible system: two targets can match every observed example yet disagree on an unseen transition. Neither more prose nor “understanding” resolves that without additional assumptions or contact.

## Design proposal: one optional transfer contact

Keep free play intact. After a frozen observation window, offer an optional encounter with a small target artifact. If a source relation was explored—for example order-sensitive composition of two transformations—construct two matched targets: fresh symbols preserving that operation structure, and a near-target changing exactly one operation. If no source structure exists, defer the transfer claim rather than impose a curriculum.

Use identical neutral invitations and identical target-only evidence across contexts; never supply the source–target map or answer. Include a revealing example of the changed operation before probing a new composition. Compare source-history accessibility against equally budgeted irrelevant history and, if feasible, a matched passive transcript. Freeze predictions before reveal. Keep these observer comparisons outside the garden's behavioral instructions; no rewards, compulsory exercises, or progress gates.

**Discriminating observation:** source-relevant context aids unfamiliar compositions after renaming while the model selectively revises behavior at the changed operation. Failure to outperform the matched alternative defeats this contact's transfer claim; copying the old operation despite contrary evidence favors rigid analogy. A single encounter is diagnostic, not an effect estimate.

## Unknowns and cross-review

Evaluation partner accepted the preserved-operation/one-change distinction and challenged attribution under voluntary participation. Adopted: log offered, accepted, declined, and uninterpretable separately; declining supplies no ability result. Conditional-on-acceptance comparisons cannot identify an effect when participation differs. Passive history tests an agency contribution imperfectly; full versus irrelevant history primarily manipulates accessible information. Visible-history success is context-supported adaptation, not weight learning. Pretraining contribution, retention after context removal, and genuinely distant transfer remain unknown; source-language causality would require a separate controlled training study outside this authorization.
