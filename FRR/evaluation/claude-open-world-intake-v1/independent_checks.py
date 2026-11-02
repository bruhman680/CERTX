"""Fresh algebra and fresh-seed contact; author-pipeline extension, not independent full rebuild."""
from fractions import Fraction as F
import ast,contextlib,io,json,pathlib
import numpy as np
R=pathlib.Path(__file__).resolve().parent
q=F(23,100); eps=F(1,20)
def noisy_joint(joint):
    return (1-2*eps)**2*joint+2*eps*(1-2*eps)*F(1,5)+eps**2
joint={k:noisy_joint(v) for k,v in {'IND':F(1,25),'DIFF':F(2,25),'SHARED':F(1,5),'PARTIAL':F(3,25)}.items()}
assert joint['DIFF']/q==F(853,2300)
assert joint['SHARED']/q==F(73,92)
diff_phi=(joint['DIFF']-q*q)/(q*(1-q))
assert diff_phi==F(324,1771) and diff_phi<F(1,4) and joint['DIFF']/q<F(3,5)
assert (joint['IND']+joint['SHARED'])/2==joint['PARTIAL']
p1=2*q-joint['SHARED'];p2=2*q-joint['IND']; pbar=(p1+p2)/2
# Even M, index x=0..M-1. E[cov(x,Y)] uses equal-weight first/second half means.
def trend(M):
    return float((p2-p1)*M/8)/np.sqrt((M*M-1)/12*float(pbar*(1-pbar)))
assert trend(400)>.11
# Dirichlet second moment: K E[d_i^2] = (alpha+1)/(K alpha+1).
assert (F(1,2)+1)/(3*F(1,2)+1)==F(3,5)
# Load ONLY reviewed imports/definitions/assignments preceding experiment loop.
p=R/'sources/FRR/lineage/sources/claude-phase3-and-scout-contacts-2026-11-02/phase3_promoted_classes.py'
tree=ast.parse(p.read_text()); nodes=[]
for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='root' for t in n.targets):break
    nodes.append(n)
ns={'__file__':str(p)};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(p),'exec'),ns)
rows=[]
for M in (400,1600,6400):
    ref=ns['calib'](M,False,2026110200+M,R=400)
    rng=np.random.default_rng(2026110300+M)
    for w in ('SWAP','PARTIAL'):
        a,b=ns['gen'](w,M,600,rng); features=ns['feats'](a,b,False); lab=ns['label'](features,ref)
        rows.append({'M':M,'world':w,'R':600,'mean_OR_trend':float(features[:,5].mean()),'UNKNOWN':float((lab=='UNKNOWN').mean()),'PARTIAL':float((lab=='PARTIAL').mean())})
result={'scope':'Exact independent algebra plus fresh-seed extension of Claude recognizer; not independent implementation of recognizer','DIFF_phi_exact':str(diff_phi),'DIFF_phi':float(diff_phi),'DIFF_guard_limit':'IND with probability approaching one; shared override vanishes','noisy_joints':{k:str(v) for k,v in joint.items()},'swap_OR_first_half':str(p1),'swap_OR_second_half':str(p2),'partial_OR_constant':str(pbar),'swap_population_OR_trend_M400':trend(400),'dirichlet_alpha_half_agreement':'3/5','rows':rows,'numpy':np.__version__}
(R/'INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
