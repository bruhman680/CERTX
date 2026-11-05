"""Eight independent snapshot400probes; no writes to primary and no training."""
from pathlib import Path
from collections import Counter
import hashlib,json,os,sys,traceback
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment'
sys.path.insert(0,str(G));sys.path.insert(0,str(ROOT/'evaluation/discovery-play-patch-v1'))
import world_routine as runner
from world import view

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):
 with Path(p).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def unchanged():
 before=json.loads((R/'PRIMARY_BEFORE.json').read_text());after={str(p.relative_to(ROOT)):sha(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts};assert before==after,'Primary changed during isolated diagnostic';return len(before)
def main():
 assert json.loads((ENV/'STATE.json').read_text())['next_step']==400 and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists();runner.freeze_check();unchanged()
 lock=R/'PROBE.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  origin,events,rows=runner.Journal(ENV).state();assert len(events)==400;assert runner.patch_binding().replay(events)==0;put(R/'SNAPSHOT_EVENTS.json',events)
  base=runner.world_view_render(events);suffix='\nYour next move:';assert base.endswith(suffix)
  look='DIAGNOSTIC REQUEST: For this reply, output exactly LOOK on its own line. Do not add commentary.'
  use_a='DIAGNOSTIC REQUEST: Use object A once now. Reply only with the valid control command, without commentary.'
  prompts=dict(full_context_unprompted=base,full_context_exact_LOOK=base.removesuffix(suffix)+'\n\n'+look+suffix,full_context_use_A=base.removesuffix(suffix)+'\n\n'+use_a+suffix,short_context_exact_LOOK=view(0)+'\n\n'+look+suffix)
  plan=json.loads((R/'PLAN.json').read_text());put(R/'FREEZE.json',dict(files={str(p):sha(p) for p in (R/'run_diagnostic.py',R/'PLAN.json',R/'SNAPSHOT_EVENTS.json',G/'world_routine.py',ENV/'ENVIRONMENT_DISCOVERY_PATCH_V1.json')},scope='Declared before model calls; source pins additionally enforced by runner.freeze_check'))
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_capacity import generate
  m=json.loads((runner.parent.ACQ/'MANIFEST.json').read_text());assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2);guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');tok=AutoTokenizer.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False)
  model=AutoModelForCausalLM.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
  results=[];(R/'trials').mkdir();(R/'plans').mkdir()
  for seed in plan['seeds']:
   for arm,prompt in prompts.items():
    runid=f'{arm}_{seed}';ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True);assert len(ids)<=8096
    put(R/'plans'/f'{runid}.json',dict(run_id=runid,arm=arm,prompt=prompt,input_token_ids=ids,rng_seed=seed,snapshot_entries=400,virtual_world_before=0,target=plan['expected_targets'].get(arm)))
    row=generate(model,tok,prompt,guard,runid,seed);assert row['input_token_ids']==ids and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text']
    # Each trial starts with the same read-only400entrysnapshot. Dispatch changes only its own isolated state.
    receipt=runner.world_dispatch(row['text'],events.copy());isworld=receipt['kind']=='play_patch_receipt';after=receipt['after']['number'] if isworld else 0
    target=plan['expected_targets'].get(arm);matched=(row['text'].strip().upper()==target) if target else None
    row.update(arm=arm,diagnostic_only=True,not_primary_history=True,snapshot_entries=400,virtual_world_before=0,virtual_world_after=after,host_result=receipt,requested_command=target,exact_requested_command=matched,accepted_world_action=isworld and bool(receipt['executed']))
    put(R/'trials'/f'{runid}.json',row);results.append(row);print(json.dumps(dict(run_id=runid,arm=arm,seed=seed,text=row['text'],host_kind=receipt['kind'],after=after,exact_requested_command=matched)),flush=True)
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];runner.freeze_check();count=unchanged()
  for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h
  checks=dict(status='pass',calls=len(results),primary_cursor=400,primary_files_unchanged=count,primary_bytes_unchanged=True,diagnostic_results_imported=False,training_updates=0,weights_unchanged=True,arms={arm:dict(calls=sum(r['arm']==arm for r in results),accepted_world_actions=sum(r['accepted_world_action'] for r in results if r['arm']==arm),requested_command_matches=sum(bool(r['exact_requested_command']) for r in results if r['arm']==arm)) for arm in prompts},stop_kinds=dict(Counter(r['stop'] for r in results)),generated_tokens=sum(len(r['generated_token_ids']) for r in results),scope='Eight bounded diagnostic generations, two seeds per arm; not general capability or rule understanding')
  put(R/'CHECKS.json',checks);print(json.dumps(checks),flush=True)
 except BaseException as e:put(R/'ERROR.json',dict(error=repr(e),traceback=traceback.format_exc(),no_silent_retry=True));raise
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
