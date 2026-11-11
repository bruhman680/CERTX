# Open research-loop ledger — FRR v0.5 Neural Garden

**Authorization interpretation (user clarification):** The user initially granted **1,000 exploratory research loops**, then explicitly authorized **another 1,000**, making **2,000 authorized research loops in total**. This is not a target of 2,000 simulation runs. A *loop* is a genuinely new *orientation → artifact/probe → evidence → criticism → next orientation* movement. There is no user-imposed limit on the number of simulation cycles, tests, probes, or revisions **within** a loop. One experiment can contain many seeded simulation runs; those are not independent research loops. This ledger counts only loops actually performed and documented. Nothing here implies autonomous execution between sessions or permanent background agents.

**Repository:** `codex/frr-v05-explorations`; preserve original historical Garden and prior experimental baselines. Use new files for variants. Record failed hypotheses, configuration changes, and mismatched comparisons, not just positive outcomes.

## Actual completed movements

| Loop | Orientation / question | Probe / artifact | Observed outcome | Next pressure |
| --- | --- | --- | --- | --- |
| 001 | Can independent neural cells learn a local predictor? | v0.1 `garden.py`, learning/frozen trials | On-policy MSE improves, but resource management and energy degrade | Separate prediction from ecological success |
| 002 | Can reward shaping redirect harvesting without changing the world? | v0.2 `stewardship_garden.py`, fresh-seed comparison | Higher energy than v0.1, still poor long-run health | Contrast against simple conditional policies |
| 003 | Does changing metabolism enable a viable regime? | v0.3 `viable_garden.py` | Energy saturates near 1.0 for learned *and frozen* controllers | Don't attribute environment effects to intelligence |
| 004 | Is ecological viability impossible under original laws? | Constant-harvest mean-field derivation, threshold counterexample | Negative drift proven only for restricted homogeneous constant-rate policies; conditional harvesting performs well | Preserve resource–action covariance |
| 005 | How strong is the fixed heuristic? | 100-run threshold screen on fresh seeds | Threshold .55 best among five tested at 600 steps | Compare neural and rule-based under same seeds/horizon |
| 006 | Are prior neural variants' findings reproducible? | 100-run five-arm sweep, independent audit | Better predictive score does not guarantee energy; altered metabolism benefits frozen cells too | Matched same-world experiments |
| 007 | Why does v0.2 shift behavior? | One-step advantage analysis `ACTION_TIMING_MECHANISM.md` | Immediate raw reward boundary .252; shaped boundary ~.474; .55 policy more conservative | Test learned actions' actual conditioning |
| 008 | Can we eliminate cross-sweep confounding? | 1,000-run four-arm matched follow-up; `THOUSAND_RUN_REPORT.md` | Under same laws/seeds/horizon, .55 fixed policy energy .48557 vs v0.1 learned .00818 and stewardship .05884 at t600; last-100 raw drift slightly negative | Test much longer horizon before calling any policy sustainable |
| 009 | Is high energy at t600 stable over longer times? | 120 long-horizon exploratory simulations to t2000 | .55 no-shock energy declines .483 at t600 to .269 at t2000; with two shocks .116 to .042 | Treat finite-horizon retention separately from equilibrium |
| 010 | Can resource rebound imply population recovery? | 200 matched exploratory shock/control runs; `PERTURBATION_SHOCK_REPORT.md` | Resource recovers rapidly after shocks, energy does not; .55 t600 energy .484 no shock vs .117 shocked | Track distinct recovery times and energy histories |
| 011 | Can neural cells acquire useful resource timing if shown examples? | `IMITATION_CAPACITY_REPORT.md` supervised teacher-action pilots | Taught stochastic learner improves energy .0088→.2278 vs fixed rule .4805; explicitly supervised imitation, not independent discovery | Test autonomous action-aware objectives and held-out disturbances |
| 012 | Is inheritance enough to yield useful evolution? | `EVOLUTION_REPORT.md` inherited-weight population and matched clonal control | Mutation mechanism runs and lineage checks pass, but mutating neural population 45.75 living cells vs clonal 46.4, no fitness advantage | Separate inheritance from selected adaptive mutations |
| 013 | Can one historical Garden be watched and steered over time? | `LIVING_GARDEN.py`, paused persistent world at tick100, checkpoint/replay tests | State-restoring continuation and cooperative pause verified; initial world not yet viable | Preserve checkpoint privately; use logged interventions and forks |
| 014 | Is the exploration branch complete and safe to resume from? | GitHub branch inventory audit, Git blob SHA comparison, archived private checkpoints | All 56 readable local branch-root files matched remote blobs exactly; bulk raw 1,000-run rows are compressed on branch and plain rows privately archived; checkpoints excluded from public branch | Keep the complete inventory and restore instructions alongside the research records |

## Active branches of inquiry

- **Matched neural baseline:** same original world, 4 policies ×250 matched seeds ×600 ticks; one completed experimental loop with 1,000 simulation runs, not 1,000 research loops.
- **Action-aware adaptive neural policy:** can cells learn timing of harvest rather than a purely one-step policy?
- **Changing conditions:** test seasonality and scarcity shocks; keep these distinct from standard-world sweeps.
- **Explicit evolution:** separate birth/death, mutation, inheritance, genealogy from ordinary weight updates.
- **Verification:** seed-level comparisons, raw energy budgets, floor/ceiling fractions, exact source/config hashes, archive failures as well as successes.
- **Longitudinal primary:** maintain one restartable Living Garden as the historical subject, with logged interventions, branchable counterfactuals and slow observation. Controlled batch runs remain secondary scientific comparators.

## Boundaries / continuation contract

Open questions and promising intuitions can trigger additional loops without asking for fresh approval every time **within this user's broad research authorization**. Yet evidence outranks enthusiasm, and tool permissions, security restrictions, available runtime, compute budgets, and transparent reporting still apply. Work can be paused/restarted from artifacts; it is not guaranteed to execute while this chat is idle. Do not claim that all 2,000 research loops have happened. Only advance the numeric count when a substantive loop finishes, and append its lineage in the ledger.
