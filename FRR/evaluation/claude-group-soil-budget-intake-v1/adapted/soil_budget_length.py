"""
SOIL BUDGET, robustness to episode length. Codex's ST-C1 notes that small passive TV at word length 6 is not a sample-complexity theorem. My soil_budget.py fixed length 6, so 'N(PASS)=11,490 episodes' counts episodes of 6 outcomes.
Hidden-state worlds can leak information over longer windows (SH never switches soil; WK switches on a ~50-step timescale). Here: Chernoff exponent C_n for blocks of n recorded outcomes, per recorded outcome (C_n/n), for SH-WK, SH-EC, EC-WK,
under PASS (n outcomes from stationarity) and DO_F (force one error, then record n outcomes). Exact enumeration of all 2^n words, n up to 16. Same worlds and Chernoff definition as soil_budget.py (models executed from soil_toy.py).

PREDICTIONS (written before running):
 P1 SH-WK under PASS: C_n/n rises with n (long windows reveal soil switching); C_16/16 is at least 5x C_6/6.
 P2 DO_F per-outcome advantage over PASS for SH-WK (C_n^DO/C_n^PASS) falls as n grows and is below 20 at n=16 (it was ~98x at n~5-6), but stays above 1.
 P3 For SH-EC and EC-WK, C_n/n under PASS is roughly flat in n beyond n~6 (echo memory is short), within a factor 1.5 between n=6 and n=16.
 P4 The conclusion 'distinguishability is cheap for SH-EC/EC-WK and expensive for SH-WK' survives at n=16 in per-outcome terms: C_16/16 (SH-WK) < C_16/16 (SH-EC) / 10 under PASS.
"""
import io, contextlib, itertools, numpy as np
from scipy.optimize import minimize_scalar
src = open('/workspace/frr/lineage/sources/claude-soil-intake-2026-10-21/soil_toy.py').read().split('# passive TV between worlds')[0]
ns = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, ns)
build, stationary, W, idx, NS = ns['build'], ns['stationary'], ns['W'], ns['idx'], ns['NS']

def forced1(world, kw):
    u = kw.get('u', 0.0); T = np.zeros((NS, NS))
    for (s, l), i in idx.items():
        nxt = ({1: 1.0} if s == 1 else {1: u, 0: 1-u}) if world == 'WK' else {s: 1.0}
        for s2, ps in nxt.items(): T[i, idx[(s2, 1)]] += ps
    return T
def word_probs(world, n, design):
    kw = W[world]; M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    v = pi if design == 'PASS' else pi @ forced1(world, kw)
    cur = v[None, :]                                  # shape (words, NS)
    for _ in range(n):
        cur = np.concatenate([cur @ M[0], cur @ M[1]], axis=0)   # word index grows by appending outcomes (consistent ordering across worlds)
    return cur.sum(1)
def chernoff(p, q):
    r = minimize_scalar(lambda lam: np.log(np.sum(np.exp(lam*np.log(p)+(1-lam)*np.log(q)))), bounds=(0, 1), method='bounded', options={'xatol': 1e-10})
    return -r.fun
PAIRS = [('SH', 'EC'), ('SH', 'WK'), ('EC', 'WK')]
NS_LIST = [6, 8, 10, 12, 14, 16]
C = {}
print("Chernoff exponent per episode C_n and per recorded outcome C_n/n")
print(f"{'design':5s} {'n':>3s}" + "".join(f"   {a}-{b} C_n/n" for a, b in PAIRS))
for design in ('PASS', 'DO_F'):
    for n in NS_LIST:
        P = {w: word_probs(w, n, design) for w in W}
        row = f"{design:5s} {n:3d}"
        for a, b in PAIRS:
            c = chernoff(P[a], P[b]); C[(design, n, a, b)] = c; row += f"   {c/n:11.6f}"
        print(row)
print("\nChecks:")
r = C[('PASS', 16, 'SH', 'WK')]/16 / (C[('PASS', 6, 'SH', 'WK')]/6)
print(f" P1 SH-WK PASS C_n/n at n=16 vs n=6: x{r:.1f}")
for n in NS_LIST: print(f" P2 n={n:2d}: DO_F/PASS exponent ratio (SH-WK) = {C[('DO_F', n, 'SH', 'WK')]/C[('PASS', n, 'SH', 'WK')]:.2f}")
for p in (('SH', 'EC'), ('EC', 'WK')):
    a = C[('PASS', 6)+p]/6; b = C[('PASS', 16)+p]/16
    print(f" P3 {p[0]}-{p[1]} PASS C_n/n n=6 -> n=16: {a:.5f} -> {b:.5f} (ratio {b/a:.2f})")
print(f" P4 PASS n=16: SH-WK {C[('PASS',16,'SH','WK')]/16:.6f} vs SH-EC/10 = {C[('PASS',16,'SH','EC')]/16/10:.6f}")
print(" N(5%) in episodes at n=16, PASS SH-WK:", round(np.log(10)/C[('PASS', 16, 'SH', 'WK')], 1), "-> recorded outcomes", round(16*np.log(10)/C[('PASS', 16, 'SH', 'WK')]))
