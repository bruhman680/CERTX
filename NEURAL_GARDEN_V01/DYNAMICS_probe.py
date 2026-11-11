"""Posthoc dynamical probe of resource threshold policies under original laws.

Tracks exact raw energy budget, joint resource/action moments and mass-balance
residual; the finite trajectories do NOT establish mathematical attractors.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from threshold_policy import ThresholdGarden

ROOT = Path(__file__).resolve().parent
THRESHOLDS = (.45, .50, .525, .55, .575, .60)
SEEDS = range(930, 938)
STEPS = 5000
TAIL = 1500
CHECK = (0, 200, 600, 1000, 2000, 3500, 5000)


def one(seed, threshold):
    g = ThresholdGarden(seed=seed, threshold=threshold)
    traces = []
    tail = []
    def sample():
        R = g.resource.copy()
        A = (R > threshold).astype(float)
        raw = .25*R*A - .063*A - .022
        resource_next = R + .08*(g._neighbors(R)-R) + .06*(1-R) - .18*R*A
        return {
            'raw_drift':float(raw.mean()),
            'harvest':float(A.mean()),
            'resource':float(R.mean()),
            'resource_action':float((R*A).mean()),
            'covariance':float((R*A).mean()-R.mean()*A.mean()),
            'resource_delta':float((resource_next-R).mean()),
            'resource_budget_residual':float((resource_next-R).mean() - .06*(1-R.mean()) + .18*(R*A).mean()),
        }
    for t in range(STEPS+1):
        if t in CHECK:
            traces.append({'tick':t,'energy':float(g.energy.mean()),'resource':float(g.resource.mean()),
                           'floor':float((g.energy<=.01).mean()),'ceiling':float((g.energy>=.99).mean())})
        if t==STEPS:break
        m=sample()
        if t>=STEPS-TAIL:
            m['energy']=float(g.energy.mean())
            m['energy_floor']=float((g.energy<=.01).mean())
            tail.append(m)
        g.step()
    summary={k:float(np.mean([x[k] for x in tail])) for k in tail[0]}
    summary['energy_end']=float(g.energy.mean())
    summary['resource_end']=float(g.resource.mean())
    summary['seed']=seed
    summary['threshold']=threshold
    summary['trace']=traces
    summary['tail_resource_budget_identity_error']=float(summary['resource_delta'] - (.06*(1-summary['resource'])-.18*summary['resource_action']))
    summary['tail_energy_budget_identity_error']=float(summary['raw_drift'] - (.25*summary['resource_action']-.063*summary['harvest']-.022))
    summary['tail_stationary_energy_approx']=float((.25/3)*(1-summary['resource'])-.063*summary['harvest']-.022)
    return summary


def run():
    rows=[one(seed, threshold) for threshold in THRESHOLDS for seed in SEEDS]
    summary={str(v):{k:float(np.mean([r[k] for r in rows if r['threshold']==v])) for k in
                     ('energy_end','raw_drift','resource','harvest','resource_action','covariance',
                      'resource_delta','energy_floor','tail_resource_budget_identity_error',
                      'tail_energy_budget_identity_error','tail_stationary_energy_approx')}
             for v in THRESHOLDS}
    result={'design':'Posthoc model-specific long-horizon threshold grid, not confirmatory optimality test',
            'thresholds':THRESHOLDS,'seeds':list(SEEDS),'steps':STEPS,'tail_steps':TAIL,
            'size':16,'rows':rows,'summary':summary,'python_version':platform.python_version(),
            'numpy_version':np.__version__,'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                for f in ('garden.py','threshold_policy.py','DYNAMICS_probe.py')}}
    (ROOT/'DYNAMICS_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':run()
