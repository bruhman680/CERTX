# SEASONS2: longitudinal seasonal hysteresis and intervention timing

Pre-outcome plan. This is a controlled **single-trajectory-per-seed** study of repeated seasons, with matched counterfactual policy continuations. It does not resume or mutate the canonical tick-100 Living Garden.

## Hypotheses

1. Repeated scarcity and recovery seasons can induce path dependence: equal current regrowth does not imply equal energy and resource distributions, because stocks retain history.
2. Intervention timing is causal: switching to the same rescue policy *before* the first scarcity episode should differ from switching after prolonged scarcity.
3. A reactive rescue rule triggered only by observable low energy may be worse than pre-emptive intervention; this would limit claims that instantaneous observations fully substitute for history.

## Frozen design

- New independent initialized grids, 16 × 16, seeds 41100–41111; no reset of a trajectory during the 12,000-tick run.
- Physics identical to `garden.py` except explicitly scheduled exogenous regrowth: 0.06 for ticks 1–1500, 0.048 for 1501–3000, 0.06 for 3001–4500, 0.048 for 4501–6000, 0.06 for 6001–7500, 0.048 for 7501–9000, 0.06 for 9001–12000. No interventions change regrowth or resources.
- Fixed threshold `.51`, fixed reverse rescue `.535` for energy below `.12`, anticipatory switch to reverse rescue at tick 1400, delayed switch at tick 5500, reactive switch permanently when population depleted fraction exceeds .10, and oracle seasonal switch between reverse in scarcity and fixed in recovery.
- Fixed reverse rescue is a historical hand-coded rule, not a learned neural policy; oracle is provided true season timing and is **not** a fair autonomous learning competitor.
- Evaluate mean energy/resource, fraction depleted, and lower decile at all season boundaries plus 12000; report raw per-seed paired differences, change-recovery differences, and seeded fractions. No p-value claims.
- Independent multi-seed trajectories, not 12k independent replicates. The scripted counterfactuals share matched initial resource and energy conditions but diverge thereafter.

## Interpretation gates

Do not call transient recovery spontaneous improvement, social cognition, or learned memory. Distinguish pre-emptive policy advantages from oracle information. Do not replace the original Garden policy or lineage. These results suggest design pressures; they cannot certify indefinite viability.
