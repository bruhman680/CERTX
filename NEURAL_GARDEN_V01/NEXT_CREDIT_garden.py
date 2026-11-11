"""One-factor causal interventions on a local neural policy-gradient updater."""
from __future__ import annotations
import numpy as np
from NEXT_WELFARE_garden import WelfareGarden


class CreditGarden(WelfareGarden):
    def __init__(self,seed=7,size=10,learning=True,reward_observation='raw',
                 trace_decay=.97,baseline_smoothing=.995):
        super().__init__(seed=seed,size=size,learning=learning,
                         objective='reserve_resource',penalty=.3)
        if reward_observation not in ('raw','clipped'):
            raise ValueError(reward_observation)
        self.reward_observation=reward_observation
        self.trace_decay=float(trace_decay)
        self.baseline_smoothing=float(baseline_smoothing)

    def step(self):
        r=self.resource.copy();e=self.energy.copy()
        x=np.stack([3*(r-.5),3*(e-.5),np.ones(self.count)],axis=1)
        p=self._sigmoid(np.sum(self.theta*x,axis=1))
        a=(self.rng_action.random(self.count)<p).astype(float)
        next_r=np.clip(r+.08*(self._neighbors(r)-r)
                       +self.regrowth*(1-r)-.18*r*a,0.,1.)
        raw=.25*r*a-.03-.055*a+.008*(1-a)
        next_e=np.clip(e+raw,0.,1.)
        actual=next_e-e
        energy_reward=raw if self.reward_observation=='raw' else actual
        reward=(energy_reward-.3*np.maximum(.18-next_e,0.)
                +.3*(next_r-r))
        rms=0.
        if self.learning:
            self.trace=self.trace_decay*self.trace+(a-p)[:,None]*x
            update=np.clip(self.lr*(reward-self.baseline)[:,None]*self.trace,-.02,.02)
            self.theta=np.clip(self.theta+update,[-10.,-10.,-5.],[10.,10.,5.])
            self.baseline=self.baseline_smoothing*self.baseline+(1-self.baseline_smoothing)*reward
            rms=float(np.sqrt(np.mean(update**2)))
        self.resource=next_r;self.energy=next_e;self.tick+=1
        self.last_action=a.copy();self.prev_action=a;self.prev_reward=actual
        self.last_raw=raw
        self._last={'tick':self.tick,'mean_energy':float(next_e.mean()),
                    'mean_resource':float(next_r.mean()),'harvest_rate':float(a.mean()),
                    'raw_drift':float(raw.mean()),
                    'energy_floor':float(np.mean(next_e<=.01)),
                    'energy_ceiling':float(np.mean(next_e>=.99)),
                    'policy_update_rms':rms,
                    'mean_energy_weight':float(np.mean(self.theta[:,1]))}
        return self.metrics()
