from pathlib import Path
import os,json,sys,hashlib
from collections import Counter
from io_utils import sha,dump_new,append
from design import schedule,render,answer,feedback,SEEDS
R=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=R.parent/'simple-readout-acquisition-v1/run/canonical';EPISODES=('persistent_failure','evidence_availability')
def freeze_check():
 f=json.loads((R/'FREEZE.json').read_text());assert all(sha(Path(p))==v for p,v in f['files'].items())
def prepare():
 dump_new(R/'SCHEDULE.json',{e:schedule(e) for e in EPISODES})
 ps=[p for p in R.iterdir() if p.suffix=='.py']+[R/'PROTOCOL.md',R/'SCHEDULE.json',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json',BASE/'config.json']
 dump_new(R/'FREEZE.json',{'timing':'before model loading and all trajectory outputs','files':{str(p):sha(p) for p in ps}})
def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from lora_cpu import inject_lora,load_adapter
 from runtime_reference import Guard,parameter_digest
 from generate import generate
 freeze_check();out=R/'run';out.mkdir();(out/'notebooks').mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');manifest=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==manifest['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73107);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=manifest['base_pin']);model.eval();assert parameter_digest(model,True)==manifest['final_digest'] and parameter_digest(model,False)==manifest['base_digest_after']
 count=0;stops=[]
 for epindex,episode in enumerate(EPISODES):
  for seed in SEEDS:
   events=[];trajectory=f'{episode}_{seed}'
   for current in schedule(episode):
    prior=list(events);step=current['step'];rngseed=seed*100+epindex*10000+step
    for arm,history in [('full',prior),('short',prior[-1:])]:
     runid=f'{trajectory}__{step:02d}__{arm}';prompt=render(current['observation'],history);ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
     append(out/'PROMPTS.jsonl',dict(run_id=runid,episode=episode,seed=seed,step=step,arm=arm,prompt=prompt,input_token_ids=ids,history_steps=[x['step'] for x in history],history_sha256=hashlib.sha256(json.dumps(history,sort_keys=True).encode()).hexdigest()))
     if len(ids)>2048:
      stops.append(dict(run_id=runid,reason='input_boundary',input_tokens=len(ids)));break
     row=generate(model,tok,prompt,guard,runid,rngseed);a=answer(row['text']);f=feedback(row['text'],current['expected']);row.update(episode=episode,seed=seed,step=step,arm=arm,state=current['state'],expected=current['expected'],phase=current['phase'],observation=current['observation'],history_steps=[x['step'] for x in history],answer=a,correct=(a==current['expected']) if a is not None else None,feedback=f);append(out/'RAW.jsonl',row);count+=1
     if arm=='full':
      event=dict(step=step,observation=current['observation'],reply=row['text'],feedback=f);events.append(event);append(out/'notebooks'/f'{trajectory}.jsonl',event)
    if stops:break
    print(json.dumps({'trajectory':trajectory,'round_complete':step+1,'calls':count}),flush=True)
   dump_new(out/'notebooks'/f'{trajectory}_CHECKPOINT.json',dict(episode=episode,seed=seed,next_step=(events[-1]['step']+1 if events else 0),events=events,planned_schedule_exhausted=len(events)==10))
   if stops:break
  if stops:break
 assert parameter_digest(model,True)==manifest['final_digest'] and parameter_digest(model,False)==manifest['base_digest_after'];assert sha(BASE/'model.safetensors')==manifest['base_pin']['weights_sha256'];freeze_check();dump_new(out/'RUN_MANIFEST.json',dict(status='complete' if count==80 else 'boundary_stop',generation_calls=count,planned_calls=80,training_updates=0,weights_unchanged=True,stops=stops,input_limit=2048,output_limit=64,temperature=.8,top_p=.9));print('Exploration batch saved',flush=True)
def verify():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);freeze_check();raw=[json.loads(x) for x in (R/'run/RAW.jsonl').read_text().splitlines()];plans={x['run_id']:x for x in [json.loads(s) for s in (R/'run/PROMPTS.jsonl').read_text().splitlines()]};groups={};initial_pairs=0
 for episode in EPISODES:
  for seed in SEEDS:
   rows=[r for r in raw if r['episode']==episode and r['seed']==seed];events=[]
   for step,current in enumerate(schedule(episode)):
    pair=[x for x in rows if x['step']==step]
    if not pair:break
    prior=list(events)
    for row in pair:
     history=prior if row['arm']=='full' else prior[-1:];assert row['prompt']==render(current['observation'],history);assert row['history_steps']==[e['step'] for e in history];p=plans[row['run_id']];assert p['history_sha256']==hashlib.sha256(json.dumps(history,sort_keys=True).encode()).hexdigest();assert p['prompt']==row['prompt'];assert p['input_token_ids']==row['input_token_ids']==tok.apply_chat_template([{'role':'user','content':row['prompt']}],tokenize=True,add_generation_prompt=True);assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];assert row['answer']==answer(row['text']);assert row['feedback']==feedback(row['text'],current['expected']);assert row['correct']==((row['answer']==current['expected']) if row['answer'] is not None else None);assert len(row['input_token_ids'])<=2048 and len(row['generated_token_ids'])<=64
     if row['stop']=='eos':assert row['generated_token_ids'][-1]==tok.eos_token_id
     else:assert row['stop']=='token_limit' and len(row['generated_token_ids'])==64
     if row['arm']=='full':events.append(dict(step=step,observation=row['observation'],reply=row['text'],feedback=row['feedback']))
    if step==0 and len(pair)==2:assert pair[0]['input_token_ids']==pair[1]['input_token_ids'] and pair[0]['generated_token_ids']==pair[1]['generated_token_ids'];initial_pairs+=1
   path=R/'run/notebooks'/f'{episode}_{seed}.jsonl'
   if path.exists():assert [json.loads(s) for s in path.read_text().splitlines()]==events
   cp=R/'run/notebooks'/f'{episode}_{seed}_CHECKPOINT.json'
   if cp.exists():assert json.loads(cp.read_text())['events']==events
   for arm in ('full','short'):
    rr=[x for x in rows if x['arm']==arm];adj=[(a,b) for a,b in zip(rr,rr[1:]) if a['observation']==b['observation']];groups[f'{episode}__{seed}__{arm}']=dict(calls=len(rr),recognized=sum(x['answer'] is not None for x in rr),correct=sum(x['correct'] is True for x in rr),incorrect=sum(x['correct'] is False for x in rr),unscored=sum(x['correct'] is None for x in rr),answers=dict(Counter(x['answer'] or 'UNSCORED' for x in rr)),cap_stops=sum(x['stop']=='token_limit' for x in rr),question_mark_replies=sum('?' in x['text'] for x in rr),identical_observation_transitions=len(adj),repairs=sum(a['correct'] is False and b['correct'] is True for a,b in adj),harms=sum(a['correct'] is True and b['correct'] is False for a,b in adj),recognized_answer_changes=sum(a['answer']!=b['answer'] for a,b in adj),tail_answers=[x['answer'] for x in rr[-4:]])
 dump_new(R/'SUMMARY.json',dict(groups=groups,calls=len(raw),paired_rounds=sum(1 for r in raw if r['arm']=='short'),paired_answer_differences=sum(a['answer']!=b['answer'] for a,b in zip(raw[::2],raw[1::2])),max_input_tokens=max(len(r['input_token_ids']) for r in raw),output_tokens=sum(len(r['generated_token_ids']) for r in raw),generation_seconds=sum(r['seconds'] for r in raw)))
 dump_new(R/'CHECKS.json',dict(status='pass',trajectory_rows=len(raw),first_round_exact_pairs=initial_pairs,history_prompt_token_feedback_notebook_reconstruction=True,weights_unchanged=json.loads((R/'run/RUN_MANIFEST.json').read_text())['weights_unchanged']));print(json.dumps(groups,indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
