"""Prospective independent audit on reserved seeds; frozen design in PLAN.

Runs the identical finalized implementation without source modifications or
reselection of rewards, checkpoints, policy modes, or seeds.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
from NEXT_ONLINE_probe import run

ROOT = Path(__file__).resolve().parent
SEEDS = tuple(range(9800, 9812))


def main():
    data = run(seeds=SEEDS, size=10, train_steps=1000, test_steps=3000,
               diag_steps=1500)
    assert len(data['rows']) == 12
    assert [x['seed'] for x in data['rows']] == list(SEEDS)
    assert all(x['same_initial_physics_rng'] for x in data['rows'])
    assert all(len(x['theta_evaluations']) == 8 for x in data['rows'])
    assert all(len(x['trajectory']) == 3 for x in data['rows'])
    assert not set(SEEDS).intersection(set(range(9600, 9612)))
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
            for f in ('NEXT_ONLINE_PLAN.md','NEXT_ONLINE_AUDIT_PLAN.md',
                      'NEXT_ONLINE_probe.py','NEXT_ONLINE_AUDIT_run.py',
                      'NEXT_WELFARE_study.py','NEXT_WELFARE_garden.py','garden.py')}
    data['audit']={'status':'executed','reserved_independent_seeds':SEEDS,
                   'main_study_seeds':tuple(range(9600,9612)),
                   'source_sha256':hashes,'python':platform.python_version(),
                   'numpy':np.__version__,
                   'same_initial_physical_and_action_rng':True,
                   'separate_deterministic_eval_regimes':['stable','mild'],
                   'caveat':'stochastic action streams may diverge because policy weights change; matched RNG draws and initial state isolate the update treatment, not identical realized actions'}
    dest=ROOT/'NEXT_ONLINE_AUDIT_results.json'
    dest.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('reserved independent audit completed',len(data['rows']),
          'online-minus-frozen stochastic',
          data['summary']['online_minus_frozen_energy_mean'],flush=True)


if __name__=='__main__':main()
