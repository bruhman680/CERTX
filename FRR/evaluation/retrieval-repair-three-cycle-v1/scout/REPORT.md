# Feedback can be available without becoming a repair

15 November2026 UTC. Small read-only scout during the main continuation. Three primary papers, all version-pinned at arXiv v2. Zero model calls, sandbox actions, installs or external code execution. This scout changes no garden files or rules. Selected HTML sections were read; this is not a full-paper or implementation audit. `SOURCES.json` records the precise scope.

## What the papers actually add

**Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet, 2310.01798v2.** Its central experiment concerns intrinsic correction without external feedback, using much larger models on reasoning benchmarks. The paper also distinguishes oracle-guided stopping, calls for comparable inference budgets, and shows that giving fuller instructions initially can outperform putting that information only in a later correction prompt. This does not directly test our receipt-conditioned135M program repair: our real errors and operator hints are external information. Its applicable contribution is experimental design, not a theorem explaining our six failures. [Versioned paper, especially §§2–3,5–7](https://arxiv.org/html/2310.01798v2).

**Chen et al., Teaching Large Language Models to Self-Debug, 2304.05128v2.** This is a positive counterexample to universal pessimism. Its procedure combines candidate code, prompted explanation/feedback, and, where available, execution of unit tests. The experiments use Codex, GPT models and StarCoder, with task-specific prompting and larger debugging budgets. Execution ablations show that feedback availability and procedure matter. Importantly, the paper's generated explanation traces are model-produced text, not captured intermediate execution states. We did not run this full method or its few-shot demonstrations. It therefore motivates a possible controlled diagnostic, not a demonstrated repair for our body. [Versioned paper, §§3–4,5.2.2](https://arxiv.org/html/2304.05128v2).

**Madaan et al., Self-Refine, 2303.17651v2.** This paper reports improvements from explicit feedback/refine prompting without additional weight training. Its weaker-model analysis is unusually relevant: Vicuna-13B can generate initial outputs but struggles with refinement, sometimes repeating earlier output or producing fabricated conversation even with oracle/hard-coded feedback. AppendixG gives an example of copying prompt content. The proposed explanation in terms of conversational training is a hypothesis, not an established causal mechanism. Vicuna-13B is still vastly larger and differently trained than our135M model. The close observation is a failure-pattern analogy, not a replication or model-size law. [Versioned paper, §4 and AppendixG](https://arxiv.org/html/2303.17651v2).

## Tie to the six local attempts

The completed local experiment supplies three actual-feedback branches and three independently matched branches with explicit operator corrections. All six miss the requested field value in stdout. Paired execution of their unchanged artifacts on B worlds also misses it. The labels below come from local raw tokens and receipts, not the papers:

- Coached wrong-path and parser-input cases exactly reproduce their prior failed generated token sequences.
- The uncoached incomplete-fence case also exactly repeats its prior generated tokens.
- Other outputs change introductory/trailing text. One actual-feedback branch replaces an unused helper key with `boundary`, reflecting receipt vocabulary, while the executed main still opens `/world.json`.
- There is no corrected executable effect. A changed sentence or recognition-like explanation does not establish repair.

These facts support a distinction between **available feedback**, **changed generation**, **correct procedure selection**, and **verified effect**. They do not reveal whether the model internally understood, ignored, attended to or emotionally reacted to feedback. No weights changed, and no durable learning is demonstrated.

The source comparison also prevents two overclaims: our failure with external hints does not prove all intrinsic correction impossible; successful external-feedback methods on larger models do not guarantee that giving any receipt to any smaller model will suffice.

## Strongest small next contact, if later pursued

Use one failed task and declare three one-reply conditions before outputs:

1. Original task plus failed assistant reply plus real error receipt.
2. The same history and receipt plus the existing explicit correction.
3. Fresh framing with the same task and the same correction supplied initially, without the failed assistant example.

This separates the usefulness of correction information from its use after a failed example. It still changes history length and position, so it initially tests presentation dependence, not a unique mechanism. Retain an unchanged-body budget and all failures. If a stronger claim about repair versus extra attempts is desired, add a budget-matched fresh retry baseline; do not count repeated deterministic inputs as independent discovery samples.

One further diagnostic could separate code generation from source explanation, as the positive debugging source does. That should be a declared new condition rather than silently making the model produce more narrative or replacing its own code with an observer's fix. Complete-fence status, actual read/extraction, wrong-path/type errors, exact-value formatting and paired artifact dependence remain separate outcomes.

Nothing in this scout recommends importing these hints or procedures into the main open garden. The main's newly authorized bounded-view continuity repair addresses a demonstrated context-capacity boundary. It is independent of whether these retrieval attempts learned or improved.

## What remains unverified

No cited code was run or audited, no reported benchmark number was replicated, and no small135M feedback method was established. Selected HTML may omit figures or layout details. Model, task, prompt, stopping rule and generation budgets differ substantially. The papers do not identify the causal mechanism of our exact repeated errors; they provide controls and contrasting observations with which to avoid premature explanations.
