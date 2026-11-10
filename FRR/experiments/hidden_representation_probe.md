# FRR v0.5 — What is linearly decodable from recurrent hidden states?

**Status:** Executed synthetic correlational representation probe, 2026-11-10 UTC.  
**Code:** `hidden_representation_probe.py` using the established `eight_state_nonlumpable_rnn.py` generator.  
**Important:** Linear decodability does not prove causal use, uniquely localized memory, or an interpretable internal representation.

## Question and protocol

Train a 16-unit GRU on next-bit prediction in the noisy (epsilon=0.1) eight-state three-bit parity world for 450 Adam steps with independent fresh 128×24 training trajectories. Freeze its weights. For a separate 768-sequence probe-fitting dataset, extract its 16-dimensional hidden state at valid times t>=2 and train a 4-output *linear* readout for (current bit, previous bit, bit two steps back, parity of three bits). Evaluate the probe on an independently generated 768-sequence dataset. All probes see labels only during probe fitting; the GRU was never trained to directly reproduce the hidden-bit labels.

Controls: the same linear readout trained on untrained randomly initialized GRU features; and a readout trained on randomly permuted labels paired with the trained GRU features. Seeds 7, 17, 29. Both independent probe datasets contain 16,896 valid timesteps per seed. The underlying trajectories have temporal correlations; results are descriptive, not independent-binomial confidence intervals.

| Condition | Current bit | Previous bit | Two-back bit | Three-bit parity |
| --- | ---: | ---: | ---: | ---: |
| Trained GRU hidden, all seeds | 100% | 100% | 100% | 100% |
| Untrained GRU, seed 7 | 98.30% | 68.83% | 68.15% | 73.21% |
| Untrained GRU, seed 17 | 98.15% | 73.50% | 66.73% | 71.68% |
| Untrained GRU, seed 29 | 100% | 77.72% | 73.33% | 71.40% |

The permuted-label readout had erratic out-of-sample results: by seed, current-bit 45.60%, 56.03%, 44.50%; previous-bit 32.55%, 47.52%, 34.90%; two-back 44.69%, 46.41%, 42.96%; parity 47.63%, 37.38%, 61.39%. Unlike the main probe, it did not reliably recover true labels, but results are not exactly 50% and should not be marketed as calibrated chance-level measurement.

## Interpretation

The trained recurrent state makes each relevant prior bit and the parity function linearly readable on new trajectories, matching the network's ability to predict the noisy future. Random recurrence already allows nontrivial decoding of earlier bits, so the result is not binary evidence that training *created* memory where none existed. Rather, supervised training substantially increased **linear accessibility** of the relevant historical variables in this particular network.

The direct next-bit prediction remains noisy (Bayes 90%) even though the historical input bits can be decoded perfectly. That distinction matters: the GRU can recover the history but cannot predict the new independent noise bit.

## Next decisive test

Intervene on recurrent representations rather than only reading them: ablate hidden coordinates, perturb the previous-bit information, test whether the forecast changes in the mathematically expected direction, and compare to retrained/sham perturbations with matched magnitudes. A linear probe establishes correlation and availability to a separate decoder, **not** that the GRU's prediction head causally reads those decoded bits in that form. For a deeper test, use information bottleneck or minimum-state representation controls and hidden-state causal mediation.
