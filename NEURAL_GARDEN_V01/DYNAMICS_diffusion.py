"""Mechanistic counterfactual for near-neutral threshold .5: diffusion on/off.

This is a labeled WORLD-LAW intervention, never used as a fair same-world
comparison. An isolated cell cycle supplies an exact analytical benchmark.
"""
import json
from pathlib import Path
import numpy as np
from threshold_policy import ThresholdGarden

ROOT=Path(__file__).resolve().parent

class DiffusionGarden(ThresholdGarden):
    def __init__(self,seed,diffusion):
        super().__init__(seed=seed, threshold=.5)
        self.diffusion=float(diffusion)
    def step(self):
        r=self.resource.copy();e=self.energy.copy();a=(r>.5).astype(float)
        next_r=np.clip(r+self.diffusion*(self._neighbors(r)-r)+.06*(1-r)-.18*r*a,0,1)
        delta=.25*r*a-.063*a-.022
        self.energy=np.clip(e+delta,0,1)
        self.resource=next_r
        self.last_action=a
        self.tick+=1
        return float(delta.mean())

def run():
    rows=[]
    for diff in (0.0,.08):
        for seed in range(980,992):
            world=DiffusionGarden(seed,diff)
            drift=[]
            for t in range(10000):
                raw=world.step()
                if t>=8000:drift.append(raw)
            rows.append({'seed':seed,'diffusion':diff,'energy_final':float(world.energy.mean()),
                         'resource_final':float(world.resource.mean()),
                         'raw_drift_tail':float(np.mean(drift)),
                         'floor_final':float((world.energy<=.01).mean()),
                         'ceiling_final':float((world.energy>=.99).mean())})
    summary={str(diff):{'raw_drift_tail':float(np.mean([r['raw_drift_tail'] for r in rows if r['diffusion']==diff])),
                         'energy_final':float(np.mean([r['energy_final'] for r in rows if r['diffusion']==diff])),
                         'floor_final':float(np.mean([r['floor_final'] for r in rows if r['diffusion']==diff]))}
             for diff in (0,.08)}
    a=.94;b=.76
    high=(.06*a*a+.06*(1+a))/(1-b*a*a)
    homogeneous_drift=(.25*high-.085-2*.022)/3
    data={'design':'posthoc diffusion ablation at fixed .5 threshold; changing diffusion is world-law intervention',
          'seeds':list(range(980,992)), 'ticks':10000,'tail_ticks':2000,
          'homogeneous_three_cycle_high_resource':high,
          'homogeneous_three_cycle_raw_drift':homogeneous_drift,
          'rows':rows,'summary':summary}
    (ROOT/'DYNAMICS_diffusion_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
