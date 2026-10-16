# Optional artifact execution harness

Source: user's screenshot of a Karpathy-inspired long-task prompt. Attribution and efficacy are unverified. This module adopts selected execution practices; it does not alter core FRR or create a running service.

Use for a bounded artifact task when observable completion checks help. Do not impose a completion checklist on open play.

1. Inspect current instructions, artifacts, and saved state. Define the requested output and observable acceptance checks before consequential edits. Establish a relevant baseline when comparison is needed.
2. Take a bounded step within the authorized scope. Preserve recoverable versions before risky changes. Run checks against the actual saved artifact and retain useful improvements and failed-attempt evidence.
3. Before retrying an interrupted external write, inspect the remote state to determine whether the first attempt succeeded. Record confirmed success separately from attempted actions.
4. Separate construction and review when useful. Supply a reviewer requirements, artifacts, and evidence references; document exposure/shared inputs if independence matters. A distinct review is useful without being independent replication.
5. Leave a concrete continuation record: current purpose/constraints, exact artifact paths, completed checks and evidence, consequential decisions, unresolved failures/blockers, and one next action. On resumption inspect referenced artifacts rather than trusting the summary alone.
6. At delivery state what was checked, what passed, what remains unresolved, and where the record is saved. Preserve historical versions and update downstream current-status references when consequential.

FRR supplies the inquiry orientation, artifact pressure, scope discipline, and recoverable revision. This optional harness makes some of those obligations operational for bounded execution. A prompt alone cannot grant storage, tools, runtime control, verification, or durable memory. No efficacy claim is made for the screenshot or this module.

For an actual comparison, use the adopted [bounded experiment loop](bounded-experiment-loop.md): isolate candidate and evaluator versions, preserve unsuccessful trials before rollback, and keep development selection separate from confirmation. The [trial card](../examples/bounded-trial-card.md) can reference an existing protocol rather than duplicate it. This addition comes from inspection of the actual autoresearch repository, not verification of the screenshot's attribution.
