"""
SOIL DISPERSION DIAGNOSTIC: can model-light statistics of window error counts detect shared/persistent soil without knowing the dynamics?
Worlds SH/EC/WK from soil_toy.py (executed unchanged); contiguous trajectory of T outcomes split into M=T/n windows of n=16. Features of the window counts k_1..k_M:
  DI  = sample variance of k / (n * pbar * (1-pbar))      (dispersion index; 1 for iid Bernoulli outcomes)
  AC1 = lag-1 autocorrelation of k_j across windows
Classifier: diagonal-Gaussian naive Bayes fitted on a SEPARATE calibration set of trajectories (independent RNG stream); evaluated on held-out trajectories.
Rival/ceiling: FULL = forward-algorithm likelihood of the whole trajectory under each of the 3 known worlds (needs the dynamics). 3-way equal-prior classification.
Analytic expectations for orientation (asymptotic, n=16): SH window count has between-window variance n^2*.032=8.2 vs binomial n*.16=2.56 -> DI about 4.2 and AC1 about .76 (same soil every window).

PREDICTIONS (written before running):
 P1 At T=1600 (100 windows) mean DI: SH in [3.5,5.0]; EC in [1.2,2.0]; WK in [2.5,4.5]. Mean AC1: SH > .5; EC < .1; WK between EC and SH and below .5.
 P2 DI alone cannot separate SH from WK (distributions overlap: 2-way SH-WK accuracy from DI alone <= .75 at T=1600); AC1 does better than DI for SH-WK.
 P3 The 2-feature diagnostic reaches 3-way accuracy >= .90 at T=1600 and >= .70 at T=320 (20 windows).
 P4 FULL likelihood beats the diagnostic at every T (it uses the exact dynamics) by at least 3 accuracy points at T=320; both approach 1.0 by T=1600 or 3200.
 P5 (misspecification link) If the diagnostic's calibration set is drawn from DIFFERENT world parameters than the test (EC with c=.35 instead of .2, same marginal rate), 3-way accuracy falls by at least 10 points at T=800, while FULL (which assumes the original laws) falls to <= .67 on the shifted EC trajectories, because EC-shift is not one of its candidates.
Not tested: unknown number of candidate worlds, real agents, finer windows, other window lengths.
"""
import io, contextlib, numpy as np
SD = '/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad/'
src = open(SD+'soil_relay/soil_toy.py').read().split('# passive TV between worlds')[0]
ns = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, ns)
build, stationary, W, idx, NS = ns['build'], ns['stationary'], ns['W'], ns['idx'], ns['NS']
ss = np.random.SeedSequence(20261030); G = [np.random.default_rng(s) for s in ss.spawn(4)]
CALR, TESTR, SHIFTR = G[0], G[1], G[2]
n = 16
WORLDS = ('SH', 'EC', 'WK')

def kern(world, kw):
    M, D, pv = build(world, **kw); pi = stationary(M[0]+M[1])
    J = np.stack([np.concatenate([M[0][s], M[1][s]]) for s in range(NS)])          # state -> joint (outcome,next) over 2*NS
    return M, pi, np.cumsum(J/J.sum(1, keepdims=True), axis=1)
def simulate(kinfo, R, T, rng):
    M, pi, cdf = kinfo
    i = rng.choice(NS, size=R, p=pi/pi.sum()); out = np.zeros((R, T), dtype=np.int8)
    U = rng.random((R, T))
    for t in range(T):
        k = (U[:, t][:, None] > cdf[i]).sum(1); k = np.minimum(k, 2*NS-1)
        out[:, t] = k//NS; i = k % NS
    return out
def features(x):
    R, T = x.shape; Mw = T//n; k = x[:, :Mw*n].reshape(R, Mw, n).sum(2).astype(float)
    pbar = k.mean(1)/n; var = k.var(1, ddof=1); DI = var/np.maximum(n*pbar*(1-pbar), 1e-9)
    kc = k-k.mean(1, keepdims=True); den = (kc**2).sum(1); AC = (kc[:, 1:]*kc[:, :-1]).sum(1)/np.maximum(den, 1e-9)
    return np.stack([DI, AC], 1)
def loglik_full_batch(kinfo_M, pi, x):
    R, T = x.shape; v = np.tile(pi, (R, 1)); ll = np.zeros(R)
    for t in range(T):
        o = x[:, t]
        v0 = v @ kinfo_M[0]; v1 = v @ kinfo_M[1]; v = np.where(o[:, None] == 1, v1, v0); z = v.sum(1); ll += np.log(z); v = v/z[:, None]
    return ll
KI = {w: kern(w, W[w]) for w in WORLDS}
def gen(rng, R, T, kinfos): return {w: simulate(kinfos[w], R, T, rng) for w in WORLDS}
def nb_fit(F):
    return {w: (F[w].mean(0), F[w].std(0)+1e-6) for w in WORLDS}
def nb_pred(model, f):
    sc = np.stack([(-0.5*((f-m)/s)**2-np.log(s)).sum(1) for m, s in (model[w] for w in WORLDS)], 1); return sc.argmax(1)
def acc_nb(model, F, true_idx_by_world):
    ok = 0; tot = 0
    for wi, w in enumerate(WORLDS): ok += (nb_pred(model, F[w]) == wi).sum(); tot += len(F[w])
    return ok/tot
def acc_full(Xs, kinfos):
    ok = tot = 0
    for wi, w in enumerate(WORLDS):
        lls = np.stack([loglik_full_batch(kinfos[v][0], kinfos[v][1], Xs[w]) for v in WORLDS], 1)
        ok += (lls.argmax(1) == wi).sum(); tot += len(Xs[w])
    return ok/tot
RC, RT = 600, 600
print("T      DI mean (SH/EC/WK)        AC1 mean (SH/EC/WK)      3-way acc: diag  FULL  | SH-WK acc: DI-only AC1-only diag")
res = {}
for T in (320, 800, 1600, 3200):
    cal = gen(CALR, RC, T, KI); test = gen(TESTR, RT, T, KI)
    Fc = {w: features(cal[w]) for w in WORLDS}; Ft = {w: features(test[w]) for w in WORLDS}
    m2 = nb_fit(Fc)
    d_acc = acc_nb(m2, Ft, None)
    f_acc = acc_full(test, KI)
    def two(feat_idx):
        mdl = {w: (Fc[w][:, feat_idx].mean(0), Fc[w][:, feat_idx].std(0)+1e-6) for w in ('SH', 'WK')}
        ok = tot = 0
        for w in ('SH', 'WK'):
            f = Ft[w][:, feat_idx]
            sc = np.stack([(-0.5*((f-mdl[v][0])/mdl[v][1])**2-np.log(mdl[v][1])).sum(1) for v in ('SH', 'WK')], 1)
            ok += (sc.argmax(1) == (0 if w == 'SH' else 1)).sum(); tot += len(f)
        return ok/tot
    res[T] = (d_acc, f_acc)
    print(f"{T:5d}  " + "/".join(f"{Ft[w][:,0].mean():.2f}" for w in WORLDS) + "          " + "/".join(f"{Ft[w][:,1].mean():+.2f}" for w in WORLDS) + f"          {d_acc:.3f}  {f_acc:.3f}  |  {two([0]):.3f}  {two([1]):.3f}  {two([0,1]):.3f}")
# ---- P5 shifted-world test: EC with c=.35 (same marginal rate .2) at T=800
T = 800
c2 = .35; p02 = .2*(1-c2)
kw_shift = dict(c=c2, p0=p02)
KS = dict(KI); KS['EC'] = kern('EC', kw_shift)
cal = gen(CALR, RC, T, KI); Fc = {w: features(cal[w]) for w in WORLDS}
mA = nb_fit(Fc)
test_shift = gen(SHIFTR, RT, T, KS); Ft = {w: features(test_shift[w]) for w in WORLDS}
print("\nP5 shifted EC (c=.35 instead of .2, same rate) at T=800:")
pred_ec_diag = nb_pred(mA, Ft['EC']); print("  diagnostic (calibrated on original worlds): fraction of shifted-EC trajectories labelled SH / EC / WK =", [round(float((pred_ec_diag == i).mean()), 3) for i in range(3)])
lls = np.stack([loglik_full_batch(KI[v][0], KI[v][1], test_shift['EC']) for v in WORLDS], 1); pf = lls.argmax(1)
print("  FULL likelihood (original three candidates): fraction labelled SH / EC / WK =", [round(float((pf == i).mean()), 3) for i in range(3)])
print("  3-way accuracy with shifted EC in the test set: diagnostic", round(float((acc_nb(mA, {**{w: Ft[w] for w in WORLDS}}, None))), 3),
      " FULL", round(float(acc_full(test_shift, KI)), 3))
print("  features of shifted EC (mean DI, AC1):", Ft['EC'].mean(0).round(3), "vs original EC:", features(gen(TESTR, 200, T, KI)['EC']).mean(0).round(3))

# ---- P6 (added AFTER seeing the first table, BEFORE running this block): why SH looked iid.
# Prediction: within one SH trajectory windows are iid at that trajectory's own rate (DI ~ 1, AC ~ 0), but the per-trajectory rate pbar varies ACROSS trajectories
# with std about sqrt(.032)=.18 at any T. For EC and WK the across-trajectory std of pbar shrinks with T (WK slowly: soil timescale ~52 steps), EC fastest.
# So a SINGLE shadow trajectory is indistinguishable from iid Bernoulli at its own rate; only several trajectories reveal the shared soil.
print("\nP6 across-trajectory std of per-trajectory error rate pbar (600 trajectories per world):")
for T in (320, 800, 1600):
    X = gen(TESTR, 600, T, KI); print(f"  T={T:5d}: " + "  ".join(f"{w} {X[w].mean(1).std():.3f}" for w in WORLDS))
