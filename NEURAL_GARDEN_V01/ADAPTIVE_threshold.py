"""Autonomous stochastic one-neuron-per-cell harvesting policy (research baseline).

Every cell learns a continuous resource threshold through REINFORCE with a
discounted eligibility trace. No threshold teacher is supplied. This is a
separate controller, not the original 12-hidden-unit recurrent Garden neural
network, and it must not be presented as learned cognition or evolution.
The environment physics remain exactly Garden v0.1's.
"""

from __future__ import annotations
import numpy as np
from garden import Garden


class AdaptiveThresholdGarden(Garden):
    def __init__(self, seed=7, size=16, learning=True, slope=14.,
                 lr=.001, trace_decay=.97, start_low=.25, start_high=.75,
                 deterministic=False):
        super().__init__(seed=seed, size=size, learning=learning)
        self.slope=float(slope); self.lr=float(lr)
        self.trace_decay=float(trace_decay)
        self.deterministic=bool(deterministic)
        self.thresholds=self.rng_init.uniform(start_low,start_high,self.count)
        self.traces=np.zeros(self.count)
        self.value_baseline=np.zeros(self.count)
        self.last_raw_delta=np.zeros(self.count)

    def step(self):
        resource=self.resource.copy(); energy=self.energy.copy()
        p=self._sigmoid(self.slope*(resource-self.thresholds))
        action=((resource>self.thresholds) if self.deterministic
                else (self.rng_action.random(self.count)<p)).astype(float)
        diffusion=.08*(self._neighbors(resource)-resource)
        regrowth=.06*(1.-resource)
        next_resource=np.clip(resource+diffusion+regrowth-.18*resource*action,0.,1.)
        raw=.25*resource*action-.03-.055*action+.008*(1.-action)
        next_energy=np.clip(energy+raw,0.,1.)
        realized=next_energy-energy
        if self.learning:
            score=-self.slope*(action-p)
            self.traces=self.trace_decay*self.traces+score
            # A delayed-action trace is necessary because harvesting affects
            # future resources; the signal is *realized* local energy change.
            advantage=realized-self.value_baseline
            update=np.clip(self.lr*advantage*self.traces,-.01,.01)
            self.thresholds=np.clip(self.thresholds+update,.05,.95)
            self.value_baseline=.99*self.value_baseline+.01*realized
        self.resource=next_resource;self.energy=next_energy
        self.prev_action=action;self.last_action=action.copy()
        self.prev_reward=realized;self.last_raw_delta=raw
        self.tick+=1
        self._last={"tick":self.tick,"mean_energy":float(next_energy.mean()),
                    "mean_resource":float(next_resource.mean()),
                    "harvest_rate":float(action.mean()),
                    "raw_energy_drift":float(raw.mean()),
                    "mean_threshold":float(self.thresholds.mean()),
                    "prediction_mse":None,"mean_reward":float(realized.mean()),
                    "weight_update_rms":float(np.sqrt(np.mean(update**2))) if self.learning else 0.}
        return self.metrics()

    def deterministic_fresh_test(self, seed, steps=600):
        """Evaluate learned thresholds in a newly seeded v0.1 world."""
        test=AdaptiveThresholdGarden(seed=seed,size=self.size,learning=False,
                                     slope=self.slope,lr=self.lr,
                                     deterministic=True)
        test.thresholds=self.thresholds.copy()
        for _ in range(steps): test.step()
        return float(test.energy.mean()),float(test.resource.mean())
