"""Independent gradient/ecology mechanism probe for NEXT_ONLINE frozen design.

Does continued online learning change action *placement* or harvest frequency,
especially when resource regeneration is reduced? Measure actual updates,
expected counterfactual one-step shaped reward, preclip energy and covariance.
Reserved audit seeds 9800-9811 are deliberately NOT used.
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
SEEDS=list(range(10080,10092))
OBJECTIVE='reserve_resource'; PENALTY=.3; SIZE=10; TRAIN=1000; TEST=3000
WINDOWS=(('baseline',1,1000),('early_scarcity',1001,1200),
         ('late_scarcity',1201,2000),('early_recovery',2001,2200),
         ('late_recovery',2201,3000))


def expected_reward_advantage(g,r,e):
    """Exact shaped immediate reward(harvest=1)-reward(rest=0)."""
    # Counterfactual actions face same current resource, energy and neighbors.
    neigh=g._neighbors(r)
    next_r0=np.clip(r+.08*(neigh-r)+g.regrowth*(1-r),0,1)
    next_r1=np.clip(next_r0-.18*r,0,1)
    raw0=np.full(g.count,-.022)
    raw1=.25*r-.085
    next_e0=np.clip(e+raw0,0,1)
    next_e1=np.clip(e+raw1,0,1)
    reward0=raw0-PENALTY*np.maximum(.18-next_e0,0)+PENALTY*(next_r0-r)
    reward1=raw1-PENALTY*np.maximum(.18-next_e1,0)+PENALTY*(next_r1-r)
    return reward1-reward0


def one_tick(g):
    r=g.resource.copy();e=g.energy.copy();theta=g.theta.copy()
    x=np.stack([3*(r-.5),3*(e-.5),np.ones(g.count)],axis=1)
    prop=g._sigmoid(np.sum(theta*x,axis=1))
    adv=expected_reward_advantage(g,r,e)
    raw_adv=.25*r-.063
    g.step()
    a=g.last_action
    delta_theta=g.theta-theta
    p=float(a.mean())
    return {
        'energy':float(g.energy.mean()),'floor':float(np.mean(g.energy<=.01)),
        'resource':float(g.resource.mean()),'harvest_rate':p,
        'propensity':float(prop.mean()),
        'resource_action_cov':float(np.mean(r*a)-r.mean()*p),
        'resource_propensity_cov':float(np.mean(r*prop)-r.mean()*prop.mean()),
        'resource_per_harvest':float(np.mean(r*a)/p) if p else None,
        'raw_drift':float(g.last_raw.mean()),
        'mean_shaped_reward_advantage':float(adv.mean()),
        'fraction_positive_shaped_reward_advantage':float(np.mean(adv>0)),
        'mean_raw_reward_advantage':float(raw_adv.mean()),
        'raw_positive_fraction':float(np.mean(raw_adv>0)),
        'resource_weight':float(g.theta[:,0].mean()),
        'energy_weight':float(g.theta[:,1].mean()),
        'bias_weight':float(g.theta[:,2].mean()),
        'resource_weight_update_mean':float(delta_theta[:,0].mean()),
        'energy_weight_update_mean':float(delta_theta[:,1].mean()),
        'bias_weight_update_mean':float(delta_theta[:,2].mean()),
        'update_abs_mean':float(np.mean(np.abs(delta_theta))),
    }


def summarize(ticks):
    names=ticks[0]
    return {k:float(np.mean([r[k] for r in ticks if r[k] is not None]))
            for k in names if all(r[k] is not None for r in ticks)}


def one_seed(seed):
    theta=train(OBJECTIVE,seed,SIZE,TRAIN)
    online=WelfareGarden(seed=seed+20000,size=SIZE,learning=True,
                         objective=OBJECTIVE,penalty=PENALTY)
    frozen=WelfareGarden(seed=seed+20000,size=SIZE,learning=False,
                         objective=OBJECTIVE,penalty=PENALTY)
    for g in (online,frozen):g.theta=theta.copy()
    assert np.array_equal(online.resource,frozen.resource)
    assert np.array_equal(online.energy,frozen.energy)
    assert np.array_equal(online.theta,frozen.theta)
    assert online.rng_action.bit_generator.state==frozen.rng_action.bit_generator.state
    records={name:{'online':[],'frozen':[]} for name,_,_ in WINDOWS}
    for t in range(1,TEST+1):
        phase=next((name for name,lo,hi in WINDOWS if lo<=t<=hi))
        for mode,g in (('online',online),('frozen',frozen)):
            g.regrowth=.055 if 1001<=t<=2000 else .06
            records[phase][mode].append(one_tick(g))
    windows={name:{mode:summarize(records[name][mode])
                   for mode in ('online','frozen')} for name,_,_ in WINDOWS}
    final={'online_energy':float(online.energy.mean()),
           'frozen_energy':float(frozen.energy.mean()),
           'online_floor':float(np.mean(online.energy<=.01)),
           'frozen_floor':float(np.mean(frozen.energy<=.01)),
           'online_theta':online.theta.mean(axis=0).tolist(),
           'frozen_theta':frozen.theta.mean(axis=0).tolist()}
    return {'seed':seed,'window_summary':windows,'final':final}


def run():
    rows=[one_seed(s) for s in SEEDS]
    ph={}
    keys=list(rows[0]['window_summary']['baseline']['online'])
    for name,_,_ in WINDOWS:
        ph[name]={}
        for mode in ('online','frozen'):
            ph[name][mode]={k:float(np.mean([row['window_summary'][name][mode][k]
                                             for row in rows])) for k in keys}
        ph[name]['online_minus_frozen']={k:ph[name]['online'][k]-ph[name]['frozen'][k] for k in keys}
    final=np.array([r['final']['online_energy']-r['final']['frozen_energy'] for r in rows])
    result={'status':'completed','objective':OBJECTIVE,'penalty':PENALTY,
      'seeds':SEEDS,'size':SIZE,'train_steps':TRAIN,'test_steps':TEST,
      'windows':WINDOWS,'independent_audit_seeds_untouched':list(range(9800,9812)),
      'exogenous_regrowth':'0.06 baseline,0.055 t1001–2000,0.06 t2001–3000',
      'mean_raw_harvest_advantage':'.25*resource-.063',
      'mean_nonreserve_shaped_harvest_advantage':'.196*resource-.063',
      'stationary_resource_budget':'mean_RA≈alpha/beta*(1-mean_resource) when global mean stationary',
      'rows':rows,'phase_summary':ph,
      'final_online_minus_frozen_mean':float(final.mean()),
      'final_online_wins':int(np.sum(final>0)),
      'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
             for name in ('garden.py','SOC_ENERGY_AWARE_policy.py',
                          'NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py',
                          'NEXT_ONLINE_probe.py',Path(__file__).name)},
      'versions':{'python':platform.python_version(),'numpy':np.__version__},
      'caveat':['Same synthetic generator and learning objective as NEXT_ONLINE, new seeds only',
                'Online and frozen trajectories diverge after learning changes, so covariance/harvest differences are observational mediators not separately randomized causes',
                'Raw action advantage is myopic; shaped exact advantage depends on energy clipping and reserve penalty',
                'Matched stochastic action mode does not guarantee identical actions after treatment diverges']}
    (ROOT/'NEXT_CREDIT_ECO_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Wrote NEXT_CREDIT_ECO_results.json with',len(rows),'seeds, mean energy delta',final.mean())
    for k in ph:
        x=ph[k]['online_minus_frozen']
        print(k,'harvest Δ',round(x['harvest_rate'],5),'cov Δ',round(x['resource_action_cov'],5),
              'resource Δ',round(x['resource'],5),'theta_bias Δ',round(x['bias_weight'],5),
              'raw Δ',round(x['raw_drift'],5))
    return result


if __name__=='__main__':run()
