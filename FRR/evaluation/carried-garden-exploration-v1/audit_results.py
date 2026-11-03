"""Additional paired-output and descriptive-transition audit; no model forwards."""
from pathlib import Path
import json,hashlib,sys
from collections import Counter
from design import schedule,SEEDS
R=Path(__file__).resolve().parent
raw=[json.loads(s) for s in (R/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==80
pairs=[];identical=0
for episode in ('persistent_failure','evidence_availability'):
 for seed in SEEDS:
  rs=[r for r in raw if r['episode']==episode and r['seed']==seed];assert len(rs)==20
  for step in range(10):
   rr=[r for r in rs if r['step']==step];assert [r['arm'] for r in rr]==['full','short'];a,b=rr;assert a['rng_seed']==b['rng_seed']
   if a['prompt']==b['prompt']:assert a['generated_token_ids']==b['generated_token_ids'];identical+=1
   pairs.append(dict(episode=episode,seed=seed,step=step,same_prompt=a['prompt']==b['prompt'],same_tokens=a['generated_token_ids']==b['generated_token_ids'],same_answer=a['answer']==b['answer'],same_text=a['text']==b['text']))
resources=[json.loads(s) for s in (R/'run/RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
# Independent recomputation from the actual first lines; unscored is not failure.
armcounts={}
for arm in ('full','short'):
 rr=[r for r in raw if r['arm']==arm];armcounts[arm]=dict(calls=len(rr),correct=sum(r['correct'] is True for r in rr),incorrect=sum(r['correct'] is False for r in rr),unscored=sum(r['correct'] is None for r in rr),question_mark_replies=sum('?' in r['text'] for r in rr),cap_stops=sum(r['stop']=='token_limit' for r in rr))
for r in raw:
 if r['answer'] is None:assert r['correct'] is None and r['feedback'].startswith('No scored')
result=dict(status='pass',paired_rounds=len(pairs),identical_prompt_exact_replays=identical,arm_counts=armcounts,paired_token_differences=sum(not x['same_tokens'] for x in pairs),paired_answer_differences=sum(not x['same_answer'] for x in pairs),pairs=pairs,max_working_estimate_bytes=max(x['working_estimate'] for x in resources),all_resource_points_below_guard=True)
with (R/'AUDIT.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
import torch,transformers,numpy
with (R/'RUNTIME.json').open('x') as f:json.dump(dict(python=sys.version,torch=torch.__version__,transformers=transformers.__version__,numpy=numpy.__version__,scope='recorded after completed run; no environment installs/changes in this experiment'),f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='pairs'},indent=2))
