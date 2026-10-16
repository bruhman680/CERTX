"""
WAKE experiment on the shadow-echo edge family.
Focal visible y in {0,1}; environment bit e in {0,1} selects the kernel K[e][y] (same table as before).
Environment update: e' = y_prev w.p. h (environment re-records the focal state), else e stays.
  h=0  frozen e (shadow);  small h  slow environment (wake);  h=1  e copies visible symbol (echo).
Whether e is 'environment' or 'focal memory' is a DECLARED BOUNDARY, not something the dynamics decide.

PREDICTIONS (written before running):
 W1. Reset effect (focal reset to y=0, env kept e0=1 vs env reset e0=0): TV at t=1 is 0.30 for every h
     (depends only on K). Later decay is governed by max(1-h, 0.45)^t; 0.45 = 2nd eigenvalue of the
     e-averaged visible chain. So for h=1 the effect still decays like 0.45^t, not instantly.
 W2. A passively-adequate history model can still be badly wrong right after reset-with-env-kept:
     excess KL at t=0 is identical for M_1 and M_10 (cleared history carries nothing), ~0.05 nats.
 W3. Belief predictor B (stationary prior over e, sees only post-reset symbols) beats M_k right after
     reset only if it uses structure; at t=0 it equals M_k (same information). It recovers e over time.
"""
import numpy as np

K = np.array([[[.85,.15],[.10,.90]],[[.55,.45],[.40,.60]]])

def Tm(h, yp):
    T = (1-h)*np.eye(2); T[:, yp] += h; return T

def joint_chain(h):
    P = np.zeros((4,4))
    for y in (0,1):
        for e in (0,1):
            for y2 in (0,1):
                for e2 in (0,1):
                    P[2*y+e, 2*y2+e2] = K[e][y][y2]*Tm(h,y)[e,e2]
    return P

def stationary(P):
    return np.ones(4)/4 @ np.linalg.matrix_power(P, 2**14)   # uniform e start (needed for h=0)

def expand(h, init, n):
    cur = {(y,): np.array(a, float) for y, a in init.items()}
    levels = [cur]
    for t in range(1, n):
        nxt = {}
        for w, a in cur.items():
            yp = w[-1]; T = Tm(h, yp)
            for y in (0,1):
                lik = np.array([K[e][yp][y] for e in (0,1)])
                nxt[w+(y,)] = (a*lik) @ T
        cur = nxt; levels.append(cur)
    return levels

def KL(p, q):
    p = np.asarray(p); q = np.asarray(q); m = p > 0
    return float((p[m]*np.log(p[m]/q[m])).sum())

def run(h):
    P = joint_chain(h); pi = stationary(P)
    stat = expand(h, {0: pi[0:2], 1: pi[2:4]}, 11)          # stationary word law, lengths 1..11
    Pst = lambda w: stat[len(w)-1][w].sum()
    def Qk(k, w):
        j = min(k, len(w)); u = w[-j:]; pu = Pst(u)
        return np.array([Pst(u+(0,)), Pst(u+(1,))])/pu
    # passive excess of order-k history model vs oracle (knows e)
    passive = {}
    for k in (1, 3, 6, 10):
        tot = 0.0
        for u, a in stat[k-1].items():
            Q = Qk(k, u)
            for e in (0,1):
                if a[e] > 0: tot += a[e]*KL(K[e][u[-1]], Q)
        passive[k] = tot
    # reset-effect TV (visible marginal), env kept (e0=1) vs env reset (e0=0)
    Pn = {0: np.linalg.matrix_power(P, 0)}
    d1 = np.zeros(4); d1[2*0+1] = 1; d0 = np.zeros(4); d0[0] = 1
    tvs = {}
    for t in (1, 2, 4, 8, 16, 32):
        Mt = np.linalg.matrix_power(P, t)
        p1 = lambda d: (d @ Mt)[2] + (d @ Mt)[3]
        tvs[t] = abs(p1(d1)-p1(d0))
    # post-reset excess KL for predictors that never see e
    prior = pi[0:2]/pi[0:2].sum()
    levB = expand(h, {0: prior}, 9)
    def reset_excess(e0, which):
        init = {0: [1.0 if e == e0 else 0.0 for e in (0,1)]}
        lev = expand(h, init, 9); out = []
        for t in range(9):
            tot = 0.0
            for w, a in lev[t].items():
                if which == 'B':
                    b = levB[t][w]; b = b/b.sum()
                    Q = sum(b[e]*np.array(K[e][w[-1]]) for e in (0,1))
                else:
                    Q = Qk(which, w)
                for e in (0,1):
                    if a[e] > 0: tot += a[e]*KL(K[e][w[-1]], Q)
            out.append(tot)
        return out
    return passive, tvs, {('M10',1): reset_excess(1,10), ('B',1): reset_excess(1,'B'),
                          ('M1',1): reset_excess(1,1), ('M10',0): reset_excess(0,10)}

print("passive excess KL of order-k history model over oracle (millinats/step)")
print("  h     k=1     k=3     k=6    k=10 |  reset-effect TV at t=1,2,4,8,16,32")
res = {}
for h in (0.0, 0.02, 0.05, 0.2, 0.5, 1.0):
    res[h] = run(h); p, tv, _ = res[h]
    print(f" {h:4.2f} " + " ".join(f"{1e3*p[k]:7.3f}" for k in (1,3,6,10)) + " |  " + " ".join(f"{tv[t]:.3f}" for t in (1,2,4,8,16,32)))
print("\npost-reset excess KL over oracle (millinats), steps t=0,1,2,4,8 after focal reset")
print("  h    env-kept(e0=1): M1 | M10 | belief B      env-reset(e0=0): M10")
for h in res:
    r = res[h][2]; idx = (0,1,2,4,8)
    f = lambda key: " ".join(f"{1e3*r[key][i]:6.1f}" for i in idx)
    print(f" {h:4.2f}  {f(('M1',1))} | {f(('M10',1))} | {f(('B',1))}      {f(('M10',0))}")
