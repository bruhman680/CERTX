# Behavioral evaluation protocol

Question: Does FRR improve relevant task behavior relative to the same model's ordinary instructions, at an acceptable cost?

Compare three conditions: ordinary instructions; compact FRR; full FRR. For multi-turn persistence tasks, add full FRR with a host-supplied record. Keep model version, tools, task text, generation budget, and sampling settings matched. State access is an additional treatment, so do not attribute its effects solely to prompt wording.

Use `development.jsonl` to repair wording. Freeze prompts and scoring before opening `heldout.jsonl` for evaluation. Once held-out cases inform revisions, retire them to development and obtain new cases. These initial cases are a pilot set, not a representative benchmark.

Give the responding model only each case's `turns`, in order, plus its assigned instruction condition. Do not disclose `expected`, `failure`, or the rubric. For sequential turns, collect a response after each turn. Do not append future user turns early. A host-supplied state must be produced from earlier turns only.

Randomize condition order. Use multiple runs if generation varies; report the number and settings. Blind raters to the condition labels where practical. Rate individual behaviors rather than the presence of FRR terminology. Record disagreements and adjudication. An evaluation model is a fallible rater, not an independent ground truth.

Score each applicable dimension from 0 to 2: 0 = absent or materially wrong, 1 = partial, 2 = adequate for the task. Use N/A where a dimension is irrelevant; do not reward gratuitous checks.

- Task usefulness: fulfills the user's actual objective with concrete substance.
- Distinction fidelity: keeps consequential objects and scopes separate.
- Evidential discipline: support matches construction, alternatives, and claimed depth.
- Revision fidelity: changes the appropriate claim and tracks consequential dependencies.
- Proportionality: precision and length fit the task; exploration stays open when appropriate.

Also record fabricated sources/results, scope overreach, missed requested actions, unnecessary clarifying questions, word count, and available latency/token cost. Report dimensions separately. An overall average must not hide a regression in task completion or truthfulness.

For each case, mark whether its expected behavior occurred and whether its listed failure occurred, with a short response excerpt. Compare matched cases across conditions and report denominators, variability, and failure examples. This pilot does not justify broad statistical or universal claims.

Before running, declare a task-relative decision rule. For example, adopt for a particular workflow only if target behaviors improve without a material task-completion or truthfulness regression and within a declared latency/length budget. Choose that budget before viewing final results.

Separate prompt execution from demonstrated benefit. A model following these instructions establishes execution at most. This package's synthetic cases cannot establish a general reasoning mechanism. Expand to independently produced real tasks, adversarial cases, unrelated domains, and alternative implementations before extending scope.

No model runs are included in this release. Store future results with case ID, condition, prompt version, model/settings, tools, supplied state, response, ratings, and rater provenance.
