"""One policy-design research loop with 40 sequential optimizer iterations.

Each iteration proposes one parameter change from prior results, tests
it on fixed developmental seeds, and updates the design state. Optimizer
iterations, seeds, ticks and cells are NOT independent research loops.
A disjoint sealed holdout evaluates
the final selected policy only after the search. Toy-world results only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden
from threshold_policy import ThresholdGarden


PARAMS = ('trace_decay', 'lr', 'slope', 'start_low', 'start_high')
BOUNDS = {'trace_decay':(.0,.999), 'lr':(.00005,.006), 'slope':(3.,40.),
          'start_low':(.10,.55), 'start_high':(.45,.90)}
INITIAL = {'trace_decay':.97,'lr':.001,'slope':14.,
           'start_low':.25,'start_high':.75}
SCALES = {'trace_decay':.06,'lr':.0007,'slope':6.,
          'start_low':.09,'start_high':.09}


def policy_trial(cfg, seeds, train_steps=500, eval_steps=800):
    rows=[]
    for seed in seeds:
        g=AdaptiveThresholdGarden(seed=seed,size=8,learning=True,
                                  **cfg)
        initial=g.thresholds.copy()
        for _ in range(train_steps): g.step()
        test_seed=seed+20_000
        learned=AdaptiveThresholdGarden(seed=test_seed,size=8,learning=False,
                                       deterministic=True, **cfg)
        learned.thresholds=g.thresholds.copy()
        untrained=AdaptiveThresholdGarden(seed=test_seed,size=8,learning=False,
                                         deterministic=True, **cfg)
        untrained.thresholds=initial
        for _ in range(eval_steps):
            learned.step();untrained.step()
        rows.append({'seed':seed,'learner':float(learned.energy.mean()),
                     'untrained':float(untrained.energy.mean()),
                     'learner_floor':float(np.mean(learned.energy<=.01)),
                     'untrained_floor':float(np.mean(untrained.energy<=.01)),
                     'threshold_mean':float(g.thresholds.mean())})
    return {
      'mean_learner':float(np.mean([r['learner'] for r in rows])),
      'mean_untrained':float(np.mean([r['untrained'] for r in rows])),
      'mean_advantage':float(np.mean([r['learner']-r['untrained'] for r in rows])),
      'mean_floor':float(np.mean([r['learner_floor'] for r in rows])),
      'per_seed':rows}


def get_baseline(seeds, steps):
    rows=[]
    for seed in seeds:
        t=ThresholdGarden(seed=seed+20_000,size=8,threshold=.50)
        for _ in range(steps):t.step()
        rows.append({'seed':seed,'energy':float(t.energy.mean()),
                     'floor':float(np.mean(t.energy<=.01))})
    return {'energy':float(np.mean([r['energy'] for r in rows])),
            'floor':float(np.mean([r['floor'] for r in rows])),
            'per_seed':rows}


def candidate(parent, rng, iteration):
    # One-at-a-time causal move. Periodic reversals and scale changes prevent
    # declaring a local lucky improvement a law; selection remains exploratory.
    name=PARAMS[(iteration-1)%len(PARAMS)]
    sign=1 if ((iteration-1)//len(PARAMS))%2==0 else -1
    magnitudes=(1.,.5,1.5,.25)
    mag=magnitudes[((iteration-1)//(2*len(PARAMS)))%4]
    if iteration%13==0:sign=int(rng.choice([-1,1]))
    cfg=dict(parent)
    cfg[name]=float(np.clip(cfg[name]+sign*mag*SCALES[name],*BOUNDS[name]))
    if cfg['start_low']>=cfg['start_high']-.05:
        cfg[name]=parent[name]
    return name,sign,mag,cfg


def run(count=40):
    rng=np.random.default_rng(9017)
    development=[6100,6101,6102,6103]
    holdout=[7100+i for i in range(12)]
    current=dict(INITIAL)
    baseline=policy_trial(current,development)
    champion={'config':dict(current),'score':baseline['mean_learner'],
              'trial':baseline,'loop':0}
    history=[]
    for i in range(1,count+1):
        name,sign,mag,cfg=candidate(champion['config'],rng,i)
        prediction=f"Changing {name} by {'+' if sign>0 else '-'}{mag} scale will improve energy at t800 compared with champion"
        trial=policy_trial(cfg,development)
        delta=trial['mean_learner']-champion['score']
        accepted=delta>.0001
        history.append({'loop':i,'orientation':prediction,
                        'changed_parameter':name,'candidate':cfg,
                        'predecessor_score':champion['score'],
                        'observed_energy_delta':delta,
                        'evidence':trial,'accepted':accepted,
                        'next_orientation':('keep candidate and test a distinct variable' if accepted
                                            else 'reject move; test a different parameter or reversal')})
        if accepted:
            champion={'config':dict(cfg),'score':trial['mean_learner'],
                      'trial':trial,'loop':i}
    final=policy_trial(champion['config'],holdout)
    initial=policy_trial(INITIAL,holdout)
    fixed=get_baseline(holdout,800)
    payload={'design':{'optimizer_iterations_within_one_research_loop':count,
                       'training_seeds':development,'sealed_holdout_seeds':holdout,
                       'train_steps_per_seed':500,'evaluation_steps_per_seed':800,
                       'size':8,'not_counted_as_loops':['ticks','seeds','cells'],
                       'selection_rule':'accept if dev energy improves by >0.0001',
                       'full_train_eval_separation':'different initial worlds at eval; identical distribution, not distribution shift'},
             'platform':{'python':platform.python_version(),'numpy':np.__version__},
             'source_sha256':{name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                for name in ('garden.py','ADAPTIVE_threshold.py','threshold_policy.py',Path(__file__).name)},
             'development_start':baseline,'optimizer_iterations':history,
             'selected_champion':champion,
             'sealed_holdout':{'selected':final,'initial':initial,'fixed50':fixed},
             'caveat':'One research loop with 40 sequential hyperparameter-design iterations, not 40 independent research loops or discoveries; repeated developer-seed reuse creates selection bias. New holdout is same generator and not ecological generality.'}
    return payload


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--loops',type=int,default=40)
    p.add_argument('--output',default=str(Path(__file__).with_name('SOC_ADAPTIVE_results.json')))
    a=p.parse_args()
    if not 1<=a.loops<=40:raise SystemExit('loops must be 1–40')
    results=run(a.loops)
    Path(a.output).write_text(json.dumps(results,indent=2)+'\n')
    selected=results['sealed_holdout']['selected']['mean_learner']
    original=results['sealed_holdout']['initial']['mean_learner']
    fixed=results['sealed_holdout']['fixed50']['energy']
    print('Completed optimizer iterations within one research loop',a.loops,'champion',results['selected_champion']['config'])
    print('Sealed holdout energy selected',selected,'initial',original,'fixed50',fixed)
