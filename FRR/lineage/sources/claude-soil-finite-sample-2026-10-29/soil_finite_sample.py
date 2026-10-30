"""
SOIL FINITE-SAMPLE CHECK. Closes the gap Codex's intake named: my printed N = ln(10)/C values were not finite-sample thresholds.
Worlds: SH/EC/WK from soil_toy.py (executed unchanged). Known laws, equal priors, likelihood-ratio classifier. Monte Carlo with independent RNG streams per role.
PART A (iid episodes from independent stationary starts): for each pair/design/window n, estimate classification error vs number of episodes N by sampling episode words
  from the exact word laws; compare to (i) the conservative bound 0.5*Z(s*)^N with s* the Chernoff optimum, (ii) the crossover N where error first <= 5%, vs the heuristic ln(10)/C.
  Bound is exact under these assumptions, so error <= bound must hold up to Monte Carlo noise (2.5k trials per cell -> SE about .004 at 5%).
PART B (contiguous trajectory, persistent soil): ONE long trajectory per trial (total T recorded outcomes) from the true world. Two classifiers:
  FULL = forward-algorithm likelihood of the whole trajectory (correct), IID-WIN = product over consecutive length-n windows of the stationary-start window law (misspecified: treats adjacent windows as independent).
  Error vs T for SH-WK and EC-WK.

PREDICTIONS (written before running):
 P1 Bound validity: observed error <= 0.5*Z^N + 3*SE in every cell.
 P2 The bound is conservative: at the heuristic N = ln(10)/C the observed error is below 5% in every cell, and the real crossover N is at least 1.3x smaller than ln(10)/C in the median over cells (because of the leading 1/2 and sub-exponential factors).
 P3 SH-WK, n=16, PASS: crossover N within a factor 2 of 244/1.3 ~ 190 (i.e. between 95 and 244) episodes.
 P4 Part B, SH-WK at T=3,900 outcomes (equal to 244 episodes x 16): FULL error <= 1% (it uses the soil's persistence), IID-WIN error >= 3% (it discards cross-window persistence). I expect FULL <= IID-WIN in every row.
 P5 Part B, EC-WK at T=640: both FULL and IID-WIN are below 5%; the gap between them is small (< 2 percentage points) because echo memory is short.
Not tested: unknown calibration, unknown candidate family, adaptive stopping, real agents.
"""
import io, contextlib, itertools, numpy as np
from scipy.optimize import minimize_scalar
SD = '/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/'
src = open(SD+'soil_relay/soil_toy.py').read().split('# passive TV between worlds')[0]
ns = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, ns)
build, stationary, W, idx, NS = ns['build'], ns['stationary'], ns['W'], ns['idx'], ns['NS']
ss = np.random.SeedSequence(20261029); G = [np.random.default_rng(s) for s in ss.spawn(4)]
RA, RB = G[0], G[1]          # part A sampling (truth P / truth Q) ; part B trajectories use G[2], G[3]

def forced1(world, kw):
    u = kw.get('u', 0.0); T = np.zeros((NS, NS))
    for (s, l), i in idx.items():
        nxt = ({1: 1.0} if s == 1 else {1: u, 0: 1-u}) if world == 'WK' else {s: 1.0}
        for s2, ps in nxt.items(): T[i, idx[(s2, 1)]] += ps
    return T
def word_probs(world, n, design):
    kw = W[world]; M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    v = pi if design == 'PASS' else pi @ forced1(world, kw)
    cur = v[None, :]
    for _ in range(n): cur = np.concatenate([cur @ M[0], cur @ M[1]], axis=0)
    p = cur.sum(1); return p/p.sum()
def chernoff(p, q):
    r = minimize_scalar(lambda lam: np.log(np.sum(np.exp(lam*np.log(p)+(1-lam)*np.log(q)))), bounds=(0, 1), method='bounded', options={'xatol': 1e-12})
    return -r.fun, r.x

# ---------------- PART A ----------------
TR = 2500
def err_curve(P, Q, Ns, rng):
    llr = np.log(P)-np.log(Q); out = {}
    Nmax = max(Ns)
    # sample TR x Nmax words under P and under Q once, take cumulative sums (nested N)
    wP = rng.choice(len(P), size=(TR, Nmax), p=P); wQ = rng.choice(len(Q), size=(TR, Nmax), p=Q)
    cP = np.cumsum(llr[wP], axis=1); cQ = np.cumsum(llr[wQ], axis=1)
    for N in Ns:
        a = cP[:, N-1]; b = cQ[:, N-1]
        e = 0.5*(np.mean(a < 0)+0.5*np.mean(a == 0)) + 0.5*(np.mean(b > 0)+0.5*np.mean(b == 0))
        out[N] = e
    return out
PAIRS = [('SH', 'EC'), ('SH', 'WK'), ('EC', 'WK')]
CASES = [('PASS', 6), ('DO_F', 5), ('PASS', 16)]
print("PART A: classification error vs episodes N (iid episodes). bound = .5*Z(s*)^N ; heuristic N_h = ln(10)/C")
viol = 0; ratios = []; below5 = []
res = {}
for design, n in CASES:
    P = {w: word_probs(w, n, design) for w in W}
    for a, b in PAIRS:
        C, s = chernoff(P[a], P[b]); Z = np.exp(-C)
        Nh = np.log(10)/C
        Nmax = int(min(max(3*Nh, 20), 30000))
        Ns = sorted(set(int(x) for x in np.unique(np.round(np.geomspace(1, Nmax, 60)))))
        e = err_curve(P[a], P[b], Ns, RA)
        bound = {N: 0.5*Z**N for N in Ns}
        for N in Ns:
            se = np.sqrt(max(e[N]*(1-e[N]), 1e-4)/TR)
            if e[N] > bound[N]+3*se: viol += 1
        cross = next((N for N in Ns if e[N] <= 0.05), None)
        Nh_i = min(Ns, key=lambda N: abs(N-Nh));
        eh = e[Nh_i]; ratios.append((Nh/cross) if cross else np.nan); below5.append(eh <= 0.05+3*np.sqrt(.05*.95/TR))
        res[(design, n, a, b)] = (C, Nh, cross, Nh_i, eh)
        print(f"  {design:4s} n={n:2d} {a}-{b}: C={C:.5f} s*={s:.3f} N_h={Nh:8.1f} | crossover N(<=5%)={cross} | err at N~N_h({Nh_i}) = {eh:.4f} | bound there {bound[Nh_i]:.4f}")
print(f"\nP1 violations of error <= bound + 3SE: {viol}")
print(f"P2 error at N_h below 5% in all cells: {all(below5)};  median(N_h / crossover) = {np.nanmedian(ratios):.2f}  (min {np.nanmin(ratios):.2f}, max {np.nanmax(ratios):.2f})")
print(f"P3 SH-WK PASS n=16: crossover {res[('PASS',16,'SH','WK')][2]} vs N_h {res[('PASS',16,'SH','WK')][1]:.0f}")

# ---------------- PART B ----------------
def simulate(world, T, rng):
    kw = W[world]; M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    i = rng.choice(NS, p=pi); out = np.zeros(T, dtype=int)
    J = [np.concatenate([M[0][s], M[1][s]]) for s in range(NS)]          # joint (outcome, next) probabilities per state
    cdf = [np.cumsum(j/j.sum()) for j in J]
    u = rng.random(T)
    for t in range(T):
        k = int(np.searchsorted(cdf[i], u[t])); k = min(k, 2*NS-1)
        o, j = divmod(k, NS); out[t] = o; i = j
    return out
def loglik_full(world, obs):
    kw = W[world]; M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    v = pi.copy(); ll = 0.0
    for o in obs:
        v = v @ M[o]; z = v.sum(); ll += np.log(z); v = v/z
    return ll
def loglik_iidwin(world, obs, n, table):
    w = obs[:len(obs)//n*n].reshape(-1, n); code = w @ (1 << np.arange(n-1, -1, -1))
    return np.sum(np.log(table[world][code]))
n = 16
table = {w: word_probs(w, n, 'PASS') for w in W}
# word_probs indexes words by the construction order (first outcome = most significant bit): matches code above
print("\nPART B: contiguous trajectory, persistent soil. error of FULL (forward likelihood) vs IID-WIN (n=16 windows treated independent), equal priors, 800 trials per cell")
RB2 = G[2]
for a, b, T in (('SH', 'WK', 800), ('SH', 'WK', 1600), ('SH', 'WK', 3904), ('EC', 'WK', 160), ('EC', 'WK', 320), ('EC', 'WK', 640)):
    trials = 800 if T <= 1600 else 400; ef = ei = 0.0
    for tr in range(trials):
        for truth, other, sgn in ((a, b, +1), (b, a, -1)):
            x = simulate(truth, T, RB2)
            df = loglik_full(truth, x)-loglik_full(other, x); di = loglik_iidwin(truth, x, n, table)-loglik_iidwin(other, x, n, table)
            ef += (df < 0)+0.5*(df == 0); ei += (di < 0)+0.5*(di == 0)
    print(f"  {a}-{b} T={T:5d} outcomes ({T//n} windows): FULL error {ef/(2*trials):.4f}   IID-WIN error {ei/(2*trials):.4f}   (trials {2*trials})")
