# Two real readouts and a scoped-mixture boundary

This note is separate analysis of a representation, not a novelty claim. Equal-length finite complex vectors with positive norms are assumed. The conjugation convention is `h=sum(conj(z_j)*w_j)`, matching q as reference in the supplied modulus/angle code. Reversing the convention reverses angle sign and must be reflected in the codebook/calibration.

Write z=x+iy, w=a+ib. Expanding gives:

    A = x dot a + y dot b
    B = x dot b - y dot a
    h = A + i B

The norm of the realification equals the complex norm. Consequently normalized complex modulus and angle are computed from the same real coordinates by `sqrt(A²+B²)/(||z||||w||)` and `atan2(B,A)`. Realified cosine is `A/(||z||||w||)`. The different modulus score reads an additional bilinear channel, not an extra semantic signal discovered by changing arithmetic notation. Real/imaginary pairing is part of the defined representation.

For a unit reference q and global code w=e^(iφ)q, modulus is1 and angleφ. A,N,U can therefore share a relevance score while retaining separate prescribed angles. This geometry does not determine whether U means uncertainty, a different relation or something else; that meaning is supplied externally.

Now choose orthogonal context/binding coordinates and positive amplitudes a,b. Let q=(a,b)/sqrt(a²+b²), w_A=q, w_N=(a,−b)/sqrt(a²+b²), and w_U=(a,e^(iφ)b)/sqrt(a²+b²). Then:

    h_A = 1
    h_N = (a²-b²)/(a²+b²)
    h_U = (a²+e^(iφ)b²)/(a²+b²)

At a=b, h_N=0: modulus0, no mathematically defined phase. At a>b, h_N is positive real, so its angle collides with h_A's0. At b>a it is negative real, anglepi. Thus an angle-only A/N codebook can change qualitatively with mixture weights even without noise or training. At φ=pi/3,a=b, h_U has anglepi/6 and modulus sqrt(3)/2, not its supplied binding phasepi/3.

These are counterexamples to treating a scoped binding rotation as a whole-vector global rotation. They are not a claim that every scoped encoder fails, nor that identical scalar angles make the entire record identical. Magnitude and the complete vectors can retain distinctions. The cancellation is in an inner product, distinct from deleting history by summing stored records.

Numeric checks use128freshly generated moderate vector pairs and3fixed amplitude ratios, with no Claude code imported. Different source/model lineage is not enough to establish external empirical independence; the proof is algebra and the finite checks validate this implementation. No universal numerical stability claim is made, especially near zero inner products where phase is ill-conditioned.
