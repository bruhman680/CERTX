"""Fresh-world stress test of conclusions from one historical Living Garden."""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from NEXT_LIVING_switch_probe import simulate

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'NEXT_LIVING_validation_results.json'
SEEDS=list(range(9000,9012))
SCHEDULES={
    'fixed_early':{101:'fixed050'},
    'rescue_early':{101:'rescue'},
    'reverse_early':{101:'reverse'},
    'learn_then_rescue':{501:'rescue'},
}


def main():
    rows=[]
    for seed in SEEDS:
        parent=Garden(seed=seed,size=12,learning=True)
        for _ in range(100):parent.step()
        fp=parent.fingerprint()
        row={'seed':seed,'initial_checkpoint_fingerprint':fp,'policies':{}}
        for name,schedule in SCHEDULES.items():
            out=simulate(parent,schedule,horizon=5000)
            row['policies'][name]=out['final']
            assert out['start_fingerprint']==fp
        assert parent.fingerprint()==fp
        rows.append(row)
    summaries={}
    for name in SCHEDULES:
        energies=np.array([r['policies'][name]['energy'] for r in rows])
        floors=np.array([r['policies'][name]['floor'] for r in rows])
        summaries[name]={'energy':float(energies.mean()),'energy_sd_across_seeds':float(energies.std(ddof=1)),
                         'floor_fraction':float(floors.mean())}
    pairings={}
    for challenger in ('rescue_early','reverse_early','learn_then_rescue'):
        d=np.array([r['policies'][challenger]['energy']-r['policies']['fixed_early']['energy'] for r in rows])
        pairings[challenger]={'mean_difference':float(d.mean()),'wins':int(np.sum(d>0)),
                              'n_seeds':len(SEEDS),'sd':float(d.std(ddof=1))}
    payload={'status':'executed','seed_unit':'independent initial world',
             'fresh_seeds':SEEDS,'size':12,'start_tick':100,'horizon':5000,
             'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in
                ('garden.py','SOC_LONGITUDINAL_explore.py','NEXT_LIVING_switch_probe.py','NEXT_LIVING_validation.py')},
             'design':'12 fresh worlds, four policy intervention schedules each, paired by seed',
             'rows':rows,'summaries':summaries,'paired_vs_fixed':pairings,
             'warning':'These policies were chosen after one-world exploration, not preregistered. Low energy is not death; initial learned neural damage varies across seeds.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'means':summaries,'paired':pairings},indent=2))

if __name__=='__main__':main()
