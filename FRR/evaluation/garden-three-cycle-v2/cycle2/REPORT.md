# Cycle2: decisions can stabilize before hidden-state identification

The [protocol](PROTOCOL.md) was frozen after Cycle1 and the peripheral scout's early decision-theory findings, before new numerical execution. This is adaptive authored decision analysis, not empirical evidence that a particular memory architecture or randomized policy is best. Four intervals and all costs were specified in advance. [run.py](run.py) and [RESULTS.json](RESULTS.json) preserve the calculation.

## Information and choice are different objects

Cycle1 permits survival probability v in[.2,.8] despite knowing the population observation law. Here the chosen actions have expected losses:

- rely on retained content:1-v;
- use a fallback:.15+.4v.

These correspond to fixed state losses(1,0) and(.15,.55) for absent/surviving content. They are illustrative task preferences, not costs inferred from the records. Their crossover is v=17/28, about.607143. On[.75,.9], rely wins for every compatible v. On[.1,.3], fallback wins throughout. Neither interval point-identifies survival, yet the specified action ordering is stable.

The other intervals cross the threshold. If choosing to minimize worst expected loss, a mixed policy with fallback probability5/7 has worst loss.392857 on[.2,.8], versus.47 for the best pure action. If minimizing worst regret relative to a policy knowing v but not individual state, the fallback probability is19/28 and worst regret.183214, versus.27 for the best pure action. Different criteria can choose different policies without disagreeing about the observed data. On[.55,.7], the regret policy changes to8/21 while the worst-loss policy remains5/7.

These are expected-loss results over an authored state/loss model. Randomization does not guarantee a safe single realization, infer the true v, or replace task constraints. A different feasible action set or different losses changes the answer.

## Looking again is an intervention with a cost

The probe observes an individual's post-intervention S', not the population parameter v. A clean probe costs.03 and leaves state unchanged. Another clean probe costs.5. A third costs.03 but independently destroys surviving content with probability.8, with an additional loss1 per surviving original destroyed. After observing S' perfectly, the policy chooses the best state-specific action.

For[.2,.8], worst expected total losses are.15,.62,.796 respectively, against.392857 for the no-probe minimax policy. Ignoring damage incorrectly predicts.15 for the destructive probe. Cheap trustworthy access can be useful; expensive or damaging access may not be. These values assume known perfect state readout, damage probability and downstream losses; no real probe was measured.

The probe policy has richer information than a policy merely knowing v. It is compared using total expected loss; the fixed-action regret benchmark is not silently reused for the state-observing probe. The destructive case is information plus state change, not a pure information refinement.

## Checks, failure and scope

All eight checks pass. Direct state/erase enumeration agrees with the probe formula within1.12e-16; analytic optimization differs from the fixed10001-point grid by at most7.72e-6, within the prespecified2e-4 bound. No random data were generated.

The first execution failed during NumPy-boolean JSON serialization before writing results. Source and streams are preserved as INITIAL_FAILED artifacts, with [repair notes](REPAIR.md). A subsequent strict scalar serializer leaves mathematical inputs unchanged; separate review replays final output. The orchestration's initial missing-results read is also disclosed. No successful subset of sampled trials was selected: there were no sampled trials.

The useful output is a scoped decision distinction: keep uncertainty about the mechanism visible, and ask whether it changes the next permitted action. A stable action under stated losses is not evidence that a causal explanation is true. Credibility of observation, intervention preservation, feasible-state bounds and loss choices remain separate obligations.
