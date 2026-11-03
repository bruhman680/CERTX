from pathlib import Path
import json,hashlib,copy
from observer import index
R=Path(__file__).resolve().parent;P=R.parent/'selective-observation-v1'
load=lambda p:[json.loads(s) for s in p.read_text().splitlines()]
old=load(P/'run/RAW.jsonl');raw=load(R/'run/RAW.jsonl');m=json.loads((R/'run/RUN_MANIFEST.json').read_text());recorded=json.loads((R/'EVENT_INDEX.json').read_text());before=hashlib.sha256(json.dumps([old,raw],sort_keys=True).encode()).hexdigest();assert index(old,raw,m['stops'])==recorded;assert hashlib.sha256(json.dumps([old,raw],sort_keys=True).encode()).hexdigest()==before
assert len(recorded['rows'])==len(raw)==m['generation_calls'];assert len(recorded['selected_flagged_ids'])<=6;selected=set(recorded['selected_flagged_ids']);assert all(x['flags'] for x in recorded['rows'] if x['run_id'] in selected)
if recorded['quiet_sample_id'] is not None:assert not next(x for x in recorded['rows'] if x['run_id']==recorded['quiet_sample_id'])['flags']
notebooks=[]
for p in (R/'run/notebooks').glob('*_CHECKPOINT.json'):
 cp=json.loads(p.read_text());parent=json.loads((P/'run/notebooks'/p.name).read_text());assert cp['events'][:len(parent['events'])]==parent['events'];tr=p.name.removesuffix('_CHECKPOINT.json');assert (R/'run/notebooks'/f'{tr}.jsonl').read_bytes().startswith((P/'run/notebooks'/f'{tr}.jsonl').read_bytes());notebooks.append(dict(trajectory=tr,next_step=cp['next_step']))
plans=load(R/'run/PROMPTS.jsonl');by={p['run_id']:p for p in plans};rawids={x['run_id'] for x in raw}
for b in m['stops']:assert b['run_id'] in by and b['run_id'] not in rawids and len(by[b['run_id']]['input_token_ids'])==b['tokens']>3072
for x in raw:assert x['task_score'] is None and x['feedback']=='Entry recorded. This open patch has no task score.'
resources=load(R/'run/RESOURCE.jsonl');assert all(x['working_estimate']<x['working_limit'] for x in resources)
oldplans={p['run_id']:p for p in load(P/'run/PROMPTS.jsonl')};resumed=[]
for stop in json.loads((P/'run/RUN_MANIFEST.json').read_text())['stops']:
 if stop['run_id'] in {x['run_id'] for x in raw}:
  row=next(x for x in raw if x['run_id']==stop['run_id']);assert row['input_token_ids']==oldplans[stop['run_id']]['input_token_ids'];resumed.append(stop['run_id'])
assert len(resumed)==2
result=dict(resumed_old_boundary_prompts_identical=resumed,status='pass',all_model_rows_indexed=len(raw),reviewed_example_slots=len(selected)+(recorded['quiet_sample_id'] is not None),mandatory_boundary_events=len(m['stops']),index_recomputed_exactly=True,observer_does_not_mutate_inputs=True,parent_prefixes_preserved=len(notebooks),notebooks=notebooks,boundary_prompts_not_sent_to_model=True,all_outputs_unscored=True)
with (R/'AUDIT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
