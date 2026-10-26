"""Descriptive reduction only; never regenerates, fits or scores inputs."""
from pathlib import Path
from collections import defaultdict
import json
p=Path(__file__).resolve().parent;run=p/'run'
a=json.loads((run/'AGGREGATES.json').read_text());d=json.loads((run/'STRUCTURAL_DIAGNOSTICS.json').read_text())
groups=defaultdict(list)
for x in a:
    if x['method'] in ('repaired','solved'):groups[tuple(x[k] for k in ('delta','probe','m','r','eval_eta','method'))].append(x)
task=[]
for key,ls in groups.items():
    n=sum(x['count'] for x in ls);s={k:sum(x['metric_sums'][k] for x in ls) for k in ls[0]['metric_sums']}
    task.append(dict(zip(('delta','probe','m','r','eval_eta','method'),key),count=n,sums=s,means={k:v/n for k,v in s.items()},solved_available=ls[0]['solved_available']))
struct=[];groups=defaultdict(list)
for x in d:groups[x['delta'],x['probe'],x['m']].append(x)
for key,ls in groups.items():
    metrics={}
    for name in ('ambient_relative_change','base_probe_distance','average_base_distance','average_binding_distance','average_target_distance','solved_binding_distance','solved_target_distance'):
        values=[x[name] for x in ls if x[name] is not None]
        metrics[name]={'mean':sum(values)/len(values),'max':max(values)} if values else None
    struct.append(dict(zip(('delta','probe','m'),key),metrics=metrics,solved_available=ls[0]['solved_available'],ranks={k:[x['fit'][k]['retained_rank'] for x in ls] for k in ('first','second','average','solved')}))
pool=json.loads((run/'OUTCOME_MAP.json').read_text());algebra=json.loads((run/'ALGEBRA_DIAGNOSTICS.json').read_text())
out={'scope':'all repaired/solved descriptive cells over3fixed source seeds; shared/repeated claims, no inference or new execution','run_summary':json.loads((run/'SUMMARY.json').read_text()),'task_cells':task,'structural_cells':struct,'algebra_controls':algebra['controls'],'pool_summary':{k:v for k,v in pool.items() if k not in ('conditions','arrays')}}
(p/'RUN_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'task_cells':len(task),'structural_cells':len(struct)}))
