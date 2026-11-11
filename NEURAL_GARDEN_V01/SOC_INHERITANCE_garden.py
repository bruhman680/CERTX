"""Experimental demographic neural threshold cells with acquired-state inheritance.

Separate model. Extends EvolutionGarden's demographics, keeps original local
resource/energy laws except an explicitly labeled seasonal regrowth phase.
Supports a one-parameter neural threshold per cell, within-lifetime teacher-free
eligibility-trace learning, genetic mutation, and acquired vs germline inheritance.
Not evidence of biological Lamarckism or population-level adaptation.
"""

from __future__ import annotations

import numpy as np

from EVOLUTION_garden import EvolutionGarden


class InheritanceGarden(EvolutionGarden):
    def __init__(self, seed=7, size=10, learning=True, inherit_acquired=True,
                 mutation_std=0., trace_decay=.97, lr=.001, slope=14.):
        super().__init__(seed=seed, size=size, policy="neural",
                         mutation_std=0., initial_occupancy=.65, max_age=240)
        self.learning = bool(learning)
        self.inherit_acquired = bool(inherit_acquired)
        self.theta_mutation_std = float(mutation_std)
        self.trace_decay = float(trace_decay)
        self.lr = float(lr)
        self.slope = float(slope)
        self.thresholds = self.rng_init.uniform(.25, .75, self.count)
        self.germline = self.thresholds.copy()
        self.traces = np.zeros(self.count)
        self.policy_baseline = np.zeros(self.count)
        self.last_raw = np.zeros(self.count)
        self.mean_abs_learning = 0.
        self._last = self._measure(np.zeros(self.count), 0, 0, 0.)

    def step(self, regrowth_rate=.06):
        resource = self.resource.copy()
        energy = self.energy.copy()
        pre_alive = self.alive.copy()
        p = self._sigmoid(self.slope * (resource - self.thresholds))
        action = ((self.rng_action.random(self.count) < p) & pre_alive)
        a = action.astype(float)

        diffusion = .08 * (self._neighbors(resource) - resource)
        regrowth = float(regrowth_rate) * (1. - resource)
        self.resource = np.clip(resource + diffusion + regrowth
                                - .18 * resource * a, 0., 1.)
        raw = (.25 * resource * a - .03 * pre_alive
               - .055 * a + .008 * (pre_alive.astype(float) - a))
        self.energy = np.where(pre_alive, np.clip(energy + raw, 0., 1.), 0.)
        realized = self.energy - energy
        self.prev_action = a
        self.last_action = a.copy()
        self.prev_reward = realized
        self.last_raw = raw
        self.age[pre_alive] += 1
        self.tick += 1

        if self.learning:
            score = -self.slope * (a - p)
            self.traces = np.where(pre_alive,
                                   self.trace_decay * self.traces + score, 0.)
            advantage = realized - self.policy_baseline
            update = np.clip(self.lr * advantage * self.traces, -.01, .01)
            self.thresholds[pre_alive] = np.clip(
                self.thresholds[pre_alive] + update[pre_alive], .05, .95)
            self.policy_baseline[pre_alive] = (
                .99 * self.policy_baseline[pre_alive] + .01 * realized[pre_alive])
            self.mean_abs_learning = float(np.abs(update[pre_alive]).mean()) if pre_alive.any() else 0.
        else:
            self.mean_abs_learning = 0.

        dying = pre_alive & ((self.energy <= .02) | (self.age >= self.max_age))
        dead_indices = np.flatnonzero(dying)
        for idx in dead_indices:
            self.lineage[int(self.genome_id[idx])]["death_tick"] = self.tick
        self.alive[dying] = False
        self.energy[dying] = 0.
        self.genome_id[dying] = -1
        self.traces[dying] = 0.
        self.policy_baseline[dying] = 0.
        self.deaths += len(dead_indices)

        newborns = 0
        parents = self.rng_init.permutation(np.flatnonzero(self.alive & (self.energy > .62)))
        for parent in parents:
            if self.rng_init.random() >= .035:
                continue
            slots = [j for j in self._neighbors_index(parent) if not self.alive[j]]
            if not slots or self.energy[parent] <= .62:
                continue
            child = int(self.rng_init.choice(slots))
            # Inheritance intervention: acquire-to-child or only germline-to-child.
            inherited = (self.thresholds[parent] if self.inherit_acquired
                         else self.germline[parent])
            mutated = float(np.clip(
                inherited + self.rng_init.normal(0., self.theta_mutation_std), .05, .95))
            self.thresholds[child] = mutated
            # Germline always follows original unlearned genetic value, plus any
            # germline mutation; acquired changes are not silently called genes.
            self.germline[child] = float(np.clip(
                self.germline[parent] + self.rng_init.normal(0., self.theta_mutation_std), .05, .95))
            self.traces[child] = 0.
            self.policy_baseline[child] = 0.
            self.energy[parent] -= .24
            self.energy[child] = .20
            self.alive[child] = True
            self.age[child] = 0
            self.prev_action[child] = 0.
            self.prev_reward[child] = 0.
            self.generation[child] = self.generation[parent] + 1
            self.genome_id[child] = self._allocate_id(
                self.genome_id[parent], self.generation[child], child,
                int(self.theta_mutation_std > 0))
            newborns += 1
        self.births += newborns
        self._last = self._measure(a, newborns, len(dead_indices), float(raw.mean()))
        self._last.update({
            "mean_threshold_living": float(self.thresholds[self.alive].mean()) if self.alive.any() else 0.,
            "mean_germline_living": float(self.germline[self.alive].mean()) if self.alive.any() else 0.,
            "mean_abs_threshold_update": self.mean_abs_learning,
        })
        return self.metrics()
