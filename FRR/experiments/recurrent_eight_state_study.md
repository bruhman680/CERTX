# FRR v0.5 — Recurrent memory and eight-state observability

**Status:** Executed controlled synthetic experiments (2026-11-10 UTC). No universal cognitive claims.  
**Lineage:** [Earlier feed-forward eight-state probe](eight_state_neural_memory_probe.md).  
**Code:** `recurrent_eight_state_probe.py` and `eight_state_nonlumpable_rnn.py`.

## Question

Can a recurrent model retain prior observations that are needed to predict a later outcome, when a current-only predictor provably cannot? Does this remain true when the current-bit projection of an eight-state Markov chain is not strongly lumpable?

## Phase A: Independent-bit delayed readout (memory-capacity control)

Given a sequence of independent fair bits `x_t`, predict `x_t XOR x_(t-d)` at each valid step. A GRU sees only `x_t` sequentially. The model has 16 hidden units, trains for 350 Adam steps (learning rate 0.012) on freshly generated 128-sequence batches (24 steps each), then scores 1,024 independently generated test sequences. Seeds: 7, 17, 29. Hidden state resets across sequences.

| Delay | GRU test accuracy, all three seeds | GRU with hidden state reset at each prediction |
| --- | --- | --- |
| 1 | 100%, 100%, 100% | 49.61%, 50.04%, 50.13% |
| 2 | 100%, 100%, 100% | 49.66%, 50.03%, 50.12% |
| 3 | 100%, 100%, 100% | 49.57%, 49.99%, 50.11% |
| 6 | 100%, 100%, 100% | 49.84%, 50.10%, 50.04% |

For delay 1 or 2, the required past is contained in the eight-state three-bit shift register. Larger delays extend beyond eight states. Here the visible input stream is iid and *is* Markov; the target is an external delayed-readout task. Thus Phase A measures learned short-term storage, not nonlumpability or hidden-state inference.

## Phase B: Genuine eight-state nonlumpable prediction

Define the microstate `S_t=(x_t,x_(t-1),x_(t-2))`, observe only `x_t`, and generate `x_(t+1)=x_t XOR x_(t-1) XOR x_(t-2) XOR eta_t`, with independent Bernoulli(0.1) noise. All eight microstates affect the transition. A uniform microstate distribution is stationary. For two microstates with equal current bit but different hidden parity, the one-step visible-future total-variation distance is `0.9-0.1=0.8`: strong lumpability fails.

The exact Bayes accuracy is 50% from the current bit, 50% from the current plus one prior bit, and 90% from all three relevant bits. A GRU gets only the current observation at each step. Training uses 450 Adam steps, fresh 128-sequence batches of length 24, 16 hidden units, and the same three seeds. Scoring uses independent 1,024-sequence held-out streams and masks predictions until the two prior observations exist.

| Seed | GRU test accuracy | Hidden reset every step |
| --- | ---: | ---: |
| 7 | 89.7283% | 50.1554% |
| 17 | 89.8260% | 49.8091% |
| 29 | 90.5140% | 51.0875% |

The above-90% sample value for seed 29 reflects finite-test sampling, not a Bayes-bound violation. The learned recurrent predictor approaches the exact information-available ceiling; resetting its hidden state destroys the advantage. The comparator ceiling follows from analytically known conditional distributions, not a separately trained feedforward baseline.

## Interpretation and important boundaries

- **Supported within these toys:** GRU hidden state makes earlier observations operationally useful; its removal lowers held-out prediction performance. The second experiment's visible projection is genuinely nonlumpable.
- **Not shown:** Persistent memory across session resets, long-horizon transfer, weight updates after deployment, decentralized memory, an FRR prompting benefit, a universal cognitive law, or biological relevance.
- **Controls still to run:** Explicit three-bit feedforward model, shuffled-history condition, simple Elman RNN/LSTM comparison, sequence-level confidence intervals, longer sequences, observation noise, and unrelated eight-state dynamics.
- **No changes** to the canonical frozen 1,550-entry Garden, model weights, source pins or feedback rules.

## Literature scout: primary research connections

1. [Kaelbling, Littman & Cassandra — POMDP survey](https://cs.brown.edu/research/pubs/techreports/reports/CS-96-08.html): belief-state updates provide an explicit inference baseline.
2. [Littman, Sutton & Singh — Predictive State Representations](https://papers.neurips.cc/paper_files/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf): predictively sufficient history need not reconstruct ontic hidden states.
3. [Hochreiter & Schmidhuber — LSTM](https://doi.org/10.1162/neco.1997.9.8.1735): gated recurrence addresses long-delay training difficulty.
4. [Arjovsky, Shah & Bengio — Unitary RNNs](https://proceedings.mlr.press/v48/arjovsky16.html): copying-memory benchmarks motivate delay controls.
5. [Sussillo & Abbott — Recurrent dynamics](https://pmc.ncbi.nlm.nih.gov/articles/PMC2756108/): recurrent dynamics can learn task-specific computations.

## Next contact

Run the untrained structural controls and several architectural baselines against the same predeclared evaluation task; test whether learned memory remains useful as history delay, state observation noise, or transition perturbation changes. Keep every result tied to its source, exact experiment generator, training regime and held-out metric.
