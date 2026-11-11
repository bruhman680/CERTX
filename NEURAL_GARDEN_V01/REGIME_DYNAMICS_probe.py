"""Posthoc robustness probe for fixed resource-threshold ecology.

The explicit exogenous alpha/beta/kappa interventions CHANGE world laws and
must not be compared as neural intelligence. All runs are finite and seeded.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from threshold_policy import ThresholdGarden

ROOT=Path(__file__).resolve().parent
THRESHOLDS=(.48,.50,.51,.525,.55)
SEEDS=(1040,1041,1042,1043)
STEPS=5000
TAIL=1500
DEFAULT={'alpha':.06,'beta':.18,'kappa':.08}
REGIMES={
    'base':DEFAULT,
    'diffusion_zero':{**DEFAULT,'kappa':0.},
    'diffusion_half':{**DEFAULT,'kappa':.04},
    'diffusion_plus_half':{**DEFAULT,'kappa':.12},
    'regrowth_low':{**DEFAULT,'alpha':.045},
    'regrowth_high':{**DEFAULT,'alpha':.075},
    'consumption_low':{**DEFAULT,'beta':.15},
    'consumption_high':{**DEFAULT,'beta':.21},
}

class RegimeGarden(ThresholdGarden):
    def __init__(self,seed,threshold,**law):
        super().__init__(seed=seed,threshold=threshold)
        self.alpha=law['alpha'];self.beta=law['beta'];self.kappa=law['kappa']
    def step_moments(self):
        r=self.resource.copy();e=self.energy.copy()
        a=(r>self.threshold).astype(float)
        ra=float((r*a).mean()); p=float(a.mean());mean_r=float(r.mean())
        next_r=np.clip(r+self.kappa*(self._neighbors(r)-r)+self.alpha*(1-r)-self.beta*r*a,0,1)
        raw=.25*r*a-.063*a-.022
        next_e=np.clip(e+raw,0,1)
        self.resource=next_r;self.energy=next_e;self.last_action=a.copy();self.tick+=1
        return {'raw_drift':float(raw.mean()), 'resource':mean_r,'harvest':p,'resource_action':ra,
                'covariance':ra-mean_r*p,'resource_delta':float((next_r-r).mean()),
                'resource_budget_residual':float((next_r-r).mean()-self.alpha*(1-mean_r)+self.beta*ra),
                'energy':float(next_e.mean()),'floor':float((next_e<=.01).mean()),
                'ceiling':float((next_e>=.99).mean())}

def one(regime,threshold,seed):
    law=REGIMES[regime]
    g=RegimeGarden(seed=seed,threshold=threshold,**law)
    k=('raw_drift','resource','harvest','resource_action','covariance','resource_delta',
       'resource_budget_residual','energy','floor','ceiling')
    sums=dict.fromkeys(k,0.)
    points={0:float(g.energy.mean())}
    for t in range(STEPS):
        m=g.step_moments()
        if t>=STEPS-TAIL:
            for name in k:sums[name]+=m[name]
        if g.tick in (600,2000,5000):points[g.tick]=float(g.energy.mean())
    result={name:sums[name]/TAIL for name in k}
    result.update({'regime':regime,'law':law,'threshold':threshold,'seed':seed,
                   'energy_end':float(g.energy.mean()),'resource_end':float(g.resource.mean()),
                   'energy_points':points})
    result['energy_identity_error']=result['raw_drift']-(.25*result['resource_action']-.063*result['harvest']-.022)
    result['stationary_raw_approx']=.25*law['alpha']/law['beta']*(1-result['resource'])-.063*result['harvest']-.022
    return result

def run():
    rows=[]
    for regime in REGIMES:
        for th in THRESHOLDS:
            for seed in SEEDS:
                rows.append(one(regime,th,seed))
    summary={}
    for regime in REGIMES:
        summary[regime]={}
        for th in THRESHOLDS:
            rr=[r for r in rows if r['regime']==regime and r['threshold']==th]
            summary[regime][str(th)]={k:float(np.mean([r[k] for r in rr])) for k in
                                    ('energy_end','raw_drift','harvest','resource',
                                     'resource_action','covariance','floor','ceiling','resource_delta')}
    data={'design':'exploratory one-factor-at-a-time world-law perturbations; thresholds selected posthoc',
          'runs':len(rows),'steps':STEPS,'tail':TAIL,'seeds':SEEDS,'thresholds':THRESHOLDS,
          'regimes':REGIMES,'summary':summary,'rows':rows,
          'python':platform.python_version(),'numpy':np.__version__,
          'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
             ('garden.py','threshold_policy.py','REGIME_DYNAMICS_probe.py')}}
    (ROOT/'REGIME_DYNAMICS_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({regime:{threshold:{k:round(v[k],5) for k in ('energy_end','raw_drift','floor')}
                                for threshold,v in summary[regime].items()} for regime in summary},indent=2))

if __name__=='__main__':run()
