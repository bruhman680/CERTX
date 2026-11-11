"""Predeclared one-factor tests of REINFORCE reward/trace/baseline mechanisms."""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from NEXT_CREDIT_garden import CreditGarden
from NEXT_WELFARE_study import WelfareGarden,RuleGarden,train

ROOT=Path(__file__).parent
ARM_CONFIGS={
 'online_raw':dict(learning=True,reward_observation='raw',trace_decay=.97,baseline_smoothing=.995),
 'online_clipped':dict(learning=True,reward_observation='clipped',trace_decay=.97,baseline_smoothing=.995),
 'online_short_trace':dict(learning=True,reward_observation='raw',trace_decay=.70,baseline_smoothing=.995),
 'online_long_trace':dict(learning=True,reward_observation='raw',trace_decay=.995,baseline_smoothing=.995),
 'online_fast_baseline':dict(learning=True,reward_observation='raw',trace_decay=.97,baseline_smoothing=.90),
 'frozen_stochastic':dict(learning=False,reward_observation='raw',trace_decay=.97,baseline_smoothing=.995),
}
CHECKPOINTS=(1000,2000,3000)


def metrics(g,tail):
    return {'energy':float(g.energy.mean()),
            'floor':float(np.mean(g.energy<=.01)),
            'ceiling':float(np.mean(g.energy>=.99)),
            'resource':float(g.resource.mean()),
            'harvest':float(g.last_action.mean()),
            'raw_tail':float(np.mean(tail)) if tail else None,
            'energy_weight_mean':float(np.mean(g.theta[:,1])) if hasattr(g,'theta') else None}


def evaluate_theta(theta,seed,size,ticks,regime):
    g=WelfareGarden(seed=seed+40000,size=size,learning=False,
                    deterministic=True,objective='reserve_resource',penalty=.3)
    g.theta=theta.copy()
    raw=[]
    for t in range(1,ticks+1):
        g.regrowth=.055 if regime=='mild' and ticks//3<t<=2*ticks//3 else .06
        g.step()
        if t>ticks-300:raw.append(float(g.last_raw.mean()))
    return metrics(g,raw)


def one_seed(seed,size=10,train_steps=1000,test_steps=3000,eval_steps=1500):
    theta=train('reserve_resource',seed,size,train_steps)
    worlds={name:CreditGarden(seed=seed+20000,size=size,**cfg)
            for name,cfg in ARM_CONFIGS.items()}
    for g in worlds.values():g.theta=theta.copy()
    manual={name:RuleGarden(seed=seed+20000,size=size,rule=name)
            for name in ('fixed50','reverse')}
    example=worlds['frozen_stochastic']
    for name,g in worlds.items():
        if not (np.array_equal(g.energy,example.energy)
                and np.array_equal(g.resource,example.resource)
                and np.array_equal(g.theta,example.theta)
                and json.dumps(g.rng_action.bit_generator.state,sort_keys=True)
                    ==json.dumps(example.rng_action.bit_generator.state,sort_keys=True)):
            raise AssertionError('unmatched initial neural control '+name)
    tails={name:[] for name in worlds}
    records={name:[] for name in list(worlds)+list(manual)}
    for t in range(1,test_steps+1):
        regrowth=.055 if test_steps//3<t<=2*test_steps//3 else .06
        for name,g in worlds.items():
            g.regrowth=regrowth;g.step()
            if t>test_steps-500:tails[name].append(float(g.last_raw.mean()))
        for name,g in manual.items():
            g.regrowth=regrowth;g.step()
        if t in CHECKPOINTS:
            for name,g in worlds.items():records[name].append({'tick':t,**metrics(g,tails[name])})
            for name,g in manual.items():records[name].append({'tick':t,**metrics(g,[])})
    evaluations={name:{regime:evaluate_theta(g.theta,seed,size,eval_steps,regime)
                       for regime in ('stable','mild')}
                 for name,g in worlds.items()}
    return {'seed':seed,'matched_initial':True,'trajectories':records,
            'final_neural':{name:metrics(g,tails[name]) for name,g in worlds.items()},
            'final_manual':{name:metrics(g,[]) for name,g in manual.items()},
            'deterministic_theta_eval':evaluations}


def summarize(rows):
    allnames=list(ARM_CONFIGS)+['fixed50','reverse']
    out={}
    for name in allnames:
        observations=[(r['final_neural'] if name in ARM_CONFIGS else r['final_manual'])[name] for r in rows]
        out[name]={k:float(np.mean([v[k] for v in observations])) for k in ('energy','floor','resource','harvest')}
        if name in ARM_CONFIGS:
            out[name]['raw_tail']=float(np.mean([v['raw_tail'] for v in observations]))
            out[name]['deterministic_theta_eval']={}
            for regime in ('stable','mild'):
                vals=[r['deterministic_theta_eval'][name][regime] for r in rows]
                out[name]['deterministic_theta_eval'][regime]={
                    k:float(np.mean([v[k] for v in vals])) for k in ('energy','floor','resource')}
    base=out['online_raw']['energy']
    for name in ARM_CONFIGS:
        diffs=[r['final_neural'][name]['energy']-r['final_neural']['online_raw']['energy'] for r in rows]
        out[name]['paired_minus_online_raw_mean']=float(np.mean(diffs))
        out[name]['paired_minus_online_raw_wins']=sum(d>0 for d in diffs)
    return out


def run(seeds=range(9700,9712),size=10,train_steps=1000,test_steps=3000,eval_steps=1500):
    rows=[one_seed(seed,size,train_steps,test_steps,eval_steps) for seed in seeds]
    return {'design':{'plan':'NEXT_CREDIT_PLAN.md','seeds':list(seeds),'size':size,
                     'pretrain_ticks':train_steps,'test_ticks':test_steps,
                     'diagnostic_frozen_eval_ticks':eval_steps,
                     'arms':ARM_CONFIGS,
                     'manual_controls':['fixed50','reverse'],
                     'regrowth':'0.06 first third,0.055 middle third,0.06 last third',
                     'one_factor_ablations':True,'no_teacher_labels':True},
            'platform':{'python':platform.python_version(),'numpy':np.__version__},
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                for f in ('garden.py','NEXT_WELFARE_garden.py','NEXT_CREDIT_garden.py',Path(__file__).name)},
            'rows':rows,'summary':summarize(rows)}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--quick',action='store_true')
    p.add_argument('--output',default=str(ROOT/'NEXT_CREDIT_results.json'))
    a=p.parse_args()
    kwargs={'seeds':range(10700,10702),'size':6,'train_steps':100,
            'test_steps':3000,'eval_steps':150} if a.quick else {}
    result=run(**kwargs)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print('completed',len(result['rows']),'seeds')
    for name,val in result['summary'].items():
        print(name,round(val['energy'],5),round(val['floor'],5))
