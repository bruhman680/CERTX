"""
SCOPED-NEGATION FIXTURE (hand-built compositional encoder; NOT a learned model).  numpy only; independent RNG stream per role.
Statements about valve v at time t in {now, yesterday} with status in {A: 'v open at t', N: 'v NOT open at t', U: 'not established that v open at t'}.
30 valves x 2 times x 3 statuses = 180 records.  Every vector is unit norm, so candidate energies are equal (R constant) -> S ranks like cosine; checked.
Vector = wb*b_(v,t) + wc*(e_v + e_open + e_t)/sqrt(3), wb=.8, wc=.6.  b = claim-specific binding (unique per valve,time); e_v shared across times, e_t shared across valves.
Encoders:
 E0 blind   : N and U get only a weak extra token (eps=.2); no polarity in phase (the 'embedding that barely sees negation' caricature).
 E1 global  : whole sentence vector gets phase: A 0, N pi, U pi/2.        (naive 'flip the sentence')
 E2 scoped  : only the claim binding b gets the phase (A: +b, N: -b, U: i*b); shared context stays phase 0.
Scorers on the same vectors: cosR (cosine on real+imag coordinates), S (published expression, direct), |cosR|.
Metadata baseline META: relevance = cosine of unsigned content vectors (no phase, no negation token) + explicit status label filter.
Query = the encoded claim plus additive complex noise of norm eta (paraphrase noise).  Tasks per valve, 20 noise draws each:
 T1 agreement  : query A(v,now);  success = top-1 is A(v,now).
 T2 evidence   : query A(v,now);  relevant = {A,N,U}(v,now) (all statuses about the claim and its time);  recall@3 and precision@3.
                 yesterday statements are NOT evidence for a claim about now (scope).
 T4 status     : query N(v,now);  success = top-1 is N(v,now) (not U, not A).

PREDICTIONS (written before running; eta=.5 unless stated):
 P1  S and cosR give identical top-3 sets for every query/encoder (equal norms).
 P2  T1 and T4: E0 about 1/3 (A,N,U nearly tied); E1 and E2 near 1.0; META near 1.0.
 P3  T2 (cosR): E0 recall@3 ~1.0 (blindness helps evidence retrieval); E1 about 1/3-2/3 (contradiction ranked last, U at 0);
     E2 about 2/3 (N below distractors at c = -.28).
 P4  T2 with |cosR|: E1 gets N back (|c|=1) but U stays at 0 -> recall ~2/3; E2 borderline for N (|c|=.28 vs .24 distractors) and noise-sensitive.
 P5  No single scorer x encoder pair is at ~1.0 on T1, T2 and T4 together; META is.
 Not tested: learned encoders; real language; quantifiers; anything about a product.
"""
import numpy as np
ss = np.random.SeedSequence(20261026); G = [np.random.default_rng(s) for s in ss.spawn(6)]
BIND, CTX, NZ = G[0], G[1], G[2]
D, NV, WB, WC = 128, 30, 0.8, 0.6
unit = lambda v: v/np.linalg.norm(v)
b = {(v, t): unit(BIND.normal(size=D)) for v in range(NV) for t in (0, 1)}      # t: 0=now, 1=yesterday
ev = [unit(CTX.normal(size=D)) for _ in range(NV)]; et = [unit(CTX.normal(size=D)) for _ in (0, 1)]; eo = unit(CTX.normal(size=D))
etok = {"N": unit(CTX.normal(size=D)), "U": unit(CTX.normal(size=D))}
ctx = lambda v, t: WC*(ev[v] + eo + et[t])/np.sqrt(3)
STATUS = ("A", "N", "U"); EPS = 0.2
def enc(kind, v, t, s):
    cx, bb = ctx(v, t), WB*b[(v, t)]
    if kind == "E0":
        x = cx + bb + (EPS*etok[s] if s in ("N", "U") else 0); return unit(x).astype(complex)
    ph = {"A": 1, "N": -1, "U": 1j}[s]
    if kind == "E1": return (ph*(cx + bb)).astype(complex)
    if kind == "E2": return (cx + ph*bb).astype(complex)
    if kind == "content": return (cx + bb).astype(complex)               # unsigned content for META
keys = [(v, t, s) for v in range(NV) for t in (0, 1) for s in STATUS]; idx = {k: i for i, k in enumerate(keys)}
def real(z): return np.concatenate([z.real, z.imag], -1)
def cosR(z, W):
    u, V = real(z), real(W); return V@u/(np.linalg.norm(V, axis=1)*np.linalg.norm(u))
def Sx(z, W):
    ez, ew = np.sum(abs(z)**2), np.sum(abs(W)**2, 1); R = 2*np.sqrt(ez*ew)/(ez+ew)
    return 0.5*np.sum(abs(z[None]+W)**2, 1)/(ez+ew)*R
absC = lambda z, W: abs(cosR(z, W))
SC = {"cosR": cosR, "S": Sx, "|cosR|": absC}
def topk(sc, k): return set(np.argsort(-sc, kind='stable')[:k])
def top1_tied(sc, target, tol=1e-9):
    m = sc.max(); tied = np.where(sc >= m-tol)[0]; return (1/len(tied)) if target in tied else 0.0

def run(eta, nd=20):
    res = {}; same_top3 = True
    for kind in ("E0", "E1", "E2"):
        W = np.array([enc(kind, *k) for k in keys])
        for name in SC: res[(kind, name)] = np.zeros(4)                    # T1, T4, T2 recall@3, T2 precision@3
        for v in range(NV):
            for _ in range(nd):
                n = NZ.normal(size=D)+1j*NZ.normal(size=D); n = eta*n/np.linalg.norm(n)
                qA = enc(kind, v, 0, "A") + n; qN = enc(kind, v, 0, "N") + n
                rel = {idx[(v, 0, s)] for s in STATUS}
                for name, f in SC.items():
                    sA, sN = f(qA, W), f(qN, W)
                    t3 = topk(sA, 3)
                    res[(kind, name)] += np.array([top1_tied(sA, idx[(v, 0, "A")]), top1_tied(sN, idx[(v, 0, "N")]),
                                                   len(t3 & rel)/3, len(t3 & rel)/3])/(NV*nd)
                    # recall@3 == precision@3 here because |relevant| = 3 = k; keep both columns for clarity
                same_top3 &= topk(cosR(qA, W), 3) == topk(Sx(qA, W), 3)
    # META baseline
    Wc = np.array([enc("content", *k) for k in keys]); st = np.array([k[2] for k in keys])
    meta = np.zeros(4)
    for v in range(NV):
        for _ in range(nd):
            n = NZ.normal(size=D)+1j*NZ.normal(size=D); n = eta*n/np.linalg.norm(n); q = enc("content", v, 0, "A") + n
            sc = cosR(q, Wc)
            sA = np.where(st == "A", sc, -9); sN = np.where(st == "N", sc, -9); t3 = topk(sc, 3); rel = {idx[(v, 0, s)] for s in STATUS}
            meta += np.array([float(np.argmax(sA) == idx[(v, 0, "A")]), float(np.argmax(sN) == idx[(v, 0, "N")]), len(t3 & rel)/3, len(t3 & rel)/3])/(NV*nd)
    return res, meta, same_top3
for eta in (0.5, 1.0):
    res, meta, same = run(eta)
    print(f"\neta = {eta}  (query noise norm; unit-norm claim vectors)   P1 S vs cosR identical top-3 sets everywhere: {same}")
    print("  encoder  scorer     T1 agree top-1   T4 status top-1   T2 evidence recall@3 (=precision@3)")
    for (kind, name), r in res.items():
        print(f"  {kind:7s}  {name:8s}   {r[0]:6.3f}           {r[1]:6.3f}            {r[2]:6.3f}")
    print(f"  META (content cosine + explicit status label)   {meta[0]:6.3f}           {meta[1]:6.3f}            {meta[2]:6.3f}")

# what the pairwise geometry looks like (noise-free), for reading the table
print("\nnoise-free similarity of the query A(v=0,now) to records about the same valve (cosR):")
for kind in ("E0", "E1", "E2"):
    q = enc(kind, 0, 0, "A"); row = {}
    for t, tn in ((0, "now"), (1, "yest")):
        for s in STATUS: row[f"{s}-{tn}"] = cosR(q, enc(kind, 0, t, s)[None])[0]
    other = np.mean([cosR(q, enc(kind, v, 0, "A")[None])[0] for v in range(1, NV)])
    print(f"  {kind}: " + "  ".join(f"{k}={x:+.2f}" for k, x in row.items()) + f"   | A-now of other valves (mean) = {other:+.2f}")
