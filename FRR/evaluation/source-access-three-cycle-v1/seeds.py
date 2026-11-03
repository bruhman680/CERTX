"""Persistent external garden with immutable event commits and out-of-band pacing."""
from pathlib import Path
import os,json,sys,time,argparse,hashlib,importlib.util
from io_utils import sha,dump_new,append
from play_tools import dispatch as play_dispatch
R=Path(__file__).resolve().parent;P=R.parent/'source-access-repair-pilot-v1';ENV=R/'cycle3/environment';BRANCH='tools_optional_1201';LIMIT=6144
spec=importlib.util.spec_from_file_location('stable_reader',P/'study.py');parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
def atomic(p,value):
 p=Path(p);tmp=p.with_name(p.name+'.tmp');b=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
 with tmp.open('wb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 os.replace(tmp,p)
def immutable(p,value):
 p=Path(p);tmp=p.with_name(p.name+f'.staging-{os.getpid()}')
 with tmp.open('xb') as f:f.write((json.dumps(value,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
 try:os.link(tmp,p)
 finally:tmp.unlink()
class Journal:
 def __init__(self,path):self.path=Path(path)
 def state(self):
  origin=[json.loads(l) for l in (self.path/'ORIGIN.jsonl').read_text().splitlines()];events=origin.copy();rows=[]
  for p in sorted((self.path/'events').glob('*.json')):
   x=json.loads(p.read_text());assert x['step']==len(events) and p.stem==f"{x['step']:06d}";rows.append(x)
   events.append(dict(step=x['step'],observation='Open exploration patch.',reply=x['text'],feedback=parent.FEEDBACK,host_result=x['host_result']))
  return origin,events,rows
 def commit(self,row):
  _,events,_=self.state();assert row['step']==len(events);immutable(self.path/'events'/f"{row['step']:06d}.json",row);self.project()
 def project(self):
  origin,events,rows=self.state();extra=b''.join((json.dumps(e,sort_keys=True)+'\n').encode() for e in events[len(origin):]);b=(self.path/'ORIGIN.jsonl').read_bytes()+extra
  q=self.path/'NOTEBOOK.jsonl.tmp';q.write_bytes(b);os.replace(q,self.path/'NOTEBOOK.jsonl')
  atomic(self.path/'STATE.json',dict(environment='small-garden-local-v1',origin_entries=len(origin),next_step=len(events),committed_steps=[x['step'] for x in rows],event_sha256={p.name:sha(p) for p in sorted((self.path/'events').glob('*.json'))},manifest_sha256=sha(self.path/'ENVIRONMENT_SEEDS_V1.json'),pause_requested=(self.path/'PAUSE').exists()))
def play_render(events):
 return parent.render(events,'tools_optional')+'\n\nSTABLE PLAY CHARTER:\n'+(R/'PLAY_CHARTER.md').read_text()+'\n\nYour next move:'
def seed_render(events):
 shelf=json.loads((ENV/'seed_shelf/0001.json').read_text())
 cards='\n'.join(x['id']+': '+x['text'] for x in shelf['seeds'])
 return parent.render(events,'tools_optional')+'\n\nOPTIONAL SEED SHELF (operator play prompts, not evidence or tasks):\n'+cards+'\nYou may use, vary, combine, ignore or revisit these. Your own ideas are welcome.\n\nSTABLE PLAY CHARTER:\n'+(R/'PLAY_CHARTER.md').read_text()+'\n\nYour next move:'
def initialize():
 assert (ENV/'PAUSE').exists() and len(Journal(ENV).state()[1])==53
 old=json.loads((ENV/'ENVIRONMENT_PLAY.json').read_text());new=dict(old,version='seed-shelf-v1',previous_manifest_sha256=sha(ENV/'ENVIRONMENT_PLAY.json'),seed_shelf_sha256=sha(ENV/'seed_shelf/0001.json'),same_garden=True,transition_step=53)
 dump_new(ENV/'ENVIRONMENT_SEEDS_V1.json',new);Journal(ENV).project()
 oldfreeze=json.loads((R/'FREEZE_PLAY.json').read_text())['files'];study=R.parent/'seed-shelf-continuation-v1';paths=[R/'seeds.py',R/'test_seeds.py',study/'PROTOCOL.md',ENV/'ENVIRONMENT_SEEDS_V1.json',ENV/'seed_shelf/0001.json']+list((ENV/'events').glob('*.json'))
 dump_new(R/'FREEZE_SEEDS.json',dict(timing='before seed-shelf outputs, same garden at entry 53',files={**oldfreeze,**{str(p):sha(p) for p in paths}}))
def freeze_check():
 for p,h in json.loads((R/'FREEZE_SEEDS.json').read_text())['files'].items():assert sha(Path(p))==h,p
 assert sha(ENV/'ORIGIN.jsonl')==json.loads((ENV/'ENVIRONMENT_SEEDS_V1.json').read_text())['origin_sha256']
 for v in parent.source_db().values():assert sha(Path('/workspace/frr')/v['source_path'].removeprefix('FRR/'))==v['source_sha256']
def wait_pacing(path,delay):
 end=time.monotonic()+delay
 while time.monotonic()<end:
  if (Path(path)/'PAUSE').exists():return False
  time.sleep(min(.25,max(0,end-time.monotonic())))
 return not (Path(path)/'PAUSE').exists()
def run(steps,delay):
 assert 0<steps<=20 and 0<=delay<=45;freeze_check();j=Journal(ENV);j.project()
 if (ENV/'PAUSE').exists():print('Environment paused; no generation.');return
 lock=ENV/'RUN.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  sessions=sorted((ENV/'sessions').glob('*.json'));number=len(sessions);session=f'{number:04d}';resource=ENV/'sessions'/f'{session}_RESOURCE.jsonl';plans=ENV/'plans';start=len(j.state()[1])
  if (plans/f'{start:06d}.json').exists():raise RuntimeError('Uncommitted prompt plan exists: inspect it before any retry')
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_continuous import generate
  m=json.loads((parent.ACQ/'MANIFEST.json').read_text());assert sha(parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2);guard=Guard(5153960755,resource);guard.read('before_model_load');tok=AutoTokenizer.from_pretrained(parent.BASE,local_files_only=True,trust_remote_code=False)
  model=AutoModelForCausalLM.from_pretrained(parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
  count=0;reason='budget_pause';boundary=None
  for k in range(steps):
   if not wait_pacing(ENV,delay):reason='pause_requested';break
   origin,events,rows=j.state();step=len(events);q=seed_render(events);ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);runid=f'continuous_{step:06d}';seed=1201*100+step-45
   immutable(plans/f'{step:06d}.json',dict(run_id=runid,step=step,prompt=q,input_token_ids=ids,rng_seed=seed,environment_sha256=sha(ENV/'ENVIRONMENT_SEEDS_V1.json')))
   if len(ids)>LIMIT:reason='input_boundary';boundary=dict(step=step,tokens=len(ids),run_id=runid);break
   row=generate(model,tok,q,guard,runid,seed);row.update(step=step,environment_version='seed-shelf-v1',host_result=play_dispatch(row['text'],events,parent.dispatch),feedback=parent.FEEDBACK,task_score=None,history_steps=[x['step'] for x in events],environment_sha256=sha(ENV/'ENVIRONMENT_SEEDS_V1.json'));j.commit(row);count+=1;print(json.dumps(dict(run_id=runid,next_step=step+1,calls=count,host_kind=row['host_result']['kind'])),flush=True)
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];freeze_check()
  (ENV/'PAUSE').touch();j.project();dump_new(ENV/'sessions'/f'{session}.json',dict(session=session,start_step=start,next_step=len(j.state()[1]),calls=count,requested_steps=steps,delay_seconds=delay,stop_reason=reason,boundary=boundary,weights_unchanged=True,training_updates=0))
 finally:lock.unlink()
def verify():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 freeze_check();tok=AutoTokenizer.from_pretrained(parent.BASE,local_files_only=True,trust_remote_code=False);j=Journal(ENV);origin,all_events,rows=j.state();events=origin.copy()
 for x in rows:
  step=len(events);assert x['step']==step;plan=json.loads((ENV/'plans'/f'{step:06d}.json').read_text());version=x.get('environment_version');isplay=version in ('play-extension-v1','seed-shelf-v1');expected=seed_render(events) if version=='seed-shelf-v1' else (play_render(events) if isplay else parent.render(events,'tools_optional'));assert x['prompt']==expected==plan['prompt'];assert x['input_token_ids']==plan['input_token_ids']==tok.apply_chat_template([{'role':'user','content':x['prompt']}],tokenize=True,add_generation_prompt=True)
  assert x['rng_seed']==plan['rng_seed']==1201*100+step-45;assert tok.decode(x['generated_token_ids'],skip_special_tokens=True)==x['text'];assert x['host_result']==(play_dispatch(x['text'],events,parent.dispatch) if isplay else parent.dispatch(x['text'],'tools_optional'));assert x['task_score'] is None and x['feedback']==parent.FEEDBACK;assert len(x['input_token_ids'])<=LIMIT and len(x['generated_token_ids'])<=96
  assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
  assert x['environment_sha256']==plan['environment_sha256']==sha(ENV/('ENVIRONMENT_SEEDS_V1.json' if version=='seed-shelf-v1' else ('ENVIRONMENT_PLAY.json' if isplay else 'ENVIRONMENT.json')));assert x['history_steps']==[e['step'] for e in events];events.append(dict(step=step,observation='Open exploration patch.',reply=x['text'],feedback=parent.FEEDBACK,host_result=x['host_result']))
 assert events==all_events;assert (ENV/'NOTEBOOK.jsonl').read_bytes().startswith((ENV/'ORIGIN.jsonl').read_bytes());assert [json.loads(l) for l in (ENV/'NOTEBOOK.jsonl').read_text().splitlines()]==events
 state=json.loads((ENV/'STATE.json').read_text());assert state['next_step']==len(events) and state['event_sha256']=={p.name:sha(p) for p in sorted((ENV/'events').glob('*.json'))}
 sessions=[json.loads(p.read_text()) for p in sorted((ENV/'sessions').glob('*.json'))];assert sum(s['calls'] for s in sessions)==len(rows)
 for s in sessions:
  if s['boundary']:
   b=s['boundary'];plan=json.loads((ENV/'plans'/f"{b['step']:06d}.json").read_text());assert len(plan['input_token_ids'])==b['tokens']>LIMIT and b['step'] not in {x['step'] for x in rows}
 resources=[json.loads(l) for p in (ENV/'sessions').glob('*_RESOURCE.jsonl') for l in p.read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
 checks=dict(status='pass',calls=len(rows),origin_byte_prefix_preserved=True,immutable_event_and_prompt_reconstruction=True,environment_version_verified_per_event=True,pause_marker_present=(ENV/'PAUSE').exists())
 summary=dict(calls=len(rows),next_step=len(events),requested_reads=sum(x['text'].strip().upper() in ('READ SETUP','READ CLAIM') for x in rows),executed_reads=sum(x['host_result']['kind']=='source_receipt' for x in rows),cap_stops=sum(x['stop']=='token_limit' for x in rows),max_input_tokens=max((len(x['input_token_ids']) for x in rows),default=0),output_tokens=sum(len(x['generated_token_ids']) for x in rows),generation_seconds=sum(x['seconds'] for x in rows),sampled_max_working_bytes=max(x['working_estimate'] for x in resources),sessions=sessions)
 index=dict(rows=[dict(run_id=x['run_id'],step=x['step'],host_kind=x['host_result']['kind'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop'],literal_patch_set_phrase='hugging face' in x['text'].lower() and 'patch' in x['text'].lower()) for x in rows])
 vdir=R/'cycle3/verification';vid=f"{len(list(vdir.glob('*_CHECKS.json'))):04d}"
 for name,value in [('CHECKS',checks),('SUMMARY',summary),('EVENT_INDEX',index)]:
  dump_new(vdir/f'{vid}_{name}.json',value)
  if not (R/f'cycle3/{name}.json').exists():dump_new(R/f'cycle3/{name}.json',value)
 atomic(R/'cycle3/CURRENT_VERIFY.json',dict(verification=vid,checks=f'verification/{vid}_CHECKS.json',summary=f'verification/{vid}_SUMMARY.json',index=f'verification/{vid}_EVENT_INDEX.json',next_step=len(events)))
 print('Continuous environment verified: '+vid)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=('init','run','verify','pause','resume'));p.add_argument('--steps',type=int,default=3);p.add_argument('--delay',type=float,default=0);a=p.parse_args()
 if a.action=='init':initialize()
 elif a.action=='run':run(a.steps,a.delay)
 elif a.action=='verify':verify()
 elif a.action=='pause':(ENV/'PAUSE').touch();Journal(ENV).project();print('Pause requested; active call may finish before pause.')
 elif a.action=='resume':(ENV/'PAUSE').unlink(missing_ok=True);Journal(ENV).project();print('Resume armed; no model call until run is invoked.')
