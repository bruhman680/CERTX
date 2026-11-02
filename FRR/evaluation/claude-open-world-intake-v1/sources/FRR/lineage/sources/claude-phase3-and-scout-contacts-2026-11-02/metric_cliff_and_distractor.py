"""
TWO SMALL CONTACTS from the arXiv scout (Claude, 2026-11-02). Self-contained besides executing the world generators in open_world_guard.py.
(A) METRIC CLIFF (after Schaeffer et al. 2304.15004): is the sharp rise of the open-set recognizer's UNKNOWN rate with M a feature of the world or of the hard threshold? Compare the hard metric (fraction flagged UNKNOWN) with a continuous one (median of the minimum distance to any known class, in z^2 units) for ANTI, DRIFT, PARTIAL over M = 50..3200, known classes IND/DIFF/SHARED only.
  A1 median min-distance grows smoothly: log-log slope vs M in [0.8,1.2] over M>=200 for ANTI and PARTIAL (z^2 scales with M for a fixed mean shift).
  A2 the hard metric looks like a cliff: for ANTI the UNKNOWN fraction goes from <=.20 to >=.80 within a factor of 4 in M.
  A3 the two metrics rank worlds differently at small M: at M=100 DRIFT has the largest median distance of the three but not the largest UNKNOWN fraction (or vice versa); report which.
(B) AGREEMENT ON WRONG ANSWERS WITHOUT COPYING (after Kim et al. 2506.07962): K=4 options, all models answer independently given the item; on each item the three wrong options have a shared 'attractiveness' vector d ~ Dirichlet(alpha,alpha,alpha). Two independent models that are both wrong pick the same wrong option with probability sum d_i^2. Exact E = (alpha+1)/(3alpha+1).
  B1 Monte Carlo (200k items) matches the exact value within .005 for alpha in {0.2,0.5,1,2,10,inf}. B2 alpha=0.5 gives .60 with NO copying and no shared model ancestry; alpha->inf gives the 1/3 'chance' baseline. B3 therefore the headline 'agreement when both wrong is far above 1/3' cannot by itself separate shared item structure from shared model lineage.
  Scope: a toy distractor model; it does not claim the paper's numbers are explained by it, and I have not checked how the paper's chance baseline is constructed.
"""
import numpy as np
src=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'open_world_guard.py')).read().split('# ---------------- PHASE 1')[0]; ns={}; exec(src,ns)
gen,feats=ns['gen'],ns['feats']
rng=np.random.default_rng(20261105)
# ---------- A ----------
def calib(M,R=600):
    ref={}
    for w in ('IND','DIFF','COMMON'):
        F1,_,_=feats(*gen(w,M,R,rng)); mu=F1.mean(0); sd=np.maximum(F1.std(0),1e-3)
        F2,_,_=feats(*gen(w,M,R,rng)); d=(((F2-mu)/sd)**2).mean(1); ref[w]=(mu,sd,np.quantile(d,.99))
    return ref
Ms=[50,100,200,400,800,1600,3200]; med={}; unk={}
for M in Ms:
    ref=calib(M)
    for w in ('ANTI','DRIFT','PARTIAL'):
        F,_,_=feats(*gen(w,M,1000,rng)); D=np.stack([(((F-ref[n][0])/ref[n][1])**2).mean(1) for n in ref],1); Dn=np.stack([D[:,i]/ref[n][2] for i,n in enumerate(ref)],1)
        med[(M,w)]=float(np.median(D.min(1))); unk[(M,w)]=float((Dn.min(1)>1).mean())
print("(A) world: median min-distance (continuous) / UNKNOWN fraction (hard threshold)")
print(f"{'M':>5s} "+" ".join(f"{w:>18s}" for w in ('ANTI','DRIFT','PARTIAL')))
for M in Ms: print(f"{M:5d} "+" ".join(f"{med[(M,w)]:9.2f}/{unk[(M,w)]:.2f}   " for w in ('ANTI','DRIFT','PARTIAL')))
def slope(w):
    xs=np.log([M for M in Ms if M>=200]); ys=np.log([med[(M,w)] for M in Ms if M>=200]); return np.polyfit(xs,ys,1)[0]
print("A1 log-log slope of median distance vs M (M>=200):",{w:round(slope(w),2) for w in ('ANTI','DRIFT','PARTIAL')})
def span(w):
    lo=[M for M in Ms if unk[(M,w)]<=.20]; hi=[M for M in Ms if unk[(M,w)]>=.80]
    return (max(lo) if lo else None, min(hi) if hi else None)
print("A2 largest M with UNKNOWN<=.20 and smallest M with >=.80:",{w:span(w) for w in ('ANTI','DRIFT','PARTIAL')})
print("A3 M=100 ranking by median distance:",sorted(('ANTI','DRIFT','PARTIAL'),key=lambda w:-med[(100,w)])," by UNKNOWN:",sorted(('ANTI','DRIFT','PARTIAL'),key=lambda w:-unk[(100,w)]))
# ---------- B ----------
print("\n(B) both-wrong agreement among independent models, shared per-item distractor attractiveness d~Dirichlet(alpha)")
print(f"{'alpha':>6s} {'exact':>7s} {'MC':>7s}")
ok=True
for al in (.2,.5,1,2,10,1e6):
    ex=(al+1)/(3*al+1); d=rng.dirichlet([al]*3,size=200000); mc=float((d**2).sum(1).mean()); ok&=abs(mc-ex)<.005
    print(f"{al:6g} {ex:7.4f} {mc:7.4f}")
print("B1 MC within .005 of exact for all alpha:",ok)
print("B2 alpha=0.5 exact value:",round((.5+1)/(3*.5+1),4),"(no copying, no shared lineage); alpha->inf:",round((1e6+1)/(3e6+1),4))
