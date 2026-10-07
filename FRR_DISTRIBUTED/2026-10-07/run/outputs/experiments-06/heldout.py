import json, math
from pathlib import Path
from copy import deepcopy
from collections import defaultdict
import numpy as np
from true_garden_fluid_settled import TrueGardenEngine
from true_garden_field_transplant import make_donor
root=Path(__file__).resolve().parent
plan=json.loads((root/'predeclared.json').read_text())
donors={name:make_donor(seed) for name,seed in zip(('A','B'),plan['donor_seeds'])}
b=dict(donors['B'].soil_field)
fields={'virgin':{},'A':dict(donors['A'].soil_field),'B':b,'B_complement_keys':{''.join(str(1-int(x)) for x in k):v for k,v in b.items()},'B_numeric_copy':dict(b)}
rows=[]
for seed in plan['recipient_seeds']:
    base=TrueGardenEngine(seed_rng=seed,K=3,mut_rate=0)
    base.seed(); base.phase='exhale'; base.phase_age=0
    records={}
    for name,field in fields.items():
        e=deepcopy(base); e.soil_field=defaultdict(float,field); e.soil=[]
        assert e.rng.bit_generator.state==base.rng.bit_generator.state
        for (p,a),(q,c) in zip(e.fitness_table,base.fitness_table):
            assert p==q and np.array_equal(a,c)
        for _ in range(plan['horizon']):e.step()
        records[name]={'K':e.K,'K_int':e.last_K_int,'archive_n':len(e.soil),'rng':e.rng.bit_generator.state,'targets':{c.label:{'status':c.status,'average':float(np.mean(c.fit_history[-5:])),'fitness':float(c.fitness),'genome':''.join(map(str,c.genome))} for c in e.candidates.values() if c.label.startswith('seed-')}}
    rows.append({'recipient_seed':seed,'records':records})
def wilson(k,n):
    z=1.96; p=k/n; den=1+z*z/n; center=(p+z*z/(2*n))/den; delta=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [center-delta,center+delta]
summary={}
for name in fields:
    if name=='virgin':continue
    per={f'seed-{i}':0 for i in range(7)}; changed=0; kdiff=0; rngdiff=0; all_diff=[]
    for row in rows:
        v=row['records']['virgin']; t=row['records'][name]; differences=[]
        for label in per:
            if t['targets'][label]['status']!=v['targets'][label]['status']: per[label]+=1; differences.append(label)
        changed+=bool(differences); kdiff+=t['K']!=v['K']; rngdiff+=t['rng']!=v['rng']
        if differences:all_diff.append({'seed':row['recipient_seed'],'labels':differences})
    summary[name]={'any_status_changed':changed,'recipient_n':len(rows),'fraction':changed/len(rows),'wilson95_descriptive':wilson(changed,len(rows)),'per_label_changed':per,'K_different':kdiff,'rng_different':rngdiff,'changed_cases':all_diff}
assert all(row['records']['B']==row['records']['B_numeric_copy'] for row in rows)
(root/'results.json').write_text(json.dumps({'plan':plan,'donor_fields':fields,'summary':summary,'rows':rows},indent=2))
print(json.dumps(summary,indent=2))
