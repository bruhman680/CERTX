# Role switching: executed probe and narrowed gaps

User direction: use the decoherence-to-coherence spectrum across logic, reasoning, and reference as the present working direction. This probe operationalizes a limited numerical analogue; it does not claim one measured semantic spectrum or a general quantum/physical interpretation.

## Executed contact

[Code](../experiments/role_rotation_probe.py), [results](results/role-rotation-probe.json). Twenty seeds, 48 scalar sites, 120 steps; seven policies, three initial conditions, and correct/wrong references: 840 paired constructed runs. These are not 840 AI agents or independent research replications.

EXECUTOR takes a small step toward a known task target with noise. AUDITOR contracts the field toward a supplied reference. Their roles are implemented operations, not labels on language-model agents. References can be correct or inverted. Initial conditions are correct, inverted-but-ordered, or dispersed.

Order proxy: abs(mean(x*target))/mean(abs(x)). This intentionally erases orientation, so correct and inverted consensus can both have order 1. It reads a known task direction and therefore is not a deployable generic reasoning evaluator. It is neither Shannon entropy nor a measurement of chaos. Correctness is separately measured by task mean-squared error and sign accuracy.

Policies: fixed EXECUTOR; scheduled audit; randomly scheduled audit; audit at order>0.9; audit at order<0.6; audit at either extreme; and an oracle target-residual trigger at MSE>0.5. Each has a cap of 24 audits; realized counts differ and are reported. Shared seeds pair noise and initial preparations. No timing/threshold calibration or independent final model evaluation occurred. This is a constructed diagnostic, expanded after inspecting initial outputs.

## What survived and what failed

For dispersed initial states, mean final task MSE:

| Policy | Correct reference | Wrong reference |
|---|---:|---:|
| Fixed executor | 0.1377 | 0.1377 |
| Scheduled audits | 0.0153 | 2.9097 |
| Random audits | 0.0106 | 3.1730 |
| High-order trigger | 0.0622 | 1.1702 |
| Low-order trigger | 0.1045 | 1.5815 |
| Either-extreme trigger | 0.0785 | 0.3491 |
| Oracle residual trigger | 0.0960 | 0.3126 |

These numbers reflect explicitly encoded task and audit maps. Gains with a correct reference do not independently validate the proposed auditing mechanism. The scheduled/random policies also often outperform spectrum triggers when references are correct; the spectrum has not earned an optimality claim. Triggered runs can spend their budget early, while scheduled interventions remain available later. Timing and reference quality are both consequential.

An already correct initial state with a wrong reference has final MSE 0.0855 under fixed execution, versus 2.9097 under scheduled auditing. A low-order-only policy avoids auditing that initially ordered state, yet also fails to recognize an ordered wrong state as a problem. A high-order-only policy triggers for both correct and inverted order. Thus neither end of this scalar spectrum locates factual error by itself.

## Gap status

- **Closed locally:** executable EXECUTOR/AUDITOR switching; high/low-order triggers; fixed/scheduled/random comparators; event records; deliberately wrong-reference control.
- **Narrowed:** a spectrum measures organization, while correction requires a separately warranted reference or discriminating evidence. Reference agreement is not reference validity.
- **Still open here:** semantic coherence metrics; soundness of a derivation; reference provenance/reliability evaluation; WANDERING/thermal intervention; equal realized-cost comparison; learned thresholds; multiscale boundary updates; actual FRR-agent performance.

No need to force all these into one score. For consequential reasoning, retain a small set of distinguishable observations: relation consistency, derivation validity, external evidence agreement, and consequential residual. Ask which changed before choosing a role. A low-entropy correct solution need not be disturbed; a fluent false explanation may require new contact despite high coherence.

## Next discriminating repair

Replace the oracle target with independently generated observations and reference provenance. Test stale, mutually inherited, correct, and adversarial references. Compare evaluation-gated role switching with spectrum-only switching under equal realized intervention counts and task budgets. Include thermal exploration only when it can produce a testable candidate rather than count random movement as progress. Separate calibration and final task cases.

This probe closes an implementation gap and demonstrates a trigger limitation. It does not close general reasoning correctness or establish that role rotation improves FRR.
