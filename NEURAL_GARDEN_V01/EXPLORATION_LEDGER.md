# Open research-loop ledger — FRR v0.5 Neural Garden

**Authorization interpretation (user clarification):** The user granted up to **1,000 exploratory research loops**, not 1,000 simulation runs. A *loop* is a genuinely new *orientation → artifact/probe → evidence → criticism → next orientation* movement. There is no user-imposed limit on the number of simulation cycles, tests, probes, or revisions **within** a loop. One experiment can contain many seeded simulation runs; those are not independent research loops. This ledger counts only loops actually performed and documented. Nothing here implies autonomous execution between sessions or permanent background agents.

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
| 008 | Can we eliminate cross-sweep confounding? | 1,000-run four-arm matched follow-up launched, raw resource/action metrics | **In progress** at ledger creation; do not predeclare outcome | Examine results and run robustness tests |

## Active branches of inquiry

- **Matched neural baseline:** same original world, 4 policies ×250 matched seeds ×600 ticks; this is one experimental loop with 1,000 simulation runs, not 1,000 research loops.
- **Action-aware adaptive neural policy:** can cells learn timing of harvest rather than a purely one-step policy?
- **Changing conditions:** test seasonality and scarcity shocks; keep these distinct from standard-world sweeps.
- **Explicit evolution:** separate birth/death, mutation, inheritance, genealogy from ordinary weight updates.
- **Verification:** seed-level comparisons, raw energy budgets, floor/ceiling fractions, exact source/config hashes, archive failures as well as successes.

## Boundaries / continuation contract

Open questions and promising intuitions can trigger additional loops without asking for fresh approval every time **within this user's broad research authorization**. Yet evidence outranks enthusiasm, and tool permissions, security restrictions, available runtime, compute budgets, and transparent reporting still apply. Work can be paused/restarted from artifacts; it is not guaranteed to execute while this chat is idle. Do not claim that all 1,000 research loops have happened. Only advance the numeric count when a substantive loop finishes, and append its lineage in the ledger.
