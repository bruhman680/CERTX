"""Independent safety-constrained consolidation validation; see preregistration."""
from pathlib import Path
import json,hashlib
import numpy as np
from MEMORY2_probe import assess,SNAPSHOTS
from NEXT_WELFARE_study import WelfareGarden,train

HERE=Path(__file__).parent

def one(seed):
    protected=train('reserve_resource',seed,8,800)
    g=WelfareGarden(seed=seed+10000,size=8,learning=True,
                    objective='reserve_resource',penalty=.3)
    g.theta=protected.copy()
    banks={'protected':protected.copy()}
    for tick in range(1,1601):
        g.regrowth=.055 if 534<tick<=1067 else .06
        g.step()
        if tick in SNAPSHOTS:banks[str(tick)]=g.theta.copy()
    validation={n:{regime:{k:float(np.mean([assess(theta,seed+30000+i,regime)[k]
                              for i in range(2)])) for k in ('score','floor')}
                    for regime in ('stable','mild')}
                for n,theta in banks.items()}
    composite={n:float(np.mean([v[regime]['score']
                                 for regime in ('stable','mild')]))
               for n,v in validation.items()}
    best=max(banks,key=lambda n:composite[n])
    regular=best if composite[best]-composite['protected']>.005 else 'protected'
    safe=[n for n,v in validation.items()
          if all(v[regime]['floor']<=validation['protected'][regime]['floor']+.01
                 for regime in ('stable','mild'))
          and composite[n]>composite['protected']+.005]
    guarded=max(safe,key=lambda n:composite[n]) if safe else 'protected'
    testing={regime:{name:[assess(theta,seed+40000+i,regime)
                          for i in range(2)] for name,theta in banks.items()}
             for regime in ('stable','mild')}
    return {'seed':seed,'selected_composite':regular,'selected_safety':guarded,
            'validation':validation,'testing':testing}

def run():
    rows=[one(s) for s in range(11200,11206)]
    summary={}
    for regime in ('stable','mild'):
        arms={}
        for mode in ('protected','latest','composite','safety'):
            vals=[];cohort_scores=[]
            for row in rows:
                name={'protected':'protected','latest':'1600',
                      'composite':row['selected_composite'],
                      'safety':row['selected_safety']}[mode]
                tests=row['testing'][regime][name]
                vals.extend(tests)
                cohort_scores.append(float(np.mean([v['score'] for v in tests])))
            arms[mode]={key:float(np.mean([x[key] for x in vals]))
                        for key in ('energy','floor','score')}
            arms[mode]['cohort_scores']=cohort_scores
        for mode in ('latest','composite','safety'):
            arms[mode]['paired_cohort_wins_vs_protected']=sum(
                a>b for a,b in zip(arms[mode]['cohort_scores'],arms['protected']['cohort_scores']))
        summary[regime]=arms
    return {'design':'MEMORY2_SAFETY_PLAN.md','rows':rows,'summary':summary,
            'sha256':hashlib.sha256((HERE/'MEMORY2_SAFETY_probe.py').read_bytes()).hexdigest()}

if __name__=='__main__':
    x=run()
    (HERE/'MEMORY2_SAFETY_results.json').write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x['summary'],indent=2))
