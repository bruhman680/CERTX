# What is moved, what is supplied, and what is estimated

Written before the main execution. This is a deterministic linear model, not a model of private reasoning or a learned semantic encoder.

For column vectors, let q'=Qq and w'=Qw, where Q is real orthogonal acting complex-linearly. Then q'^H w'=q^H w. Realifying each complex coordinate as two real coordinates gives the same real cosine, together with a second bilinear channel for the imaginary component. A general orthogonal transformation on those doubled real coordinates would require preserving/transporting the complex structure too; it is outside this design.

Let P be an orthogonal binding projector, so P=P^H=P^2. The identical operation in new coordinates is P_Q=QPQ^T:

    P_Q q' = QPq
    (P_Q q')^H(P_Q w') = (Pq)^H(Pw).

Keeping P instead produces PQq. There is no reason PQq equals QPq when P and Q do not commute. A performance change in that arm need not indicate erased memory: it can be a readout that failed to move with its representation. Conversely, agreement for a particular small rotation does not establish universal invariance of the fixed mask.

The pair model supplies more than outputs. Before training noise, a normalized r=1 pair is

    w_A = (c,b)/sqrt(2), w_N = (c,-b)/sqrt(2),
    (w_A-w_N)/2 = (0,b)/sqrt(2).

Here c and b each have unit norm and the pair's shared c is exactly matched. Rotation makes that contrast Q(0,b)/sqrt(2). Thus the paired labels and common-context assumption expose a sample of the binding subspace. This is supervised linear identification under a supplied cancellation mechanism; it does not discover what a sentence means or which claims are true.

For m clean pairs, span(D) lies inside the true rank-d binding subspace. If rank(D)=m<d, its projector has rank m. The normalized distance used in this contact is

    ||P_hat-P_Q||_F / sqrt(2d) = sqrt((d-m)/(2d)).

For d=12,m=4 it is sqrt(1/3), despite perfect containment. With d linearly independent clean binding samples, the span equals the full subspace; m>=d alone is insufficient unless those samples span it. With noise, the fitted rank min(m,d) remains a chosen dimension, not evidence for a true dimension. Top-subspace uniqueness can fail at a truncation-boundary singular-value tie.

Task performance need not be a monotone function of full projector recovery. A partial projection can keep enough distinctions for this finite candidate set; a full vector can exploit useful context in noisy queries. Separate the geometric target, the retrieval target and the decoder's calibration policy. Encoded U remains a source status, and ABSTAIN remains a decoder outcome.

Source contact: paired defining-set scatter/SVD in Bolukbasi et al. is a methodological analogue; eigenvalue-gap perturbation analysis in Yu et al. supplies conditional stability context. Neither proves language semantics or a universal sample budget. See scout/REPORT.md for exact read scope and assumptions.
