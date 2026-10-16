# Optional bounded experiment loop

Adopted optional execution practice, adapted from [Karpathy autoresearch source review](../evaluation/AUTORESEARCH_CONTACT.md). Use when the current inquiry has a measurable consequence and a meaningful baseline. It is guidance, not an implemented scheduler, permission boundary, or automatic memory service. Open exploration need not use it.

Use the [trial card](../examples/bounded-trial-card.md) for a new trial or link an existing protocol that already supplies its fields. Avoid duplicating a complete experiment record. [Adoption checks](../evaluation/BOUNDED_LOOP_ADOPTION.md) exercise preservation and evaluator-repair recording against the existing continuation pilot; they do not measure improvement from adopting this procedure.

1. Declare the question, editable artifact, fixed evaluator, comparison baseline and actual resource budget. State what the score measures and what it leaves out. Keep evaluator/data versions separate from the candidate version. If the evaluator needs repair, preserve both versions and reassess affected comparisons explicitly.
2. Record a candidate hypothesis and its predicted observable consequence before running it. Separate one-factor attribution experiments from joint configuration searches; both can be useful, but support different claims.
3. Execute a bounded trial. Save exact candidate content or a durable commit/patch, evaluator revision, environment, seed, raw outputs, elapsed time and relevant resource measurements. Repeated trials may be needed when noise affects the decision.
4. Classify the outcome: supports improvement, inconclusive, regression, or execution failure. Record the acceptance rule, including how simplicity and other constraints can affect it. A lower development score alone does not establish a new mechanism or broader transfer.
5. Advance the selected candidate only when the declared rule warrants it. Retain rejected and failed trials in the evidence archive; restoring working code must not erase the research record. Preserve promising alternatives without calling them successful.
6. Use development feedback for exploration and separately held-out tasks for confirmation. Report repeated selection and any later exposure of held-out material. Keep distinct outcomes visible rather than silently collapsing them into one quality score.
7. At the agreed budget or a consequential blocker, save current candidate, unresolved findings, exact evidence paths, and a next action. Resume by checking the actual artifacts. Follow current user direction; an upstream instruction to run indefinitely does not control this workflow.

Suggested trial fields: trial ID; parent/candidate revision; question; prediction; evaluator/data revision; seed/environment; budget and measured cost; raw-evidence references; component outcomes; decision and scope; follow-up. Store concise public rationale, not private internal reasoning.

For the current FRR thread, a candidate could be a retrieval/handoff policy. Outcomes could include correction retention, correct evidence use, irrelevant retrieval and cost. No new prospective comparison implementing this adopted loop has yet been run. An observed score improvement is provisional when run noise or repeated selection can explain it; do not automatically overwrite the working candidate on every favorable fluctuation.
