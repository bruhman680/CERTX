"""
PHASE 3 (Claude, 2026-11-02): promote the categories I saw BY EYE in phase 1 of open_world_guard.py into recognizer classes, freeze, then test on worlds the recognizer never saw.
Hindsight caveat stated up front: I wrote the phase-1 worlds, so the 7 classes (IND, DIFF, SHARED=COMMON/COPY/UPSTREAM, ANTI, LAG, DRIFT, PARTIAL) are not discovered categories; they are my own worlds turned into labels.
Held-out worlds (never in class construction): SWAP (B copies A in first half only; pooled features look like PARTIAL), LAG2 (b_i = a_{i-2}; the feature set only has lag-1 cross-correlation), COMPOSITE (ANTI relationship plus a rising shared rate; combines two features at once).
Recognizer: diag-Gaussian over 7 features (phi, P(b|a), P(a|b), xlag a->b, xlag b->a, trend, rate diff), mean z^2 distance to each class, 99% band calibrated on separate seeds; UNKNOWN outside every band; nearest-by-D/threshold inside.
Post-hoc stage (flagged): add two features (lag-2 cross-correlation, and phi(first half)-phi(second half)); re-calibrate the same 7 classes with 9 features and re-test the held-out worlds. They are then no longer held out.

PREDICTIONS (written before running):
 R1 At M=400 each of the 7 own-world classes is recognised >=.85 (own label) including ANTI, LAG, DRIFT, PARTIAL; at M=100 ANTI and DRIFT are recognised >=.50.
 R2 SWAP at M=400 is labelled PARTIAL in >=.60 of runs (right scope, wrong structure) and UNKNOWN <=.30.
 R3 LAG2 at M=400 is labelled IND in >=.80 of runs (no lag-2 feature, so it looks independent), i.e. the recognizer is confidently wrong about an unseen kind of structure.
 R4 COMPOSITE at M=400 is UNKNOWN in >=.60 of runs.
 R5 (post hoc) With the two added features LAG2 moves from IND to UNKNOWN (>=.80) at M=400, and SWAP is separated from PARTIAL (labelled PARTIAL <=.20, UNKNOWN >=.60).
 R6 In-family false-UNKNOWN stays <=.05 for all 7 classes at M=400 in both feature sets.
Not tested: any learner that proposes its own classes or features; real agents; whether these worlds are representative.
"""
import numpy as np
src=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'open_world_guard.py')).read().split('# ---------------- PHASE 1')[0]
ns={}; exec(src,ns)
gen_known,corr,feats7=ns['gen'],ns['corr'],ns['feats']
EPS=.05
def raw2(w,M,R,rng):
    if w=='LAG2':
        a=rng.random((R,M))<.2; b=np.concatenate([rng.random((R,2))<.2,a[:,:-2]],1); return a,b
    if w=='COMPOSITE':
        p=np.linspace(.05,.35,M)[None,:]; a=rng.random((R,M))<p; b=np.where(a,False,rng.random((R,M))<np.clip(p*1.35,0,1)*.95); return a,b
    raise KeyError(w)
def gen(w,M,R,rng):
    if w in ('LAG2','COMPOSITE'):
        a,b=raw2(w,M,R,rng); fl=lambda x:x^(rng.random(x.shape)<EPS); return fl(a),fl(b)
    return gen_known(w,M,R,rng)
def feats(a,b,ext):
    F,_,_=feats7(a,b)
    if not ext: return F
    M=a.shape[1]; h=M//2
    x2=corr(a[:,:-2],b[:,2:]); dphi=corr(a[:,:h],b[:,:h])-corr(a[:,h:],b[:,h:])
    return np.concatenate([F,x2[:,None],dphi[:,None]],1)
CLASSES={'IND':('IND',),'DIFF':('DIFF',),'SHARED':('COMMON','COPY','UPSTREAM'),'ANTI':('ANTI',),'LAG':('LAG',),'DRIFT':('DRIFT',),'PARTIAL':('PARTIAL',)}
WORLD2CLASS={w:c for c,ws in CLASSES.items() for w in ws}
def calib(M,ext,seed,R=800):
    rng=np.random.default_rng(seed); ref={}
    for c,ws in CLASSES.items():
        F1=np.concatenate([feats(*gen(w,M,R//len(ws),rng),ext) for w in ws]); mu=F1.mean(0); sd=np.maximum(F1.std(0),1e-3)
        F2=np.concatenate([feats(*gen(w,M,R//len(ws),rng),ext) for w in ws]); d=(((F2-mu)/sd)**2).mean(1); ref[c]=(mu,sd,np.quantile(d,.99))
    return ref
def label(F,ref):
    names=list(ref); D=np.stack([(((F-ref[n][0])/ref[n][1])**2).mean(1)/ref[n][2] for n in names],1)
    out=np.full(F.shape[0],'UNKNOWN',dtype=object); ok=D.min(1)<=1; out[ok]=np.array(names,dtype=object)[D.argmin(1)][ok]; return out
root=np.random.SeedSequence(20261104); S=root.spawn(30); si=0; R=1000; res={}
WORLDS=['IND','DIFF','COMMON','COPY','UPSTREAM','ANTI','LAG','DRIFT','PARTIAL','SWAP','LAG2','COMPOSITE']
for ext in (False,True):
    for M in (100,400):
        ref=calib(M,ext,S[si]); si+=1; rng=np.random.default_rng(S[si]); si+=1
        print(f"\n=== features={'9 (post hoc: +lag2 +half-split)' if ext else '7'}  M={M} ===  label fractions")
        for w in WORLDS:
            lab=label(feats(*gen(w,M,R,rng),ext),ref); frac={k:float((lab==k).mean()) for k in list(CLASSES)+['UNKNOWN']}
            res[(ext,M,w)]=frac; top=sorted(frac.items(),key=lambda kv:-kv[1])[:3]
            tag='' if w not in ('SWAP','LAG2','COMPOSITE') else '  (held out)' if not ext else '  (no longer held out)'
            print(f"  {w:10s} "+"  ".join(f"{k}:{v:.2f}" for k,v in top)+tag)
g=lambda e,M,w,k: res[(e,M,w)][k]
own=lambda e,M,w: g(e,M,w,WORLD2CLASS[w])
print("\nCHECKS")
print(" R1 M=400 own-class recognition:",{w:round(own(False,400,w),2) for w in WORLD2CLASS}," M=100 ANTI/DRIFT:",round(own(False,100,'ANTI'),2),round(own(False,100,'DRIFT'),2))
print(" R2 SWAP M=400 PARTIAL/UNKNOWN:",round(g(False,400,'SWAP','PARTIAL'),2),round(g(False,400,'SWAP','UNKNOWN'),2))
print(" R3 LAG2 M=400 IND:",round(g(False,400,'LAG2','IND'),2)," UNKNOWN:",round(g(False,400,'LAG2','UNKNOWN'),2))
print(" R4 COMPOSITE M=400 UNKNOWN:",round(g(False,400,'COMPOSITE','UNKNOWN'),2))
print(" R5 post hoc: LAG2 UNKNOWN",round(g(True,400,'LAG2','UNKNOWN'),2),"IND",round(g(True,400,'LAG2','IND'),2),"| SWAP PARTIAL",round(g(True,400,'SWAP','PARTIAL'),2),"UNKNOWN",round(g(True,400,'SWAP','UNKNOWN'),2))
print(" R6 in-family false-UNKNOWN M=400 (7 feat / 9 feat):",{w:(round(g(False,400,w,'UNKNOWN'),2),round(g(True,400,w,'UNKNOWN'),2)) for w in WORLD2CLASS})
