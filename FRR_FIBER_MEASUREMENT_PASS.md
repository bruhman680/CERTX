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
