"""Neural Garden v0.1: independent neural cells in a local resource world.

This is a small experimental simulator, not a claim of emergent intelligence.
Each cell owns distinct neural weights and recurrent state. Each step consists
of observation, action selection, simultaneous world update, then learning from
the actual consequence. World rules and learning objectives are explicit.
"""

from __future__ import annotations

import hashlib
import json
import os
import pickle
import tempfile
from pathlib import Path

import numpy as np


class Garden:
    INPUTS = 7
    HIDDEN = 12

    def __init__(self, seed: int = 7, size: int = 16, learning: bool = True):
        if not (2 <= size <= 128):
            raise ValueError("size must be between 2 and 128")
        self.seed = int(seed)
        self.size = int(size)
        self.learning = bool(learning)
        self.count = size * size
        self.tick = 0
        self.rng_init = np.random.default_rng(seed)
        self.rng_action = np.random.default_rng(seed + 100_003)

        self.resource = self.rng_init.uniform(.35, .75, self.count).astype(np.float64)
        self.energy = self.rng_init.uniform(.45, .65, self.count).astype(np.float64)
        self.hidden = np.zeros((self.count, self.HIDDEN), dtype=np.float64)
        self.prev_action = np.zeros(self.count, dtype=np.float64)
        self.prev_reward = np.zeros(self.count, dtype=np.float64)
        self.reward_baseline = np.zeros(self.count, dtype=np.float64)
        self.last_action = np.zeros(self.count, dtype=np.float64)

        # Every cell owns independent tensors, including its recurrent matrix.
        self.win = self.rng_init.normal(0, .22, (self.count, self.INPUTS, self.HIDDEN))
        self.wrec = self.rng_init.normal(0, .07, (self.count, self.HIDDEN, self.HIDDEN))
        self.bhidden = self.rng_init.normal(0, .03, (self.count, self.HIDDEN))
        self.wpred = self.rng_init.normal(0, .18, (self.count, self.HIDDEN))
        self.bpred = self.rng_init.normal(0, .05, self.count)
        self.wact = self.rng_init.normal(0, .18, (self.count, self.HIDDEN))
        self.bact = self.rng_init.normal(0, .05, self.count)
        self._last = {"tick": 0, "mean_energy": float(self.energy.mean()),
                      "mean_resource": float(self.resource.mean()),
                      "harvest_rate": 0., "prediction_mse": None,
                      "mean_reward": 0., "weight_update_rms": 0.}

    def _neighbors(self, values):
        grid = np.asarray(values).reshape(self.size, self.size)
        return ((np.roll(grid, 1, 0) + np.roll(grid, -1, 0)
                 + np.roll(grid, 1, 1) + np.roll(grid, -1, 1)) / 4).reshape(-1)

    @staticmethod
    def _sigmoid(x):
        return 1. / (1. + np.exp(-np.clip(x, -30, 30)))

    def step(self):
        """Advance one synchronous tick. Returns measured post-step metrics."""
        before_resource = self.resource.copy()
        before_energy = self.energy.copy()
        before_hidden = self.hidden.copy()
        observations = np.stack([
            before_resource,
            before_energy,
            self._neighbors(before_resource),
            self._neighbors(before_energy),
            self.prev_action,
            np.clip(self.prev_reward * 5., -1., 1.),
            np.ones(self.count),
        ], axis=1)

        hidden = np.tanh(np.einsum('ni,nih->nh', observations, self.win)
                         + np.einsum('ni,nih->nh', before_hidden, self.wrec)
                         + self.bhidden)
        prediction = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wpred) + self.bpred)
        propensity = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wact) + self.bact)
        action = (self.rng_action.random(self.count) < propensity).astype(np.float64)

        # Fixed synchronous environmental laws, independent of model internals.
        diffusion = .08 * (self._neighbors(before_resource) - before_resource)
        regrowth = .06 * (1. - before_resource)
        consumption = .18 * before_resource * action
        next_resource = np.clip(before_resource + diffusion + regrowth - consumption, 0., 1.)
        delta_energy = .25 * before_resource * action - .03 - .055 * action + .008 * (1.-action)
        next_energy = np.clip(before_energy + delta_energy, 0., 1.)
        actual_delta = next_energy - before_energy
        mse = float(np.mean((prediction - next_resource)**2))
        update_rms = 0.

        if self.learning:
            # Local prediction error with actual (post-step) target. The action
            # policy also gets a one-step REINFORCE signal from realized energy.
            # Both updates truncate recurrent gradients at the prior hidden state.
            delta_p = (prediction - next_resource) * prediction * (1. - prediction)
            advantage = np.clip((actual_delta - self.reward_baseline) * 5., -.5, .5)
            delta_a = -(action - propensity) * advantage
            dh = delta_p[:, None] * self.wpred + .35 * delta_a[:, None] * self.wact
            dz = np.clip(dh * (1. - hidden**2), -.5, .5)

            lr_pred = .06
            lr_policy = .02
            self.wpred -= lr_pred * delta_p[:, None] * hidden
            self.bpred -= lr_pred * delta_p
            self.wact -= lr_policy * delta_a[:, None] * hidden
            self.bact -= lr_policy * delta_a
            delta_win = np.clip(observations[:, :, None] * dz[:, None, :], -.5, .5)
            delta_rec = np.clip(before_hidden[:, :, None] * dz[:, None, :], -.5, .5)
            self.win -= .02 * delta_win
            self.wrec -= .02 * delta_rec
            self.bhidden -= .02 * dz
            self.reward_baseline = .95 * self.reward_baseline + .05 * actual_delta
            update_rms = float(np.sqrt(np.mean((.02 * delta_win)**2)))

        self.resource = next_resource
        self.energy = next_energy
        self.hidden = hidden
        self.prev_action = action
        self.last_action = action.copy()
        self.prev_reward = actual_delta
        self.tick += 1
        self._last = {
            "tick": self.tick,
            "mean_energy": float(next_energy.mean()),
            "mean_resource": float(next_resource.mean()),
            "harvest_rate": float(action.mean()),
            "prediction_mse": mse,
            "mean_reward": float(actual_delta.mean()),
            "weight_update_rms": update_rms,
        }
        return self.metrics()

    def metrics(self):
        return dict(self._last)

    def snapshot(self):
        return {
            "size": self.size, "tick": self.tick, "seed": self.seed,
            "learning": self.learning,
            "energy": self.energy.reshape(self.size, self.size).tolist(),
            "resource": self.resource.reshape(self.size, self.size).tolist(),
            "activity": self.last_action.reshape(self.size, self.size).tolist(),
            "metrics": self.metrics(),
        }

    def prediction_probe(self, seed: int = 1729, n: int = 128):
        """Nonmutating, standardized prediction test on synthetic local cases.

        The target is the expected next resource for a REFERENCE action rate
        of 1/2, independent of each cell's actual learned policy. This is an
        off-policy diagnostic, not a held-out sample from the Garden's lived
        trajectory; recurrent state is standardized to zero for each case.
        """
        if n < 1:
            raise ValueError('n must be positive')
        rng = np.random.default_rng(seed)
        errors = []
        for _ in range(n):
            resource = rng.uniform(.25, .75, self.count)
            neighbor_resource = rng.uniform(.25, .75, self.count)
            energy = rng.uniform(.2, .9, self.count)
            neighbor_energy = rng.uniform(.2, .9, self.count)
            prev_action = rng.integers(0, 2, self.count).astype(float)
            observations = np.stack([resource, energy, neighbor_resource,
                neighbor_energy, prev_action, np.zeros(self.count),
                np.ones(self.count)], axis=1)
            hidden = np.tanh(np.einsum('ni,nih->nh', observations, self.win)
                              + self.bhidden)
            prediction = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wpred) + self.bpred)
            # A reference policy with independently sampled 50% harvest.
            target = np.clip(resource + .08*(neighbor_resource-resource)
                             + .06*(1-resource) - .09*resource, 0., 1.)
            errors.append(float(np.mean((prediction-target)**2)))
        return float(np.mean(errors))

    def fingerprint(self):
        """A hash of the full checkpoint state, including RNG and weights."""
        digest = hashlib.sha256()
        for name, value in sorted(self.__dict__.items()):
            digest.update(name.encode('utf-8'))
            if isinstance(value, np.ndarray):
                digest.update(str((value.shape, value.dtype)).encode('ascii'))
                digest.update(np.ascontiguousarray(value).tobytes())
            elif isinstance(value, np.random.Generator):
                digest.update(json.dumps(value.bit_generator.state, sort_keys=True).encode('utf-8'))
            else:
                digest.update(json.dumps(value, sort_keys=True).encode('utf-8'))
        return digest.hexdigest()

    def save(self, path):
        """Atomically checkpoint *all* simulator state, including RNG streams."""
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.garden-',
                                         suffix='.tmp', delete=False) as f:
            tmp = f.name
            try:
                pickle.dump(self, f, protocol=4)
                f.flush()
                os.fsync(f.fileno())
            except BaseException:
                f.close()
                os.unlink(tmp)
                raise
        os.replace(tmp, destination)

    @classmethod
    def load(cls, path):
        # Pickle is trusted local checkpoint input only. Never load untrusted
        # checkpoint bytes: Python pickle may execute arbitrary code.
        with open(path, 'rb') as f:
            obj = pickle.load(f)
        if not isinstance(obj, cls):
            raise TypeError('checkpoint does not contain a Garden')
        return obj

