"""Untouched-seed posthoc long horizon checks for near-neutral threshold candidates."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from threshold_policy import ThresholdGarden

ROOT=Path(__file__).resolve().parent
THRESHOLDS=(.5,.525,.55)
SEEDS=range(950,958)
STEPS=20000
CHECK={0,600,2000,5000,10000,15000,20000}

def run_one(seed,tau):
    g=ThresholdGarden(seed=seed,threshold=tau)
    checkpoints=[]
    tail_sum=np.zeros(5)
    n=0
    for t in range(STEPS+1):
        if t in CHECK:
            checkpoints.append({'tick':t,'energy':float(g.energy.mean()),'resource':float(g.resource.mean()),
                                'floor':float((g.energy<=.01).mean()),'ceiling':float((g.energy>=.99).mean())})
        if t==STEPS:break
        if t>=STEPS-5000:
            r=g.resource
            a=(r>tau).astype(float)
            tail_sum+=np.array([float((.25*r*a-.063*a-.022).mean()),
                                float(r.mean()),float(a.mean()),float((r*a).mean()),
                                float((g.energy<=.01).mean())])
            n+=1
        g.step()
    return {'seed':seed,'threshold':tau,'checkpoints':checkpoints,
            'tail_raw_drift':tail_sum[0]/n,'tail_resource':tail_sum[1]/n,
            'tail_harvest':tail_sum[2]/n,'tail_resource_action':tail_sum[3]/n,
            'tail_floor':tail_sum[4]/n}

def run():
    rows=[run_one(seed,tau) for tau in THRESHOLDS for seed in SEEDS]
    summary={str(tau):{'final_energy':float(np.mean([r['checkpoints'][-1]['energy'] for r in rows if r['threshold']==tau])),
                        'tail_raw_drift':float(np.mean([r['tail_raw_drift'] for r in rows if r['threshold']==tau])),
                        'tail_harvest':float(np.mean([r['tail_harvest'] for r in rows if r['threshold']==tau])),
                        'tail_floor':float(np.mean([r['tail_floor'] for r in rows if r['threshold']==tau]))}
             for tau in THRESHOLDS}
    data={'design':'posthoc exploratory 20k tick test; candidate thresholds selected after 5k probe',
          'seeds':list(SEEDS),'thresholds':THRESHOLDS,'ticks':STEPS,'rows':rows,'summary':summary,
          'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                           for f in ('garden.py','threshold_policy.py','DYNAMICS_followup.py')}}
    (ROOT/'DYNAMICS_followup_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
