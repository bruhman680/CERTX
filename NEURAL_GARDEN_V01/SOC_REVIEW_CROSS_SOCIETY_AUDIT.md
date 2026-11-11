# Independent adjudication — adaptive and longitudinal societies

**Audit intent:** Prevent computational proposals, repeated seed runs, and posthoc tuning moves from being misreported as independent scientific discoveries or distinct research loops. Reviewed `SOC_ADAPTIVE_sequential.py`, `SOC_ADAPTIVE_results.json`, `SOC_ADAPTIVE_validation.py`, `SOC_ADAPTIVE_validation.json`, `SOC_LONGITUDINAL_explore.py`, `SOC_LONGITUDINAL_results.json`, `SOC_LONGITUDINAL_validation.py`, and `SOC_LONGITUDINAL_validation.json`. The source SHA-256 values embedded in the two primary search JSON records matched local source bytes at audit time. This is code-and-data review, not human external replication.

## Adaptive society: 40 optimization iterations are not 40 distinct conceptual loops

The algorithm evaluates 40 one-at-a-time hyperparameter perturbations of a per-cell sigmoid harvest policy. Its five rotated parameters are trace decay, learning rate, slope, and two initialization thresholds. It trains on the *same four developmental seeds* for every proposed edit and accepts a candidate when the mean 800-tick development score increases by >0.0001. A sealed 12-seed set is tested only after search.

All 40 moves have explicit numeric hypotheses and accept/reject decisions; they are real **sequential experimental design iterations** (16 accepted), not merely simulation ticks. But the conceptual question remains the same: *Can local hyperparameter search improve the current learned policy?* The parameter schedule is substantially predetermined, and repeated use of four development seeds invites overfitting. Under strict research-loop accounting, **count the 40-step optimization as one substantive conceptual research loop**, with separate loops for sealed evaluation and later post-selection robustness testing. Do not count 40 discoveries.

### What the two evaluation stages really show

| Evaluation | Learned selected policy energy | Fixed 0.50 energy | Learned floor fraction | Context |
| --- | ---: | ---: | ---: | --- |
| Sealed size8, 800 ticks, 12 seeds | .64618 | .61480 | .09115 | Advantage at optimized horizon; same generator, distinct seeds |
| Post-selection size16, 3,000 ticks, 12 new seeds | **.64076** | **.64982** | **.12012** | Result reverses; fixed has **zero** energy-floor cells |

On the later 12-seed paired test, learned beats fixed 0.50 in **1/12 seeds**, loses in **11/12**, average difference `−.00906`. The learned controller still improves over its **own** untrained same-initialization thresholds (`.64076` vs `.39559`), which is legitimate within-generator evidence of learning. But it has **not demonstrated a stable ecological advantage** over a tuned hand-coded rule, especially when cell-level floor occupancy counts.

Do not call the second test “external confirmation”: size/horizon changes were chosen after exploratory search and earlier experiments; the worlds are synthetic and share model equations.

## Longitudinal society: hand-coded policy creativity is not autonomously evolved intelligence

The 25 entries in `SOC_LONGITUDINAL_results.json` are legitimate distinct policy configurations and counterfactual tests from the **same canonical seed37 tick100 state**, but no repeated proposals represent independent natural-world replication. Most entries fall into a smaller set of genuinely distinct explanatory burdens:

1. Baseline and narrow threshold bracketing.
2. Energy-ceiling gated rest (two caps).
3. Low-energy rescue (two settings).
4. Neighbor-gradient correction and adversarial sign reversal.
5. Temporal-resource trend and reversal.
6. Three-tick/17-tick periodic intervention.
7. Hysteresis and reverse hysteresis.
8. Stochastic-threshold sharpening.
9. Longer-horizon challenge of selected policies.
10. Resource-shock challenge of selected policies.
11. Disjoint fresh-seed validation of selected policy classes.

Conservatively: **11 substantive policy-family/validation research loops**, or perhaps 12 if original baseline establishment is separately argued. Do **not** count every one of the 25 parameter proposals as a separate conceptual discovery. They are 25 numerical design moves inside ~11 distinct questions.

### The strongest result and its limitation

On *the historical seed37 state*, a hand-coded `energy_rescue` policy (harvest threshold .51, reduce threshold by .025 when energy <.12) had mean energy `.6271` at tick20,000 versus fixed `.50` `.4588`; the exact canonical checkpoint remained unmodified. This is a useful policy hypothesis, **not neural adaptation**. It exploits explicitly provided cell energy information and is a one-world posthoc choice.

On **24 fresh matched seeds** at t10,000, more cautious conclusions follow:

| Policy | Mean energy | Mean near-floor fraction |
| --- | ---: | ---: |
| Fixed .50 | .67662 | .00602 |
| Fixed .51 | .67459 | .00732 |
| Energy rescue | .68295 | 0 |
| Neighbor gradient | **.69120** | .00570 |

Energy rescue beats fixed .50 in only **13/24** seeds (paired mean +.00633, seed SD .01487). It beats fixed .51 in 24/24, but the comparator choice matters. The neighbor-gradient policy is even higher on average; paired against fixed .50 it wins **21/24** seeds (mean +.01458), and against rescue it wins **17/24** (mean +.00826). These modest, posthoc-selected margins need prospective holdout before a robust ranking claim.

The strongest defensible finding is that **hand-coded resource/energy/spatially conditioned policies can surpass simple fixed thresholds in this toy world**. Nothing yet shows that the Garden's neural cells discover those structures autonomously.

## Shared safeguards and future priority

- **A world history is not a population replicate.** Exact same-state forks isolate interventions for *that world*. Generality requires fresh independent starting worlds and larger environmental distributions.
- **Distribution matters:** report floor and ceiling occupancy, raw pre-clipping drift, mean energy, resource-action covariance, and time horizon. A high mean can coexist with failed cells.
- **Selection matters:** distinguish optimization-development seeds, first heldout seeds, post-selection fresh seeds, and actual prospective intervention sets. “New seeds” within the same generator are not out-of-domain validation.
- **Mechanism matters:** a hand-coded decision using energy, gradients, or hysteresis is not spontaneously learned cognition. A low-dimensional sigmoid neuron is not equivalent to the original 12-hidden-unit recurrent neural network.
- **Time matters:** a ranking at 800 or 5,000 ticks may reverse by 3,000, 10,000 or 20,000 ticks; no finite horizon establishes indefinite sustainability.

**Recommended next research loop:** predeclare a small policy set (`fixed .50`, `fixed .51`, neighbor-gradient, energy-rescue, selected neural learner) and jointly evaluate on one untouched family of independent seeds and deliberately varied benign world regimes with the same horizon, measurements, and information budget. Use prospective seed groups for selection and confirmation; do not re-optimize on the confirmation data. Then examine whether adding neural adaptation makes an incremental difference *on top of the strongest simple action-conditioned behavior*.
