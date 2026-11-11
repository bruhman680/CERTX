"""Action-conditioned predictor and supervised policy-control diagnostic.

This is *not* an autonomous discovery algorithm: an external fixed threshold
provides the correct action label. It tests whether distinct per-cell recurrent
neural networks can represent and learn resource-sensitive decisions when the
teaching signal is clear. Environment laws are unchanged from Garden v0.1.
"""

import numpy as np
from garden import Garden


class ImitationGarden(Garden):
    def __init__(self, seed=7, size=16, learning=True, teacher_threshold=.55,
                 imitation_rate=.22, deterministic_action=False):
        super().__init__(seed=seed, size=size, learning=learning)
        self.teacher_threshold = float(teacher_threshold)
        self.imitation_rate = float(imitation_rate)
        self.deterministic_action = bool(deterministic_action)
        self.action_pred_weight = np.zeros(self.count, dtype=float)

    def step(self):
        before_resource = self.resource.copy()
        before_energy = self.energy.copy()
        before_hidden = self.hidden.copy()
        observations = np.stack([
            before_resource, before_energy, self._neighbors(before_resource),
            self._neighbors(before_energy), self.prev_action,
            np.clip(self.prev_reward * 5, -1, 1), np.ones(self.count),
        ], axis=1)
        hidden = np.tanh(np.einsum('ni,nih->nh', observations, self.win)
                         + np.einsum('ni,nih->nh', before_hidden, self.wrec)
                         + self.bhidden)
        propensity = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wact) + self.bact)
        if self.deterministic_action:
            action = (propensity >= .5).astype(float)
        else:
            action = (self.rng_action.random(self.count) < propensity).astype(float)
        prediction = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wpred)
                                   + self.bpred + self.action_pred_weight * action)

        # Original v0.1 laws, same coefficients and update ordering.
        diffusion = .08 * (self._neighbors(before_resource) - before_resource)
        regrowth = .06 * (1 - before_resource)
        consumption = .18 * before_resource * action
        next_resource = np.clip(before_resource + diffusion + regrowth - consumption, 0, 1)
        raw_delta = .25 * before_resource * action - .03 - .055 * action + .008 * (1 - action)
        next_energy = np.clip(before_energy + raw_delta, 0, 1)
        actual_delta = next_energy - before_energy
        teacher_action = (before_resource > self.teacher_threshold).astype(float)
        mse = float(np.mean((prediction - next_resource)**2))
        imitation_accuracy = float(np.mean((propensity >= .5) == teacher_action))
        update_rms = 0.

        if self.learning:
            # Action-conditioned next-resource model: observation + *current* action.
            delta_p = (prediction - next_resource) * prediction * (1 - prediction)
            old_prediction_head = self.wpred.copy()
            old_action_head = self.wact.copy()
            self.wpred -= .06 * delta_p[:, None] * hidden
            self.bpred -= .06 * delta_p
            self.action_pred_weight -= .06 * delta_p * action

            # External supervised teacher. No credit for ecological discovery.
            delta_a = propensity - teacher_action
            self.wact -= self.imitation_rate * delta_a[:, None] * hidden
            self.bact -= self.imitation_rate * delta_a
            dh = delta_p[:, None] * old_prediction_head + delta_a[:, None] * old_action_head
            dz = np.clip(dh * (1 - hidden ** 2), -.5, .5)
            delta_win = np.clip(observations[:, :, None] * dz[:, None, :], -.5, .5)
            delta_rec = np.clip(before_hidden[:, :, None] * dz[:, None, :], -.5, .5)
            self.win -= .02 * delta_win
            self.wrec -= .02 * delta_rec
            self.bhidden -= .02 * dz
            update_rms = float(np.sqrt(np.mean((.02 * delta_win) ** 2)))

        self.resource = next_resource
        self.energy = next_energy
        self.hidden = hidden
        self.prev_action = action
        self.last_action = action.copy()
        self.prev_reward = actual_delta
        self.tick += 1
        self._last = dict(tick=self.tick, mean_energy=float(next_energy.mean()),
                          mean_resource=float(next_resource.mean()),
                          harvest_rate=float(action.mean()), prediction_mse=mse,
                          mean_reward=float(actual_delta.mean()),
                          weight_update_rms=update_rms,
                          teacher_imitation_accuracy=imitation_accuracy,
                          raw_energy_drift=float(raw_delta.mean()))
        return self.metrics()
