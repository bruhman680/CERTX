"""Isolate reward-objective effects at identical deterministic deployment mode."""
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import WelfareGarden,train,score

SEEDS=tuple(range(9500,9512))
OBJECTIVES=('raw','reserve','resource','reserve_resource')

def run():
    rows=[]
    for seed in SEEDS:
        policies={objective:train(objective,seed,10,1000)
                  for objective in OBJECTIVES}
        for regime in ('stable','mild'):
            for objective in OBJECTIVES:
                g=WelfareGarden(seed=seed+20_000,size=10,learning=False,
                                objective=objective,deterministic=True)
                g.theta=policies[objective].copy()
                checkpoints=[]
                for t in range(1,3001):
                    g.regrowth=(.055 if regime=='mild' and 1000<t<=2000 else .06)
                    g.step()
                    if t in (1000,2000,3000):
                        checkpoints.append({'t':t,'energy':float(g.energy.mean()),
                                            'floor':float(np.mean(g.energy<=.01))})
                rows.append({'seed':seed,'regime':regime,'objective':objective,
                             'energy':float(g.energy.mean()),
                             'floor':float(np.mean(g.energy<=.01)),
                             'score':score(g),'checkpoints':checkpoints})
    summary={}
    for regime in ('stable','mild'):
        for objective in OBJECTIVES:
            z=[r for r in rows if r['regime']==regime and r['objective']==objective]
            summary[regime+'/'+objective]={'energy':float(np.mean([r['energy'] for r in z])),
                                         'floor':float(np.mean([r['floor'] for r in z])),
                                         'score':float(np.mean([r['score'] for r in z]))}
    return {'design':{'seeds':SEEDS,'size':10,'pretrain_ticks':1000,'test_ticks':3000,
                      'teacher_free':True,'deterministic_frozen_deployment':True,
                      'regimes':['original unchanged','mild regrowth .06-.055-.06'],
                      'all_objectives_tested_without_selection':True},
            'summary':summary,'rows':rows,'sha256':{f:hashlib.sha256((Path(__file__).parent/f).read_bytes()).hexdigest()
               for f in ('garden.py','NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py',Path(__file__).name)}}

if __name__=='__main__':
    z=run();Path(__file__).with_name('NEXT_WELFARE_deterministic_results.json').write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps(z['summary'],indent=2))
