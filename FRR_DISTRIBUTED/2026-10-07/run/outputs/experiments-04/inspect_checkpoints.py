import json
from copy import deepcopy
from statistics import mean
from garden_wake_probe import record
from true_garden_fluid_settled import TrueGardenEngine, compute_fitness

def extra(g):
    r=record(g)
    live=[c for c in g.candidates.values() if c.status!='extinct']
    r['recomputed_mean_fit']=mean(compute_fitness(c.genome,g.fitness_table,g.soil_field) for c in live) if live else 0
    r['cached_minus_recomputed']=r['mean_fit']-r['recomputed_mean_fit']
    return r
out={}
for start in (40,120):
    g=TrueGardenEngine(K=3,mut_rate=.08,seed_rng=99);g.seed();g.run(start)
    variants={}
    for name,field,archive in [('unaltered',False,False),('clear_wake_field',True,False),('clear_soil_archive',False,True),('clear_both',True,True)]:
        v=deepcopy(g)
        if field:v.soil_field.clear()
        if archive:v.soil.clear()
        observations={'0':extra(v)}
        for h in range(1,101):
            v.step()
            if h in (1,3,12,100):observations[str(h)]=extra(v)
        variants[name]=observations
    out[str(start)]=variants
print(json.dumps(out,indent=2))
