"""Independent stable-world comparison for the development-selected welfare objective."""
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import WelfareGarden,RuleGarden,train,score

SEEDS=tuple(range(9400,9412))
ARMS=('resource_online','resource_frozen','resource_deterministic','raw_online',
      'fixed50','rescue','reverse')

def run():
    out=[]
    for s in SEEDS:
        theta=train('resource',s,10,1000)
        rawtheta=train('raw',s,10,1000)
        for arm in ARMS:
            if arm.startswith('resource') or arm=='raw_online':
                obj='raw' if arm=='raw_online' else 'resource'
                learn=arm.endswith('online')
                det=arm.endswith('deterministic')
                g=WelfareGarden(seed=s+20_000,size=10,objective=obj,learning=learn,
                                deterministic=det)
                g.theta=(rawtheta if obj=='raw' else theta).copy()
            else:
                g=RuleGarden(seed=s+20_000,size=10,rule=arm)
            checkpoints=[]
            for t in range(1,3001):
                g.step()
                if t in (1000,2000,3000):
                    checkpoints.append({'tick':t,'energy':float(g.energy.mean()),
                                        'floor':float(np.mean(g.energy<=.01))})
            out.append({'seed':s,'arm':arm,'score':score(g),
                        'energy':float(g.energy.mean()),
                        'floor':float(np.mean(g.energy<=.01)),
                        'checkpoints':checkpoints})
    summary={}
    for arm in ARMS:
        rows=[r for r in out if r['arm']==arm]
        summary[arm]={'mean_energy':float(np.mean([r['energy'] for r in rows])),
                      'mean_floor':float(np.mean([r['floor'] for r in rows])),
                      'mean_score':float(np.mean([r['score'] for r in rows]))}
    return {'design':{'seeds':SEEDS,'size':10,'ticks':3000,
                      'world_laws':'unchanged original Garden',
                      'selected_objective':'resource chosen on prior development only'},
            'summary':summary,'individual':out,
            'source_sha256':{f:hashlib.sha256((Path(__file__).parent/f).read_bytes()).hexdigest()
                for f in ('garden.py','NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py',Path(__file__).name)}}

if __name__=='__main__':
    z=run()
    path=Path(__file__).with_name('NEXT_WELFARE_stable_results.json')
    path.write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps(z['summary'],indent=2))
