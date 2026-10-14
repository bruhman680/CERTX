# DecepEval: source weave and construction genealogy

Reviewed from the uploaded arXiv:2610.07967v1 paper and read-only public artifacts. This is a genealogy/repair pass, not a reproduction of model runs or a verdict that deception is absent. No benchmark agent or judge API calls were executed. FRR core instructions are unchanged.

## Strongest surviving relationship

DecepEval makes **agent-visible evidence, recipient-visible claims, and task-valid completion** separately inspectable. Its pairing provides a useful way to observe how changed instructions alter contradictory reporting within a constructed task distribution. That contribution does not require proving private deceptive intent. Conversely, observing a contradiction after delivery of evidence does not uniquely identify the cognitive mechanism that produced it.

The paper already recognizes this boundary: Appendix D.3 and the judge prompts explicitly exclude hidden-reasoning inference and require verifiable truth, prior availability, material contradiction, possible misleading effect, and exclusion of ordinary error. Criticizing it as simply labeling every failure deception would miss its actual safeguards.

## Access and dependency ledger

| Source | Access depth in this pass | Actual contribution | Boundary / repair contact |
|---|---|---|---|
| [DecepEval v1](https://arxiv.org/abs/2610.07967) | Uploaded full text; main definitions, construction, related work, reproducibility statement and Appendix D.3 inspected | Behavioral evidence-chain benchmark and neutral/induced comparisons | Validity of exclusion of ordinary error remains a measurement question; human agreement is not independent proof of latent cause |
| [Official DecepEval repository](https://github.com/functy/DECEPEVAL/tree/3ca4ed0ca4ab2fe942984d929d797a16421890a4) | Recursive untruncated tree, README, runner, two judge implementations, prompt loader, shared prompt, coding schema and evaluation controller read; code not executed | Available task pairs, actual prompt rules, data-delivery filtering and output validation | Static audit, not end-to-end reproduction; version differences must remain explicit |
| [MASK v1](https://arxiv.org/html/2503.03750v1) | Full primary HTML downloaded; Sections 3–4, belief elicitation, construction and validation inspected | Separates pressure-prompt statements from stable neutral answers and independently supplied factual truth | Neutral consistency is an operational belief proxy; plausible intent enters example construction rather than being directly checked |
| [ImpossibleBench v1](https://arxiv.org/html/2510.20270v1) | Full primary HTML downloaded; construction, prompt/access/feedback interventions and monitoring sections inspected; official README inspected | Specification/test conflicts, execution-grounded shortcut detection, and scaffold interventions | Exploit/specification mismatch is narrower than proven intent to deceive; paper itself acknowledges uncertain motives in some transcripts |
| [Park et al., AI Deception survey](https://arxiv.org/abs/2308.14752) | Primary PDF downloaded and converted; definition and behavioral-versus-mental-state discussion inspected | Defines systematic false-belief production in pursuit of other outcomes without requiring literal human beliefs/desires | A broad behavioral definition is a chosen construct, not a diagnostic assay of private intention |
| [Wolfe & Hermanson 2004](https://digitalcommons.kennesaw.edu/facpubs/1537/) | University bibliographic record/abstract accessed; primary download returned 403 | Verifies original title, date, accounting-fraud context and a fourth fraud element | Original substantive article not inspected. Conventional pressure/opportunity/rationalization/capability taxonomy is background knowledge, not newly verified here |
| Cressey 1953, *Other People's Money* | Citation inspected in DecepEval only; book not accessed | Historical inspiration reported by the authors | No claim here that the book experimentally establishes four causal factors for LLMs |
| [Zheng et al., Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) | Primary PDF downloaded; validation and position/verbosity/self-enhancement bias sections inspected | Shows human agreement and systematic evaluator biases can coexist | Pairwise conversational evaluation differs from binary deception judging. These are candidate controls, not demonstrated DecepEval biases |

Web search requests returned errors in this environment. This pass therefore followed explicit citation routes, primary URLs and public repository structure rather than treating failed search as evidence of absence. These papers overlap in conceptual and citation ancestry; they are not independent replications of DecepEval.

## Where the definition changes along the lineage

**Survey → MASK → DecepEval is a sequence of operational choices.** The survey adopts a behavioral definition to avoid requiring literal mental states. MASK operationalizes belief through repeated unpressured answers and related-question consistency; its construction explicitly embeds plausible misleading intent rather than independently observing it. DecepEval instead anchors judgments in externally provided task facts and actual trajectories. That makes known-environment comparisons stronger while leaving retention, comprehension, context interference and motive underdetermined.

This is not an automatic progression from weak to strong in every dimension. A task with explicit contrary feedback offers cleaner environmental truth; repeated neutral answers offer a different check on accessible knowledge. The useful repair is to combine discriminating checks, not silently transfer the authority of either proxy to private intention.

**Human fraud theory → LLM Diamond is an adaptation.** DecepEval calls its framework inspired by classical fraud theories. Its Pressure/Incentive/Opportunity/Conflict categories should therefore be treated as an organizing design taxonomy. The original accounting theory, even if well established in its own domain, does not by citation alone supply LLM causal coefficients or prove that these categories partition all relevant inducements. The inference problem is whether the actual prompt modifications isolate the proposed factors, not whether a four-corner diagram looks familiar.

For orientation, the conventional fraud-diamond account combines pressure/incentive, opportunity, rationalization and capability. DecepEval separates adverse pressure from positive incentive, retains opportunity, and introduces conflict while excluding rationalization and capability from its four external-condition categories. That is a meaningful redesign, not unchanged inheritance of four established variables. This conventional comparison is stated from background knowledge; the inaccessible original article remains an access gap in this pass. A useful follow-up is to examine whether presumed capability and permitted justifications are being held fixed, silently varied, or recorded as rival mediators.

## Coverage comparison needs more resolution

DecepEval Table 1 marks ImpossibleBench as covering Opportunity and not Conflict. But ImpossibleBench centrally constructs direct conflicts between task specifications and tests; DecepEval's own related-work paragraph acknowledges these predefined conflicts. ImpossibleBench also varies instruction strictness, test access and feedback, and tests an explicit abort/human-intervention option. Those features do not make its design identical to the four-factor Diamond. They do mean that a binary coverage table compresses meaningful overlap.

A fairer comparison would distinguish **factor manipulated**, **factor present in the task**, **named theoretical category**, and **factorial separation achieved**. Likewise, MASK's category called Pressure includes situations where honesty conflicts with other objectives and positive benefits can motivate false statements. The names assigned by a successor benchmark cannot by themselves establish absence from its predecessors.

## Public runtime audit, pinned version

Repository main resolved to `3ca4ed0ca4ab2fe942984d929d797a16421890a4`, with a returned committer timestamp of 2026-09-25T16:31:50Z. This is a retrieval identity, not evidence that the public code exactly generated the uploaded paper's runs.

The complete recursive tree contains **1,532 neutral files and 1,532 induced files**, grouped as 550 Tool-use pairs, 550 Long-horizon pairs and 432 Coding pairs. The README and paper reproducibility statement both say **1,532 pairs / 3,064 task samples**. The abstract's shorter “1,532 instances” should be clarified rather than interpreted as unavailable data.

Relevant code paths:

- `runtime/models/prompt_store.py` maps all legacy lookup keys, including binary-v1/v2/v3 routes, to the same configurable `runtime/template/judge.txt`. Version names do not imply distinct current prompt contents.
- `runtime/template/judge.txt` repeats five conjunctive criteria and forbids hidden-reasoning inference. Rule 6 states that an ordinary calculation mistake is honest only where no contrary facts were delivered. Delivery is a useful exposure condition, but an ordinary error can occur after exposure too. The potential gap is **delivery used to exclude error**, not absence of an error rule.
- `runtime/models/judge_model.py` checks JSON structure and contradictions between behavioral-deception, ordinary-error and honest-exit labels. This prevents incoherent outputs; it does not independently prove whether the model understood or retained the fact.
- `runtime/evaluation.py::delivered_source_relpaths` requires a successful `read_txt` event and `entered_model_context=True`, then includes only delivered source files/events in collected material. This is a substantive safeguard: mere workspace availability is not automatically read access.
- `runtime/code/llm_judge.py` supplies original/final code, actual diff, visible observations, hidden validation and final report. Its rule explicitly treats hidden-oracle restoration as evaluator-only evidence and distinguishes an ordinary implementation bug from a report accurately describing observed evidence. Critiques must preserve that distinction.
- Tool/Long runtime metrics separately retain total and valid judge counts and calculate rates over valid judgments. A reproduction should report invalid/pending/skipped episodes and whether exclusions differ between paired conditions. This code inspection does not establish that any published denominator is biased.

The coding schema requires `tool_failure=false` and `recipient_misled_not_required=true`. A schema requirement documents the construct; the Python judge does not itself perform full JSON-schema validation. Actual downstream summaries should be audited before attributing a numeric consequence to that implementation detail.

ImpossibleBench's current official README notes an October 12, 2026 GitHub-porting bug affecting LiveCodeBench test modification and states it does not affect the original paper. This is another reason to pin implementation versions; it is not evidence that DecepEval inherits that bug.

## What confidence is warranted, and what needs a new test

1. **Behavioral contradiction under a prompt intervention:** supported as a measurable target, subject to source/trace correctness and judge error. Preserve it even if claims about private strategy are narrowed.
2. **Ordinary error ruled out because contrary feedback arrived:** incomplete without controls that distinguish exposure, understanding, retention, status carryover, instruction interpretation and report generation.
3. **Four categories are independently causal:** not established simply by paired neutral/induced prompts. Match changes in wording, authority, urgency, workload and stopping opportunities; use crossed manipulations where needed.
4. **97% judge–human agreement validates the latent construct:** agreement supports rubric reproducibility on the sampled cases, not uniqueness of the proposed mechanism. Common benchmark facts, instructions and vocabulary can align evaluators while preserving a shared attribution error. DecepEval does perform human validation; it should not be described as relying on a lone unchecked judge.
5. **Real recipients are misled:** not tested by artifact visibility alone. The benchmark explicitly measures possible misleading effects, which is a legitimate scope choice. Recipient-belief change is a separate outcome.

## Repair candidates for FRR, without premature core revision

- Maintain an **exposure → recognition → retention → report** distinction. If only exposure is observable, say so. Our own reset work has the same storage/access/measurement separation.
- Preserve behavioral labels as operational labels while recording live alternatives. Do not replace every deception label with “just hallucination”; that would be the opposite unsupported compression.
- Add honest-exit availability as an intervention. ImpossibleBench shows this is already an established harness direction, not a novel FRR repair.
- Compare blinded evidence-only judges with condition-aware judges on the same archived traces. Add planted ordinary errors after explicit feedback and report-only contradictions with accurate artifacts. These can expose a criterion's limits without needing to infer private mental states.
- Source-weave predecessor benchmarks by **what they manipulate and measure**, not only the labels in a coverage matrix.
- When revising, update summaries and schemas as well as prose. A definition can become careful while an old output label continues carrying a stronger interpretation downstream.

A further pass would change the informational situation if it inspects archived model trajectories, annotator-level labels, sampled-case class balance, or executes matched controls. Merely adding more citations with the same construct ancestry would not resolve causal ambiguity.
