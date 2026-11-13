"""Two-bank policy consolidation using a separate training world and validation gate.

Immutable design MEMORY2_PLAN.md; executed outcomes MEMORY2_results.json.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import WelfareGarden, train

HERE=Path(__file__).parent
SNAPSHOTS=(400,800,1200,1600)

def assess(theta,seed,regime,ticks=1800):
    g=WelfareGarden(seed=seed,size=8,learning=False,deterministic=True,
                    objective='reserve_resource',penalty=.3)
    g.theta=theta.copy()
    for t in range(1,ticks+1):
        g.regrowth=.055 if regime=='mild' and ticks//3<t<=2*ticks//3 else .06
        g.step()
    energy=float(g.energy.mean());floor=float(np.mean(g.energy<=.01))
    return {'energy':energy,'floor':floor,'score':energy-.5*floor}

def one(seed):
    base=train('reserve_resource',seed,8,800)
    candidate=WelfareGarden(seed=seed+10000,size=8,learning=True,
                            objective='reserve_resource',penalty=.3)
    candidate.theta=base.copy()
    banks={'protected':base.copy()}
    for tick in range(1,1601):
        candidate.regrowth=.055 if 534<tick<=1067 else .06
        candidate.step()
        if tick in SNAPSHOTS:banks[str(tick)]=candidate.theta.copy()
    choices=list(banks)
    validation={}
    for name,theta in banks.items():
        validation[name]=float(np.mean([
            assess(theta,seed+30000+i,regime)['score']
            for i in range(2) for regime in ('stable','mild')]))
    best=max(choices,key=lambda key:validation[key])
    selected=best if validation[best]-validation['protected']>.005 else 'protected'
    holdout={regime:{name:[assess(theta,seed+40000+i,regime)
                                for i in range(2)]
                     for name,theta in banks.items()}
             for regime in ('stable','mild')}
    return {'seed':seed,'validation':validation,'selected':selected,
            'best_validation':best,'heldout':holdout}

def run():
    rows=[one(s) for s in range(11000,11006)]
    summary={'selection_counts':{n:sum(r['selected']==n for r in rows)
                                 for n in ('protected',*[str(s) for s in SNAPSHOTS])},
             'regimes':{}}
    for regime in ('stable','mild'):
        arm={}
        for label in ('protected','latest','selected','oracle'):
            scores=[]; energies=[];floors=[];wins=0
            for row in rows:
                scores0={k:float(np.mean([x['score'] for x in vals]))
                         for k,vals in row['heldout'][regime].items()}
                chosen={'protected':'protected','latest':'1600',
                        'selected':row['selected'],'oracle':max(scores0,key=scores0.get)}[label]
                vals=row['heldout'][regime][chosen]
                scores.extend(x['score'] for x in vals)
                energies.extend(x['energy'] for x in vals)
                floors.extend(x['floor'] for x in vals)
                if scores0[chosen]>scores0['protected']:wins+=1
            arm[label]={'mean_score':float(np.mean(scores)),
                        'mean_energy':float(np.mean(energies)),
                        'mean_floor':float(np.mean(floors)),
                        'cohort_score_wins_vs_protected':wins}
        summary['regimes'][regime]=arm
    return {'design':'MEMORY2_PLAN.md','snapshots':SNAPSHOTS,'rows':rows,
            'summary':summary,
            'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest()
                             for f in ('MEMORY2_probe.py','NEXT_WELFARE_garden.py',
                                       'NEXT_WELFARE_study.py')}}

if __name__=='__main__':
    out=run()
    (HERE/'MEMORY2_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['summary'],indent=2))
