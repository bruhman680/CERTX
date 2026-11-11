"""Matched external resource-shock experiment, separate from the original-law sweeps.

Exogenous shocks multiply the *post-step* resource field at designated ticks.
Between shocks the original Garden/ThresholdGarden step equations are unchanged.
This intervention is not claimed to be the original unperturbed world.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden
from threshold_policy import ThresholdGarden


ROOT = Path(__file__).resolve().parent
SEEDS = list(range(710, 730))
TICKS = 600
SIZE = 16
SHOCKS = (200, 400)
SHOCK_MULTIPLIER = .40
CHECKPOINTS = {0, 100, 199, 200, 201, 220, 250, 300, 399, 400, 401, 420, 450, 500, 600}


def make(policy: str, seed: int):
    if policy == 'neural_learning':
        return Garden(seed=seed, size=SIZE, learning=True)
    if policy == 'neural_frozen':
        return Garden(seed=seed, size=SIZE, learning=False)
    if policy.startswith('threshold_0'):
        return ThresholdGarden(seed=seed, size=SIZE, threshold=float('0.' + policy.split('_')[1][1:]))
    raise ValueError(policy)


def trial(policy: str, seed: int, shocks: bool):
    garden = make(policy, seed)
    checkpoints = []
    cumulative_harvest = 0.
    cumulative_covariance = 0.
    cumulative_raw_drift = 0.
    recovery = {t: None for t in SHOCKS}
    shock_baselines = {}
    postshock_energy = {t: None for t in SHOCKS}

    def snapshot():
        return {
            'tick': garden.tick,
            'mean_energy': float(garden.energy.mean()),
            'mean_resource': float(garden.resource.mean()),
            'energy_floor_fraction': float((garden.energy <= .01).mean()),
            'energy_ceiling_fraction': float((garden.energy >= .99).mean()),
            'harvest_rate': float(garden.last_action.mean()),
        }

    checkpoints.append(snapshot())
    for _ in range(TICKS):
        r = garden.resource.copy()
        garden.step()
        a = garden.last_action
        cumulative_covariance += float(np.mean((r-r.mean())*(a-a.mean())))
        cumulative_harvest += float(a.mean())
        cumulative_raw_drift += float((.25*r*a - .03 - .055*a + .008*(1-a)).mean())
        if shocks and garden.tick in SHOCKS:
            shock_baselines[garden.tick] = float(garden.resource.mean())
            garden.resource *= SHOCK_MULTIPLIER
            postshock_energy[garden.tick] = float(garden.energy.mean())
        for event in SHOCKS:
            if shocks and event in shock_baselines and recovery[event] is None and garden.tick > event:
                if float(garden.resource.mean()) >= shock_baselines[event]:
                    recovery[event] = garden.tick-event
        if garden.tick in CHECKPOINTS:
            record = snapshot()
            if shocks and garden.tick in SHOCKS:
                record['exogenous_shock_applied'] = True
                record['pre_shock_resource_mean'] = shock_baselines[garden.tick]
            checkpoints.append(record)
    return {
        'policy': policy, 'seed': seed, 'shocks': shocks,
        'checkpoints': checkpoints,
        'final_energy': float(garden.energy.mean()),
        'final_resource': float(garden.resource.mean()),
        'floor_fraction': float((garden.energy <= .01).mean()),
        'avg_harvest': cumulative_harvest/TICKS,
        'avg_cov_resource_action': cumulative_covariance/TICKS,
        'avg_raw_energy_drift': cumulative_raw_drift/TICKS,
        'recovery_to_pre_shock_resource_ticks': recovery,
        'energy_at_shock': postshock_energy,
    }


def aggregate(rows):
    summary = {}
    for policy in ('neural_learning', 'neural_frozen', 'threshold_045', 'threshold_055', 'threshold_065'):
        for shock in (False, True):
            vals = [r for r in rows if r['policy']==policy and r['shocks']==shock]
            summary[f'{policy}_{"shocked" if shock else "control"}'] = {
                'n': len(vals),
                **{k: {'mean': float(np.mean([v[k] for v in vals])),
                       'sample_sd': float(np.std([v[k] for v in vals], ddof=1))}
                   for k in ('final_energy','final_resource','floor_fraction','avg_harvest',
                             'avg_cov_resource_action','avg_raw_energy_drift')},
                'recovery_200': [v['recovery_to_pre_shock_resource_ticks'][200] for v in vals],
                'recovery_400': [v['recovery_to_pre_shock_resource_ticks'][400] for v in vals],
            }
    return summary


def run():
    source_paths = ('garden.py','threshold_policy.py','PERTURBATION_shock_pilot.py')
    sources = {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in source_paths}
    rows = [trial(policy, seed, shock) for policy in ('neural_learning','neural_frozen','threshold_045','threshold_055','threshold_065')
            for seed in SEEDS for shock in (False, True)]
    result = {
        'description': 'external resource loss, controlled matched-policy pilot',
        'laws': 'original laws within every step; exogenous post-step resource multiplier at 200/400',
        'status': 'pilot, nonconfirmatory',
        'seeds': SEEDS, 'size':SIZE, 'ticks':TICKS, 'shock_ticks':SHOCKS,
        'shock_resource_multiplier':SHOCK_MULTIPLIER, 'run_count':len(rows),
        'python':platform.python_version(), 'numpy':np.__version__,
        'source_sha256':sources, 'summary':aggregate(rows), 'runs':rows,
    }
    out = ROOT/'PERTURBATION_shock_results.json'
    out.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'output':str(out),'runs':len(rows),'summary':result['summary']}, indent=2))


if __name__=='__main__':
    run()
