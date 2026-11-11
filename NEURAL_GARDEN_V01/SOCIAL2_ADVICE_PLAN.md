# Pre-outcome follow-up: non-destructive social observations

Hypothesis: preserving individually learned neural policy weights while providing fresh neighborhood resource observations may improve performance compared with both no advice and matched placebo observations. This is explicit designer-supplied communication, not learned messaging.

Every cell trains its own energy-aware three-feature policy for 1,500 stable ticks (`SOC_ENERGY_AWARE_policy.py`), then is evaluated with weight updates **off** and deterministic actions. Keep original world laws except tested stable regrowth .06 versus modest shift to .055. Fresh seeds 10800–10811; grid size 12; 2,000 post-training evaluation ticks, record energy and floor at 500 and 2,000 ticks. Same trained checkpoints forked for each advice mode.

Arms change *observation only*, leaving theta byte-for-byte untouched:
1. Own current resource observation (frozen/no communication).
2. Average own/current resource and current cardinal-neighbor resource (50:50).
3. Current resource and a current random-neighbor resource (50:50; source sampled once per cell, spatially local).
4. Average own resource with **globally shuffled** current resource (placebo matching mixing strength but without local topology).
5. Average own resource and **one-step stale** neighbor-average resource (freshness control).

Metrics include final mean energy, depleted fraction, lower-decile energy, and matched wins vs own-only and shuffled. No outcomes are assumed; local spatial mixing might reduce individual signal quality or erroneously change an action threshold. Shared observations are inputs, not new learned representations. The primary Living Garden and source policy remain unchanged.
