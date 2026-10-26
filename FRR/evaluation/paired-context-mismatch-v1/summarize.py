"""Reduce saved results only; no generation, fitting or inference."""
from pathlib import Path
from collections import defaultdict
import json

p=Path(__file__).resolve().parent;run=p/'run'
ag=json.loads((run/'AGGREGATES.json').read_text())
sd=json.loads((run/'STRUCTURAL_DIAGNOSTICS.json').read_text())
groups=defaultdict(list)
for x in ag:
    c=x['condition']
    if c['method']=='estimated':groups[(c['arm'],c['m'],c['r'],c['eval_eta'])].append(x)
task=[]
for key,values in groups.items():
    n=sum(x['count'] for x in values)
    sums={k:sum(x['metric_sums'][k] for x in values) for k in values[0]['metric_sums']}
    task.append(dict(zip(('arm','m','r','eval_eta'),key),n=n,metric_sums=sums,means={k:v/n for k,v in sums.items()}))
groups=defaultdict(list)
for x in sd:groups[(x['arm'],x['m'])].append(x)
structure=[]
metrics=('distance_to_intended_binding','distance_to_population_target','train_relative_residual','validation_relative_residual','moment_operator_deviation')
for key,values in groups.items():
    structure.append(dict(zip(('arm','m'),key),seeds=[x['seed'] for x in values],
        summaries={k:{'mean':sum(x[k] for x in values)/len(values),'min':min(x[k] for x in values),'max':max(x[k] for x in values)} for k in metrics}))
out={'scope':'all estimated-arm descriptive cells; no outcomes selection, new input or experiment; means over3fixed seeds/reused claims, no population confidence inference',
     'run_summary':json.loads((run/'SUMMARY.json').read_text()),'task_cells':task,'structural_cells':structure,
     'population_diagnostics':json.loads((run/'POPULATION_DIAGNOSTICS.json').read_text())}
(p/'RUN_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'task_cells':len(task),'structural_cells':len(structure)}))
