# Optional carried exploration protocol

Use external append-only notebooks to make trajectory persistence explicit. A frozen model with fresh caches does not automatically remember prior calls; include the declared history in its input and save every version. Preserve old outputs, observations, actual feedback, RNGseeds, checkpoint identity and scheduled external changes.

Allow public answers, uncertainty, questions or notes without requiring every run to produce an improvement. Separate unscored activity from recognized task errors. Preserve whole batches, not only interesting excerpts or successful endpoints. Repeated behavior and quiet tails are observations, not proof of crystallization or an intrinsic plateau.

Matched latest-event replay controls can test the contribution of older history at identical current evidence/last feedback, but differ in context length and are not independently evolving agents. Use further controls before attributing a change specifically to learning from failure. Model self-explanations remain outputs, not access to internal reasoning.

Resource bounds apply to execution; exploration need not predefine every possible public strategy. Log limits rather than silently truncate/prune history. More action space, tool use, altered prompts or checkpoints must be explicit experimental branches. No generated text should silently rewrite the evaluator, history or task contract.

Evidence: [first bounded season](../evaluation/carried-garden-exploration-v1/REPORT.md). This is an optional research harness, not a validated general emergence engine or default production policy.
