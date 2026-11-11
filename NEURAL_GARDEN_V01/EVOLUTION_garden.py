"""A separate experimental evolutionary branch of Neural Garden.

This is an ecological toy model, not an evolutionary or cognition claim.
Agents have unique ancestry IDs, finite lifetimes, local offspring, and
heritable mutating independent recurrent controller weights. No gradient
learning takes place. The base v0.1 code is left unchanged.
"""

from __future__ import annotations

import numpy as np

from garden import Garden


class EvolutionGarden(Garden):
    """Locally reproducing, mutating per-cell RNN society.

    `policy="neural"` selects action from the inherited neural controller;
    `policy="threshold"` is a non-neural ecological positive control. Both
    use the same demographic and resource rules. Any seeming advantage of
    the threshold policy is not evidence for genome evolution.
    """

    def __init__(self, seed=7, size=16, policy="neural", mutation_std=.025,
                 initial_occupancy=.65, max_age=240):
        super().__init__(seed=seed, size=size, learning=False)
        if policy not in {"neural", "threshold"}:
            raise ValueError("policy must be neural or threshold")
        if mutation_std < 0 or not 0 <= initial_occupancy <= 1:
            raise ValueError("invalid mutation/occupancy")
        if max_age < 2:
            raise ValueError("max_age must be >=2")
        self.policy = policy
        self.mutation_std = float(mutation_std)
        self.max_age = int(max_age)
        self.alive = self.rng_init.random(self.count) < initial_occupancy
        self.energy[~self.alive] = 0.
        self.age = np.zeros(self.count, dtype=np.int64)
        self.genome_id = np.full(self.count, -1, dtype=np.int64)
        self.generation = np.zeros(self.count, dtype=np.int64)
        self.lineage = {}   # persistent ancestry records
        self.next_id = 0
        for idx in np.flatnonzero(self.alive):
            uid = self._allocate_id(parent=-1, generation=0, location=int(idx), mutations=0)
            self.genome_id[idx] = uid
        self.births = 0
        self.deaths = 0
        self._last = self._measure(np.zeros(self.count), 0, 0, 0.)

    def _allocate_id(self, parent, generation, location, mutations):
        uid = self.next_id
        self.next_id += 1
        self.lineage[uid] = {"parent": int(parent), "generation": int(generation),
                             "birth_tick": int(self.tick), "death_tick": None,
                             "birth_location": int(location),
                             "mutated_parameters": int(mutations)}
        return uid

    def _neighbors_index(self, idx):
        y, x = divmod(int(idx), self.size)
        return (((y-1)%self.size)*self.size+x,
                ((y+1)%self.size)*self.size+x,
                y*self.size+(x-1)%self.size,
                y*self.size+(x+1)%self.size)

    def _measure(self, action, births, deaths, drift):
        alive = self.alive
        return {"tick": self.tick, "population": int(alive.sum()),
                "mean_energy_all": float(self.energy.mean()),
                "mean_energy_living": float(self.energy[alive].mean()) if alive.any() else 0.,
                "mean_resource": float(self.resource.mean()),
                "harvest_rate_living": float(action[alive].mean()) if alive.any() else 0.,
                "births_this_tick": int(births), "deaths_this_tick": int(deaths),
                "births_cumulative": int(getattr(self, "births", 0)),
                "deaths_cumulative": int(getattr(self, "deaths", 0)),
                "max_generation": int(self.generation[alive].max()) if alive.any() else 0,
                "raw_energy_drift_all": float(drift)}

    def step(self):
        before_resource = self.resource.copy()
        before_energy = self.energy.copy()
        alive_pre = self.alive.copy()
        obs = np.stack([before_resource, before_energy,
                        self._neighbors(before_resource), self._neighbors(before_energy),
                        self.prev_action, np.clip(self.prev_reward*5, -1, 1),
                        np.ones(self.count)], axis=1)
        hidden = np.tanh(np.einsum('ni,nih->nh', obs, self.win)
                         + np.einsum('ni,nih->nh', self.hidden, self.wrec)
                         + self.bhidden)
        if self.policy == "neural":
            p = self._sigmoid(np.einsum('nh,nh->n', hidden, self.wact) + self.bact)
            action = (self.rng_action.random(self.count) < p) & alive_pre
        else:
            action = (before_resource > .55) & alive_pre
        a = action.astype(float)
        diffusion = .08*(self._neighbors(before_resource)-before_resource)
        regrowth = .06*(1-before_resource)
        self.resource = np.clip(before_resource + diffusion + regrowth
                                - .18*before_resource*a, 0, 1)
        # Dead spots are inert; only living agents pay metabolism or harvest.
        raw = (.25*before_resource*a - .03*alive_pre
               - .055*a + .008*(alive_pre.astype(float)-a))
        self.energy = np.where(alive_pre, np.clip(before_energy+raw, 0, 1), 0.)
        self.hidden = np.where(alive_pre[:,None], hidden, 0.)
        self.prev_action = a
        self.last_action = a.copy()
        self.prev_reward = self.energy-before_energy
        self.age[alive_pre] += 1
        self.tick += 1

        dying = alive_pre & ((self.energy <= .02) | (self.age >= self.max_age))
        dead_indices = np.flatnonzero(dying)
        for idx in dead_indices:
            self.lineage[int(self.genome_id[idx])]["death_tick"] = self.tick
        self.alive[dying] = False
        self.energy[dying] = 0.
        self.genome_id[dying] = -1
        self.hidden[dying] = 0.
        self.deaths += len(dead_indices)

        # Reproduction: child receives energy transferred from its parent;
        # 0.24 debited, 0.20 credited, 0.04 overhead. No free energy source.
        newborns = 0
        parents = self.rng_init.permutation(np.flatnonzero(self.alive & (self.energy > .62)))
        for parent_idx in parents:
            if self.rng_init.random() >= .035:
                continue
            options = [j for j in self._neighbors_index(parent_idx) if not self.alive[j]]
            if not options or self.energy[parent_idx] <= .62:
                continue
            child_idx = int(self.rng_init.choice(options))
            for key in ("win", "wrec", "bhidden", "wpred", "bpred", "wact", "bact"):
                tensor = getattr(self, key)
                tensor[child_idx] = tensor[parent_idx] + self.rng_init.normal(
                    0, self.mutation_std, np.shape(tensor[parent_idx]))
            self.energy[parent_idx] -= .24
            self.energy[child_idx] = .20
            self.alive[child_idx] = True
            self.age[child_idx] = 0
            self.hidden[child_idx] = 0.
            self.prev_action[child_idx] = 0.
            self.prev_reward[child_idx] = 0.
            self.generation[child_idx] = self.generation[parent_idx]+1
            self.genome_id[child_idx] = self._allocate_id(
                parent=self.genome_id[parent_idx],
                generation=self.generation[child_idx], location=child_idx,
                mutations=(int(sum(np.asarray(getattr(self, key)[child_idx]).size for key
                    in ("win", "wrec", "bhidden", "wpred", "bpred", "wact", "bact")))
                    if self.mutation_std > 0 else 0))
            newborns += 1
        self.births += newborns
        self._last = self._measure(a, newborns, len(dead_indices), float(raw.mean()))
        return self.metrics()

    def fingerprint(self):
        # Full-state digest includes ancestry, arrays and RNG streams.
        return super().fingerprint()

    def ancestry(self, uid):
        """Trace one lineage to its founding ancestor; no history discarded."""
        ancestors = []
        while uid != -1:
            if uid not in self.lineage:
                raise KeyError(uid)
            ancestors.append(uid)
            uid = self.lineage[uid]["parent"]
        return ancestors

    def snapshot(self):
        s = super().snapshot()
        s.update({"policy": self.policy, "population": int(self.alive.sum()),
                  "alive": self.alive.reshape(self.size,self.size).tolist(),
                  "generation": self.generation.reshape(self.size,self.size).tolist(),
                  "genome_ids": self.genome_id.reshape(self.size,self.size).tolist(),
                  "lineage_entries": len(self.lineage), "births": self.births,
                  "deaths": self.deaths})
        return s

