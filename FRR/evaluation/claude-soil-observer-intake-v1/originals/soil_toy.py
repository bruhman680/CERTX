"""
SOIL TOY: error propensity as substrate.  Exact enumeration only (no sampling => no shared-draw bug).

Outcome o in {0,1} (1 = error).  Joint state = (s, l): s = soil level in {0,1} (error propensity), l = agent's last outcome.
Three carriers of error clustering, tuned to the SAME stationary error rate and the SAME lag-1 covariance:
  SH  shadow : soil frozen, uniform hidden level; p = P[s].                          (condition, not rewritten)
  EC  echo   : no soil heterogeneity; p = p0 + c*l.                                   (agent-local memory)
  WK  wake   : soil rewritten by outcomes: after error s->1 w.p. u; after success s->0 w.p. d; p = P[s] (own levels, see tuning).
Interventions: do(F) = force one error (soil/agent update as after an error) vs observe(F) = condition on an error;
  agent reset = l:=0 ; soil reset = s:=0 (applied right after the probe).  Control for a reset = same reset without the probe.

PREDICTIONS (written before running):
 P1. Matched marginal & lag-1 cov hold by construction; lag-k cov: SH constant in k, EC geometric (c^k), WK nonconstant, decaying.
 P2. do(F) effect on later error rate: SH exactly 0 at every lag; EC = c at lag 1 and exactly 0 at lag>=2; WK > 0 at lag>=2.
 P3. observe(F) effect: SH > 0 and constant in lag; EC equals do(F); WK exceeds do(F) at every lag (hidden-soil update + deposit).
 P4. After the probe: agent reset zeroes the do-effect in EC (all lags) and leaves WK unchanged; soil reset zeroes it in WK
     and leaves EC unchanged.  (Exact zeros up to 1e-15.)
 P5. Integral (EWMA) estimator of the error rate: the probe raises its estimate in ALL worlds, so in SH it 'winds up' on a probe
     that changed nothing: its excess KL vs the oracle after do(F) is > 0 at lag 1 (sign only; other cells exploratory).
 NOT tested: real agents; selectivity of the resets; anything about causal identification beyond this constructed family.
"""
import numpy as np, itertools

# ---------- model construction ----------
STATES = [(s, l) for s in (0, 1) for l in (0, 1)]
idx = {st: i for i, st in enumerate(STATES)}
NS = len(STATES)

def build(world, P=(0.0, 0.0), c=0.0, p0=0.0, u=0.0, d=0.0):
    """returns M[o] (emission-weighted transition), D (forced-error transition), pvec (P(error|state))."""
    M = [np.zeros((NS, NS)), np.zeros((NS, NS))]; D = np.zeros((NS, NS)); pv = np.zeros(NS)
    for (s, l), i in idx.items():
        p = {'SH': P[s], 'EC': p0 + c*l, 'WK': P[s]}[world]
        pv[i] = p
        for o in (0, 1):
            po = p if o == 1 else 1 - p
            if world == 'WK':
                if o == 1: nxt = {1: 1.0} if s == 1 else {1: u, 0: 1-u}
                else:      nxt = {0: 1.0} if s == 0 else {0: d, 1: 1-d}
            else: nxt = {s: 1.0}
            for s2, ps in nxt.items():
                j = idx[(s2, o)]
                M[o][i, j] += po*ps
                if o == 1: D[i, j] += ps
    return M, D, pv

def stationary(Ms):
    pi = np.ones(NS)/NS
    return pi @ np.linalg.matrix_power(Ms, 2**14)

def stats(world, **kw):
    M, D, pv = build(world, **kw); Ms = M[0] + M[1]; pi = stationary(Ms)
    r = pi @ pv
    def cov(k): return (pi @ M[1]) @ np.linalg.matrix_power(Ms, k-1) @ pv - r*r
    return r, [cov(k) for k in range(1, 7)]

# ---------- tuning: matched marginal r=.2, lag-1 cov = .032 ----------
R, C1 = 0.2, 0.032
c_ec = C1/(R*(1-R))                      # lag-1 cov of AR-type chain: c*Var(X)
p0 = R*(1-c_ec)
delta = np.sqrt(C1); Plev = (R-delta, R+delta)
# WK needs its OWN soil levels: with SH's levels a soil that actually moves cannot reach the lag-1 cov (first attempt collapsed to u=d=0 = frozen).
# Fix deposit strength u=.5 and the low level .02; solve (d, Phi) for marginal R and lag-1 cov C1.
from scipy.optimize import fsolve
U_WK, PLO = 0.5, 0.02
def f(x):
    d, Phi = x; r, cv = stats('WK', P=(PLO, Phi), u=U_WK, d=d); return [r-R, cv[0]-C1]
best = (9, None)
for d in np.linspace(0.01, 0.99, 99):
    for Phi in np.linspace(0.25, 0.99, 75):
        e = sum(v*v for v in f((d, Phi)))
        if e < best[0]: best = (e, (d, Phi))
d_wk, Phi_wk = fsolve(f, best[1]); res = f((d_wk, Phi_wk))
assert max(abs(x) for x in res) < 1e-8 and 0 < d_wk < 1 and PLO < Phi_wk < 1, ("tuning failed", d_wk, Phi_wk, res)
u_wk = U_WK; Pwk = (PLO, Phi_wk)
print(f"tuning: EC c={c_ec:.4f} p0={p0:.4f} | SH levels {Plev[0]:.4f},{Plev[1]:.4f} | WK u={u_wk:.3f} d={d_wk:.4f} levels {Pwk[0]:.3f},{Pwk[1]:.4f}")
W = {'SH': dict(P=Plev), 'EC': dict(c=c_ec, p0=p0), 'WK': dict(P=Pwk, u=u_wk, d=d_wk)}

print("\nP1  stationary error rate and covariance at lags 1..6 (matched at lag 1 by construction)")
for w, kw in W.items():
    r, cv = stats(w, **kw); print(f"  {w}: rate={r:.5f}  cov_k = " + " ".join(f"{x:.5f}" for x in cv))

# passive TV between worlds at word length 6
def law(world, n, **kw):
    M, D, pv = build(world, **kw); Ms = M[0] + M[1]; pi = stationary(Ms); out = {}
    for w in itertools.product((0, 1), repeat=n):
        v = pi.copy()
        for o in w: v = v @ M[o]
        out[w] = v.sum()
    return out
L = {w: law(w, 6, **kw) for w, kw in W.items()}
tv = lambda a, b: 0.5*sum(abs(a[k]-b[k]) for k in a)
print("\n  passive TV of length-6 error-word laws (matched lag-1 cov): "
      f"SH-EC {tv(L['SH'],L['EC']):.4f}  SH-WK {tv(L['SH'],L['WK']):.4f}  EC-WK {tv(L['EC'],L['WK']):.4f}")
# exchangeability: words with the same error count have equal probability iff mixture of iid
def exch_gap(Lw):
    g = 0.0
    for k in range(7):
        ps = [Lw[w] for w in Lw if sum(w) == k]; g = max(g, max(ps)-min(ps))
    return g
print("  exchangeability gap (max prob spread within equal-count words): " + "  ".join(f"{w}={exch_gap(L[w]):.2e}" for w in W))

# ---------- interventions ----------
def curves(world, **kw):
    M, D, pv = build(world, **kw); Ms = M[0] + M[1]; pi = stationary(Ms); r = pi @ pv
    def fut(v, k): return v @ np.linalg.matrix_power(Ms, k-1) @ pv
    pi_do = pi @ D                                  # force an error
    pi_ob = pi @ M[1]; pi_ob = pi_ob/pi_ob.sum()     # condition on an error
    RA = np.zeros((NS, NS)); RS = np.zeros((NS, NS))
    for (s, l), i in idx.items(): RA[i, idx[(s, 0)]] = 1; RS[i, idx[(0, l)]] = 1
    out = {}
    out['do'] = [fut(pi_do, k) - r for k in range(1, 7)]
    out['observe'] = [fut(pi_ob, k) - r for k in range(1, 7)]
    out['do|agentReset'] = [fut(pi_do@RA, k) - fut(pi@RA, k) for k in range(1, 7)]
    out['do|soilReset'] = [fut(pi_do@RS, k) - fut(pi@RS, k) for k in range(1, 7)]
    return out
CV = {w: curves(w, **kw) for w, kw in W.items()}
print("\nP2/P3/P4  effect of the probe on error rate at lags 1..6")
for key in ('do', 'observe', 'do|agentReset', 'do|soilReset'):
    print(f" {key}:")
    for w in W: print(f"   {w}: " + " ".join(f"{x:+.5f}" for x in CV[w][key]))

# ---------- P5: integral (EWMA) estimator vs oracle after a probe ----------
alpha = 0.3
def kl(p, q): return p*np.log(p/q) + (1-p)*np.log((1-p)/(1-q))
def ewma_excess(world, probe, T=6, **kw):
    M, D, pv = build(world, **kw); Ms = M[0] + M[1]; pi = stationary(Ms); r = pi @ pv
    q0 = r                                     # estimator starts calibrated to the stationary rate
    if probe: v0 = pi @ D; qp = (1-alpha)*q0 + alpha*1.0
    else:     v0 = pi.copy(); qp = q0         # no probe: estimator has seen nothing new
    # expected KL(oracle p(state) || q(history)) at each lag k=1..T, enumerating histories
    alphas = {(): (v0, qp)}; res = []
    for k in range(1, T+1):
        tot = 0.0
        for h, (v, q) in alphas.items():
            for i in range(NS): tot += v[i]*kl(np.clip(pv[i], 1e-9, 1-1e-9), np.clip(q, 1e-9, 1-1e-9))
        res.append(tot)
        new = {}
        for h, (v, q) in alphas.items():
            for o in (0, 1): new[h+(o,)] = (v @ M[o], (1-alpha)*q + alpha*o)
        alphas = new
    return np.array(res)
print("\nP5  EWMA(alpha=.3) estimator: expected KL(oracle||estimate) in millinats, lags 1..6; excess = probe minus no-probe")
for w, kw in W.items():
    a = ewma_excess(w, True, **kw); b = ewma_excess(w, False, **kw)
    print(f"  {w}: probe " + " ".join(f"{1e3*x:7.2f}" for x in a) + " | no-probe " + " ".join(f"{1e3*x:7.2f}" for x in b)
          + " | excess " + " ".join(f"{1e3*(x-y):+7.2f}" for x, y in zip(a, b)))
