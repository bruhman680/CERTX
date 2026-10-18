# Proposed HG1 reader packet contract, version 0.1

Design preparation only; no behavioral launch. Six explicitly requested agent reviews informed this contract. Reviewers shared parent context and filesystem and are not independent experimental subjects.

A reader receives an anonymous trial ID, exact normalized final handoff, continuation update, common instructions, and any explicitly declared task-definition shell. Save the actual serialized packet and its hash. Preserve the original handoff and transformation record. Keys and other actor outputs are not assigned reader inputs; shared filesystem access remains a limitation unless isolation is actually enforced.

Before launch choose one policy for all arms: require task rules to survive in handoffs, or supply a common neutral task-definition shell. The present scheduling updates do not independently supply all original rules: worker count, integer start times and nonpreemption must be accounted for. Supplying these only to an evaluator would create an unfair omniscient score. Do not silently add case-specific evidence in a shell.

Proposed response fields: status (answered, partial, insufficient_evidence, conflicting_evidence), answer, support, missing_or_conflicting, conditional_assumptions. Freeze exact schema and tolerances before behavioral execution. Preserve malformed raw answers rather than silently repairing them.

Score source truth and packet warrant separately. A corrupted but internally consistent handoff can support locally valid arithmetic that is wrong against the original source. Record writer corruption and objective error without automatically assigning the false premise to reader invention. Honest abstention can be appropriate and still leave the task incomplete. A lucky correct guess does not establish grounded completion.

Sufficiency concerns information, not a primitive-field checklist:

- WEIGHT-1 group rates A (.9,.6), B (.8,.5) support equal-weight results .75 and .65 without original counts. Pooled .63 and .77 alone do not.
- LINEAR-2 a+c=19-2b suffices with b=3 to obtain 13; original equations need not be copied.
- LINEAR-1 a-c=-2 alone does not recover a,c,total after b=4.
- FORECAST old aggregate Brier scores alone do not generally support recomputing changed labels; ordered probabilities or equivalent sufficient information can.
- SCHED accept any feasible optimal schedule in the declared domain, not only the answer key's witness.

Adjudicators need the actual reader packet and original-source truth in separate fields. They must distinguish original underdetermination, writer omission/corruption, reader inference error, update error, and evaluator error. Semantic sufficiency needs checked derivations or adjudication; file presence alone cannot establish it.
