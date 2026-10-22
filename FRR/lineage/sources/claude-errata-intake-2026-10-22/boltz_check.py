import numpy as np
N = 8
dec = lambda i: (i//2, i%2)
E = np.array([0.5*dec(i)[0] + 0.3*dec(i)[1] for i in range(N)])

def rates(beta):
    k = np.zeros((N,N))
    for i in range(N):
        xi, ei = dec(i)
        for j in range(N):
            xj, ej = dec(j)
            if i != j and abs(xi-xj) + abs(ei-ej) == 1:
                k[i,j] = np.exp(-beta*max(E[j]-E[i], 0))
    return k

def stat(P): return np.ones(N)/N @ np.linalg.matrix_power(P, 2**14)

print("beta   old-chain error   predicted pi ~ e^{-bE}(S_i+1) error   fixed-chain error")
for beta in (0.5, 1.0, 2.0, 5.0):
    k = rates(beta); S = k.sum(1); boltz = np.exp(-beta*E); boltz /= boltz.sum()
    # old construction: each row divided by (its own exit rate + 1)
    P_old = k/(S+1)[:,None]; P_old[np.diag_indices(N)] = 1/(S+1)
    pi_old = stat(P_old)
    pred = boltz*(S+1); pred /= pred.sum()
    # fix: one common normalizer, rejections become self-loops
    Z = 1.05*S.max(); P_fix = k/Z; P_fix[np.diag_indices(N)] = 1 - P_fix.sum(1)
    pi_fix = stat(P_fix)
    print(f"{beta:4.1f}   {np.abs(pi_old-boltz).max():.5f}           {np.abs(pi_old-pred).max():.2e}                         {np.abs(pi_fix-boltz).max():.2e}")
print("\nexit-rate sums S_i at beta=2 (differ by state):", np.round(rates(2.0).sum(1), 3))
