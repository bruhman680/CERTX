"""Precommitted independent long-horizon credit-mechanism audit.

Seeds and outcome burden fixed in NEXT_CREDIT_AUDIT_PLAN.md before viewing
NEXT_CREDIT outcomes; selected fast-baseline arm using ONLY development data.
"""
from __future__ import annotations
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from NEXT_CREDIT_garden import CreditGarden
from NEXT_WELFARE_study import RuleGarden, train

ROOT=Path(__file__).parent
SEEDS=tuple(range(9900,9908))
SIZE=10
TRAIN=1000
TICKS=8000
CONTROLLERS=('online_fast_baseline','online_raw','frozen_stochastic','reverse','neighbor')
CHECKPOINTS=(1000,2000,3000,5000,8000)

def measure(g,raws,floors):
    e=g.energy
    return {'energy':float(e.mean()),'floor':float(np.mean(e<=.01)),
            'bottom_decile':float(np.mean(np.sort(e)[:max(1,len(e)//10)])),
            'resource':float(g.resource.mean()),
            'tail_raw_drift':float(np.mean(raws[-500:])),
            'cumulative_floor':float(np.mean(floors)),
            'harvest':float(g.last_action.mean())}

def run_seed(seed,regime):
    theta=train('reserve_resource',seed,SIZE,TRAIN)
    worlds={
       'online_fast_baseline':CreditGarden(seed=seed+20000,size=SIZE,learning=True,
                         reward_observation='raw',trace_decay=.97,baseline_smoothing=.90),
       'online_raw':CreditGarden(seed=seed+20000,size=SIZE,learning=True,
                         reward_observation='raw',trace_decay=.97,baseline_smoothing=.995),
       'frozen_stochastic':CreditGarden(seed=seed+20000,size=SIZE,learning=False,
                         reward_observation='raw',trace_decay=.97,baseline_smoothing=.995),
       'reverse':RuleGarden(seed=seed+20000,size=SIZE,rule='reverse'),
       'neighbor':RuleGarden(seed=seed+20000,size=SIZE,rule='neighbor'),
    }
    for name in CONTROLLERS[:3]:worlds[name].theta=theta.copy()
    ref=worlds['frozen_stochastic']
    for name,g in worlds.items():
        assert np.array_equal(g.energy,ref.energy) and np.array_equal(g.resource,ref.resource),name
        if name in CONTROLLERS[:3]:
            assert np.array_equal(g.theta,ref.theta),name
            assert json.dumps(g.rng_action.bit_generator.state,sort_keys=True)==json.dumps(ref.rng_action.bit_generator.state,sort_keys=True),name
    raw={name:[] for name in CONTROLLERS}
    flo={name:[] for name in CONTROLLERS}
    checkpoints={name:{} for name in CONTROLLERS}
    for t in range(1,TICKS+1):
        rg=.055 if regime=='mild' and 1001<=t<=2000 else .06
        for name,g in worlds.items():
            g.regrowth=rg;g.step()
            raw[name].append(float(g.last_raw.mean()) if hasattr(g,'last_raw')
                              else float(g._last['raw_drift']))
            flo[name].append(float(np.mean(g.energy<=.01)))
        if t in CHECKPOINTS:
            for name,g in worlds.items():
                checkpoints[name][str(t)]=measure(g,raw[name],flo[name])
    # Competence check: online policies transferred, frozen, same fresh physical world.
    evaluation={}
    for name in CONTROLLERS[:3]:
        test=CreditGarden(seed=seed+40000,size=SIZE,learning=False)
        # CreditGarden always samples stochastically, so do not mistake this
        # for deterministic competence. Retain exact action-mode matching.
        test.theta=worlds[name].theta.copy()
        for t in range(1,1501):
            test.regrowth=.06;test.step()
        evaluation[name]={'energy':float(test.energy.mean()),
                          'floor':float(np.mean(test.energy<=.01))}
    return {'seed':seed,'regime':regime,'test_world_seed':seed+20000,
            'checkpoints':checkpoints,'final':{name:checkpoints[name][str(TICKS)] for name in CONTROLLERS},
            'frozen_same_stochastic_weight_evaluation':evaluation,
            'matched_initial_conditions':True}

def run():
    records=[run_seed(seed,regime) for regime in ('stable','mild') for seed in SEEDS]
    summary={}
    for regime in ('stable','mild'):
        rows=[x for x in records if x['regime']==regime]
        summary[regime]={name:{k:float(np.mean([r['final'][name][k] for r in rows]))
                 for k in ('energy','floor','bottom_decile','resource','tail_raw_drift','cumulative_floor')}
                 for name in CONTROLLERS}
        for name in CONTROLLERS:
            base='frozen_stochastic'
            paired=[r['final'][name]['energy']-r['final'][base]['energy'] for r in rows]
            summary[regime][name]['paired_energy_minus_frozen_mean']=float(np.mean(paired))
            summary[regime][name]['paired_energy_minus_frozen_wins']=int(sum(d>0 for d in paired))
    source=('garden.py','SOC_ENERGY_AWARE_policy.py','NEXT_WELFARE_garden.py',
            'NEXT_WELFARE_study.py','NEXT_CREDIT_garden.py','NEXT_CREDIT_probe.py',
            'NEXT_CREDIT_AUDIT_PLAN.md',Path(__file__).name)
    result={'design':{'predeclared_plan':'NEXT_CREDIT_AUDIT_PLAN.md',
       'selection':'online_fast_baseline maximizes energy−0.5*floor among changed online credit arms on 9700–9711 only',
       'seeds':SEEDS,'train_steps':TRAIN,'test_ticks':TICKS,'test_world_offset':20000,
       'mild_shift':'0.055 regrowth at t1001..2000, else 0.06',
       'matched_frozen_stochastic':True,'frozen_weight_evaluation_mode':'stochastic 1500 tick',
       'controls':CONTROLLERS},'rows':records,'summary':summary,
       'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source},
       'versions':{'python':platform.python_version(),'numpy':np.__version__}}
    (ROOT/'NEXT_CREDIT_AUDIT_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    z=run()
    for regime,v in z['summary'].items():
        print(regime)
        for name,s in v.items():print(name,round(s['energy'],5),round(s['floor'],5),round(s['tail_raw_drift'],7),s['paired_energy_minus_frozen_wins'])
