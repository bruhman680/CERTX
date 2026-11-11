"""Controlled alternative welfare rewards for the existing neural-cell Garden.

Research prototype. No claims of human welfare or general intelligence.
The only changed ingredient is how per-cell learning values consequences;
environmental dynamics remain those of EnergyAwareGarden. Explicitly chosen
reward shapes are *engineered objectives*, not spontaneously learned ethics.
"""
from __future__ import annotations

import numpy as np
from SOC_ENERGY_AWARE_policy import EnergyAwareGarden


class WelfareGarden(EnergyAwareGarden):
    def __init__(self, seed=7, size=12, learning=True, objective="raw",
                 penalty=.3, regrowth=.06, deterministic=False):
        super().__init__(seed=seed, size=size, learning=learning,
                         energy_feature=True, reward_mode="raw", regrowth=regrowth)
        if objective not in ("raw", "reserve", "resource", "reserve_resource"):
            raise ValueError(objective)
        self.objective=objective
        self.penalty=float(penalty)
        self.deterministic=bool(deterministic)

    def step(self):
        resource=self.resource.copy()
        energy=self.energy.copy()
        x=np.stack([3*(resource-.5),3*(energy-.5),np.ones(self.count)],axis=1)
        p=self._sigmoid(np.sum(self.theta*x,axis=1))
        if self.deterministic:
            action=(p>=.5).astype(float)
        else:
            action=(self.rng_action.random(self.count)<p).astype(float)
        nxt_r=np.clip(resource+.08*(self._neighbors(resource)-resource)
                      +self.regrowth*(1-resource)-.18*resource*action,0.,1.)
        raw=.25*resource*action-.03-.055*action+.008*(1-action)
        nxt_e=np.clip(energy+raw,0.,1.)
        actual=nxt_e-energy
        reward=raw.copy()
        if self.objective in ("reserve","reserve_resource"):
            reward-=self.penalty*np.maximum(.18-nxt_e,0.)
        if self.objective in ("resource","reserve_resource"):
            reward+=self.penalty*(nxt_r-resource)
        update_rms=0.
        if self.learning:
            self.trace=self.trace_decay*self.trace+(action-p)[:,None]*x
            change=np.clip(self.lr*(reward-self.baseline)[:,None]*self.trace,-.02,.02)
            self.theta=np.clip(self.theta+change,[-10.,-10.,-5.],[10.,10.,5.])
            self.baseline=.995*self.baseline+.005*reward
            update_rms=float(np.sqrt(np.mean(change**2)))
        self.resource=nxt_r;self.energy=nxt_e
        self.prev_action=action;self.last_action=action.copy();self.prev_reward=actual
        self.last_raw=raw;self.tick+=1
        self._last={'tick':self.tick,'mean_energy':float(nxt_e.mean()),
                    'mean_resource':float(nxt_r.mean()),'harvest_rate':float(action.mean()),
                    'raw_drift':float(raw.mean()),'energy_floor':float(np.mean(nxt_e<=.01)),
                    'energy_welfare':float(nxt_e.mean()-.5*np.mean(nxt_e<=.01)),
                    'energy_weight_abs_mean':float(np.mean(np.abs(self.theta[:,1]))),
                    'weight_update_rms':update_rms}
        return self.metrics()
