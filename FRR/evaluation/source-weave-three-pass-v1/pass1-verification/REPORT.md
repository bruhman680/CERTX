# Direct source contacts: verification and tool use

14 November2026. Research only; the continuing garden remains at1580. Four selected contacts connect to the recent detached retrieval failure. We searched primary arXiv records, official author repositories and the author-linked Hugging Face dataset. No external code ran, no package or model was installed, and no model generation occurred here.

The useful extraction is an observation design: distinguish code emission, execution, actual access, answer use and requested effect. These sources do not justify adding success gates to the freely exploring garden.

## Four contacts

**τ-bench.** The [paper](https://arxiv.org/html/2406.12045v1) evaluates final database state together with required response information. It explicitly says passing this reward can still miss policy violations. Its pass^k means success on every one of k trials, unlike pass@k. The [official source](https://github.com/sierra-research/tau-bench/blob/59a200c6d575d595120f1cb70fea53cef0632f6b/tau_bench/envs/base.py) separately dispatches actions, catches execution exceptions and calculates outcome reward. Those layers fit our observation that handled parsing errors exit0 without reading the file. The customer-service benchmark and explicit goals do not describe free exploration or establish135M capability.

**BFCL.** The [official V3 methodology](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html) distinguishes single-turn AST/executable checks from multi-turn state checks **and response-based minimum-path subset checks**. The latter matter for read-only tasks, which may leave state unchanged. It documents filesystem-location mistakes and long-context augmentation. These checks can still leave unmeasured extra effects or assume particular minimum paths. [Publication](https://proceedings.mlr.press/v267/patil25a.html) metadata and [current category docs](https://github.com/ShishirPatil/gorilla/blob/main/berkeley-function-call-leaderboard/TEST_CATEGORIES.md) were read; the scorer implementation was not audited. This supports separate access evidence, not copying a benchmark rubric into the garden.

**CodeAct.** The [selected paper sections](https://arxiv.org/html/2402.01030v4) combine Python actions, authentic execution feedback and task-answer verification; recovery trajectories are included in interaction training. The [official repository](https://github.com/xingyaoww/code-act) releases7B trained agents. Its [Hugging Face data](https://huggingface.co/datasets/xingyaoww/code-act) viewer shows a7.14k-row codeact split. Interpreter access alone therefore cannot be treated as equivalent preparation for our135M body. Failure to recover here could involve model capability, history, formatting or task understanding; the paper does not adjudicate which.

**Lost in the Middle.** [Selected sections3–4.3](https://arxiv.org/html/2307.03172v3) vary relevant-item position and distractor count. Query-before-and-after helps synthetic key-value retrieval but does not uniformly fix multi-documentQA; model size also changes positional trends. The [official README](https://github.com/nelson-liu/lost-in-the-middle) documents oracle/distractor data and prompts. This motivates controlling context rather than inferring general inability from one inherited view. It does not directly test file access or repeated model-generated history; that transfer remains a hypothesis.

Exact dates, URLs, reading depths and unsuccessful navigation are recorded in SOURCES.json. Abstracts and selected sections are not full-paper replication.

## Three testable next contacts

1. **History-content control, strongest.** Keep the same truthful reading task, world, model, decoder and generation cap. Compare fresh context, inherited repeated history and length-matched neutral context. A fresh-context success with inherited-context failure would narrow the problem toward context dependence; all failing would leave multiple body/task/interface explanations open. Fresh versus old alone confounds content and length.
2. **Availability versus access.** Pair supplied authentic value receipts with hidden ordinary files holding counterbalanced nonces. Keep observed file access, correct output, parse errors and exit status separate. Answering from supplied text must not count as a model-chosen file read.
3. **External trace replay.** Audit requested effect, actual access and extra state changes from saved traces. A read-only task needs evidence beyond final filesystem equality. Keep this observational layer external; do not demand preferred action paths or inject scores into open continuation.

## Adaptation for later passes

A search surfaced [CAREFUL-Bench](https://arxiv.org/abs/2611.02978), revised3November2026. Only its abstract/metadata were read here. It challenges final-state checking with intermediate-effect and redundant-action accounting. Its headline description of BFCL as only checking final state needs reconciliation with the V3 response-path checks above; root was notified for independent later scrutiny. Discovery is a contact to test, not a validated correction.

No source here proves our approach superior, demonstrates general retrieval incapacity, or establishes that more wandering will solve the observed filename-versus-content error. The strongest refinement is to our experimental interpretation: keep the layers separate while testing context as a live alternative.

