"""Extend the fixed-threshold shock test through 2,000 ticks.

External resource shocks occur exactly after ordinary ticks 200 and 400.
All ticks thereafter use the original, unmodified world equations.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from threshold_policy import ThresholdGarden


ROOT = Path(__file__).resolve().parent
SEEDS = range(820, 840)
THRESHOLDS = (.45, .55, .65)
TICKS = 2000
SHOCKS = (200, 400)
CHECK = {0, 100, 199, 200, 201, 400, 401, 600, 800, 1000, 1500, 2000}


def run_one(seed, threshold, shock):
    world = ThresholdGarden(seed=seed, threshold=threshold)
    initial = float(world.energy.mean())
    traces = [{'tick':0,'energy':initial,'resource':float(world.resource.mean())}]
    for _ in range(TICKS):
        world.step()
        if shock and world.tick in SHOCKS:
            world.resource *= .4
        if world.tick in CHECK:
            traces.append({'tick':world.tick, 'energy':float(world.energy.mean()),
                           'resource':float(world.resource.mean()),
                           'floor_fraction':float((world.energy <= .01).mean())})
    return {'seed':seed,'threshold':threshold,'shocks':shock,'checkpoints':traces,
            'final_energy':float(world.energy.mean()), 'final_resource':float(world.resource.mean())}


def run():
    rows = [run_one(seed, threshold, shock) for threshold in THRESHOLDS
            for seed in SEEDS for shock in (False, True)]
    out = {'design':'follow-up selected posthoc from initial shock pilot',
           'runs':rows,'run_count':len(rows),'ticks':TICKS,'size':16,
           'shock_ticks':SHOCKS,'shock_multiplier':.4,'seeds':list(SEEDS),
           'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                            for f in ('garden.py','threshold_policy.py','PERTURBATION_longhorizon.py')}}
    by_policy = {}
    for threshold in THRESHOLDS:
        for shock in (False,True):
            subset = [r for r in rows if r['threshold']==threshold and r['shocks']==shock]
            by_policy[f'{threshold}_shocks_{shock}'] = {str(t):float(np.mean(
                [next(c['energy'] for c in row['checkpoints'] if c['tick']==t) for row in subset]))
                for t in (600,800,1000,1500,2000)}
    out['summary_by_tick'] = by_policy
    (ROOT/'PERTURBATION_longhorizon_results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(by_policy, indent=2))


if __name__=='__main__':
    run()
