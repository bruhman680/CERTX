"""Explicitly nonstationary world for adaptive-threshold policy stress tests.

World laws are Garden v0.1 except in the labeled scarcity segment. Separate
artifact avoids editing original Garden, and does not modify neural weights.
"""
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden


class RegimeGarden(AdaptiveThresholdGarden):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.regime_events=[]
        self.last_raw_delta=np.zeros(self.count)

    def step(self):
        tick=self.tick
        # One exogenous shared resource shock at the start of scarcity.
        if tick==1000:
            self.resource*=.70
            self.regime_events.append({"tick":1000,"kind":"resource_shock","factor":.70})
        scarcity=1000<=tick<2000
        regrowth_rate=.025 if scarcity else .06
        harvest_cost=.070 if scarcity else .055
        resource=self.resource.copy();energy=self.energy.copy()
        p=self._sigmoid(self.slope*(resource-self.thresholds))
        action=((resource>self.thresholds) if self.deterministic
                else (self.rng_action.random(self.count)<p)).astype(float)
        diffusion=.08*(self._neighbors(resource)-resource)
        regrowth=regrowth_rate*(1.-resource)
        next_resource=np.clip(resource+diffusion+regrowth-.18*resource*action,0.,1.)
        raw=.25*resource*action-.03-harvest_cost*action+.008*(1.-action)
        next_energy=np.clip(energy+raw,0.,1.)
        realized=next_energy-energy
        if self.learning:
            score=-self.slope*(action-p)
            self.traces=self.trace_decay*self.traces+score
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
                    "weight_update_rms":float(np.sqrt(np.mean(update**2))) if self.learning else 0.,
                    "regime":"scarcity" if scarcity else ("recovery" if tick>=2000 else "baseline")}
        return self.metrics()
