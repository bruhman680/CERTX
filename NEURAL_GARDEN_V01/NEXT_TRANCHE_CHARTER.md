# Neural Garden — next 200 research loops, evidence charter

**Status:** User authorized the next 200 research loops on 2026-11-11 (America/Chicago), continuing from 69 already documented substantive loops out of the wider 2,000-loop allowance. This charter is a plan and authority boundary, **not** a claim that 200 have run. Our explicit task is evidence-driven recursive inquiry. Do not count seeds, cells, ticks, routine parameter changes or tool calls as independent research loops.

## Shared questions and independent society roles

1. **Online welfare learning:** Can teacher-free neural policy updates improve several outcomes together (mean energy, depleted-cell fraction, raw energy drift, recovery) under changing environments, beyond a matched frozen copy and strong handcoded rules?
2. **Ecological mechanisms:** Does targeting resource-rich cells, spatial diffusion, observation delay or phase structure explain retention independently of total harvest counts?
3. **One living historical world:** Compare exact checkpoint forks without overwriting the canonical paused t100 world, including intervention provenance, memory continuity and recovery.
4. **Macro-memory and inheritance:** Distinguish actual learned memory and transmitted adaptive benefit from predictive phase proxies and mere parameter inheritance.
5. **Adversarial review:** Freeze comparator definitions, inspect outcome bias and causal controls; reject overstated claims and inflated loop counts.
6. **Predeclared benchmark:** Compare fixed .50/.51, exact energy-rescue, reverse rescue, neighbor-gradient and neural controllers on *untouched* seeds and bounded environmental changes across scales/horizons.

### Exact manual-policy baselines (avoid naming drift)

- `fixed50`: harvest iff local resource `R > .50`.
- `fixed51`: harvest iff `R > .51`.
- `historical_rescue`: harvest iff `R > .51 OR (E < .12 AND R > .485)`.
- `reverse_rescue`: nominal `R > .51`, but when `E < .12`, require `R > .535`.
- `neighbor_gradient`: harvest iff `R > .51 + .5*(neighbor_resource-R)`.

**Do not** mistake `SOC_ENERGY_AWARE_policy.ExplicitRuleGarden(rescue=True)`, which uses other cutoffs, for the historical rescue comparator. These are hand-designed nonlearning policies. They are candidate controls, not demonstrated universal optima.

## Measurement and lineage

- Match seeds, world laws, initial resources/energy, grid size and horizon across arms; distinguish deterministic and stochastic actions; report actual perturbations.
- Track mean energy **and** floor fraction, lower-energy quantiles, resource–action covariance, raw pre-clipping drift, shock recovery and seed-level variability. Equilibrium, viability, survival and aggregate prosperity are different claims.
- Preserve direct source/config SHA-256, package versions, novel code and raw results. When scripts optimize on development seeds, evaluation must use genuinely untouched seeds.
- Independently audit candidate improvements. A within-world observed advantage is not yet autonomous intelligence, biological relevance or an established universal law.
- Preserve the original `Garden` v0.1 model and canonical `runs/living_world` tick100 checkpoint (already privately backed up). All interventions operate on forked or freshly initialized worlds.

At tranche closure, append only **adjudicated, actually completed** loops to `EXPLORATION_LEDGER.md`; keep per-agent algorithmic iteration logs separately. Work does not continue automatically after the chat/runtime stops.
