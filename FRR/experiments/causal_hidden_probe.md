# FRR v0.5 — Paired hidden-state interventions on learned eight-state memory

**Status:** Executed synthetic causal intervention, 2026-11-11 UTC.  
**Code:** `causal_hidden_probe.py`; reuses the established parity world and 16-unit GRU training procedure.

## The pressure point

A linear decoder can recover history from hidden units, but that alone does not show that the trained prediction head *uses* the history. Here we intervene on the recurrent state delivered to the head, holding the current observation and model weights fixed.

## Controlled construction

Train GRU for 450 Adam steps on eight-state noisy parity world: `x_(t+1)=x_t XOR x_(t-1) XOR x_(t-2) XOR eta`, `eta~Bernoulli(.1)`.

For each seed, generate 2,048 independent held-out trajectories (length 18). Evaluate at fixed `t=12`. Create three versions of each observed prefix:

1. **Original:** genuine prefix through `t-1`.
2. **Relevant edit:** flip the observation at `t-2` in that prefix.
3. **Sham edit:** flip the observation at `t-5` instead, identical bit-flip magnitude but outside the true three-bit predictive window.

Run the GRU on each prefix to produce the hidden state immediately before `t`. Then feed the **same original current bit `x_t`** into that GRU with each hidden-state version and compare the model's logits and decisions. Thus the observed current input, the final predictor head, all network weights, and the case identity are held fixed; only the preceding hidden state induced by the edited history differs.

The edited histories are counterfactual input interventions, not necessarily dynamically consistent trajectories in the original world. The relevant-edit comparison is scored against the parity rule *for the edited history*, not against the unchanged actual-world next bit. It is a mechanistic test of the model's conditional mapping, not an estimate of causal effect on the environment.

## Results (2,048 trajectories per seed)

| Seed | Baseline parity-rule agreement | Relevant edit changes decision | Sham edit changes decision | Mean absolute relevant logit change | Sham logit change |
| --- | ---: | ---: | ---: | ---: | ---: |
| 7 | 100% | 100% | 0% | 4.2152 | 0.0736 |
| 17 | 100% | 100% | 0% | 4.3197 | 0.0362 |
| 29 | 100% | 100% | 0% | 4.2822 | 0.0578 |

After the relevant edit, the model's decision matched the flipped counterfactual parity in all cases. After the sham edit, it kept the original parity decision in all cases. The network is not simply reacting indiscriminately to any historical bit flip.

The true-world next bit has 10% independent noise; our parity-rule agreement measures the learned conditional decision, *not* 100% prediction accuracy against actual noisy outcomes.

## Inference and limits

This supports a causal role for relevant observation history *as carried through the recurrent hidden state* in the trained model's prediction. It upgrades the prior linear-decoding observation from mere availability to a controlled input-history/hidden-state effect for this task. It does **not** isolate a unique neuron or a specific linearly decoded coordinate as the necessary mediator; many hidden features may change after editing the prefix. The nonzero sham logit difference also shows irrelevant history is not entirely absent from continuous hidden activity, even though it did not change any decisions.

Strong next tests: precisely edit a decoded subspace while matching Euclidean perturbation norms, exchange hidden states between matched contexts, evaluate mediation and reversibility, and repeat across multiple timesteps and dynamics. Maintain sham comparisons, off-manifold caveats, and independence of held-out trajectories.
