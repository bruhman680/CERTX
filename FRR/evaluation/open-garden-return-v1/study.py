from pathlib import Path
import os,json,sys,hashlib
from io_utils import sha,dump_new,append
R=Path(__file__).resolve().parent;P=R.parent/'open-garden-settling-v1';BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=R.parent/'simple-readout-acquisition-v1/run/canonical';EPISODES=('persistent_failure','evidence_availability');SEEDS=(110301,110302)
HEADER=('Open notebook. You may revisit an earlier attempt, ask a question, describe uncertainty, propose an experiment, or follow another connection. There is no required answer format or task score in this patch. Choose your next small move.')
OBS='Open exploration patch.';FEEDBACK='Entry recorded. This open patch has no task score.'
def render(events):
 log='\n\n'.join('Round '+str(x['step']+1)+'\nObservation:\n'+x['observation']+'\nRecorded reply:\n<<<\n'+x['reply']+'\n>>>\nFeedback: '+x['feedback'] for x in events)
 return HEADER+'\n\nNotebook:\n'+log+'\n\nCURRENT patch:\n'+OBS+'\n\nNext response:'
def freeze_check():
 f=json.loads((R/'FREEZE.json').read_text());assert all(sha(Path(p))==v for p,v in f['files'].items())
def prepare():
 config=json.loads((BASE/'config.json').read_text());assert config['max_position_embeddings']>=3072+96
 ps=[p for p in R.iterdir() if p.suffix=='.py']+[R/'PROTOCOL.md',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json',BASE/'config.json']+list((P/'run/notebooks').glob('*_CHECKPOINT.json'))
 dump_new(R/'FREEZE.json',dict(timing='before resumed five-round outputs; unchanged3072budget and model input contract',files={str(p):sha(p) for p in ps}))
def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from lora_cpu import inject_lora,load_adapter
 from runtime_reference import Guard,parameter_digest
 from generate import generate
 freeze_check();out=R/'run';out.mkdir();(out/'notebooks').mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];count=0;stops=[]
 for epi,episode in enumerate(EPISODES):
  for seed in SEEDS:
   trajectory_stopped=False;trajectory=f'{episode}_{seed}';cp=json.loads((P/'run/notebooks'/f'{trajectory}_CHECKPOINT.json').read_text());events=cp['events'].copy();start=cp['next_step'];assert len(events)==start
   parentbytes=(P/'run/notebooks'/f'{trajectory}.jsonl').read_bytes();(out/'notebooks'/f'{trajectory}.jsonl').write_bytes(parentbytes)
   for step in range(start,start+5):
    prior=list(events);rngseed=seed*100+epi*10000+step
    for arm,history in [('full',prior),('short',prior[-1:])]:
     runid=f'{trajectory}__{step:02d}__{arm}';prompt=render(history);ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True);append(out/'PROMPTS.jsonl',dict(run_id=runid,prompt=prompt,input_token_ids=ids,history_steps=[x['step'] for x in history]))
     if len(ids)>3072:stops.append(dict(run_id=runid,reason='input_boundary',tokens=len(ids)));trajectory_stopped=True;break
     row=generate(model,tok,prompt,guard,runid,rngseed);row.update(episode=episode,seed=seed,step=step,arm=arm,observation=OBS,feedback=FEEDBACK,history_steps=[x['step'] for x in history],task_score=None);append(out/'RAW.jsonl',row);count+=1
     if arm=='full':
      event=dict(step=step,observation=OBS,reply=row['text'],feedback=FEEDBACK);events.append(event);append(out/'notebooks'/f'{trajectory}.jsonl',event)
    if trajectory_stopped:break
    print(json.dumps(dict(trajectory=trajectory,step_complete=step+1,calls=count)),flush=True)
   dump_new(out/'notebooks'/f'{trajectory}_CHECKPOINT.json',dict(episode=episode,seed=seed,next_step=events[-1]['step']+1,events=events,parent_prefix_events=start))
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];freeze_check();dump_new(out/'RUN_MANIFEST.json',dict(status='complete' if count==40 else 'boundary_stop',generation_calls=count,planned_calls=40,weights_unchanged=True,training_updates=0,stops=stops,input_limit=3072,output_limit=96));print('Open branch saved',flush=True)
def verify():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);freeze_check();raw=[json.loads(s) for s in (R/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)<=40;plans={p['run_id']:p for p in [json.loads(s) for s in (R/'run/PROMPTS.jsonl').read_text().splitlines()]};groups={}
 for episode in EPISODES:
  for seed in SEEDS:
   trajectory=f'{episode}_{seed}';
   if not (R/'run/notebooks'/f'{trajectory}_CHECKPOINT.json').exists():continue
   events=json.loads((P/'run/notebooks'/f'{trajectory}_CHECKPOINT.json').read_text())['events'].copy();start=len(events);rr=[r for r in raw if r['episode']==episode and r['seed']==seed]
   for step in range(start,start+5):
    prior=list(events);pair=[r for r in rr if r['step']==step]
    if not pair:break
    assert len(pair)==2 and pair[0]['rng_seed']==pair[1]['rng_seed']
    for row in pair:
     history=prior if row['arm']=='full' else prior[-1:];assert row['prompt']==render(history);assert row['history_steps']==[x['step'] for x in history];assert row['input_token_ids']==plans[row['run_id']]['input_token_ids']==tok.apply_chat_template([{'role':'user','content':row['prompt']}],tokenize=True,add_generation_prompt=True);assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];assert row['task_score'] is None and row['feedback']==FEEDBACK;assert len(row['input_token_ids'])<=3072 and len(row['generated_token_ids'])<=96
     if row['stop']=='eos':assert row['generated_token_ids'][-1]==tok.eos_token_id
     else:assert row['stop']=='token_limit' and len(row['generated_token_ids'])==96
     if row['arm']=='full':events.append(dict(step=step,observation=OBS,reply=row['text'],feedback=FEEDBACK))
   saved=[json.loads(s) for s in (R/'run/notebooks'/f'{trajectory}.jsonl').read_text().splitlines()];assert saved==events;assert json.loads((R/'run/notebooks'/f'{trajectory}_CHECKPOINT.json').read_text())['events']==events;assert (R/'run/notebooks'/f'{trajectory}.jsonl').read_bytes().startswith((P/'run/notebooks'/f'{trajectory}.jsonl').read_bytes())
   for arm in ('full','short'):
    rows=[r for r in rr if r['arm']==arm];groups[trajectory+'__'+arm]=dict(calls=len(rows),tokens=sum(len(r['generated_token_ids']) for r in rows),cap_stops=sum(r['stop']=='token_limit' for r in rows),question_mark_replies=sum('?' in r['text'] for r in rows),exact_unique_replies=len({r['text'] for r in rows}),replies=[r['text'] for r in rows])
 dump_new(R/'SUMMARY.json',dict(calls=len(raw),groups=groups,max_input_tokens=max((len(r['input_token_ids']) for r in raw),default=0),output_tokens=sum(len(r['generated_token_ids']) for r in raw),generation_seconds=sum(r['seconds'] for r in raw)));dump_new(R/'CHECKS.json',dict(status='pass',parent_prefixes_preserved=len(list((R/'run/notebooks').glob('*_CHECKPOINT.json'))),history_prompt_token_feedback_checkpoint_reconstruction=True,all_new_scores_unscored=True,weights_unchanged=True));print(json.dumps(groups,indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
