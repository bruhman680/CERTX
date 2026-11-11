"""Causal parameter-update ablation within the online welfare-policy experiment.

Every arm begins with exact same physical state, theta, RNG and selected reward.
An intervention restores one coefficient after each normal online update, so
stochastic action paths subsequently diverge; it is a component intervention,
not a full mediation proof. Original Garden physics unchanged except named
mild regrowth dip.
"""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from NEXT_WELFARE_garden import WelfareGarden
from NEXT_WELFARE_study import train

ROOT=Path(__file__).parent
SEEDS=list(range(10180,10192)); ARMS=('online','frozen','freeze_bias','freeze_energy','freeze_resource')

def one_seed(seed,size=10,train_steps=1000,test_steps=3000):
    theta=train('reserve_resource',seed,size,train_steps)
    models={arm:WelfareGarden(seed=seed+20000,size=size,learning=(arm!='frozen'),
                             objective='reserve_resource',penalty=.3)
            for arm in ARMS}
    for g in models.values():g.theta=theta.copy()
    anchor=models['online']
    for arm,g in models.items():
        assert np.array_equal(g.energy,anchor.energy) and np.array_equal(g.resource,anchor.resource)
        assert np.array_equal(g.theta,anchor.theta)
        assert g.rng_action.bit_generator.state==anchor.rng_action.bit_generator.state
    checkpoints={arm:[] for arm in ARMS};tail={arm:[] for arm in ARMS}
    for t in range(1,test_steps+1):
        for arm,g in models.items():
            g.regrowth=.055 if 1000<t<=2000 else .06
            before=g.theta.copy()
            g.step()
            if arm=='freeze_bias':g.theta[:,2]=before[:,2]
            elif arm=='freeze_energy':g.theta[:,1]=before[:,1]
            elif arm=='freeze_resource':g.theta[:,0]=before[:,0]
            if t>2500:
                a=g.last_action;r=g.resource
                tail[arm].append({'harvest':float(a.mean()),'raw':float(g.last_raw.mean()),
                                  'floor':float((g.energy<=.01).mean()),
                                  'resource':float(r.mean())})
            if t in (1000,2000,3000):
                checkpoints[arm].append({'tick':t,'energy':float(g.energy.mean()),
                    'floor':float((g.energy<=.01).mean()),
                    'resource':float(g.resource.mean()),
                    'harvest':float(g.last_action.mean()),
                    'theta_mean':g.theta.mean(axis=0).tolist()})
    out={}
    for arm,g in models.items():
        out[arm]={'energy':float(g.energy.mean()),
                  'floor':float((g.energy<=.01).mean()),
                  'resource':float(g.resource.mean()),
                  'theta_mean':g.theta.mean(axis=0).tolist(),
                  'checkpoints':checkpoints[arm],
                  'tail':{k:float(np.mean([x[k] for x in tail[arm]]))
                          for k in ('harvest','raw','floor','resource')}}
    return {'seed':seed,'results':out}

def run():
    rows=[one_seed(s) for s in SEEDS]
    summary={}
    for arm in ARMS:
        summary[arm]={k:float(np.mean([r['results'][arm][k] for r in rows]))
                      for k in ('energy','floor','resource')}
        summary[arm]['tail']={k:float(np.mean([r['results'][arm]['tail'][k] for r in rows]))
                              for k in ('harvest','raw','floor','resource')}
    paired={}
    for arm in ARMS[1:]:
        d=np.array([r['results']['online']['energy']-r['results'][arm]['energy'] for r in rows])
        paired[arm]={'mean_online_minus_arm':float(d.mean()),
                     'sd_seed':float(d.std(ddof=1)),
                     'online_wins':int(np.sum(d>0)),
                     'n':len(d)}
    result={'status':'completed',
            'design':'Parameter-component update inhibition; same training and stochastic action mode',
            'arms':ARMS,'seeds':SEEDS,'train_steps':1000,'test_steps':3000,'size':10,
            'regrowth_schedule':'.06 1-1000, .055 1001-2000, .06 2001-3000',
            'objective':'reserve_resource','penalty':.3,
            'summary':summary,'paired':paired,'rows':rows,
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                              for f in ('garden.py','SOC_ENERGY_AWARE_policy.py',
                                        'NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py',
                                        Path(__file__).name)},
            'versions':{'python':platform.python_version(),'numpy':np.__version__},
            'caveats':['Component inhibition changes downstream policy state and trajectories',
                       'Online vs frozen comparison has same stochastic action-selection mode only initially',
                       'No guarantee improving a coefficient ablation generalizes beyond this selected synthetic world and reward']}
    (ROOT/'NEXT_CREDIT_ECO_ablation_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'summary':summary,'paired':paired},indent=2))
    return result

if __name__=='__main__':run()
