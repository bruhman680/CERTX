# Independent algebra and interval check

This note derives expectations from the stated measurement construction only. It does not inspect run outcomes or infer task success from geometry. `BETA_GAIN_ERROR` denotes the clarified mode: four exact alpha witnesses and four beta witnesses with error +0.1 and declared beta radius 0.12. Neither role is missing in that mode.

## Reconstruction and invariance

Let D = n+s, D' = alpha*n+beta*s, true gap g = beta-alpha, and estimated gap h = bhat-ahat. For h != 0,

    shat = (D' - ahat*D)/h
         = ((alpha-ahat)/h)*n + ((beta-ahat)/h)*s.

Writing da = ahat-alpha and db = bhat-beta gives

    h = g+db-da,
    nuisance coefficient = -da/h,
    signal coefficient = (g-da)/h,
    shat-s = (-da*n-db*s)/h.

Thus errors in alpha generally change the mixture direction. If alpha is exact, shat = (g/(g+db))*s: beta error changes only scalar gain, provided g != 0 and h != 0. Any nonzero scalar preserves the column space, row space, and corresponding orthogonal projector of a matrix s, or the unoriented line/projector of a vector s. Negative scalar gain reverses oriented vectors but preserves the orthogonal projector. Norms and actual reconstructed values need not be preserved.

This statement requires nonzero signal and the intended rank. If s = 0, no nonzero signal direction exists; if g = 0 with exact alpha, the numerator is zero and yields no direction even when a biased beta estimate makes h nonzero. If signal rank is lower than the requested projector rank, extra singular vectors are arbitrary. Numerically, rank and singular-value tolerances must reject zero or nearly zero recovered signal before claiming direction recovery. A full-rank scalar multiple has the same projector only when its magnitude is safely resolved numerically.

For exact coefficients, inversion amplifies perturbations by terms proportional to 1/|g|. With estimated coefficients,

    ||shat-s|| <= (|da|*||n|| + |db|*||s||)/|g+db-da|.

A small true gap is intrinsically poorly conditioned; cancellation making the estimated gap small worsens the actual calculation. If |db-da| <= r < |g|, the denominator is at least |g|-r. A gate merely excluding zero need not provide a useful conditioning margin.

## Bounded witness certificate

For each role, intersect its declared intervals:

    A = intersection_i [yalpha_i-epsalpha_i, yalpha_i+epsalpha_i],
    B = intersection_i [ybeta_i-epsbeta_i, ybeta_i+epsbeta_i].

For finite, nonempty A=[La,Ua] and B=[Lb,Ub], the compatible gap set is

    G = [Lb-Ua, Ub-La].

Every compatible coefficient pair has nonzero gap iff 0 is excluded from G, equivalently the closed intervals A and B are strictly disjoint: Ub < La or Ua < Lb. Touching endpoints fail. Its guaranteed gap margin is min(abs(G.lower), abs(G.upper)) only when zero is excluded.

This is a statement about the compatible set. It applies to the true coefficients only conditional on the measurement bounds being valid. Empty intersections are inconsistent evidence, not a vacuous certificate. A missing role provides no unconditional finite repair or nonsingularity certificate; overlap likewise gives no unconditional repair, although some pairs in the compatible set may be nonsingular.

A mean point estimate should be checked for membership in its role intersection; arithmetic means need not generally belong to intersections. In the four concrete constructions below, the specified mean estimates do belong to their intersections. Their membership does not rescue invalid bounds.

## Predicted witness coverage and gaps

The four true probes have (alpha,beta) equal to (-1,1), (0.9,1), (1,-1), and (1,1), hence g = 2, 0.1, -2, and 0. Means below are arithmetic means of the four witnesses for each role. Endpoints are exact decimal constructions; numeric code should account for floating-point tolerances without materially changing strict separation.

| Mode | A relative to true alpha | B relative to true beta | Mean gap | Compatible gap G | True coefficient coverage |
|---|---|---|---|---|---|
| EXACT0 | [0,0] | [0,0] | g | [g,g] | Both roles; 8/8 witness intervals |
| BOUNDED | [-0.01,0.06] | [-0.06,0.01] | g-0.05 | [g-0.12,g+0.02] | Both roles; 8/8 witness intervals |
| BETA_GAIN_ERROR | [0,0] | [-0.02,0.22] | g+0.10 | [g-0.02,g+0.22] | Both roles; 8/8 witness intervals |
| INVALID_SHARED_BIAS | [0.10,0.14] | [-0.14,-0.10] | g-0.24 | [g-0.28,g-0.20] | Neither role; 0/8 witness intervals |

BOUNDED uses alpha errors (0.04,0.03,0.02,0.01), beta errors (-0.01,-0.02,-0.03,-0.04), and both radii 0.05. INVALID_SHARED_BIAS uses errors +0.12 and -0.12 with radius 0.02, violating both declared bounds. Its intersections remain nonempty because the bias is shared across repeated witnesses.

| Mode | True g | Mean gap | Compatible gap | Separation gate |
|---|---:|---:|---|---|
| EXACT0 | 2 | 2 | [2,2] | pass |
| EXACT0 | 0.1 | 0.1 | [0.1,0.1] | pass |
| EXACT0 | -2 | -2 | [-2,-2] | pass |
| EXACT0 | 0 | 0 | [0,0] | abstain |
| BOUNDED | 2 | 1.95 | [1.88,2.02] | pass |
| BOUNDED | 0.1 | 0.05 | [-0.02,0.12] | abstain |
| BOUNDED | -2 | -2.05 | [-2.12,-1.98] | pass |
| BOUNDED | 0 | -0.05 | [-0.12,0.02] | abstain |
| BETA_GAIN_ERROR | 2 | 2.1 | [1.98,2.22] | pass |
| BETA_GAIN_ERROR | 0.1 | 0.2 | [0.08,0.32] | pass |
| BETA_GAIN_ERROR | -2 | -1.9 | [-2.02,-1.78] | pass |
| BETA_GAIN_ERROR | 0 | 0.1 | [-0.02,0.22] | abstain |
| INVALID_SHARED_BIAS | 2 | 1.76 | [1.72,1.80] | pass |
| INVALID_SHARED_BIAS | 0.1 | -0.14 | [-0.18,-0.10] | pass, wrong inferred gap sign |
| INVALID_SHARED_BIAS | -2 | -2.24 | [-2.28,-2.20] | pass |
| INVALID_SHARED_BIAS | 0 | -0.24 | [-0.28,-0.20] | pass, false identification |

In EXACT0 the point estimator is unavailable at g=0 because its denominator is zero; this differs from the nonzero-denominator estimates that a conservative interval gate abstains from using in other modes. Missing evidence also differs from these two cases.

In BETA_GAIN_ERROR the point reconstructions at the three nonzero true gaps have gains 20/21, 1/2, and 20/19 respectively, and hence exactly preserve the signal projector in exact arithmetic. At true g=0 its numerator is zero, so no signal direction is recovered; the interval gate correctly abstains.

The invalid-bound copy probe (alpha=beta=1) demonstrates false identification sharply: D'=D, ahat=1.12, bhat=0.88, so shat=(-0.12*D)/(-0.24)=0.5*D. The recovered mixture can be nonzero and possess an apparently stable projector, while it supplies no separation of nuisance from signal. Neither repeated biased agreement nor exclusion of zero by the declared interval set validates the bounds. The invalid near-gap probe also produces a compatible gap sign opposite to the true sign.

These predictions establish algebraic consistency, conditional coefficient coverage, gate behavior, and direction-versus-gain distinctions. They establish no downstream task accuracy or success.
