"""Descriptive reduction of saved results; never generates or scores new inputs."""
import json
from pathlib import Path
from collections import defaultdict

p=Path(__file__).resolve().parent
run=p/'run'
aggregates=json.loads((run/'AGGREGATES.json').read_text())
structural=json.loads((run/'STRUCTURAL_DIAGNOSTICS.json').read_text())
invariance=json.loads((run/'INVARIANCE.json').read_text())

def grouped(rows,keys):
    groups=defaultdict(list)
    for row in rows:
        c=row['condition'];groups[tuple(c[k] for k in keys)].append(row)
    answer=[]
    for key,values in groups.items():
        n=sum(v['count'] for v in values)
        sums={k:sum(v['metric_sums'][k] for v in values) for k in values[0]['metric_sums']}
        answer.append(dict(zip(keys,key),n=n,metric_sums=sums,means={k:v/n for k,v in sums.items()}))
    return answer

out={'scope':'post-outcome descriptive summaries; all conditions retained in archived AGGREGATES.json; no additional execution or tuning',
     'run_summary':json.loads((run/'SUMMARY.json').read_text()),
     'transport_table':grouped([v for v in aggregates if v['condition']['train_eta']==0 and v['condition']['m']==48],['Q','r','eval_eta','method']),
     'estimated_dense_table':grouped([v for v in aggregates if v['condition']['Q']=='dense' and v['condition']['method']=='estimated'],['r','eval_eta','train_eta','m']),
     'structural_identity': [v for v in structural if v['Q']=='identity'],
     'invariance_summary':{'condition_comparisons':len(invariance),'query_comparisons':32*len(invariance),
       **{k:sum(len(v[k]) if isinstance(v[k],list) else v[k] for v in invariance) for k in ['top3_set_mismatch_queries','top3_order_mismatch_queries','prediction_mismatch_items','reason_mismatch_items','metric_mismatch_queries']},
       'duplicated_control_conditions_included':True}}
(p/'RUN_SUMMARY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'transport_cells':len(out['transport_table']),'estimated_dense_cells':len(out['estimated_dense_table']),'summary':'RUN_SUMMARY.json'}))
