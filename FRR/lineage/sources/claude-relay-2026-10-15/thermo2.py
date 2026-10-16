"""
THERMODYNAMIC REBUILD. Ring of N states, exact local detailed balance, cycle affinity A.
  rate i->j = exp(-beta*(E_j-E_i)/2 + s_ij*A/(2N)),  s=+1 forward, -1 backward.  Uniformized, leftover = self-loop.
  At A=0 the stationary law is EXACTLY Boltzmann (symmetric proposal, rejections kept as self-loops).
Observer sees only a labeling of states (a partition). True EPR per step is compared with word-statistics
estimators d_n = D_n - D_{n-1}, where D_n = KL( P(visible words of length n) || P(reversed words) ).

PREDICTIONS (written before running):
 T1. A=0: stationarity error ~1e-15 vs Boltzmann; true EPR = 0.
 T2. d_n nondecreasing in n and bounded by the true EPR (data processing). A violation = bug.
 T3. 3-ring, partition {0,1}|{2}: visible law is an alternating renewal process (independent runs) =>
     time-reversible => d_n = 0 for ALL n although true EPR > 0 ("total shadow", not recoverable by history).
 T4. d_2 equals the first-order lumped-chain EPR (flux method) for any partition (identity).
 No prediction made for the other partitions; they are exploratory.
"""
import numpy as np

def ring_chain(N, E, beta, A):
    r = np.zeros((N,N))
    for i in range(N):
        f = (i+1) % N; b = (i-1) % N
        r[i,f] = np.exp(-beta*(E[f]-E[i])/2 + A/(2*N))
        r[i,b] = np.exp(-beta*(E[b]-E[i])/2 - A/(2*N))
    Z = 1.05*r.sum(1).max()
    P = r/Z; P[np.diag_indices(N)] = 1 - P.sum(1)
    return P

def stat(P):
    return np.ones(len(P))/len(P) @ np.linalg.matrix_power(P, 2**14)

def epr(P, pi):
    s = 0.0
    for i in range(len(P)):
        for j in range(len(P)):
            if i != j and P[i,j] > 0 and P[j,i] > 0:
                s += pi[i]*P[i,j]*np.log(pi[i]*P[i,j]/(pi[j]*P[j,i]))
    return s

def lumped_epr(P, pi, lab, m):
    lab = np.array(lab); F = np.zeros((m,m))
    for a in range(m):
        for b in range(m):
            F[a,b] = sum(pi[i]*P[i,j] for i in range(len(P)) for j in range(len(P)) if lab[i]==a and lab[j]==b)
    s = 0.0
    for a in range(m):
        for b in range(m):
            if a != b and F[a,b] > 0 and F[b,a] > 0:
                s += F[a,b]*np.log(F[a,b]/F[b,a])
    return s

def word_D(P, pi, lab, m, nmax):
    lab = np.array(lab); masks = np.stack([(lab==a).astype(float) for a in range(m)])
    vecs = pi[None,:]*masks; D = {1: 0.0}
    for t in range(2, nmax+1):
        nv = vecs @ P
        vecs = (nv[:,None,:]*masks[None,:,:]).reshape(-1, len(pi))
        p = vecs.sum(1); idx = np.arange(m**t)
        rev = sum(((idx // m**q) % m) * m**(t-1-q) for q in range(t))
        pr = p[rev]; ok = p > 0
        D[t] = np.inf if np.any(pr[ok] <= 0) else float((p[ok]*np.log(p[ok]/pr[ok])).sum())
    return D

def report(name, N, E, beta, A, lab, m, nmax, show):
    P = ring_chain(N, E, beta, A); pi = stat(P); sig = epr(P, pi)
    D = word_D(P, pi, lab, m, nmax)
    d = {n: D[n]-D[n-1] for n in range(2, nmax+1)}
    mono = all(d[n+1] >= d[n]-1e-12 for n in range(2, nmax))
    bound = all(d[n] <= sig+1e-12 for n in d)
    print(f"{name:34s} sigma={sig:.5f} lumped1={lumped_epr(P,pi,lab,m):.5f} d_2={d[2]:.5f} | "
          + " ".join(f"n{n}:{d[n]/sig:.3f}" for n in show if n in d) + f" | mono={mono} <=sigma={bound}")

E3 = [0, .6, .2]; E4 = [0, .5, 1.0, .4]; E6 = [0, .5, 1.0, .3, .8, .2]
beta = 1.0
# T1
for N, E in ((3,E3),(4,E4),(6,E6)):
    P = ring_chain(N, E, beta, 0.0); pi = stat(P); b = np.exp(-beta*np.array(E)); b /= b.sum()
    print(f"T1 N={N} A=0: |pi - Boltzmann|max={np.abs(pi-b).max():.2e}  EPR={epr(P,pi):.2e}")
print("\nfraction of true EPR recovered by forward/reversed word statistics (d_n / sigma), A=2")
show = (2,3,4,6,8,10,12,14)
report("3-ring {01}|{2}  (binary)", 3, E3, beta, 2.0, [0,0,1], 2, 14, show)
report("4-ring {01}|{23} (binary)", 4, E4, beta, 2.0, [0,0,1,1], 2, 14, show)
report("6-ring {012}|{345} (binary)", 6, E6, beta, 2.0, [0,0,0,1,1,1], 2, 14, show)
report("6-ring alternating (binary)", 6, E6, beta, 2.0, [0,1,0,1,0,1], 2, 14, show)
report("6-ring {01}|{23}|{45} (ternary)", 6, E6, beta, 2.0, [0,0,1,1,2,2], 3, 9, (2,3,4,5,6,7,8,9))
report("6-ring {0}|{1,2,3,4}|{5} (tern.)", 6, E6, beta, 2.0, [0,1,1,1,1,2], 3, 9, (2,3,4,5,6,7,8,9))
print("\naffinity sweep, 6-ring {012}|{345} binary")
for A in (0.5, 1.0, 2.0, 4.0, 6.0):
    report(f"  A={A}", 6, E6, beta, A, [0,0,0,1,1,1], 2, 14, (2,4,8,14))
print("\naffinity sweep, 6-ring ternary {01}|{23}|{45}")
for A in (0.5, 1.0, 2.0, 4.0, 6.0):
    report(f"  A={A}", 6, E6, beta, A, [0,0,1,1,2,2], 3, 9, (2,4,6,9))
