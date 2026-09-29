# CERTX Experiment Status Ledger

**Branch:** `codex/evidence-lineage-audit`  
**Source lineage:** [`claude/plan-certx-architecture-ojiem`](https://github.com/bruhman680/CERTX/tree/claude/plan-certx-architecture-ojiem)  
**Prepared:** 2026-09-29  
**Scope:** Experiments 001–018 as committed at source commit `18b7e4eb86cfd0982b1b5a40376d574eb1cbb628`

> Preserve the exploration; calibrate the claim.

This ledger does not replace the experiment code, results, paper, Shadow Ledger, or original interpretations. It adds an evidential layer: what each experiment currently establishes, what remains useful, and what still requires independent contact.

## Evidence vocabulary

- **Established method:** Standard mathematics or statistics correctly implemented for its declared role.
- **Empirical result:** Measured on independently sourced or generated observations with a non-circular target.
- **Pilot result:** Genuine execution with limited scale, seeds, controls, or external validity.
- **Falsification / null:** A prediction failed under stated conditions; scientifically useful.
- **Synthetic demonstration:** Shows that a formula or pipeline behaves as constructed, not that nature or LLMs exhibit the behavior.
- **Conditional mathematics:** A conclusion follows after assumptions or parameters are supplied; it did not independently emerge.
- **Interpretive silhouette:** A productive analogy or cross-domain relationship awaiting a mechanism and discriminating test.
- **Unsupported claim:** The present evidence does not establish it, or the conclusion conflicts with the output.

These labels apply to claims, not to the worth of an experiment. One experiment may support several claims at different depths.

## Status by experiment

| Experiment | Evidence status | What currently survives |
|---|---|---|
| 001 Harmonics | Synthetic pattern / unsupported validation | A generative musical analogy. It does not establish universal `tau=7` or `zeta=1.2`; the dissonance classification and imported time ratios require independent justification. |
| 002 Stability reserve | Circular toy | The simulator scaffolding and perturbation-recovery question survive. The function returns `(N+1)/N` directly, so the claimed law is assumed rather than derived. |
| 003 Kuramoto | Valuable falsification | The simulated ratios do not approximate `(N+1)/N`; reported values include 1, 10, 18, and 13. Preserve this as a failed prediction and rebuild thresholds using finite-size Kuramoto baselines. |
| 004 Repository mesh | Uncalibrated prototype | Contributor-network analysis may become useful. Current healthy bounds are assumed; co-editing is not necessarily collaboration; aliases, time windows, isolates, and weighting matter. The semantic baseline is reversed because `git log` is newest-first while the first window is called the founding window. |
| 005 TruthfulQA | Valuable null | Surface proxies produced roughly chance discrimination. This is evidence that the observables are inadequate at this scale, not that hallucination has no fiber structure. |
| 006 GSM8K | Task-specific pilot / unit test | The arithmetic tag verifier works on matched corruptions. `C_struct` and `C_symb` are largely held constant by construction, so fiber independence was not discovered. Keep as a verifier test, not universal hallucination validation. |
| 007 Adaptive weights | Calibration scaffold | The train/calibration/test idea is useful. Math AUC was unchanged across weightings; structural improvement was tiny. Weight claims need nested validation, uncertainty, and independent data. |
| 008 Synthetic biographies | Constructed separation | Specific dates and entities were deliberately added to one class, causing `C_num` separation. Useful as a specificity-confound stress test, not factuality validation. Its own Regime A prediction failed. |
| 009 Local biography pipeline | Circular validation | `factscore_label` is passed directly into `C_num`, so the strongest asymmetry result inherits manually supplied labels. The 17-example threshold is calibrated and tested on the same corpus. Retain pipeline wiring only. |
| 010 Attention heads | Unresolved literature synthesis | Entered literature proportions disagree with the original prediction. Reframing it afterward as a lower bound moves the target. Requires source-by-source taxonomy and comparable operational definitions. |
| 011 EEG | Valuable falsification | Only 2 of 7 zone predictions succeeded; the CQ mapping and `zeta=1.2` prediction failed. Preserve the explicit `REFINE` verdict. |
| 012 Mixed corpus | Executable truth table | Manually assigned fibers make it useful for checking detector algebra and regime logic. It cannot validate universal thresholds or `min(fibers)` on independent observations. |
| 013 / 013b Dynamics | Conditional mathematics | The nonlinear playground survives. Phi does not naturally emerge in 013; in 013b it follows after a parameter ratio is set to phi. Do not label this independent emergence. |
| 014 Zipf deviation | Confounded synthetic signal | `D_z` partially separates vocabularies deliberately generated with different word pools. Slopes are far from the proposed Zipf regime; TMR fails. Compare against length, TTR, and lexical-diversity baselines on real outputs. |
| 015 `D_z` versus TTR | Valuable confound discovery | `D_z` is strongly related to vocabulary breadth in the constructed corpus. This improves interpretation and should constrain paper language. |
| 016 Grokking | Strongest genuine pilot | A real modular-addition training trajectory shows memorization, delayed generalization, post-peak weight-norm decline, and an honest partial verdict. One seed cannot establish universality; expand across seeds, architectures, optimizers, and controls. |
| 017 Wrapper | Executable specification | A hand-authored trajectory evaluated by related CERTX formulas checks controller arithmetic. It does not show that the wrapper improves an independently measured system. |
| 018 Prompt demo | Concept demonstration | The scripted state updates clarify intended interaction. No live LLM intervention or independent outcome is measured. |

## Strongest surviving core

The repository currently supports a research program more strongly than a universal physical theory:

> CERTX is a developing methodology for tracking heterogeneous signals during reasoning and learning, then testing whether their imbalance, trajectory, or coupling predicts independently measured failures or transitions.

Reusable components include:

1. Separating numerical/factual, structural, and semantic behavior rather than trusting one aggregate score.
2. Treating standard deviation across fibers as a descriptive imbalance statistic without assuming a universal cutoff.
3. Matched perturbation designs when manipulated and preserved variables are explicit.
4. ROC/AUC and held-out calibration when leakage and threshold reuse are prevented.
5. Arithmetic verification within arithmetic domains.
6. Kuramoto, graph-Laplacian, Fiedler, Dirichlet, and nonlinear-dynamics tools when their established assumptions are respected.
7. Trajectory measurements during actual learning, especially Experiment 016.
8. Preserving nulls, contradictions, and confounds through the Shadow Ledger.

## Claims still requiring independent evidence

The present repository does not establish:

- `zeta*=(N+1)/N=1.2` as a universal law;
- `tau=7` as a universal cognitive breathing period;
- 30/40/30 weights as mathematically derived or universally optimal;
- `C_symb < 1/N` as a universal hallucination floor;
- `lambda_2,crit=1/N` as a universal spectral boundary;
- `sigma_fiber > 0.35` as a calibrated cross-domain threshold;
- `min(fibers)` as a universal hallucination detector;
- CQ as a physically calibrated measure of cognition;
- the current Lagrangian/master equation as a derived law of LLM cognition;
- independent convergence when outputs may inherit the same prompts, assumptions, vocabulary, or source lineage.

These remain hypotheses, interpretive silhouettes, or experiment-generating conjectures.

## Priority path

1. Replicate Experiment 016 across seeds, widths, depths, optimizers, regularization levels, and a non-grokking control; predeclare transition criteria.
2. Rebuild fiber observables from independently scored factuality, contradiction/NLI, semantic coherence, and lexical baselines.
3. Use separate data or nested cross-validation for calibration, threshold selection, and final evaluation.
4. Repair Experiment 003 with finite-size Kuramoto baselines and multiple definitions of onset and healthy synchronization.
5. Repair Experiment 004 with chronological windows, contributor normalization, weighted temporal networks, null graphs, and outcome-based calibration.
6. Test `1.2`, `7`, `0.35`, `0.2`, and 30/40/30 against nearby alternatives.
7. Compare FRR/CERTX prompting with a simpler structured-reasoning prompt and an unprompted baseline on preregistered cases.

## Lineage rule

Historical code and results remain unchanged. Corrections belong in new commits, annotations, or successor experiments. A later result may downgrade an interpretation without erasing the path that produced it.
