# Mathematics 02 — observation equivalence is not transition congruence

Status: bounded mathematical audit, one executed finite witness; no empirical substrate claim, remote write, or original-script execution. The shared seed is an inherited specification, not independent corroboration.

## Finding and exact burden

FRR v0.5 lines 558–576 define b_D:H_D→B_D and equality of its outputs as an equivalence relation. This always yields a set quotient. Calling that quotient an effective *dynamical* state additionally requires the congruence in lines 605–615. These are different burdens; the text already recognizes their separation but could make the existence theorem explicit. Equality of current observations, passive trajectories, equilibrium measurements, or a finite prediction horizon does not alone supply intervention closure.

Let H be a set, q:H→S its surjective quotient, and T_a:H→H total deterministic maps for a declared action set A. There exists a unique induced map \bar T_a:S→S satisfying q∘T_a=\bar T_a∘q if and only if q(h)=q(h') implies q(T_a h)=q(T_a h') for all h,h'. Necessity follows by substituting the shared quotient value; sufficiency defines \bar T_a([h])=[T_a h], and the implication makes this representative independent. No additional topology is needed for this set-level statement. If measurability or continuity is claimed, those are additional requirements.

For partial maps T_a:D_a→H, a macro action with representative-independent availability requires D_a to be a union of quotient classes, together with congruence on D_a. Otherwise one must expose availability as extra state or specify a weaker existential semantics; silently applying the total-map theorem is invalid. Intervention domain includes action availability, intervention semantics, duration, allowed compositions, and whether the environment is included in H. If an action changes the field, H must include sufficient field/rule variables or be an appropriate history space: otherwise T_a may not even be a function of the purported state.

## Explicit finite counterexample

H={x,y,z}, observation o(x)=o(y)=0 and o(z)=1. Passive action w is identity. Probe p has p(x)=z, p(y)=y, p(z)=z. Quotient by current observation is S={{x,y},{z}}. Under arbitrarily long passive observation, x and y both produce 000…; thus even equality of every passive finite-horizon prediction fails to distinguish them. Under p, the traces are 01 and 00. Attempting \bar p({x,y}) requires simultaneously {z} and {x,y}, so it is not well defined.

Executed Python enumeration checks all ordered same-block pairs. Wait produces no failures; probe produces exactly (x,y) and (y,x). Saved transitions, traces, and witness in `outputs/mathematics-02/finite-witness.json`. Five-step passive traces are executed; the infinite passive equality is proved from w=id, not inferred from five samples. For A={w} the original quotient is valid. For A={w,p}, retaining the observation requires splitting x and y; the minimal stable refinement is the three singleton blocks. This constructed example witnesses a logical boundary; it is not experimental evidence that a particular physical system has hidden states.

## Stochastic criterion and serious rival

For finite stochastic kernels P_a, a representative-independent one-step macro kernel exists precisely when, for every macro block C and action a,

    sum_{k:q(k)=C} P_a(h,k) = sum_{k:q(k)=C} P_a(h',k)
    whenever q(h)=q(h').

Then \bar P_a(q(h),C) is this common sum (controlled strong lumpability). In general measurable spaces the pushforward q_*P_a(h,·) must factor measurably through q; pairwise equality alone should not conceal a measurable-factorization assumption. An approximate target needs an explicit norm, action family, and horizon. Pairwise total-variation discrepancies ≤ε allow selection of representative rows with row defect ≤ε; finite-horizon accumulation can then be bounded by tε, capped at 1, under shared macro-history policies and appropriate finite-state coupling. This does not license microstate-dependent control, unbounded-horizon accuracy, or stationary-distribution accuracy without additional assumptions.

A serious rival is *task-relative predictive sufficiency*, rather than actionwise strong lumpability. Under a fixed initial mixture or passive policy, a macro process may admit a useful predictive law even when another initial distribution or intervention breaks it (weak lumpability or policy-relative prediction). The finite example itself supports this rival: compressing x and y is perfectly adequate for the wait-only task. Strong congruence would be an unnecessarily severe demand for that declared task. Thus the repair is not to reject observational equivalence categorically, but to label which transition/policy family it serves. Exact output-trace equivalence over **all** admissible action words, with prefix-compatible availability and deterministic updates, is a stable equivalence: prepending action a establishes the congruence. A truncated horizon does not have that closure automatically.

## Surviving relation and concrete repair

The surviving relationship is action-indexed factorization: an erased distinction is safely omitted exactly when the required projected transformation cannot recover it. This is a valid bridge between quotient reasoning and FRR's warning that the field may carry persistence. It does not identify a universal mechanism of memory, soil deposition, graph reinforcement, or contextual processing.

Recommended insertion after FRR line 615:

> Equality of the chosen behavior always defines a set quotient; an induced dynamics is a further claim. Declare admissible actions and their availability. For total deterministic transformations, the stated congruence is necessary and sufficient for a unique representative-independent macro transformation. For partial transformations also require action domains to be unions of equivalence classes. For stochastic dynamics require each action's projected transition law to agree within each class, or explicitly restrict the initial distribution, policy, horizon, and error criterion of a weaker predictive claim.

Recommended operational audit: record (H,o,A,domains,horizon,tolerance); seek same-class witnesses; compute deterministic split signatures `(o(h), [q(T_a h)]_a)` and iteratively split until stable for the declared finite system. Finite termination follows because splitting increases block count until at most |H| blocks; the result is the coarsest congruence refining the initial observation partition. Keep a valid passive quotient as a separate dormant/task-limited artifact rather than erasing it because a control quotient needs refinement. Recommendation only: FRR source was not edited.

## Inspected provenance and limitations

- `/workspace/frr-distributed-2026-10-07/NOW.md`: active authorization and inherited evidence constraints.
- `/workspace/recovered-originals/2026-10-05/FLUID_RELATIONAL_REASONING_v0.5_CANDIDATE.md`: compact seed inspected; lines 558–625 explicitly numbered, quotient/weave/faithful-compression sections through 735 inspected. Lines 620–625 motivate projected-law comparison; the exact stochastic condition above is this report's derivation.
- `/workspace/recovered-originals/2026-10-05/RECOVERY_NOTE.md`: recovery lineage, graph/optimizer/model limitations, archive/field coupling, and later batch availability inspected. Historical pause is superseded by NOW.
- `/workspace/CERTX-context/CONTINUATION_HANDOFF.md` and `RECOVERED_CODEX_HISTORY.md`: recovery boundaries and repository-history provenance inspected; no history reconstructed beyond those records.
- `/workspace/recovered-originals/gemini-screenshots/ASSEMBLED_RECORD.md`: opening artifact-status and clipping caveats inspected, not a complete screenshot audit.
- `/workspace/adaptive-boundary-reconstruction/README.md`: inferred-model status, specified diffusion rules, writer-location dependence inspected. This is not recovered-original evidence and its numerical results were not rerun here.
- Executed evidence: only the isolated Python finite witness above, with assertions on enumerated failures. No literature search, empirical measurements, or supplied substrate scripts executed. Existing provenance documents contextualize scope; they do not independently validate the theorem or witness.
