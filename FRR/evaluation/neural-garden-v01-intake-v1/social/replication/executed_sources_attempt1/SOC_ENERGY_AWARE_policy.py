"""Teacher-free local energy-aware policy-gradient controller.

Two locally observed features (resource, energy), no demonstrations or
explicit low-energy rescue in the learner. Original Garden physics unless an
experiment explicitly changes the regrowth coefficient.
"""
from __future__ import annotations
import numpy as np
from garden import Garden


class EnergyAwareGarden(Garden):
    def __init__(self,seed=7,size=16,learning=True,energy_feature=True,
                 reward_mode='raw',lr=.04,trace_decay=.97,regrowth=.06):
        super().__init__(seed=seed,size=size,learning=learning)
        self.energy_feature=bool(energy_feature)
        if reward_mode not in ('raw','clipped'):
            raise ValueError('reward_mode must be raw or clipped')
        self.reward_mode=reward_mode
        self.lr=float(lr);self.trace_decay=float(trace_decay)
        self.regrowth=float(regrowth)
        # Shared resource-sensitive *inductive bias* across arms, not a learned
        # threshold or teacher example; the extra energy coefficient starts 0.
        # This design tests whether an energy input can be USED, not whether
        # resource dependence arises from completely random connectivity.
        self.theta=np.stack([self.rng_init.normal(4.,.35,self.count),
                             np.zeros(self.count),
                             self.rng_init.normal(0.,.1,self.count)],axis=1)
        self.trace=np.zeros((self.count,3))
        self.baseline=np.zeros(self.count)
        self.last_raw=np.zeros(self.count)

    def step(self):
        resource=self.resource.copy();energy=self.energy.copy()
        x=np.stack([3*(resource-.5),3*(energy-.5),np.ones(self.count)],axis=1)
        if not self.energy_feature:x[:,1]=0.
        p=self._sigmoid(np.sum(self.theta*x,axis=1))
        action=(self.rng_action.random(self.count)<p).astype(float)
        diffusion=.08*(self._neighbors(resource)-resource)
        nxt_r=np.clip(resource+diffusion+self.regrowth*(1.-resource)
                      -.18*resource*action,0.,1.)
        raw=.25*resource*action-.03-.055*action+.008*(1.-action)
        nxt_e=np.clip(energy+raw,0.,1.)
        actual=nxt_e-energy
        update_rms=0.
        if self.learning:
            reward=raw if self.reward_mode=='raw' else actual
            self.trace=self.trace_decay*self.trace+(action-p)[:,None]*x
            change=np.clip(self.lr*(reward-self.baseline)[:,None]*self.trace,-.02,.02)
            self.theta=np.clip(self.theta+change,[-10.,-10.,-5.],[10.,10.,5.])
            if not self.energy_feature:self.theta[:,1]=0.
            self.baseline=.995*self.baseline+.005*reward
            update_rms=float(np.sqrt(np.mean(change**2)))
        self.resource=nxt_r;self.energy=nxt_e
        self.prev_action=action;self.last_action=action.copy();self.prev_reward=actual
        self.last_raw=raw;self.tick+=1
        self._last={'tick':self.tick,'mean_energy':float(nxt_e.mean()),
                    'mean_resource':float(nxt_r.mean()),'harvest_rate':float(action.mean()),
                    'raw_drift':float(raw.mean()),'energy_floor':float(np.mean(nxt_e<=.01)),
                    'energy_weight_abs_mean':float(np.mean(np.abs(self.theta[:,1]))),
                    'weight_update_rms':update_rms}
        return self.metrics()


class ExplicitRuleGarden(Garden):
    def __init__(self,seed=7,size=16,rescue=False,regrowth=.06):
        super().__init__(seed=seed,size=size,learning=False)
        self.rescue=bool(rescue);self.regrowth=float(regrowth)

    def step(self):
        r=self.resource.copy();e=self.energy.copy()
        threshold=np.where(e<.18,.48,.50) if self.rescue else .50
        action=(r>threshold).astype(float)
        nxt_r=np.clip(r+.08*(self._neighbors(r)-r)+self.regrowth*(1-r)
                      -.18*r*action,0.,1.)
        raw=.25*r*action-.03-.055*action+.008*(1-action)
        nxt_e=np.clip(e+raw,0.,1.)
        self.resource=nxt_r;self.energy=nxt_e;self.tick+=1
        self.last_action=action;self.prev_action=action
        self._last={'tick':self.tick,'mean_energy':float(nxt_e.mean()),
                    'mean_resource':float(nxt_r.mean()),'harvest_rate':float(action.mean()),
                    'raw_drift':float(raw.mean()),'energy_floor':float(np.mean(nxt_e<=.01)),
                    'weight_update_rms':0.}
        return self.metrics()

