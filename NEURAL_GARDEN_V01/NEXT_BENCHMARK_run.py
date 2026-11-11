"""Frozen-design cross-condition benchmark for six Garden policies.

Read NEXT_BENCHMARK_PLAN.md. Run once and do not change policies after seeing outcomes.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden

ROOT = Path(__file__).resolve().parent
SIZES = (8, 12, 16)
SEEDS = (33000, 33001, 33002, 33003)
REGIMES = ('stable', 'mild_regrowth', 'no_diffusion', 'shock')
POLICIES = ('fixed050', 'fixed051', 'energy_rescue', 'reverse_rescue',
            'neighbor_gradient', 'learned_energy')
CHECKPOINTS = (1000, 3000, 6000)


def neighbor(values: np.ndarray, size: int) -> np.ndarray:
    z = values.reshape(size, size)
    return ((np.roll(z, 1, 0) + np.roll(z, -1, 0)
             + np.roll(z, 1, 1) + np.roll(z, -1, 1)) / 4).reshape(-1)


def choose_action(policy, resource, energy, near_r, theta):
    if policy == 'fixed050': return resource > .50
    if policy == 'fixed051': return resource > .51
    if policy == 'energy_rescue':
        return (resource > .51) | ((energy < .12) & (resource > .485))
    if policy == 'reverse_rescue':
        return resource > np.where(energy < .12, .535, .51)
    if policy == 'neighbor_gradient':
        return resource > (.51 + .5 * (near_r - resource))
    if policy == 'learned_energy':
        obs = np.stack([3 * (resource - .5), 3 * (energy - .5),
                        np.ones_like(resource)], axis=1)
        return np.sum(theta * obs, axis=1) > 0.
    raise ValueError(policy)


def train_teacher_free(size, seed):
    g = EnergyAwareGarden(seed=25000 + (seed - 33000), size=size,
                          learning=True, energy_feature=True,
                          reward_mode='raw', lr=.04, trace_decay=.97)
    for _ in range(1200): g.step()
    return g.theta.copy()


def run_one(size, seed, regime, policy, theta, initial_resource, initial_energy):
    resource = initial_resource.copy()
    energy = initial_energy.copy()
    last_actions = []
    last_raw = []
    last_cov = []
    points = []
    for tick in range(1, 6001):
        near = neighbor(resource, size)
        action = choose_action(policy, resource, energy, near, theta).astype(float)
        regrowth = .055 if regime == 'mild_regrowth' and 501 <= tick <= 1500 else .06
        diffusion = 0. if regime == 'no_diffusion' else .08
        raw = .25 * resource * action - .03 - .055 * action + .008 * (1. - action)
        next_r = np.clip(resource + diffusion * (near - resource)
                         + regrowth * (1. - resource) - .18 * resource * action, 0., 1.)
        next_e = np.clip(energy + raw, 0., 1.)
        cov = float(np.mean(resource * action) - resource.mean() * action.mean())
        resource = next_r
        energy = next_e
        if regime == 'shock' and tick == 600: resource *= .70
        last_actions.append(float(action.mean()))
        last_raw.append(float(raw.mean()))
        last_cov.append(cov)
        if len(last_actions) > 100:
            last_actions.pop(0); last_raw.pop(0); last_cov.pop(0)
        if tick in CHECKPOINTS:
            points.append({
                'tick': tick, 'energy': float(energy.mean()),
                'floor': float(np.mean(energy <= .01)),
                'ceiling': float(np.mean(energy >= .99)),
                'lower_decile_energy': float(np.quantile(energy, .10)),
                'resource': float(resource.mean()),
                'harvest_tail_100': float(np.mean(last_actions)),
                'raw_drift_tail_100': float(np.mean(last_raw)),
                'resource_action_cov_tail_100': float(np.mean(last_cov)),
            })
    return {'size':size, 'seed':seed, 'regime':regime, 'policy':policy,
            'run_id':f'bench-{regime}-n{size}-s{seed}-{policy}', 'points':points}


def main():
    from datetime import datetime, timezone
    plan = (ROOT / 'NEXT_BENCHMARK_PLAN.md').read_bytes()
    source = {name:hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
              for name in ('garden.py','SOC_ENERGY_AWARE_policy.py',
                           'NEXT_BENCHMARK_run.py','NEXT_BENCHMARK_PLAN.md')}
    rows=[]
    training=[]
    for size in SIZES:
        for seed in SEEDS:
            # The training and test worlds are intentionally disjoint.
            theta=train_teacher_free(size,seed)
            training.append({'size':size,'train_seed':25000+(seed-33000),
                             'theta_sha256':hashlib.sha256(theta.tobytes()).hexdigest(),
                             'energy_coef_mean':float(theta[:,1].mean())})
            base=Garden(seed=seed,size=size,learning=False)
            init_r=base.resource.copy();init_e=base.energy.copy()
            for regime in REGIMES:
                for policy in POLICIES:
                    rows.append(run_one(size,seed,regime,policy,theta,init_r,init_e))
            print(f'completed size={size} seed={seed}; {len(rows)}/288 trajectories',flush=True)
    assert len(rows)==288 and len({r['run_id'] for r in rows})==288
    summary={}
    for regime in REGIMES:
        summary[regime]={}
        for tick in CHECKPOINTS:
            summary[regime][str(tick)]={}
            for policy in POLICIES:
                values=[pt for row in rows if row['regime']==regime and row['policy']==policy
                        for pt in row['points'] if pt['tick']==tick]
                summary[regime][str(tick)][policy]={k:float(np.mean([p[k] for p in values]))
                    for k in ('energy','floor','ceiling','lower_decile_energy','resource',
                              'harvest_tail_100','raw_drift_tail_100',
                              'resource_action_cov_tail_100')}
    payload={'status':'executed','description':'frozen-design cross-condition policy benchmark',
             'created_utc':datetime.now(timezone.utc).isoformat(),
             'plan_sha256':hashlib.sha256(plan).hexdigest(),
             'source_sha256':source,
             'platform':{'python':platform.python_version(),'numpy':np.__version__},
             'design':{'policies':POLICIES,'regimes':REGIMES,'sizes':SIZES,
                       'test_seeds':SEEDS,'checkpoints':CHECKPOINTS,
                       'training_ticks':1200,'test_ticks':6000,
                       'distinct_trajectories':288,
                       'nested_checkpoint_observations':864},
             'training':training,'summary':summary,'rows':rows,
             'caveats':['preselected policies, only four test seeds per size',
                        'same seed across regimes shares initial state but not exogenous trajectory',
                        'checkpoint observations of one trajectory are not independent',
                        'frozen deterministic learned policy is not online adaptive learning',
                        'finite horizons are not proof of infinite sustainability']}
    p=ROOT/'NEXT_BENCHMARK_results.json'
    p.write_text(json.dumps(payload,indent=2)+'\n')
    print('saved',p,'plan_sha',payload['plan_sha256'])

if __name__=='__main__':main()
