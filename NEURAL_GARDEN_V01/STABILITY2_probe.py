"""Per-cell trust-region test. See STABILITY2_PLAN.md; no canonical checkpoint writes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import train
from NEXT_WELFARE_garden import WelfareGarden

HERE=Path(__file__).parent
RADII=(0.025,0.10,0.40,1.00)


def metrics(g,tail,reference):
    delta=np.linalg.norm(g.theta-reference,axis=1)
    return {'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
            'resource':float(g.resource.mean()),'harvest':float(g.last_action.mean()),
            'raw_tail':float(np.mean(tail)),'theta_mean_distance':float(delta.mean()),
            'theta_max_distance':float(delta.max())}


def one(seed,size=10,training=1000,ticks=3000):
    initial=train('reserve_resource',seed,size,training)
    names=('frozen','online')+tuple(f'radius_{r:g}' for r in RADII)
    gs={name:WelfareGarden(seed=seed+20000,size=size,learning=name!='frozen',
          objective='reserve_resource',penalty=.3) for name in names}
    init_state=gs['frozen'].rng_action.bit_generator.state
    for name,g in gs.items():
        g.theta=initial.copy()
        if not np.array_equal(g.energy,gs['frozen'].energy) or not np.array_equal(g.resource,gs['frozen'].resource):
            raise AssertionError('unmatched physical state')
        if json.dumps(g.rng_action.bit_generator.state,sort_keys=True)!=json.dumps(init_state,sort_keys=True):
            raise AssertionError('unmatched action RNG')
    tails={name:[] for name in names}
    for t in range(1,ticks+1):
        growth=.055 if ticks//3<t<=2*ticks//3 else .06
        for name,g in gs.items():
            g.regrowth=growth
            g.step()
            if name.startswith('radius_'):
                bound=float(name.split('_',1)[1]);diff=g.theta-initial
                norm=np.linalg.norm(diff,axis=1)
                scale=np.minimum(1.,bound/np.maximum(norm,1e-15))
                g.theta=initial+diff*scale[:,None]
            if t>ticks-500:tails[name].append(float(g.last_raw.mean()))
    vals={name:metrics(g,tails[name],initial) for name,g in gs.items()}
    return {'seed':seed,'conditions':vals}


def main(seeds,training=1000,ticks=3000,size=10):
    rows=[one(seed,size,training,ticks) for seed in seeds]
    names=rows[0]['conditions'].keys()
    summary={}
    for name in names:
        v=[row['conditions'][name] for row in rows]
        summary[name]={key:float(np.mean([x[key] for x in v])) for key in v[0]}
        summary[name]['wins_vs_frozen']=sum(row['conditions'][name]['energy']>row['conditions']['frozen']['energy'] for row in rows)
        summary[name]['wins_vs_online']=sum(row['conditions'][name]['energy']>row['conditions']['online']['energy'] for row in rows)
    sources=('STABILITY2_PLAN.md','STABILITY2_probe.py','NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py')
    return {'design':{'seeds':list(seeds),'training':training,'ticks':ticks,'size':size,
            'radius':RADII,'status':'development' if seeds[0]<10400 else 'holdout',
            'holdout_reserved':list(range(10400,10408))},
            'sources_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in sources},
            'rows':rows,'summary':summary}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--holdout',action='store_true');p.add_argument('--quick',action='store_true')
    a=p.parse_args();seeds=range(10400,10408) if a.holdout else range(10300,10308)
    if a.quick:seeds=range(10300,10302)
    x=main(seeds,training=100 if a.quick else 1000,ticks=200 if a.quick else 3000,size=6 if a.quick else 10)
    target=HERE/('STABILITY2_holdout_results.json' if a.holdout else 'STABILITY2_results.json')
    if a.quick:target=HERE/'STABILITY2_smoke.json'
    target.write_text(json.dumps(x,indent=2)+'\n')
    for key,v in x['summary'].items():print(key,round(v['energy'],5),round(v['floor'],5),v['wins_vs_frozen'])
