"""Designer-imposed temporal gate on per-cell REINFORCE weight updates."""
from __future__ import annotations
import numpy as np
from NEXT_CREDIT_garden import CreditGarden


class GateGarden(CreditGarden):
    def __init__(self,seed=7,size=10,mode='online_all'):
        super().__init__(seed=seed,size=size,learning=True,
                         reward_observation='raw',trace_decay=.97,
                         baseline_smoothing=.995)
        if mode not in ('online_all','gate_scarcity','gate_sham',
                        'gate_recovery','frozen_all'):
            raise ValueError(mode)
        self.mode=mode

    def _update_enabled(self):
        t=self.tick+1
        return (self.mode=='online_all'
                or self.mode=='gate_scarcity' and not 1001<=t<=2000
                or self.mode=='gate_sham' and not 1<=t<=1000
                or self.mode=='gate_recovery' and not 2001<=t<=3000)

    def step(self):
        r=self.resource.copy();e=self.energy.copy()
        x=np.stack([3*(r-.5),3*(e-.5),np.ones(self.count)],axis=1)
        p=self._sigmoid(np.sum(self.theta*x,axis=1))
        a=(self.rng_action.random(self.count)<p).astype(float)
        next_r=np.clip(r+.08*(self._neighbors(r)-r)
                       +self.regrowth*(1-r)-.18*r*a,0.,1.)
        raw=.25*r*a-.03-.055*a+.008*(1-a)
        next_e=np.clip(e+raw,0.,1.)
        reward=(raw-.3*np.maximum(.18-next_e,0.)+.3*(next_r-r))
        self.trace=.97*self.trace+(a-p)[:,None]*x
        update=np.clip(self.lr*(reward-self.baseline)[:,None]*self.trace,-.02,.02)
        enabled=self._update_enabled()
        if enabled:self.theta=np.clip(self.theta+update,[-10.,-10.,-5.],[10.,10.,5.])
        self.baseline=.995*self.baseline+.005*reward
        self.resource=next_r;self.energy=next_e;self.tick+=1
        self.last_action=a.copy();self.prev_action=a;self.prev_reward=next_e-e
        self.last_raw=raw
        self._last={'tick':self.tick,'mean_energy':float(next_e.mean()),
                    'mean_resource':float(next_r.mean()),'harvest_rate':float(a.mean()),
                    'raw_drift':float(raw.mean()),
                    'energy_floor':float(np.mean(next_e<=.01)),
                    'energy_ceiling':float(np.mean(next_e>=.99)),
                    'policy_update_rms':float(np.sqrt(np.mean(update**2))) if enabled else 0.,
                    'mean_energy_weight':float(np.mean(self.theta[:,1]))}
        return self.metrics()
