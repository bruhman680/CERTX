# Pre-outcome discriminating experiment: spatial signal or temporal smoothing?

`SOCIAL2_ADVICE_REPORT.md` observed better frozen-neural performance using one-step-stale neighbor resource observations, but global shuffling helped too. The follow-up isolates three possible causes: (a) own-resource temporal smoothing, (b) neighbor-specific spatial information, (c) generic perturbation of neural input by smoothing or arbitrary observations.

Fresh matched seeds 11000–11011, independently trained for 1,500 ticks in regrowth .06. Frozen neural parameters thereafter; 2,000 deployment ticks at regrowth .06 or .055. Each alternative observation is exactly 50% own *current* resource + 50% one supplementary observation except own-only. Same stable laws, deterministic actions, 12x12 torus. Arms:

1. `own_only`: current own resource (baseline).
2. `own_previous`: one-step-old own resource (non-social temporal averaging).
3. `neighbor_previous`: one-step-old mean cardinal-neighbor resource (main prior result).
4. `neighbor_current`: fresh mean cardinal-neighbor resource.
5. `global_previous`: one-step-old resource from a fixed random permutation of all cells (spatial placebo, same time lag).
6. `neighbor_older`: five-step-old mean cardinal-neighbor resource (temporal-lag control).
7. `own_older`: five-step-old own resource (non-social matched-lag control).
8. `neighbor_time_scramble`: randomly chosen 1–5-step-old neighbor averages each tick (temporal-coherence placebo; no future information).

At the first five ticks, unavailable history is padded by initial observed resource, explicitly identical across arms. Outcomes at 500 and 2,000 ticks: energy, energy-floor, resource, bottom decile, matched seed wins. If `neighbor_previous` dominates `own_previous` and `global_previous` across seeds, we have evidence for a spatial contribution *within this synthetic world*. If effects match or reverse, refrain from calling it social learning. No learned messaging, no editing canonical checkpoint.

