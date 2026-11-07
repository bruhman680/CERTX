"""Final frozen garden contract: durable continuation after entry850.

Only prepare/start/resume under the recorded contract. No inference on import.
Observer cadence changes never alter model-facing state, messages or sampling.
"""
from pathlib import Path
import argparse,base64,hashlib,json,os,shutil,sys,traceback,uuid
H=Path(__file__).resolve().parent;F=H.parent.parent
P=H.parent/'cloud-garden-750-to-850-v1';PR=P/'run'
G=H.parent/'source-access-three-cycle-v1';E=G/'cycle3/environment'
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
WEIGHTS='5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c'
SEED='Follow your curiosity and explore your universe. You may play, observe, wonder, experiment, and learn. 😁'
R=H/'run';CONTRACT=H/'CONTRACT.json'
sys.path[:0]=[str(H),str(G),'/workspace']
from world import World,NOTICE,receive,action,immutable,sha,stable

def read(p):return json.loads(Path(p).read_text())
def digest(p):return sha(Path(p).read_bytes())
def atomic(p,value):
 p=Path(p);q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(value,sort_keys=True)+'\n');os.replace(q,p)
def file_inventory(root):
 root=Path(root)
 return {str(p.relative_to(root)):digest(p) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def rows():return [read(p) for p in sorted((R/'events').glob('*.json'))]
def parent_rows():return [read(p) for p in sorted((PR/'events').glob('*.json'))]
def bundle_id(bundle):return sha(stable({'entries':bundle['entries'],'root_mode':bundle['root_mode']}))
def state():return read(R/'STATE.json')
def entry_seed(entry):return 120100+entry-1-45

def model_feedback(feedback):
 if feedback is None:return None
 return {k:feedback[k] for k in ['stdout','stderr','exit_code','boundary']}

def native_messages(before,current_rows):
 """No stock behavioral system text; twelve raw replies cross the boundary."""
 history=(parent_rows()+current_rows)[-12:]
 messages=[{'role':'system','content':''},{'role':'user','content':NOTICE+'\n\n'+SEED}]
 for row in history:
  messages.append({'role':'assistant','content':row['text']})
  feedback=model_feedback(row['visible_feedback'])
  messages.append({'role':'user','content':'' if feedback is None else json.dumps(feedback,ensure_ascii=False,sort_keys=True)})
 names=sorted(set(x[0].split('/')[0] for x in before['entries']))
 messages[-1]['content']+='\nDirectory entries: '+json.dumps(names,ensure_ascii=False)
 return messages

def contract_check():
 c=read(CONTRACT)
 assert isinstance(c['version'],str) and c['parent_entry']==850 and c['seed']==SEED
 return c

def prepare():
 c=contract_check();assert not R.exists(),'Never replace an existing phase state'
 assert read(PR/'STATE.json')['next_entry']==850 and read(PR/'STATE.json')['paused']
 assert (PR/'PAUSE').exists() and not (PR/'PENDING.json').exists() and not (PR/'RUN.lock').exists()
 assert read(P/'INDEPENDENT_FINAL_CHECK.json')['status']=='pass'
 R.mkdir()
 for name in ['events','plans','raw','results','bundles','objects','sessions','checks','reports','observer']:(R/name).mkdir()
 immutable(R/'PARENT_INVENTORY.json',file_inventory(P));immutable(R/'ORIGINAL_PRIMARY_INVENTORY.json',file_inventory(E))
 immutable(R/'PARENT_ACTIVE_POINTER.json',read(F/'ACTIVE_GARDEN_PHASE.json'))
 shutil.copytree(PR/'objects',R/'objects',dirs_exist_ok=True)
 parent_bundle=read(PR/'bundles/000850.json')
 assert parent_bundle==read(PR/'PAUSED_WORLD.json') and parent_bundle['id']==bundle_id(parent_bundle)
 # Byte-identical copy, not merely equivalent reconstruction.
 shutil.copyfile(PR/'bundles/000850.json',R/'bundles/000850.json')
 w=World()
 try:
  w.restore(parent_bundle,R/'objects');assert w.capture(R/'objects')==parent_bundle
 finally:w.close()
 pins={str(p):digest(p) for p in [H/'runner.py',H/'generation.py',H/'world.py',H/'server.py',CONTRACT,H/'HOST_RUNTIME_IDENTITY.json',G/'runtime_reference.py',BASE/'config.json',BASE/'tokenizer_config.json',BASE/'tokenizer.json']}
 manifest=dict(version=c['version'],parent_entry=850,parent_event_sha256=digest(PR/'events/000850.json'),
   parent_manifest_sha256=digest(PR/'MANIFEST.json'),parent_phase=str(P.relative_to(F)),
   initial_bundle_sha256=digest(R/'bundles/000850.json'),initial_bundle_id=parent_bundle['id'],
   parent_inventory_sha256=digest(R/'PARENT_INVENTORY.json'),original_inventory_sha256=digest(R/'ORIGINAL_PRIMARY_INVENTORY.json'),
   contract_sha256=digest(CONTRACT),code_pins=pins,base_model=str(BASE),weights_sha256=WEIGHTS,
   added_adapter=False,training_updates=0,message_policy='empty system; fixed facts+agreed seed; last12 assistant replies and user actual consequences, crossing850; current directory facts in finaluser',
   input_limit=8096,output_limit=96,temperature=.8,top_p=.9,torch_threads=2,max_block=250,
   integrity_interval=10,report_interval=50,observer_zoom_entries=5,world_notice=NOTICE)
 immutable(R/'MANIFEST.json',manifest)
 atomic(R/'STATE.json',dict(next_entry=850,paused=True,latest_bundle='000850.json',last_event_sha256=manifest['parent_event_sha256']))
 (R/'PAUSE').touch()
 print(json.dumps({'prepared':True,'parent_entry':850,'initial_bundle_byte_identical':True,'world_unchanged':True}),flush=True)

def verify_pins():
 m=read(R/'MANIFEST.json');contract_check()
 assert digest(CONTRACT)==m['contract_sha256']
 assert digest(R/'PARENT_INVENTORY.json')==m['parent_inventory_sha256']
 assert digest(R/'ORIGINAL_PRIMARY_INVENTORY.json')==m['original_inventory_sha256']
 assert file_inventory(P)==read(R/'PARENT_INVENTORY.json'),'Parent stage changed'
 assert file_inventory(E)==read(R/'ORIGINAL_PRIMARY_INVENTORY.json'),'Original stage changed'
 assert digest(PR/'MANIFEST.json')==m['parent_manifest_sha256']
 assert digest(PR/'events/000850.json')==m['parent_event_sha256']
 assert digest(R/'bundles/000850.json')==m['initial_bundle_sha256']
 assert (R/'bundles/000850.json').read_bytes()==(PR/'bundles/000850.json').read_bytes()
 for p,h in m['code_pins'].items():assert digest(p)==h,p
 assert digest(BASE/'model.safetensors')==WEIGHTS
 for p,h in read(H/'HOST_RUNTIME_IDENTITY.json')['critical_guest_executables_sha256'].items():assert digest(p)==h,p
 return m

def validate(w,tok,model=None):
 m=verify_pins();allrows=rows();previous=read(R/'bundles/000850.json');last=m['parent_event_sha256']
 assert previous['id']==bundle_id(previous)==m['initial_bundle_id']
 for entry,row in enumerate(allrows,851):
  assert row['entry']==entry and row['parent_event_sha256']==last
  plan=read(R/'plans'/f'{entry:06d}.json');raw=read(R/'raw'/f'{entry:06d}.json');result=read(R/'results'/f'{entry:06d}.json')
  assert plan['entry']==entry and plan['manifest_sha256']==digest(R/'MANIFEST.json')
  assert plan['before_id']==row['before_id']==previous['id']
  assert row['raw_sha256']==digest(R/'raw'/f'{entry:06d}.json')
  messages=native_messages(previous,allrows[:entry-851])
  assert messages==plan['messages']==raw['messages']==row['messages']
  assert messages[0]=={'role':'system','content':''}
  ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
  assert ids==plan['input_token_ids']==raw['input_token_ids'] and len(ids)<=8096
  assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==row['text']
  assert 0<len(raw['generated_token_ids'])<=96
  assert raw['rng_seed']==plan['rng_seed']==entry_seed(entry)
  assert raw['stop']==row['stop']
  assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
  assert result==row['result'] and row['visible_feedback']==model_feedback(result['feedback'])
  assert result['kind']==('shell' if action(raw['text']) is not None else 'notebook')
  after=read(R/'bundles'/f'{entry:06d}.json');assert after['id']==bundle_id(after)==row['after_id']
  previous=after;last=digest(R/'events'/f'{entry:06d}.json')
 s=state();assert s['next_entry']==850+len(allrows) and s['last_event_sha256']==last
 assert s['latest_bundle']==f"{s['next_entry']:06d}.json"
 # Validate all retained bytes, including inactive objects inherited from parent.
 object_count=0
 for p in (R/'objects').glob('*.json'):
  q=read(p);b=base64.b64decode(q['base64'],validate=True)
  assert sha(b)==p.stem==q['sha256'] and len(b)==q['bytes'];object_count+=1
 assert w.capture(R/'objects')==previous
 restored=World()
 try:
  restored.restore(previous,R/'objects');assert restored.capture(R/'objects')==previous
 finally:restored.close()
 if model is not None:
  from runtime_reference import parameter_digest
  assert parameter_digest(model,False)==read(R/'MODEL_CONDITION.json')['tensor_digest']
 return dict(status='pass',entry=s['next_entry'],new_entries=len(allrows),parent850_unchanged=True,
    original750_unchanged=True,record_chain=True,messages_reconstructed=True,
    tokens_and_stops_verified=True,objects_verified=object_count,world_matches_bundle=True,
    fresh_mount_restoration=True,model_weights_unchanged=True,training_updates=0)

def report(start,end):
 batch=[r for r in rows() if start<r['entry']<=end]
 kinds={k:sum(r['result']['kind']==k for r in batch) for k in ['notebook','shell']}
 value=dict(from_exclusive=start,through_entry=end,entries=len(batch),kinds=kinds,
    notebook_storage_faults=sum(r['result']['kind']=='notebook' and r['visible_feedback'] is not None for r in batch),
    shell_exit_codes=[r['visible_feedback']['exit_code'] for r in batch if r['result']['kind']=='shell'],
    eos=sum(r['stop']=='eos' for r in batch),token_cap=sum(r['stop']=='token_limit' for r in batch),
    distinct_texts=len(set(r['text'] for r in batch)))
 immutable(R/'reports'/f'{start+1:06d}_{end:06d}.json',value);print(json.dumps({'report':value}),flush=True)

def preflight():
 """Complete no-model world reconstruction and token-framing checks."""
 verify_pins()
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 w=World()
 try:
  w.restore(read(R/'bundles'/state()['latest_bundle']),R/'objects')
  check=validate(w,tok)
  messages=native_messages(w.capture(R/'objects'),rows())
  rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
  assert rendered.startswith('<|im_start|>system\n<|im_end|>\n<|im_start|>user\n')
  assert messages[0]['content']==''
  assert [x['content'] for x in messages if x['role']=='assistant']==[r['text'] for r in (parent_rows()+rows())[-12:]]
  assert len(tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True))<=8096
  check.update(empty_system_verified=True,parent_recent_replies_preserved=True,model_calls=0)
 finally:w.close()
 print(json.dumps(check),flush=True);return check

def observer_request(entry,seen):
 p=R/'observer/ZOOM_REQUEST.json'
 if not p.exists():return seen,None,None
 try:raw=p.read_bytes()
 except OSError as error:return seen,None,str(error)
 key=sha(raw)
 if key==seen:return seen,None,None
 try:
  request=json.loads(raw);through=request['through_entry']
  if type(through) is not int or through<0:raise ValueError('through_entry must be a nonnegative integer')
  if through<entry:return key,None,None
  if through>entry+4:raise ValueError('External zoom request must cover at most five entries including the current entry')
  return key,through-entry+1,None
 except (ValueError,TypeError,KeyError) as error:return key,None,str(error)

def _run_locked(command,steps,start,target,session,integrity_every,report_every):
 s=state();assert s['next_entry']==start and s['paused']
 for name,value in {'HF_HUB_OFFLINE':'1','HF_HUB_DISABLE_PROGRESS_BARS':'1','OMP_NUM_THREADS':'2','MKL_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1'}.items():os.environ[name]=value
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from generation import generate
 torch.set_num_threads(2)
 assert not (R/'sessions'/f'{session}_PLAN.json').exists(),'Session already attempted'
 immutable(R/'sessions'/f'{session}_PLAN.json',dict(start=start,target=target,steps=steps,integrity_every=integrity_every,report_every=report_every,contract_sha256=digest(CONTRACT),manifest_sha256=digest(R/'MANIFEST.json')))
 guard=Guard(5153960755,R/'sessions'/f'{session}_RESOURCE.jsonl');guard.read('before_model_load')
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 model.requires_grad_(False);model.eval();model_digest=parameter_digest(model,False)
 condition=R/'MODEL_CONDITION.json'
 if condition.exists():assert read(condition)['tensor_digest']==model_digest
 else:immutable(condition,dict(tensor_digest=model_digest,weights_sha256=WEIGHTS,added_adapter=False,trainable_parameters=0,training_updates=0))
 w=World();calls=0;reason='completed';last_report=start;zoom_remaining=0;request_seen=None
 try:
  w.restore(read(R/'bundles'/s['latest_bundle']),R/'objects')
  initial=validate(w,tok,model);immutable(R/'sessions'/f'{session}_PRECHECK.json',initial)
  (R/'PAUSE').unlink();s['paused']=False;atomic(R/'STATE.json',s)
  for entry in range(start+1,target+1):
   if (R/'STOP').exists() or (R/'PAUSE').exists():reason='explicit_pause';break
   current=rows();before=w.capture(R/'objects');messages=native_messages(before,current)
   ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);assert len(ids)<=8096
   plan=dict(entry=entry,messages=messages,input_token_ids=ids,rng_seed=entry_seed(entry),before_id=before['id'],manifest_sha256=digest(R/'MANIFEST.json'))
   immutable(R/'plans'/f'{entry:06d}.json',plan)
   immutable(R/'PENDING.json',dict(entry=entry,status='plan-before-generation; interrupted action outcome must be inspected, never replayed automatically'))
   raw=generate(model,tok,messages,guard,f'final_garden_{entry:06d}',entry_seed(entry));calls+=1
   immutable(R/'raw'/f'{entry:06d}.json',raw)
   result=receive(w,raw['text']);immutable(R/'results'/f'{entry:06d}.json',result)
   after=w.capture(R/'objects');immutable(R/'bundles'/f'{entry:06d}.json',after)
   row=dict(entry=entry,messages=messages,text=raw['text'],stop=raw['stop'],parent_event_sha256=state()['last_event_sha256'],before_id=before['id'],after_id=after['id'],result=result,visible_feedback=model_feedback(result['feedback']),raw_sha256=digest(R/'raw'/f'{entry:06d}.json'))
   immutable(R/'events'/f'{entry:06d}.json',row)
   atomic(R/'STATE.json',dict(next_entry=entry,paused=False,latest_bundle=f'{entry:06d}.json',last_event_sha256=digest(R/'events'/f'{entry:06d}.json')))
   (R/'PENDING.json').unlink()
   non_notebook_change=({'root_mode':before['root_mode'],'entries':[x for x in before['entries'] if x[0]!='notebook.txt']}!={'root_mode':after['root_mode'],'entries':[x for x in after['entries'] if x[0]!='notebook.txt']})
   event=result['kind']=='shell' or result['feedback'] is not None or non_notebook_change
   if event:
    zoom_remaining=6
    immutable(R/'observer'/f'{entry:06d}_ZOOM.json',dict(entry=entry,reason='explicit_action_or_actual_environment_error_or_non_notebook_delta',next_entries=5,model_facing_changes=False))
   # External requests are consumed once and bounded to 1–5 entries.
   request_seen,requested_zoom,request_error=observer_request(entry,request_seen)
   if requested_zoom is not None:zoom_remaining=max(zoom_remaining,requested_zoom)
   if request_error is not None:
    immutable(R/'observer'/f'{session}_{entry:06d}_REQUEST_ERROR.json',dict(kind='external_observer_request_error',message=request_error,model_facing_changes=False))
   if (entry-850)%integrity_every==0 or zoom_remaining>0:
    check=validate(w,tok,model)
    immutable(R/'checks'/f'{entry:06d}.json',check);print(json.dumps({'integrity':check}),flush=True)
   if zoom_remaining>0:zoom_remaining-=1
   if entry-last_report>=report_every:report(last_report,entry);last_report=entry
  if state()['next_entry']>last_report:report(last_report,state()['next_entry'])
  final=validate(w,tok,model);immutable(R/'sessions'/f'{session}_FINAL_CHECK.json',final)
 except BaseException as error:
  reason='interrupted_or_failed'
  immutable(R/'sessions'/f'{session}_ERROR.json',dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc(),pending=(R/'PENDING.json').exists()))
  raise
 finally:
  try:
   immutable(R/'sessions'/f'{session}_PAUSED_WORLD.json',w.capture(R/'objects'))
  except BaseException as error:
   reason='interrupted_or_failed'
   immutable(R/'sessions'/f'{session}_CAPTURE_ERROR.json',dict(type=type(error).__name__,message=str(error),changes_after_last_committed_bundle='unknown'))
   raise
  finally:
   w.close()
   s=state()
   immutable(R/'sessions'/f'{session}_RESULT.json',dict(start=start,target=target,actual_end=s['next_entry'],calls=calls,reason=reason,training_updates=0,contract_sha256=digest(CONTRACT)))

def run_block(command,steps,integrity_every=10,report_every=50):
 assert type(steps) is int and 0<steps<=250
 assert type(integrity_every) is int and 1<=integrity_every<=10
 assert report_every in [50,100]
 # Exclusive ownership is acquired before model/session side effects. A losing
 # concurrent invocation never pauses or deletes the winning invocation's lock.
 verify_pins();s=state();start=s['next_entry'];target=start+steps
 assert s['paused'] and (R/'PAUSE').exists()
 assert not (R/'PENDING.json').exists(),'Uncertain attempt: inspect, do not repeat automatically'
 assert not (R/'plans'/f'{start+1:06d}.json').exists(),'Outstanding plan: inspect, never regenerate silently'
 assert (command=='start' and start==850) or (command=='resume' and start>=850)
 pointer=read(F/'ACTIVE_GARDEN_PHASE.json')
 assert pointer['phase']==str(H.relative_to(F)) and pointer['state']==str((R/'STATE.json').relative_to(F)),'Activate final phase pointer explicitly before inference'
 token=uuid.uuid4().hex
 fd=os.open(R/'RUN.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY)
 with os.fdopen(fd,'w') as f:json.dump({'pid':os.getpid(),'token':token},f);f.flush();os.fsync(f.fileno())
 session=f"{len(list((R/'sessions').glob('*_PLAN.json'))):04d}_{start:06d}_{target:06d}"
 try:
  _run_locked(command,steps,start,target,session,integrity_every,report_every)
 except BaseException as error:
  error_path=R/'sessions'/f'{session}_ERROR.json'
  if not error_path.exists():immutable(error_path,dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc(),pending=(R/'PENDING.json').exists()))
  raise
 finally:
  # This outer cleanup also covers model-load and initial-world failures.
  owns=False
  try:owns=read(R/'RUN.lock').get('token')==token
  except (OSError,ValueError,AttributeError):pass
  if owns:
   s=state();s['paused']=True;atomic(R/'STATE.json',s);(R/'PAUSE').touch()
   (R/'RUN.lock').unlink()
 print(json.dumps({'paused_at':state()['next_entry'],'session':session,'result':read(R/'sessions'/f'{session}_RESULT.json')}),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','preflight','start','resume','verify']);parser.add_argument('--steps',type=int);parser.add_argument('--integrity-every',type=int,choices=range(1,11),default=10);parser.add_argument('--report-every',type=int,choices=[50,100],default=50)
 args=parser.parse_args()
 if args.command=='prepare':prepare()
 elif args.command in ['preflight','verify']:preflight()
 else:
  if args.steps is None:parser.error('--steps is required')
  run_block(args.command,args.steps,args.integrity_every,args.report_every)
