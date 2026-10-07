# Expansion boundary review — adaptive graph and retained signals

7 October 2026. Independent design review before interpreting the new graph-diffusion experiment. Based on SWARM_BOUNDARY_CURIOSITY.md, GEMINI_LOCAL_ANNEALING_EXPLORATION.md, and GEMINI_MATHEMATICAL_LEDGER.md. This note proposes controls; it does not report execution or model-agent performance.

## Live seed and exact burden

Can local interactions produce communication boundaries that preserve useful distinctions, while allowing a targeted intervention to reopen one region without disrupting unrelated information? A conductance-adapting numerical graph can establish an executable mechanism for this relation. It cannot by itself establish that FRR agents spontaneously form such boundaries, that the boundaries preserve truth, or that all swarms share a critical threshold.

If edges weaken according to local signal disagreement, emergence means a global partition was not explicitly supplied, while the local preference for agreement was supplied. Both facts belong in the interpretation. The design can discover where boundaries fall without discovering whether disagreement should weaken communication.

## Most consequential confounds

1. **Conservation mistaken for recall.** Retaining x values longer under weak diffusion preserves existing signal; it does not show that a reader can recover an earlier message after signal reset. Separate signal retention, fresh-reader access to retained signal, and reconstruction from conductance alone.
2. **Encoded distinction mistaken for independent discovery.** Two constant-valued planted blocks supply a partition directly to a difference-sensitive rule. Add smooth/noisy signals with no planted blocks, different task messages on the same graph, and independent held-out patterns. Report planted-block performance as a synthetic demonstration.
3. **Slower communication mistaken for better memory architecture.** A graph can preserve every initial distinction by setting all weights to zero. Require positive cross-boundary communication on a new task or a declared transfer-rate target. Compare retention at matched useful communication cost, not retention alone.
4. **Budget mismatch.** Adaptive graphs with less total conductance diffuse less even without meaningful organization. Include a frozen scalar-rescaled graph matching total weight, and shuffled learned weights preserving the weight multiset. Distinguish wall-clock time, simulated time, and cumulative communication exposure.
5. **Noise placement mistaken for intelligent intervention.** Local noise has an obvious collateral advantage if the relevant region is supplied by an oracle. Match total injected energy and number of update steps; include random-region noise and imperfect localization. Separately test an actual trigger if semantic detection is claimed.
6. **Reader leakage.** A fresh reader supplied planted block labels, stored original payloads, or a tuned evaluation threshold has inherited the answer. Calibration histories and readers must be separate from held-out evaluation histories.
7. **Summary failure.** One graph-gap number cannot identify which message crosses which boundary. Report targeted passage, sign/order preservation, and recovery error. Smaller gap can mean useful modularity, useless isolation, or communication failure.

## A minimal falsifying pair for topology-only memory

Suppose conductance updates depend on absolute or squared local differences. Training on x and on -x produces identical conductance histories under otherwise identical deterministic dynamics; x and x+c also have the same differences for translation-equivariant signal dynamics. Consequently the learned conductances alone cannot determine payload sign or absolute offset. A fresh reader cannot recover both correctly from the same graph.

This is a structural counterexample to unrestricted topology-only payload recall, not a failure of boundary retention. If additional asymmetric deposits, anchor states, or node attributes distinguish the histories, name those carriers explicitly. They are a useful repair, but then the graph conductances are not the complete memory state.

## Smallest useful comparison

Use a small connected graph, multiple preregistered seeds, and a declared scalar signal task. Compare:

- Frozen initial conductances.
- Locally adapting conductances.
- Frozen learned conductances, retaining the same signal state at freeze time.
- Shuffled learned weights or a total-conductance-matched frozen graph.

First measure retained distinctions and passage of a newly injected signal. Next reset only the reader, then reset signal values while retaining the graph, then reset graph and signal together. The reset hierarchy identifies the persistence carrier. Do not infer topology memory from the first reset alone.

For reopening, compare no perturbation, targeted local perturbation, random-region perturbation, and global perturbation at equal total noise energy. Declare a local objective and an unrelated retention objective separately. An intervention helps only if it improves the first sufficiently to justify measured losses in the second; a scalar average can conceal destruction of the protected message.

## Fair failure and recoverable residues

If adaptation merely lowers total conductance, the performance claim narrows to a retention/communication tradeoff; the implementation and budget diagnostic survive. If the frozen learned graph matches ongoing adaptation, persistent structure is useful but continued plasticity has not earned its cost. If shuffled weights match performance, the learned spatial organization is not yet explanatory. If topology-only recall fails but retained-signal recall works, the carrier is node signal state, with graph-mediated preservation/access. If oracle targeting works but random targeting fails, localization matters and a detector remains unbuilt.

A favorable result can establish a model-specific local rule that forms useful boundaries under declared tasks. Testing real FRR reasoning agents would require actual message traffic, task quality and disagreement measures, matched budgets, and a comparison without FRR. No mathematical node should be counted as an independently reasoning AI agent.
