"""Explicit energy/resource rescue at late policy switch, with full lineage."""

import copy
import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_LONGITUDINAL_explore import PolicyFork
from NEXT_LIVING_switch_probe import POLICIES, summarize

ROOT=Path(__file__).resolve().parent
CANONICAL=ROOT/'runs/living_world/state.pkl'
OUT=ROOT/'NEXT_LIVING_repair_results.json'
MODES=('none','resource_only','energy_only','both')


def run(anchor,mode,horizon=5000):
    g=copy.deepcopy(anchor)
    for _ in range(g.tick+1,501):g.step()
    pre=g.fingerprint()
    g=PolicyFork(g,POLICIES['rescue'])
    before={'energy':float(g.energy.mean()),'resource':float(g.resource.mean())}
    if mode in ('resource_only','both'):
        g.resource=np.clip(g.resource*2,0,1)
    if mode in ('energy_only','both'):
        g.energy=np.maximum(g.energy,.3)
    after={'energy':float(g.energy.mean()),'resource':float(g.resource.mean())}
    checkpoints={}
    raw=[]
    for _ in range(501,horizon+1):
        pre_r=g.resource.copy();g.step()
        a=g.last_action
        raw.append(float((.25*pre_r*a-.03-.055*a+.008*(1-a)).mean()))
        if g.tick in (600,1000,2000,3000,5000):
            checkpoints[g.tick]=summarize(g,raw[-500:])
    return {'mode':mode,'source_state_fingerprint_at_500':pre,
            'intervention_at_tick_500':{'before':before,'after':after,
                'resource_multiplier':2 if mode in ('resource_only','both') else 1,
                'energy_floor_injection':.3 if mode in ('energy_only','both') else None},
            'checkpoints':checkpoints,'final_fingerprint':g.fingerprint()}


def main():
    original=Garden.load(CANONICAL)
    assert original.tick==100
    fp=original.fingerprint()
    seeds=['canonical']+list(range(9100,9112))
    rows=[]
    for seed in seeds:
        if seed=='canonical':anchor=original
        else:
            anchor=Garden(seed=seed,size=12,learning=True)
            for _ in range(100):anchor.step()
        entry={'seed':seed,'start_tick':anchor.tick,
               'start_fingerprint':anchor.fingerprint(), 'arms':{}}
        for mode in MODES:entry['arms'][mode]=run(anchor,mode)
        assert anchor.fingerprint()==entry['start_fingerprint']
        rows.append(entry)
    assert Garden.load(CANONICAL).fingerprint()==fp
    fresh=rows[1:]
    summaries={mode:{'energy':float(np.mean([r['arms'][mode]['checkpoints'][5000]['energy'] for r in fresh])),
                     'floor':float(np.mean([r['arms'][mode]['checkpoints'][5000]['floor'] for r in fresh]))}
               for mode in MODES}
    payload={'status':'executed','hypothesis':'Are late-policy-switch failures caused by depleted resources or depleted energy?',
             'canonical_fingerprint_unchanged':fp,'fresh_seeds':list(range(9100,9112)),
             'intervention_time':500,'horizon':5000,'rows':rows,
             'fresh_seed_summaries':summaries,
             'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
                  for n in ('garden.py','SOC_LONGITUDINAL_explore.py','NEXT_LIVING_repair_probe.py')},
             'caution':'One-time resource or energy injection is external, not learned. Energy injection alters world state, not law. No population death occurs at floor. All controls start exact physical and neural state at switch.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
