# SR-C1: imperfect resets and interaction-dependent observation

This executes a bounded slice of the [AS-C1 priority1 design](../arxiv-scout-v1/NEXT_CONTACTS_DRAFT.md): a separately coded six-state model, explicit leaky/off-target reset matrices, mixed routes, and population-level response identification. [Protocol](PROTOCOL.md) was saved before the first numerical run; its SHA256 remained `90454c0d9d021339a6a704b2b95f478db6e8b6aa1328a773c885e2c937a56377`. [Implementation](run.py), [raw results](RESULTS.json), [stdout](RUN.stdout.txt), [stderr](RUN.stderr.txt), and [scalar cross-check](check.py) are preserved.

This is finite enumeration using floating-point linear algebra, not exact rational arithmetic, an independent laboratory replication or real-agent experiment. It rebuilds the mechanism in a different state space/parameterization; it does not reproduce Claude's tuned numerical values. No model parameter was changed after observing outputs.

## Construction and timing

States are binary agent memory m and three-level environment s. Shadow keeps s fixed; echo updates m from the outcome; wake updates s; mixed updates both. Agent updates retain state with probability .6, soil updates with .7. Other coordinates redraw from declared fixed distributions. Every world is tested with additive emission `.05+.2m+.2s` and an interaction emission adding `.08ms`.

A forced outcome updates state without Bayesian reweighting; an observed natural outcome also reweights its initial state likelihood. The reset follows this update, then six natural outcomes can occur. Agent-target reset replaces m by0 with probability .8 and s by0 with probability .1; soil-target reverses those rates. Shared reset uses .6 for each; sham and perfect-both controls are included. The reset maps are independent coordinate replacements, with no hidden access gate. Kernels, stationary preparations and all reset matrices are in RESULTS.json. Static shadow uses an explicitly selected uniform soil mixture; it has no unique stationary mixture implied by the kernel alone.

## Findings

**1. Calibration matters even in pure-route examples.** For the additive echo, the true first-outcome contribution is agent .064, soil0. If imperfect resets are mistakenly read as perfect, the apparent allocation is agent .0576, soil .0128. For wake, the true allocation is agent0, soil .072; the same mistake gives agent .0144, soil .0648. The apparent secondary contribution is produced by reset semantics, not a newly demonstrated memory carrier.

**2. Diverse calibrated resets recover the defined additive contributions; redundant ones do not.** Let a=.2 DeltaE[m] and b=.2 DeltaE[s] after forced1 versus forced0. The next-outcome contrast after reset rates rA,rS is exactly within numerical tolerance:

`D(rA,rS) = (1-rA)a + (1-rS)b`.

Sham plus coordinate-diverse rows has rank2 and condition number2.56. Sham plus repeated shared-reset rows has rank1: arbitrary allocations (.1,0) and (0,.1) give the same first-outcome responses. More repetitions of those population equations cannot add the missing rank. This does not claim those two allocations are realizable worlds with identical full observation laws.

**3. An interaction readout breaks the two-component explanation.** Adding `.08ms` introduces `c=.08 DeltaE[ms]`, with reset factor `(1-rA)(1-rS)`. The three-term expression agrees with the actual transition matrices. In the mixed interaction case c=.0331941; an additive-only least-squares fit leaves Euclidean residual .0137101 across sham/agent/soil, far above numerical error. The three-term design has rank3 and condition number5.60, and recovers the defined terms. This is a response decomposition conditional on known readout/reset structure, not discovery of an additional physical memory carrier. Even the pure echo mechanism has a nonzero interaction term when read against a random background soil.

**4. A null forced response does not imply absent environmental persistence.** Static shadow has zero forced1-minus-forced0 response. Yet soil-target reset changes its baseline next-error probability from .35 to .18. A probe difference cancels that baseline change. Both baseline and contrast must be recorded.

## Full-law check prevents a false impossibility claim

We enumerate length4 binary-word probabilities for 8 worlds ×5 reset maps ×3 preparations =120 normalized distributions. Candidate sets under each declared design are saved. All8 fixed candidate worlds are already distinguishable by their passive length4 laws; the minimum pairwise passive TV is .0393190. The worlds were not tuned to match error rates or correlations.

Therefore this example does NOT show interventions are necessary to distinguish these known candidates. The shared-reset ambiguity concerns arbitrary first-outcome contribution allocation, not their full temporal laws. The reported intervention-design TVs average uniformly across different contexts and are not an equal-budget performance ranking. Finite-sample precision or real-world label recovery cannot be inferred from these population distances.

## Verification and scope

All seven model checks passed. A second implementation enumerated update/reset outcomes through scalar loops, without the matrix formula, and agreed on first contrasts within1.60e-16. All120 word laws normalize within1.34e-15; stationary distributions and protocol integrity checks passed. This is a same-model numerical cross-check, not independent evidence for the model assumptions. [CHECKS.json](CHECKS.json) also preserves every passive pair distance.

Known reset rates/readouts are stipulated, not measured by witnesses. Unknown calibration, off-target uncertainty, reset dependence, different target distributions, nonlinear dynamics, gate restoration, finite-sample tests at equal budgets, and actual-agent transfer remain open. Interaction terms can be missed if the tested design lacks enough distinct rows; the expanded model's fit is not by itself evidence it is uniquely true outside the declared family.

## Consequence for practice and next contact

The [verification layer](../../modules/verification-layer.md) should interpret an intervention through its actual operator and inspect baseline shifts and model mismatch before locating a response route. Preserve an unresolved outcome when calibration or the observation model is missing. There is no universal erasure threshold here.

The next useful extension is a separately frozen calibration/witness experiment with noisy and off-target uncertainty, followed by equal-budget repeated versus diverse interventions. SR-C1 does not complete the broader LEGACY-01 or MEM-03 families. The practical source/access agent comparison and readable-code/history idea remain deferred; no FRR core/schema or scientific queue status is changed.
