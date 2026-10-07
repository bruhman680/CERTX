"""User-supplied True Garden model, retained as submitted for examination."""

import numpy as np
from collections import defaultdict

DIMS = 6
N_GEN = 6

SEED_GENOMES = [
    [1,0,1,0,0,1],
    [0,1,0,1,1,0],
    [1,1,0,0,1,0],
    [1,0,0,1,0,0],
    [0,1,1,0,0,1],
    [0,0,1,1,0,1],
    [1,0,1,0,1,0],
]

class Candidate:
    __slots__ = ('id','label','genome','fitness','pos','status','age','verifications','fit_history','parent_id','children','dormant')
    def __init__(self, cid, label, genome, fitness, pos, parent_id=None):
        self.id = cid
        self.label = label
        self.genome = tuple(genome)
        self.fitness = fitness
        self.pos = tuple(pos)
        self.status = 'spark'
        self.age = 0
        self.verifications = 0
        self.fit_history = [fitness]
        self.parent_id = parent_id
        self.children = []
        self.dormant = False

def build_nk_table(K, rng):
    K = int(np.clip(K,0,7))
    table = []
    for i in range(N_GEN):
        pool = np.array([j for j in range(N_GEN) if j!=i])
        rng.shuffle(pool)
        partners = pool[:K].tolist()
        n_entries = 2**(K+1) if K>0 else 2
        entries = rng.random(n_entries)
        table.append((partners, entries))
    return table

def compute_fitness(genome, table, soil_field):
    total = 0.0
    for i,(partners, entries) in enumerate(table):
        key = genome[i]
        for p in partners:
            key = key*2 + genome[p]
        total += entries[key % len(entries)]
    base = total / N_GEN
    wake = soil_field.get(''.join(map(str, genome)), 0.0)
    v = base + wake
    return 1.0 if v>1 else 0.0 if v<0 else v

def position_in_space(genome):
    coords = []
    for d in range(DIMS):
        v = 0.0
        for i,g in enumerate(genome):
            v += g * np.sin((d+1)*(i+1)*1.618)
        coords.append(1/(1+np.exp(-v)))
    return tuple(coords)

def distance(c1, c2):
    return np.sqrt(sum((a-b)**2 for a,b in zip(c1.pos, c2.pos)))

class TrueGardenEngine:
    def __init__(self, K=3, mut_rate=0.08, seed_rng=None,
                 alpha=0.8, beta=0.7, target_div=0.55, lr=0.08, soil_decay=0.997):
        self.rng = np.random.default_rng(seed_rng)
        self.K = float(K)
        self.mut_rate = mut_rate
        self.alpha = alpha
        self.beta = beta
        self.target_div = target_div
        self.lr = lr
        self.soil_decay = soil_decay

        self.candidates = {}
        self.soil = []
        self.soil_field = defaultdict(float)
        self.step_n = 0
        self.phase_age = 0
        self.phase = 'inhale'
        self.uid = 0
        self.last_K_int = int(K)
        self.fitness_table = build_nk_table(int(K), self.rng)
        self.history = {
            'step':[], 'K':[], 'pop':[], 'fossils':[], 'mean_fit':[],
            'diversity':[], 'soil_richness':[], 'dormant':[], 'wake_growth':[]
        }

    def _new_id(self):
        self.uid += 1
        return f"G{self.uid}"

    def _create(self, label, genome, parent_id=None):
        cid = self._new_id()
        fit = compute_fitness(genome, self.fitness_table, self.soil_field)
        pos = position_in_space(genome)
        c = Candidate(cid, label, genome, fit, pos, parent_id)
        self.candidates[cid] = c
        return c

    def _mutate(self, genome):
        return tuple(1-g if self.rng.random()<self.mut_rate else g for g in genome)

    def seed(self):
        used = {c.label for c in self.candidates.values()}
        for i,g in enumerate(SEED_GENOMES):
            label = f"seed-{i}"
            if label not in used:
                self._create(label, g)

    def _die(self, c):
        c.status = 'extinct'
        key = ''.join(map(str, c.genome))
        self.soil_field[key] += c.fitness * 0.08
        self.soil.append(c.genome)

    def soil_richness(self):
        if not self.soil:
            return 0.0
        wake = sum(self.soil_field.values())
        return min(1.0, wake/3 + len(self.soil)/80)

    def diversity(self):
        live = [c for c in self.candidates.values() if c.status!='extinct']
        if len(live)<2:
            return 0.0
        d=0.0; n=0
        for i in range(len(live)):
            for j in range(i+1, len(live)):
                d+= distance(live[i], live[j]); n+=1
        return d/n if n else 0.0

    def branch(self, parent=None):
        if parent is None:
            live = [c for c in self.candidates.values() if c.status in ('spark','proto','fossil')]
            if not live: return None
            parent = self.rng.choice(live)
        child = self._create(f"mut({parent.label[:10]})", self._mutate(parent.genome), parent.id)
        parent.children.append(child.id)
        return child

    def cross_pollinate(self):
        live = [c for c in self.candidates.values() if c.status in ('spark','proto')]
        if len(live)<2: return None
        self.rng.shuffle(live)
        p1 = live[0]
        p2 = next((c for c in live[1:] if distance(c,p1)>0.3), live[1] if len(live)>1 else None)
        if p2 is None: return None
        cp = 1 + self.rng.integers(0, N_GEN-2)
        genome = tuple(list(p1.genome[:cp]) + list(p2.genome[cp:]))
        child = self._create(f"{p1.label.split()[0]}x{p2.label.split()[0]}", genome, f"{p1.id}x{p2.id}")
        return child

    def inject_entropy(self):
        self.fitness_table = build_nk_table(int(round(self.K)), self.rng)
        woke=0
        for c in self.candidates.values():
            if c.status=='dormant':
                c.status='spark'; c.dormant=False; woke+=1
            if c.status in ('spark','proto') and self.rng.random()<0.3:
                c.genome = self._mutate(c.genome)
                c.fitness = compute_fitness(c.genome, self.fitness_table, self.soil_field)
        return woke

    def compost(self):
        n = sum(1 for c in self.candidates.values() if c.status=='extinct')
        self.candidates = {cid:c for cid,c in self.candidates.items() if c.status!='extinct'}
        if self.soil_richness()>0.45 and len(self.soil)>=3:
            donors = self.rng.choice(self.soil, 3, replace=False)
            genome = tuple(self.rng.choice([d[i] for d in donors]) for i in range(N_GEN))
            self._create(f"emergent-{len(self.soil)}", genome)
        return n

    def step(self):
        self.step_n += 1
        self.phase_age += 1
        if self.phase_age % 14 == 0:
            self.phase = 'exhale' if self.phase=='inhale' else 'inhale'
            if self.phase=='exhale':
                self.compost()

        for key in list(self.soil_field.keys()):
            self.soil_field[key] *= self.soil_decay
            if self.soil_field[key] < 1e-4:
                del self.soil_field[key]

        alive = [c for c in self.candidates.values() if c.status!='extinct']
        prev_wake = sum(self.soil_field.values())

        for c in alive:
            c.age += 1
            c.verifications += 1
            if self.rng.random()<0.5:
                new_genome = self._mutate(c.genome)
                c.genome = new_genome

            new_fit = compute_fitness(c.genome, self.fitness_table, self.soil_field)
            c.fitness = new_fit
            c.fit_history.append(new_fit)
            avg = np.mean(c.fit_history[-5:])

            if c.status=='spark':
                if avg>0.65 and c.verifications>=3:
                    c.status='proto'
                elif avg<0.25 and c.verifications>=2:
                    self._die(c)
            elif c.status=='proto':
                if avg>0.78 and c.verifications>=6:
                    c.status='fossil'
                elif avg<0.3 and c.verifications>=3:
                    if c.age>15 and all(f>0.6 for f in c.fit_history[-3:]):
                        c.dormant=True; c.status='dormant'
                    else:
                        self._die(c)
            elif c.status=='fossil':
                if new_fit<0.4:
                    c.status='proto'
            elif c.status=='dormant':
                if self.soil_richness()>0.5 and self.rng.random()<0.15:
                    c.status='spark'; c.dormant=False

        if self.phase=='inhale':
            cands = sorted([c for c in alive if c.status in ('spark','proto')], key=lambda x: -x.fitness)
            if cands and self.rng.random()<0.4:
                self.branch(cands[0])

        if self.step_n % 5 == 0:
            self.cross_pollinate()

        live = [c for c in self.candidates.values() if c.status!='extinct']
        if len(live)>30:
            weakest = sorted([c for c in live if c.status=='spark'], key=lambda x: x.fitness)
            if weakest: self._die(weakest[0])

        div = self.diversity()
        soil = self.soil_richness()
        dK = self.lr * (self.alpha*(div - self.target_div) - self.beta*soil + 0.07*np.sin(self.step_n*0.05) + 0.03*self.rng.normal())
        self.K = float(np.clip(self.K + dK, 0, 7))
        new_K_int = int(round(self.K))
        if new_K_int!= self.last_K_int:
            self.fitness_table = build_nk_table(new_K_int, self.rng)
            for c in live:
                c.fitness = compute_fitness(c.genome, self.fitness_table, self.soil_field)
            self.last_K_int = new_K_int

        if soil > 0.6:
            self.inject_entropy()

        mean_fit = np.mean([c.fitness for c in live]) if live else 0.0
        curr_wake = sum(self.soil_field.values())
        self.history['step'].append(self.step_n)
        self.history['K'].append(self.K)
        self.history['pop'].append(len(live))
        self.history['fossils'].append(sum(1 for c in live if c.status=='fossil'))
        self.history['mean_fit'].append(mean_fit)
        self.history['diversity'].append(div)
        self.history['soil_richness'].append(soil)
        self.history['dormant'].append(sum(1 for c in live if c.status=='dormant'))
        self.history['wake_growth'].append(curr_wake - prev_wake)
        return live

    def run(self, steps=2000):
        for _ in range(steps):
            self.step()
        return self.history

    def snapshot(self):
        live = [c for c in self.candidates.values() if c.status!='extinct']
        return {
            'step': self.step_n,
            'K': self.K,
            'K_int': int(round(self.K)),
            'pop': len(live),
            'fossils': sum(1 for c in live if c.status=='fossil'),
            'soil_richness': self.soil_richness(),
            'diversity': self.diversity(),
            'mean_fit': np.mean([c.fitness for c in live]) if live else 0,
        }

if __name__ == '__main__':
    g = TrueGardenEngine(K=3, mut_rate=0.08, seed_rng=99)
    g.seed()
    hist = g.run(2000)
    print(f"Settled: K last500={np.mean(hist['K'][-500:]):.2f} ±{np.std(hist['K'][-500:]):.2f}")
    print(f" diversity={np.mean(hist['diversity'][-500:]):.3f} soil={np.mean(hist['soil_richness'][-500:]):.3f} fit={np.mean(hist['mean_fit'][-500:]):.3f}")
    print(f" final snapshot:", g.snapshot())
    try:
        import matplotlib.pyplot as plt
        plt.plot(hist['step'], hist['K'], label='K')
        plt.plot(hist['step'], [d*6 for d in hist['diversity']], label='div x6')
        plt.plot(hist['step'], [s*6 for s in hist['soil_richness']], label='soil x6')
        plt.legend(); plt.savefig('garden_settled.png', dpi=150)
        print("saved garden_settled.png")
    except: pass
