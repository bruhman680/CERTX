# FRR v0.5 — Online feedback after an inverted eight-state law

**Status:** Executed bounded synthetic intervention, 2026-11-11 UTC.  
**Code:** `online_adaptation.py` (PyTorch), imports the previous preserved 8-state parity generator and rule-shift generator.  
**No changes** to the frozen canonical Garden; no live external-agent learning claim.

## Question

After a model learns the three-bit parity world, can labeled feedback help it recover when the parity law is inverted? Does adapting only the output readout differ from adapting all weights? Is previous-rule knowledge retained?

## Design

For each seed (7,17,29), pretrain a 16-unit GRU for 450 fresh 128×24 sequence batches on the noisy (`epsilon=.1`) three-bit XOR parity world. At a declared switch boundary, test an inverse-parity world. Clone identical pretrained weights into three arms:

- **Frozen:** no parameter updates.
- **Head-only:** Adam updates (`lr=.012`) on output linear head, recurrent encoder fixed.
- **Full:** Adam updates (`lr=.012`) to all network parameters.

Each of 80 post-switch feedback batches contains 128 newly generated independent inverted-rule episodes, length 24. After a batch's observations and target outcomes are available, the head/full arms take one gradient step. This batch is **not used for the reported test accuracy**: checkpoints 0,1,2,5,10,20,40,80 are scored on separate, fixed, held-out 1,024×24 streams never used for optimization. Predictions at scored times start at `t>=2`, after the necessary observations exist. The post-switch condition is deliberately supervised and known to the experimenter; it is **not** autonomous change detection. Each independent episode resets recurrent state.

Additionally, a frozen-model within-episode diagnostic uses 2,048 continuous 24-step trajectories with the law inverted at prediction time `t=12`. The GRU receives the entire observation sequence in one forward pass, with hidden state **continuous across the switch**. No new label feedback or learning is supplied. This isolates the immediate consequence of an unannounced law change.

## Main results

| Condition / time | Seed 7 | Seed 17 | Seed 29 |
| --- | ---: | ---: | ---: |
| Frozen model, inverted world | 10.13% | 9.94% | 9.91% |
| Full adaptation after 10 batches | 51.90% | 67.81% | 64.01% |
| Full adaptation after 20 batches | 76.44% | 77.17% | 81.05% |
| Full adaptation after 80 batches | 83.24% | 84.87% | 85.16% |
| Head-only adaptation after 80 batches | 43.74% | 9.94% | 25.74% |
| Full model **original-world** accuracy after 80 | 77.86% | 64.96% | 65.99% |

Before adaptation, original-world accuracy was 89.74%, 89.90%, 90.23% respectively. The head-only arm varied sharply by seed and did not quickly invert the rule under the chosen fixed learning rate/step budget; this is a *particular optimizer and parameterization result*, not proof the frozen representation lacks sufficient information. Full parameter adaptation improved the new rule but reduced performance on the old rule, illustrating a stability/plasticity tradeoff in this toy.

### Continuous hidden-state switch (no feedback)

| Seed | Pre-switch accuracy | Post-switch accuracy |
| --- | ---: | ---: |
| 7 | 90.37% | 10.35% |
| 17 | 89.99% | 10.15% |
| 29 | 90.52% | 9.92% |

The hidden state was carried normally across the law change; this alone did not repair predictions. No adaptation was possible because no feedback was given in this diagnostic.

## Evidential boundaries

1. These are **independent new synthetic sequences** drawn from the same small family of worlds, not natural data. Although scored test sequences are independent of training, timepoints within each sequence are correlated; uncertainty should resample whole sequences.
2. The main adaptation arm uses labeled post-switch feedback and a known intervention boundary. Recovery is standard supervised gradient learning, **not** self-directed change detection, persistent autobiographical memory, or evidence of FRR prompting efficacy.
3. The frozen model was a negative control. No explicit rule-hypothesis Bayes detector, replay, regularizer, optimizer sweep, or no-change false-alarm control was trained here. The `head_original` and `full_original` evaluations are forgetting/retention checks, not a separate ongoing never-change treatment.
4. More steps could improve the full model toward the 90% Bayes limit; we did not tune the budget after seeing outcomes. A simple explicit flip of the model's decision under a known inverted rule would be an informative non-neural comparator.

## Next contact

Compare an *unannounced* mid-trajectory switch with causal feedback, online Bayesian rule posteriors, a frozen network + detected output mapping flip, replay-preserving weight updates, and a no-change control. Use matched information and update budgets. Track adaptation delay, false alarms, accuracy/calibration before and after the change, and original-rule retention.
