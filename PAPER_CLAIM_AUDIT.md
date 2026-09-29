# CERTX Paper Claim Audit

**Target:** `PAPER_DRAFT_v1.md`  
**Audit branch:** `codex/evidence-lineage-audit`  
**Purpose:** classify the paper's consequential claims before any prose revision  
**Non-action:** this audit does not alter the paper or reinterpret historical experiment artifacts

## Verdict

The draft currently supports a **developing research program with explicit hypotheses, useful falsifications, calibration work, and one comparatively strong pilot**. It does not yet support a universal physical theory, a validated hallucination detector, or independent cross-domain convergence on fixed constants.

The main defect is not absence of useful work. It is **status compression**: conditional mathematics, synthetic demonstrations, exploratory pilots, null results, analogies, and unsupported mechanisms are often narrated together as established evidence.

This audit applies the vocabulary in `EXPERIMENT_STATUS_LEDGER.md`:

- Established method
- Empirical result
- Pilot result
- Falsification / null
- Synthetic demonstration
- Conditional mathematics
- Interpretive silhouette
- Unsupported claim

## Priority map

| Priority | Revision target | Reason |
|---|---|---|
| P0 | Abstract, contribution list, §§3.3–3.5, §§4.2–4.3, §8.1, conclusion | These locations carry the universal constants, detector performance, and convergence claims. |
| P1 | §§5.3–5.9 | These sections mix pilots, constructed tests, nulls, and validation language. |
| P1 | All of §6 | Most relationships are analogies or mappings, not independent validations. |
| P2 | §7 control rules and thermodynamic language | The implementation is useful, but its physical interpretation and thresholds are not calibrated. |
| P2 | Remaining architecture prose | Retain as hypotheses or design vocabulary with explicit status labels. |

## Claim ledger

| ID | Paper location | Claim family | Current status | Evidence carrier / defect | Maximum justified wording now |
|---|---|---|---|---|---|
| A01 | Abstract; §§3.3, 8.1; conclusion | ζ*=6/5=1.2 is a universal operating constant | Unsupported claim | No independent estimator or preregistered multi-domain test isolates the ratio. Numerical proximity across unlike quantities is not a shared mechanism. | “CERTX hypothesizes a preferred reserve ratio near 1.2.” |
| A02 | Abstract; §§4.2–4.3; conclusion | σ_fiber>0.35 is a derived universal phase transition | Unsupported claim | Threshold provenance is not supported by an independently calibrated dataset. | “0.35 is a provisional decision threshold requiring calibration.” |
| A03 | Abstract; §§4.3, 8.1; conclusion | Fiber variance detects hallucination at F1≈0.92 | Conditional mathematics / unsupported empirical claim | The value is a model-based or projected performance figure, not a reported held-out benchmark with uncertainty. | “The present model predicts F1 near 0.92 under stated assumptions.” |
| A04 | Abstract; §5.1 | Kuramoto order r≈0.41 is derived and validated | Conditional mathematics | The calculation follows only after assuming a particular coupling ratio and model mapping. Earlier flat-ρ behavior did not establish phase locking. | “A Kuramoto analogy yields r≈0.41 under the assumed mapping.” |
| A05 | Abstract; §§5.5, 8.1 | Code evaluation n=10, AUC=1.0 establishes cross-modality validity | Pilot result | Very small, author-scored sample; not an independent or blinded benchmark. | “A ten-item exploratory code pilot separated the constructed cases perfectly.” |
| A06 | Abstract; §6; conclusion | Multiple external domains independently converge on CERTX constants/mechanisms | Interpretive silhouette | Object mappings, observables, units, and defect measures are generally unspecified; several comparisons are post-hoc numerical or verbal similarities. | “Several literatures offer candidate analogies to test.” |
| I01 | Introduction | Hallucination is an integration failure rather than knowledge failure | Research hypothesis | The framework proposes this mechanism; current experiments do not distinguish it from rival mechanisms on independent data. | “CERTX models some hallucinations as integration failures.” |
| I02 | Introduction / contributions | The constants are theoretically derived rather than tuned | Unsupported claim | Derivations depend on prior architectural choices and cross-domain identifications that are not independently established. | “The framework motivates candidate constants from its assumptions.” |
| I03 | Introduction / contributions | GSM8K provides independent validation | Synthetic demonstration / task-specific unit test | The evaluation uses matched arithmetic corruptions; structural and symbolic channels are identical by construction while the numeric channel is manipulated. | “The GSM8K-derived corruption test checks whether the numeric-consistency component responds as designed.” |
| M01 | §3.1 | 30/40/30 weights follow from K=2 or a general law | Conditional mathematics / design choice | The weights can be used as an architecture choice, but available experiments do not establish uniqueness or universality. | “The current implementation uses 30/40/30 as a provisional weighting.” |
| M02 | §3.3 | A reserve law uniquely selects ζ*=1.2 | Conditional mathematics | The conclusion is conditional on the selected objective and constraints. | State assumptions and label the result a conditional optimum. |
| M03 | §3.4 | Scale invariance or fractal nesting is mathematically necessary | Unsupported claim | No proof connects the formal objects in the paper to the empirical system at the claimed generality. | Present as a proposed modeling principle. |
| M04 | §3.5 | 1/N, Fiedler values, Kuramoto criticality, and symbolic complexity are equivalent manifestations | Interpretive silhouette | Similar-looking thresholds belong to different objects and units; an explicit map preserving an invariant is missing. | List them as candidate correspondences, not equivalences. |
| M05 | §3.5 | τ_micro=4.38, τ_macro=59.67, nesting=13.62 are established system scales | Unsupported claim | Their empirical carrier and uncertainty are not established in the committed evidence set. | Label as illustrative or remove pending provenance. |
| M06 | §§3.5, 4 | CQ bands and control thresholds are calibrated | Unsupported claim | No held-out calibration, sensitivity analysis, or error-cost analysis establishes the cutoffs. | Label all cutoffs provisional. |
| D01 | §§4.1–4.3 | Fiber variance is model-free | Unsupported claim | The statistic depends on the chosen fibers, scoring functions, normalization, and aggregation. | “Fiber variance is architecture-relative but can be computed without fitting an additional classifier.” |
| D02 | §4.3 | The proposed detector is ready as a general detection system | Unsupported claim | Independent datasets, baselines, confidence intervals, and prospective thresholds are absent. | “The detector is a prototype specification awaiting external validation.” |
| E01 | §5.1 | Earlier r=.989 evidence supports the oscillator account | Falsified / retracted | The draft itself notes the earlier value was invalid. | Preserve as a corrected false start; do not reuse as support. |
| E02 | §5.2 | Discrete tiers are observed | Unsupported claim | The section is predictive; no experiment establishes the proposed tier boundaries. | “CERTX predicts discrete operating tiers.” |
| E03 | §5.3 | τ≈18.3 is shown by pilot data | Unresolved pilot claim | The dataset, procedure, code, and uncertainty need a traceable evidence carrier. | Retain only after adding provenance; otherwise mark unverified. |
| E04 | §5.4 | Cross-model convergence verifies the architecture | Explicitly unverified | The draft acknowledges the test is not complete. | Keep as a planned test. |
| E05 | §5.5 | Perfect code separation establishes substrate independence | Pilot result with overextended interpretation | n=10 can motivate a larger test; it cannot establish substrate-independent laws. | Report sample construction, scoring, and uncertainty without the generalization. |
| E06 | §5.6 | TruthfulQA AUC≈0.53 behaves as expected | Valuable null | Calling a null “expected” after observation risks post-hoc protection. | “The tested score did not discriminate TruthfulQA labels in this run.” |
| E07 | §5.7 | GSM8K confirms independent multi-fiber detection | Task-specific pilot / unit test | Only the altered numeric evidence is informative in the constructed pairs. | “The experiment validates sensitivity to engineered numeric corruption.” |
| E08 | §5.8 | Synthetic biographies confirm Regime A and symbolic detection | Constructed separation | Specific versus vague examples permit separation by specificity and do not test confident, specific falsehoods. | “The constructed test exposes a specificity-sensitive behavior to challenge on real factual errors.” |
| E09 | §5.9 | Adaptive weights confirm 30/40/30 | Uncalibrated pilot | Selection and evaluation are not cleanly separated; the same constructed regime influences both. | “The pilot shows the adaptive rule can reproduce the chosen weighting under its calibration setup.” |
| X01 | §6.1 | MoxE is a mathematical realization of CERTX | Interpretive silhouette | A suggestive component mapping is not a proof of equivalence. | “MoxE suggests an implementation analogy.” |
| X02 | §6.2 | S2MoE ε validates the ζ* mechanism | Interpretive silhouette | Parameters have different definitions and roles without a tested translation. | Present as a possible control analogy. |
| X03 | §6.3 | Tsallis results validate a CERTX upgrade | Interpretive silhouette | Shared non-extensive language does not establish the paper’s mechanism or constants. | “Tsallis-style measures are candidates for future extensions.” |
| X04 | §6.4 | LEGOMem independently derives the Shadow Ledger | Interpretive silhouette | Functional resemblance is not independent derivation of the same formal object. | “LEGOMem motivates a related memory design.” |
| X05 | §6.5 | A 5% meta-cognitive allocation independently validates CERTX | Unsupported claim | Needs a precise source, comparable quantity, effect estimate, and preregistered relation. | Remove validation language pending a formal comparison. |
| X06 | §6.6 | Grokking validates discrete tiers, SDI, and critical dynamics | Pilot result plus interpretation | Experiment 016 is the strongest genuine contact, but it is one seed with proxy corrections; criticality and thermodynamic readings remain hypotheses. | “A one-seed grokking pilot found an SDI-aligned transition signature worth replicating.” |
| X07 | §6.7 | MASO K=3 proves or realizes the three fibers | Unsupported claim | MASO’s partition parameter is not automatically the CERTX fiber count; no invariant-preserving mapping is given. | “MASO provides a geometric vocabulary that may help formalize fiber partitions.” |
| X08 | §6.8 | Architectural correspondence is cross-validation | Interpretive silhouette | Component resemblance is hypothesis generation, not independent validation. | Use “correspondence map,” not “cross-validation.” |
| X09 | §6.9 | nanochat empirically confirms each CERTX mechanism | Unsupported claim / interpretive silhouette | The mappings are post-hoc; τ=4 does not support τ=7, and a 1.15 ratio does not establish the 1.2 mechanism. | Present each item as a falsifiable analogy with its own required test. |
| C01 | §7 | Shadow Ledger is a validated controller | Synthetic demonstration / executable specification | Experiments 012 and 017 support executable logic and specification, not deployed efficacy. | “Shadow Ledger is an executable controller specification.” |
| C02 | §7 | DREAM/rest has a demonstrated thermodynamic role | Interpretive silhouette / conditional mathematics | The physical terminology outruns the evidence carrier. | Use operational language unless thermodynamic quantities are defined and measured. |
| C03 | §7 | Hard escalation and reserve thresholds are safe/calibrated | Unsupported claim | No prospective utility or risk analysis establishes them. | Mark thresholds provisional and configurable. |
| Z01 | §8.1 | “What we have” includes confirmed universal constants and detector performance | Unsupported summary | It restates the strongest claims without preserving their evidence status. | Replace with a status-separated inventory. |
| Z02 | §8.2 | Critical gaps are identified | Supported research planning | The gap list is one of the paper’s strongest pieces of epistemic hygiene. | Retain and link each gap to a decisive experiment. |
| Z03 | §8.3 | Falsification criteria make the theory falsifiable | Partially supported | Criteria need operational definitions, preregistered datasets, estimators, uncertainty, and decision rules. | Retain as draft preregistration targets. |
| Z04 | Conclusion | The framework is empirically validated across domains | Unsupported claim | Current evidence is mostly synthetic, constructed, task-specific, or interpretive; experiment 016 remains a pilot. | Conclude that CERTX is testable and has survived some internal checks while failing others. |

## Statements supportable now

The following claims survive the audit with modest wording:

1. CERTX is a developing architecture for separating and reintegrating several kinds of consistency evidence.
2. The repository contains executable specifications, synthetic demonstrations, falsifications, null results, calibration scaffolds, and exploratory pilots.
3. Experiment 003 and experiment 011 are valuable falsifications rather than failures to hide.
4. Experiment 005 is a valuable null.
5. Experiment 015 identifies a genuine confound in an earlier validation route.
6. Experiment 016 is the strongest current empirical contact, but remains a one-seed pilot requiring replication and stronger measurements.
7. The GSM8K-derived and synthetic-biography evaluations are useful targeted tests of constructed failure modes, not broad external validation.
8. The proposed constants, thresholds, and cross-domain mappings are testable hypotheses.
9. The current corpus motivates independent, preregistered experiments; it does not remove the need for them.

## Required paper changes after audit acceptance

Do not edit `PAPER_DRAFT_v1.md` until the evidence ledger and this audit are accepted. Once accepted, revise in this order:

1. **Abstract and conclusion:** replace universality and validation language with status-calibrated statements.
2. **Contribution list and §8.1:** separate formal proposals, executable artifacts, empirical pilots, falsifications/nulls, and open hypotheses.
3. **§§3.3–3.5 and §§4.2–4.3:** state assumptions for mathematical results; relabel constants and thresholds as provisional.
4. **§§5.3–5.9:** add provenance, sample construction, baselines, uncertainty, and limitations; preserve nulls and confounds.
5. **§6:** convert “independent validation” claims into explicit correspondence hypotheses with defined maps and decisive tests.
6. **§7:** distinguish controller specification from validated intervention and replace physical metaphors with operational definitions where possible.
7. Add a compact evidence-status tag to every headline quantitative claim.

## Acceptance gate

This audit is ready for human review when the following remain true:

- the original paper blob is unchanged;
- no historical experiment code or result is rewritten;
- every headline claim has an evidence-status classification;
- falsifications, nulls, and confounds remain visible;
- future paper edits can be traced to an accepted audit row.

Acceptance of this file authorizes a later prose revision; it does **not** itself endorse any scientific claim.
