"""Isolated diagnostic: sustained no-deposition differs from one-shot reset."""
import json
from copy import deepcopy
from statistics import mean
from true_garden_fluid_settled import TrueGardenEngine, compute_fitness

class NoDeposit(TrueGardenEngine):
    def _die(self, c):
        c.status = 'extinct'
        self.soil.append(c.genome)

class NoDepositNoRichness(NoDeposit):
    def soil_richness(self):
        return 0.0

def observe(g):
    live = [c for c in g.candidates.values() if c.status != 'extinct']
    return dict(snapshot=g.snapshot(), archive=len(g.soil), wake=sum(g.soil_field.values()),
                recomputed_fit=mean(compute_fitness(c.genome,g.fitness_table,g.soil_field) for c in live) if live else 0,
                table=[(p,e.tolist()) for p,e in g.fitness_table])

g = TrueGardenEngine(seed_rng=99)
g.seed(); g.run(120)
rows = {}
for label, cls, clear_archive in [('one_shot', TrueGardenEngine,False),('no_deposition',NoDeposit,False),('no_deposition_no_richness',NoDepositNoRichness,False),('no_deposition_no_archive',NoDeposit,True)]:
    v = deepcopy(g); v.__class__=cls; v.soil_field.clear()
    if clear_archive: v.soil.clear()
    rows[label]={'0':observe(v)}
    for t in range(1,101):
        v.step()
        if t in (1,3,12,100): rows[label][str(t)]=observe(v)
    if cls is not TrueGardenEngine: assert not v.soil_field

# Explicit compost read cannot repopulate field; its output can die and deposit.
v = deepcopy(g); v.soil_field.clear(); v.soil = v.soil*3
before = len(v.candidates); v.compost()
children=[c for c in v.candidates.values() if c.label.startswith('emergent-')]
assert children and not v.soil_field
c = children[-1]; v._die(c)
assert sum(v.soil_field.values()) == c.fitness*.08
rows['compost_read_then_death']={'archive':len(v.soil),'created_genome':c.genome,'created_fitness':c.fitness,'wake_after_compost':0,'wake_after_death':sum(v.soil_field.values())}
# Equal aggregate snapshot does not retain transition state.
a = deepcopy(g); b=deepcopy(g)
b.rng.random()
assert a.snapshot()==b.snapshot()
rows['equal_snapshot_different_rng']={'equal_snapshot':True,'rng_equal':a.rng.bit_generator.state==b.rng.bit_generator.state}
print(json.dumps(rows,indent=2,default=lambda x: x.item()))
