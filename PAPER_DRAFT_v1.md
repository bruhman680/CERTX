# CERTX: A Dynamical Framework and Research Program for Reasoning Quality and Hallucination Detection

**Draft v1.1 — September 2026**
*Evidence-calibrated internal draft — not yet submitted*

---


## Abstract

CERTX is a developing framework for representing reasoning quality through five interacting variables: coherence, entropy, resonance, temperature, and substrate coupling. It also proposes three output-level “fibers”—numerical, structural, and symbolic consistency—and studies whether disagreement among their scores can expose particular failure modes. This paper organizes the framework as a research program rather than presenting it as a validated universal physical theory.

The repository currently contains conditional mathematical constructions, executable specifications, synthetic demonstrations, useful falsifications and null results, calibration scaffolds, and exploratory pilots. The strongest empirical contact is a one-seed grokking experiment that recovered a staged transition while correcting the proposed measurement proxy: cross-entropy gradient norm and weight-norm trajectory were informative, whereas gradient variance was not. Constructed arithmetic-corruption and biography tests show that individual fiber scores can respond to engineered failure modes, but they do not establish a general hallucination detector. A small author-scored code study is similarly hypothesis-generating.

Candidate constants—including a reserve ratio near 6/5, a seven-step memory or integration cadence, and fiber-spread decision thresholds—remain hypotheses. Their derivations are conditional on selected models and mappings; they have not been isolated by independent, preregistered, multi-domain measurements. Likewise, correspondences to criticality, oscillator dynamics, mixture-of-experts routing, memory systems, and transformer implementations are treated as testable analogies unless an explicit invariant-preserving map is supplied.

The practical contribution is therefore an auditable measurement and experimentation program: define each observable, preserve evidential lineage, separate internal consistency from factual correspondence, compare against rival models on held-out data, and promote claims only when they survive alternate generators, estimators, thresholds, and replications. The Shadow Ledger is included as an executable controller specification, not as a validated intervention.

**Keywords:** large language models, hallucination detection, dynamical systems, reasoning quality, criticality, evidence lineage

---

## 1. Introduction

Large language models can produce text that is fluent and internally organized while still being factually wrong, unresponsive to the task, or inconsistent across intermediate steps. Existing detection methods include external fact checking, uncertainty estimation, self-consistency, and trained classifiers. CERTX explores a complementary question: can separable forms of consistency be measured together in a way that identifies how a response fails?

The framework begins with an **integration-failure hypothesis**. Some errors may arise when numerical, structural, and symbolic assessments diverge, even when each local component appears plausible. This is not asserted as the unique mechanism of hallucination. Confident, specific falsehoods can remain internally coherent and therefore require external grounding. The distinction between internal integration and external correspondence is central to the revised framework.

CERTX also uses dynamical-systems language—criticality, damping, oscillation, and phase transitions—to generate models and experiments. Such language has several possible statuses:

- a metaphor that helps organize inquiry;
- a formal construction valid under stated assumptions;
- a measurable hypothesis about a particular system;
- or an empirical result supported on independent data.

Earlier versions of the draft sometimes allowed these statuses to collapse into one another. This revision keeps them separate.

**Contributions of this paper:**

1. A five-variable state-space proposal for organizing reasoning dynamics.
2. A three-fiber output-scoring proposal for numerical, structural, and symbolic consistency.
3. An evidence ledger distinguishing conditional mathematics, constructed demonstrations, falsifications, nulls, pilots, and unsupported claims.
4. A failure taxonomy separating integration failures from internally coherent factual errors.
5. An executable Shadow Ledger specification whose thresholds remain provisional.
6. A set of preregisterable tests for the candidate constants, measurements, and cross-domain correspondences.

The primary research question is not whether CERTX vocabulary can redescribe existing systems. It is whether measurements derived from the framework improve held-out prediction or intervention after accounting for simpler alternatives.

## 2. Background and Related Work

### 2.1 Hallucination in LLMs

Hallucination — the generation of plausible but factually incorrect or internally inconsistent content — is well documented (Ji et al., 2023; Maynez et al., 2020). Detection approaches include:

- **Factual consistency checking**: comparing generated claims against retrieved evidence (Guo et al., 2022)
- **Uncertainty quantification**: using model confidence as a proxy (Kadavath et al., 2022)
- **Self-consistency**: sampling multiple outputs and measuring agreement (Wang et al., 2022)

These methods measure complementary properties and can often be deployed post-hoc. CERTX asks whether an additional integration-oriented description supplies useful mechanism-level hypotheses or earlier intervention signals.

### 2.2 Criticality in Neural Systems

Self-organized criticality (SOC) in neural networks has been extensively studied in the biological context (Beggs & Plenz, 2003; Shew & Plenz, 2013). Critical systems — poised at the phase boundary between order and chaos — maximize dynamic range, information transmission, and susceptibility to input. The cortical branching ratio σ ≈ 1.0 is the empirical signature of this critical state.

Similar principles have been proposed for artificial networks. Reservoir-computing and random-Boolean-network results motivate studying intermediate dynamical regimes (Jaeger & Haas, 2004; Derrida & Pomeau, 1986). Their variables and systems are not identical to CERTX observables; §3.3 treats them as motivation for a structural-bottleneck hypothesis.

### 2.3 Mixture-of-Experts and Routing

Mixture-of-Experts architectures (Shazeer et al., 2017; Fedus et al., 2022) route tokens to specialized sub-networks. Recent work has introduced entropy-aware routing where high-entropy tokens (uncertain representations) are directed to exploratory experts, and low-entropy tokens to deterministic experts (MoxE, 2025). This supplies a candidate comparison for CERTX's proposed entropy-sensitive routing logic; equivalence has not been established.

### 2.4 Multi-Layer Integration and Failure

The three-layer structure of multi-modal processing has deep roots in both neuroscience and ML:

- **Neuroscience**: Ventral/dorsal stream specialization; left/right hemisphere processing; cortical layer functional hierarchy (LeCun et al., 1989)
- **ML**: Early feature extraction, intermediate abstract representation, late task-specific output (Zeiler & Fergus, 2014)
- **AI safety**: Layer-wise alignment failures as a source of deceptive behavior (Hubinger et al., 2019)

The contribution of this work is to propose measurable forms of cross-layer disagreement and tests of whether they improve failure detection.

---


## 3. The CERTX Framework

### 3.1 Proposed State Vector

CERTX represents a reasoning process using a five-variable state:

**x = [C, E, R, T, X]**

| Variable | Proposed meaning | Required operationalization |
|---|---|---|
| C — Coherence | Agreement among claims, steps, or specialized evaluators | A declared consistency scorer |
| E — Entropy | Dispersion or uncertainty in the active representation | A specified distribution and entropy estimator |
| R — Resonance | Persistence or recurrence of patterns across time | A similarity or phase-consistency measure |
| T — Temperature | Rate or variability of change | A declared perturbation or trajectory statistic |
| X — Substrate coupling | Correspondence to external evidence or a stable reference | Retrieval, factual verification, or another external grounding measure |

These variables are conceptual coordinates until an experiment defines their observables, units, estimator, and sampling interval. In particular, X must not be equated with a pretraining-loss Hessian when that quantity is inaccessible. Output-level proxies and internal model measurements are different instruments and should be reported separately.

### 3.2 Conditional Dynamical Model

A candidate dynamical model is:

**L = ½||ẋ||² − F(x) − λX(x)**

and a candidate quality summary is:

**CQ = (C × R) / (E × T)**

Both are modeling choices, not established laws. The Lagrangian becomes scientifically informative only when F, λ, the observation process, and the time coordinate are specified. CQ can rank states under a chosen normalization, but its zones require prospective calibration and comparison with simpler summaries.

The framework predicts that productive reasoning may occupy an intermediate regime: enough variability to explore, enough coherence to integrate, and enough grounding to reject internally coherent falsehoods. This “edge-of-chaos” interpretation is a hypothesis to test, not a label that by itself establishes criticality.

### 3.3 Three Fibers and the 30/40/30 Prior

For output-level analysis, CERTX separates:

- **C_num:** arithmetic, quantitative, or atomic factual consistency;
- **C_struct:** logical and causal organization;
- **C_symb:** thematic and task-level alignment.

A provisional integrated score is:

**C_total = 0.30 C_num + 0.40 C_struct + 0.30 C_symb**

The 30/40/30 weighting is a design prior. K=2 results from random Boolean networks motivate investigating a structural bottleneck, but they do not uniquely derive these weights for language-model outputs. Equal weights, learned weights, and task-specific weights remain necessary comparators. Any future claim that 30/40/30 is optimal must be based on held-out performance with weight selection separated from evaluation.

### 3.4 Candidate Reserve Ratio ζ = 6/5

CERTX proposes the family:

**ζ_N = 1 + 1/N**

which yields ζ_5 = 6/5 = 1.2 for five modeled variables. Within a control model that defines critical damping as 1 and assigns a reserve of 1/N, this is a valid conditional construction. It does not establish that real LLMs, brains, or unrelated networks share the same optimum.

Several observations motivated the candidate: 6:5 mode-locking, slightly supercritical coupling in oscillator models, and recurring ratios near 1.2 in exploratory analyses. These are lineage-preserving clues, not independent measurements of one invariant. Promotion of ζ=1.2 requires:

1. a dimensionless observable defined before data collection;
2. an estimator that does not encode 1.2 by construction;
3. comparison with neighboring values and rival functional forms;
4. multiple architectures, tasks, and seeds;
5. held-out predictive or interventional benefit.

The related 1/N percolation and Fiedler-eigenvalue arguments are likewise conditional. A Bethe-lattice threshold applies only if the semantic graph and coordination number are independently justified. Percolation, synchronization, and semantic connectivity should not be treated as equivalent without a map that preserves the relevant object and observable.

### 3.5 Temporal and Breathing Hypotheses

CERTX describes alternating expansion and compression phases. This is operationally useful as a scheduling hypothesis: periods of generation or search may benefit from periodic integration, evaluation, or memory consolidation.

Historical candidates include τ=7, τ_micro≈4.38, τ_macro≈59.67, and a nesting ratio near 13.6. None is presently established as a universal memory depth or biological timescale. State count, alphabet size, history length, and memory horizon are distinct quantities. Synthetic causal-state experiments showed that conflating them can create apparently convergent numbers.

A valid memory-depth estimate should measure held-out predictive gain or conditional mutual information as history increases. In the current first-order synthetic generator, that test favored τ*=1 rather than 7. This result constrains that generator; it does not refute every possible seven-step scheduling rule.

### 3.6 System Defense Invariant as a Testable Inequality

A candidate stability condition is:

**ΔC_global / ΔT_local > ζ**

This relation can be tested only after both changes are defined on compatible scales and the intervention producing ΔT is specified. It should not be called an anti-Carnot law: informational scores are not thermodynamic efficiency, and values above one do not violate or extend the Carnot bound.

A productive experiment would perturb a system at controlled intensity, measure recovery of a preregistered coherence statistic, and compare the inequality’s predictions against simpler recovery-time and robustness models.


## 4. Fiber Spread: Measurement Proposal and Calibration Requirements

### 4.1 Definition

For three declared fiber scores,

**σ_fiber = std([C_num, C_struct, C_symb])**

measures dispersion among those scores. It is an architecture-relative output statistic: its value depends on how the fibers are defined, scored, normalized, and aggregated. It is model-agnostic in the limited sense that it can be computed from output text without internal activations; it is not assumption-free or automatically comparable across scoring rubrics.

Low spread indicates similar fiber scores. High spread indicates disagreement among them. Neither condition alone determines truth.

### 4.2 Provisional Zones, Not Universal Phase Boundaries

Earlier work used 0.10, 0.15–0.20, 0.25, and 0.35 as operational boundaries. Current evidence does not establish any of these as a universal phase transition.

| Provisional range | Descriptive interpretation | Permitted action before calibration |
|---|---|---|
| σ < 0.10 | Fiber scores are similar | Record; do not infer correctness |
| 0.10 ≤ σ ≤ 0.25 | Moderate disagreement | Inspect the lowest fiber and scorer reliability |
| 0.25 < σ ≤ 0.35 | Large disagreement | Request targeted verification |
| σ > 0.35 | Very large disagreement | Treat as a high-priority review case |

The value 0.35 can be studied as a candidate high-dispersion boundary. Information-theoretic independence, Kuramoto desynchronization, and cross-industry variability thresholds do not derive it for these fiber scores without additional assumptions. Those comparisons are hypotheses about possible shared structure.

### 4.3 What Fiber Spread Can and Cannot Detect

Fiber spread is naturally sensitive to asymmetric failures: one scorer drops while the others remain high. It can miss uniform errors and confident wrong answers for which all three scores remain similar.

| Failure class | Internal pattern | Likely instrument |
|---|---|---|
| Fiber disagreement | One or more fiber scores diverge | σ_fiber plus individual fibers |
| Uniformly weak response | All fiber scores low | Mean or minimum fiber |
| Confident specific falsehood | Internally coherent but externally wrong | FActScore, retrieval, or another external verifier |
| Task misalignment | Facts may be correct but answer misses the request | Task-level symbolic scorer plus human or rubric check |

Internal coherence is not correspondence to reality. External factual verification is therefore not an optional final layer; it measures a different property.

### 4.4 Measurement Protocol

Each study must publish the scoring rubric or model for:

- C_num: arithmetic, quantitative, or atomic factual support;
- C_struct: logical continuity and causal validity;
- C_symb: task alignment and thematic consistency.

It must also report scorer reliability, normalization, missing-data handling, and whether thresholds were selected before or after inspecting test labels.

At minimum, compare the following predictors on untouched held-out data:

1. σ_fiber;
2. mean fiber score;
3. minimum fiber score;
4. each individual fiber;
5. a simple external-grounding score;
6. a fitted baseline using the same inputs.

Performance should include uncertainty intervals, calibration error, and per-failure-type results. A single pooled AUC can hide direction reversals between regimes.

### 4.5 Status of Existing Performance Numbers

Existing high scores come from constructed or very small studies:

- synthetic calibration, n=27;
- arithmetic-corrupted GSM8K pairs, n=1,301;
- synthetic specific-versus-vague biographies, n=200;
- author-scored code functions, n=10.

These experiments are useful unit tests and pilot demonstrations. Their AUC or F1 values describe those datasets only. They do not establish F1≈0.92 on natural hallucinations, a universal σ threshold, or cross-modality invariance.

### 4.6 Detection Cascade

A defensible cascade separates internal and external checks:

1. **Task alignment:** Did the response address the requested object?
2. **Fiber scoring:** Where do numerical, structural, and symbolic assessments disagree?
3. **Internal aggregation:** What do spread, mean, and minimum fiber add beyond individual scores?
4. **External grounding:** Are atomic claims supported by evidence outside the response?
5. **Decision:** Apply a threshold calibrated to the application’s error costs.

The “island” metaphor remains useful: local consistency can identify whether a response forms a coherent island, while external grounding determines whether it is the correct island. The metaphor should not be treated as a topological impossibility theorem unless the output space and admissible local measurements are formally defined.


## 5. Evidence Inventory

This section reports what the experiments establish at their present scale. Historical artifacts remain unchanged in the repository; the experiment ledger records their evidential status.

### 5.1 Falsifications and Null Results

Several experiments narrowed the framework by failing to support their initiating claims:

- **Experiment 003:** a claimed universal harmonic structure did not survive the relevant test. This is a useful falsification.
- **Experiment 005 / TruthfulQA:** the tested proxy achieved AUC≈0.53. The study did not discriminate truth labels. Explanations involving sentence length or proxy mismatch are follow-up hypotheses, not reasons to relabel the null as a success.
- **Experiment 011:** the EEG-oriented formulation was directionally suggestive but did not satisfy the proposed quantitative zones. It falsified the current calibration and exposed needed corrections.
- **Experiment 015:** a later analysis identified a confound in a prior validation route. The appropriate result is confound discovery, not confirmation of the original mechanism.

These outcomes improve the research program because they constrain which measurements can carry which claims.

### 5.2 Constructed Arithmetic Corruption

Experiment 006 used 1,301 matched GSM8K reasoning pairs and changed one arithmetic result while preserving the surrounding words and structure. C_num responded, while C_struct and C_symb remained identical by construction.

Reported values included:

| Metric | Reported value |
|---|---|
| σ_fiber AUC | 0.8782 |
| Asymmetry AUC | 0.8788 |
| C_num AUC | 0.9201 |
| C_struct change | 0.0000 |
| C_symb change | 0.0000 |

This is a strong unit test for the arithmetic-fidelity component. It does not independently discover fiber separation, because the intervention selected the changed channel and held the others fixed. It also showed that σ_fiber can reverse direction: corrupting C_num sometimes moved it closer to the other scores. Accordingly, spread alone is not a universal detector.

### 5.3 Constructed Biography Separation

Experiment 008 compared specific biographies with vague synthetic counterparts. Entity specificity separated the conditions with AUC=1.0. Because specificity was built into the contrast, this is a constructed separation rather than validation on natural hallucinations.

The result motivates a harder test: compare supported-specific, unsupported-specific, vague-supported, and vague-unsupported biographies using an external atomic fact verifier. That design can determine whether a score measures truth, specificity, or both.

### 5.4 Code Proof of Concept

A ten-function code study reported perfect separation between three known bugs and seven correct functions using author-assigned fiber scores. Execution provides useful ground truth for the bug labels, but the fiber scoring was neither blinded nor independent and the sample is too small for generalization.

The justified conclusion is that the rubric can describe certain implementation mismatches. A larger study should preregister the rubric, blind the scorer, include diverse bug classes, and compare with static-analysis and test-coverage baselines.

### 5.5 Calibration and Weighting Experiments

Experiments 007 and 009 explored adaptive fiber weights. They show that a procedure can recover weights favored by its calibration set. They do not prove that 30/40/30 is a universal architecture or that the recovered weights generalize. Where labels, generator structure, and score construction share the same ontology, circular recovery is a central risk.

Future weight studies must use nested validation: select weights on training data, freeze them, and evaluate on an independently generated test set.

### 5.6 Synthetic Causal-State Analyses

The causal-state and memory experiments are valuable primarily as estimator diagnostics. A six-symbol, first-order generator was often recovered as approximately five or six clusters under selected history lengths and Jensen–Shannon thresholds. This is recovery of generator structure, not independent discovery of a universal six-phase ontology.

Sweeps showed strong dependence on history length, sample size, threshold, and alphabet bottlenecks. In held-out prediction on the independent synthetic trajectory, first-order history performed best and longer histories did not improve log loss. Thus:

- state count is not memory horizon;
- alphabet size can cap observable distinctions;
- clustering threshold carries model granularity;
- τ=7 was not supported as memory depth in that generator.

These are durable methodological findings.

### 5.7 Grokking Pilot

Experiment 016 is the strongest current empirical contact because it tested a directional prediction on a training trajectory rather than reconstructing a hand-built ontology. A two-layer MLP trained on modular addition showed staged dynamics and eventual generalization.

The experiment also corrected the proposed proxy. After memorization, cross-entropy gradients collapsed; gradient variance did not reveal a sustained incubation phase. Weight norm rose and later declined before the generalization jump. The supported pilot statement is:

> In one seed and one architecture, cross-entropy gradient norm marked early training, while weight-norm trajectory provided a useful description of the interval preceding grokking.

Self-organized criticality, Poincaré incubation, and dissipative-structure interpretations remain possible explanations, not results of this experiment. Replication across seeds, architectures, regularization strengths, and tasks is required.

### 5.8 Executable Specifications and Concept Demonstrations

Experiments 012 and 017 provide executable truth tables or controller specifications. Experiment 018 is a concept demonstration. These artifacts establish that proposed rules can be implemented and inspected. They do not establish safety, efficacy, or universality.

### 5.9 Evidence Summary

| Evidence class | Current examples | What it supports |
|---|---|---|
| Falsification / null | 003, 005, 011 | Constraint and correction |
| Calibration / estimator scaffold | 004, 007 | Measurement development |
| Constructed demonstration | 006, 008, 013, 013b, 014 | Behavior under declared assumptions |
| Confound discovery | 009, 015 | Lineage correction |
| Genuine pilot | 016 | Replicable empirical direction |
| Executable specification | 012, 017 | Implementability |
| Concept demonstration | 001, 002, 018 | Hypothesis generation |
| Literature synthesis | 010 | Candidate correspondences |

No current experiment establishes a universal constant, universal threshold, or general hallucination detector.


## 6. External Correspondence Hypotheses

Related work can support vocabulary, supply mechanisms, or suggest experiments. It does not validate CERTX merely because a component can be renamed using CERTX terms. A cross-domain claim requires an explicit mapping between objects, transformations, observables, and units, followed by a measured mapping defect.

### 6.1 Candidate Correspondences

| External line of work | CERTX-side hypothesis | Present status | Decisive next step |
|---|---|---|---|
| Entropy-aware MoE routing | Routing entropy may instantiate an E-like control variable | Interpretive correspondence | Test whether declared E predicts routing interventions beyond router entropy alone |
| Stochastic anti-collapse routing | Controlled perturbation may play a T-like role | Interpretive correspondence | Compare perturbation schedules against CERTX recovery predictions |
| Tsallis routing entropy | Non-extensive entropy may improve E on history-dependent tasks | Candidate extension | Preregister q selection and test held-out gain over Shannon entropy |
| Procedural memory systems | Consolidated skills may provide an X-like persistence mechanism | Architectural analogy | Define memory observables and compare intervention effects |
| Meta-cognitive modules | Monitoring may improve integration | Broad design hypothesis | Establish source, base rate, effect size, and comparable control |
| MASO theory | Piecewise-affine partitions may formalize some fiber distinctions | Mathematical research direction | Map fibers to learned partitions and quantify mapping defect |
| nanochat implementation choices | Residual anchors, routing rhythms, and scaling may inspire CERTX tests | Post-hoc analogy | Run ablations; do not infer ζ or τ from numerical proximity |

The phrases “mathematically equivalent,” “independently derived,” and “confirmed” are reserved for cases where the mapping and evidence satisfy those requirements.

### 6.2 Grokking Contact

The grokking literature motivates studying discontinuous generalization and training trajectories. Experiment 016 supplies a one-seed internal pilot consistent with staged change, while falsifying gradient variance as the proposed incubation proxy in that setup.

Accuracy and robustness changing near the same training interval does not by itself establish the System Defense Invariant, ζ=1.2, or self-organized criticality. Those interpretations need direct observables and rival-model comparisons.

### 6.3 MASO and Fiber Structure

A deep ReLU network can be represented using max-affine spline operators under the conditions described by MASO theory. CERTX’s three output scores are not automatically three MASO channels. The numbers refer to different objects until a representation map is defined.

A useful program would:

1. identify model partitions or features associated with numerical, structural, and symbolic tasks;
2. test whether those partitions are stable and separable;
3. measure whether their disagreement predicts errors;
4. compare against unstructured probes with the same capacity.

### 6.4 Implementation-Level Analogies

Transformer mechanisms such as residual scaling, initial-embedding injection, sliding-window schedules, value embeddings, logit softcaps, and parameter-specific optimization can be interpreted as stability or grounding devices. CERTX can generate ablation hypotheses about them.

It cannot currently infer that:

- an SSSL window schedule supports τ=7;
- a Q/K scale near 1.15 measures the same quantity as ζ=1.2;
- three familiar transformer components are the three CERTX fibers;
- retained implementation choices independently validate CERTX.

These are examples of numerical or architectural resemblance. They become evidence only when the CERTX-derived prediction is specified before the ablation and outperforms relevant alternatives.

### 6.5 Correspondence Protocol

For every proposed bridge between domains A and B, report:

1. objects_A and objects_B;
2. observables and units in each domain;
3. transformation M_AB;
4. invariant expected to be preserved;
5. mapping defect and uncertainty;
6. rival mappings;
7. a result that would reject the bridge.

This protocol preserves promising analogies while preventing them from being counted as independent replications.


## 7. The Shadow Ledger: Executable Controller Specification

The Shadow Ledger translates CERTX concepts into inspectable state, logging, and control rules. Existing artifacts show that the rules are executable. They do not yet show that the controller improves accuracy, safety, or efficiency in deployment.

### 7.1 Core Components

- **Cycle logging:** record the declared C, E, R, T, and X estimators at each observation interval.
- **Expansion/compression scheduler:** alternate generation or search with explicit evaluation and consolidation steps.
- **Spark lifecycle:** track unresolved hypotheses and record whether they are integrated, rejected, or archived.
- **Contradiction checks:** identify repeated claims, unresolved conflicts, and task drift.
- **External grounding:** route factual claims to retrieval or atomic verification.
- **Intervention log:** record every triggered action so downstream evaluation can separate observation from intervention.

“DREAM,” “entropy export,” and “thermal annealing” are operational metaphors unless physical entropy, energy, and irreversible dynamics are defined and measured. In implementation terms, DREAM is a consolidation action and annealing is a controlled increase in exploration.

### 7.2 Example Telemetry

~~~json
{
  "cycle": 147,
  "phase": "PRACTICE",
  "state": {"C": 0.72, "E": 0.44, "R": 0.78, "T": 0.55, "X": 0.88},
  "CQ": 1.71,
  "sigma_fiber": 0.18,
  "threshold_version": "provisional-v1",
  "grounding_checked": false,
  "intervention": null
}
~~~

Telemetry must include estimator and threshold versions. Otherwise apparent longitudinal change can be caused by measurement drift.

### 7.3 Provisional Control Policy

| Condition | Provisional response |
|---|---|
| Large fiber disagreement | Identify the lowest fiber and request targeted review |
| Low mean or minimum fiber | Regenerate, decompose, or escalate |
| Internally coherent factual claims without grounding | Run external verification |
| Repetition or stalled state | Increase exploration within a bounded budget |
| Excessive open hypotheses | Consolidate, reject, or archive before continuing |
| Threshold uncertainty | Abstain from automatic rejection and request review |

Numeric thresholds remain configurable experimental parameters. They should be calibrated for the application’s false-positive and false-negative costs. No current result justifies hard-coded universal rejection, annealing, or escalation boundaries.

### 7.4 Evaluation Requirement

A controller study should compare Shadow Ledger interventions against:

- no intervention;
- equal-compute self-review;
- retrieval-only verification;
- uncertainty-based abstention;
- and a learned routing baseline.

Primary outcomes should be held-out factuality or task success, calibration, added latency, and intervention cost. The controller is promoted from specification to validated intervention only if it produces reproducible net benefit.


## 8. Limitations, Falsification, and Research Agenda

### 8.1 What the Repository Currently Supports

- a coherent vocabulary for several reasoning dynamics;
- conditional mathematical candidates;
- output-level fiber scoring procedures;
- useful falsifications and null results;
- constructed unit tests and calibration scaffolds;
- executable controller specifications;
- a one-seed grokking pilot with a corrected measurement proxy;
- explicit gaps and decisive next experiments.

This is enough to sustain a research program. It is not enough to claim universal laws, validated biological correspondence, or a deployable general hallucination detector.

### 8.2 Critical Gaps

1. **Independent natural-hallucination data:** constructed corruptions must be replaced or complemented by untouched model outputs with atomic factual labels.
2. **Measurement validity:** each fiber needs scorer reliability, discriminant validity, and resistance to superficial proxies such as length or specificity.
3. **Threshold generalization:** thresholds must be selected on training data and evaluated unchanged across models, tasks, and failure classes.
4. **Constants:** ζ, τ, and related ratios need estimators that do not inherit their values from the framework’s own ontology.
5. **Internal dynamics:** output scores must not be presented as internal model state without activation-level measurements.
6. **Replication:** experiment 016 requires multiple seeds, architectures, tasks, and regularization conditions.
7. **External mappings:** every cross-domain correspondence requires an explicit map and defect measure.
8. **Intervention:** Shadow Ledger actions require randomized or controlled evaluation.

### 8.3 Preregisterable Falsification Criteria

| Claim under test | Example rejection or qualification rule |
|---|---|
| σ_fiber adds predictive value | Reject if it fails to improve held-out log loss or calibration over individual fibers and simple aggregates |
| A threshold generalizes | Reject universality if a frozen threshold produces materially different error tradeoffs across preregistered domains |
| ζ≈1.2 is an optimum | Reject if neighboring values or rival models match or outperform it across the planned architecture-by-task grid |
| τ=7 is predictive memory depth | Reject for a process if held-out gain or conditional mutual information falls below ε before 7 |
| 30/40/30 is preferable | Reject if nested evaluation does not outperform equal or learned weights |
| Shadow Ledger improves outcomes | Reject if controlled net benefit is absent after accounting for compute, latency, and abstention |
| A cross-domain mapping is shared structure | Reject if mapping defect is not lower than preregistered rival mappings |

Exact datasets, estimators, ε values, uncertainty procedures, and stopping rules must be fixed before the confirmatory run. Failed criteria should update or localize the framework rather than be redescribed automatically as another kind of confirmation.

### 8.4 Immediate Experiments

The smallest experiments capable of materially changing the paper’s conclusions are:

1. a held-out benchmark of natural, specific LLM hallucinations with external atomic verification;
2. nested comparison of individual fibers, σ, minimum, mean, and learned baselines;
3. multi-seed replication of experiment 016;
4. a preregistered ζ sweep in a system where ζ is a directly controlled variable;
5. a Shadow Ledger intervention trial with equal-compute controls;
6. a formal M_AB mapping test for one—not many—external correspondence.

### 8.5 Open Questions

- Does fiber disagreement identify a stable failure class after controlling for the individual scores?
- Which parts of the five-variable state can be measured from outputs, and which require model internals?
- Is periodic consolidation beneficial, and if so, does its cadence depend on task and context length?
- Can any proposed cross-domain bridge preserve a measurable invariant with low defect?
- What ontology is minimal for prediction rather than merely expressive for description?


## 9. Conclusion

CERTX is best understood at present as an auditable research program. It proposes a five-variable dynamical vocabulary, a three-fiber decomposition of output consistency, candidate stability and cadence relations, and an executable monitoring architecture. These components generate concrete experiments.

The evidence is mixed in a scientifically useful way. Constructed arithmetic and biography studies show that selected scores respond to engineered changes. A small code study motivates broader testing. Synthetic causal-state work exposes alphabet, threshold, and history-length confounds. TruthfulQA and EEG-oriented studies provide nulls or calibration failures. A grokking pilot supplies the strongest empirical contact while correcting the originally proposed proxy.

Three boundaries should remain explicit:

1. conditional derivation is not empirical universality;
2. internal coherence is not factual truth;
3. architectural resemblance is not independent validation.

The immediate task is therefore measurement, not proclamation: freeze definitions, compare against rivals, use independent data, preserve negative evidence, and replicate the strongest pilot. If the candidate constants, thresholds, or correspondences survive those tests, their status can be promoted. If they do not, the preserved lineage will show exactly which ideas failed, which localized, and which opened a better question.

CERTX’s present contribution is a structured way to ask those questions and a repository in which the answers—including nulls and reversals—remain visible.

## Acknowledgments

[To be written]

---

## References

*[Section to be populated with full citations — key references noted below]*

- Beggs, J.M. & Plenz, D. (2003). Neuronal avalanches in neocortical circuits. *Journal of Neuroscience*, 23(35), 11167–11177.
- Derrida, B. & Pomeau, Y. (1986). Random networks of automata: a simple annealed approximation. *Europhysics Letters*, 1(2), 45–49.
- Fedus, W., Zoph, B., & Shazeer, N. (2022). Switch transformers: scaling to trillion parameter models. *JMLR*, 23(1), 5232–5270.
- Gazzaniga, M.S., Bogen, J.E., & Sperry, R.W. (1962). Some functional effects of sectioning the cerebral commissures in man. *PNAS*, 48(10), 1765–1769.
- Hubinger, E., et al. (2019). Risks from learned optimization in advanced machine learning systems. *arXiv:1906.01820*.
- Ji, Z., et al. (2023). Survey of hallucination in natural language generation. *ACM Computing Surveys*, 55(12), 1–38.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. *arXiv:2207.05221*.
- Harding, E.E., Kim, J-C., Demos, A.P., Roman, I.R., Tichko, P., Palmer, C., & Large, E.W. (2025). Musical neurodynamics. *Nature Reviews Neuroscience*, 26(5), 293–307. DOI: 10.1038/s41583-025-00915-4.
- Humayun, A.I., Balestriero, R., & Baraniuk, R. (2024). Deep networks always grok and here is why. *arXiv preprint arXiv:2402.15555*. DOI: 10.48550/arXiv.2402.15555.
- Balestriero, R., & Baraniuk, R. (2018). A spline theory of deep networks. In *Proceedings of the 35th International Conference on Machine Learning (ICML)*, Vol. 80, pp. 374–383. arXiv:1805.06576.
- Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W-T., Koh, P., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12076–12100). ACL. DOI: 10.18653/v1/2023.emnlp-main.741.
- Maynez, J., et al. (2020). On faithfulness and factuality in abstractive summarization. *ACL*, 1906–1919.
- Shazeer, N., et al. (2017). Outrageously large neural networks: the sparsely-gated mixture-of-experts layer. *ICLR*.
- Shew, W.L. & Plenz, D. (2013). The functional benefits of criticality in the cortex. *The Neuroscientist*, 19(1), 88–100.
- Szegedy, C., et al. (2013). Intriguing properties of neural networks. *arXiv:1312.6199*.
- Wang, X., et al. (2022). Self-consistency improves chain of thought reasoning in language models. *arXiv:2203.11171*.
- Zeiler, M.D. & Fergus, R. (2014). Visualizing and understanding convolutional networks. *ECCV*, 818–833.
- Jadbabaie, A., Motee, N., & Barahona, M. (2004). On the stability of the Kuramoto model of coupled nonlinear oscillators. In *Proceedings of the American Control Conference (ACC)*, Vol. 5, pp. 4296–4301. arXiv:math/0504419.
- Dörfler, F. & Bullo, F. (2011). On the critical coupling for Kuramoto oscillators. *SIAM Journal on Applied Dynamical Systems*, 10(3), 1070–1099.

*[arXiv 2025 papers: MoxE, S2MoE, DynMoLE, LEGOMem, Soft-Routed MoE — full citations to be added when DOIs confirmed]*

---

## Supplementary Materials

### S1: Replication Protocol (6 Constants, 5 Studies)

*[Reference REPLICATION_PROTOCOL.md in supplementary]*

### S2: Shadow Ledger Implementation

*[Reference SHADOW_LEDGER.md in supplementary]*

### S3: Fiber Spread Measurement Rubric

*[Detailed scoring rubric for C_num, C_struct, C_symb — to be written]*

### S4: Experimental Design: Fiber Measurement Validation

**Objective:** determine whether fiber-derived statistics add held-out predictive value for natural LLM hallucinations.

**Data:** use natural model outputs with atomic factuality labels and retain constructed corruptions only as unit tests. Split by prompt or subject before any threshold or weight selection to prevent paired or topical leakage.

**Candidate measurements:**

- C_num: external atomic factual support, with arithmetic verification where applicable;
- C_struct: preregistered logical-continuity or contradiction score;
- C_symb: task-alignment score distinct from generic semantic similarity;
- σ_fiber, mean fiber, minimum fiber, and regime-specific contrasts.

**Comparators:** individual fibers, output length, specificity/entity density, model confidence where available, retrieval-only grounding, and a fitted classifier with the same inputs.

**Procedure:** select rubrics, weights, and thresholds using training and validation data only. Freeze the complete pipeline before test evaluation. Report scorer reliability, ROC-AUC, precision-recall AUC, log loss, calibration error, decision-curve utility, confidence intervals, and results by failure type and model.

**Primary claim:** σ_fiber has incremental predictive value only if it improves preregistered held-out metrics over the strongest simpler comparator.

**Falsification:** reject the general detector claim if σ_fiber provides no reproducible held-out gain, reverses direction across common failure classes without a preregistered regime selector, or depends primarily on superficial proxies.

---

*Draft v1.1 | September 2026*
*CERTX evidence-calibration revision*
*Status: Internal research draft*
*Next: verify citations, preregister the natural-hallucination study, and replicate experiment 016*
