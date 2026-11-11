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

## Macrostate society: thirteen recorded decisions, four substantive questions

`SOC_MACRO_probe.py` uses learned v0.1 trajectories projected into eight observable categories by three booleans (resource, energy, previous action). Its target is always the **next eight-category micro label**, which commendably prevents trivial information gain by shrinking both inputs and targets. The greedy merge path is chosen on training worlds only, with separate test seeds; the frozen three-label mapping was additionally evaluated on fresh confirmation seeds. This is a methodologically meaningful controlled exploration of information erased by projections.

However, the 13 table rows in `SOC_MACRO_REPORT.md` do not represent 13 unrelated conceptual burdens. I conservatively recognize **four substantive loops**:

1. How much next-micro prediction is lost as the currently observed partition is compressed? (One six-step greedy merge path, not six discoveries.)
2. Can one, two, or three lagged coarse states repair the lost information? (One history-depth experiment, not three distinct theories.)
3. Which single observable projection (resource, energy, action) carries most predictive signal? (One matched three-way ablation.)
4. Does the chosen three-label memory result survive separate untouched simulator seeds and aligned target time windows? (One frozen-mapping confirmatory test.)

The full eight-label reference row is an integrity/control measurement, not a fifth independent finding. Coarse TV defect varies with each partition and is not a direct monotonic index of lost prediction; exactly zero defect for the full eight-label identity mapping is vacuous. The eight visible bins are **not the complete Markov microstate**, and must not be named `C_num`, `C_struct` or `C_symb` without independent projection definitions.

The most defensible quantitative result is from the frozen-mapping confirmation: at aligned accessible target ticks, three-label current-only NLL `.82125` falls to `.79758` with three prior coarse states (gain `.02367` nats); a full-eight-label current model scores `.79093` on its different full window. The conclusion is predictive-memory repair within this synthetic generator, not proof of a minimal sufficient state or novel Markov theorem.

## Learning/evolution society: thirty-two searches are not endogenous evolution

`SOC_LEARNING_search.py` cycles 32 designer-chosen coordinate proposals over an initial action bias, a multiplier on recurrent weights, and offspring mutation scale, evaluated on the **same six development seeds** using a hand-selected score `(population/100)+mean_energy`. Only **two proposals** were accepted. The selected model has a manually reduced action bias and **mutation disabled**, with the recurrent gain unchanged. These 32 hyperparameter moves are one conceptual designer-optimization loop with 32 numerical design iterations, **not** 32 emergent adaptive generations.

Separate held-out tests over 40 untouched seeds address around **five genuinely different burdens**:

1. Whether the selected designer intervention repeats its ecological advantage beyond the six development seeds (population 84.93 vs 64.63 original); this intervention combines two changed parameters, so causal attribution remains partly confounded.
2. Whether turning mutation back on helps against the otherwise tuned clonal policy (82.85 vs 84.93 living cells): no established advantage; small paired effect and high variance do not prove mutation universally harmful.
3. Whether recurrent-memory matrix removal harms the tuned clonal policy (83.78 vs 84.93 living cells): weak evidence, not proof that meaningful event memory was used.
4. Whether a stronger non-neural fixed harvesting baseline still matches or exceeds the tuned neural design (85.65 living cells and higher mean energy): yes; no neural superiority established.
5. Whether the static action-response phenotype differs with resource input (tuned response sensitivity ~.01061 vs original ~.00257), distinct from proof of lineage-selected behavior or actual recurrent event recall.

These are separate **demographic world** experiments; do not compare their raw population/energy directly against fixed-occupancy Garden v0.1. Reproduction and inherited weight mutation are implemented but beneficial selection has not been demonstrated. The stronger next test is a matched history-swap or memory-reset experiment where genotype and local world state remain identical while only recurrent hidden state differs.

## Conservative society-count recommendation

| Society | Logged moves | Distinct substantive research loops suggested | Why |
| --- | ---: | ---: | --- |
| Adaptive | 40 OAT design + holdout + longer validation | **3** | One optimization burden, two distinct tests of generalization/horizon |
| Longitudinal | 25 configurations + fresh validation | **11** | ~8 policy-family burdens plus long-horizon, shock and independent validation; many repeated settings |
| Macro | 13 representations/history decisions + fresh confirmation | **4** | Coarse merge, history, projection, independent confirmation |
| Learning/evolution | 32 design steps + heldout controls | **6** | One designer search, five distinct causal/control questions |
| Independent review | 7 methodological probes, 52 small runs | **4** | Four substantive horizon/physics/shock research burdens; three other probes are integrity checks |

**Total conservative recommendation for these five societies: 28 substantive loops**, rather than adding every locally labeled search iteration or parameter proposal. This is an interpretation of evidence lineage, not an externally mandated ontology of what a research loop is. If the ledger prefers to record all 40, 25, 13 and 32 computational decisions, place them in a *separate nested iteration counter* and do not call them distinct intellectual discoveries. Distinguish all such counts from simulation ticks, independent seeded runs, and the user's remaining authorization.
