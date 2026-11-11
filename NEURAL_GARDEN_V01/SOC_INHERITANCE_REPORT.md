# Inheritance society — acquired behavior versus genetic and memory controls

**Status:** Three substantive paired hypotheses plus a direct first-birth mechanism audit executed. Sources `SOC_INHERITANCE_garden.py`, `SOC_INHERITANCE_probe.py`, `SOC_INHERITANCE_causal.py`; complete 120 row-level simulation records in `SOC_INHERITANCE_results.json`, 20 exact first-birth comparisons in `SOC_INHERITANCE_causal_results.json`.

## Why a new model was necessary

The earlier `EvolutionGarden` inherited recurrent neural weights but performed **no within-life learning**. It cannot answer whether a cell transmits an acquired improvement to its offspring. This separately labeled variant uses an independent one-parameter neural threshold per cell, with teacher-free REINFORCE updates and optional delayed eligibility trace. The underlying demographic world uses the same local energy and resource equations as `EvolutionGarden`, except a deliberately logged regrowth change `.06 → .055 → .06` during ticks1001–2000 of 3000. It retains explicit death, reproduction cost, unique IDs and genealogy. **It is not the original fixed-occupancy Garden and its results must not be merged numerically with that world's results.**

Offspring have two selectable inheritance modes:

- **Acquired:** inherit the parent's *current, updated* threshold value. This is an engineered transmission mechanism, not a claim about biological inheritance.
- **Germline:** inherit the parent's unlearned threshold parameter, while each individual's within-life updates remain local and disappear at death.

Other controls isolate mutation σ=0 versus .025, eligibility trace λ=.97 versus 0, and no learning at all. Six arms share **20 matched fresh seeds 2600–2619**, 10×10 cells, 3000 ticks, identical population and environmental laws. Every run includes unique ID, checkpoints, full-state fingerprints and source SHA-256.

## Measured outcomes at tick3000

| Condition | Mean living population /100 | Mean energy /site | Mean living threshold |
| --- | ---: | ---: | ---: |
| Within-life learning, acquired threshold inherited, no mutation | **71.40** | .3563 | .425 |
| Within-life learning, only germline threshold inherited, no mutation | 68.65 | **.3605** | .439 |
| Acquired threshold inheritance, mutation σ=.025 | 71.30 | .3452 | .420 |
| Germline-only inheritance, mutation σ=.025 | **76.25** | .3506 | .435 |
| Acquired inheritance, **no eligibility trace** (λ=0) | 45.90 | .2035 | .232 |
| No within-life learning, germline clonal inheritance | 70.85 | .3522 | .436 |

### Hypothesis 1 — Does inheritance of acquired adjustments improve outcomes?

The acquired-inheritance model ended with **+2.75 living cells per 100** over germline-only inheritance, but the paired seed SD was **20.43** and it won only **12/20** seeds. Its mean energy was *lower* by .00421. This is a weak, non-robust difference; **no demonstrated fitness advantage from acquired transmission**.

### Hypothesis 2 — Does mutation help inherited adaptation?

With acquired inheritance, mutation σ=.025 versus σ=0 changed mean population by **−0.10** and energy by **−.0111**. The paired population SD was 16.61. Mutation is not shown beneficial in this arm. Interestingly, germline-only mutation had a higher mean population than germline-only clones (76.25 versus 68.65); this is a candidate follow-up, **not evidence of selected adaptive genetic mutations**, because we have not isolated genotype fitness, position effects, or historical chance.

### Hypothesis 3 — Does delayed reward memory matter?

Turning eligibility traces off while keeping learning enabled made the acquired model much worse: the trace-preserving controller had **+25.5 living cells** and **+.1528 mean energy** relative to the trace-free control, with wins in **20/20** paired seeds. The trace-free thresholds drifted downward to ~.232, encouraging aggressive harvest. This demonstrates that delayed reward handling matters **for this update rule**, not that the full recurrent neural network discovered a memory mechanism. Crucially, the **no-learning** baseline performed almost as well as the trace-preserving learner (acquired learned minus no-learning population +.55, SD 16.23; energy +.00409), so we have **not** shown that learning itself improves ecological fitness relative to a strong unchanging initial behavior.

### Mechanistic audit — Is an acquired threshold actually transferred?

The paired `SOC_INHERITANCE_causal.py` experiment starts acquired/germline worlds from identical states and RNG streams, then compares the *same first birth* across 20 fresh seeds. Before the birth, all environmental and action states matched. The acquired child received its parent's learned threshold while the germline-only child received its unlearned threshold; the child difference exactly matched the parent's acquired-minus-germline difference for **20/20** tests. Mean absolute difference was only **0.000264** at the early first birth. This verifies implementation semantics, **not any ecological advantage**.

## FRR interpretation and next pressure

**Inheritance ≠ adaptation ≠ selection.** We constructed explicit acquired-threshold transmission, proved it happens, and yet could not establish that it improves long-term population health. The strongest positive contrast was not between inherited variants but between **trace-preserving and trace-free** within-life learning; however no-learning did similarly well, which undermines any premature claim that the learned behavior was beneficial.

The next independent test should link **genotype → phenotype → number of viable descendants**, with controlled founder swaps, and separate learning-update advantage from inherited-parameter advantage. Test adaptation in a less lethal regime where cell lineage histories remain informative, alongside strong fixed-rule controls.
