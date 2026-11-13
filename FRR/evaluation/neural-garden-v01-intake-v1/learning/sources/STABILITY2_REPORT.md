# STABILITY2 — keeping the learner close to what already works

**Evidence status:** One completed substantive research loop, with exploratory setup check and independent reserved holdout. This is a synthetic mechanism test, not evidence of autonomous metacognition or open-ended intelligence.

## Predeclared question and control

Can simple per-cell Euclidean trust regions around transferred trained weights prevent harmful continued stochastic updating? `STABILITY2_PLAN.md` was written before results, with `STABILITY2_probe.py` specifying six matched policies. Every seed uses the same trained neural parameters, initial energy/resource, random action stream, and regrowth .060/.055/.060 across three 1000-tick periods. All learning arms make stochastic decisions. Only per-cell parameter displacement after each ordinary optimizer update differs. Neural controllers remain individual; no network architecture change.

Eight development seeds 10300–10307 and **eight previously reserved unseen holdout seeds 10400–10407**; 10×10 worlds, 1000 pretraining ticks, 3000 test ticks, 96 total 3000-tick policy trajectories. Smoke tests are not in these counts.

| Policy | Development mean energy | Holdout mean energy | Development floor | Holdout floor | Holdout wins vs frozen |
|:--|--:|--:|--:|--:|--:|
| Frozen weights, stochastic actions | .05169 | .04895 | 13.13% | 14.38% | — |
| Unrestricted online updates | .03696 | .03718 | 19.88% | 18.88% | 0/8 |
| Online updates, radius .025 | .05035 | .04754 | 13.63% | 14.50% | 0/8 |
| Online updates, radius .10 | .04617 | .04404 | 13.38% | 15.50% | 0/8 |
| Online updates, radius .40 | .03981 | .03902 | 16.88% | 17.00% | 0/8 |
| Online updates, radius 1.0 | .03744 | .03771 | 18.50% | 18.25% | 0/8 |

The tightest trust region beats unrestricted updating on **8/8 development and 8/8 holdout seeds**, recovering most of the lost energy, but it does **not** beat simply freezing the same transferred trained weights on **any** seed. Holdout per-cell average distance from transferred parameters: .016 for radius .025, .075 for radius .1, .221 for radius .4, .289 unrestricted.

## Interpretation

The result strongly supports **parameter drift as a local failure mechanism** for this specific learning rule: smaller post-update displacements are associated with less ecological harm under otherwise matched physical initialization. This does **not** prove that learning itself is useful, adaptive, or self-regulated. Bounding updates is a designer constraint and nearly freezing a competent policy is a powerful baseline. It is important that a near-zero radius cannot be counted as a new learned capability.

The plan listed a zero-centered clipping sham; the source does not execute it, because projecting onto a sphere around zero would discard pretraining and would not be a meaningful same-information control. This planned but unexecuted arm remains explicitly acknowledged. The frozen and unrestricted modes are the stronger causal comparators.

## Next evidential pressure

Search for a regime where updating can **exceed**, rather than just approach, a competent frozen controller. Test a genuine shift that makes transferred strategies fail, with explicitly measured detection delays, observation-only signal gates, and negative controls for sham gating. Crucially, any claim of *learning when to learn* requires the gate to depend on observations, not a designer oracle or absolute timestamp.

Raw per-seed metrics, source fingerprints and source: `STABILITY2_results.json`, `STABILITY2_holdout_results.json`, `STABILITY2_probe.py`.
