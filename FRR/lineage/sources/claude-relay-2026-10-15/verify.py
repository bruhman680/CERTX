import sys, io, contextlib
sys.path.insert(0, "/tmp/claude-0/-home-claude/ed722431-0b93-5ef2-81ce-e6127e458ac9/scratchpad")
with contextlib.redirect_stdout(io.StringIO()):
    import thermo2 as T
    import wake as W
import numpy as np

print("V1: correct invariants. Claim A: d_n >= 0.  Claim B: D_n <= (n-1)*sigma for every n (data processing).")
print("    My original T2 (d_n nondecreasing AND d_n <= sigma) is checked separately.")
cases = [("3-ring {01}|{2}", 3, T.E3, [0,0,1], 2, 14), ("4-ring binary", 4, T.E4, [0,0,1,1], 2, 14),
         ("6-ring halves", 6, T.E6, [0,0,0,1,1,1], 2, 14), ("6-ring alternating", 6, T.E6, [0,1,0,1,0,1], 2, 14),
         ("6-ring tern 2-2-2", 6, T.E6, [0,0,1,1,2,2], 3, 9), ("6-ring tern 1-4-1", 6, T.E6, [0,1,1,1,1,2], 3, 9)]
for A in (2.0, 6.0):
    for name, N, E, lab, m, nmax in cases:
        P = T.ring_chain(N, E, 1.0, A); pi = T.stat(P); sig = T.epr(P, pi); D = T.word_D(P, pi, lab, m, nmax)
        d = [D[n]-D[n-1] for n in range(2, nmax+1)]
        r = max(D[n]/((n-1)*sig) for n in range(2, nmax+1))
        print(f" A={A} {name:20s} min d_n={min(d):+.1e}  max D_n/((n-1)sigma)={r:.4f}  "
              f"d_n nondecreasing? {all(d[i+1] >= d[i]-1e-12 for i in range(len(d)-1))}  max d_n/sigma={max(d)/sig:.3f}")

print("\nV2: edge decomposition. First-order lumped EPR should equal the dissipation carried by block-boundary edges.")
for name, lab in (("tern 2-2-2", [0,0,1,1,2,2]), ("tern 1-4-1", [0,1,1,1,1,2])):
    P = T.ring_chain(6, T.E6, 1.0, 2.0); pi = T.stat(P); ep = []
    for i in range(6):
        f = (i+1) % 6; J = pi[i]*P[i,f]-pi[f]*P[f,i]
        ep.append((i, f, J*np.log(pi[i]*P[i,f]/(pi[f]*P[f,i]))))
    tot = sum(x[2] for x in ep); bnd = sum(x[2] for x in ep if lab[x[0]] != lab[x[1]])
    print(f" {name}: sum of edge terms={tot:.5f} (direct sigma {T.epr(P,pi):.5f}); boundary-edge share={bnd:.5f}; "
          f"lumped first-order={T.lumped_epr(P,pi,lab,3):.5f}")

print("\nV3: wake, env kept (e0=1). Truncated-window history models M2, M4 vs belief B (millinats), t=0,1,2,4,8")
def reset_cmp(h, e0=1, Tmax=8):
    P = W.joint_chain(h); pi = W.stationary(P)
    stat = W.expand(h, {0: pi[0:2], 1: pi[2:4]}, 11); Pst = lambda w: stat[len(w)-1][w].sum()
    def Qk(k, w):
        j = min(k, len(w)); u = w[-j:]; pu = Pst(u); return np.array([Pst(u+(0,)), Pst(u+(1,))])/pu
    prior = pi[0:2]/pi[0:2].sum(); levB = W.expand(h, {0: prior}, Tmax+1)
    lev = W.expand(h, {0: [1.0 if e == e0 else 0.0 for e in (0,1)]}, Tmax+1); out = {}
    for name in ("M2", "M4", "B"):
        row = []
        for t in (0, 1, 2, 4, 8):
            tot = 0.0
            for w, a in lev[t].items():
                if name == "B":
                    b = levB[t][w]; b = b/b.sum(); Q = sum(b[e]*np.array(W.K[e][w[-1]]) for e in (0,1))
                else:
                    Q = Qk(int(name[1:]), w)
                for e in (0,1):
                    if a[e] > 0: tot += a[e]*W.KL(W.K[e][w[-1]], Q)
            row.append(1e3*tot)
        out[name] = row
    return out
for h in (0.05, 0.2, 0.5, 1.0):
    r = reset_cmp(h)
    print(f" h={h:4.2f}  " + "   ".join(f"{k}: " + " ".join(f"{x:6.1f}" for x in v) for k, v in r.items()))
