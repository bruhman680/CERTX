# Working-copy correction: independent fair-coin noise; original preserved.
import numpy as np
rng = np.random.default_rng(1)
K = np.array([[[.85,.15],[.10,.90]],[[.55,.45],[.40,.60]]])

def T_shadow(eps, yp):
    return np.array([[1-eps, eps],[eps, 1-eps]])
def T_echo(delta, yp):
    row = np.zeros(2); row[yp] += (1-delta); row += delta/2
    return np.array([row, row])
def getT(model, p):
    return (lambda yp: T_shadow(p, yp)) if model == 'shadow' else (lambda yp: T_echo(p, yp))

def forward(model, p, n):
    """alpha[w] = P(w, e_next); y0 uniform, e0 uniform."""
    T = getT(model, p)
    cur = {(0,): 0.25*np.ones(2)*2/2*0.5*2/2, (1,): 0.25*np.ones(2)*2/2*0.5*2/2}
    cur = {(0,): np.array([.25,.25]), (1,): np.array([.25,.25])}   # P(y0)=.5, P(e0)=.5
    for t in range(1, n):
        nxt = {}
        for w, a in cur.items():
            yp = w[-1]; Tm = T(yp)
            for y in (0, 1):
                lik = np.array([K[e][yp][y] for e in (0, 1)])
                nxt[w+(y,)] = (a*lik) @ Tm
        cur = nxt
    return cur

def law(model, p, n):
    return {w: a.sum() for w, a in forward(model, p, n).items()}

def tv(a, b):
    return 0.5*sum(abs(a[k]-b[k]) for k in a)

def pred_count(model, p, n):
    s = set()
    for w, a in forward(model, p, n).items():
        b = a/a.sum()
        s.add(round(float(sum(b[e]*K[e][w[-1]][1] for e in (0, 1))), 9))
    return len(s)

# ---------- sanity checks ----------
n = 8
ref = tv(law('shadow', 0.0, n), law('echo', 0.0, n))
print(f"sanity: TV(shadow eps=0, echo delta=0) n=8 = {ref:.4f}  (earlier run: 0.3604)")
print(f"sanity: TV(shadow eps=.5, echo delta=1) n=8 = {tv(law('shadow',0.5,n), law('echo',1.0,n)):.2e}  (both iid-e; expect ~0)")
print(f"sanity: total probability = {sum(law('shadow',0.1,n).values()):.12f}")

IID = lambda n: law('shadow', 0.5, n)

# ---------- Sweep A: noisy shadow ----------
print("\nA. shadow(eps): e flips w.p. eps per step (eps=0 frozen, eps=.5 iid e)")
print(" eps    TV->echo0(n=8) TV->echo0(n=12) TV->iid(n=12) predStates(n=12)")
n12E = law('echo', 0.0, 12); n8E = law('echo', 0.0, 8); n12I = IID(12)
for eps in (0, .005, .01, .02, .05, .1, .2, .35, .5):
    L8 = law('shadow', eps, 8); L12 = law('shadow', eps, 12)
    print(f" {eps:5.3f}  {tv(L8,n8E):10.4f}   {tv(L12,n12E):10.4f}   {tv(L12,n12I):10.4f}   {pred_count('shadow',eps,12):6d}")

# ---------- Sweep B: noisy echo ----------
print("\nB. echo(delta): e' = y_prev w.p. 1-delta, else fair coin (delta=0 echo, delta=1 iid e)")
print(" delta  TV->shadow0(n=12) TV->echo0(n=12) TV->iid(n=12) predStates(n=12)")
n12S = law('shadow', 0.0, 12)
for d in (0, .05, .1, .2, .35, .5, .75, 1.0):
    L12 = law('echo', d, 12)
    print(f" {d:5.2f}  {tv(L12,n12S):10.4f}      {tv(L12,n12E):10.4f}    {tv(L12,n12I):10.4f}   {pred_count('echo',d,12):6d}")

# ---------- Simulation: spread of per-trajectory switch rate ----------
def sim_rates(model, p, T=3000, R=200):
    U = rng.random((R, T)); V = rng.random((R, T)); W = rng.random((R, T)); out = np.empty(R)
    for r in range(R):
        e = rng.integers(2); y = rng.integers(2); yp_old = y; sw = 0
        for t in range(T):
            y2 = 1 if U[r, t] < K[e][y][1] else 0
            sw += (y2 != y)
            if model == 'shadow':
                if V[r, t] < p: e = 1-e
            else:
                e = y if V[r, t] >= p else int(W[r, t] < 0.5)
            y = y2
        out[r] = sw/T
    return out

print("\nSim: per-trajectory switch rate, T=3000, 200 runs (hist bins 0.10..0.50)")
bins = np.linspace(0.1, 0.5, 9)
for name, model, p in (("shadow eps=0", 'shadow', 0.0), ("shadow eps=.0005", 'shadow', 0.0005),
                       ("shadow eps=.002", 'shadow', 0.002), ("shadow eps=.01", 'shadow', 0.01),
                       ("shadow eps=.05", 'shadow', 0.05), ("shadow eps=.5 (iid e)", 'shadow', 0.5),
                       ("echo delta=0", 'echo', 0.0), ("echo delta=.2", 'echo', 0.2)):
    r = sim_rates(model, p)
    print(f" {name:22s} mean={r.mean():.3f} sd={r.std():.4f} hist={np.histogram(r,bins=bins)[0].tolist()}")
