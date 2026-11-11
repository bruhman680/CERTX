# Learning when to harvest: autonomous per-cell threshold-policy probes

**Status:** Exploratory research loops, 2026-11-11 UTC. Code: `ADAPTIVE_threshold.py`, `ADAPTIVE_probe.py`; individual seed measurements: six `ADAPTIVE_*_results.json` files. This is a *one-neuron stochastic threshold controller per cell*, **not** the original 12-hidden-unit recurrent network and **not** teacher imitation, open-ended evolution, or a claim of general cognition.

## Orientation and mechanism

The original Neural Garden's immediate reward encourages harvesting at resource >.252, which depletes future resource; a hand-coded .55 rule works better for several hundred ticks but ultimately loses energy. Can cells learn a useful **resource-conditional action** from their own energy change, without being shown a teacher's actions?

For every cell `i`, policy `P(harvest)=sigmoid(14*(resource_i - threshold_i))`. At initialization each threshold is independently drawn uniformly from `[.25,.75]`; no optimal teacher threshold is supplied. Each cell updates its own threshold from actual local energy changes through a REINFORCE score trace:

`trace_i(t)=.97*trace_i(t-1) - 14*(action_i(t)-p_i(t))`

`threshold_i += .001 * (realized_delta_energy_i - running_baseline_i) * trace_i` (clipped per-tick update and threshold bounds). All environmental resource and energy laws match original Garden v0.1. When testing, training stops and thresholds are deterministically applied in **fresh worlds** on unseen seeds. The original untrained thresholds are also tested from identical fresh-world starts, which isolates the value of learned updates beyond initial parameter heterogeneity.

**Invariant check:** An `AdaptiveThresholdGarden` with `learning=False`, deterministic action, and all thresholds .55 matches `ThresholdGarden(.55)` resource and energy arrays **bit-for-bit over 500 ticks** with a fresh seed. Thus the environment laws agree in this tested case.

## Observations (run/seed as replication unit)

### Probe 1: initial 10-seed exploration

Train 900 ticks, size12; frozen deterministic transfer to fresh worlds for 1,000 ticks. Learned mean energy .31668, initial-untrained threshold population .29802, fixed .55 .42237. Learned thresholds shift a modest mean absolute .00880. Seed range 900–909. This pilot informed subsequent testing and is *not* independent preregistration.

### Probe 2: fresh 30-seed validation under fixed design

Fresh training seeds 920–949, same sizes, durations, policy slope, learning rate, trace decay, and test protocol as Probe 1.

| Frozen deployment | Mean final energy at 1,000 ticks |
| --- | ---: |
| **Learned heterogeneous thresholds** | **.30494** |
| Same initial heterogeneous thresholds, never learned | .27924 |
| Fixed threshold .55 | **.42335** |

Paired learned-minus-untrained energy = **+.02569** across 30 fresh seeds, descriptive seed SD .01109; all 30 differences positive. A normal-approximation descriptive 95% seed-mean interval is `[+.02173,+.02966]`. **The fixed .55 rule still wins substantially at this 1,000-tick horizon.**

### Probe 3: causal pressure on delayed eligibility

Twenty matched fresh seeds 1000–1019, 900 training/1,000 testing, size12:

| Credit update | Learned energy | Initial untrained | Mean learned threshold |
| --- | ---: | ---: | ---: |
| Trace decay 0, learning rate .001 (instantaneous score) | .06223 | .28180 | .40300 |
| Trace decay .97, learning rate .001 | **.30416** | .28180 | .49424 |
| Trace decay 0, **lower** learning rate .0001 | .25944 | .28180 | .48703 |

At this chosen step size, instantaneous policy learning aggressively lowers thresholds and harms ecology; retaining a delayed eligibility trace avoids that collapse. However changing trace decay also changes update scale/noise, and the low-rate control mitigates the damage; the result is **not proof** that delayed credit assignment alone is causally responsible.

### Probe 4: longer fresh transfer horizon

Another 15 training seeds 1100–1114, size16, 1,200 training ticks, **2,000-tick independent frozen deployment** on corresponding fresh test seeds 6100–6114:

| Frozen deployment | Mean final energy at 2,000 ticks |
| --- | ---: |
| **Learned heterogeneous thresholds** | **.31764** |
| Initial heterogeneous thresholds, never learned | .29118 |
| Fixed threshold .55 | .27183 |

Paired learned-minus-untrained difference = **+.02647**, across-seed SD .01434; all 15 seed pairs favor learning. Descriptive normal-approximation 95% seed interval `[+.01921,+.03372]`. Learned-minus-.55 difference = **+.04581**; 13/15 seed pairs favor the learned policy. Crucial: even the **untrained heterogeneous threshold distribution** outperforms fixed .55 on average at this horizon, so do not attribute all of the learned policy's lead over .55 to learning. This is an **exploratory**, researcher-selected horizon after observing earlier probes, not an untouched confirmatory claim of global superiority.

## Interpretation and limits

1. **Evidence for small within-toy-world autonomous learning:** The threshold policy receives no teacher examples, trains on local energy feedback, and consistently improves over the exact same initially random per-cell thresholds under several fresh-seed test protocols.
2. **Heterogeneity is a genuine independent baseline:** a *population of different static resource thresholds* can outperform one uniform threshold at longer horizons. Measure initial diversity separately from acquired changes.
3. **No proof of sustainability:** A higher mean at tick2,000 is not a stationary energy budget, robust ecosystem equilibrium, or indefinite ecological health. Extending with complete energy trajectories is necessary.
4. **Restricted architecture:** The trained controller is a scalar one-neuron logistic action rule, not an LLM, transformer, or the inherited original 12-hidden-unit recurrent predictor. Neural recurrent weights still exist in inherited storage but do **not** control these new actions. This intervention tests the *learning principle* with minimal assumptions before migrating it to the richer network.
5. **Reward clipping, selection bias, and statistics:** Policy gradient uses realized post-clipping energy and can suffer floor-signal loss; 30 or 15 seeds represent within-generator variation only, not real-world generalizability. Hyperparameters were hand-selected for exploratory use, and future claims require frozen-design unseen perturbation studies, seed-level paired statistics, and controls for matched update magnitude.
6. **Transfer protocol:** Each trained vector of 144 or 256 spatial per-cell thresholds is transferred into a *freshly seeded but same-size and same-law* world; per-coordinate parameter mapping is fixed and does not transfer to arbitrary new grid sizes or unseen ecological physics.

### Probe 5: deeper 5,000-step counterexample — fixed threshold .50

We extended the test with 10 further seeds 1200–1209, 1,200 training ticks, and *new matched worlds* for a 5,000-tick deterministic deployment at size16. A separate independent audit identified the omitted comparator **uniform threshold .50**, which was added *posthoc* to this long-horizon probe. Therefore this is an explicitly adaptive-design exploratory screen, not a blind confirmation.

| Policy in fresh test world | Energy at t500 | t2000 | t5000 | Energy-floor fraction at t5000 |
| --- | ---: | ---: | ---: | ---: |
| Learned heterogeneous thresholds | .34317 | .33222 | .32903 | **41.60%** |
| Initial untrained heterogeneous thresholds | .31266 | .30030 | .29777 | 45.51% |
| Uniform fixed threshold .55 | .49466 | .26630 | .03629 | 13.71% |
| **Uniform fixed threshold .50** | **.60838** | **.63340** | **.67117** | **0.00%** |

This is a **substantial correction** to the earlier comparison: learning improves heterogeneous thresholds over their own untrained starting points by about .031 energy at tick5000, but **does not approach** the much better fixed .50 rule. Every cell in the .50 condition retained energy >.1 at tick5000 in this selected synthetic-world probe, while about 42% of learned-heterogeneous cells were at the near-zero energy floor. The learned condition's mean energy hides a polarized distribution (about 18% at the upper cap), so mean energy alone misrepresents ecological health.

At tick5000 the *instantaneous* raw energy drift of fixed .50 averaged ~-.0006, so even this favorable trajectory does not establish an indefinitely sustainable steady state. Average drift over a long window, resource seasonality, external shocks, and still longer trajectories are necessary. The `.50` setting was identified by searching nearby alternatives after earlier outcomes; **do not report it as an untouched holdout discovery**. Detailed per-seed checkpoints, raw pre-clipping drift, floor/ceiling fractions, and action–resource covariance are in `ADAPTIVE_longterm_results.json`.

## Strongest next loop

**Freeze fixed .50 as the current strong baseline**, then verify on entirely new seeds across 10,000–50,000 ticks and perturbed resource laws, with raw pre-clipping drift, floor/ceiling occupancy, and recovery metrics. Compare learned heterogeneity against strong nearby fixed thresholds and optimized heterogeneous populations with matched mean/variance. A learning mechanism should not be promoted to an ecological discovery until it competes with that baseline; only then consider porting the objective into the original per-cell recurrent controller.
