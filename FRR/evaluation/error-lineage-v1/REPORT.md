# EL-C1: Matching mistakes do not identify their route

This bounded contact develops the user's suggestion that failures can have shared soil, patterns and propagation. It supplies exact counterexamples and a practical repair prompt. It does not measure actual agent culture, prove FRR efficacy or establish a universal criticality threshold.

## What ran

[Protocol](PROTOCOL.md) and [code](../../experiments/error_lineage_contact.py) were hash-bound before execution in [MANIFEST.json](MANIFEST.json). Analytical predictions were known during design: this is a development demonstration, not independent confirmation. [RESULTS.json](RESULTS.json) preserves exact rational results, numerical branching calculations and the saved-data replay. Twelve declared witness/replay checks passed. Those checks verify the constructed contrasts, not external validity.

| Contact | Result | Practical implication |
|---|---|---|
|32 binary outputs, each error probability0.1 | Both models average3.2 errors. P(at least16 errors) is1.2420273563e-8 for independent errors and0.1 for a shared all-or-none cause. | A mean alone omits dependence and group-wide tails. These two extreme models are illustrations, not estimates of real teams. |
| Common cause A=U,B=U versus copying A=U,B=A | Exactly identical observational distributions. Correcting A before B computes separates them: B error probability remains0.1 versus0. Correcting A after B computes does not separate them. | Observation alone can leave causal routes unresolved. Intervention timing and access matter. |
| Shared difficulty, independent errors conditional on item | Easy/hard error probabilities0/0.2, equally frequent, give marginal0.1 and error covariance0.01. | Correlated mistakes need not mean copying or a shared false fact. |
| Stipulated wrong source and two cached answers | Source-only repair leaves two wrong completed answers. Source repair plus recomputation produces two correct completed answers. Suppression produces zero wrong answers and zero completed answers. | Repair inherited records as well as the source; distinguish correction, abstention and missing work. |
| Sham and off-target controls | Sham preserves outcomes. Silencing B masks the common-cause/copying difference. | A channel intervention must not silently damage observation or evidence access. |
| Binomial(2,p) branching | With R=1, expected generation size stays1, while extinction by generation20 is0.84619 and eventual extinction is1. With R=1.2 eventual extinction is4/9, not0. | A model-specific average growth threshold does not determine each trajectory. There is no measured reasoning-system R here. |

The branching calculation uses Z0=1, R=2p, q0=0 and q(t+1)=(1-p+p q(t))². E[Zt]=R^t. It concerns an unbounded-population Galton–Watson model without collisions, repair or resource limits; finite agent networks need not follow it. No entropy threshold is derived.

## Contact with existing work

The published [PG-C1 residual extract](../practice-growth-v1/RESIDUALS.json) replays to12000 samples, mean−0.00027989575, MAE0.05983533110 and1855 absolute residuals above0.08. The earlier [PG report](../practice-growth-v1/REPORT.md) records near-identical residual streams across seven controllers.

The explanation has additional provenance: [pid_contact.py](../../experiments/pid_contact.py) recreates an RNG with the same seed inside each simulation. Separate controllers reuse the generated noise; they do not read each other's outputs. The extract alone cannot establish this route. This contact did not rerun all controllers or create new sensor measurements. Repeated streams do not multiply independent evidence.

## Primary-source contacts

The source scout read these actual texts; the root synthesis relies on that explicitly delegated reading:

- Shalizi & Thomas, [institutional-hosted draft of *Homophily and Contagion Are Generically Confounded in Observational Social Network Studies*](https://www.stat.cmu.edu/~brian/780/bibliography/01%20homophily%20and%20contagion/shalizi-thomas-homophily-contagion-2011-SMR.pdf): introduction, §2.1, asymmetry discussion and opening constructive responses. Shared traits, selection and external causes can confound influence under their assumptions. Temporal/asymmetric associations do not automatically identify transmission. This does not make all causal identification impossible.
- Reason, [*Human error: models and management*, BMJ2000, NHS-hosted original](https://qi.elft.nhs.uk/wp-content/uploads/2026/02/r_03-james-reason-2000-human-error.pdf): all three pages. Investigate recurring conditions, defenses and recovery alongside immediate mistakes. This is a conceptual safety-management article, not an AI trial. Direct PMC/BMJ/EuropePMC access failed; the NHS mirror supplied the article.

These motivate questions and controls, not a claim that human organizations and AI workflows share one physical mechanism.

## What we can use now

The optional [error-lineage practice](../../modules/error-lineage.md) adds one prompt when a consequential mistake recurs: trace the source, route, conditions and affected descendants, then choose a check that distinguishes plausible explanations. A changed source flags descendants for reassessment, not automatic refutation: conclusions may be insensitive to the change, differently scoped or independently supported. Existing reopening tooling binds one assessment; it does not discover a semantic dependency graph or automatically reopen every inherited claim.

This remains a precursor to FIELD-01 and LEGACY-06. Actual agents under independently varied source correctness, peer-answer exposure and difficulty are still needed. Keep source-only, transmission-only and mixed mechanisms available; do not force one diagnosis. Measure corrected completion, recurrence, repair cost and appropriate uncertainty, not consensus alone. No core runtime/schema change or completed family is claimed.

## Separate review

The archive reviewer inspected the script and results and found no concrete mathematical/output mismatch. It checked joint laws, timing, tails, difficulty covariance, cache semantics and extinction formulas. It emphasized that branching uses floating-point evaluation and repair success is stipulated in the toy. Its recommendation to reassess rather than automatically refute descendants is incorporated in the optional practice. This review is not independent empirical confirmation.
