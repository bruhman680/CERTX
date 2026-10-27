"""
SOIL BUDGET: equal-budget comparison of observation/intervention designs for telling shadow / echo / wake apart.  Exact enumeration + asymptotic Chernoff exponent. No sampling.
Reuses the soil toy's three carriers (same rate .2, same lag-1 covariance .032) by executing the model section of soil_toy.py unchanged.
A 'design' is what happens at the start of an episode (from the stationary state) before outcomes are recorded:
  PASS        observe 6 outcomes, no intervention
  DO_F        force one error (state updates as after an error; the forced outcome is not recorded), observe the next 5
  DO_S        force one success the same way, observe 5
  RESET_A     exact agent reset l:=0, observe 6        RESET_S  exact soil reset s:=0, observe 6        RESET_S80  soil reset succeeds w.p. .8 else no change
Arms can be mixed with known assignment (e.g. DO_F/DO_S half-half).  Budget = number of episodes (each episode records 5 or 6 binary outcomes).
For worlds P,Q and a design (or mixture with fractions f_a) the Chernoff exponent is C = -min_{lam in [0,1]} sum_a f_a log sum_w P_a(w)^lam Q_a(w)^(1-lam), per episode.
Asymptotically the equal-prior Bayes error is about (1/2)exp(-N C), so N(5%) ~ ln(10)/C (APPROXIMATION; small-N error is not guaranteed by this).  KL is also reported.

PREDICTIONS (written before running):
 P1 Under PASS the hardest pair is SH-WK (smallest C): N(5%) at least 20x that of SH-EC.
 P2 DO_F raises C for SH-WK by at least 5x relative to PASS (SH ignores the probe, WK has a .084 lag-1 response).
 P3 DO_F raises C for EC-WK by less than 3x relative to PASS (both respond; they differ in decay).
 P4 Exact RESET_S gives the largest C among single-arm designs for SH-EC and EC-WK; for SH-WK it is uncertain (both have a soil).
 P5 The leaky reset keeps a fraction of the exact reset's C: C(RESET_S80)/C(RESET_S) between .5 and .8 for each pair (information roughly quadratic in effect size).
 P6 SH-WK needs at least 1,000 PASS episodes for ~5% error but under 100 episodes with the best design.
 Not tested: sample sizes below the asymptotic regime, real agents, calibration uncertainty of resets, unequal intervention cost.
"""
import io, contextlib, itertools, numpy as np
from scipy.optimize import minimize_scalar
src = open('/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/soil_relay/soil_toy.py').read().split('# passive TV between worlds')[0]
ns = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, ns)
build, stationary, W, idx, NS, STATES = ns['build'], ns['stationary'], ns['W'], ns['idx'], ns['NS'], ns['STATES']

def forced(world, kw, o):
    """transition for a forced outcome o (no emission weight)."""
    P = kw.get('P'); u = kw.get('u', 0.0); d = kw.get('d', 0.0); T = np.zeros((NS, NS))
    for (s, l), i in idx.items():
        if world == 'WK':
            if o == 1: nxt = {1: 1.0} if s == 1 else {1: u, 0: 1-u}
            else:      nxt = {0: 1.0} if s == 0 else {0: d, 1: 1-d}
        else: nxt = {s: 1.0}
        for s2, ps in nxt.items(): T[i, idx[(s2, o)]] += ps
    return T
RA = np.zeros((NS, NS)); RS = np.zeros((NS, NS))
for (s, l), i in idx.items(): RA[i, idx[(s, 0)]] = 1; RS[i, idx[(0, l)]] = 1

def design_law(world, design):
    kw = W[world]; M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    n = 6
    if design == 'PASS': v = pi
    elif design == 'DO_F': v = pi @ forced(world, kw, 1); n = 5
    elif design == 'DO_S': v = pi @ forced(world, kw, 0); n = 5
    elif design == 'RESET_A': v = pi @ RA
    elif design == 'RESET_S': v = pi @ RS
    elif design == 'RESET_S80': v = 0.2*pi + 0.8*(pi @ RS)
    out = {}
    for w in itertools.product((0, 1), repeat=n):
        x = v.copy()
        for o in w: x = x @ M[o]
        out[w] = x.sum()
    return out
LAW = {(w, d): design_law(w, d) for w in W for d in ('PASS', 'DO_F', 'DO_S', 'RESET_A', 'RESET_S', 'RESET_S80')}

def kl(P, Q): return sum(p*np.log(p/Q[w]) for w, p in P.items() if p > 0)
def chernoff(arms, A, B):
    def g(lam): return sum(f*np.log(sum((LAW[(A, d)][w]**lam)*(LAW[(B, d)][w]**(1-lam)) for w in LAW[(A, d)])) for d, f in arms)
    r = minimize_scalar(g, bounds=(0, 1), method='bounded', options={'xatol': 1e-10})
    return -r.fun
def klmix(arms, A, B): return sum(f*kl(LAW[(A, d)], LAW[(B, d)]) for d, f in arms)
PAIRS = [('SH', 'EC'), ('SH', 'WK'), ('EC', 'WK')]
DESIGNS = {
 'PASS': [('PASS', 1)], 'DO_F': [('DO_F', 1)], 'DO_F/DO_S': [('DO_F', .5), ('DO_S', .5)],
 'RESET_A': [('RESET_A', 1)], 'RESET_S': [('RESET_S', 1)], 'RESET_S80': [('RESET_S80', 1)],
 'RESET_A/RESET_S': [('RESET_A', .5), ('RESET_S', .5)], 'PASS/DO_F': [('PASS', .5), ('DO_F', .5)],
 'PASS/RESET_S': [('PASS', .5), ('RESET_S', .5)],
}
C = {}
print("Chernoff exponent C per episode (nats), and N(5%) ~ ln(10)/C episodes [asymptotic approximation]")
print(f"{'design':18s}" + "".join(f"  {a}-{b:2s} C        N(5%)   KL(A||B)/KL(B||A)" for a, b in PAIRS))
for name, arms in DESIGNS.items():
    row = f"{name:18s}"
    for a, b in PAIRS:
        c = chernoff(arms, a, b); C[(name, a, b)] = c
        row += f"  {c:9.5f} {np.log(10)/c:9.1f}  {klmix(arms, a, b):.4f}/{klmix(arms, b, a):.4f}"
    print(row)
print("\nChecks against predictions:")
n_pass = {p: np.log(10)/C[('PASS',)+p] for p in PAIRS}
print(f" P1 hardest pair under PASS: {min(PAIRS, key=lambda p: C[('PASS',)+p])}; N(SH-WK)/N(SH-EC) = {n_pass[('SH','WK')]/n_pass[('SH','EC')]:.1f}")
for p in PAIRS: print(f" P2/P3 C(DO_F)/C(PASS) for {p[0]}-{p[1]} = {C[('DO_F',)+p]/C[('PASS',)+p]:.2f}")
for p in PAIRS:
    singles = {k: C[(k,)+p] for k in ('PASS', 'DO_F', 'RESET_A', 'RESET_S')}
    print(f" P4 best single-arm design for {p[0]}-{p[1]}: {max(singles, key=singles.get)}  (" + ", ".join(f"{k} {v:.4f}" for k, v in singles.items()) + ")")
for p in PAIRS: print(f" P5 C(RESET_S80)/C(RESET_S) for {p[0]}-{p[1]} = {C[('RESET_S80',)+p]/C[('RESET_S',)+p]:.2f}")
best = {p: max(C[(k,)+p] for k in DESIGNS) for p in PAIRS}
bk = {p: max(DESIGNS, key=lambda k: C[(k,)+p]) for p in PAIRS}
for p in PAIRS: print(f" P6 {p[0]}-{p[1]}: N(PASS) {n_pass[p]:.0f}  best design {bk[p]} N {np.log(10)/best[p]:.1f}")
# sanity: laws normalize
print("\nmax |sum(law)-1| over all design laws:", max(abs(sum(v.values())-1) for v in LAW.values()))

# ---- P7 (added after seeing the first table, before running this block): C of a known-assignment mixture is at most the f-weighted average of its arms' C
# (min of an average >= average of mins). So no DO_F/RESET_S mixture can beat the better arm on the pair where the other arm is weak.
# Prediction: max over f of min-over-pairs C(f*DO_F + (1-f)*RESET_S) is attained at f=1 (pure DO_F, min-pair C ~ .0197).
print("\nP7 mixture f*DO_F + (1-f)*RESET_S: min over pairs of C, and the bound check C_mix <= weighted average of arm C")
viol = 0
for f in (0, .25, .5, .75, .9, 1.0):
    arms = [('DO_F', f), ('RESET_S', 1-f)] if 0 < f < 1 else [('DO_F', 1)] if f == 1 else [('RESET_S', 1)]
    cs = {p: chernoff(arms, *p) for p in PAIRS}
    for p in PAIRS:
        avg = f*C[('DO_F',)+p] + (1-f)*C[('RESET_S',)+p]
        viol += cs[p] > avg + 1e-9
    print(f"  f={f:4.2f}  min-pair C = {min(cs.values()):.5f} (N5% {np.log(10)/min(cs.values()):6.1f})  " + "  ".join(f"{p[0]}-{p[1]}:{v:.4f}" for p, v in cs.items()))
print("  bound violations:", viol)
