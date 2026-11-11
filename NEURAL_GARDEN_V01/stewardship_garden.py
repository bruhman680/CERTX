"""Separate v0.2 stewardship-reward intervention on Neural Garden v0.1.

Identical world transition laws, neural architecture, random streams and
supervised resource prediction. Only local policy reinforcement differs:
the action reward includes a local resource-change term. This is an explicit
designer-supplied incentive, not spontaneous ecological understanding.
"""

import numpy as np

from garden import Garden


class StewardshipGarden(Garden):
    STEWARDSHIP_WEIGHT = .65
    METABOLISM = .03  # v0.2 world law remains identical to v0.1

    def step(self):
        before_resource = self.resource.copy()
        before_energy = self.energy.copy()
        before_hidden = self.hidden.copy()
        observations = np.stack([
            before_resource, before_energy,
            self._neighbors(before_resource), self._neighbors(before_energy),
            self.prev_action, np.clip(self.prev_reward*5., -1., 1.),
            np.ones(self.count)], axis=1)
        hidden = np.tanh(np.einsum('ni,nih->nh', observations, self.win)
                         + np.einsum('ni,nih->nh', before_hidden, self.wrec)
                         + self.bhidden)
        prediction = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wpred)+self.bpred)
        propensity = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wact)+self.bact)
        action = (self.rng_action.random(self.count) < propensity).astype(float)

        # World transition is copied verbatim from v0.1. Only the learner's
        # reward signal below is different.
        diffusion = .08*(self._neighbors(before_resource)-before_resource)
        regrowth = .06*(1.-before_resource)
        consumption = .18*before_resource*action
        next_resource = np.clip(before_resource+diffusion+regrowth-consumption,0.,1.)
        delta_energy = .25*before_resource*action-self.METABOLISM-.055*action+.008*(1.-action)
        next_energy = np.clip(before_energy+delta_energy,0.,1.)
        actual_delta = next_energy-before_energy
        stewardship_reward = actual_delta + self.STEWARDSHIP_WEIGHT*(next_resource-before_resource)
        mse = float(np.mean((prediction-next_resource)**2))
        update_rms=0.
        if self.learning:
            delta_p=(prediction-next_resource)*prediction*(1.-prediction)
            advantage=np.clip((stewardship_reward-self.reward_baseline)*5.,-.5,.5)
            delta_a=-(action-propensity)*advantage
            dh=delta_p[:,None]*self.wpred+.35*delta_a[:,None]*self.wact
            dz=np.clip(dh*(1.-hidden**2),-.5,.5)
            self.wpred-=.06*delta_p[:,None]*hidden
            self.bpred-=.06*delta_p
            self.wact-=.02*delta_a[:,None]*hidden
            self.bact-=.02*delta_a
            delta_win=np.clip(observations[:,:,None]*dz[:,None,:],-.5,.5)
            delta_rec=np.clip(before_hidden[:,:,None]*dz[:,None,:],-.5,.5)
            self.win-=.02*delta_win
            self.wrec-=.02*delta_rec
            self.bhidden-=.02*dz
            self.reward_baseline=.95*self.reward_baseline+.05*stewardship_reward
            update_rms=float(np.sqrt(np.mean((.02*delta_win)**2)))

        self.resource=next_resource
        self.energy=next_energy
        self.hidden=hidden
        self.prev_action=action
        self.last_action=action.copy()
        self.prev_reward=actual_delta
        self.tick+=1
        self._last={
            "tick": self.tick,
            "mean_energy":float(next_energy.mean()),
            "mean_resource":float(next_resource.mean()),
            "harvest_rate":float(action.mean()),
            "prediction_mse":mse,
            "mean_reward":float(actual_delta.mean()),
            "mean_stewardship_reward":float(stewardship_reward.mean()),
            "weight_update_rms":update_rms,
        }
        return self.metrics()

    def snapshot(self):
        snapshot=super().snapshot()
        snapshot["stewardship_weight"]=self.STEWARDSHIP_WEIGHT
        snapshot["metabolism"]=self.METABOLISM
        return snapshot
