"""
ERASE-GATE ATTRIBUTION with IMPERFECT interventions.  Exact enumeration (no sampling except the last section,
which draws binomial counts with independent generators per condition).

World: payload b (fair bit) written to a FIELD carrier f (=b w.p. qf) and a PRIVATE carrier p (=b w.p. qp).
Reader: reads f w.p. wF, reads p w.p. wP if gate open, else answers by coin; channel flips read bit w.p. eta.
Observable: contrast c = P(y=b) - 1/2.
Interventions (each can be imperfect):
  ERASE   : the branch's 'reset': field -> coin w.p. 1 (success), AND in gated worlds closes the gate.
  clearP(s,d): private -> coin w.p. s ; off-target: field -> coin w.p. d.   (applied k times independently)
  openGate: gate forced open.

PREDICTIONS (written before running):
 P1. Gated-private world and pure-field world with matched strength have IDENTICAL (keep, erase) contrasts,
     so naive keep-minus-erase attributes 'field' in both  (false positive in the gated world).
 P2. With openGate + k clearP applications, contrast c_k = F(1-d)^k + P(1-s)^k exactly (enumeration must match).
 P3. Single-probe estimator of F has bias  -d*F + (1-s)*P.
 P4. Repeated clearing (k=0..3, Prony on exponential sum) recovers (F,P,d,s) exactly in the noiseless law,
     but is unidentifiable when (1-d)=(1-s) (decay rates coincide) and ill-conditioned nearby.
 P5. With finite samples, error of the Prony estimate of F blows up as |s-d| -> 0.  No prediction on magnitudes.
 Assumptions NOT tested: that the probes have the stipulated selectivity; that which decay belongs to the field
 is labelled by an independent swap probe.  A private spoof with a field-like decay law would pass.
"""
import numpy as np, itertools

def contrast(qf, qp, wF, wP, eta, gate_open=True, field_clear=0.0, priv_clear=0.0):
    """exact: enumerate b,f,p,reader-route,channel-flip; field_clear/priv_clear = prob carrier replaced by coin."""
    tot = 0.0
    for b in (0, 1):
        for f, pf in ((b, qf), (1-b, 1-qf)):
            for p, pp in ((b, qp), (1-b, 1-qp)):
                for fc, pfc in ((0, 1-field_clear), (1, field_clear)):     # fc=1 -> field replaced by coin
                    for pc, ppc in ((0, 1-priv_clear), (1, priv_clear)):
                        w = 0.5*pf*pp*pfc*ppc
                        # route probabilities
                        wP_eff = wP if gate_open else 0.0
                        wC = 1 - wF - wP_eff
                        pcorrect = 0.0
                        for route, pr in (('F', wF), ('P', wP_eff), ('C', wC)):
                            if pr == 0: continue
                            if route == 'C': pcorrect += pr*0.5; continue
                            if route == 'F': read_ok = (0.5 if fc else float(f == b))
                            else:            read_ok = (0.5 if pc else float(p == b))
                            pcorrect += pr*(read_ok*(1-eta) + (1-read_ok)*eta)
                        tot += w*pcorrect
    return tot - 0.5

qf, qp, wF, wP, eta = 0.9, 0.9, 0.4, 0.4, 0.1
F = contrast(qf, qp, wF, wP, eta, gate_open=False)           # field alone (gate shut)
P = contrast(qf, qp, wF, wP, eta, gate_open=True) - F        # private share
print(f"field-only contrast F={F:.5f}  private-only share P={P:.5f}  (P2 linear split check)")
print(f"  field only (gate shut) + private only (field cleared): {F + contrast(qf,qp,wF,wP,eta,True,1.0,0.0):.5f}"
      f" vs both {contrast(qf,qp,wF,wP,eta):.5f}")

print("\nP1  keep vs ERASE.  ERASE = clear field AND close gate.  Matched strengths so worlds are comparable.")
cF = wF*(2*qf-1)*(1-2*eta)
worlds = {"pure FIELD":        dict(wF=0.4, wP=0.0, erase_gate=False),
          "GATED private":     dict(wF=0.0, wP=0.4, erase_gate=True),
          "UNGATED private":   dict(wF=0.0, wP=0.4, erase_gate=False),
          "FIELD+GATED priv":  dict(wF=0.4, wP=0.4, erase_gate=True)}
for name, w in worlds.items():
    keep = contrast(qf, qp, w['wF'], w['wP'], eta, True)
    er = contrast(qf, qp, w['wF'], w['wP'], eta, gate_open=not w['erase_gate'], field_clear=1.0)
    print(f"  {name:18s} keep={keep:.5f} erase={er:.5f}  naive 'field effect' = keep-erase = {keep-er:.5f}")

print("\nP2/P3  openGate + clearP(s,d) applied k times.  enumeration vs closed form; single-probe bias.")
def ck(F, P, s, d, k): return F*(1-d)**k + P*(1-s)**k
for s, d in ((0.9, 0.0), (0.9, 0.1), (0.7, 0.2), (0.5, 0.5)):
    cs = [contrast(qf, qp, wF, wP, eta, True, 1-(1-d)**k, 1-(1-s)**k) for k in range(4)]
    cf = [ck(F, P, s, d, k) for k in range(4)]
    err = max(abs(a-b) for a, b in zip(cs, cf))
    est1 = cs[1]; bias = est1 - F
    print(f"  s={s} d={d}: max|enum-closed|={err:.1e}  1-probe est of F={est1:.5f} bias={bias:+.5f} "
          f"(predicted {-d*F+(1-s)*P:+.5f})")

print("\nP4  Prony on c_0..c_3 = A r1^k + B r2^k :  recover (A,B,r1,r2). Noiseless, then noisy.")
def prony(c):
    # c_{k+2} = a c_{k+1} + b c_k  ->  roots r of r^2 - a r - b
    M = np.array([[c[1], c[0]], [c[2], c[1]]]); a, b = np.linalg.solve(M, [c[2], c[3]])
    r = np.roots([1, -a, -b]).real; r.sort()
    V = np.array([[1, 1], [r[0], r[1]]]); A = np.linalg.solve(V, [c[0], c[1]])
    return r, A
for s, d in ((0.9, 0.1), (0.7, 0.3), (0.6, 0.5)):
    cs = [ck(F, P, s, d, k) for k in range(4)]
    r, A = prony(cs)
    print(f"  s={s} d={d}: roots {np.round(r,4)} (true {sorted([1-s,1-d])}) amplitudes {np.round(A,5)} (true F={F:.5f}, P={P:.5f})")

print("\nP5  finite-sample Prony, independent generator per condition, N samples per k, 400 repeats.")
rng = np.random.default_rng(12345)
N = 200_000
print("   |s-d|   cond(Vandermonde)   median |F_hat-F|  frac failed(complex/NaN)   (root with 1-d matched to field via swap-probe label, ASSUMED)")
for s, d in ((0.9, 0.1), (0.8, 0.3), (0.7, 0.5), (0.6, 0.55), (0.6, 0.58)):
    cs = np.array([ck(F, P, s, d, k) for k in range(4)])
    rd = 1 - d; rs = 1 - s
    cond = np.linalg.cond(np.array([[1, 1], [rd, rs]]))
    errs = []; fail = 0
    for _ in range(400):
        # each k observes N independent Bernoulli(P(y=b)) draws; separate generator stream per k
        hat = np.array([rng.binomial(N, 0.5 + c)/N - 0.5 for c in cs])
        try:
            r, A = prony(hat)
            if not np.all(np.isfinite(A)): fail += 1; continue
            i = int(np.argmin(abs(r - rd))); errs.append(abs(A[i] - F))
        except Exception:
            fail += 1
    print(f"   {abs(s-d):.2f}    {cond:10.1f}          {np.median(errs) if errs else float('nan'):.5f}"
          f"          {fail/400:.2f}")
