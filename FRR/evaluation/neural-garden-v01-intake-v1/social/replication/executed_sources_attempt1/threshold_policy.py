"""Simple resource-threshold heuristic baseline for Neural Garden.

No neural action selection or learning. The same world transition equations
from Garden v0.1 apply, but harvest iff local resource > threshold. This
supplies an interpretable comparator before claiming neural policy advantage.
"""

import numpy as np

from garden import Garden


class ThresholdGarden(Garden):
    def __init__(self, seed=7, size=16, threshold=.55):
        super().__init__(seed=seed, size=size, learning=False)
        self.threshold = float(threshold)
        if not 0. <= self.threshold <= 1.:
            raise ValueError('threshold must be in [0,1]')

    def step(self):
        before_resource=self.resource.copy()
        before_energy=self.energy.copy()
        action=(before_resource > self.threshold).astype(float)
        diffusion=.08*(self._neighbors(before_resource)-before_resource)
        regrowth=.06*(1.-before_resource)
        next_resource=np.clip(before_resource+diffusion+regrowth
                              -.18*before_resource*action,0.,1.)
        delta_energy=.25*before_resource*action-.03-.055*action+.008*(1.-action)
        next_energy=np.clip(before_energy+delta_energy,0.,1.)
        self.resource=next_resource
        self.energy=next_energy
        self.prev_action=action
        self.last_action=action.copy()
        self.prev_reward=next_energy-before_energy
        self.tick+=1
        self._last={"tick":self.tick,"mean_energy":float(next_energy.mean()),
                    "mean_resource":float(next_resource.mean()),
                    "harvest_rate":float(action.mean()),
                    "prediction_mse":None,
                    "mean_reward":float(self.prev_reward.mean()),
                    "weight_update_rms":0.}
        return self.metrics()

    def snapshot(self):
        snapshot=super().snapshot()
        snapshot['policy']='threshold'
        snapshot['threshold']=self.threshold
        return snapshot

