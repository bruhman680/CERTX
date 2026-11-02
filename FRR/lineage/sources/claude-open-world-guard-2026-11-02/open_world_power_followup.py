"""
FOLLOW-UP to open_world_guard.py (added AFTER seeing its results; predictions written before running THIS file).
Observed there at M=100: F_open (mean-of-z^2 distance, 99% band) flagged UNKNOWN on LAG (.99) but only .07/.03/.06/.10 on ANTI/DRIFT/PARTIAL/SWAP, so O2/O3/O4 mostly FAILED.
Two rival explanations: (D) design dilution: averaging 7 squared z-scores hides a single anomalous feature; (P) power: at M=100 these worlds are barely separable from the known ones on these features, so no recognizer could flag them.
Tests: (1) replace the mean by the MAX z^2 over features ("max" mode) at M=100, same 99% calibration; (2) raise M to 400 and 1000 for both modes.
 Q1 (D): max mode at M=100 raises UNKNOWN on DRIFT by >=.3 (trend feature z is large) and on ANTI/PARTIAL by >=.15, with in-family false-UNKNOWN <=.10 (threshold calibrated at 99% but heavy-tailed correlations may exceed it).
 Q2 (P): with max mode UNKNOWN on ANTI at M=100 stays < .5 (about 1.8 sigma separation), and rises to >=.8 at M=400.
 Q3 PARTIAL and SWAP: max mode UNKNOWN >=.8 at M=400 and >=.9 at M=1000.
 Q4 F_care (closed) overreach on ANTI/DRIFT/PARTIAL/SWAP does NOT fall with M (a closed vocabulary cannot use more data to say 'none of the above'): at M=400 it is >=.9 on each.
 Q5 (framing) If Q1 fails and Q2 holds, the earlier failure is power; if Q1 holds, it was design.
"""
import numpy as np, re
src=open('open_world_guard.py').read().split('# ---------------- PHASE 1')[0]
ns={}; exec(src,ns)
gen,feats,KNOWN,OUT,care_claim_world,EPS=ns['gen'],ns['feats'],ns['KNOWN'],ns['OUT'],ns['care_claim_world'],ns['EPS']
def calibrate(M,rng,mode,R=800):
    ref={}
    for w in ('IND','DIFF','COMMON'):
        a1,b1=gen(w,M,R,rng); F1,_,_=feats(a1,b1); mu=F1.mean(0); sd=np.maximum(F1.std(0),1e-3)
        a2,b2=gen(w,M,R,rng); F2,_,_=feats(a2,b2); z2=((F2-mu)/sd)**2; d=(z2.max(1) if mode=='max' else z2.mean(1)); ref[w]=(mu,sd,np.quantile(d,.99))
    return ref
def claim(w,a,b,ref,mode,rng,bud=3):
    F,_,_=feats(a,b); names=list(ref); D=[]
    for n in names:
        z2=((F-ref[n][0])/ref[n][1])**2; D.append((z2.max(1) if mode=='max' else z2.mean(1))/ref[n][2])
    D=np.stack(D,1); ok=D.min(1)<=1.0; lab=np.array(names,dtype=object)[D.argmin(1)]; out=np.full(a.shape[0],'UNKNOWN',dtype=object); out[ok]=lab[ok]
    sh=out=='COMMON'; p=.95 if w=='COPY' else .05; k=(rng.random((a.shape[0],bud))<p).sum(1); out[sh]=np.where(k[sh]>bud/2,'COPY','COMMON'); return out
root=np.random.SeedSequence(20261103); S=root.spawn(20); si=0; R=1200; res={}
print("UNKNOWN fraction (open) / overreach fraction (closed F_care) by world; in-family false-UNKNOWN = mean over known worlds")
for M in (100,400,1000):
    for mode in ('mean','max'):
        ref=calibrate(M,np.random.default_rng(S[si]),mode); si+=1; rng=np.random.default_rng(S[si]); si+=1
        row={}
        for w in KNOWN+OUT:
            a,b=gen(w,M,R,rng); cl=claim(w,a,b,ref,mode,rng); row[w]=float((cl=='UNKNOWN').mean())
            if mode=='mean':
                cc=care_claim_world(w,a,b,M,rng); res[(M,w,'care_over')]=float(((cc!=w)&(cc!='UNRES_INDDIFF')).mean()) if w in KNOWN else float((cc!='UNRES_INDDIFF').mean())
        res[(M,mode)]=row
        print(f"M={M:4d} {mode:4s} in-family false-UNKNOWN {np.mean([row[w] for w in KNOWN]):.3f} | "+" ".join(f"{w}:{row[w]:.2f}" for w in OUT))
print("\nF_care (closed) overreach on outside worlds by M:")
for M in (100,400,1000): print(f"  M={M:4d} "+" ".join(f"{w}:{res[(M,w,'care_over')]:.2f}" for w in OUT))
g=lambda M,mo,w: res[(M,mo)][w]
print("\nCHECKS")
print(" Q1 max-mean UNKNOWN gain at M=100: DRIFT",round(g(100,'max','DRIFT')-g(100,'mean','DRIFT'),2),"ANTI",round(g(100,'max','ANTI')-g(100,'mean','ANTI'),2),"PARTIAL",round(g(100,'max','PARTIAL')-g(100,'mean','PARTIAL'),2)," in-family false-UNKNOWN (max):",round(np.mean([g(100,'max',w) for w in KNOWN]),3))
print(" Q2 ANTI max: M=100",round(g(100,'max','ANTI'),2)," M=400",round(g(400,'max','ANTI'),2))
print(" Q3 PARTIAL/SWAP max: M=400",round(g(400,'max','PARTIAL'),2),round(g(400,'max','SWAP'),2)," M=1000",round(g(1000,'max','PARTIAL'),2),round(g(1000,'max','SWAP'),2))
print(" Q4 closed overreach M=400 ANTI/DRIFT/PARTIAL/SWAP:",[round(res[(400,w,'care_over')],2) for w in ('ANTI','DRIFT','PARTIAL','SWAP')])
