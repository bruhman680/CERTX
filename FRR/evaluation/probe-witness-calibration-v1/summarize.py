"""Descriptive saved-data reductions only. No fitting/generation/inference."""
from pathlib import Path
from collections import defaultdict
import json,re
p=Path(__file__).resolve().parent;r=p/'run'
w=[json.loads(x) for x in (r/'WITNESS_DIAGNOSTICS.jsonl').read_text().splitlines()]
s=[json.loads(x) for x in (r/'STRUCTURAL_DIAGNOSTICS.jsonl').read_text().splitlines()]
a=json.loads((r/'AGGREGATES.json').read_text());groups=defaultdict(list);allcells={}
pattern=r's(\d+)_a([34])_(CONTEXT|WEAK|SIGNAL|COPY)_(EXACT|BOUNDED|BETA_GAIN_ERROR|INVALID_SHARED_BIAS)_(BINDING_ORACLE|COEFF_ORACLE|ADVERTISED|POINT|GATED)_r([01])_e([01])'
for x in a:
    seed,ai,probe,mode,method,ri,ei=re.fullmatch(pattern,x['condition']).groups()
    c=(int(seed),int(ai),probe,mode,method,int(ri),int(ei));allcells[c]=x
    if method in ('POINT','GATED','ADVERTISED'):groups[(float(.5 if ai=='3' else 1.5),probe,mode,method,int(ri),int(ei))].append(x)
task=[]
for key,ls in groups.items():
    n=sum(x['count'] for x in ls);sums={k:sum(x['sums'][k] for x in ls) for k in ls[0]['sums']}
    task.append(dict(zip(('delta','probe','witness_mode','method','r_index','noise_index'),key),count=n,sums=sums,means={k:v/n for k,v in sums.items()}))
by_mode=[]
for mode in ('EXACT','BOUNDED','BETA_GAIN_ERROR','INVALID_SHARED_BIAS'):
    v=[x for x in w if x['witness_mode']==mode]
    by_mode.append({'mode':mode,'configs':len(v),'covered':sum(x['true_pair_covered'] for x in v),'gate_passed':sum(x['gate_passed'] for x in v),'false_identification':sum(x['false_identification_under_actual_model'] for x in v),'oracle_relative_withholding':sum(x['oracle_relative_withholding'] for x in v)})
beta_comparisons=[]
for c,x in allcells.items():
    seed,ai,probe,mode,method,ri,ei=c
    if mode=='BETA_GAIN_ERROR' and probe!='COPY' and method in ('POINT','GATED'):
        ref=allcells[seed,ai,probe,mode,'BINDING_ORACLE',ri,ei]
        beta_comparisons.append({'condition':x['condition'],'all_metric_sums_equal_oracle':x['sums']==ref['sums']})
out={'scope':'all3estimated/advertised methods descriptive cells, no new experiment; paired/reused inputs, not population inference','run_summary':json.loads((r/'SUMMARY.json').read_text()),'witness_mode_counts':by_mode,'task_cells':task,'structural_diagnostics':s,'beta_gain_task_oracle_comparisons':beta_comparisons}
(p/'RUN_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'task_cells':len(task),'beta_gain_task_oracle_comparisons':len(beta_comparisons),'all_equal':all(x['all_metric_sums_equal_oracle'] for x in beta_comparisons),'witness_counts':by_mode}))
