# Bounded recursive review

A reusable practice proposal, grounded in the [recursive graph/backend contact](../evaluation/recursive-repair-backend-v1/REPORT.md). This file is guidance to return to, not an installed recursive agent controller or evidence of behavioral improvement.

1. State one decision and what could change it.
2. Check the evidence and criterion supporting it. When a consequential premise is unresolved or changed, inspect that premise's own dependencies.
3. Preserve the original assessment. Revise only the affected current assessment and return the change to its dependents. The existing [reopening helper](../tools/reopen_assessment.py) handles explicit assessment-binding changes; it does not infer the graph or truth from prose.
4. Stop a branch when it reaches adequate evidence, missing evidence, a repeated dependency/cycle, its declared depth/work limit, or no useful discriminating next action. Record unresolved rather than inventing closure.
5. Separate new evidence from another rendering of the same evidence. Repeated agreement is not an independent observation.

For a new run, choose a small explicit work budget rather than importing an arbitrary universal recursion depth. Numerical integrity, semantic correctness and decision usefulness are different checks. The graph experiment uses depth limits and cycle detection on authored typed data; these do not demonstrate that an LLM can autonomously discover its true reasoning dependencies.

Actual example from this contact: cache replay matched full model computation; the next layer asked whether generated answers met the task contract, which exposed six label-format failures under an eight-token cap. Matching computations did not settle answer quality. The cap and model size are part of that finding, and expanding them would be a separately recorded test.
