# Social information, policy replacement, and eight-category memory

12 November2026, America/Chicago. Pinned source: `bruhman680/CERTX`, branch `codex/frr-v05-explorations`, commit `3204c81ebc6922d66b0ae2623ee83d629f11f3b8`, directory `NEURAL_GARDEN_V01`. This is a targeted intake and bounded offline reproduction, not a merge or continuation of either saved Garden. Zero language-model calls, remote pickle loads, paid endpoints, or canonical world changes occurred.

## What was actually checked

Fourteen source/report/data files were read. Every final copy in `sources/` matches its pinned Git blob SHA exactly; see `PROVENANCE.json`. Initial apply-patch copies had an extra trailing newline. Their first execution/results and exact executed source files are preserved under `replication/ATTEMPT1_*` and `executed_sources_attempt1/`. After correcting only that trailing byte to recover exact original blobs, the bounded reproduction was rerun. No semantic code repair was made.

- `ROW_CHECK.json` recomputes the complete SOCIAL2_LAG supplied summary from its24 seed/regime rows, representing192 arm deployments. The recomputed summary equals the supplied summary exactly. This is an arithmetic audit, not a rerun of all192 deployments.
- `replication/RESULT.json` reruns source seed11000 at both regrowth coefficients, all eight observation arms,1500 training and2000 evaluation ticks. Every retained500/2000 metric matches the original row with maximum absolute error0.0.
- The same result reconstructs the fixed-threshold macro experiment using all eight training seeds7200–7207 and eight test seeds8200–8207 at420 steps. Full-eight current NLL .4750146682727352, aligned three-label current NLL .4650057589828851, and three-prior-label NLL .0025850528224942173 all match the supplied result exactly.
- Exploratory new controls test a global clock and per-cell category recurrence. They were selected after reading the source, so they are explanatory diagnostics, not fresh confirmatory trials.

Code was inspected before import/execution. The imported source constructs fresh NumPy simulators; no `Garden.load` or pickle deserialization was called. All work is confined to this intake's `social/` subtree.

## Sharing observations is different from replacing a policy

`SOCIAL2_probe.py` makes copies of the trained policy coefficients `theta`, choosing a high-energy, low-energy, random neighbor, global permutation, or neighbor mean. It copies simultaneously from an unmodified donor array. The receiving cell retains its own resource and energy. Replacing weights can therefore discard a policy specialized to a different local state. The reported recurrent-copy result says such external replacement generally damaged stable-world mean energy; this review inspected the mechanism but did not reproduce that complete144-deployment copying study.

`SOCIAL2_LAG_probe.py` instead leaves every cell's learned coefficients fixed and changes the supplied resource feature. The action is a deterministic threshold on three features: transformed resource observation, own current energy, and bias. Although its class inherits `Garden`, this policy does not use the original seven-input/twelve-hidden recurrent controller during deployment. Its recurrent Garden arrays exist but are not on this policy's action path. The externally maintained history list supplies delayed observations. This is not learned communication or newly acquired neural memory.

Each supplement is a50/50 blend with current own resource. In the stable regime the source's twelve matched seeds all favor one-step-stale neighborhood mean over own-one-step averaging and global stale-cell permutation. Under regrowth .055 the respective counts are11/12 and12/12. I recomputed these counts from all supplied rows, and reproduced the complete seed11000 row. The stable spatial contribution is supported within these constructed conditions; it is not a universal social-learning advantage.

## Remaining controls matter

The neighborhood supplement averages four cells; the global placebo supplies one cell. Their marginal variance, noise and degree of averaging need not match. The fixed global permutation may include self or nearby cells; it is not a strictly distant-donor intervention. Thus a variance-matched shuffled-four-cell mean or local identity shuffle would discriminate spatial coupling more cleanly.

The randomly selected1–5-step lag is one shared lag index per whole-world tick, not independent lag noise for each cell. Its spatially shared temporal perturbation is another experimental choice. The source correctly keeps all data causal and pads unavailable history with initial resource, but the experimenter defines who and when to observe.

The five-step-old own-resource arm beats the main stale-neighbor arm on shifted-world mean energy and floor fraction in the supplied aggregate. This makes lag/phase structure a live competitor to social interpretation. Fresh information is not universally best across distinct controllers. The current data do not directly identify why a particular lag helps, and almost all shifted results remain near depletion.

Training is repeated deterministically per seed, with paired forks across arms. Twelve seeded worlds are the grouping unit;192 deployments,144 cells per world, and2000 correlated ticks are not192 independent replications or millions of independent observations. No significance claim or population-level causal law follows from the win counts alone.

## What the dramatic eight-category memory gain contains

The eight labels encode three thresholded bits: resource>=.48, energy>=.12, and last harvest. They are an observer's bins, not the complete physical Markov state: continuous fields, neighbors and neural recurrent activity are omitted. The three-label partition is trained on earlier data and frozen for this transfer. The predictor is an offline smoothed lookup table, trained on eight worlds and evaluated on eight other worlds, always predicting the same eight-way next category. Adding three prior labels means a four-label input including the current label. Aligned current/history windows avoid a simple transient-window advantage for the primary within-policy contrast.

The source appropriately warns that the learned and threshold policies induce different trajectories, occupancy and target entropy. Their absolute NLLs cannot rank learning algorithms. Empirical weighted within-fibre TV is not a proof of strong Markov lumpability. Neither these labels nor their memory gain measure `C_num`, `C_struct`, or `C_symb`.

The fixed-threshold reproduction gives a strong ordinary explanation for the large gain: late local periodicity. In the same eight heldout worlds, category equality at lag3 is .995553 over the full record and **1.0 after tick220**. Lag6 also reaches1.0 late; lag1/2 remain near one third. This checks the representation's local recurrence, not exact asymptotic periodicity of every continuous value or every possible world.

A global timestep-modulo3 lookup does not reproduce the low NLL: it gets approximately .65586, versus .002585 for local label history. That is consistent with distinct cells/worlds occupying different cycle phases. A common external clock is not enough; local history can reveal which phase a particular trajectory occupies. These controls use the same heldout worlds after inspection and are exploratory, not independently held-out confirmation. Their results are in `replication/RESULT.json` and `PHASE_CONTROL.json`.

The predictive memory therefore lives in the observer's retained label history and its readout. The threshold agent has no learning or new recurrent-neural memory. Environmental resource dynamics supply the repeated pattern. A stronger carrier diagnosis would manipulate history, physical phase, fields, or controller state separately; the current prediction results do not uniquely locate a general cognitive mechanism.

## Grounded uses for the computational-notebook Garden

1. Treat input delivery as a mechanism. A neighbor feature and a replay window are both experimenter-chosen observations. Their usefulness should be tested without labeling them an agent's discovery.
2. Separate readable information from replacement of the receiver. Exchanging observations, replaying prior text, transplanting a checkpoint, and changing learned weights are different interventions with different side effects.
3. Inspect phase before interpreting a history benefit as sophisticated memory. Predictable output loops can yield large statistical gains while adding no capability to act, retrieve files, or correct an error.
4. Match timing, amount, noise and variance in controls. A longer or smoother context is not necessarily a more informative one, and duplicated material can alter behavior without new facts.
5. Preserve actual world consequences and ancestry. This intake neither supplies a reward to the notebook model nor justifies adopting a harvest objective, a social-copy rule, or a memory summary there.

The most useful next synthetic test is a matched-radius/matched-variance spatial shuffle crossed with lag, with action-resource covariance and autocorrelation measured. The most useful transfer to the notebook study is observer-side design: distinguish current observations, own prior text, stored-file retrieval and actual action receipts. No positive result here establishes that a similar change will improve the135M model or its free behavior.
