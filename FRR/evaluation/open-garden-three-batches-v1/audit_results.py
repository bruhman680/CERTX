"""Prospective descriptive metrics and independent checkpoint audit; no model forwards."""
from pathlib import Path
import json,hashlib
from collections import Counter
R=Path(__file__).resolve().parent;P=R.parent/'open-notebook-continuation-v1'
MARKERS=('<<<','>>>','Feedback:','CURRENT patch:','Next response:','Notebook:','Observation:')
def rows(p):return [json.loads(s) for s in p.read_text().splitlines()]
def main():
 raw=rows(R/'run/RAW.jsonl');m=json.loads((R/'run/RUN_MANIFEST.json').read_text());assert len(raw)==m['generation_calls'];by={(r['episode'],r['seed'],r['step'],r['arm']):r for r in raw};pairs=[];checkpoints=[];groups=[]
 for row in raw:
  assert row['task_score'] is None and row['feedback']=='Entry recorded. This open patch has no task score.'
  if row['arm']=='short':
   a=by[row['episode'],row['seed'],row['step'],'full'];assert a['rng_seed']==row['rng_seed'];pairs.append(dict(episode=row['episode'],seed=row['seed'],step=row['step'],same_reply=a['text']==row['text'],same_tokens=a['generated_token_ids']==row['generated_token_ids']))
 for cpfile in (R/'run/notebooks').glob('*_CHECKPOINT.json'):
  cp=json.loads(cpfile.read_text());tr=cpfile.name.removesuffix('_CHECKPOINT.json');parent=json.loads((P/'run/notebooks'/cpfile.name).read_text());assert cp['events'][:15]==parent['events'];notebook=R/'run/notebooks'/f'{tr}.jsonl';assert notebook.read_bytes().startswith((P/'run/notebooks'/f'{tr}.jsonl').read_bytes());assert rows(notebook)==cp['events']
  for n,end in [(1,20),(2,25),(3,30)]:
   p=R/'run/notebooks'/f'{tr}_BATCH_{n}.json'
   if end<=cp['next_step']:
    b=json.loads(p.read_text());assert b['next_step']==end and b['events']==cp['events'][:end];checkpoints.append(dict(trajectory=tr,batch=n,next_step=end,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 for batch in (1,2,3):
  for arm in ('full','short'):
   rr=[r for r in raw if (r['step']-15)//5+1==batch and r['arm']==arm]
   if not rr:continue
   groups.append(dict(batch=batch,arm=arm,calls=len(rr),bare_old_labels=sum(r['text'].strip() in ('YES','NO','WITHHOLD','UNKNOWN') for r in rr),marker_replies=sum(any(x in r['text'] for x in MARKERS) for r in rr),question_mark_replies=sum('?' in r['text'] for r in rr),cap_stops=sum(r['stop']=='token_limit' for r in rr),tokens=sum(len(r['generated_token_ids']) for r in rr),exact_unique_replies=len({r['text'] for r in rr})))
 resource=rows(R/'run/RESOURCE.jsonl');assert all(x['working_estimate']<x['working_limit'] for x in resource)
 result=dict(status='pass',calls=len(raw),paired_rounds=len(pairs),paired_text_differences=sum(not x['same_reply'] for x in pairs),parent_prefixes_preserved=len(list((R/'run/notebooks').glob('*_CHECKPOINT.json'))),batch_checkpoints_checked=checkpoints,all_new_outputs_unscored=True,groups=groups,max_working_estimate_bytes=max(x['working_estimate'] for x in resource),scope='Counts are descriptive, four coupled trajectories and fixed sampling/interface; no population or plateau guarantee')
 with (R/'AUDIT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 with (R/'UNIQUE_REPLIES.json').open('x') as f:json.dump(Counter(r['text'] for r in raw),f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in result.items() if k!='batch_checkpoints_checked'},indent=2))
if __name__=='__main__':main()
