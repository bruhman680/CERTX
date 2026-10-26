# Independent prospective algebra: bias references and raw reconstruction

Authored mathematical toy; no experiment or task-retrieval outcomes were run for this review. Read predecessor `probe-witness-calibration-v1/REPORT.md` and `NEXT_CONTACT.md`. The results below are deterministic and conditional. A reference supplies additional warranted information; agreement does not establish its warrant.

## 1. Observation and bias contracts

Let

    D = n + s,             D' = alpha*n + beta*s,
    y_a = alpha + b_a + e_a,
    y_b = beta  + b_b + e_b,
    |e_a|, |e_b| <= epsilon.

Here alpha and beta are scalar response coefficients. In the proposed finite study n,s are nonzero orthogonal vectors with known norm ratio rho=||n||/||s||. Orthogonality and rho are extra supplied information for the raw-error certificate; coefficient witnesses alone do not establish them. Without such a geometric bound, a coefficient-only raw relative error guarantee need not exist.

For role-specific bias intervals b_a in [L_a,U_a], b_b in [L_b,U_b], the compatible coefficient rectangle is

    I_a = [y_a-U_a-epsilon, y_a-L_a+epsilon],
    I_b = [y_b-U_b-epsilon, y_b-L_b+epsilon].

These formulas are exact interval projections. Treating the rectangle as the whole compatible set additionally permits the role biases and residual errors to vary independently. If the actual model imposes a relation between biases, this rectangle is an outer approximation; its certificates remain sufficient but its refusal can be more conservative.

Repeated same-channel readings can intersect residual intervals but do not narrow a shared bias merely by repeating it. Identical readings are not independent references.

The proposed contracts with epsilon=.02 should be stated as follows:

* BLIND: declares b_a=b_b=0; coefficient radius .02. This is invalid under an actual .12 bias with zero residual.
* HONEST_ALLOWANCE: declares each bias in [-.15,.15]; coefficient radius .17, not .15, when residual .02 is also retained.
* WARRANTED_REFERENCE: receives two role readings r_a,r_b with separately assumed |r_j-b_j|<=.01. Bias intervals are [r_j-.01,r_j+.01], so coefficient radius .03 about y_j-r_j.
* INVALID_REFERENCE: reports r_a=r_b=0 with the same declared reference radius .01 while actual opposed biases are (+.12,-.12). Its coefficient radius is still .03, but its contract is false.

The reference requirement is a measurement/transport assumption about the same bias affecting each target role. A same-origin number with a new name is not a separately warranted reference. Two unrestricted role biases require two constraints (or an explicit lower-dimensional bias model); one scalar reference cannot identify both unrestricted biases. Resource accounting should list reference scalar values, role labels, transport assumptions, and supplied bounds.

## 2. Common and opposed biases differ

Write b_a=c+t, b_b=c-t. Then

    y_b-y_a = (beta-alpha) - 2*t + (e_b-e_a).

A common same-sign offset c cancels from the gap. It can cause raw nuisance leakage, but with equal offsets and no residual it cannot manufacture a nonzero gap from an actually singular operator. The prior INVALID_SHARED_BIAS fixture was c=0,t=.12: one shared latent cause with opposite role signs, not an identical additive offset on both coefficients.

For an explicit latent-bias model c=0, t in [T_L,T_U], the exact compatible gap interval is

    G = [y_b-y_a + 2*T_L - 2*epsilon,
         y_b-y_a + 2*T_U + 2*epsilon].

Retaining that relation is optional for the proposed small study; replacing it by independent role intervals changes the declared information and should be acknowledged.

## 3. Non-identification without a bias constraint

With exact scalar readings y_a=1.12,y_b=.88, both worlds below give the same readings and the same D'=D:

* World S: alpha=beta=1; biases (+.12,-.12); arbitrary n,s with n+s=D. The operator is singular and s is not identified by D,D'.
* World N: alpha=1.12,beta=.88; biases (0,0); n=s=D/2. The operator is nonsingular and reconstructs s=D/2.

This is a structural observational-equivalence argument for unrestricted decompositions. It does not claim these two worlds both satisfy the separately imposed nonzero-orthogonality fixture; World N does not. It proves that readings and D,D' alone do not authenticate bias bounds or identify singularity. Reference/geometric assumptions remove worlds by adding information.

More generally, y_a=alpha+b_a,y_b=beta+b_b do not identify either coefficient if both biases are unrestricted: any proposed coefficient pair has corresponding biases. Even a single opposed latent bias leaves the gap unidentified unless that latent bias is bounded or referenced. A common same-sign bias alone leaves the exact gap identified while the numerator needed for raw reconstruction remains uncertain.

## 4. Conditional nonsingularity certificate

Write I_a=[a_L,a_U], I_b=[b_L,b_U]. The exact rectangle gap interval is

    G = [b_L-a_U, b_U-a_L].

The compatible set excludes singularity iff G lies strictly on one side of zero. A numerical tolerance, if used, must be predeclared and is an implementation guard rather than a mathematical coverage probability. Valid bounds and a passing gate imply actual nonsingularity. Passing under invalid bounds establishes nothing about the actual gap.

If zero belongs to G, the available set permits singularity. Refusal is justified under that information even when the particular authored actual coefficients are nonsingular. It does not assert the actual operator is singular.

## 5. Exact raw error for an available point inverse

Choose point estimates ahat,bhat (for symmetric role intervals their midpoints), and set h=bhat-ahat. For h!=0 define

    s_hat = (D' - ahat*D)/h.

Direct subtraction gives

    s_hat - s = ((alpha-ahat)*n + (beta-bhat)*s)/h.

Under n perpendicular s and known rho=||n||/||s||:

    E^2 := ||s_hat-s||^2/||s||^2
         = ((alpha-ahat)^2*rho^2 + (beta-bhat)^2)/h^2.

This identity includes both gain distortion and nuisance contamination. It does not infer raw fidelity from a normalized projector or retrieval score. If h=0 the point inverse is unavailable; do not encode its error as zero. An available zero-valued output and an unavailable inverse also remain different states.

For rectangle bounds define

    A = max(|a_L-ahat|, |a_U-ahat|),
    B = max(|b_L-bhat|, |b_U-bhat|).

Then

    E <= E_bound = sqrt(A^2*rho^2+B^2)/|h|.

For the independent rectangle and fixed geometry this is the exact worst-case error of the fixed point estimator: the maximizing alpha and beta endpoints can be attained together. For correlated compatible sets this expression is a sufficient outer bound. At midpoint symmetric halfwidths w_a,w_b, A=w_a and B=w_b.

A squared threshold test avoids square-root rounding:

    A^2*rho^2+B^2 <= tau^2*h^2.

With rational authored inputs, both sides, gap endpoints, actual E^2, and bound E_bound^2 can be evaluated exactly using fractions. Decimal display of E or E_bound need not become a decision rule. A raw-error acceptance rule should require the intended nonsingularity gate and the stated error threshold separately if both claims are desired.

For unknown geometry but a justified rho upper bound R, the triangle inequality instead gives E <= (A*R+B)/|h|, which does not assume orthogonality. Without a finite bound on ||n||/||s|| or equivalent observed-data constraints, A>0 permits arbitrarily large raw relative error. Relative error also presupposes ||s||>0.

## 6. Exact prospective expectations and useful checks

For actual biases (+.12,+.12) and blind midpoint estimates:

    h=g=beta-alpha,
    E^2 = .12^2*(rho^2+1)/g^2,  for g!=0.

Thus gap correctness does not imply raw correctness. COPY remains h=0 in this common-offset case.

For actual biases (+.12,-.12), blind estimates have h=g-.24 and

    E^2 = .12^2*(rho^2+1)/(g-.24)^2.

On COPY g=0, h=-.24: the blind point is finite although the actual operator is singular. Its compatible gap with coefficient radius .02 is [-.28,-.20], so its false contract passes the conditional gate. The point output equals .5*(n+s), and E^2=(rho^2+1)/4. This is not separation of the original components.

An invalid zero-centered reference with coefficient radius .03 gives COPY gap [-.30,-.18], also passing while excluding the actual coefficients. It illustrates that merely adding a named reference does not repair a false warrant.

An accurate reference centered on actual biases gives ahat=alpha,bhat=beta for the fixed zero-residual readings. Point error is then zero whenever g!=0, but its declared coefficient radius .03 still gives an uncertainty envelope and can withhold at weak gaps. With WEAK g=.1, its gap interval is [.04,.16], so the nonsingularity gate passes. Its raw envelope is

    E_bound^2 = .03^2*(rho^2+1)/.1^2
              = .09*(rho^2+1).

At rho=.5,1,2 the envelope is respectively sqrt(.1125),sqrt(.18),sqrt(.45), approximately .3354,.4243,.6708, despite actual point error zero. The bound represents compatible possibilities, not an estimate of error prevalence. A threshold .5, if prospectively chosen for illustration, would pass the first two and withhold the last for raw fidelity even though all three have the same passing gap gate.

HONEST_ALLOWANCE has coefficient radius .17. Its symmetric gap halfwidth is .34 about its uncorrected point gap; WEAK is withheld for both zero and opposed .12 bias because its corresponding gap intervals contain zero. Strong-gap probes can pass yet have a substantially larger raw envelope. This is a cost of admitted uncertainty, not evidence that the honest contract is inaccurate.

## 7. Claims that this contact can support

The small finite table can check conditional interval arithmetic, exact error formulas, and the difference between singularity and raw-fidelity claims. It can expose failure under deliberately omitted/false bias warrants and the information cost of a valid reference. It cannot estimate real-world reference reliability, establish source independence, validate role authority, prove a durable reasoning policy, or show a retrieval improvement. No new task score or gain-invariant task inference is needed.
