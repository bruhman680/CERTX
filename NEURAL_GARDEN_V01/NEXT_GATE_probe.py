"""Preregistered update-timing gates: matched seeds and learning opportunities."""
from __future__ import annotations
import argparse,hashlib,json,platform
from pathlib import Path
import numpy as np
from NEXT_GATE_garden import GateGarden
from NEXT_WELFARE_study import WelfareGarden,RuleGarden,train

ROOT=Path(__file__).parent
NAMES=('online_all','gate_scarcity','gate_sham','gate_recovery','frozen_all')

def metrics(g,tail):
    return {'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
            'resource':float(g.resource.mean()),'harvest':float(g.last_action.mean()),
            'raw_tail':float(np.mean(tail)) if tail else None,
            'mean_energy_weight':float(np.mean(g.theta[:,1])) if hasattr(g,'theta') else None}

def eval_theta(theta,seed,size,ticks,regime):
    g=WelfareGarden(seed=seed+40000,size=size,learning=False,
                    deterministic=True,objective='reserve_resource',penalty=.3)
    g.theta=theta.copy();raw=[]
    for t in range(1,ticks+1):
        g.regrowth=.055 if regime=='mild' and ticks//3<t<=2*ticks//3 else .06
        g.step()
        if t>ticks-300:raw.append(float(g.last_raw.mean()))
    return metrics(g,raw)

def one_seed(seed,size=10,train_steps=1000,test_steps=3000,eval_steps=1500):
    theta=train('reserve_resource',seed,size,train_steps)
    worlds={name:GateGarden(seed=seed+20000,size=size,mode=name) for name in NAMES}
    manual=RuleGarden(seed=seed+20000,size=size,rule='reverse')
    for g in worlds.values():g.theta=theta.copy()
    anchor=worlds['frozen_all']
    for name,g in worlds.items():
        if not (np.array_equal(g.energy,anchor.energy) and
                np.array_equal(g.resource,anchor.resource) and
                np.array_equal(g.theta,anchor.theta) and
                json.dumps(g.rng_action.bit_generator.state,sort_keys=True)==
                json.dumps(anchor.rng_action.bit_generator.state,sort_keys=True)):
            raise AssertionError('unmatched '+name)
    records={name:[] for name in (*NAMES,'manual_reverse')}
    tails={name:[] for name in NAMES}
    for t in range(1,test_steps+1):
        regrowth=.055 if test_steps//3<t<=2*test_steps//3 else .06
        for name,g in worlds.items():
            g.regrowth=regrowth;g.step()
            if t>test_steps-500:tails[name].append(float(g.last_raw.mean()))
        manual.regrowth=regrowth;manual.step()
        if t in (1000,2000,3000):
            for name,g in worlds.items():records[name].append({'tick':t,**metrics(g,tails[name])})
            records['manual_reverse'].append({'tick':t,**metrics(manual,[])})
    return {'seed':seed,'matched_initial':True,'checkpoints':records,
            'final':{**{name:metrics(g,tails[name]) for name,g in worlds.items()},
                     'manual_reverse':metrics(manual,[])},
            'deterministic_theta_eval':{name:{regime:eval_theta(g.theta,seed,size,eval_steps,regime)
                                               for regime in ('stable','mild')}
                                        for name,g in worlds.items()}}

def summarize(rows):
    names=(*NAMES,'manual_reverse');out={}
    for name in names:
        out[name]={k:float(np.mean([r['final'][name][k] for r in rows]))
                   for k in ('energy','floor','resource','harvest')}
        if name in NAMES:
            out[name]['raw_tail']=float(np.mean([r['final'][name]['raw_tail'] for r in rows]))
            out[name]['deterministic_theta_eval']={regime:{k:float(np.mean([
                r['deterministic_theta_eval'][name][regime][k] for r in rows]))
                for k in ('energy','floor','resource')} for regime in ('stable','mild')}
            out[name]['paired_minus_sham_energy']=float(np.mean([
                r['final'][name]['energy']-r['final']['gate_sham']['energy'] for r in rows]))
            out[name]['paired_vs_sham_wins']=sum(r['final'][name]['energy']>
                r['final']['gate_sham']['energy'] for r in rows)
    return out

def run(seeds=range(10100,10112),size=10,train_steps=1000,test_steps=3000,eval_steps=1500):
    rows=[one_seed(s,size,train_steps,test_steps,eval_steps) for s in seeds]
    return {'design':{'plan':'NEXT_GATE_PLAN.md','seeds':list(seeds),'size':size,
                     'pretrain_ticks':train_steps,'test_ticks':test_steps,
                     'diagnostic_frozen_eval_ticks':eval_steps,'arms':NAMES,
                     'manual':'reverse','regrowth':'.06/.055/.06 equal thirds',
                     'theta_only_gate':True,'trace_baseline_always_update':True},
            'platform':{'python':platform.python_version(),'numpy':np.__version__},
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                    for f in ('garden.py','NEXT_WELFARE_garden.py','NEXT_CREDIT_garden.py',
                              'NEXT_GATE_garden.py',Path(__file__).name)},
            'rows':rows,'summary':summarize(rows)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true')
    p.add_argument('--output',default=str(ROOT/'NEXT_GATE_results.json'))
    a=p.parse_args()
    kw={'seeds':range(11100,11102),'size':6,'train_steps':100,'test_steps':3000,
        'eval_steps':150} if a.quick else {}
    result=run(**kw)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print('completed',len(result['rows']),'seeds')
    for name,val in result['summary'].items():print(name,round(val['energy'],5),round(val['floor'],5))
