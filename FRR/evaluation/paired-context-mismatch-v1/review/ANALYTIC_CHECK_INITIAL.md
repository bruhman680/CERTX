# Prospective analytic check

This is an outcome-blind algebraic review of the supplied toy model. No main-run arrays, task outcomes, or finite-sample diagnostics were inspected. The random-direction model, the ordered paired supervision, the rank-12 estimator, and the binding/context decomposition are supplied assumptions, not learned facts about language or memory.

## Population second moments and targets

Let d=12, x=(delta*a,b)/sqrt(2), and P=diag(0,I_d). Vectors a,b are real unit directions. E[aa^T]=E[bb^T]=I_d/d. The estimator takes the leading d right-singular directions of the uncentered difference matrix; its population analogue uses M=E[xx^T]. Here the mean is zero, so covariance and second moment agree. Multiplying all differences by a common scalar changes eigenvalues but does not change the target projector.

For independent a,b, E[ab^T]=0 and

    M_ind = diag(delta^2 I_d, I_d)/(2d).

For 0<=delta<1 the unique leading rank-d projector is P; for delta>1 it is C=I-P. The cutoff gap is |1-delta^2|/(2d). At delta=1 the moment is I_(2d)/(2d), so every rank-d projector is optimal and there is no unique leading target. Repeated eigenvalues within one selected block do not destroy uniqueness of its full rank-d projector.

For aligned a=b,

    M_al = [[delta^2 I_d, delta I_d], [delta I_d, I_d]]/(2d).
    T_delta = [delta I_d; I_d]/sqrt(1+delta^2).
    G_delta = T_delta T_delta^T
            = [[delta^2 I_d, delta I_d], [delta I_d, I_d]]/(1+delta^2).

There are d eigenvalues (1+delta^2)/(2d) and d zero eigenvalues. Thus G_delta is the unique leading rank-d projector for every finite delta, with gap (1+delta^2)/(2d). It projects onto the graph {(delta*v,v):v in R^d}; it is neither a noisy version of P nor generically P itself.

Using the declared normalized distance D(H,P)=||H-P||_F/sqrt(2d),

    D(P,P)=0; D(C,P)=1;
    D(G_delta,P)=|delta|/sqrt(1+delta^2).

The aligned principal-angle cosines against the binding span are all 1/sqrt(1+delta^2).

| Pair condition | delta | Unique population target | Cutoff gap | Distance to P |
|---|---:|---|---:|---:|
| Clean | 0 | P | 1/24 | 0 |
| Independent mismatch | 0.5 | P | 1/32 | 0 |
| Independent mismatch | 1.5 | C | 5/96 | 1 |
| Aligned mismatch | 0.5 | G_0.5 | 5/96 | 1/sqrt(5), about 0.447214 |
| Aligned mismatch | 1.5 | G_1.5 | 13/96 | 3/sqrt(13), about 0.832050 |

These are population predictions. For independent nonzero mismatch the difference distribution occupies all 24 dimensions; its empirical top-12 subspace can fluctuate around its population target. More pairs do not remove a wrong population target, and samplewise improvement need not be monotone. In the aligned case every observed difference lies in the same d-dimensional graph. With at least d independent continuous directions spanning R^d, noiseless top-d SVD recovers G_delta exactly in exact arithmetic; no asymptotic approximation is needed. The analogous clean statement recovers P. Numerical rank conventions and roundoff remain implementation questions.

## Held-out projection and phase angles

Let the held-out scoped record be

    y_p=(r*c,p*b)/sqrt(1+r^2),
    p_A=1, p_N=-1, p_U=exp(i*pi/3),

where c,b are real unit vectors and remain independent of the training graph directions. A clean matching A-reference query is q=y_1. The identities below hold for every real t=c^T b in [-1,1], and do not assume c=b. They concern clean queries only; noisy-query outcomes require their actual arrays.

Under P, projection removes context and normalized relevant products are exactly p. Thus A,N,U angles are 0,pi,pi/3 with unit modulus, irrespective of r. Under C, projection removes binding and all three projected status records coincide. All relevant normalized products are 1: A/N/U angle collision is exact.

Under G_delta put k=delta*r. The projected record is

    G_delta y_p = [delta I_d; I_d](k*c+p*b)
                 /((1+delta^2)*sqrt(1+r^2)).

After the common isometry/scaling is removed, normalized products use the graph coordinates u_A=k*c+b and u_p=k*c+p*b. Their unnormalized Hermitian product and squared norms are

    u_A^* u_p = k^2 + k*t*(1+p) + p;
    ||u_A||^2 = k^2+1+2*k*t;
    ||u_p||^2 = k^2+1+2*k*t*Re(p).

The positive norm denominator changes magnitude but not angle whenever both norms are nonzero. In particular,

    u_A^* u_N = k^2-1.

Consequently the N angle is pi for k<1, undefined for k=1, and 0 for k>1. At k>1, A and N collide in angle even though their projected vectors need not coincide and their normalized product magnitude need not be 1. That distinction matters for a phase decoder versus a retrieval score.

At k=1 the N product is zero for EVERY t. This does not require a zero N vector: ||u_N||^2=2(1-t), so its vector is nonzero unless c=b. Likewise ||u_A||^2=2(1+t), so its vector is zero only if c=-b. For ordinary independent continuous c,b, both vectors are nonzero almost surely, yet they are orthogonal and the complex angle of their zero product is undefined. Software returning angle(0)=0 must not turn this into an A/N collision. A declared small-product validity threshold can also render nearby finite-precision products undefined.

| Aligned target | r | k=delta*r | Clean relevant N angle |
|---|---:|---:|---|
| G_0.5 | 0.5 | 0.25 | pi |
| G_0.5 | 2 | 1 | undefined zero product, usually nonzero vectors |
| G_1.5 | 0.5 | 0.75 | pi |
| G_1.5 | 2 | 3 | 0, collides with A in angle |

For U the product is

    k^2 + k*t + (1+k*t)*exp(i*pi/3).

Its argument generally depends on t, so a single universal U phase is not recovered by the mixed graph. At k=1 and t>-1 this reduces to (1+t)*(1+exp(i*pi/3)), whose angle is pi/6; N remains undefined. For k<1 the imaginary part is strictly positive. For k>1 the imaginary part can vanish at t=-1/k; then the real part is k^2-1>0 and U also collides with A in angle. This exact equality is a measure-zero alignment for continuous held-out directions, not a predicted empirical frequency. For k=3, U's imaginary part is negative when t<-1/3; no universal claim that its angle stays between A and the original U phase is justified.

## Scope of inference

The oracle P is supplied structural access. The clean paired setup supplies exact nuisance cancellation. Independent mismatch tests whether nuisance variance outranks binding variance; aligned mismatch changes the identifiable subspace itself. A large spectral gap establishes stability around the selected population subspace, not correctness relative to P.

The phase identities establish possible calibration failures and exact clean relevant-record geometry. They do not by themselves establish top-3 retrieval, downstream completion, noisy-query decoding, empirical calibration centers, or finite-sample failure rates. In particular, if a decoder requires every status center, exact k=1 zero N products can make the entire clean calibration unavailable; whether a finite estimated projector and the implementation's threshold produce that condition must be checked from the frozen run. At k>1, coincident A/N phase centers can cause ties even with distinct vectors. Those are different failure mechanisms and should be recorded separately.

All conclusions above are original algebra from the supplied generator. No external mathematical result beyond elementary moments, spectral decomposition, and orthogonal projection is required.
