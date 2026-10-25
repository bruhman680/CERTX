"""
TEST OF THE GEMINI 'PAM' SUMMARY CLAIMS on constructed data.  numpy only.  Independent RNG stream per role (SeedSequence spawn).
Score S = R/2 + R^2 c/2 on complex vectors (computed DIRECTLY from the published expression, not from the identity).

CLAIMS UNDER TEST (Gemini): (A) phase score fixes negation blindness; (B) unit-normalisation deletes useful magnitude information
(S restores it); (C) 'posture' = tunable resonance bandwidth, needs phase; (D) agent wave packets interfere without packaging;
(E) time as phase progression lets the DB query event sequences.

PREDICTIONS (written before running):
 A1  amplitude-only cosine ties +/- records exactly -> top-1 = 50%.   A2 realified cosine, S(complex) and S(real control) have
     IDENTICAL rankings at every phase-noise level (equal norms) -> identical accuracy; A3 S has no gap over info-matched cosine.
 A4  evidence retrieval (query wants records that support OR contradict a claim): S ranks the contradicting record LAST of 2K
     (S=0 < unrelated), so recall@2 = 0.5; amplitude cosine and |c| give recall@2 = 1.
 B   M1 (norm = strength that should MATCH the query): S ~100%, cosine ~chance, control (cos + explicit norm feature) ~100%.
     M2 (norm = arbitrary artifact): cosine ~100%, S < cosine.  M3 (norm = confidence, higher is better): raw dot product best,
     S not best; control with an explicit confidence feature matches the best.  No numeric prediction for S in M2/M3.
 C   For equal norms softmax(S/T_S) == softmax(c/T_c) with T_S=T_c/2 and threshold t on S == threshold 2t-1 on c (to 1e-12);
     for unequal norms they differ.  The score has no bandwidth parameter, so 'bandwidth' is not testable as stated.
 D   Under a summed packet, the zero aggregate has a fibre containing 'nobody spoke' and many disputes.
 E1  S(z_t1, z_t2) is symmetric in the time difference: before/after are indistinguishable for a single event pair.
 E2  sequences that bind different topics to different times ARE distinguishable (S<1 for swapped order).
 NOT tested: real text, real encoders, any product kernel.
"""
import numpy as np, itertools
ss = np.random.SeedSequence(20261024); R_ = [np.random.default_rng(s) for s in ss.spawn(10)]
ENC, NOISE, QRY, CAL, AGG, TIE = R_[0], R_[1], R_[2], R_[3], R_[4], R_[5]

def S(z, w):                                    # published expression, direct
    ez, ew = np.sum(abs(z)**2, -1), np.sum(abs(w)**2, -1)
    R = 2*np.sqrt(ez*ew)/(ez+ew); return 0.5*np.sum(abs(z+w)**2, -1)/(ez+ew)*R
def real(z): return np.concatenate([z.real, z.imag], -1)
def cosr(z, w):
    u, v = real(z), real(w); return np.sum(u*v, -1)/np.sqrt(np.sum(u*u, -1)*np.sum(v*v, -1))
def cosamp(z, w):
    a, b = abs(z), abs(w); return np.sum(a*b, -1)/np.sqrt(np.sum(a*a, -1)*np.sum(b*b, -1))
def S_ctrl(z, w):                                # information-matched real control: realified coords + R from norms
    u, v = real(z), real(w); eu, ev = np.sum(u*u, -1), np.sum(v*v, -1); c = np.sum(u*v, -1)/np.sqrt(eu*ev)
    R = 2*np.sqrt(eu*ev)/(eu+ev); return R/2 + R*R*c/2

def top1_expected(scores, target_idx, tol=1e-12):
    m = scores.max(); tied = np.where(scores >= m - tol)[0]
    return (1.0/len(tied)) if target_idx in tied else 0.0
def recallk_expected(scores, targets, k, tol=1e-12):
    order = np.argsort(-scores, kind='stable'); thr = scores[order[k-1]]
    above = np.where(scores > thr + tol)[0]; tie = np.where(abs(scores-thr) <= tol)[0]
    need = k - len(above); hit = len(set(targets) & set(above))
    hit += (len(set(targets) & set(tie))/len(tie))*need if len(tie) else 0
    return hit/len(targets)

# ------------------------------------------------------------------ A: negation, evidence retrieval
K, d = 200, 32
A0 = np.abs(ENC.normal(size=(K, d))) + 0.1
def runA(equalize):
    A_ = A0/np.sqrt(np.sum(A0**2, 1, keepdims=True)) if equalize else A0
    print(f"A [{'ENERGY-EQUALIZED topics' if equalize else 'topic energies VARY (the first-run design: relevant record has exactly the query energy)'}]: K={K}, d={d}; "
          "records +topic (phase 0) and -topic (phase pi); phase noise sigma on both; top-1 for agreement query, expected over exact ties")
    print("   sigma   ampCos   realCos   S(cplx)   S(real ctrl)   max|S-(1+c)/2| over all candidates")
    for sig in (0.0, 0.5, 1.0, 1.5):
        ph = NOISE.normal(scale=sig, size=(2, K, d))
        pos = A_*np.exp(1j*ph[0]); neg = A_*np.exp(1j*(np.pi+ph[1])); recs = np.concatenate([pos, neg])
        acc = {m: 0.0 for m in ("ampCos", "realCos", "S", "Sctrl")}; gap = 0.0
        for k in range(K):
            q = A_[k].astype(complex)
            sc = {"ampCos": cosamp(q[None], recs), "realCos": cosr(q[None], recs), "S": S(q[None], recs), "Sctrl": S_ctrl(q[None], recs)}
            for m in acc: acc[m] += top1_expected(sc[m], k)/K
            gap = max(gap, np.max(abs(sc["S"] - (1+sc["realCos"])/2)))
        print(f"   {sig:4.1f}   {acc['ampCos']:.3f}    {acc['realCos']:.3f}     {acc['S']:.3f}     {acc['Sctrl']:.3f}          {gap:.2e}")
    return A_
runA(False); A_ = runA(True)
print("   A4  evidence retrieval (energy-equalized): relevant = BOTH records of the query topic (support + contradict)")
recs = np.concatenate([A_.astype(complex), -A_.astype(complex)])
for name, fn in (("ampCos", cosamp), ("realCos", cosr), ("S", S), ("|realCos|", lambda a, b: abs(cosr(a, b)))):
    r2 = np.mean([recallk_expected(fn(A_[k].astype(complex)[None], recs), [k, K+k], 2) for k in range(K)])
    sc = fn(A_[0].astype(complex)[None], recs); rank_neg = int(np.sum(sc > sc[K] + 1e-12)) + 1
    print(f"      {name:10s} recall@2={r2:.3f}   rank of the contradicting record (query 0) among {2*K}: {rank_neg}")

# ------------------------------------------------------------------ B: magnitude regimes (rebuilt: noisy queries, no self-match)
print("\nB (rebuilt): 60 topics, noisy queries (cos to topic ~.82), strengths {.25,.5,1,2,4}; 200 test queries; lambda chosen on separate calibration queries.")
Kt, STR, dc = 60, np.array([0.25, 0.5, 1.0, 2.0, 4.0]), 16
TT = ENC.normal(size=(Kt, dc)) + 1j*ENC.normal(size=(Kt, dc)); TT /= np.linalg.norm(TT, axis=1, keepdims=True)
def make_pool(regime, rng):
    if regime == "M2":
        sk = STR[rng.integers(5, size=Kt)]; return TT*sk[:, None], np.arange(Kt), sk
    return (TT[:, None, :]*STR[None, :, None]).reshape(-1, dc), np.repeat(np.arange(Kt), 5), np.tile(STR, Kt)
def evaluate(regime, seed, lam_pen, lam_conf, n):
    rng = np.random.default_rng(seed); pool, tp, st = make_pool(regime, np.random.default_rng(777))
    out = {m: 0.0 for m in ("cosine", "S", "dot", "cos+normfeat", "cos+conf")}
    for _ in range(n):
        k = rng.integers(Kt); nz = rng.normal(size=dc)+1j*rng.normal(size=dc); nz = 0.7*nz/np.linalg.norm(nz)
        sq = STR[rng.integers(5)] if regime in ("M1", "M2") else 1.0
        q = (TT[k]+nz); q = q/np.linalg.norm(q)*sq
        cos = cosr(q[None], pool); nr = np.linalg.norm(pool, axis=1)
        sc = {"cosine": cos, "S": S(q[None], pool), "dot": real(pool)@real(q[None])[0],
              "cos+normfeat": cos - lam_pen*np.abs(np.log(nr/np.linalg.norm(q))), "cos+conf": cos + lam_conf*np.log(nr)}
        if regime == "M1": tgt = np.where((tp == k) & np.isclose(st, sq))[0]
        elif regime == "M2": tgt = np.where(tp == k)[0]
        else: tgt = np.where((tp == k) & (st == 4.0))[0]
        for m, v in sc.items():
            top = np.where(v >= v.max() - 1e-9)[0]; out[m] += (len(set(top) & set(tgt))/len(top))/n
    return out
GRID = (0, .01, .02, .05, .1, .2, .5, 1.0)
print("   regime                               | cosine    S      dot   cos+normfeat(lam)  cos+conf(lam)")
for regime, desc in (("M1", "norm = strength to MATCH query"), ("M2", "norm = arbitrary artifact"), ("M3", "norm = confidence (higher better)")):
    cal_seed = int(CAL.integers(1 << 30))
    pen = GRID[int(np.argmax([evaluate(regime, cal_seed, l, 0, 150)["cos+normfeat"] for l in GRID]))]
    conf = GRID[int(np.argmax([evaluate(regime, cal_seed, 0, l, 150)["cos+conf"] for l in GRID]))]
    r = evaluate(regime, int(QRY.integers(1 << 30)), pen, conf, 200)
    print(f"   {regime} {desc:34s}| {r['cosine']:.3f}  {r['S']:.3f}  {r['dot']:.3f}   {r['cos+normfeat']:.3f}({pen})        {r['cos+conf']:.3f}({conf})")

# ------------------------------------------------------------------ C: posture
print("\nC: posture. Equal-norm candidates: softmax(S/T_S) vs softmax(cos/T_c), T_S = T_c/2; thresholds t vs 2t-1.")
zq = ENC.normal(size=16)+1j*ENC.normal(size=16)
def softmax(x): e = np.exp(x-x.max()); return e/e.sum()
cands_eq = [ (lambda v: v/np.linalg.norm(v)*np.linalg.norm(zq))(ENC.normal(size=16)+1j*ENC.normal(size=16)) for _ in range(300)]
cands_un = [c*np.exp(NOISE.normal(scale=1.0)) for c in cands_eq]
for name, cands in (("equal norms", cands_eq), ("unequal norms", cands_un)):
    C_ = np.array(cands); cs = cosr(zq[None], C_); Ss = S(zq[None], C_); worst = 0.0
    for Tc in (0.05, 0.1, 0.3, 1.0):
        worst = max(worst, np.max(abs(softmax(Ss/(Tc/2)) - softmax(cs/Tc))))
    thr_same = all(set(np.where(Ss >= t)[0]) == set(np.where(cs >= 2*t-1)[0]) for t in (0.2, 0.5, 0.7, 0.9))
    print(f"   {name:14s}: max |softmax difference| = {worst:.2e}; threshold sets identical for t in (.2,.5,.7,.9): {thr_same}")

# ------------------------------------------------------------------ D: summed packets
print("\nD: n agents each emit +z, -z or nothing about the same topic; the DB stores only the sum.")
for n in (2, 4, 6):
    from collections import Counter
    cnt = Counter(); disp = Counter()
    for h in itertools.product((-1, 0, 1), repeat=n):
        m = sum(h); cnt[m] += 1; disp[m] += (1 in h and -1 in h)
    print(f"   n={n}: histories with aggregate 0: {cnt[0]} of {3**n}; all-silent: 1; with a +/- dispute: {disp[0]}; "
          f"fraction of zero-aggregate histories containing a dispute: {disp[0]/cnt[0]:.3f}")

# ------------------------------------------------------------------ E: time as phase
print("\nE: time as phase, z_t = A * exp(i*(phi0 + omega*t)) per coordinate (omega_k random).")
om = np.abs(ENC.normal(size=24))+0.2; A24 = np.abs(ENC.normal(size=24))+0.3; ph0 = ENC.uniform(0, 2*np.pi, 24)
ev = lambda t: A24*np.exp(1j*(ph0+om*t))
t0, dt = 3.0, 1.7
print(f"   E1 single event pair: S(z_t0, z_t0+dt) = {S(ev(t0)[None], ev(t0+dt)[None])[0]:.12f};  S(z_t0+dt, z_t0) = {S(ev(t0+dt)[None], ev(t0)[None])[0]:.12f};"
      f"  S(z_t0, z_t0-dt) = {S(ev(t0)[None], ev(t0-dt)[None])[0]:.12f}")
B1 = np.abs(ENC.normal(size=24))+0.3; B2 = np.abs(ENC.normal(size=24))+0.3          # two different topics bound to different coordinates? use disjoint halves
mask1 = np.r_[np.ones(12), np.zeros(12)]; mask2 = 1-mask1
evA = lambda t: A24*mask1*np.exp(1j*(ph0+om*t)); evB = lambda t: A24*mask2*np.exp(1j*(ph0+om*t))
seq1 = evA(t0)+evB(t0+dt); seq2 = evA(t0+dt)+evB(t0); seq1b = evA(t0+5)+evB(t0+5+dt)
print(f"   E2 two-topic sequences: S(seq1,seq1)={S(seq1[None],seq1[None])[0]:.6f}; S(seq1, swapped order)={S(seq1[None],seq2[None])[0]:.6f}; "
      f"S(seq1, same order shifted by +5)={S(seq1[None],seq1b[None])[0]:.6f}")
