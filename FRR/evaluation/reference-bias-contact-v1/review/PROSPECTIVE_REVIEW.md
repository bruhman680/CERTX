# Prospective critique: reference information and shared bias

Written before any new main run, 26 October 2026. Scope: independently critique the next contact proposed in `probe-witness-calibration-v1/REPORT.md` and `NEXT_CONTACT.md`. This review does not approve uninspected implementation or outcomes. It introduces no new main execution or empirical claims. Coordinate algebra with `review/MATH.md`.

## Main judgment

A useful contact can demonstrate the value and limits of an added reference under an explicit bias-transport model. It cannot demonstrate that reference agreement authenticates that model. Freeze the reference's information, role mapping, error bounds, allowed biases and failure controls before task scoring. Count reference knowledge as additional privileged information rather than treating it as a free improvement to the old gate.

The predecessor's `INVALID_SHARED_BIAS` is shared across repeated witnesses but **role dependent**: every alpha reading has +.12 error and every beta reading has -.12 error. Calling that merely a “common scalar bias” conceals the property responsible for its false nonsingularity certificate.

## Distinguish the bias models

Let `y_a = alpha + b_a + e_a` and `y_b = beta + b_b + e_b`, with bounded residuals `e`. Equivalently, `b_a = c-d`, `b_b = c+d`: `c` is a same-sign common offset and `d` is the differential offset. A shared latent parameter with known opposite role signs is a one-dimensional *role-opposed* bias model; it is not the same as an equal same-sign offset.

| Model | Information in observed gap before residual error | Consequence |
|---|---|---|
| Equal same-sign bias, `b_a=b_b=c` | `y_b-y_a = beta-alpha` | Gap cancels bias. With valid residual bounds a same-sign bias alone cannot falsely certify COPY as nonsingular. Raw reconstruction still has nuisance/signal contamination. |
| Known role-opposed bias, `b_a=-b_b` | Gap includes differential bias | One reference can identify the latent bias only if its signed loading is known, nonzero and transported correctly to both roles. |
| General role-dependent bias, unrestricted `b_a,b_b` | Gap contains `b_b-b_a` | One scalar reference normally leaves a degree of freedom; use two justified independent constraints or retain the unidentified directions. |
| Role- or condition-dependent transport | Depends on reference-to-target mismatch | A reference calibrated on one role, probe, seed or condition need not constrain another. The declared transport domain is part of the contract. |

At a point estimate, with `h = b_hat-a_hat`, reconstruction is `((alpha-a_hat)/h)n + ((beta-a_hat)/h)s`. Thus an equal offset `c` with exact residuals gives `s_hat = s - (c/(beta-alpha))(n+s)` for a nonsingular true operator. Cancellation in the gap does not establish raw fidelity. Conversely, a beta-only gain error can preserve the task projector despite wrong raw amplitude, as the predecessor already showed. Keep these claims separate.

## What a reference cannot verify on its own

1. A known reference response supplies truth only conditional on its assigned reference value and role. If these were authored from the same hidden coefficients, that is supplied oracle information rather than discovery of external authority.
2. The same-origin witness and reference can share an unmodeled error. Their agreement or a narrow intersection does not validate residual bounds, error independence, or transport. Repeated identical patterns across seeds are not independent instruments.
3. A reference with known scalar value does not certify its role labels, the rotated anchor roles, purity of response, linear mixing model, or absence of cross-role coupling. Those remain assumptions unless a separate channel challenges them.
4. One reference cannot identify arbitrary two-role bias. Nor does successful correction under a frozen known-sign latent model establish correction under unrestricted role bias.
5. A nonsingularity certificate establishes neither a small reconstruction error nor good conditioning, observed signal rank, decoder success, retrieval success, or general truth. COPY remains unidentifiable from identical stored mixtures; an apparent point inverse cannot manufacture missing information.
6. Even an empty compatible set only falsifies the joint stated contract. It does not localize blame to reference, witnesses, role assignment or residual radius without extra information.
7. A reference and a bias allowance may correctly withhold useful repairs. Oracle-relative opportunity cost is descriptive; do not relabel withholding as logically unnecessary given the method's actual information.

## Meaningful fixed comparisons

Use identical source arrays, actual operators, queries and scoring for paired comparisons. Preserve the predecessor's task semantics and thresholds. No method may select its radius, reference mapping or bias model from task answers.

| Method | Supplied knowledge | Purpose |
|---|---|---|
| Omitted-bias contract | Original readings and residual-only radii | Exposes consequences of the wrong contract, explicitly labeled misspecified. |
| Honest bias allowance | Same readings plus a fixed valid prior bias region | Tests safe withholding without new reference observations; uncertainty must retain allowed correlation. |
| Reference-informed allowance | Same prior plus measured reference and declared reference error/loading | Measures added information against the honest allowance; use intersection, never replace the prior with an unbounded point correction. |
| Known-coefficient oracle | True target coefficients | Structural upper control, including unavailability at true singularity. |
| Known-role/binding oracle | Privileged signal subspace | Distinct task access control; do not conflate it with coefficient inversion or newly observed evidence. |

If a point debiaser is included, give it the same reference observations and state that it ignores residual set width; compare availability, error and task outcomes separately. It should not be the sole reference baseline. Include a bias-aware contract without a reference so the study separates gains from declaring a larger valid model from gains due to new measurements.

Freeze a small structural fixture grid covering: zero bias; equal common offset; the predecessor's role-opposed offset; residual noise at a justified allowed setting; true COPY; weak and well-separated true gaps; and at least one reference-transport violation. The violation may be a reference-only shared offset or an unmodeled role-dependent offset. Label it deliberately invalid rather than treating it as an empirical error prevalence estimate. Keep valid-model and invalid-model results in separate descriptive cells.

For the role-opposed compact design, a same-sign common-offset stress case is especially informative: it is outside a pure role-opposed correction model unless the model also allows `c`. If the study instead targets general `(c,d)`, give references enough linearly independent known loadings, or explicitly show non-identification. A same-origin reference control is useful only if its shared blind spot is represented; it must not be called an independent verification.

## Predeclared readouts and interpretation

Primary structural readouts should include true coefficient inclusion in the declared feasible set; empty-set rate; certified nonsingularity; false certification on true COPY; and withholding on truly nonsingular fixtures. Also retain actual bias inclusion when the artifact exposes it, so a reference can be diagnosed without collapsing all failures into gate availability.

Report compatible true-gap range, or an analytically justified alternative, using the **joint** feasible set. Independent marginal coefficient intervals may be conservative but can erase correlations that the reference supplies; disclose that approximation and its effect. A common-offset uncertainty need not widen the gap at all. Reference point correction followed by narrow residual intervals is justified only when reference uncertainty and transport uncertainty have been propagated.

Keep raw reconstruction error and projector/task results separate, and distinguish unavailable reconstruction, available rank-zero output, and decoder abstention. Retain the weak-probe scale-invariant control if raw fidelity is discussed. No task success should be used as proof the measurement contract was valid.

Audit actual information counts: distinct reference values/patterns, independent source sets, repeated target readouts, role labels, prior bounds, reference bounds and loadings. Counts of duplicated query rows or repeated fixed bias patterns are not replication counts. Report the extra reference acquisition/knowledge cost even in a synthetic fixture where monetary cost is unspecified.

## Freeze and review boundary

Before the sole main: specify the entire valid and invalid bias/reference table, signs, loadings, radii, set-construction equations, numerical guards, methods, fixed source/probe cells, outcomes and artifact provenance. Algebra fixtures may check set inclusion and explicit singular/weak cases without task fitting or scoring. Review the final source against the frozen contract before approving execution; this document alone is not that source review.

A positive result would be narrow: under a valid authored reference-transport contract, extra constraints may tighten the compatible set and change permitted reconstruction; under a violated transport contract they may still yield confident error. This is a conditional information study, not validation of reference authority, empirical independence, learned language behavior, or durable agent verification practice.

## Disposition of the frozen candidate protocol

Read `PROTOCOL.md` after the foregoing independent critique. Its 144-row fresh exact toy is **approved for implementation and subsequent source review**, subject to source matching the protocol. This is design approval before outcomes, not source approval or main-run approval. The protocol selects unrestricted per-role bias intervals and two separately labeled role references; it does not pretend that a single scalar reference identifies both role biases. COMMON and OPPOSED are distinct fixed fixtures. BAD_REFERENCE explicitly tests invalid authority in both nonzero-bias worlds.

The protocol intentionally has no additional residual-noise realization: `y=coefficient+bias`, and the quoted BLIND/WIDE intervals bound the whole primary bias. The reference radius `.01` bounds total reference error under its transport contract. Do not add `.02` to this radius or describe these as residual-plus-bias radii. My earlier generic residual-noise grid recommendation is not a requirement for this deliberately smaller fixture. It would be a separate future contact, not grounds to expand this frozen grid after observing results.

For a fixed point `(a_hat,b_hat)` with nonzero denominator `h`, the protocol's squared bound `((E_a*rho)^2+E_b^2)/h^2` is valid under coefficient coverage, orthogonality and known norm ratio. Over its declared independent rectangular coefficient set it is also the attained supremum: the two absolute errors can attain their endpoint maxima together. It does not range over a changing reconstruction denominator. Gating may still withhold although that fixed-point bound is finite. A raw certificate additionally requires the predeclared gate and raw-error budget, so report both conditions without conflation.

The nominal `.01` reference radius and exact `r=bias` observation supply a valid conservative set around an exact point in REFERENCE. That favorable centering is authored; it does not establish real reference accuracy. BAD_REFERENCE is equally authored and coherent within its declared model while excluding truth. Its failures demonstrate that extra reference measurements cannot authenticate their own authority.

REFERENCE is its own total bias contract rather than an intersection with WIDE. This is acceptable here because the protocol explicitly defines each comparator's information. Do not claim it estimates the causal benefit of two extra measurements while holding every other contract fixed: both prior width and reference authority differ. The honest WIDE comparison still separates a valid conservative allowance from invalid BLIND. If reporting an intersection interpretation, establish that the intersection is exactly the implemented interval in every frozen fixture, and state that WIDE knowledge is also supplied.

The observed-equivalent pair is useful as a primary-scalar-reading non-identification witness. Specify the scope: identical `y_a,y_b` do not identify singularity when biases are unknown. Distinct coefficient worlds can also have different mixture vector `D'` if the same latent `n,s` are held fixed. Do not claim full observed-data equivalence for `D,D'` or every available diagnostic unless a construction explicitly preserves those too. Known pure-role anchors and known true latent norms are privileged modeled structure; references do not newly establish those roles.

The raw envelope is allowed to depend on the supplied `rho` and orthogonality. This is a conditional toy task requirement, not a general raw-error guarantee when nuisance/signal norms or their angle are unknown. No retrieval, projector, probability or real-language claim is supported by this run. Keep the 12 coefficient/bias worlds separate from the 144 method/norm rows.
