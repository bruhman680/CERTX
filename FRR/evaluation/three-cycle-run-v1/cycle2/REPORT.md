# Cycle2: marginal calibration can miss reset dependence

## Decision from Cycle1 and prior exposure

Cycle1's noisy-calibration results showed that known/estimated marginal reset calibration and distinct interventions can help finite-family identification, but redundant designs can remain ambiguous. Root selected this challenge: are marginal calibration rates enough once the readout contains an interaction?

The adjacent [rival-review sandbox](../rival_review/NOTES.md) had already exposed the mixed-interaction example. This cycle is an adaptive counterexample analysis, not preregistered or sealed confirmation. [PROTOCOL.md](PROTOCOL.md) was saved before this expanded execution, preserving all8 SR-C1 worlds and all36 reset-marginal pairs on a fixed grid, with independent/positive/negative dependence:864 population cells. No model parameters were retuned. The shared row is an out-of-fit check, not an independent test dataset.

## Result

Each coordinate can have the same erasure rate under different joint reset operators. Let q be probability both coordinates erase. Then joint survival is `J=1-rA-rS+q`. The first-outcome response is

`D=(1-rA)*a + (1-rS)*b + J*c`.

Independence replaces J with `(1-rA)(1-rS)`. That replacement is valid for the additive control c=0 regardless of event dependence, but can fail when c is nonzero. Our reset-event law is state independent; other laws may need a different derivation.

On SR-C1 mixed_interaction, fitting three coefficients from three sham/agent/soil equations while incorrectly assuming independence interpolates to floating-point precision. Yet the out-of-fit shared reset is wrong by−.00753596 under positive coupling and+.00358855 under negative coupling. A zero training residual therefore cannot validate independence in this saturated design.

A direct same-run joint-survival witness supplies J. Its full-rank design recovers the defined contributions across all three dependence laws, within3.80e-17. This witness is stipulated to observe the relevant nonzero coordinate pair directly and accurately. It is not a measurement of unknown hardware or an inaccessible latent state in real agents.

Without joint calibration, marginal rates bound J by the Fréchet interval:

`max(0,1-rA-rS) <= J <= min(1-rA,1-rS)`.

Using true coefficients, the resulting response sensitivity envelopes contain all864 calculated responses. They are conditional algebraic envelopes, not empirical confidence intervals or identification from marginal data alone. Coefficient estimation uncertainty and witness error would need propagation in a noisy application. The envelope can be too wide to support a useful decision; it does not automatically choose the true dependence law.

## Checks and limits

[RESULTS.json](RESULTS.json) preserves every(q,J), erase-event probability, prediction, interval and outcome; [run.py](run.py) specifies the calculation. All9 checks pass:864 legal cells, operator formula, calibrated recovery and predictions, interval containment, independent/additive controls, the declared mismatch, and the10second execution budget. Runtime was about.05seconds; largest operator/formula difference5.56e-17. [stdout](RUN.stdout.txt) and [stderr](RUN.stderr.txt) are retained. These are same-model floating-point checks, not independent replication of the assumptions.

A witness that loses its access gate can confuse unreadable information with erased information. This cycle does not model or test that confound. Missing witness output should remain missing, not be encoded as erased state. A separate independently accessible witness or restored-access control would be required to distinguish them under declared assumptions.

An interaction term is a response feature, not a new physical memory carrier. Correlated erasures need not be the only rival explanation for prediction error. The three joint-witness training equations also saturate their model; successful recovery here does not prove that model uniquely describes a real system.

## Useful consequence

When an intended observation depends on relationships between coordinates, calibrate or bound the joint intervention law, not merely its marginal success rates. Preserve an out-of-fit operator check where consequential. Root can incorporate this into the optional verification/specialization guidance during Cycle3; no global navigation, core schema, GitHub publication or queue status was changed by this agent.
