# QP-C1 exact route-quality acquisition model

Resumption after SJ commit3f25c7967f3915cbdd4a842e6117a7dafd05f892. Client date26October2026 America/Chicago; source scouts separately record their observed access dates. User authorized parallel source scouts and resumed research. This is one bounded finite-model precursor, not another participant comparison or a paper reproduction. Three phases: primary-source contact and prospective model review; one frozen exact execution; independent audit/synthesis/sync.

Question: under declared pre-query information, what can adaptive lookup achieve beyond a fixed set, and how much apparent advantage comes from free reliability metadata? The relation to SJ's calibration/scope joins is conceptual; records below use bit relations rather than real sensor calibration or natural language.

## Model and supplied knowledge

Seven latent bits T,qP,qR,X,Y,u,v define128 authored microstates. T is task truth, the others specify route reliability, two fragments and two irrelevant bad-route fragments. T,X,Y,u,v are independent fair bits. qP,qR are independent Bernoulli with explicitly known probabilities pP,pR. Four prior settings: FAIR=(1/2,1/2), PRIMARY_FAVORED=(3/4,1/4), REFERENCE_FAVORED=(1/4,3/4), BOTH_BAD=(0,0). Weight every microstate by the exact product, drop zero-weight worlds from inference. Repeated observable worlds retain their combined probability; unused latent bits are not extra observations or independent trials.

Available records, each cost1 and queried at most once:

    P = X
    C = (qP, kP), kP = X XOR T if qP=1, otherwise u
    R = Y
    M = (qR, kR), kR = Y XOR T if qR=1, otherwise v.

Thus quality is observable when the associated C/M record is read, not supplied initially. The same quality record also provides the relation fragment; this is authored metadata access, not automatic discovery of reference truth. All agents/policies know the finite generative model, prior and record meanings. They do not know actual latent bits. Route names do not imply measured authority. XOR relations are a simple complementary-information proxy; no causal or semantic model claim.

The only warranted task completion is exact T identification: all positive-weight worlds compatible with observed records have the same T. Otherwise withhold; do not turn a majority posterior into verification. Record posterior exact Fractions and the feasible truth set. Even full access cannot identify T in a both-bad world under this model.

## Fixed comparisons

Budgets B=0,1,2,3,4. Adaptive finite-horizon DP may STOP or query an unqueried record. Lexicographically maximize expected exact-identification probability, then minimize expected number of queries. Resolve remaining exact ties by STOP then record order P,C,R,M. STOP yields reward1 iff T identified, else0, with no further cost. Recursive values use exact Fraction branch masses conditioned on observations. No true T or unobserved q enters policy selection.

Evaluate every fixed subset of size<=B: query its full set, certify T from those observations, report exact resolution probability and fixed query count. Best subset uses the same probability-first/cost-second/canonical tie rule. These fixed-set policies do not adaptively stop; cost differences include stopping as well as branch selection and are not an isolated test of either. B may be unused when further queries cannot improve reward. No claimed improvement over an optimized fixed-order policy with adaptive stopping is made.

Privileged-quality oracle receives actual qP,qR before spending budget but does not receive T. If B>=2 and any route is good, it chooses a good pair and identifies T with2queries; otherwise stops without identifying. Report exact expected resolution and query cost. Free quality disclosure is extra information, not an equal-information policy benefit or an empirical reliability estimate. Prior, reliability flags, logical meaning and query prices are supplied assumptions for every result.

## Outputs, freeze and audit

Four priors x five budgets =20root comparisons. Save all128microstate assignments and exact weights perprior, complete observation projections, all encountered DP belief/mask/budget states, chosen actions, value/cost and branch transitions, each fixed subset's outputs and root oracle outcomes. Counts of rows/states are implementation size, not empirical repetitions. State schema must make all policy branches replayable without main imports.

Preserve code/schema/protocol/prospective math/source review hashes before the sole main. No outcomes or parameter search during implementation. Syntax checks and source-only inspections allowed. Main uses Pythonstandardlibrary exactFraction; displaydecimal optional but not decisions. Save elapsed walltime/Pythonversion/stdout/stderr; failure would preserve original source/output/logs before diagnosis and any repair. No favorable-outcome reruns.

Reviewer independently derives expected20root values and recomputes policy transitions/probabilities/costs from saved worlds without importing experiment.py. Check known-prior weighting, unused-bit aggregation, absence of latent oracle input in ordinary policy, path costs and eventual feasible truth sets. Any audit repair preserves its first failed version/log. Compare saved exact values rather than adopting a new tolerance. Freeze all scientific inputs before execution; no new participant study in this unit.

Scope: finite authored information acquisition, no empirical confidence interval, natural-source authentication, semantic memory benefit, model self-training or FRR efficacy claim. The three screenshot papers are independently scoped source contacts; this model does not reproduce their algorithms or validate their claims. No installation or runtime/core/schema/queue-status change follows automatically. End at report and current sync with proposed next contact.
