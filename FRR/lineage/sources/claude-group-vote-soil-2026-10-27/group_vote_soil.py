"""
GROUP-VOTE x SOIL toy: does matching marginal error rate and pairwise error covariance determine majority-vote error?  Exact computation (no sampling). numpy not needed.
n agents each give a binary outcome (1 = error). Marginal error rate .2 and mean pairwise covariance .032 (so pairwise correlation rho=.2) in every dependent world, as in the soil toy.
Worlds:
 IND     independent, p=.2.
 SH-sym  shared hidden soil (exchangeable mixture): levels .0211/.3789, prob 1/2 each  (soil toy's SH values; var .032).
 SH-asym shared hidden soil, SAME mean .2 and SAME variance .032 but asymmetric: levels .1 / .52 with P(high)=h=.238095 (solved from h(H-l)=.1, (1-h)(H-l)=.32).
 EC      sequential 'copy' chain: agent1 errs w.p. .2, agent k errs w.p. .16+.2*(agent k-1 erred). Adjacent covariance .032, geometric decay beyond that (NOT all pairs).
Majority wrong = more than n/2 errors (n odd).
Intervention contrast for n=5: baseline P(majority wrong); observe(agent 1 wrong); do(agent 1 forced wrong). In SH soil is not touched by do; in EC downstream agents respond causally; in IND nothing spreads.

PREDICTIONS (written before running):
 P1 mean pairwise covariance is .032 in SH-sym and SH-asym by construction (exchangeable) and below .032 averaged over all pairs in EC (adjacent only matches). Report it.
 P2 n=3 majority error ordering: IND(.104) < EC < SH-asym < SH-sym < .2 (perfect sharing).
 P3 large n: IND -> 0, EC -> 0, SH-sym -> 0 (both soil levels < .5), SH-asym -> P(high soil)=.238 (high level .52 > .5). So at matched marginal and matched pairwise covariance SH-sym and SH-asym have opposite large-n limits. Ordering at n=101 reverses: SH-asym worst by far.
 P4 n=5 intervention: SH: do(agent1 wrong) leaves the other four exactly as at baseline; observe raises them. EC and IND: observe == do for downstream agents (no hidden confounder); EC propagates, IND does not.
 Not claimed: any of this describes real agents; levels, mixture weights and the copy rule are constructed.
"""
from math import comb
def f_binom_tail(n, p, need):                                      # P(Binomial(n,p) >= need)
    return sum(comb(n, k)*p**k*(1-p)**(n-k) for k in range(need, n+1))
def mix_maj(n, levels):                                            # levels: [(weight, p)]
    need = n//2+1
    return sum(w*f_binom_tail(n, p, need) for w, p in levels)
def chain_dist(n, start_last=None, start_count=0, first_p=None):
    # DP over (errors so far, last outcome). EC rule p_k = .16 + .2*last
    pw = {(0, 0): 0.0, (0, 1): 0.0}
    dist = {}
    if start_last is None:
        dist = {(1, 1): .2, (0, 0): .8}; k0 = 1
    else:
        dist = {(start_count, start_last): 1.0}; k0 = 1
    for _ in range(k0, n):
        nd = {}
        for (c, l), pr in dist.items():
            p = .16+.2*l
            nd[(c+1, 1)] = nd.get((c+1, 1), 0)+pr*p
            nd[(c, 0)] = nd.get((c, 0), 0)+pr*(1-p)
        dist = nd
    return dist
def chain_maj(n, **kw):
    d = chain_dist(n, **kw); return sum(pr for (c, l), pr in d.items() if c > n/2)
lo, hi = .0211, .3789
SYM = [(.5, lo), (.5, hi)]
h = .1/.42; L, H = .1, .52
ASYM = [(1-h, L), (h, H)]
def mom(levels):
    m = sum(w*p for w, p in levels); v = sum(w*p*p for w, p in levels)-m*m; return m, v
print("soil moments (mean, var=pairwise covariance for exchangeable mixture):  SH-sym", [round(x, 6) for x in mom(SYM)], " SH-asym", [round(x, 6) for x in mom(ASYM)], " h =", round(h, 6))
# EC: mean pairwise covariance for n=9
def chain_pair_cov(n):
    import itertools
    tot = 0; cnt = 0
    # exact joint of the chain via enumeration
    P = {}
    for bits in itertools.product((0, 1), repeat=n):
        pr = .2 if bits[0] else .8
        for k in range(1, n):
            p = .16+.2*bits[k-1]; pr *= p if bits[k] else (1-p)
        P[bits] = pr
    m = [sum(pr*b[i] for b, pr in P.items()) for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            e = sum(pr*b[i]*b[j] for b, pr in P.items()); tot += e-m[i]*m[j]; cnt += 1
    adj = sum(sum(pr*b[i]*b[i+1] for b, pr in P.items())-m[i]*m[i+1] for i in range(n-1))/(n-1)
    return tot/cnt, adj
mc, adj = chain_pair_cov(9)
print(f"P1: EC chain (n=9) mean pairwise covariance {mc:.5f}, adjacent {adj:.5f}; SH-sym and SH-asym mean pairwise covariance .032 by exchangeability.")
print("\nMajority-wrong probability (exact):")
print("   n      IND      EC     SH-sym   SH-asym   perfect-sharing (=.2)")
for n in (1, 3, 5, 9, 15, 31, 101):
    print(f"{n:4d}  {mix_maj(n, [(1, .2)]):7.4f}  {chain_maj(n):7.4f}  {mix_maj(n, SYM):7.4f}  {mix_maj(n, ASYM):7.4f}   .2000")
print("limit n->inf: SH-asym tends to P(high soil) =", round(h, 6), "(level .52 > .5); SH-sym levels both < .5 -> 0")

n = 5; need = n//2+1
print("\nn=5 intervention contrast: P(majority wrong) and the mean error rate of the OTHER four agents")
def sh_other(levels, mode):
    if mode == "base": w = [(wt, p) for wt, p in levels]
    elif mode == "observe":
        z = sum(wt*p for wt, p in levels); w = [(wt*p/z, p) for wt, p in levels]
    else: w = [(wt, p) for wt, p in levels]                          # do: soil untouched
    maj = sum(wt*f_binom_tail(n-1, p, need-1) for wt, p in w) if mode != "base" else mix_maj(n, levels)
    oth = sum(wt*p for wt, p in w); return maj, oth
for name, lv in (("SH-sym", SYM), ("SH-asym", ASYM), ("IND", [(1, .2)])):
    b = sh_other(lv, "base"); o = sh_other(lv, "observe"); d = sh_other(lv, "do")
    print(f"  {name:8s} base maj {b[0]:.4f} others {b[1]:.4f} | observe(1 wrong) maj {o[0]:.4f} others {o[1]:.4f} | do(1 wrong) maj {d[0]:.4f} others {d[1]:.4f}")
bd = chain_dist(n); base = chain_maj(n)
dd = chain_dist(n, start_last=1, start_count=1); mj = chain_maj(n, start_last=1, start_count=1)
oth = sum(pr*(c-1) for (c, l), pr in dd.items())/(n-1)
print(f"  EC       base maj {base:.4f} others {.2:.4f} | observe(1 wrong)=do(1 wrong) maj {mj:.4f} others {oth:.4f}  (no hidden confounder: observe == do for downstream agents)")
