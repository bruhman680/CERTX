"""Versioned Scheme extension of the original garden, not a new model history.

Past runners remain frozen. Raw generations precede side effects. Request IDs
are stable across explicit recovery; source is never extracted or repaired.
"""
from pathlib import Path
import argparse, hashlib, json, os, sys, tempfile
H=Path(__file__).resolve().parent
D=H.parent/'scheme-primary-integration-v1'
G=D.parent/'source-access-three-cycle-v1'
P=D.parent/'computational-world-portability-v1'
sys.path[:0]=[str(G),str(P/'prototype'),'/workspace']
import world_routine as old
# Old renderer adds its own module search paths; select the Scheme CLI explicitly.
sys.path.insert(0,str(P/"prototype"))
from world_store import World
from world_cli import run_isolated, compact_observation
from world_bundle import export_world, import_world
E=G/'cycle3/environment'
VERSION='continuous-scheme-user-seed-v1'
MANIFEST='ENVIRONMENT_SCHEME_USER_SEED_V1.json'
OLD_VERSION='continuous-scheme-extension-v1'
OLD_MANIFEST='ENVIRONMENT_SCHEME_V2.json'
START=500
SEED_START=650
SEED_CARD='seed_cards/0001_USER_PLAY.json'
MAX_WINDOW=10
PROFILE=json.loads((P/'constants.json').read_text())
MUTABLE={'cycle3/environment/PAUSE','cycle3/environment/STATE.json','cycle3/environment/NOTEBOOK.jsonl','cycle3/CURRENT_VERIFY.json'}
def read(p):return json.loads(Path(p).read_text())
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def config():return read(E/MANIFEST)
def db():return E/'scheme_world/world.sqlite'
def manifest_at(step):return MANIFEST if step>=SEED_START else OLD_MANIFEST
def version_at(step):return VERSION if step>=SEED_START else OLD_VERSION
def checked():
 assert db().is_file(),'Persistent SQLite store missing: restore the last checked bundle, never create an empty replacement'
 old.freeze_check()
 for name,digest in read(H/'before/PRIMARY_INVENTORY.json').items():
  if name not in MUTABLE|{'cycle3/environment/ACTIVE_RUNNER.json'}:assert h(G/name)==digest,name
 assert read(E/SEED_CARD)==read(H/'USER_SEED.json')
 assert config()['seed_activation_step']==SEED_START and config()['max_checked_window']==MAX_WINDOW
 for name,digest in read(D/'before/PRIMARY_INVENTORY.json').items():
  if name not in MUTABLE:assert h(G/name)==digest,name
 for name,digest in config()['code_pins'].items():assert h(Path(name))==digest,name
 assert read(E/'ACTIVE_RUNNER.json')['version']==VERSION
 assert h(E/'scheme_world/bundles/genesis.json')==config()['genesis_sha256']
 assert h(D/'before/PRIMARY_INVENTORY.json')==config()['baseline_inventory_sha256']
def snapshot_bundle(path):
 with tempfile.TemporaryDirectory(prefix='garden-bundle-check-') as t:
  target=Path(t)/'world.sqlite';import_world(path,target,PROFILE)
  w=World(target,PROFILE)
  try:return w.snapshot()
  finally:w.close()
def export(path):
 w=World(db(),PROFILE)
 try:
  w.verify_integrity();export_world(w,path)
  return w.snapshot()
 finally:w.close()
def render(events,snapshot):
 base=old.world_view_render(events).removesuffix('\nYour next move:')
 # No target, worked answer, task score, forced command, or generated success.
 panel=('SCHEME WORKSPACE (new local extension; earlier notebook and number patch continue):\n'
 'You may explore, build, test, revisit a failure, or leave a note. Tools are optional. '
 'To act here, use one complete Scheme command as your whole reply, beginning with (. '
 'Available commands: (help), (list), (put name datum), (define (name arg) body), '
 '(run expression), (run-save name expression), (inspect name), (drop name). '
 'Expressions include integers, booleans #t/#f, strings, quoted lists, arithmetic, if, let and named recursion. '
 'Commands run locally with finite fuel, time, storage and output limits; errors are returned. '
 'Published data and functions persist across entries; ordinary text only joins the notebook. '
 'No network, imports or host files. Existing READ HISTORY, LOOK, TOUCH and TRY actions remain available.\n'
 'Current Scheme snapshot and aliases (host record): '+json.dumps(snapshot,sort_keys=True))
 q=base+'\n\n'+panel+'\n\nYour next move:'
 if len(events)>=SEED_START:
  q=q.removesuffix('\n\nYour next move:')+'\n\nUSER TEXT SEED (invitation within this environment):\n'+read(E/SEED_CARD)['text']+'\n\nYour next move:'
 return q
def is_scheme(text):return text.lstrip().startswith('(')
def dispatch(text,events,snapshot,request_id,target=None,receipt_path=None):
 if not is_scheme(text):return old.world_dispatch(text,events)
 receipt=run_isolated(target or db(),PROFILE,request_id,snapshot['id'],text)
 assert receipt.get('status') not in ('HOST_STORAGE_UNKNOWN','UNKNOWN_COMMIT','PENDING'), 'Uncertain commit: pause and inspect; never retry generation'
 if receipt_path is not None:
  if Path(receipt_path).exists():assert read(receipt_path)==receipt
  else:old.immutable(receipt_path,receipt)
 return dict(kind='scheme_receipt',executed=bool(receipt.get('event')),request_id=request_id,
             status=receipt.get('status'),result=compact_observation(receipt,PROFILE),
             receipt_sha256=hashlib.sha256(json.dumps(receipt,sort_keys=True).encode()).hexdigest())
class Journal(old.Journal):
 def project(self):
  super().project()
  state=read(self.path/'STATE.json');state.update(manifest_sha256=h(self.path/MANIFEST),
   environment_version=VERSION,activation_step=START,seed_activation_step=SEED_START,active_runner=str(Path(__file__)),
   previous_manifest_sha256=h(self.path/old.NEW_MANIFEST))
  # A projection only; receipts and portable bundles retain authoritative state.
  with WorldContext() as w:state['scheme_snapshot']=w.snapshot()
  old.atomic(self.path/'STATE.json',state)
class WorldContext:
 def __enter__(self):self.w=World(db(),PROFILE);return self.w
 def __exit__(self,*args):self.w.close()
def activate():
 assert (E/'PAUSE').exists() and not (E/'RUN.lock').exists()
 assert db().is_file() and len(old.Journal(E).state()[1])==SEED_START
 latest=read(E.parent/'CURRENT_VERIFY.json')
 assert latest['next_step']==SEED_START and read(E.parent/latest['checks'])['status']=='pass'
 assert not (E/MANIFEST).exists() and not (E/SEED_CARD).exists()
 old.freeze_check()
 prior=read(E/OLD_MANIFEST)
 for name,digest in prior['code_pins'].items():assert h(Path(name))==digest,name
 for name,digest in read(H/'before/PRIMARY_INVENTORY.json').items():assert h(G/name)==digest,name
 (E/SEED_CARD).parent.mkdir(exist_ok=True)
 old.immutable(E/SEED_CARD,read(H/'USER_SEED.json'))
 manifest=dict(prior)
 manifest.update(version=VERSION,revision=3,seed_activation_step=SEED_START,
  original_scheme_activation_step=START,max_checked_window=MAX_WINDOW,
  previous_extension_manifest_sha256=h(E/OLD_MANIFEST),
  seed_card=SEED_CARD,seed_sha256=h(E/SEED_CARD),user_seed_text=read(E/SEED_CARD)['text'],
  condition_changes=['Exact user text seed including emoji from entry 651','User-authorized checked window maximum increased from 5 to 10'],
  unchanged='Same history, world, runtime profile, model, canonical adapter, sampling and output/input caps. No display-framing repair, training, test import or output normalization.',
  curious_event_rule='Pause after any non-note host result for observer review; ordinary wording/repetition does not require a stop.')
 manifest['code_pins']=dict(prior['code_pins'])
 for p in [Path(__file__),H/'USER_SEED.json',E/SEED_CARD]:manifest['code_pins'][str(p)]=h(p)
 old.immutable(E/MANIFEST,manifest)
 old.atomic(E/'ACTIVE_RUNNER.json',dict(version=VERSION,runner=str(Path(__file__)),manifest=MANIFEST,
  activation_step=START,seed_activation_step=SEED_START,revision=3,max_checked_window=MAX_WINDOW,
  previous_pointer_sha256=h(H/'before/ACTIVE_RUNNER.json')))
 Journal(E).project();checked();print('Activated exact user seed at original cursor 650; paused; world and history preserved.')
def complete(step):
 plan=read(E/'plans'/f'{step:06d}.json');rawpath=E/'scheme_world/raw'/f'{step:06d}.json';row=read(rawpath)
 assert row['run_id']==plan['run_id'] and row['prompt']==plan['prompt'] and row['rng_seed']==plan['rng_seed']
 events=Journal(E).state()[1];assert len(events)==step
 snap=snapshot_bundle(E/plan['scheme_before_bundle']);assert snap==plan['scheme_before_snapshot']
 obs=E/'scheme_world/observations'/f'{step:06d}.json'
 if obs.exists():host=read(obs)['host_result']
 else:
  host=dispatch(row['text'],events,snap,f'primary-{step:06d}',receipt_path=E/'scheme_world/observations'/f'{step:06d}_FULL.json')
  old.immutable(obs,dict(step=step,host_result=host))
 after=E/'scheme_world/bundles'/f'{step:06d}_after.json'
 if not after.exists():export(after)
 row.update(step=step,environment_version=VERSION,host_result=host,feedback=old.parent.FEEDBACK,task_score=None,
  history_steps=old.memory_view.view_steps(events),archive_available_range=[0,len(events)],environment_sha256=h(E/MANIFEST),
  scheme_before_bundle=plan['scheme_before_bundle'],scheme_after_bundle=str(after.relative_to(E)),
  scheme_before_sha256=plan['scheme_before_sha256'],scheme_after_sha256=h(after))
 Journal(E).commit(row);return row

def should_zoom(row):return row["host_result"]["kind"]!="record_receipt"
def run(steps):
 assert 0<steps<=MAX_WINDOW;checked();j=Journal(E)
 latest=read(E.parent/'CURRENT_VERIFY.json');assert latest['next_step']==len(j.state()[1]) and read(E.parent/latest['checks'])['status']=='pass','Verify the saved cursor before another window'
 assert not (E/'PAUSE').exists(),'Resume explicitly before run'
 fd=os.open(E/'RUN.lock',os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 session=f"{len(list((E/'sessions').glob('*.json'))):04d}";start=len(j.state()[1]);calls=0;reason='budget_pause'
 try:
  assert not (E/'plans'/f'{start:06d}.json').exists(),'Outstanding plan; inspect and explicitly recover, never regenerate silently'
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_capacity import generate
  m=read(old.parent.ACQ/'MANIFEST.json');assert h(old.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256']
  torch.set_num_threads(2);guard=Guard(5153960755,E/'sessions'/f'{session}_RESOURCE.jsonl');guard.read('before_model_load')
  tok=AutoTokenizer.from_pretrained(old.parent.BASE,local_files_only=True,trust_remote_code=False)
  model=AutoModelForCausalLM.from_pretrained(old.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
  inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,old.parent.ACQ/'final',base_pin=m['base_pin']);model.eval()
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
  for _ in range(steps):
   if (E/'PAUSE').exists():reason='pause_requested';break
   events=j.state()[1];step=len(events);before=E/'scheme_world/bundles'/f'{step:06d}_before.json';snap=export(before)
   q=render(events,snap);ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True)
   assert len(ids)<=old.LIMIT,'Input boundary: pause; no truncation'
   runid=f'continuous_{step:06d}';seed=1201*100+step-45
   old.immutable(E/'plans'/f'{step:06d}.json',dict(run_id=runid,step=step,prompt=q,input_token_ids=ids,rng_seed=seed,
    environment_sha256=h(E/MANIFEST),history_steps=old.memory_view.view_steps(events),archive_available_range=[0,step],
    scheme_before_bundle=str(before.relative_to(E)),scheme_before_sha256=h(before),scheme_before_snapshot=snap,user_seed_sha256=h(E/SEED_CARD)))
   row=generate(model,tok,q,guard,runid,seed);calls+=1
   old.immutable(E/'scheme_world/raw'/f'{step:06d}.json',row)
   row=complete(step);print(json.dumps(dict(next_step=step+1,kind=row['host_result']['kind'],stop=row['stop'])),flush=True)
   if should_zoom(row):reason='curious_event_pause';break
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
  assert h(old.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];checked()
 except BaseException:
  reason='interrupted_or_failed';raise
 finally:
  (E/'PAUSE').touch();j.project()
  old.immutable(E/'sessions'/f'{session}.json',dict(session=session,start_step=start,next_step=len(j.state()[1]),calls=calls,
   requested_steps=steps,input_limit=old.LIMIT,environment_version=VERSION,delay_seconds=0,stop_reason=reason,
   boundary=None,weights_unchanged=reason!='interrupted_or_failed',training_updates=0))
  (E/'RUN.lock').unlink()
def verify():
 checked();os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(old.parent.BASE,local_files_only=True,trust_remote_code=False)
 j=Journal(E);origin,events,rows=j.state();new=[r for r in rows if r['step']>=START]
 prior=E/'scheme_world/bundles/genesis.json'
 for r in new:
  step=r['step'];p=read(E/'plans'/f'{step:06d}.json');before=E/r['scheme_before_bundle'];after=E/r['scheme_after_bundle']
  assert prior.read_bytes()==before.read_bytes(),'World continuity broken'
  assert h(before)==r['scheme_before_sha256']==p['scheme_before_sha256'] and h(after)==r['scheme_after_sha256']
  snap=snapshot_bundle(before);assert snap==p['scheme_before_snapshot']
  assert r['prompt']==p['prompt']==render(events[:step],snap)
  assert r['input_token_ids']==p['input_token_ids']==tok.apply_chat_template([{'role':'user','content':r['prompt']}],tokenize=True,add_generation_prompt=True)
  assert r['rng_seed']==p['rng_seed']==1201*100+step-45
  assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text']
  assert r['environment_version']==version_at(step) and r['environment_sha256']==p['environment_sha256']==h(E/manifest_at(step))
  if step>=SEED_START:assert p['user_seed_sha256']==h(E/SEED_CARD)
  assert r['task_score'] is None and r['feedback']==old.parent.FEEDBACK
  assert r['history_steps']==p['history_steps']==old.memory_view.view_steps(events[:step])
  assert r['archive_available_range']==p['archive_available_range']==[0,step]
  assert len(r['input_token_ids'])<=old.LIMIT and 0<len(r['generated_token_ids'])<=96
  assert (r['stop']=='eos' and r['generated_token_ids'][-1]==tok.eos_token_id) or (r['stop']=='token_limit' and len(r['generated_token_ids'])==96)
  raw=read(E/'scheme_world/raw'/f'{step:06d}.json');assert all(r[k]==v for k,v in raw.items())
  with tempfile.TemporaryDirectory(prefix='garden-replay-') as t:
   target=Path(t)/'world.sqlite';import_world(before,target,PROFILE)
   expected=dispatch(r['text'],events[:step],snap,f'primary-{step:06d}',target,Path(t)/'receipt.json')
   if is_scheme(r['text']):assert read(Path(t)/'receipt.json')==read(E/'scheme_world/observations'/f'{step:06d}_FULL.json')
   assert expected==r['host_result']==read(E/'scheme_world/observations'/f'{step:06d}.json')['host_result']
   w=World(target,PROFILE)
   try:export_world(w,Path(t)/'after.json')
   finally:w.close()
   assert (Path(t)/'after.json').read_bytes()==after.read_bytes(),'Independent world replay differs'
  prior=after
 with tempfile.TemporaryDirectory(prefix='garden-live-export-') as t:
  export(Path(t)/'live.json');assert (Path(t)/'live.json').read_bytes()==prior.read_bytes()
 assert [json.loads(l) for l in (E/'NOTEBOOK.jsonl').read_text().splitlines()]==events
 assert (E/'NOTEBOOK.jsonl').read_bytes().startswith((D/'before/NOTEBOOK.jsonl').read_bytes())
 state=read(E/'STATE.json');assert state['next_step']==len(events) and state['manifest_sha256']==h(E/MANIFEST)
 assert state['event_sha256']=={p.name:h(p) for p in sorted((E/'events').glob('*.json'))}
 assert state['scheme_snapshot']==snapshot_bundle(prior) and state['pause_requested']==(E/'PAUSE').exists()
 sessions=[read(p) for p in (E/'sessions').glob('*.json')];assert sum(s['calls'] for s in sessions)==len(rows)
 resources=[json.loads(l) for p in (E/'sessions').glob('*_RESOURCE.jsonl') for l in p.read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
 checks=dict(status='pass',next_step=len(events),baseline_copy_reconstruction_500=True,
  immutable_old_prefix_checked=True,new_generations_reconstructed=len(new),independent_world_replays=len(new),
  notebook_prefix_preserved=True,live_world_matches_last_bundle=True,model_training_updates=0,
  pause_marker_present=(E/'PAUSE').exists(),legacy_interrupted_unknown='unchanged; not retroactively resolved')
 vid=f"{len(list((E.parent/'verification').glob('*_CHECKS.json'))):04d}"
 summary=dict(next_step=len(events),new_calls=len(new),scheme_replies=sum(is_scheme(r['text']) for r in new),
  host_kinds=[r['host_result']['kind'] for r in new],stops=[r['stop'] for r in new],
  max_input_tokens=max((len(r['input_token_ids']) for r in new),default=0),scheme_snapshot=state['scheme_snapshot'])
 for name,value in [('CHECKS',checks),('SUMMARY',summary),('EVENT_INDEX',dict(rows=[dict(step=r['step'],host_kind=r['host_result']['kind']) for r in new]))]:old.immutable(E.parent/'verification'/f'{vid}_{name}.json',value)
 old.atomic(E.parent/'CURRENT_VERIFY.json',dict(verification=vid,next_step=len(events),checks=f'verification/{vid}_CHECKS.json',summary=f'verification/{vid}_SUMMARY.json',index=f'verification/{vid}_EVENT_INDEX.json',active_runner=str(Path(__file__))))
 print(json.dumps(dict(verification=vid,**summary)),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['activate','run','verify','resume','pause','recover']);p.add_argument('--steps',type=int,default=10);a=p.parse_args()
 if a.action=='activate':activate()
 elif a.action=='run':run(a.steps)
 elif a.action=='verify':verify()
 elif a.action=='resume':checked();(E/'PAUSE').unlink(missing_ok=True);Journal(E).project();print('Armed; run required for model calls.')
 elif a.action=='pause':(E/'PAUSE').touch();Journal(E).project()
 elif a.action=='recover':
  checked();assert (E/'PAUSE').exists() and not (E/'RUN.lock').exists();complete(len(Journal(E).state()[1]));print('Recovered saved raw generation; no new inference. Reconcile session counts before verify.')
