# PF-C1/PF-C2: what readout and prediction can establish

Two bounded constructed follow-ups to [CE-C1](../claude-errata-intake-v1/REPORT.md), authorized by the user. [Protocol](PROTOCOL.md), [code](../../experiments/probe_followups.py) and [manifest](MANIFEST.json) preceded the first local execution. This is an authored development experiment, not an independently reserved benchmark, physical calibration or real-agent memory test. No original scripts or earlier reports were edited.

[RESULTS.json](RESULTS.json) preserves every generated count, selected fit, optimizer attempt and held-out prediction; [CHECKS.json](CHECKS.json) records scope, environment and post-run checks. The run completed in about2.83 seconds, without stderr. All six recorded structural/contrast checks and seven calibration subchecks passed. These checks do not require any fitting method to win.

## PF-C1: loss of stored information versus loss of access

Both toy worlds contain a field carrier and a private carrier written with fidelity0.9. The **reader's route differs**: one uses the field; the other uses private storage through a gate. This compares which retained signal the reader uses, not exclusive existence of storage.

| Main-reader success contrast above chance | Field-reading world | Gated-private-reading world |
|---|---:|---:|
|Keep / sham|0.128|0.128|
|Erase field and close private gate|0|0|
|Same field erasure, restore private gate|0|0.128|

The first two rows cannot distinguish these worlds; the third can **under the stated intervention semantics**. Restoring access is different from restoring erased field content.

The direct carrier witnesses bypass the main read gate by construction. After erasure, the field witness answers correctly with probability0.5 and the private witness with0.9 in both worlds; private information survives even when the main reader loses its signal. A contaminated private witness that shares the closed gate drops to0.5 and falsely resembles erased storage if that access distinction is omitted.

A separate idealized calibration prepares perfect known-payload inputs, rather than the main world's0.9-fidelity carriers. Imperfect clearP randomizes field contents with probability d=0.1 and private contents with probability s=0.9. Gate-independent witness success is respectively0.95 and0.55, so the formula2*(1−success) recovers d and s. These are exact probabilities, not finite calibration measurements. Correct witness access/accuracy and known preparation remain assumptions; no procedure here independently validates all of its own instruments.

A main-reader two-exponential curve is also invariant under swapping the amplitude/rate pairs. Fitting two components therefore does not label one “field” and the other “private.” The distinction needs justified access or intervention information beyond the fitted curve.

## PF-C2: additional measurements and held-out prediction

Five stipulated generators, twelve replicates each, produce independent binomial measurements with success probability0.5+c(k). Four early training counts use300000 trials per count; six spread training counts use200000 each. Both allocate1200000 training trials. This is equal statistical sampling budget, not equal optimization cost or an agent-compute comparison. Training counts are independently generated between arms; precision from paired resampling is not claimed.

Sparse training k=[0,1,2,3]; spread training k=[0,1,2,3,5,7]. Held-out k=[4,6,8,10] use separate counts shared only for evaluating the fits. Parameters are chosen exclusively by training squared error. We fit bounded nonnegative one- and two-exponential families, using the prespecified multistart optimizer. Embedding the one-component fit ensures the two-component candidate cannot be worse on training loss. This nesting does **not** ensure better prediction.

There were240 selected model fits and720 optimizer starts. All starts reported success; this is not a global-optimum guarantee. The two-component model is permitted to collapse to one component.

The following is mean held-out squared probability error against the **known toy generator**. It equals expected Brier-score regret. It is not empirical calibration error or a field-observable ground-truth estimate. Raw results also include empirical held-out Brier scores from the separately generated test counts.

| Generator | Early counts, one component | Early counts, two | Spread counts, one | Spread counts, two |
|---|---:|---:|---:|---:|
|Separated rates0.9/0.1|8.64e-4|2.62e-5|1.63e-4|1.23e-6|
|Close rates0.45/0.4|5.83e-9|7.95e-7|1.26e-8|1.12e-8|
|Coincident rates0.7/0.7|1.14e-7|3.50e-6|2.22e-7|3.40e-7|
|Single rate0.9|1.98e-6|2.72e-5|4.41e-7|1.14e-6|
|Oscillating, outside both families|9.52e-5|9.52e-5|8.61e-6|8.61e-6|

Read rows within their task; the different generators have different difficulty and contrast at late probe counts. These twelve-replicate summaries are descriptive; no confidence interval, monotonic law or universal preferred design is inferred.

**Separated components:** spread measurements with two components improve mean prediction error relative to early-count two-component fits here, and beat the spread one-component fit in all twelve replicates. Median absolute slow-amplitude error drops from0.00610 to0.00281, against a true slow amplitude0.128. This is recovery of a generator coefficient, not a named carrier.

**Close components:** spread two-component predictions are very accurate, yet median slow-amplitude error remains0.06026—roughly the entire other component's true amplitude0.06. Accurate prediction is compatible with poor mixture decomposition. The simple early-count one-component fit has the smallest mean regret among these four settings. The small aggregate difference between spread one/two is not broad evidence for two components; the raw strict “better” count includes numerical ties/near-ties and should not be read as a statistical win count.

**Collision and single-component controls:** one component performs well, while added flexibility can fit noise. At a true collision the amplitude split is unidentifiable from any number of these same response measurements, even without sampling noise.

**Misspecified response:** more spread observations improve prediction on these held-out positions, but cannot validate either functional form. A deterministic post-run shape check, explicitly added after seeing results, shows c(3)=0.06257 and c(4)=0.07700: an increase impossible for a nonnegative mixture of decaying exponentials. The original protocol requested a noiseless curve check; this separate post-run audit supplies it without changing fitted models or outcomes. A good score at selected positions is not proof the full response law is correct.

## What changed in our understanding

1. Witness access and calibration are part of the evidential claim. An instrument sharing the impaired gate cannot independently certify erasure.
2. Additional probe positions can improve prediction at the same total sample budget, but do not uniformly help every generator or restore identification at a collision.
3. Numerical optimizer success, physical admissibility, predictive usefulness, component recovery and carrier attribution remain different questions.
4. A simpler model is an informative control. More flexible fitting has a guaranteed opportunity to lower training residuals, not a guaranteed right to a stronger interpretation.

These are model-specific contacts. There is still no independently validated physical or semantic probe, inferred real-agent memory carrier or demonstrated general FRR advantage. No core guidance or schema version changes, and no broader queue family is completed. A useful next direction would depend on access to an actual independently checkable carrier or a specific reasoning workflow; further synthetic fitting alone cannot supply that evidence.
