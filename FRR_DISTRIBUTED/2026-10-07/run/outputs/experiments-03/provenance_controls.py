import json, platform
from copy import deepcopy
from collections import defaultdict
import numpy as np
from true_garden_field_transplant import make_donor, make_recipient
from true_garden_fluid_settled import compute_fitness
b=make_donor(23)
base=make_recipient()
key='011001'
full=dict(b.soil_field)
removed={k:v for k,v in full.items() if k!=key}
target_only={key:full[key]}
rows={}
for name,field in [('virgin',{}),('B_full',full),('B_target_removed',removed),('B_target_only',target_only)]:
 e=deepcopy(base); e.soil_field=defaultdict(float,field); e.soil=[]
 t=next(c for c in e.candidates.values() if c.label=='seed-4')
 initial_stored=t.fitness
 for _ in range(3):e.step()
 rows[name]={'initial_stored_fitness':float(initial_stored),'fitness_history':list(map(float,t.fit_history)),'promotion_average':float(np.mean(t.fit_history[-5:])),'status':t.status,'K':e.K,'archive_n':len(e.soil)}
print(json.dumps({'python':platform.python_version(),'numpy':np.__version__,'controls':rows},indent=2))
