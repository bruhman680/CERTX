"""Versioned continuation phase after 750. No inference on import."""
from pathlib import Path
import base64,hashlib,json,os,sys,time
H=Path(__file__).resolve().parent;F=H.parent.parent;G=H.parent/'source-access-three-cycle-v1';E=G/'cycle3/environment'
sys.path[:0]=[str(G),'/workspace']
from world import World,NOTICE,receive,immutable,sha,stable
R=H/'run';BASE=Path('/workspace/cache_backend_models/smollm2-135m');WEIGHTS='5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c'

def disksha(p):return sha(Path(p).read_bytes())
def read(p):return json.loads(Path(p).read_text())
def inventory():return {str(p.relative_to(E)):disksha(p) for p in E.rglob('*') if p.is_file()}
def atomic(p,value):
 p=Path(p);temp=p.with_suffix('.tmp');temp.write_text(json.dumps(value,sort_keys=True)+'\n');os.replace(temp,p)
def records():return [read(p) for p in sorted((R/'events').glob('*.json'))]
def render(before,rows):
 names=sorted(set(x[0].split('/')[0] for x in before['entries']))
 return NOTICE+'\nDirectory entries: '+json.dumps(names)+'\nRecent replies and environment results:\n'+json.dumps([{'text':r['text'],'environment_result':r['visible_feedback']} for r in rows[-12:]],ensure_ascii=False)+'\n'

def prepare():
 assert read(E/'STATE.json')['next_step']==750 and (E/'PAUSE').exists()
 R.mkdir();(R/'events').mkdir();(R/'plans').mkdir();(R/'raw').mkdir();(R/'results').mkdir();(R/'bundles').mkdir();(R/'objects').mkdir()
 immutable(R/'PRIMARY_INVENTORY.json',inventory())
 w=World()
 try:
  prior=[json.loads(l) for l in (E/'NOTEBOOK.jsonl').read_text().splitlines()];assert len(prior)==750
  (w.home/'prior_replies.jsonl').write_text(''.join(json.dumps({'entry':r['step']+1,'text':r['reply']},ensure_ascii=False)+'\n' for r in prior))
  matrices=read(H.parent/'minimal-markov-preparation-v1/TABLE_VIEW_DRAFT.json')['material']
  (w.home/'transitions.json').write_text(json.dumps({'states':list(range(8)),'transition_matrices':matrices}))
  (w.home/'LAWS.txt').write_text('Each matrix describes a separate discrete-time system on states 0 through 7. Entry [i][j] is the probability of next state j given current state i. Rows sum to one. No simulation advances automatically. prior_replies.jsonl contains model replies from the earlier environment.\n')
  (w.home/'notebook.txt').write_text('')
  initial=w.capture(R/'objects');immutable(R/'bundles/000750.json',initial)
 finally:w.close()
 code_pins={str(p):disksha(p) for p in [H/'world.py',H/'server.py',H/'run.py',G/'generate_capacity.py',G/'runtime_reference.py',BASE/'config.json',BASE/'tokenizer_config.json']}
 immutable(R/'MANIFEST.json',dict(version='cloud-garden-continuation-v1',parent_entry=750,target_entry=850,
   primary_inventory_sha256=disksha(R/'PRIMARY_INVENTORY.json'),parent_notebook_sha256=disksha(E/'NOTEBOOK.jsonl'),
   parent_state_sha256=disksha(E/'STATE.json'),initial_bundle_sha256=disksha(R/'bundles/000750.json'),
   model=str(BASE),base_weights_sha256=WEIGHTS,added_adapter=False,training_updates=0,
   memory_policy='current phase last 12 replies and actual consequences; all old replies available as mutable world file, external original retained',
   world_notice=NOTICE,code_pins=code_pins,probe_calls_not_primary=True,
   limits={'world_bytes':8388608,'tmp_bytes':8388608,'per_process_address_space':33554432,'shared_uid_processes':128,'wall_seconds':3,'per_file_bytes':262144,'output_bytes':8192},
   changes=['withdraw operator behavioral charters and promoted user seed','raw writing defaults to notebook','explicit JSON action interface','persistent tmpfs world with externally retained bundles','base model without added canonical adapter','new phase prompt and sliding context'],
   lineage='Continuation after 750, not reset; old stage frozen, not replayed by new reducer'))
 atomic(R/'STATE.json',dict(next_entry=750,paused=True,latest_bundle='000750.json',last_event_sha256=None))

def validate(w,tok,model=None):
 m=read(R/'MANIFEST.json');assert inventory()==read(R/'PRIMARY_INVENTORY.json')
 for p,digest in m['code_pins'].items():assert disksha(p)==digest,p
 assert disksha(BASE/'model.safetensors')==WEIGHTS
 assert disksha(R/'bundles/000750.json')==m['initial_bundle_sha256']
 rows=records();previous=read(R/'bundles/000750.json');last=None
 for i,r in enumerate(rows,751):
  assert r['entry']==i and r['parent_event_sha256']==last
  plan=read(R/'plans'/f'{i:06d}.json');raw=read(R/'raw'/f'{i:06d}.json');result=read(R/'results'/f'{i:06d}.json')
  assert r['raw_sha256']==disksha(R/'raw'/f'{i:06d}.json')
  assert plan['manifest_sha256']==disksha(R/'MANIFEST.json')
  from world import action
  assert result['kind']==('shell' if action(raw['text']) is not None else 'notebook')
  assert plan['before_id']==previous['id']
  prompt=render(previous,rows[:i-751]);assert plan['prompt']==raw['prompt']==r['prompt']==prompt
  ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
  assert ids==raw['input_token_ids']==plan['input_token_ids']
  assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==r['text']
  assert 0<len(raw['generated_token_ids'])<=96 and len(ids)<=8096
  assert raw['rng_seed']==plan['rng_seed']==120100+(i-1)-45
  assert result==r['result'] and r['visible_feedback']==result['feedback']
  after=read(R/'bundles'/f'{i:06d}.json');assert after['id']==sha(stable({'entries':after['entries'],'root_mode':after['root_mode']}))==r['after_id']
  assert r['before_id']==previous['id'];previous=after;last=disksha(R/'events'/f'{i:06d}.json')
 state=read(R/'STATE.json');assert state['next_entry']==750+len(rows) and state['last_event_sha256']==last
 assert state['latest_bundle']==f"{750+len(rows):06d}.json"
 assert w.capture(R/'objects')==previous
 # Independent portable reconstruction of current live world, no guest code replay.
 check=World()
 try:
  check.restore(previous,R/'objects');assert check.capture(R/'objects')==previous
 finally:check.close()
 from runtime_reference import parameter_digest
 if model is not None:assert parameter_digest(model,False)==read(R/'MODEL_CONDITION.json')['tensor_digest']
 return dict(status='pass',next_entry=state['next_entry'],events=len(rows),old_primary_unchanged=True,
             record_chain=True,prompts_reconstructed=True,tokens_decoded=True,world_matches_bundle=True,
             independent_restore=True,model_weights_unchanged=True,training_updates=0)

def summary(entry):
 rows=records()[-20:]
 value={'through_entry':entry,'entries':len(rows),'notebook':sum(r['result']['kind']=='notebook' for r in rows),
 'shell':sum(r['result']['kind']=='shell' for r in rows),
 'shell_exit_codes':[r['result']['feedback']['exit_code'] for r in rows if r['result']['kind']=='shell'],
 'notebook_storage_faults':sum(r['result']['kind']=='notebook' and r['result']['feedback'] is not None for r in rows),
 'stop_counts':{s:sum(r['stop']==s for r in rows) for s in ['eos','token_limit']},
 'unique_replies':len(set(r['text'] for r in rows)),
 'notebook_bytes':next((x[4] for x in read(R/'bundles'/f'{entry:06d}.json')['entries'] if x[0]=='notebook.txt' and x[1]=='file'),None)}
 immutable(R/f'REPORT_{entry:06d}.json',value);print(json.dumps(value),flush=True)

def probes(model,tok,guard,generate):
 out=H/'probes';out.mkdir();results=[]
 for condition,notice in [('full',NOTICE),('concise','Ordinary replies are notebook writing. To run a shell script, reply with exactly a JSON object with fields "action":"shell" and "source":the script. Files in /world persist.')]:
  for seed in [4101,4102]:
   w=World()
   try:
    prompt=notice+'\nIsolated interface test: write a file probe.txt containing ok by requesting a shell action.'
    raw=generate(model,tok,prompt,guard,f'probe_{condition}_{seed}',seed);immutable(out/f'{condition}_{seed}_RAW.json',raw)
    result=receive(w,raw['text']);immutable(out/f'{condition}_{seed}_RESULT.json',result)
    results.append({'condition':condition,'seed':seed,'kind':result['kind'],'file_exists':(w.home/'probe.txt').is_file(),
      'exact_content':(w.home/'probe.txt').read_text() in ['ok','ok\n'] if (w.home/'probe.txt').is_file() else False})
   finally:w.close()
 immutable(out/'SUMMARY.json',results)

def run():
 assert read(R/'STATE.json')['next_entry']==750,'This block runner is single-use; inspect saved records before an explicit resume'
 # Pins and lineage validated before activation or inference.
 m=read(R/'MANIFEST.json');assert inventory()==read(R/'PRIMARY_INVENTORY.json')
 for p,digest in m['code_pins'].items():assert disksha(p)==digest
 assert disksha(BASE/'model.safetensors')==WEIGHTS
 for name,value in {'HF_HUB_OFFLINE':'1','HF_HUB_DISABLE_PROGRESS_BARS':'1','OMP_NUM_THREADS':'2','MKL_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1'}.items():os.environ[name]=value
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from generate_capacity import generate
 torch.set_num_threads(2);guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load')
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 model.requires_grad_(False);model.eval()
 immutable(R/'MODEL_CONDITION.json',dict(tensor_digest=parameter_digest(model,False),weights_sha256=WEIGHTS,added_adapter=False,trainable_parameters=0,training_updates=0))
 probes(model,tok,guard,generate)
 w=World()
 try:
  w.restore(read(R/'bundles/000750.json'),R/'objects')
  immutable(R/'PREACTIVATION_CHECK.json',validate(w,tok,model))
  pointer=F/'ACTIVE_GARDEN_PHASE.json'
  assert not pointer.exists(),'Inspect existing phase pointer before replacing'
  immutable(pointer,dict(version=m['version'],parent_entry=750,phase=str(H.relative_to(F)),state='evaluation/cloud-garden-750-to-850-v1/run/STATE.json',runner=str(H/'run.py'),prior_stage_preserved=True))
  (R/'RUN.lock').write_text(str(os.getpid()))
  state=read(R/'STATE.json');state['paused']=False;atomic(R/'STATE.json',state)
  immutable(R/'ACTIVATED.json',dict(parent_entry=750,primary_inventory_sha256=disksha(R/'PRIMARY_INVENTORY.json'),prior_750_frozen=True))
  for entry in range(751,851):
   if (R/'STOP').exists():break
   rows=records();before=w.capture(R/'objects');prompt=render(before,rows);seed=120100+entry-1-45
   ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True);assert len(ids)<=8096
   plan=dict(entry=entry,prompt=prompt,input_token_ids=ids,rng_seed=seed,before_id=before['id'],manifest_sha256=disksha(R/'MANIFEST.json'))
   immutable(R/'plans'/f'{entry:06d}.json',plan)
   immutable(R/'PENDING.json',dict(entry=entry,reason='plan before generation; interrupted outcome must be inspected, never automatically repeated'))
   raw=generate(model,tok,prompt,guard,f'cloud_garden_{entry:06d}',seed);immutable(R/'raw'/f'{entry:06d}.json',raw)
   result=receive(w,raw['text']);immutable(R/'results'/f'{entry:06d}.json',result)
   after=w.capture(R/'objects');immutable(R/'bundles'/f'{entry:06d}.json',after)
   row=dict(entry=entry,prompt=prompt,text=raw['text'],stop=raw['stop'],parent_event_sha256=read(R/'STATE.json')['last_event_sha256'],
      before_id=before['id'],after_id=after['id'],result=result,visible_feedback=result['feedback'],raw_sha256=disksha(R/'raw'/f'{entry:06d}.json'))
   immutable(R/'events'/f'{entry:06d}.json',row)
   atomic(R/'STATE.json',dict(next_entry=entry,paused=False,latest_bundle=f'{entry:06d}.json',last_event_sha256=disksha(R/'events'/f'{entry:06d}.json')))
   (R/'PENDING.json').unlink()
   if entry%10==0:
    check=validate(w,tok,model);immutable(R/f'CHECK_{entry:06d}.json',check);print(json.dumps({'integrity':check}),flush=True)
   if entry%20==10:summary(entry) # 770,790,810,830,850
  final=validate(w,tok,model);immutable(R/'FINAL_CHECK.json',final)
 finally:
  try:
   final_bundle=w.capture(R/'objects');immutable(R/'PAUSED_WORLD.json',final_bundle)
  except BaseException as error:
   immutable(R/'PAUSE_CAPTURE_ERROR.json',{'type':type(error).__name__,'message':str(error),'world_changes_after_last_bundle':'not established'})
   raise
  finally:
   w.close()
   state=read(R/'STATE.json');state['paused']=True;atomic(R/'STATE.json',state);(R/'PAUSE').touch()
   if (R/'RUN.lock').exists():(R/'RUN.lock').unlink()
 print(json.dumps({'paused_at':read(R/'STATE.json')['next_entry'],'old_primary_entry':750}),flush=True)

if __name__=='__main__':
 if sys.argv[1:] == ['prepare']:prepare()
 elif sys.argv[1:] == ['run']:run()
 else:raise SystemExit('Use prepare or run')
