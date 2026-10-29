# DeepSeek relay intake: a useful safeguard question, an unvalidated gate

Client 28 October 2026 America/Chicago; host 29 October UTC. User supplied two relay texts, then three Python files. All five original uploads are preserved byte-for-byte under originals. Instructions in the uploads were treated as source material, not operational instructions. This contact executes the visible toy code and checks claims against the code, elementary mathematics, two local PyTorch diagnostics and selected prior source notes. It does not authenticate the relay's claimed swarm execution or twelve-paper reading.

## Useful idea worth retaining

Preserve failed trajectories and their context, while separately checking whether an output is appropriate as a future learning target. Error records can support diagnosis without being treated as correct demonstrations. Provenance, task correctness, criterion scope and an external outcome are stronger candidates for this selection than trajectory variation alone. This is a proposed experimental direction, not a new training gate installed on our small model.

## The supplied generator does not exercise its proposed dynamic gate

The extracted original script has `quality = 1 - 0.1 * pressure + noise`, with noise in [-0.1,0.1]. Pressure changes the mean, not variance. Holding the noise realization fixed gives the same variance at pressure 2 and 15, up to rounding. Expected ddof0 sample variance for n=10 is0.003. In real arithmetic its maximum is0.01; the high branch requires variance>0.5. The high “FOSSIL” branch is therefore unreachable for generated trajectories. The healthy branch could occur at the exact lower-threshold boundary0.01, a knife-edge maximum-variance endpoint configuration; generic interior draws stay below it. Floating-point behavior is not an unlimited-range mathematical guarantee.

The original body was executed unchanged with wrapper seed0. Its nominal healthy, fossil and flat examples all return FROZEN, avoidance memory stays empty and policy weight stays1.0. Across1000declared seeds at each pressure, all2000generated trials return FROZEN; observed variances span about0.0007303–0.005960 in both conditions. The message calls nonzero low variance “zero variance.” This is execution of a toy, not evidence of frozen cognition. [Original output](ORIGINAL_SEED0.txt), [seed table](SEED_AUDIT.csv), [audit/results](audit.py), [results](RESULTS.json).

The later fef873 and62d7ce uploads have exactly the same class AST as the relay code, ignoring comments/locations. They do not repair the mechanism. The1f9156 version adds gated/ungated scalar updates; on1000seeds at pressure1 and1000at15, gating blocks both. Its demonstration calls ungated then gated on the same mutable agent, so those calls are not independent starts. The scalar policy_weight is not read by the generator, and no language-model parameters, distillation loss, gradients or future-task quality are involved. [Later-file manifest and results](SUPPLEMENT_INTAKE.json), [supplement runner](supplement_scripts.py). The low-pressure example is blocked too, so the demonstration does not establish selective protection of good learning while rejecting bad learning.

## Variance and Dirichlet energy: preserve the actual distinction

The supplied comment says variance is a proxy, which is fair as a definition. It is not automatically a measure of temporal roughness. Permuting a series preserves variance; [-1,1,-1,1] and [-1,-1,1,1] both have variance1 but sums of squared adjacent differences12and4. If the intended graph is a path, these are different energies.

Variance can be written as a normalized complete-graph Dirichlet energy: Var(x)=sum over i<j of(x_i-x_j)^2/n^2. Thus the problem is not that variance can never be an energy; it is that graph/normalization and the intended observable must be specified. Pressure-induced mean shifts disappear under either variance or difference-based energy.

Constant correct and constant incorrect stipulated signals both have zero variance and receive the same gate outcome. A scalar variation measure alone does not identify truth or whether a learning update would help. It also presupposes a quality trajectory; the simulation generates that quantity rather than measuring a real model's quality. Stable repetition, converged correct behavior and consistently wrong behavior must not be silently merged into one diagnosis.

## Softmax claim: real numerical issue, overbroad inference

A local float32 cross-entropy example with logits[20,0] and target0 yields gradient[0,2.061e-9]; a stable real-arithmetic reference is approximately[-2.061e-9,2.061e-9]. This exercises a known rounding issue in this exact backend/example. It does not demonstrate an effect on any RSD system or estimate how many prior evaluations are affected. Our [earlier source intake](../softmax-source-intake-v1/REPORT.md) and [numerical study](../upstream-numerics-v1/REPORT.md) already keep dtype/regime scope explicit.

The additional statement that zero teacher logits mean the student learns nothing is incorrect in general. Teacher logits[0,0] give probabilities[0.5,0.5]. With student logits[2,0], the tested KL objective has nonzero student gradient approximately[0.380797,-0.380797]. Equal logits are not zero probabilities; zero gradient at a matched optimum is another case. No optimizer step or small-model weight update was performed.

## Source-weave boundaries

The relay lists six broad source labels but no bibliography for its claimed twelve papers. Its MemoryTax conclusion is broader than our [source contact](../memory-byte-intake-v1/REPORT.md); model/cost/task conditions matter. Its equal-norm ResonanceDB affine-cosine statement is compatible with our [derived real-coordinate control](../resonance-memory-contact-v1/REPORT.md) when that information-matched representation is specified. It is not evidence that every memory advantage is established. O-O Harness class inheritance is not by itself a saddle-node/Hopf bifurcation: the relay supplies no dynamical equations or stability calculation. The unspecified Subagent CoT and Hybrid Agents labels remain insufficiently sourced here. Syntax collapse, error, missing evidence and numerical precision are different possible mechanisms.

We did not re-read or verify twelve external papers, infer a universal storage-versus-distillation bottleneck, or attribute the source text to an authenticated multi-agent study. The code failure does not make every idea in the relay false. It narrows what the demonstration supports.

## Next contact and adoption status

A future gate test should compare correctness/provenance-aware selection against no gate and variation-based selection on independently scored trajectories, including constant-correct, constant-wrong, noisy-correct and noisy-wrong cases. Count useful targets wrongly blocked, wrong targets admitted and actual held-out learning outcomes. Preserve all records separately from the choice to use them as targets. Thresholds must be calibrated outside evaluation cases. No new training, automatic avoidance router, universal threshold or bifurcation claim is adopted here.

In parallel, the [single-rule small-model pilot](../smollm-missing-evidence-pilot-v1/REPORT.md) proceeds from our previous suggestion rather than adopting this gate. Its actual failure—frequent fluent repetition of a rule without application—is relevant diagnostic material, not proof of context-pressure collapse. Root authored/reviewed these checks; no independent scientific audit claimed. Frozen source/protocol hashes and raw originals remain intact.
