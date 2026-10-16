"""
CONWAY'S LIFE on a 4x4 torus: all 2^16 configurations, exact successor map f.
Three candidate meanings of 'node' are measured:
  (1) merge node       : state where trajectories intersect (in-degree >= 2); retrodiction ambiguity.
  (2) recurrent node   : state on a cycle (what trajectories end up in).
  (3) behavioral node  : class of states with identical OBSERVABLE sequence for t steps (partition refinement,
                         the deterministic analogue of grouping histories by identical futures).

PREDICTIONS (written before running):
 P1. Gardens of Eden exist (in-degree 0), sum of in-degrees = 65536, and the fraction with an empty depth-k
     preimage is nondecreasing in k.
 P2. Behavioral class count C_t is nondecreasing in t and stabilizes; constant observable -> 1 class for all t;
     full-state observable -> 65536 for all t; popcount stabilizes far below 65536.
 P3. Popcount is NOT lumpable: first-order macro model has large defect at t=1.
 P4. Sanity: block is a still life; blinker has period 2.
 No prediction on the actual numbers of cycles, basin sizes or class counts.
"""
import numpy as np

n = 4; N = 1 << 16
s = np.arange(N, dtype=np.uint32)
bits = ((s[:, None] >> np.arange(16, dtype=np.uint32)) & 1).astype(np.int8).reshape(N, 4, 4)
nb = sum(np.roll(np.roll(bits, dy, 1), dx, 2) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))
new = ((nb == 3) | ((bits == 1) & (nb == 2))).astype(np.uint32).reshape(N, 16)
succ = (new << np.arange(16, dtype=np.uint32)).sum(1).astype(np.int64)

# ---- sanity (P4)
enc = lambda cells: sum(1 << (r*4+c) for r, c in cells)
block = enc([(1,1),(1,2),(2,1),(2,2)]); blink = enc([(1,0),(1,1),(1,2)])
print("sanity: block fixed:", succ[block] == block, "| blinker period 2:", succ[succ[blink]] == blink and succ[blink] != blink,
      "| empty fixed:", succ[0] == 0)

# ---- (1) merge nodes and retrodiction
cnt = np.ones(N); print("\nPREIMAGE DEPTH k: fraction of states with NO ancestor at depth k | mean log2(#ancestors) over those with some | max #ancestors | sum check")
for k in range(1, 9):
    cnt = np.bincount(succ, weights=cnt, minlength=N)
    z = (cnt == 0).mean(); ml = np.log2(cnt[cnt > 0]).mean(); mx = cnt.max()
    print(f" k={k}: {z:.4f} | {ml:.3f} | {int(mx)} | {int(cnt.sum())}")
indeg = np.bincount(succ, minlength=N)
print(f"in-degree: Garden of Eden (0) {np.mean(indeg==0):.4f}, in-degree>=2 (merge) {np.mean(indeg>=2):.4f}, max {indeg.max()}, sum {indeg.sum()}")

# ---- (2) recurrent structure
g = succ.copy()
for _ in range(17): g = g[g]
R = np.unique(g); cyc = -np.ones(N, dtype=np.int64); lens = []
for r in R:
    if cyc[r] < 0:
        cid = len(lens); x = r; L = 0
        while cyc[x] < 0:
            cyc[x] = cid; x = succ[x]; L += 1
        lens.append(L)
basin = np.bincount(cyc[g], minlength=len(lens))
trans = np.full(N, -1); trans[R] = 0; level = 0
while True:
    m = (trans < 0) & (trans[succ] == level)
    if not m.any(): break
    level += 1; trans[m] = level
print(f"\nrecurrent states: {len(R)} ({len(R)/N:.4f}); cycles: {len(lens)}; cycle lengths: {dict(zip(*np.unique(lens, return_counts=True)))}")
print(f"largest basin share: {basin.max()/N:.4f} (cycle length {lens[int(basin.argmax())]}); max transient: {trans.max()}; mean transient: {trans.mean():.2f}")

# ---- (3) behavioral nodes
def classes_by_horizon(o, T=40):
    c = np.unique(o, return_inverse=True)[1]; out = [int(c.max()+1)]
    for t in range(1, T+1):
        key = o.astype(np.int64)*(c.max()+1) + c[succ]
        c = np.unique(key, return_inverse=True)[1]; out.append(int(c.max()+1))
    return out
flat = bits.reshape(N, 16)
obs = {"constant": np.zeros(N, dtype=np.int64), "popcount (all cells)": flat.sum(1).astype(np.int64),
       "left-window count (cols 0-1)": bits[:, :, 0:2].sum((1, 2)).astype(np.int64), "full state": s.astype(np.int64)}
print("\nBEHAVIORAL NODES: number of classes C_t after t steps of watching, per observable")
print(" observable                    " + " ".join(f"t={t:<3d}" for t in (0, 1, 2, 3, 5, 10, 20, 40)) + "  stable at")
for name, o in obs.items():
    C = classes_by_horizon(o)
    st = next((t for t in range(1, len(C)) if C[t] == C[t-1]), None)
    nondec = all(C[i+1] >= C[i] for i in range(len(C)-1))
    print(f" {name:29s} " + " ".join(f"{C[t]:<5d}" for t in (0, 1, 2, 3, 5, 10, 20, 40)) + f"  t={st}  nondecreasing={nondec}")

# ---- popcount lumpability defect (user's test, deterministic micro-dynamics)
o = obs["popcount (all cells)"]; m = 17
Pm = np.zeros((m, m)); fib = np.bincount(o, minlength=m)
np.add.at(Pm, (o, o[succ]), 1.0); Pm /= fib[:, None]
f_t = np.arange(N); print("\npopcount macro-model (fibre-averaged), defect = 1 - predicted prob of actual macro outcome")
for t in (1, 2, 3):
    f_t = succ[f_t]; pred = np.linalg.matrix_power(Pm, t)[o, o[f_t]]; d = 1 - pred
    print(f" t={t}: average defect {d.mean():.4f}, worst {d.max():.4f}")
