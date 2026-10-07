# Experiments 01: scalar optimizer audit reproduction

Executed locally on 2026-10-07. Scope is the supplied standard-library scalar recurrence, not GammaCAdam training, tensor implementation, or empirical generalization. Original files were preserved; executions used an isolated byte-identical copy. No downloads, credentials, remote writes, or agents were used.

## Evidence and actual execution

Read shared NOW.md; FRR v0.5 Compact Runtime Seed; RECOVERY_NOTE.md; October 5 field-wakes note optimizer section; gamma_c_optimizer_audit.py; CONTINUATION_HANDOFF.md and RECOVERED_CODEX_HISTORY.md. NOW explicitly supersedes historical intake pauses. Source snapshot ancestry is shared: this reproduction is not independent empirical replication. Batch 1, batch 2, and executed audit copy have identical SHA-256 `bbf5a29e2d5f0617bb62ee704e767bfc78b46050ed96f3282e9265016bba80db`.

Command (exit 0):

```sh
python /workspace/frr-distributed-2026-10-07/outputs/experiments-01/gamma_c_optimizer_audit.py
```

Full stdout is in the sibling output directory, `audit.stdout.txt`. Key observed values:

| Sequence | S | Retention 1-eta*decay |
|---|---:|---:|
| 10,000 zeros then one | 9.999448728298962 | -455.5550811999983 |
| 10,000 alternating signs | .0027700830747922375 | .9999963007678941 |
| 10,000 ones | .9999999899999975 | .9999794517211472 |

Spike eta=.00025608070274898905, decay=1782856.249217321. Thus the claimed bounded-in-[0,1] score and safe shrinkage fail under the mathematical defaults. A nonzero weight's multiplicative decay component flips and amplifies; this is not a demonstration of an entire training trajectory diverging.

Quadratics with curvature 1, 10, 1000, and 1,000,000 produce gradient/weight proxies approximately .99999999 at weight 1 by choosing their centers appropriately. Hence this proxy cannot distinguish these curvatures. The printed GD threshold comparison is a heuristic witness of missing curvature information, not an Adam stability theorem.

## Surviving relationship and serious rival

Gradient history changes moments and therefore later update rules even at the same current gradient and weight. This is a valid domain-local relational silhouette; whether moments are an external field depends on the declared system boundary. It does not establish material persistence, universal criticality, or useful optimizer performance.

The serious rival is ordinary exponential moving-average lag mismatch: differing beta timescales explain the high ratio without crystallization or curvature. Typical gradients might never realize the constructed spike; that could preserve practical usefulness but cannot rescue a universal guarantee. Clipping alone would still leave curvature inference and functional neighbor geometry unvalidated.

## Precision improvement, implemented reversibly

Do not equate “outside [0,1]” with “mathematically unbounded for the fixed defaults.” Added isolated `fixed_beta_bound.py`, executed with Python (exit 0), stdout in `bound.stdout.txt`. For bias-corrected positive weights a_i on gradients and b_i on squared gradients, Cauchy-Schwarz gives S <= sum(a_i^2/b_i), since eps >= 0. Here a_i=(1-beta1)beta1^(t-i)/(1-beta1^t), and b_i=(1-beta2)beta2^(t-i)/(1-beta2^t). With beta1^2 < beta2, the geometric-series envelope has finite asymptotic value 52.8571428571428; at t=10,000 it is 52.854755123141146. The bias-correction factor is bounded over positive integer t, so the fixed-default recurrence has a finite global envelope. This calculation is supplementary analysis, not recovered historical evidence or an optimizer repair. It corrects the broad “unbounded moment ratio” phrase in NOW without changing the unsafe retention conclusion.

Recommended reversible next step: change downstream wording to “not bounded in the asserted [0,1] interval”; if optimizer exploration resumes, prototype separately a declared bounded signal and explicit 0<=eta*decay<1 guard before matched-budget controls. No repair is implemented here. Keep broader field/context/play branches open; this audit does not supersede them.

## Provenance and limits

Inputs live under `/workspace/recovered-originals/2026-10-05/` and are normalized recovered artifacts; their recovery note explicitly distinguishes executable source from prior results. FRR supplies evidential discipline, not additional measurements. Context handoff/history supplies lineage only. I did not inspect or execute the missing original optimizer, test the tensor API issue, reproduce diffusion behavior, or consult remote documentation. The auxiliary bound is this worker's transparent new calculation. All artifacts are removable without modifying historical input.
