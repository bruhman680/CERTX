# Frozen plan — causal value of online policy updates versus exploration cost

**Frozen before executing any outcome-bearing NEXT_ONLINE experiment.** Separate research question from the preceding `NEXT_WELFARE_*` objective search. No further reward-shape tuning or policy selection based on this experiment.

## Burden / prediction

Previous results showed that continuing stochastic neural learning under an altered resource world often performed worse than freezing the trained weights, while freezing and deploying deterministically was far better. Is that because the *weight changes* are harmful, or because stochastic exploratory actions are costly?

Predeclared objective: `reserve_resource`, penalty `.3`, raw reward from the existing `WelfareGarden` prototype. Choose this based on the earlier independent mild-regime deterministic comparison; do not reselect if the result fails. No teacher examples. Original Garden resource/energy laws except for one marked mild regrowth change.

**Primary causal contrast:** trained online-updating stochastic vs exact trained frozen stochastic, identical initial theta, physical state, RNG stream, action-selection mode, same regrowth schedule. Their action streams may diverge *after* updates alter propensity; this is an intentional consequence of treatment. Evaluate differences as paired outcomes by world seed.

**Secondary diagnostic:** extract theta from online and frozen policies at t0, t1000, t2000 and t3000. Independently deploy each captured theta as a frozen *deterministic* policy from identical fresh initial conditions. Use the same validation seed at every checkpoint. This asks whether online weight updates improve competence *without exploratory actions during evaluation*, independently of the learners' experienced energy state. It does not prove online ecological benefit.

## Fully specified design

- Main study: **12 fresh matched train seeds 9600–9611**, per-cell grid 10×10, stable pretraining 1000 ticks, then 3000 online/frozen test ticks.
- Test world for both arms initialized at `train_seed+20000`; exact state and RNG match before treatment. `learning=True` only in online treatment, `learning=False` in frozen stochastic control.
- Regrowth schedule in test: `.06` ticks1–1000, `.055` ticks1001–2000, `.06` ticks2001–3000. Other original environmental coefficients unchanged.
- Capture full trained `theta` at checkpoint t0,1000,2000,3000 separately from each arm.
- Diagnostic evaluation: for each checkpoint/arm, initialize `WelfareGarden(seed=train_seed+40000, size=10, learning=False, deterministic=True, objective='reserve_resource', penalty=.3)` with the captured theta; evaluate 1500 ticks under two explicit environments: stable `.06` throughout, and mild `.055` ticks501–1000 with `.06` before/after. Every checkpoint uses the same evaluation seed, distinct from the main test-world seed. There are 4×2×2 deterministic diagnostic evaluations per train seed.
- Controls are not collapsed across modes: stochastic online/frozen raw world trajectories and deterministic frozen policy competence are reported *separately*.
- Outcomes: mean energy, energy-floor share (≤.01), raw pre-clipping energy drift/tail, harvest frequency, mean energy-weight coefficient. Primary paired metric = online minus frozen stochastic energy at main t3000, plus floor differences; secondary paired metric = online-updated vs frozen-theta deterministic deployment at checkpoints on identical validation worlds.
- No success criterion based solely on average energy. Report distribution/floor, seed variation, and paired win count; also note whether any stage approaches energy ceiling.

## Independent review holdout

Reserved **untouched audit seeds 9800–9811**, distinct from development seeds, to be executed by `/root/benchmark` after source and protocol are frozen. Do not inspect their outcomes or retune this experiment before the independent audit. Independent reviewer should test source hash, exact policy mode, and verify same initial physical state and action RNG.

## Threats and stop conditions

- Frozen-deterministic diagnostic results are **off-trajectory transfers**, not proof the original online ecological trajectory survived.
- Reward `.3` explicitly engineers resource conservation and low-energy reserve; not spontaneous moral preference or universal welfare.
- The simulator is synthetic; 12 seeds quantify only within-generator variability, not external scientific replication.
- Raw energy can differ from clipped observed energy; floor/ceiling must be reported.
- No modification of canonical `runs/living_world` nor any preexisting source file. All files prefixed `NEXT_ONLINE_`; no GitHub writes by this agent.
- If code or plan changes after execution, record them transparently rather than silently revising the frozen burden.
