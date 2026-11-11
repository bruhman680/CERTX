"""Held-aside deterministic environmental recovery forks."""
import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone

import numpy as np
from garden import Garden
from SEASONS2_probe import neighbor, summer

HERE=Path(__file__).resolve().parent
SEEDS=tuple(range(41120,41124))

def step(r,e,regrowth):
    a=(r>.51).astype(float)
    nr=np.clip(r+.08*(neighbor(r)-r)+regrowth*(1.-r)-.18*r*a,0.,1.)
    ne=np.clip(e+.25*r*a-.03-.055*a+.008*(1.-a),0.,1.)
    return nr,ne

def simulate(seed):
    base=Garden(seed=seed,size=16,learning=False)
    r,e=base.resource.copy(),base.energy.copy()
    for t in range(1,12001): r,e=step(r,e,.06 if summer(t) else .048)
    parent={'energy':float(e.mean()),'resource':float(r.mean()),'floor':float(np.mean(e<=.01))}
    worlds={}
    for label in ('normal','boosted','recurring'):
        rr,ee=r.copy(),e.copy()
        points=[]
        for future in range(1,8001):
            rg=.06 if label=='normal' else .07 if label=='boosted' else (.048 if ((future-1)//1500)%2==0 else .06)
            rr,ee=step(rr,ee,rg)
            if future in (1500,3000,5000,8000):
                points.append({'elapsed':future,'energy':float(ee.mean()),'resource':float(rr.mean()),'floor':float(np.mean(ee<=.01))})
        worlds[label]=points
    return {'seed':seed,'parent':parent,'worlds':worlds}

def main():
    rows=[simulate(s) for s in SEEDS]
    summary={}
    for label in ('normal','boosted','recurring'):
        summary[label]={str(t):{k:float(np.mean([next(p[k] for p in row['worlds'][label] if p['elapsed']==t) for row in rows])) for k in ('energy','resource','floor')} for t in (1500,3000,5000,8000)}
    src={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('garden.py','SEASONS2_RECOVERY_PLAN.md','SEASONS2_probe.py','SEASONS2_RECOVERY_probe.py')}
    obj={'created_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':src,'seeds':SEEDS,'summary':summary,'rows':rows,
        'causal_note':'Three arms are exact same parent per seed. Differences are imposed regrowth laws, not adaptation.'}
    (HERE/'SEASONS2_RECOVERY_results.json').write_text(json.dumps(obj,indent=2)+'\n')

if __name__=='__main__':main()
