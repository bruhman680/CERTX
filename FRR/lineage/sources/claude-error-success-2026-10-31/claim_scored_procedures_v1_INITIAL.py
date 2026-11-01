"""
CLAIM-SCORED PROCEDURE COMPARISON (Claude, 2026-11-01). Toy: two answerers A,B over M items; hidden world decides how their errors arise. Procedures observe error flags (flip prob eps=.05) and may spend probes.
Worlds (marginal error rate .2 each):
 IND    independent errors.
 DIFF   shared item difficulty: hard (prob .5) -> p=.4, easy -> p=0; independent given item (EL-C1 style). phi(A,B)=.25.
 COMMON hidden source defect hits an item set (each item w.p. .2); A and B both err on it, B has its own copy of the defect.
 COPY   A errs w.p. .2; B copies A's answer.      COMMON and COPY give IDENTICAL passive error flags. Only an intervention (correct A's source, re-ask B on an error item) separates them: B's error vanishes under COPY, stays under COMMON. Probe reads correctly w.p. .95.
Procedures (claims are from {IND, DIFF, COMMON, COPY, UNRES_SHARED = COMMON-or-COPY, UNRES_INDDIFF = IND-or-DIFF}):
 S        success accumulation: high pass rate / agreement => claims IND always (agreement treated as independent confirmation).
 F_naive  failure-first, passive only: phi_hat>.125 threshold; if error sets match (>=90% overlap) claims COMMON (the favoured story).
 F_care   failure-first with claim discipline: IND only if phi_hat+2/sqrt(M)<.25, DIFF only if phi_hat-2/sqrt(M)>0, else UNRES_INDDIFF; if error sets match claims UNRES_SHARED, and with b>=1 probes resolves it by majority of probes.
 F_probe  always probes b=3 on errors regardless of passive pattern and claims COMMON/COPY from the probe majority (route-attribution reflex).
Scoring against truth: correct = claim equals truth; honest_unresolved = an unresolved set containing the truth; overreach = specific wrong claim or an unresolved set missing the truth.

PREDICTIONS (written before running):
 P1 S: correct only in IND (25% overall); overreach 75% at every M.
 P2 F_naive at M=100: correct >=.85 in IND, DIFF, COMMON; in COPY it claims COMMON >=.9 of runs; overall overreach about 25%.
 P3 F_care b=0: in COMMON and COPY, honest_unresolved >=.9 and overreach <=.05 at M=100; correct in IND/DIFF >=.85 at M=100. With b=3, correct in COMMON and COPY >=.9.
 P4 At M=20, F_naive misclassifies IND/DIFF in more than 25% of runs; F_care overreach there is below F_naive's by at least 10 points, paid for by more honest_unresolved.
 P5 F_probe spends probes in IND/DIFF where there is no source to find, and overreaches there (about 100%); its total overreach at M=100 >= 45%.
 P6 No procedure wins on all of: low overreach, probes used, and correctness at small M. State the tradeoff found.
Not tested: real agents, unknown world families, claim scope beyond the cause label, repair of downstream cached answers.
"""
import numpy as np
rng=np.random.default_rng(20261101)
EPS=.05; PR=.95; R=3000
WORLDS=('IND','DIFF','COMMON','COPY')
def gen(w,M):
    if w=='IND': a=rng.random((R,M))<.2; b=rng.random((R,M))<.2
    elif w=='DIFF':
        h=rng.random((R,M))<.5; p=np.where(h,.4,0.0); a=rng.random((R,M))<p; b=rng.random((R,M))<p
    elif w=='COMMON': d=rng.random((R,M))<.2; a=d.copy(); b=d.copy()
    else: a=rng.random((R,M))<.2; b=a.copy()
    fl=lambda x: x^(rng.random(x.shape)<EPS)
    return fl(a),fl(b)
def phi(a,b):
    a=a.astype(float); b=b.astype(float); ma,mb=a.mean(1),b.mean(1)
    cov=(a*b).mean(1)-ma*mb; va=ma*(1-ma); vb=mb*(1-mb); return cov/np.sqrt(np.maximum(va*vb,1e-12))
def match(a,b):
    both=(a&b).sum(1); either=(a|b).sum(1); return both/np.maximum(either,1)   # Jaccard of error sets
def probes(w,n_err,b):
    """majority of b probes: returns True if judged 'B's error vanished' (COPY)."""
    if b==0: return None
    p=PR if w=='COPY' else 1-PR
    k=(rng.random((R,b))<p).sum(1); return k>b/2
def claims(proc,w,a,b,M,bud=0):
    ph=phi(a,b); J=match(a,b); ident=J>=.9-.0; pr=0
    if proc=='S': return np.array(['IND']*R),0
    out=np.empty(R,dtype=object)
    if proc=='F_naive':
        out[:]=np.where(ph>.125,'DIFF','IND'); out[ident]='COMMON'; return out,0
    if proc=='F_care':
        hi=ph+2/np.sqrt(M); lo=ph-2/np.sqrt(M)
        out[:]='UNRES_INDDIFF'; out[hi<.25]='IND'; out[(lo>0)&(hi>=.25)]='DIFF'
        if bud==0: out[ident]='UNRES_SHARED'; return out,0
        cp=probes(w,None,bud); out[ident]=np.where(cp[ident],'COPY','COMMON'); return out,bud*ident.mean()
    if proc=='F_probe':
        cp=probes(w,None,3); out[:]=np.where(cp,'COPY','COMMON'); return out,3.0
def score(claim,truth):
    c=claim; o=np.empty(R,dtype=object)
    for i in range(R):
        x=c[i]
        if x==truth: o[i]='correct'
        elif x=='UNRES_SHARED': o[i]='honest' if truth in('COMMON','COPY') else 'over'
        elif x=='UNRES_INDDIFF': o[i]='honest' if truth in('IND','DIFF') else 'over'
        else: o[i]='over'
    return {k:float((o==k).mean()) for k in('correct','honest','over')}
table={}
PROCS=[('S',0),('F_naive',0),('F_care',0),('F_care',3),('F_probe',3)]
print(f"{'M':>4s} {'procedure':12s} " + " ".join(f"{w:>20s}" for w in WORLDS) + "   overall overreach  probes/run")
for M in (20,40,100):
    data={w:gen(w,M) for w in WORLDS}
    for proc,bud in PROCS:
        row=[];ov=[];pr_tot=0
        for w in WORLDS:
            cl,pr=claims(proc,w,*data[w],M,bud); sc=score(cl,w); table[(M,proc,bud,w)]=sc
            row.append(f"c{sc['correct']:.2f}/h{sc['honest']:.2f}/o{sc['over']:.2f}"); ov.append(sc['over']); pr_tot+=pr
        print(f"{M:4d} {proc+('_b%d'%bud if proc=='F_care' else ''):12s} "+" ".join(f"{r:>20s}" for r in row)+f"   {np.mean(ov):.3f}             {pr_tot/4:.2f}")
    print()
T=table
print("CHECKS")
print(" P1 S overall overreach:",[round(np.mean([T[(M,'S',0,w)]['over'] for w in WORLDS]),3) for M in (20,40,100)])
print(" P2 F_naive M=100 correct IND/DIFF/COMMON:",[round(T[(100,'F_naive',0,w)]['correct'],2) for w in ('IND','DIFF','COMMON')]," COPY over:",round(T[(100,'F_naive',0,'COPY')]['over'],2))
print(" P3 F_care b0 M=100 honest COMMON/COPY:",[round(T[(100,'F_care',0,w)]['honest'],2) for w in ('COMMON','COPY')]," over:",[round(T[(100,'F_care',0,w)]['over'],2) for w in ('COMMON','COPY')]," correct IND/DIFF:",[round(T[(100,'F_care',0,w)]['correct'],2) for w in ('IND','DIFF')])
print("    F_care b3 M=100 correct COMMON/COPY:",[round(T[(100,'F_care',3,w)]['correct'],2) for w in ('COMMON','COPY')])
print(" P4 M=20 F_naive IND/DIFF misclassified:",[round(T[(20,'F_naive',0,w)]['over'],2) for w in ('IND','DIFF')]," overall over naive vs care_b0:",round(np.mean([T[(20,'F_naive',0,w)]['over'] for w in WORLDS]),3),round(np.mean([T[(20,'F_care',0,w)]['over'] for w in WORLDS]),3))
print(" P5 F_probe M=100 overreach IND/DIFF:",[round(T[(100,'F_probe',3,w)]['over'],2) for w in ('IND','DIFF')]," overall:",round(np.mean([T[(100,'F_probe',3,w)]['over'] for w in WORLDS]),3))
