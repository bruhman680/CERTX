# FRR Measurement Pass: What the Fibers Preserve

**Status:** proposed experiment design, not a validated CERTX result  
**Branch:** `codex/evidence-lineage-audit`  
**Date:** 2026-09-29

## The pressure point

The three fibers compress an output into `F(text) = (C_num, C_struct, C_symb)`. Before interpreting this tuple as a detector or mechanism, specify the behavior it is meant to preserve: factual correctness, logical compatibility, topical continuity, prediction over a sequence, or response to external checking. These targets need not coincide.

The [experiment ledger](EXPERIMENT_STATUS_LEDGER.md) already records the relevant lineage:

- [Experiment 008](EXPERIMENTS/exp_008_regime_a_language_confabulation.py) scores dates, numbers, and names as a `C_num` proxy. These measure *specificity*, not whether the named facts are true. Its corpus varies specificity together with the constructed label.
- [Experiment 009](EXPERIMENTS/exp_009_sigma_fiber_factscore_pipeline.py) can pass a supplied `factscore_label` straight into `C_num`; the strongest separation on its 17 constructed examples therefore cannot independently validate factuality detection. Its [committed result](EXPERIMENTS/results/exp_009_results.json) reports asymmetry AUC 1.0 and fiber-spread AUC 0.6714 under that construction.
- [Experiment 012](EXPERIMENTS/results/exp_012_results.txt) gives manually scored fibers to examples designed around the proposed regimes. Multiple summary rules tie at AUC 1.0; the output itself calls the result an executable truth table.

This does not discard the three fibers. It asks whether an operational version retains the distinctions needed for a particular use.

## Candidate measurement contract

| Name in the model | Current proxy may capture | Distinction to check independently |
|---|---|---|
| `C_num` | Explicit dates, quantities, entities, or arithmetic tags | Specificity versus truth against an external reference |
| `C_struct` | Lexical continuity and simple contradiction cues | Readable transitions versus logical compatibility of claims |
| `C_symb` | Topic overlap within a passage | Staying on topic versus preserving intended meaning |

Keep the original fiber names as working handles. Record each actual scorer and version next to a result; do not assume a similarly named score measures the same construct across domains.

## First discriminating contact: truth × specificity

Construct or source passages in four cells: true and specific, true and vague, false and specific, false and vague. Hold subject, length, style, and number of atomic claims as closely as practical. A subject-level split keeps paraphrases and facts about one person out of both training and final testing.

1. Annotate atomic claims and verify their truth against recorded references. Allow `unsupported` and `unverifiable` as distinct outcomes; do not label mere vagueness hallucination.
2. Score specificity without the truth labels. Score factual accuracy from the references through a separate process. Keep both raw scores instead of inserting the target into `C_num`.
3. Measure the original fiber tuple and proposed asymmetry. Compare them with simple specificity-only, length, and entity-count baselines.
4. Decide thresholds and weights using training/calibration data only. Evaluate once on held-out subjects, report uncertainty, and include failures by cell.

**Possible failure:** a false, specific passage gets high `C_num` and a reassuring aggregate despite verified false claims. That outcome would locate a lost distinction in the present observable, not disprove every use of a numerical fiber.

**Possible survival:** after specificity is controlled, independently scored fibers still predict false claims better than the simple baselines on held-out subjects. This supports a scoped predictive result, not yet a mechanism or universal threshold.

## Second contact: preserve the path

Construct paired passages with similar whole-passage counts and topic words but different claim order or cross-sentence dependencies. Record a sequence of per-claim or per-sentence observations alongside the final three scores. Ask whether two passages treated as equivalent by the final tuple have different contradiction or verification outcomes over the path.

A one-step or whole-output summary may be adequate for one task and inadequate for another. If path information matters, test a trajectory-aware statistic against the original tuple on held-out pairs; do not automatically relabel the missing distinction as model memory.

## Three projections of one process

In the earlier A/B/C example, A, B, and C are *macrostates of one projection*. They are not `C_num`, `C_struct`, and `C_symb`. A more precise mathematical candidate uses one micro-dynamics `P` and three maps `Q_num`, `Q_struct`, and `Q_symb`, each merging states for a different declared purpose. Strictly, the fibers are the preimages of a map (the states it merges); `C_i` is a proposed *score of preservation* under that map.

For a hard projection `Q_i`, let `[u]_i` be the projected class of microstate `u`. One possible defect at horizon `t` is

```text
d_i(t) = max over u,v with [u]_i = [v]_i
         TV( row_u(P^t Q_i), row_v(P^t Q_i) ).
```

It asks whether states merged now have the same distribution over *their own projected future* after `t` steps. `d_i(1)=0` is the strong lumpability condition for this finite hard partition; `d_i(t)>0` locates a lost distinction. The marginal at one horizon is not the full visible-path law. A provisional toy score `C_i(t)=1-d_i(t)` is normalized here because total variation lies in [0,1]; it is not a calibrated CERTX measurement or evidence that three real cognitive mechanisms exist.

The [reproducible three-projection sandbox](EXPERIMENTS/three_projection_sandbox.py) uses eight states `(b0,b1,b2)` and three binary coordinate projections of the *same* transition matrix. A tunable coupling makes the future of coordinate `i` depend on a bit erased by `Q_i`. The coordinate labels are placeholders: permuting them changes no mathematics and says nothing by itself about numerical, structural, or symbolic cognition.

| Constructed case | One-step defects | Minimum score | Mean score | Score spread (population SD) |
|---|---:|---:|---:|---:|
| All exact | (0, 0, 0) | 1.000 | 1.000 | 0 |
| Only one fails | (0.4, 0, 0) | 0.600 | 0.867 | 0.189 |
| One approximate | (0.05, 0, 0) | 0.950 | 0.983 | 0.024 |
| All fail equally | (0.4, 0.4, 0.4) | 0.600 | 0.600 | 0 |

The script asserts the analytic one-step defects for all cases and shows that a refinement from `Q_0` to `(Q_0,Q_1)` repairs its one-channel failure in this construction. It also reports two-step defects. These vary with dynamics and horizon; a one-step ranking should not silently become an all-horizon claim.

The lesson for `sigma_fiber` is exact within this toy: *zero spread* occurs for uniform health and uniform failure. Minimum, mean, and spread answer different questions. No single statistic is an automatic detector. The toy checks the algebra and the measurement contract; it cannot validate CERTX on language.

For a real numerical/factual component, the preserved behavior may require an external observable or reference `g_num` rather than merely `P^tQ_num`. Structural preservation might concern dependency or transition relations; symbolic preservation might concern task-conditioned meaning. Each needs its own observation, cost, horizon, and legitimate `unknown` state. A shared formula is an optional scaffold, not an obligation to force unlike phenomena into identical scores.

## Further pressure: local preservation need not compose

The same sandbox now includes a separate joint-only construction. Let the source microstate be three bits `(a,b,c)`. In the next state, `a'` and `b'` are each individually fair coins, but their parity `a' XOR b'` equals the source bit `c`; `c'` is fair. Each one-bit projection is exact at every tested marginal horizon. Yet the joint projection `(a,b)` merges states with different source `c` and has the maximum one-step defect:

```text
(d_a(1), d_b(1), d_c(1)) = (0, 0, 0)
d_(a,b)(1) = 1
d_(a,b)(2) = 0
```

At the second horizon the joint *marginal* defect vanishes because `c'` was randomized. The first-step joint distribution, and potentially a visible path law, still carry information that the separate one-bit tests discard. The vector of *three scores* `(1,1,1)` is therefore insufficient to infer joint preservation. Observing all three coordinate *values* is a different, finer representation; in this eight-state construction their joint tuple identifies the microstate. Do not confuse a tuple of adequacy scores with the joint observation itself.

For CERTX this opens an **integration question** distinct from each component's health: can locally adequate numerical, structural, and symbolic descriptions be used together for a declared task? One might compare joint behaviors or check cross-component constraints. This is a mathematical reason to test integration; it does not establish that real language fibers have this form or supply a universal integration score.

### Refinement needs a fixed target

The original defect uses the same `Q` twice: once to decide which present states are grouped, and again to decide what future behavior is observed. Separate those jobs:

```text
d(A, O, t) = max over u,v grouped together by A
             TV( row_u(P^t O), row_v(P^t O) ).
```

Here `A` is the current abstraction and `O` is the declared target observable. If `O` stays fixed, refining `A` removes pairs from the maximum, so this worst-case defect cannot increase. In the sandbox's single-failure case, keeping the target at bit 0 while refining the current grouping from bit 0 to bits (0,1) changes the defect from 0.4 to 0. This is a scoped repair, paid for with a larger effective state.

If the target observation is refined at the same time, the numerical defects are not comparable by that monotonic argument. The joint-only construction makes this vivid: each one-bit self-defect is zero while the two-bit self-defect is one. This is no contradiction; the question changed. Record separately **what states are merged now** and **what future distinction must survive**. In factual language, the latter may be a reference-checked claim outcome that is not available from text alone.

### What the controlled cases do and do not establish

- They establish mathematical possibilities and expose insufficiencies in using spread alone or inferring global adequacy from local scores.
- They do not choose the correct observational lenses, costs, or thresholds for language.
- They do not show that a specific failure lies inside a model. A score can fail because of its observable, its abstraction, its target, its horizon, or its data construction.
- They preserve a useful residual: define the integration behavior before deciding whether a fourth score, pairwise tests, a joint projection, or a trajectory representation is needed.

## What the eight-state experiments clarify

The eight-state work is a *measurement analogy*, not a claim that an LLM output has eight hidden states or that the three fibers are Markov states. Its useful object is the many-to-one map: several underlying configurations or trajectories can receive the same visible description. A fiber scorer likewise maps a rich passage and its claim history to three numbers.

Three different adequacy questions follow:

1. **Present description:** If two passages receive similar fiber tuples, do they agree on the independently measured property at issue? A specific false claim and a specific true claim can have the same entity-count proxy. This is a present hidden distinction (an FRR shadow) relative to that scorer.
2. **Continuation:** Does the tuple retain what matters as a passage unfolds? The supplied eight-state shadow/echo construction agrees for one visible transition but separates over longer visible paths. For text, score successive claims and their cross-claim relations before assuming a whole-passage average preserves contradiction or correction.
3. **Intervention:** Does the tuple predict what happens when a source is supplied, a claim is challenged, or a sentence is replaced? A score that predicts passive labels need not predict response to checking. This requires a separately declared intervention and outcome; an output-only score cannot identify a model's internal mechanism by itself.

For a declared target `Y` and observable fiber tuple `F`, a practical sufficiency question is whether knowing the underlying passage details or path `H` changes prediction after `F` is known: `Pr(Y | F, H) ≈ Pr(Y | F)` on held-out cases. The approximation depends on the chosen target, population, horizon, and tolerance. It is a research test, not an identity supplied by the fiber definitions. For interventions `a`, ask the question separately for `Pr(Y^a | F, H)`; passive prediction does not grant interventional sufficiency.

The thermodynamic eight-state construction supplies a second warning: a two-state visible summary can report zero stationary current while an internal driven cycle dissipates. Its 100% hidden fraction depends partly on that two-state coarse-graining, and its normalized equilibrium chain does not have the stated Boltzmann distribution. Thus it motivates looking for process information erased by a score; it does **not** license calling fiber spread physical entropy production or reading hidden computational cost from three output scores.

### A minimal measurement translation

| Eight-state question | Fiber question | Direct check |
|---|---|---|
| What distinction did the quotient merge? | Did a proxy merge specificity with truth, or topic continuity with logical consistency? | Cross the properties independently and seek matched-score counterexamples. |
| Does agreement persist across horizons? | Do final scores conceal a contradiction, correction, or drift in the claim sequence? | Compare whole-output and time-resolved scores on paired passages. |
| Does a probe expose or create a difference? | Does checking against a source alter the measured outcome or the continuation? | Record pre-check output, probe, and post-check response separately. |
| Is the same visible result evidence of one mechanism? | Could different model processes produce the same three scores? | Compare rival baselines and interventions; keep mechanism claims open. |

The lesson is to measure the **behavior we ask the fibers to preserve**, then find a pair they currently treat alike that behaves differently. A repair may change a proxy, retain a path, or narrow a claim. It need not immediately add a fourth fiber.

## Interpretation boundary

Treat `F` as a proposed task-relative compression. Its adequacy depends on the observation, target, horizon, intervention family, and tolerance. If two cases with matched `F` differ on the declared target, locate the residual before adding dimensions or asserting an internal mechanism. Possible repairs include changing the scorer, retaining a verified truth channel, preserving the sequence, narrowing the claim, or refining the fiber partition.

This is an FRR intuition–artifact–pressure pass: the existing experiments generated useful measurement questions; a crossed and held-out design supplies pressure that their constructed examples could not. Historical code, data, and results remain unchanged.
