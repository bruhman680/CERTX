# Eight-state observable-history neural probe

**Date:** 2026-11-10 UTC  
**Status:** Executed, deterministic constructed toy; not an empirical cognitive-memory finding  
**Code:** [eight_state_neural_memory_probe.py](eight_state_neural_memory_probe.py)

## Question

Does adding an informative previous observation repair a prediction failure caused by a coarse current-state observation?

## Construction

Eight equally weighted microstates are the binary triples `(current, previous, spare)`. The observable current bit is `current`; the target next bit is `current XOR previous`. The spare bit changes neither observable nor target. On the exhaustive uniform eight-state table, current-only information is irreducibly ambiguous: for every current bit, the target is equally likely 0 or 1. Both networks have a 16-unit tanh hidden layer and are trained with Adam and binary cross-entropy for 1,000 epochs, seed 7.

## Observed run

Run using PyTorch 2.9.1+cpu, CPU, Python 3.12:

| Learner input | Accuracy on eight fitting cases | Cross-entropy loss | Exact Bayes limit |
| --- | ---: | ---: | ---: |
| Current bit only | 4/8 = 50% | 0.693147 | 50% |
| Current and previous bit | 8/8 = 100% | 0.00004986 | 100% |

The output probabilities were 0.5 for every current-only case. The history-supplied learner predicted all eight cases correctly. The neural training outcome agrees with the exact conditional-information limit of the constructed task.

## Interpretation and limits

This demonstrates access to a missing distinction, **not** learned internal recurrent memory. The informative historical bit is supplied directly. The same exhaustive eight microstates are used to fit and score both models; there is no held-out generalization claim. The result is not evidence of a universal CERTX fiber threshold, a biological memory mechanism, or an inherent advantage of FRR prompting. A constant predictor also reaches 50% accuracy; 50% is the Bayes optimum for current-only observation in this balanced construction.

## Next discriminating contact

Use sequences and a recurrent network whose hidden state must encode the past without being handed a previous-bit feature at prediction time. Compare against matched feedforward and explicitly history-windowed baselines, use unseen sequences and multiple seeds, and vary memory delay and observational ambiguity. Keep the frozen 1,550-entry Garden entirely separate.
