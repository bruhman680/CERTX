"""
SCOPED-NEGATION v2 (hand-built compositional encoder; NOT a learned model; phase is oracle-supplied). numpy only.
Fixes from v1 (see v1 output): (a) every record AND query is renormalized to EXACT unit norm, so R=1 and S==(1+c)/2 holds to float precision;
(b) E0 now gives A, N, U records a symmetric small stance token (eps), so no status gets an 'absent token' identity advantage;
(c) noise swept over eta in {.5,1,2,4} (v1 hid the blind encoder's tiny margin behind low noise); (d) added modulus scorer and stance readout.
Records: valve v (30), time t in {now, yest}, status s in {A: 'open', N: 'NOT open', U: 'not established open'} -> 180 records.
x(v,t) = ctx + wb*b_(v,t); ctx = wc*(e_v+e_open+e_t)/sqrt3; wb=.8, wc=.6. Encoders (then unit-normalized):
 E0: x + eps*tok_s (real; tok random per status; N and U are NOT opposite).   E1: phase*x (global flip).   E2: ctx + phase*wb*b (scoped flip). phase: A 1, N -1, U i.
Query for status s_q at (v,now) = same encoder applied to that claim, plus complex noise of norm eta, renormalized.  (T1: s_q=A, T4: s_q=N, T2/T3: s_q=A.)
Scorers: cosR (cosine on real+imag coords), S (published expression computed directly), mod = |<q,w>| (complex inner-product modulus, phase-blind).
Tasks: T1 top-1 is A(v,now). T4 (query N) top-1 is N(v,now). T2 evidence: top-3 == {A,N,U}(v,now) (recall@3; yest records are out of scope).
 T3 stance readout for the 3 relevant records of a query-A: classify by the angle of <q,w> to nearest calibration centre (centres from a separate CAL set of valves).
META: unsigned content cosine (ctx+b, no phase, no token) with an explicit status label filter for T1/T4; T2 = top-3 by content cosine.
'Two-channel' = T2 by mod, T1/T4 by cosR, T3 by angle.

PREDICTIONS (written before running):
 P1 S and cosR give identical top-1 and top-3 sets (allow float-tie flips: report count); S top-3 == cosR top-3 in >99.9% of queries.
 P2 E0 (eps=.2): noise-free margin of the true status over the others ~ eps^2/(1+eps^2)=.038 -> T1,T4 ~1.0 at eta=.5, falling toward chance (1/3) by eta=4.
    E1: T1,T4 ~1.0 at all eta (margin 1 or 2 vs noise). E2: T1,T4 ~1.0 at eta<=2, a bit lower at eta=4 (margin ~.6).
 P3 T2 cosR: E0 ~1.0 for eta<=2 (blind to status; relevance is topical). E1 =.333 (A, then two distractors; N=-1, U=0). E2 ~.4.
 P4 T2 mod: E0 ~ same as cosR (real vectors: mod==|cos|... for E0 positive) ~1.0; E1 ~1.0 (all statuses on one complex line); E2 ~.7 (N modulus .28 vs distractors ~.24).
 P5 T3: E1 ~1.0, E2 ~1.0 at low noise, E0 ~chance (no phase information).
 P6 Two-channel under E1 reaches ~1.0 on T1,T2,T3,T4 at eta<=2; META also ~1.0. No single-scorer x encoder is ~1.0 on T1,T2,T4 together except E0 at low noise (and that one fails T3).
 Not tested: learned encoders; real language; quantifiers; whether an encoder can learn the E1/E2 contracts; anything about a product.
"""
import numpy as np
ss = np.random.SeedSequence(20261027); G = [np.random.default_rng(s) for s in ss.spawn(6)]
BIND, CTX, NZ, CAL = G[0], G[1], G[2], G[3]
D, NV, NCAL, WB, WC = 128, 30, 20, 0.8, 0.6
unit = lambda v: v/np.linalg.norm(v)
nb = NV+NCAL                                   # valves 0..29 evaluation, 30..49 calibration
b = {(v, t): unit(BIND.normal(size=D)) for v in range(nb) for t in (0, 1)}
ev = [unit(CTX.normal(size=D)) for _ in range(nb)]; et = [unit(CTX.normal(size=D)) for _ in (0, 1)]; eo = unit(CTX.normal(size=D))
tok = {s: unit(CTX.normal(size=D)) for s in "ANU"}
ctx = lambda v, t: WC*(ev[v]+eo+et[t])/np.sqrt(3)
PH = {"A": 1, "N": -1, "U": 1j}
def enc(kind, v, t, s, eps):
    cx, bb = ctx(v, t), WB*b[(v, t)]
    if kind == "E0": x = cx+bb+eps*tok[s]
    elif kind == "E1": x = PH[s]*(cx+bb)
    elif kind == "E2": x = cx+PH[s]*bb
    else: x = cx+bb                              # content (META)
    return unit(np.asarray(x, dtype=complex))
STAT = "ANU"
keys = [(v, t, s) for v in range(nb) for t in (0, 1) for s in STAT]; idx = {k: i for i, k in enumerate(keys)}
ev_idx = np.array([i for i, k in enumerate(keys) if k[0] < NV])              # evaluation pool = valves 0..29 only
def real(z): return np.concatenate([z.real, z.imag], -1)
def cosR(q, W): u, V = real(q), real(W); return V@u/(np.linalg.norm(V, axis=1)*np.linalg.norm(u))
def Sx(q, W):
    eq, ew = np.sum(abs(q)**2), np.sum(abs(W)**2, 1); R = 2*np.sqrt(eq*ew)/(eq+ew)
    return 0.5*np.sum(abs(q[None]+W)**2, 1)/(eq+ew)*R
def mod(q, W): return abs(W@np.conj(q))/(np.linalg.norm(W, axis=1)*np.linalg.norm(q))
def noisy(q, eta):
    n = NZ.normal(size=D)+1j*NZ.normal(size=D); return unit(q+eta*unit(n))
def top1(sc, pool, target):
    s = sc[pool]; m = s.max(); tied = np.where(s >= m-1e-9)[0]; return (1/len(tied)) if pool[tied].tolist().count(target) else 0.0
def top3(sc, pool): return set(pool[np.argsort(-sc[pool], kind='stable')[:3]].tolist())

def run(eta, eps, nd=20):
    out = {}; s_mismatch = 0; s_n = 0
    for kind in ("E0", "E1", "E2"):
        W = np.array([enc(kind, *k, eps) for k in keys])
        # calibration centres for stance angles: query A, relevant records of CAL valves, no noise-free shortcut: use noisy queries
        ang = {s: [] for s in STAT}
        for v in range(NV, nb):
            for _ in range(5):
                q = noisy(enc(kind, v, 0, "A", eps), eta)
                for s in STAT: ang[s].append(np.angle(W[idx[(v, 0, s)]] @ np.conj(q)))
        cen = {s: np.angle(np.mean(np.exp(1j*np.array(ang[s])))) for s in STAT}
        res = np.zeros(5)                      # T1, T4, T2 cosR, T2 mod, T3
        for v in range(NV):
            rel = {idx[(v, 0, s)] for s in STAT}
            for _ in range(nd):
                qA = noisy(enc(kind, v, 0, "A", eps), eta); qN = noisy(enc(kind, v, 0, "N", eps), eta)
                scA, scN = cosR(qA, W), cosR(qN, W)
                s_mismatch += top3(scA, ev_idx) != top3(Sx(qA, W), ev_idx); s_n += 1
                cnt = 0.0
                for s in STAT:
                    a = np.angle(W[idx[(v, 0, s)]] @ np.conj(qA))
                    pred = min(STAT, key=lambda z: abs(np.angle(np.exp(1j*(a-cen[z])))))
                    cnt += (pred == s)/3
                res += np.array([top1(scA, ev_idx, idx[(v, 0, "A")]), top1(scN, ev_idx, idx[(v, 0, "N")]),
                                 len(top3(scA, ev_idx) & rel)/3, len(top3(mod(qA, W), ev_idx) & rel)/3, cnt])/(NV*nd)
        out[kind] = res
    Wc = np.array([enc("content", *k, eps) for k in keys]); st = np.array([k[2] for k in keys]); meta = np.zeros(3)
    for v in range(NV):
        rel = {idx[(v, 0, s)] for s in STAT}
        for _ in range(nd):
            q = noisy(enc("content", v, 0, "A", eps), eta); sc = cosR(q, Wc)
            pA = ev_idx[st[ev_idx] == "A"]; pN = ev_idx[st[ev_idx] == "N"]
            meta += np.array([top1(sc, pA, idx[(v, 0, "A")]), top1(sc, pN, idx[(v, 0, "N")]), len(top3(sc, ev_idx) & rel)/3])/(NV*nd)
    return out, meta, s_mismatch, s_n

for eps in (0.2, 0.5):
    print(f"\n===== eps (stance-token weight in E0) = {eps} =====")
    for eta in (0.5, 1.0, 2.0, 4.0):
        out, meta, mm, n = run(eta, eps)
        print(f"\neta={eta}   P1: S vs cosR top-3 set mismatches {mm}/{n}")
        print("  enc   T1 agree@1  T4 status@1  T2 evid cosR  T2 evid mod  T3 stance")
        for k, r in out.items(): print(f"  {k}   {r[0]:6.3f}      {r[1]:6.3f}       {r[2]:6.3f}        {r[3]:6.3f}      {r[4]:6.3f}")
        print(f"  META  {meta[0]:6.3f}      {meta[1]:6.3f}       {meta[2]:6.3f}        (label filter)")
print("\nnoise-free cosR / mod of query A(v=0,now) vs same-valve records (E0 eps=.2, E1, E2):")
for kind in ("E0", "E1", "E2"):
    q = enc(kind, 0, 0, "A", .2); W = {(t, s): enc(kind, 0, t, s, .2) for t in (0, 1) for s in STAT}
    print(f"  {kind}: " + "  ".join(f"{s}{'now' if t==0 else 'yst'}={cosR(q, W[(t,s)][None])[0]:+.2f}/{mod(q, W[(t,s)][None])[0]:.2f}" for t in (0, 1) for s in STAT))
