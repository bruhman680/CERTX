"""Independent recomputation of two Codex corrections to my open-world relay (written fresh, not copied from Codex's checker).
C1: SWAP's pooled OR-flag rate rises from the shared level to the independent level, so corr(item index, A|B) has population value ~.118 at M=400.
C2: my v3 closed guard (IND if phi_hat+2/sqrt(M)<.25) labels the KNOWN DIFF world IND with probability -> 1 as M grows, because noisy DIFF phi = 324/1771 = .1829 < .25.
Predictions (before running): C1 exact OR rates .2775 -> .4071 and corr .1183 at M=400 (+-.002); Monte Carlo mean trend within .01 of that. C2 fraction of DIFF runs called IND: rises monotonically with M, >=.9 by M=1600, and the guard never says DIFF at M=6400 more than 5%."""
import numpy as np
e=.05
# exact noisy rates
def noisy(p): return p*(1-e)+(1-p)*e
# shared: a=b=d(.2). observed flags independent flips.
pa=noisy(.2)
j_shared=(.2*(1-e)**2+.8*e**2)           # both flagged
or_shared=2*pa-j_shared
j_ind=pa*pa; or_ind=2*pa-j_ind
print("OR rate shared %.4f  independent %.4f  (joint shared %.4f ind %.4f)"%(or_shared,or_ind,j_shared,j_ind))
M=400; X=np.arange(M); Y=np.where(X<M//2,or_shared,or_ind)
print("population corr(index, OR) at M=400 for SWAP:",round(float(np.corrcoef(X,Y)[0,1]),5))
rng=np.random.default_rng(20261106)
R=2000; a=rng.random((R,M))<.2; ind=rng.random((R,M))<.2; half=np.arange(M)[None,:]>=M//2; b=np.where(half,ind,a)
fl=lambda x:x^(rng.random(x.shape)<e); A,B=fl(a),fl(b); O=(A|B).astype(float)
Xc=X-X.mean(); r=((O-O.mean(1,keepdims=True))*Xc).sum(1)/np.sqrt(((O-O.mean(1,keepdims=True))**2).sum(1)*(Xc**2).sum())
print("Monte Carlo mean trend feature, SWAP M=400:",round(float(r.mean()),4)," sd",round(float(r.std()),4))
# PARTIAL for contrast
a=rng.random((R,M))<.2; cp=rng.random((R,M))<.5; b=np.where(cp,a,rng.random((R,M))<.2); A,B=fl(a),fl(b); O=(A|B).astype(float)
r2=((O-O.mean(1,keepdims=True))*Xc).sum(1)/np.sqrt(((O-O.mean(1,keepdims=True))**2).sum(1)*(Xc**2).sum()); print("PARTIAL trend feature mean:",round(float(r2.mean()),4))
# C2
print("\nnoisy DIFF phi exact:",324/1771)
def corr(x,y):
    x=x.astype(float);y=y.astype(float);xm=x-x.mean(1,keepdims=True);ym=y-y.mean(1,keepdims=True)
    return (xm*ym).sum(1)/np.sqrt(np.maximum((xm**2).sum(1)*(ym**2).sum(1),1e-9))
print("M     DIFF called IND / DIFF / UNRES_INDDIFF (v3 closed guard, shared-route override ignored since cond.agreement ~.37<.6)")
for M in (100,400,1600,6400):
    R=1000; h=rng.random((R,M))<.5; p=np.where(h,.4,0.); a=rng.random((R,M))<p; b=rng.random((R,M))<p; A,B=fl(a),fl(b)
    ph=corr(A,B); hi=ph+2/np.sqrt(M); lo=ph-2/np.sqrt(M)
    ind=(hi<.25); dif=(lo>0)&(hi>=.25); un=~ind&~dif
    print(f"{M:5d}  {ind.mean():.2f} / {dif.mean():.2f} / {un.mean():.2f}")
