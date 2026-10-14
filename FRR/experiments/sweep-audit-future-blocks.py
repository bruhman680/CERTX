"""Finite-horizon prediction audit. No infinite-state or cross-substrate claim."""
import itertools,json
from pathlib import Path
import numpy as np
K=np.array([[[.85,.15],[.10,.90]],[[.55,.45],[.40,.60]]])
def histories(eps,n):
    cur={(0,):np.array([.25,.25]),(1,):np.array([.25,.25])}
    T=np.array([[1-eps,eps],[eps,1-eps]])
    for _ in range(1,n):
        cur={w+(y,):(a*K[:,w[-1],y])@T for w,a in cur.items() for y in (0,1)}
    return cur

def block(y,b,T,horizon):
    cur={(y,):b}
    for _ in range(horizon):
        cur={w+(z,):(a*K[:,w[-1],z])@T for w,a in cur.items() for z in (0,1)}
    return np.array([a.sum() for a in cur.values()])
rows=[]
for eps in (0,.01,.05,.2,.5):
    T=np.array([[1-eps,eps],[eps,1-eps]])
    for depth in (4,8,12):
        H=histories(eps,depth)
        vectors={h:np.array([block(w[-1],a/a.sum(),T,h) for w,a in H.items()]) for h in (1,2,3)}
        assert abs(sum(a.sum() for a in H.values())-1)<1e-12
        for h,V in vectors.items():
            assert np.max(np.abs(V.sum(axis=1)-1))<1e-12
            rows.append(dict(eps=eps,depth=depth,future_length=h,counts={str(d):len(set(map(tuple,np.round(V,d)))) for d in (9,3,2)}))
# Collision after coarse one-step rounding: same bin, different two-step prediction.
H=histories(.05,12); W=list(H); T=np.array([[.95,.05],[.05,.95]])
V1=np.array([block(w[-1],a/a.sum(),T,1)[1] for w,a in H.items()]); V2=np.array([block(w[-1],a/a.sum(),T,2) for w,a in H.items()])
bins={}
example=None
for i,v in enumerate(V1):
    key=round(float(v),2)
    if key in bins:
        j=bins[key]; tv=float(np.abs(V2[i]-V2[j]).sum()/2)
        if example is None or tv>example['future_tv']: example=dict(histories=[''.join(map(str,W[j])),''.join(map(str,W[i]))],rounded_next=key,exact_next=[float(V1[j]),float(v)],future_tv=tv)
    else: bins[key]=i
result={'scope':'nonstationary uniform initial distribution; finite histories; counts of rounded future-block probability vectors','rows':rows,'coarse_collision':example,'generic_counterexample':{'construction':'A and B both emit 0 deterministically; A transitions to C, which emits 1; B transitions to B. Initial hidden state A versus B.','next_output_distribution':[1,0],'two_output_A':'01','two_output_B':'00','two_output_tv':1},'special_kernel':'Next probability identifies (last visible symbol, hidden-bit belief): y=0 range [.15,.45], y=1 range [.6,.9], each affine with nonzero slope. Thus exact one-step equality IS sufficient for full-future equality in this specified kernel.'}
Path('/workspace/frr/evaluation/results/sweep-audit-future-blocks.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'coarse_collision':example,'rows':len(rows)}))
