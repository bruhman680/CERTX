# Parallel feedback scout — 2 November 2026

Delegated source reading by feedback_knowledge_scout, not an experimental replication. Read the prior SDPO extraction and review-menu report, then exactly two primary papers. Root records the scout's checked depth and cautions here; no claim of a second independent full-paper audit.

- [Huang et al., 2310.01798v2](https://arxiv.org/html/2310.01798v2): abstract, sections1–7, Tables2–8 and reproducibility statement; appendix examples not fully inspected. Oracle stopping protects initially correct answers using ground truth. Intrinsic correction lacks that protection. Track both correct-to-wrong and wrong-to-correct changes over all cases; keep oracle gating distinct from feedback content. Model/task scales differ substantially from135M. No author code link located in the bounded check; this is not proof none exists.
- [Gou et al., CRITIC, 2305.11738v4](https://arxiv.org/html/2305.11738v4): method sections3–4, selected tables/appendices, official README and QA/program correction scripts. Execution output supplies evidence about behavior, not guaranteed semantic correctness; evidence can be misread and corrections can harm. Smallest tested Llama-2 is7B. [Official code](https://github.com/microsoft/ProphetNet/tree/master/CRITIC) separates execution evidence entering the correction prompt from execution used for evaluation.

Implication for our frozen study: matched original/no-feedback baselines, all cases retained, repairs and harms, reliable versus wrong-source notes, and separation of evaluator metadata from model inputs. Simplification changes presentation and cannot itself establish a feedback effect. No result transfers automatically to our135M reader; no evidence here of retained weight learning or authenticated source selection.

Scouting did not modify the frozen design after output inspection; it supports controls already specified before the model run. No paid service, install or new model was used.
