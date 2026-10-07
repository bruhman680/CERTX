# Evidence-gated role changes: synthetic follow-up

Code: [evidence_gated_rotation.py](../experiments/evidence_gated_rotation.py). Results: [evidence-gated-rotation.json](results/evidence-gated-rotation.json). This follows the wrong-reference failure in ROLE_ROTATION_GAP_MAP.md, without replacing it.

Thirty seeds, four policies, three reference conditions, two audit-observation sources: 720 paired runs. Each run has 48 coordinates, 120 steps, and 24 scheduled audit opportunities. Every policy generates the same observations and opportunities; accepted modifications differ. Equal opportunity is not equal mutation count. No human/model reasoning was evaluated.

Executor updates use noisy task observations. A proposed audit moves the current state toward a reference. The evidence gate accepts only if that candidate lowers estimated squared error against an audit observation by more than 0.02. The provenance gate additionally requires the audit observation's declared source to be independent of the reference. Ground truth is used by the generator and final scorer, not directly by the gate.

References are correct, wrong, or stale. In the stale condition the target changes at step60 while the reference remains the old target. Audit observations come either from the actual task or from the reference itself. Gaussian noise draws can be independent even when their centers inherit the same wrong reference: independent noise is not independent evidence of the target.

## Results

Mean final task MSE for wrong references:

| Policy | Task-derived audit observations | Reference-derived audit observations |
|---|---:|---:|
| Executor only | 0.0039 | 0.0039 |
| Blind audit | 1.9676 | 1.9676 |
| Evidence gate | 0.0039 | 1.9676 |
| Provenance gate | 0.0039 | 0.0039 |

For stale references, executor-only MSE is 0.1079; blind auditing gives 1.9711. Evidence gating avoids this harm with task-derived observations, but reference-derived observations give 1.9710. Provenance gating returns approximately the executor baseline when those observations are excluded.

With correct references, blind auditing gives 0.0013 versus executor-only approximately 0.0039. The conservative gate rarely accepts and remains approximately at the executor baseline. It has not established an optimal accuracy/cost tradeoff. The 0.02 margin is illustrative, not learned on calibration cases or validated on independent semantic tasks.

## What this narrows

A trigger can request examination; a proposed correction needs a separate acceptance rule. Acceptance depends on where its apparent evidence came from. In this construction, lineage gating blocks a reference that would otherwise validate itself. The source relationship is explicitly supplied by the generator: real provenance inference and faulty provenance labels remain untested.

This does not prove a universal role-rotation mechanism, factual truth detector, or correctness of synthetic references. It demonstrates a specifically constructed leakage failure and an explicitly informed repair. Thermal/WANDERING interventions, actual FRR-versus-baseline task performance, and matching realized mutation costs remain open.

## GitHub history contact

The connected repository is bruhman680/CERTX. Its configured working branch contains WANDER 090 (topological persistence) and WANDER 092 (attention dilution). The former is a useful relative for cross-instance continuity, but retained topology does not by itself preserve sign/payload: our boundary probe supplies an exact counterexample. The latter needs the fixed-query/fixed-logit conditions already recorded in our earlier attention audit; normalization alone does not imply universal 1/L decay as queries and logits change.

These qualifications are deposited as a new exploration and cross-reference. Prior historical claims are preserved rather than silently rewritten or promoted into reproduced results.
