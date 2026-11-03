from pathlib import Path
import json,hashlib
from collections import Counter
R=Path(__file__).resolve().parent;P=R.parent/'carried-garden-exploration-v1'
raw=[json.loads(s) for s in (R/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==40
markers=('<<<','>>>','Feedback:','CURRENT patch:','Next response:','Notebook:','Observation:');rows={}
for arm in ('full','short'):
 rr=[r for r in raw if r['arm']==arm];rows[arm]=dict(calls=len(rr),bare_old_labels=sum(r['text'].strip() in ('YES','NO','WITHHOLD','UNKNOWN') for r in rr),notebook_marker_replies=sum(any(m in r['text'] for m in markers) for r in rr),question_mark_replies=sum('?' in r['text'] for r in rr),tokens=sum(len(r['generated_token_ids']) for r in rr),cap_stops=sum(r['stop']=='token_limit' for r in rr),unique_replies=dict(Counter(r['text'] for r in rr)))
for i in range(0,len(raw),2):
 a,b=raw[i:i+2];assert a['arm']=='full' and b['arm']=='short';assert (a['episode'],a['seed'],a['step'],a['rng_seed'])==(b['episode'],b['seed'],b['step'],b['rng_seed'])
 assert a['task_score'] is None and b['task_score'] is None
 assert a['feedback']==b['feedback']=='Entry recorded. This open patch has no task score.'
parentpins={}
for p in (P/'run/notebooks').glob('*.jsonl'):
 q=R/'run/notebooks'/p.name;assert q.read_bytes().startswith(p.read_bytes());parentpins[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
resources=[json.loads(s) for s in (R/'run/RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
with (R/'AUDIT.json').open('x') as f:json.dump(dict(status='pass',matched_seed_pairs=20,all_new_entries_unscored=True,actual_feedback_not_replaced_by_generated_text=True,parent_prefix_sha256=parentpins,arm_observations=rows,max_working_estimate_bytes=max(x['working_estimate'] for x in resources)),f,indent=2);f.write('\n')
print(json.dumps({a:{k:v for k,v in x.items() if k!='unique_replies'} for a,x in rows.items()},indent=2))
