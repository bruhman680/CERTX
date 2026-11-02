"""
OPEN-WORLD GUARD (Claude, 2026-11-02). Responds to (i) Thomas's point that a closed test only follows the groove it cuts, and (ii) Codex's intake (real-artifact-provenance-v1 §5-6) asking for an outside-family / sham-calibration check of the v3 guard.
Self-contained (no external files, no absolute paths). Reuses the v3 toy: two answerers A,B over M items, marginal error .2, flag flips eps=.05, probes read correctly w.p. .95.
Corrections accepted from Codex before this run: (a) exact DIFF conditional agreement under flag noise is 853/2300=.3709, not my .42 (I left noise off DIFF); COMMON/COPY .7935; the .6 threshold still separates them. (b) The v1 docstring's '>=.9 overlap' wording is stale; v3 executes cond.agreement>=.6 both ways with >=3 errors each.
KNOWN worlds: IND, DIFF, COMMON, COPY (as before). OUTSIDE worlds (not in the closed claim vocabulary):
 ANTI    B errs only when A does not: P(b|a=1)=0, P(b|a=0)=.25 (marginal .2).   LAG   b_i = a_{i-1}, a iid.
 DRIFT   shared error rate rises .05->.35 across the run, A,B independent given the rate.   PARTIAL  B copies A w.p. .5 else independent (cond.agreement about .6 before noise).
 UPSTREAM both copy a hidden third source (signature identical to COMMON/COPY; vocabulary cannot name it).   SWAP (HELD OUT, not looked at in phase 1) B copies A in the first half, independent in the second half.
PHASE 1 (open, unscored): print per-world feature means (phi, P(b|a), P(a|b), cross-lag corr both ways, trend, rate diff) and what closed F_care claims on each outside world. Look first, define after.
PHASE 2 (frozen): F_open = diagonal-Gaussian open-set recognizer over the same features, calibrated on separate seeds from the known simulators (mean/sd on one half, 99th-percentile distance threshold on the other half); outputs a known class or UNKNOWN. Shared signature resolved by b=3 probes. F_open_est replaces known eps with eps estimated from G gold items (planted known-error and known-correct items) and snaps to an eps grid. Calibration parameters are hashed BEFORE the evaluation seeds are drawn.
Scoring: known worlds: correct/overreach/honest-unresolved as before; outside worlds: honest = UNKNOWN (or UNRES for shared-signature); overreach = any specific known claim. UPSTREAM is reported separately (its signature is SHARED, which is not an overreach but cannot name the route).

PREDICTIONS (written before running):
 O1 Closed F_care (v3 rules) overreaches silently on outside worlds at M=100: claims IND on ANTI and LAG in >=90% of runs; claims DIFF or IND on DRIFT in >=70%.
 O2 F_open at M=100: UNKNOWN >=.70 on ANTI, LAG, DRIFT; in-family false-UNKNOWN <=.15; in-family correct rates within .10 of F_care v3 (cost of vigilance).
 O3 HELD-OUT SWAP: F_open UNKNOWN or unresolved >=.50 (never tuned on it); closed F_care overreach >=.50.
 O4 PARTIAL sits between DIFF and SHARED on the conditional-agreement feature; F_open does NOT claim a specific known class on it more than 30% of the time.
 O5 F_open_est: guard fire rate on COMMON/COPY at M=100 is .80-.95 with G=40 gold items and >=.93 with G=400.
 O6 At M=40 F_open in-family false-UNKNOWN is higher than at M=100 or its outside-world UNKNOWN is lower (small M cannot support open-world claims); name which.
 Not tested: real agents, free-form behaviour, a learner that discovers its own categories (phase 1 only inspects features by eye), whether the six outside worlds are representative of anything.
"""
import numpy as np, hashlib, json, itertools
EPS=.05; PR=.95
root=np.random.SeedSequence(20261102); S=root.spawn(8)
KNOWN=('IND','DIFF','COMMON','COPY'); OUT=('ANTI','LAG','DRIFT','PARTIAL','UPSTREAM','SWAP')
def raw(w,M,R,rng):
    if w=='IND': a=rng.random((R,M))<.2; b=rng.random((R,M))<.2
    elif w=='DIFF':
        h=rng.random((R,M))<.5; p=np.where(h,.4,0.0); a=rng.random((R,M))<p; b=rng.random((R,M))<p
    elif w=='COMMON': d=rng.random((R,M))<.2; a=d.copy(); b=d.copy()
    elif w=='COPY': a=rng.random((R,M))<.2; b=a.copy()
    elif w=='UPSTREAM': c=rng.random((R,M))<.2; a=c.copy(); b=c.copy()
    elif w=='ANTI':
        a=rng.random((R,M))<.2; b=np.where(a,False,rng.random((R,M))<.25)
    elif w=='LAG':
        a=rng.random((R,M))<.2; b=np.concatenate([rng.random((R,1))<.2,a[:,:-1]],1)
    elif w=='DRIFT':
        p=np.linspace(.05,.35,M)[None,:]; a=rng.random((R,M))<p; b=rng.random((R,M))<p
    elif w=='PARTIAL':
        a=rng.random((R,M))<.2; cp=rng.random((R,M))<.5; b=np.where(cp,a,rng.random((R,M))<.2)
    elif w=='SWAP':
        a=rng.random((R,M))<.2; ind=rng.random((R,M))<.2; half=np.arange(M)[None,:]>=M//2; b=np.where(half,ind,a)
    return a,b
def gen(w,M,R,rng,eps=EPS):
    a,b=raw(w,M,R,rng); fl=lambda x: x^(rng.random(x.shape)<eps); return fl(a),fl(b)
def corr(x,y):
    x=x.astype(float); y=y.astype(float); xm=x-x.mean(1,keepdims=True); ym=y-y.mean(1,keepdims=True)
    return (xm*ym).sum(1)/np.sqrt(np.maximum((xm**2).sum(1)*(ym**2).sum(1),1e-9))
def feats(a,b):
    R,M=a.shape; both=(a&b).sum(1).astype(float); na=a.sum(1); nb=b.sum(1)
    pba=both/np.maximum(na,1); pab=both/np.maximum(nb,1); idx=np.broadcast_to(np.arange(M,dtype=float),(R,M))
    return np.stack([corr(a,b),pba,pab,corr(a[:,:-1],b[:,1:]),corr(b[:,:-1],a[:,1:]),corr(idx,(a|b)),(a.mean(1)-b.mean(1))],1), na, nb
FN=['phi','P(b|a)','P(a|b)','xlag a->b','xlag b->a','trend','rate diff']
def phi_(a,b): return corr(a,b)
def care_claim(a,b,M,rng,bud=3):
    ph=phi_(a,b); both=(a&b).sum(1).astype(float); na=a.sum(1); nb=b.sum(1)
    pba=both/np.maximum(na,1); pab=both/np.maximum(nb,1); ident=(na>=3)&(nb>=3)&(pba>=.6)&(pab>=.6)
    hi=ph+2/np.sqrt(M); lo=ph-2/np.sqrt(M); out=np.full(a.shape[0],'UNRES_INDDIFF',dtype=object)
    out[hi<.25]='IND'; out[(lo>0)&(hi>=.25)]='DIFF'
    k=(rng.random((a.shape[0],bud))<PR).sum(1); out[ident]=np.where(k[ident]>bud/2,'COPY','COMMON')   # probe outcome placeholder replaced per world below
    return out,ident
def care_claim_world(w,a,b,M,rng,bud=3):
    out,ident=care_claim(a,b,M,rng,bud)
    p=PR if w=='COPY' else 1-PR            # oracle probe: only COPY removes B's error (UPSTREAM/others behave like not-COPY)
    k=(rng.random((a.shape[0],bud))<p).sum(1); out[ident]=np.where(k[ident]>bud/2,'COPY','COMMON'); return out
# ---------------- PHASE 1: open look ----------------
print("PHASE 1 (open, unscored). Feature means over 600 runs at M=100 (flag noise .05)")
print(f"{'world':9s} "+" ".join(f"{n:>10s}" for n in FN))
r1=np.random.default_rng(S[0])
for w in KNOWN+OUT[:5]:                      # SWAP is held out of phase 1
    a,b=gen(w,100,600,r1); F,_,_=feats(a,b); print(f"{w:9s} "+" ".join(f"{x:10.3f}" for x in F.mean(0)))
print("\nClosed F_care (v3) claims on outside worlds, M=100 (fractions)")
for w in OUT[:5]:
    a,b=gen(w,100,600,r1); cl=care_claim_world(w,a,b,100,r1); labs=sorted(set(cl)); print(f"  {w:9s} "+"  ".join(f"{l}:{(cl==l).mean():.2f}" for l in labs))
# ---------------- PHASE 2: calibrate, freeze, evaluate ----------------
def calibrate(eps,M,seed,R=600):
    rng=np.random.default_rng(seed); ref={}
    for w in ('IND','DIFF','COMMON'):                        # COMMON/COPY pooled as the SHARED class (identical passive signature)
        a1,b1=gen(w,M,R,rng,eps); F1,_,_=feats(a1,b1); mu=F1.mean(0); sd=np.maximum(F1.std(0),1e-3)
        a2,b2=gen(w,M,R,rng,eps); F2,_,_=feats(a2,b2); d2=(((F2-mu)/sd)**2).mean(1); thr=np.quantile(d2,.99)
        ref[w]=(mu,sd,thr)
    return ref
GRID=(0.0,.025,.05,.075,.1)
REF={}; sq=S[1].spawn(20); k=0
for M in (40,100):
    for e in GRID: REF[(M,e)]=calibrate(e,M,sq[k]); k+=1
digest=hashlib.sha256(json.dumps({f"{M}_{e}":{w:[v[0].round(6).tolist(),v[1].round(6).tolist(),round(float(v[2]),6)] for w,v in r.items()} for (M,e),r in REF.items()},sort_keys=True).encode()).hexdigest()[:16]
print(f"\nPHASE 2: calibration frozen, digest {digest}; evaluation seeds drawn after this line.")
def open_claim(w,a,b,M,eps,rng,bud=3):
    ref=REF[(M,min(GRID,key=lambda g:abs(g-eps)))]; F,na,nb=feats(a,b)
    names=list(ref); D=np.stack([(((F-ref[n][0])/ref[n][1])**2).mean(1)/ref[n][2] for n in names],1)   # <=1 means inside that world's 99% band
    best=D.argmin(1); ok=D.min(1)<=1.0; out=np.full(a.shape[0],'UNKNOWN',dtype=object)
    lab=np.array(names,dtype=object)[best]; out[ok]=lab[ok]
    sh=out=='COMMON'                                              # SHARED class -> resolve by probes
    p=PR if w=='COPY' else 1-PR; k=(rng.random((a.shape[0],bud))<p).sum(1); out[sh]=np.where(k[sh]>bud/2,'COPY','COMMON')
    return out
def est_eps(G,rng):
    # gold set: G/2 items with planted TRUE error, G/2 planted TRUE correct; flags flip w.p. EPS. eps_hat=(miss+false alarm)/2
    miss=(rng.random(G//2)<EPS).mean(); fa=(rng.random(G//2)<EPS).mean(); return (miss+fa)/2
rE=np.random.default_rng(S[2]); R=1500
def score(cl,w):
    if w in KNOWN:
        return dict(correct=float((cl==w).mean()), unknown=float((cl=='UNKNOWN').mean()), over=float(((cl!=w)&(cl!='UNKNOWN')&(cl!='UNRES_INDDIFF')).mean()), unres=float((cl=='UNRES_INDDIFF').mean()))
    return dict(unknown=float((cl=='UNKNOWN').mean()), over=float(((cl!='UNKNOWN')&(cl!='UNRES_INDDIFF')).mean()), unres=float((cl=='UNRES_INDDIFF').mean()))
res={}
for M in (40,100):
    print(f"\n=== M={M} ===  (K=known; per cell: correct/unknown/overreach/unres for known worlds, unknown/overreach/unres for outside)")
    for w in KNOWN+OUT:
        a,b=gen(w,M,R,rE)
        cc=care_claim_world(w,a,b,M,rE); co=open_claim(w,a,b,M,EPS,rE)
        for G in (40,400):
            eh=np.array([est_eps(G,rE) for _ in range(R)]); ce=np.empty(R,dtype=object)
            for e in set(min(GRID,key=lambda g:abs(g-x)) for x in eh):
                m=np.array([min(GRID,key=lambda g:abs(g-x))==e for x in eh]); ce[m]=open_claim(w,a[m],b[m],M,e,rE)
            res[(M,w,f'open_est{G}')]=score(ce,w)
        res[(M,w,'care')]=score(cc,w); res[(M,w,'open')]=score(co,w)
        f=lambda k_: " ".join(f"{k}:{v:.2f}" for k,v in res[(M,w,k_)].items())
        print(f" {w:9s} care[{f('care')}]  open[{f('open')}]")
        print(f"           open_est40[{f('open_est40')}]  open_est400[{f('open_est400')}]")
R100=lambda w,p,k: res[(100,w,p)][k]
print("\nCHECKS (M=100 unless noted)")
print(" O1 care claims IND on ANTI/LAG:",[round(1-res[(100,w,'care')]['unknown']-res[(100,w,'care')]['unres']-0,2) for w in ('ANTI','LAG')],"(this is overreach incl. any known claim); DRIFT overreach:",round(R100('DRIFT','care','over'),2))
print(" O2 open UNKNOWN ANTI/LAG/DRIFT:",[round(R100(w,'open','unknown'),2) for w in ('ANTI','LAG','DRIFT')]," in-family false-UNKNOWN IND/DIFF/COMMON/COPY:",[round(R100(w,'open','unknown'),2) for w in KNOWN]," correct open vs care:",[(round(R100(w,'open','correct'),2),round(R100(w,'care','correct'),2)) for w in KNOWN])
print(" O3 SWAP open unknown+unres:",round(R100('SWAP','open','unknown')+R100('SWAP','open','unres'),2)," care overreach:",round(R100('SWAP','care','over'),2))
print(" O4 PARTIAL open overreach (specific known claim):",round(R100('PARTIAL','open','over'),2)," unknown:",round(R100('PARTIAL','open','unknown'),2))
print(" O5 est-eps guard (correct on COMMON/COPY incl. probe): G=40",[round(R100(w,'open_est40','correct'),2) for w in ('COMMON','COPY')]," G=400",[round(R100(w,'open_est400','correct'),2) for w in ('COMMON','COPY')]," known-eps open",[round(R100(w,'open','correct'),2) for w in ('COMMON','COPY')])
print(" O6 M=40 vs M=100 open: in-family false-UNKNOWN",[round(np.mean([res[(M,w,'open')]['unknown'] for w in KNOWN]),2) for M in (40,100)]," outside UNKNOWN",[round(np.mean([res[(M,w,'open')]['unknown'] for w in ('ANTI','LAG','DRIFT','PARTIAL','SWAP')]),2) for M in (40,100)])
