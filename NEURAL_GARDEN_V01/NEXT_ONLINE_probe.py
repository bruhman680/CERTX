"""Predeclared online-updating vs frozen-stochastic causal probe.

See NEXT_ONLINE_PLAN.md for the immutable scientific burden. Frozen source can
be invoked with different independent seeds by an external audit without edits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import WelfareGarden, train

HERE=Path(__file__).parent
OBJECTIVE='reserve_resource'
PENALTY=.3
CHECKPOINTS=(0,1000,2000,3000)


def vec_metrics(g,raw_tail):
    return {'energy':float(g.energy.mean()),
            'floor':float(np.mean(g.energy<=.01)),
            'ceiling':float(np.mean(g.energy>=.99)),
            'resource':float(g.resource.mean()),
            'harvest_rate':float(g.last_action.mean()),
            'mean_energy_weight':float(g.theta[:,1].mean()),
            'raw_tail':float(np.mean(raw_tail)) if raw_tail else None}


def evaluate_weights(theta,seed,size,regime,ticks):
    g=WelfareGarden(seed=seed+40000,size=size,learning=False,
                    deterministic=True,objective=OBJECTIVE,penalty=PENALTY)
    g.theta=theta.copy()
    raw=[]
    for t in range(1,ticks+1):
        g.regrowth=.055 if regime=='mild' and ticks//3<t<=2*ticks//3 else .06
        g.step()
        if t>ticks-300:raw.append(float(g.last_raw.mean()))
    return vec_metrics(g,raw)


def one_seed(seed, size=10, train_steps=1000, test_steps=3000, diag_steps=1500):
    theta=train(OBJECTIVE,seed,size,train_steps)
    testseed=seed+20000
    online=WelfareGarden(seed=testseed,size=size,learning=True,
                         objective=OBJECTIVE,penalty=PENALTY)
    frozen=WelfareGarden(seed=testseed,size=size,learning=False,
                         objective=OBJECTIVE,penalty=PENALTY)
    online.theta=theta.copy()
    frozen.theta=theta.copy()
    # Do not compare full object fingerprints: learning=True/False is the
    # deliberately varied treatment. All physical state and random streams
    # must match before the first learning update.
    same_initial=(np.array_equal(online.resource,frozen.resource)
                  and np.array_equal(online.energy,frozen.energy)
                  and np.array_equal(online.theta,frozen.theta)
                  and json.dumps(online.rng_action.bit_generator.state,sort_keys=True)
                      ==json.dumps(frozen.rng_action.bit_generator.state,sort_keys=True))
    if not same_initial:raise AssertionError('unmatched online/frozen initial worlds')
    snapshots={0:{'online':online.theta.copy(),'frozen':frozen.theta.copy()}}
    trajectory=[]
    tail_online=[];tail_frozen=[]
    for t in range(1,test_steps+1):
        regrowth=.055 if test_steps//3<t<=2*test_steps//3 else .06
        online.regrowth=regrowth;frozen.regrowth=regrowth
        online.step();frozen.step()
        if t>test_steps-500:
            tail_online.append(float(online.last_raw.mean()))
            tail_frozen.append(float(frozen.last_raw.mean()))
        if t in CHECKPOINTS:
            snapshots[t]={'online':online.theta.copy(),'frozen':frozen.theta.copy()}
            trajectory.append({'tick':t,'regrowth':regrowth,
                               'online':vec_metrics(online,tail_online),
                               'frozen':vec_metrics(frozen,tail_frozen)})
    evals=[]
    for cp in CHECKPOINTS:
        for regime in ('stable','mild'):
            a=evaluate_weights(snapshots[cp]['online'],seed,size,regime,diag_steps)
            b=evaluate_weights(snapshots[cp]['frozen'],seed,size,regime,diag_steps)
            evals.append({'checkpoint':cp,'eval_regime':regime,
                          'online_trained_theta':a,'frozen_theta':b,
                          'energy_update_advantage':a['energy']-b['energy'],
                          'floor_update_advantage':b['floor']-a['floor']})
    return {'seed':seed,'same_initial_physics_rng':same_initial,
            'trajectory':trajectory,
            'online_final':vec_metrics(online,tail_online),
            'frozen_final':vec_metrics(frozen,tail_frozen),
            'paired_online_minus_frozen_energy':float(online.energy.mean()-frozen.energy.mean()),
            'paired_online_minus_frozen_floor':float(np.mean(online.energy<=.01)-np.mean(frozen.energy<=.01)),
            'theta_evaluations':evals}


def summarize(rows):
    out={}
    for mode in ('online_final','frozen_final'):
        out[mode]={key:float(np.mean([r[mode][key] for r in rows]))
                   for key in ('energy','floor','ceiling','resource','harvest_rate','mean_energy_weight','raw_tail')}
    out['online_minus_frozen_energy_mean']=float(np.mean([r['paired_online_minus_frozen_energy'] for r in rows]))
    out['online_minus_frozen_energy_seed_sd']=float(np.std([r['paired_online_minus_frozen_energy'] for r in rows],ddof=1)) if len(rows)>1 else None
    out['online_energy_paired_wins']=sum(r['paired_online_minus_frozen_energy']>0 for r in rows)
    out['online_minus_frozen_floor_mean']=float(np.mean([r['paired_online_minus_frozen_floor'] for r in rows]))
    out['deterministic_eval']={}
    for cp in CHECKPOINTS:
        for regime in ('stable','mild'):
            a=[e for r in rows for e in r['theta_evaluations'] if e['checkpoint']==cp and e['eval_regime']==regime]
            out['deterministic_eval'][f'{cp}/{regime}']={
                'online_weight_energy':float(np.mean([e['online_trained_theta']['energy'] for e in a])),
                'frozen_weight_energy':float(np.mean([e['frozen_theta']['energy'] for e in a])),
                'mean_delta_energy':float(np.mean([e['energy_update_advantage'] for e in a])),
                'seed_wins':sum(e['energy_update_advantage']>0 for e in a),
                'online_weight_floor':float(np.mean([e['online_trained_theta']['floor'] for e in a])),
                'frozen_weight_floor':float(np.mean([e['frozen_theta']['floor'] for e in a]))}
    return out


def run(seeds=range(9600,9612),size=10,train_steps=1000,test_steps=3000,diag_steps=1500):
    rows=[one_seed(seed,size,train_steps,test_steps,diag_steps) for seed in seeds]
    return {'design':{'burden':'NEXT_ONLINE_PLAN.md',
                     'train_seeds':list(seeds),
                     'independent_audit_seeds_reserved':list(range(9800,9812)),
                     'size':size,'train_steps':train_steps,'test_steps':test_steps,
                     'diagnostic_eval_steps':diag_steps,
                     'objective':OBJECTIVE,'penalty':PENALTY,
                     'test_regrowth':'0.06 first third, 0.055 middle third, 0.06 final third',
                     'learning_modes':'online and frozen both stochastic; deterministic only secondary diagnostic',
                     'predeclared_checkpoints':CHECKPOINTS,
                     'mode_distinction':'deterministic theta transfer uses separate equal initial worlds'},
            'platform':{'python':platform.python_version(),'numpy':np.__version__},
            'source_sha256':{f:hashlib.sha256((HERE/f).read_bytes()).hexdigest()
                             for f in ('garden.py','NEXT_WELFARE_garden.py',
                                       'NEXT_WELFARE_study.py',Path(__file__).name)},
            'rows':rows,'summary':summarize(rows)}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--quick',action='store_true')
    p.add_argument('--output',default=str(HERE/'NEXT_ONLINE_results.json'))
    a=p.parse_args()
    kwargs={'seeds':range(10600,10602),'size':6,'train_steps':100,
            'test_steps':3000,'diag_steps':150} if a.quick else {}
    z=run(**kwargs)
    Path(a.output).write_text(json.dumps(z,indent=2)+'\n')
    print('completed',len(z['rows']),'seeds',z['summary']['online_minus_frozen_energy_mean'])
