# Why state-dependent harvesting escapes the constant-rate energy bound

**Status:** Analytical result under stated approximation; interpreted alongside separately executed neural and threshold-policy experiments. No universal biological or cognitive law is claimed.

Under the **original** Neural Garden v0.1 homogeneous, constant-harvest approximation, let every cell harvest with state-independent probability `p` and let `r` denote mean available resource. Ignoring local diffusion (which cancels in homogeneous mean), the stationary resource equation is

`0 = alpha(1-r) - beta*r*p`, with `alpha=.06`, `beta=.18`, hence

`r*(p) = .06/(.06+.18*p)`.

The unclipped per-step expected energy change is

`DeltaE(p) = .25*r*(p)*p - .03 - .055*p + .008*(1-p)`

`          = .015*p/(.06+.18*p) - .063*p - .022`.

Setting its derivative to zero gives a maximizer near `p=0.331`, with `r*=0.502` and **maximal drift approximately −0.00133** per step. Within this restricted uniform constant-rate class, no stationary policy has nonnegative average raw energy drift. The result does *not* establish an impossibility for every spatially heterogeneous or state-dependent policy.

For an arbitrary local action `A` and local resource `R`, the raw mean energy change is instead

`E[DeltaE] = .25*E[R*A] - .063*E[A] - .022`

`           = .25*(E[R]*E[A] + Cov(R,A)) - .063*E[A] - .022`.

The constant-rate approximation suppresses the correlation term `Cov(R,A)`. A threshold policy that harvests only when local resource is high can create **positive covariance**, improving the energy yield per harvest even when the mean harvest frequency is similar.

In exploratory runs with `harvest iff resource > .55`, the raw energy drift remained positive (about +0.00305 at t=600 averaged over a 20-seed follow-up) and mean energy was about 0.484, far above current learned policies under original laws. This does not prove `.55` is optimal; the threshold was selected during exploration and only then frozen for new tests.

Two implementation cautions:

1. Actual stored energy is clipped to `[0,1]`. Once energy hits zero, the observed `actual_delta` can approach zero even if the **unclipped** resource budget remains negative. Do not mistake a flat observed energy curve at the floor for viability.
2. A changed metabolism law (v0.3) changes the feasible region by construction; upper saturation then measures the easier environment, not improved neural intelligence.

**FRR reading:** A mean value can erase a consequential relationship. Here the relevant missing distinction is the covariance between *where resource exists* and *when action occurs*. This is a concrete, testable information-preservation point—not a new universal constant.
