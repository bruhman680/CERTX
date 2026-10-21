# Optional evidence-gated feedback procedure

Candidate synthesis from [PID-C1](../evaluation/pid-contact-v1/REPORT.md), prior wrong-reference experiments and correction-preserving handoffs. Not a core FRR revision, implemented autonomous controller or demonstrated reasoning improvement. PID-C1 tests controller mechanics, not this procedure on model reasoning. Related established work includes feedback control and [metareasoning](https://people.eecs.berkeley.edu/~russell/papers/mitecs-metareasoning.pdf).

Use for an inquiry where a mismatch may require action. The goal is useful correction with bounded effort; neither agreement nor permanent uncertainty is the target.

1. **Orient.** Record the current question, relevant distinction, task success condition and resource bound. Locate the current claim and its source/version. Mark what is unresolved rather than treating all uncertainty as error.
2. **Check the feedback.** Ask whether the observation measures the intended outcome and whether the reference is authoritative for this scope. Identify stale summaries, inherited assumptions and shared-source dependence. If the check is unavailable, keep the uncertainty explicit; do not silently certify provenance.
3. **Select a discriminating move.** Choose a source check, calculation, rival construction, retrieval or bounded test whose possible outcomes could change the decision. Say what would differ under the rivals. Use a simple cost/benefit rationale; do not pretend expected information gain is calibrated when it is not.
4. **Bound intervention pressure.** Track unresolved persistence separately from belief confidence. Repeating the same evidence does not increase its independence. If action is saturated by missing inputs, permission, budget or unavailable measurement, pause accumulation of urgency and record the blocker. Do not merely rerun an identical unsuccessful move without a changed reason. Rebase trend/persistence bookkeeping when the goal or measurement changes; preserve its history.
5. **Gate the update.** Check the proposed correction against task-relevant evidence and plausible alternatives. Accept when the warrant suffices for the decision, retain scope/uncertainty and permit justified reversal. Independent observation noise alone does not make a shared inherited reference independent evidence. Do not require impossible certainty to close a settled task.
6. **Preserve and decide.** Record the previous claim, new status, evidence, reason for change and remaining question. Continue if another affordable discriminating action is available; otherwise finish, pause with a specific reopening condition, or request the missing input. A broad framework can prompt a check, but it does not guarantee an error will be recognized.

Minimal executable-by-a-person/agent procedure:

```text
until the stated decision is warranted or the resource bound is reached:
    inspect the discrepancy and feedback provenance
    choose an affordable action that can distinguish consequential alternatives
    if no such action is available:
        record the unresolved distinction and what would reopen it; pause
    collect/check the action's result
    accept, reject or narrow the proposed update using the evidence
    preserve the old claim, new status and source/version
return current warranted result plus its practical limits
```

This is a scheduling and acceptance procedure. Its investigations need domain-specific reasoning. Where a calibrated numeric process exists, P can regulate present mismatch, I persistent mismatch and filtered D its trend, with explicit actuator/budget limits. In free-form reasoning, these remain scheduling analogies: a confidence score is not a temperature, a contradiction count is not a calibrated error signal, and more textual repetition is not integral evidence. No gains or universal role-rotation/entropy thresholds are adopted.

To test value rather than appeal, compare against ordinary review and a simpler provenance-only procedure on separately authored held-out tasks under matched budgets. Include wrong references, stale but coherent summaries, correct noisy observations and genuine new evidence. Score grounded decisions, justified changes, unnecessary interventions and cost separately. Prefer the simpler procedure if outcomes are comparable. Until that test, this module is optional and provisional.

Further diagnostic guide: [ES-C1](../evaluation/error-success-contact/REPORT.md) separates premises, inference, measurement, objectives, actions and outcome luck before increasing correction. This is conceptual refinement with exact counterexamples, not a new efficacy result.
