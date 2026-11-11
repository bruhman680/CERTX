"""Severe regrowth-shift trust-bound and shuffled-gradient sham. See predeclared plan."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import train
from NEXT_WELFARE_garden import WelfareGarden

HERE=Path(__file__).parent
MODES=('frozen','online','radius_0.025','radius_0.1','sham_0.1')


def project(g,reference,bound):
    diff=g.theta-reference
    norm=np.linalg.norm(diff,axis=1)
    g.theta=reference+diff*np.minimum(1.,bound/np.maximum(norm,1.e-15))[:,None]


def one(seed,size=10,training=1000,ticks=3000):
    theta=train('reserve_resource',seed,size,training)
    worlds={name:WelfareGarden(seed=seed+20000,size=size,learning=name!='frozen',objective='reserve_resource',penalty=.3)
            for name in MODES}
    for name,g in worlds.items():
        g.theta=theta.copy()
        if not np.array_equal(g.energy,worlds['frozen'].energy) or not np.array_equal(g.resource,worlds['frozen'].resource):
            raise AssertionError('nonidentical initial physical fields')
        if json.dumps(g.rng_action.bit_generator.state,sort_keys=True)!=json.dumps(worlds['frozen'].rng_action.bit_generator.state,sort_keys=True):
            raise AssertionError('nonidentical initial action RNG')
    rng=np.random.default_rng(seed+800000)
    tails={name:[] for name in MODES};mid={name:[] for name in MODES};stage={name:[] for name in MODES}
    for t in range(1,ticks+1):
        growth=.03 if ticks//3<t<=2*ticks//3 else .09
        for name,g in worlds.items():
            g.regrowth=growth
            old=g.theta.copy() if name=='sham_0.1' else None
            g.step()
            if name=='sham_0.1':
                grad=g.theta-old
                g.theta=old+grad[rng.permutation(g.count)]
            if name.startswith('radius_'):
                project(g,theta,float(name.split('_',1)[1]))
            elif name=='sham_0.1':
                project(g,theta,.10)
            if t>ticks-500: tails[name].append(float(g.last_raw.mean()))
            if ticks//3<t<=2*ticks//3:mid[name].append(float(g.energy.mean()))
            if t in (ticks//3,2*ticks//3,ticks):stage[name].append({'tick':t,'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01))})
    return {'seed':seed,'conditions':{name:{'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
                'resource':float(g.resource.mean()),'raw_tail':float(np.mean(tails[name])),
                'scarcity_mean_energy':float(np.mean(mid[name])),
                'theta_mean_distance':float(np.linalg.norm(g.theta-theta,axis=1).mean()),'stage':stage[name]}
            for name,g in worlds.items()}}


def run(seeds,training=1000,ticks=3000,size=10):
    rows=[one(seed,size,training,ticks) for seed in seeds]
    summary={}
    for name in MODES:
        summary[name]={key:float(np.mean([r['conditions'][name][key] for r in rows])) for key in
            ('energy','floor','resource','raw_tail','scarcity_mean_energy','theta_mean_distance')}
        summary[name]['wins_vs_frozen']=sum(r['conditions'][name]['energy']>r['conditions']['frozen']['energy'] for r in rows)
        summary[name]['wins_vs_sham']=sum(r['conditions'][name]['energy']>r['conditions']['sham_0.1']['energy'] for r in rows)
    return {'design':{'seeds':list(seeds),'size':size,'training':training,'ticks':ticks,'regrowth':'0.09 then .03 then .09',
        'holdout_reserved':list(range(10600,10608))},
        'sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in ('STABILITY2_SHIFT_PLAN.md','STABILITY2_SHIFT_probe.py')},
        'rows':rows,'summary':summary}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--holdout',action='store_true');p.add_argument('--quick',action='store_true');a=p.parse_args()
    seeds=range(10600,10608) if a.holdout else range(10500,10508)
    if a.quick:seeds=range(10500,10502)
    z=run(seeds,training=100 if a.quick else 1000,ticks=300 if a.quick else 3000,size=6 if a.quick else 10)
    target='STABILITY2_SHIFT_holdout_results.json' if a.holdout else 'STABILITY2_SHIFT_results.json'
    if a.quick:target='STABILITY2_SHIFT_smoke.json'
    (HERE/target).write_text(json.dumps(z,indent=2)+'\n')
    for name,v in z['summary'].items():print(name,round(v['energy'],5),round(v['floor'],5),v['wins_vs_frozen'])
