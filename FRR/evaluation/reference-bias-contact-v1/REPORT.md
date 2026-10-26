# Reference authority, inversion and raw accuracy

RB-C1/2/3, 26 October 2026 America/Chicago. Completed bounded authored mathematical contact after [PW](../probe-witness-calibration-v1/REPORT.md). This study tests supplied bias contracts, not real reference reliability, language semantics or agent efficacy. No new paper search, retrieval experiment, model training or external API call was needed.

In garden terms: a second measuring stick helps only if its markings and relation to the first stick are warranted. A beautifully narrow ruler can be consistently wrong. We also need to specify whether we want to separate the roots, estimate their sizes, or merely make a decision that is insensitive to size.

## Three completed phases

1. Independent algebra, prospective critique and review of deferred actual-reader contacts. Root fixed a smaller fresh scalar fixture rather than replaying the previous large retrieval pipeline. Initial protocol and math drafts remain alongside corrected versions. Review distinguished equal common offsets from role-opposed bias, total error bounds from additional residual noise, and scalar-channel ambiguity from full observed-vector equivalence.
2. Root verified approved source/protocol/schema hashes and froze them before the sole main execution. Python 3.12.14; standard library only; all decisions exact rational arithmetic. Main exited 0 in approximately 0.0595 seconds, with no failure or rerun. [Execution](EXECUTION.json), [freeze](FREEZE.json), [stdout](STDOUT.txt), [stderr](STDERR.txt).
3. A separate auditor rebuilt all main and supplemental rows without reading/importing the main implementation. Its explicit two-dimensional vector reconstruction and four-corner envelope maximization agreed with every saved exact quantity and decision: 10,432 comparisons, zero mismatches. [Audit](review/AUDIT.md), [machine receipt](review/AUDIT.json). Final prose review is saved separately.

Six contexts including root collaborated: mathematical derivation, prospective/source reviewer, implementer, independent replay auditor and deferred-direction reviewer. They communicated before execution. They are same-platform reviewers, not independent empirical subjects or a demonstrated group-reasoning treatment.

## Fixed worlds and information

Let D=n+s and D'=alpha*n+beta*s, where n and s are perpendicular, ||s||=1 and rho=||n|| is 1/2, 1 or 2. The four coefficient pairs are CONTEXT=(-1,1), WEAK=(.9,1), SIGNAL=(1,-1), COPY=(1,1). Scalar observations are y_a=alpha+b_a, y_b=beta+b_b. There is no additional residual measurement noise.

Bias pairs are ZERO=(0,0), COMMON=(.12,.12), OPPOSED=(.12,-.12). These make 12 coefficient/bias worlds. Four contracts and three norm ratios give 144 main rows. The same primary scalar readings are reused across contracts and norm ratios. Eight additional diagnostic rows describe two scalar-ambiguous worlds at rho=1; they are excluded from all main counts. There are no independent repetitions, estimated probabilities or significance tests.

| Contract | Declared bias information | Point coefficients | Additional scalar readings |
|---|---|---|---:|
| BLIND | Each bias in [-.02,.02] | y_a,y_b | 0 |
| WIDE | Each bias in [-.15,.15] | y_a,y_b | 0 |
| REFERENCE | Role references r_a=b_a,r_b=b_b, each error bounded by .01 | y_a-r_a,y_b-r_b | 2 |
| BAD_REFERENCE | Reports r_a=r_b=0 with the same .01 bound | y_a,y_b | 2 |

BLIND and BAD_REFERENCE deliberately violate their contracts in nonzero-bias worlds. REFERENCE is exactly centered by construction; its accuracy and transported role authority are supplied, not discovered. WIDE is valid but conservative. No contract treats different roles as statistically independent. REFERENCE changes both available measurements and the declared uncertainty contract, so comparison with WIDE is not an isolated causal estimate of acquisition benefit.

Two primary observations are reused within each world. Each reference method nominally adds two values, but only three reference pairs exist across the whole grid: ZERO, COMMON and OPPOSED; BAD_REFERENCE repeats the zero pair. This is information accounting, not 72 independently acquired reference observations. Norms, orthogonality, response model, role labels and bounds are also supplied knowledge. Acquisition cost in real equipment, money or tokens was not measured.

## What is certified

For bias interval [l,u], the coefficient interval is [y-u,y-l]. With coefficient intervals I_a=[L_a,U_a], I_b=[L_b,U_b], the compatible gap lies in [L_b-U_a,U_b-L_a]. A gate passes only if this entire interval strictly excludes zero. It certifies nonsingularity conditional on those coefficient bounds being valid. It does not validate their authority.

For point estimates a_hat,b_hat, set h=b_hat-a_hat, g=beta-alpha, da=a_hat-alpha, db=b_hat-beta. If h is nonzero:

    s_hat = (D' - a_hat*D)/h
    s_hat - s = (-da*n - db*s)/h
    relative_error_squared = (da^2*rho^2 + db^2)/h^2.

Define A=max(|a_hat-L_a|,|a_hat-U_a|) and B similarly for beta. Then under coverage and supplied geometry:

    relative_error_squared <= (A^2*rho^2+B^2)/h^2.

This is the exact supremum over the independent coefficient rectangle for this fixed point denominator and geometry. It is an outer bound if additional coefficient relations are retained. It does not exploit additional constraints one might extract from full observed vectors, and it is not a maximum over changing denominators. Unknown geometry would require different information or a different bound; the triangle bound with justified rho<=R is (A*R+B)/|h| in relative-error units.

The raw requirement was fixed before execution: relative error <= .1. Raw certification requires both the gap gate and squared envelope <= .01. Actual truth is used only afterward to evaluate a certificate. Unavailable inversion (h=0), a finite diagnostic point that is withheld, and a certified point remain different states. No projector/status/retrieval metric was computed here.

## Complete main results

Each row below has 36 method/norm configurations, not 36 independent trials. [All 144 rows](run/ROWS.json) and [all summaries plus eight ambiguity diagnostics](run/SUMMARY.json) are preserved without rounding rational decisions.

| Contract | True pair covered | Gap gate passes | Passes on true COPY | Raw certificates | False raw certificates |
|---|---:|---:|---:|---:|---:|
| BLIND | 12 | 30 | 3 | 19 | 5 |
| WIDE | 36 | 18 | 0 | 7 | 0 |
| REFERENCE | 36 | 27 | 0 | 18 | 0 |
| BAD_REFERENCE | 12 | 30 | 3 | 22 | 8 |

Across all rows: 96 coefficient sets cover truth; 105 gap gates pass and 39 withhold; 117 point inversions are available and 27 unavailable. Nine truly nonsingular rows are withheld, all WIDE/WEAK combinations. This refusal is warranted by the method's compatible set, even though the authored true operator is nonsingular. No interval is empty in this fixture.

The conditional error envelope holds on all 75 covered, point-available rows. Forty-two uncovered available rows violate their putative envelope. There are 66 raw certificates and 13 false raw certificates, all under deliberately invalid contracts. These descriptive counts do not estimate real failure rates or rank algorithms at equal information.

## Three instructive cases

**A common offset preserves the gap but can violate raw accuracy.** At CONTEXT/COMMON/rho=2, true gap and estimated gap are both 2. BLIND's actual squared error is 9/500=.018, or approximately .1342 relative error, while its claimed squared envelope is 1/2000=.0005. It falsely certifies the .1 requirement. BAD_REFERENCE claims the even narrower envelope 1/8000 and makes the same erroneous point estimate. WIDE covers truth and withholds raw certification; REFERENCE corrects the point exactly. Therefore correct gap estimation is insufficient for correct raw values.

**Opposite offsets can counterfeit separation.** On OPPOSED/COPY the true gap is zero, but BLIND and BAD_REFERENCE see point gap -.24. BLIND's compatible gap is [-.28,-.20]; BAD_REFERENCE's is [-.26,-.22]. Both pass under invalid contracts. Their point reconstruction is .5*(n+s), with squared relative error (rho^2+1)/4. It is not separation of the components. Three rho settings repeat each of these two false structural certificates; they are not six independent discoveries.

**Exact actual recovery can lack a warranted .1 bound.** On every REFERENCE/WEAK row the point coefficients are exact and actual error is zero. The compatible gap [.08,.12] excludes zero, yet squared raw envelopes are 1/80,1/50,1/20 at rho=.5,1,2. Their square roots are approximately .1118,.1414,.2236, all above the requirement. The uncertainty contract permits worse points than the authored truth. Withholding the guarantee is not an observed reconstruction failure.

## The scalar ambiguity boundary

Primary readings (1.12,.88) fit both (alpha,beta)=(1,1) with biases (.12,-.12) and (1.12,.88) with zero biases. Their singularity differs. Thus the two scalar readings alone do not identify singularity if bias is unrestricted. A valid reference distinguishes them by adding warranted information.

This does not establish equivalence of the whole orthogonal fixture. If n and s are held fixed, their D' vectors differ. An alternative construction preserving full D,D' requires changing latent decomposition and can violate this fixture's orthogonality assumptions; [math review](review/MATH.md) labels that separate scope explicitly. Agreement of scalar witnesses is the tested limitation, not an impossibility theorem for every richer observation scheme.

## Corrections and preservation

Before execution we preserved [initial protocol](PROTOCOL_INITIAL.md) and [initial math draft](review/MATH_INITIAL.md). The math draft initially included an extra residual-noise term, giving .17/.03 widths; the selected protocol intentionally has zero residual noise, so final widths are .15/.01. Reviewer and root caught the discrepancy before freeze. Scalar-only ambiguity wording and eight supplemental diagnostic rows were also made explicit prospectively. No favorable-outcome tuning, main failure, main rerun or audit repair occurred. [Prospective critique](review/PROSPECTIVE_REVIEW.md), [source approval](review/SOURCE_REVIEW.md), [final math](review/MATH.md), [schema](SCHEMA.md), [implementation](experiment.py).

The historical CR strict ordered-replay failure remains unchanged; this exact Fraction audit does not repair or relabel it. PW's source corrections and earlier successes/failures remain preserved. Core/runtime/schema and machine queue statuses are unchanged. Hashes bind bytes, not measurement truth.

## Next useful contact and confidence

High confidence in the scoped algebra, exact finite table and independent all-row replay. No empirical confidence estimate for reference quality, natural-language authority, semantic memory or durable habits follows.

The strongest practical bridge is a small actual-reader source-ancestry/authority contact. Earlier tests used overt wrong-run cues or withheld decisive sources; writer handoffs often retained every queried basis. A new design should include both true and false claims with copied and separately generated support, available and insufficient references, and separate scores for rejecting unsafe reuse versus actually repairing a value. Source independence and task entailment are different questions. [Deferred-direction review](DEFERRED_DIRECTION_REVIEW.md) specifies prior coverage and confounds; [next contact](NEXT_CONTACT.md) remains proposed, not launched.

A numerical extension could relax orthogonality or add reference-to-target transport mismatch, with prospective geometry bounds. That is useful if raw-value guarantees become the intended task. Repeating the same exact-reference grid or treating more copied witnesses as extra assurance would add little.
