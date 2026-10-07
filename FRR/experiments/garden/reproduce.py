"""Reproduction harness; original engine and uploaded probes remain unchanged."""
from pathlib import Path
from copy import deepcopy
import json, hashlib, platform
import numpy as np
from true_garden_fluid_settled import TrueGardenEngine, compute_fitness, position_in_space, build_nk_table
from true_garden_field_transplant import experiment
from garden_wake_probe import compare_from_checkpoint

ROOT=Path(__file__).resolve().parents[2]
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(tuple,list)):return [clean(v) for v in x]
 if isinstance(x,np.generic):return x.item()
 return x

g=TrueGardenEngine(seed_rng=99);g.seed();g.run(2000)
summary={'snapshot':g.snapshot(),'last500':{k:{'mean':np.mean(g.history[k][-500:]),'std':np.std(g.history[k][-500:])} for k in ['K','diversity','soil_richness','mean_fit']},'archive_n':len(g.soil),'field_total':sum(g.soil_field.values()),'logged_wake_growth_total':sum(g.history['wake_growth'])}
seeds=[]
for seed in range(1,6):
 s=TrueGardenEngine(seed_rng=seed);s.seed();s.run(1000)
 seeds.append({'seed':seed,'mean_K_last200':np.mean(s.history['K'][-200:]),'mean_soil_last200':np.mean(s.history['soil_richness'][-200:]),'archive_n':len(s.soil)})
checkpoint=TrueGardenEngine(seed_rng=99);checkpoint.seed();checkpoint.run(120)
stale=sum(c.pos!=position_in_space(c.genome) for c in checkpoint.candidates.values() if c.status!='extinct')
target='010100';genome=tuple(map(int,target))
field_contrast={'genome':target,'with_field':compute_fitness(genome,checkpoint.fitness_table,checkpoint.soil_field),'without_field':compute_fitness(genome,checkpoint.fitness_table,{})}
perturbed=deepcopy(checkpoint);perturbed.inject_entropy()
mutation_count=sum(c.genome!=checkpoint.candidates[cid].genome for cid,c in perturbed.candidates.items())
assert perturbed.K==checkpoint.K and perturbed.soil==checkpoint.soil and perturbed.soil_field==checkpoint.soil_field
# Artificial carrier intervention confirms richness's gate and archive floor.
f=deepcopy(checkpoint);f.soil=[]
a=deepcopy(checkpoint);a.soil_field.clear();a.soil=[genome]*80
assert f.soil_richness()==0 and sum(f.soil_field.values())>0
assert a.soil_richness()==1 and not a.soil_field
# Tables beyond actual maximum partners contain unreachable entries.
table=build_nk_table(7,np.random.default_rng(1))
assert all(len(partners)==5 and len(entries)==256 for partners,entries in table)
donors,transplant=experiment()
assert transplant['field_B_empty'][3]['target_status']=='proto'
assert all(transplant[name][3]['target_status']=='spark' for name in ['virgin_empty','field_A_empty','virgin_archive_B'])
assert all(row['target_genome']=='011001' for records in transplant.values() for row in records.values())
reset={t:compare_from_checkpoint(start=t) for t in [40,120]}
results={'kind':'execution of unchanged submitted engine and probes plus explicit diagnostic interventions','python':platform.python_version(),'numpy':np.__version__,'engine_sha256':hashlib.sha256(Path('true_garden_fluid_settled.py').read_bytes()).hexdigest(),'baseline_seed99_steps2000':summary,'other_seeds_steps1000':seeds,'checkpoint120':{'stale_live_positions':stale,'field_contrast':field_contrast,'inject_entropy_mutated_candidates':mutation_count,'inject_entropy_preserved_K_archive_field':True},'transplant':transplant,'reset_replay':reset,'limits':['Seed 7 selected near promotion threshold.','Shared RNG initial states can diverge after different random draw consumption.','No physical EPR or general FRR effectiveness established.']}
out=ROOT/'evaluation/results/garden-reproduced-2026-10-05.json';out.write_text(json.dumps(clean(results),indent=2)+'\n')
print(json.dumps(clean({'seed99':summary,'other_seeds':seeds,'stale_positions':stale,'field_contrast':field_contrast,'entropy_mutated':mutation_count}),indent=2))
print('Saved',out)
