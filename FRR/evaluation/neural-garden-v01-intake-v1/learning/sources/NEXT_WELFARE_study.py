"""Bounded, preregistered-in-code welfare-objective research and heldout controls."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
from garden import Garden
from NEXT_WELFARE_garden import WelfareGarden


OBJECTIVES=("raw","reserve","resource","reserve_resource")


class RuleGarden(Garden):
    def __init__(self,seed=7,size=10,rule="fixed50"):
        super().__init__(seed=seed,size=size,learning=False)
        self.rule=rule
        self.regrowth=.06

    def step(self):
        r=self.resource.copy();e=self.energy.copy()
        if self.rule=="fixed50": threshold=np.full(self.count,.5)
        elif self.rule=="rescue": threshold=np.where(e<.12,.485,.51)
        elif self.rule=="reverse": threshold=np.where(e<.12,.535,.51)
        elif self.rule=="neighbor":threshold=.51+.5*(self._neighbors(r)-r)
        else: raise ValueError(self.rule)
        action=(r>threshold).astype(float)
        nxt_r=np.clip(r+.08*(self._neighbors(r)-r)+self.regrowth*(1-r)
                      -.18*r*action,0.,1.)
        raw=.25*r*action-.03-.055*action+.008*(1-action)
        nxt_e=np.clip(e+raw,0.,1.)
        self.resource=nxt_r;self.energy=nxt_e;self.last_action=action.copy()
        self.tick+=1
        self._last={'tick':self.tick,'mean_energy':float(nxt_e.mean()),
                    'mean_resource':float(nxt_r.mean()),'harvest_rate':float(action.mean()),
                    'raw_drift':float(raw.mean()),'energy_floor':float(np.mean(nxt_e<=.01))}
        return self.metrics()


def score(g):
    return float(g.energy.mean()-.5*np.mean(g.energy<=.01))


def train(objective,seed,size,steps):
    g=WelfareGarden(seed=seed,size=size,learning=True,objective=objective,penalty=.3)
    for _ in range(steps):g.step()
    return g.theta.copy()


def trial(objective,seed,size,train_steps,test_steps,mode):
    theta=train(objective,seed,size,train_steps)
    testseed=seed+20_000
    if mode=="online": learn=True;det=False
    elif mode=="frozen_stochastic":learn=False;det=False
    elif mode=="frozen_deterministic":learn=False;det=True
    else:raise ValueError(mode)
    g=WelfareGarden(seed=testseed,size=size,learning=learn,objective=objective,
                    penalty=.3,deterministic=det)
    g.theta=theta.copy()
    rows=[]
    for t in range(1,test_steps+1):
        g.regrowth=.055 if test_steps//3 < t <=2*test_steps//3 else .06
        m=g.step()
        if t in (test_steps//3,2*test_steps//3,test_steps):
            rows.append({'tick':t,'energy':m['mean_energy'],'floor':m['energy_floor'],
                         'resource':m['mean_resource'],'raw':m['raw_drift']})
    return {'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
            'resource':float(g.resource.mean()),'score':score(g),
            'tail':rows,'mean_energy_weight':float(g.theta[:,1].mean())}


def rule_trial(rule,seed,size,test_steps):
    g=RuleGarden(seed=seed+20_000,size=size,rule=rule)
    rows=[]
    for t in range(1,test_steps+1):
        g.regrowth=.055 if test_steps//3 < t <=2*test_steps//3 else .06
        m=g.step()
        if t in (test_steps//3,2*test_steps//3,test_steps):
            rows.append({'tick':t,'energy':m['mean_energy'],'floor':m['energy_floor'],
                         'resource':m['mean_resource'],'raw':m['raw_drift']})
    return {'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
            'resource':float(g.resource.mean()),'score':score(g),'tail':rows}


def aggregate(rows):
    return {'n':len(rows),'mean_energy':float(np.mean([r['energy'] for r in rows])),
            'mean_floor':float(np.mean([r['floor'] for r in rows])),
            'mean_score':float(np.mean([r['score'] for r in rows])),
            'individual':rows}


def run(dev_seeds=range(9100,9104),holdout_seeds=range(9200,9212),
        dev_size=8,holdout_size=10,dev_steps=1200,test_steps=3000):
    # Selection is based ONLY on development seeds and a declared multiobjective
    # score. Holdout and comparators are never used to select reward shape.
    development={}
    for objective in OBJECTIVES:
        vals=[trial(objective,s,dev_size,800,dev_steps,'online') for s in dev_seeds]
        development[objective]=aggregate(vals)
    selected=max(OBJECTIVES,key=lambda k:development[k]['mean_score'])
    armdefs=[(selected,'online'),(selected,'frozen_stochastic'),
             (selected,'frozen_deterministic'),('raw','online'),('raw','frozen_stochastic')]
    results={}
    for obj,mode in armdefs:
        key=obj+'__'+mode
        results[key]=aggregate([trial(obj,s,holdout_size,1000,test_steps,mode)
                                for s in holdout_seeds])
    for rule in ('fixed50','rescue','reverse','neighbor'):
        results['rule__'+rule]=aggregate([rule_trial(rule,s,holdout_size,test_steps)
                                        for s in holdout_seeds])
    named={r['seed']:r for r in []}  # no independent-cell replication; per-seed rows above.
    return {'design':{'development_seeds':list(dev_seeds),'holdout_seeds':list(holdout_seeds),
                      'development_size':dev_size,'holdout_size':holdout_size,
                      'development_test_steps':dev_steps,'holdout_test_steps':test_steps,
                      'train_steps_holdout':1000,'regrowth_schedule':'normal third, 0.055 middle third, normal final third',
                      'score':'mean_energy - 0.5 * fraction_energy_le_0.01',
                      'selected_from_development_only':True,
                      'rule_comparators':{'rescue':'r>.51 or (e<.12 and r>.485)',
                           'reverse':'r>.51 if e>=.12 else r>.535',
                           'neighbor':'r>.51+.5*(neighbor_resource-r)',
                           'fixed50':'r>.50'},
                      'no_teacher':True,'modified_world':'regrowth only, explicitly exogenous'},
            'selected_objective':selected,'development':development,'holdout':results,
            'platform':{'python':platform.python_version(),'numpy':np.__version__},
            'sha256':{f:hashlib.sha256((Path(__file__).parent/f).read_bytes()).hexdigest()
                      for f in ('garden.py','SOC_ENERGY_AWARE_policy.py',
                                'NEXT_WELFARE_garden.py',Path(__file__).name)},
            'caveats':['hypothesis family and coefficient choices are designed',
                       'development selection biases its scores; holdout is same generator',
                       'frozen deterministic vs online stochastic confounds exploration',
                       'no indefinite sustainability or real-world welfare inference']}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--quick',action='store_true')
    p.add_argument('--output',default=str(Path(__file__).with_name('NEXT_WELFARE_results.json')))
    a=p.parse_args()
    kwargs=({'dev_seeds':range(9100,9102),'holdout_seeds':range(9200,9203),
             'dev_size':6,'holdout_size':8,'dev_steps':250,'test_steps':500}
            if a.quick else {})
    z=run(**kwargs)
    Path(a.output).write_text(json.dumps(z,indent=2)+'\n')
    print('selected',z['selected_objective'])
    for arm,val in z['holdout'].items():
        print(arm,round(val['mean_energy'],5),round(val['mean_floor'],5),round(val['mean_score'],5))
