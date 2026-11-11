# Cycle 1 — A two-timescale rule-belief controller

**Status:** Executed constructed experiment, 2026-11-11 UTC. This is an explicit algorithm, not neural meta-cognition or proof of FRR efficacy.  
**Code:** `hybrid_controller.py` (NumPy; imports deterministic 8-state rule generator from `change_detection.py`).

## Question

If fast observation history is retained while a slow belief/commitment layer chooses its interpretation, does a committed rule policy outperform a probabilistic mixture under rule change?

## Setup

The actual world is the eight-state parity register (last three true bits) with Bernoulli(.1) transition noise. The observer sees each true bit, predicts the next bit **before** it is revealed, and then updates beliefs over four known candidate laws. A rule switch from XOR3 to inverse-XOR3 occurs at an unknown uniformly chosen t=24..40; history is continuous across it. Null controls never switch. Runs: 500 switch and 500 no-switch independent length-64 episodes for each seed 7,17,29.

The *fast* state is explicit observation window `(x_t,x_(t-1),x_(t-2))`. The *slow* state is a four-rule Bayesian posterior updated through a symmetric hazard `.03`. The new hard-commit variant starts with XOR3 and requires the **same** most probable alternative rule to exceed posterior `.8` for three consecutive updates before changing its committed rule. This is a design choice informed by prior development diagnostics. To check the previously noticed mismatched-alarm problem, **the same actual commit event** is counted as a switch detection and as a no-switch false alarm. A subsequent review found and repaired a pending-candidate identity bug (three successive *different* alternatives could otherwise add to the same streak). After freezing the corrected algorithm, a fresh confirmation set used seeds 401/502/603; development seeds 7/17/29 and intermediate-review seeds 101/202/303 are not counted as the final confirmation. Because the design and threshold were selected on earlier experiments, this confirms only the corrected candidate on the same synthetic generator family.

Comparators: known-rule oracle, permanently frozen original rule, soft posterior predictive mixture, hard-committed rule. No neural model, weights, external memory, unknown-out-of-set rules, or observation corruption is included.

## Results (three seeds; means shown)

| Period | Oracle | Frozen | Soft belief mixture | Hard-committed rule |
| --- | ---: | ---: | ---: | ---: |
| Before switch | 90.06% | 90.06% | 85.31% | 89.91% |
| First five post-switch transitions | 90.04% | 9.96% | 40.67% | 10.53% |
| From sixth post-switch onward | 89.75% | 10.25% | 87.95% | 79.31% |

Hard commitment detected 99.6–100% of actual switches with median 8-transition delay on the new seeds. In never-changing worlds, at least one erroneous hard-rule commitment occurred in 1.4–2.4% of episodes across three seeds. Some switches also occurred spuriously before the real switch (1.2–2.0% of switch episodes). The same controller event was used for detection and false-alarm counting, although the observation windows and hazards differ between switched and unswitched worlds.

## Interpretation

The result reveals a genuine *tradeoff*, not a universal win for the hybrid:

- Before a switch, the hard-commit rule nearly matches the oracle and exceeds the uncertain soft mixture.
- Immediately after the switch it remains confidently wrong until enough evidence accumulates.
- Later the soft mixture predicts better (~88.2%) than the hard commitment (~79.7%) because it responds to accumulating posterior evidence before the delayed commit occurs.

This does not justify describing a hard commitment controller as generally better. It demonstrates that a fast explicit history and a slower cautious interpretive state can interact, and that confirmation policies trade false alarms against recovery delay. Different costs or switch frequencies could reverse the preferred policy.

## Open controls

Independently tune thresholds on training episodes then evaluate on held-out episode groups; add novel laws outside the four hypotheses, noisy observation histories (requiring an eight-state hidden-state filter), changing event costs, replay/weight adaptation, confidence calibration, and repeated switches. A slower persistent parameter state is a *proposed* third timescale, not part of this experiment.
