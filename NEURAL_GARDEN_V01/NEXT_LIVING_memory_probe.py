"""Does preserving recurrent state rescue original neural policy after a hiatus?"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from NEXT_LIVING_switch_probe import simulate

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'NEXT_LIVING_memory_results.json'
SEEDS=list(range(9200,9212))
ARMS={
    'rescue_all_the_way':({101:'rescue'},()),
    'restore_neural_memory':({101:'rescue',2501:'learned'},()),
    'restore_neural_reset_hidden':({101:'rescue',2501:'learned'},(2501,)),
}


def main():
    rows=[]
    for seed in SEEDS:
        initial=Garden(seed=seed,size=12,learning=True)
        for _ in range(100):initial.step()
        fp=initial.fingerprint()
        row={'seed':seed,'initial_fingerprint':fp,'arms':{}}
        for name,(schedule,resets) in ARMS.items():
            out=simulate(initial,schedule,horizon=5000,reset_modes=resets)
            row['arms'][name]=out['final']
        assert initial.fingerprint()==fp
        rows.append(row)
    summaries={}
    for name in ARMS:
        e=np.array([r['arms'][name]['energy'] for r in rows]);f=np.array([r['arms'][name]['floor'] for r in rows])
        summaries[name]={'mean_energy':float(e.mean()),'floor_fraction':float(f.mean())}
    deltas=np.array([r['arms']['restore_neural_memory']['energy']-r['arms']['restore_neural_reset_hidden']['energy'] for r in rows])
    result={'status':'executed','hypothesis':'Does recurrent hidden-state history, rather than preserved learned weights, help after switching back from manual rescue?',
            'seeds':SEEDS,'size':12,'start_tick':100,'switch_back_tick':2501,'horizon':5000,
            'rows':rows,'summary':summaries,
            'memory_minus_reset_mean':float(deltas.mean()),
            'memory_minus_reset_max_abs':float(np.max(np.abs(deltas))),
            'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
                for n in ('garden.py','SOC_LONGITUDINAL_explore.py','NEXT_LIVING_switch_probe.py','NEXT_LIVING_memory_probe.py')},
            'limitations':"The original neural weights were not updated during manual rescue; dormant hidden states are stale. Reset comparison isolates that stored hidden vector, not all forms of memory. This is a toy world's negative policy restoration test."}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'summaries':summaries,'memory_minus_reset':float(deltas.mean())},indent=2))

if __name__=='__main__':main()
