"""Explicitly recover492from its preserved plan, then complete493–494; no policy change."""
from pathlib import Path
import os,sys,json,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parent.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment';sys.path.insert(0,str(G));sys.path.insert(0,str(ROOT/'evaluation/discovery-play-patch-v1'))
import world_routine as runner

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,x):
 with Path(p).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def main():
 proof=json.loads((R/'INTERRUPTION.json').read_text());assert sha(ENV/'plans/000492.json')==proof['original_plan_sha256'];assert sha(ENV/'sessions/0090_RESOURCE.jsonl')==proof['old_resource_sha256'];runner.freeze_check();j=runner.Journal(ENV);assert len(j.state()[1])==492 and not (ENV/'PAUSE').exists();v=json.loads((ENV.parent/'CURRENT_VERIFY.json').read_text());assert v['next_step']==492 and json.loads((ENV.parent/v['checks']).read_text())['status']=='pass'
 lock=ENV/'RUN.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  session=f"{len(list((ENV/'sessions').glob('*.json'))):04d}";resource=ENV/'sessions'/f'{session}_RESOURCE.jsonl';assert not resource.exists();put(R/'FREEZE_RECOVERY.json',dict(files={str(p):sha(p) for p in (R/'run_recovery.py',R/'INTERRUPTION.json',ENV/'plans/000492.json',G/'world_routine.py',G/'generate_capacity.py',ENV/'ENVIRONMENT_DISCOVERY_PATCH_V1.json')},scope='Recovery code/preserved plan/source pinned before replacement inference; original unknown attempt retained'))
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_capacity import generate
  torch.set_num_threads(2);m=json.loads((runner.parent.ACQ/'MANIFEST.json').read_text());assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];guard=Guard(5153960755,resource);guard.read('before_model_load');tok=AutoTokenizer.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False);model=AutoModelForCausalLM.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
  for step in range(492,495):
   assert not (ENV/'PAUSE').exists();_,events,_=j.state();assert len(events)==step;q=runner.world_view_render(events);ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert len(ids)<=8096;seed=1201*100+step-45;runid=f'continuous_{step:06d}';plan=dict(run_id=runid,step=step,prompt=q,input_token_ids=ids,rng_seed=seed,environment_sha256=sha(ENV/runner.NEW_MANIFEST),history_steps=runner.memory_view.view_steps(events),archive_available_range=[0,len(events)]);path=ENV/'plans'/f'{step:06d}.json'
   if step==492:
    assert path.exists() and sha(path)==proof['original_plan_sha256'];assert json.loads(path.read_text())==plan;put(R/'ATTEMPT_492.json',dict(step=492,kind='explicit_recovery_attempt_after_external_interruption',original_plan_sha256=sha(path),same_prompt_and_ids=True,same_seed=seed,prior_attempt_output='unobserved, not scored or discarded',new_resource_path=str(resource)))
   else:
    assert not path.exists();runner.immutable(path,plan)
   row=generate(model,tok,q,guard,runid,seed);row.update(step=step,environment_version=runner.NEW_VERSION,host_result=runner.world_dispatch(row['text'],events),feedback=runner.parent.FEEDBACK,task_score=None,history_steps=runner.memory_view.view_steps(events),archive_available_range=[0,len(events)],environment_sha256=sha(ENV/runner.NEW_MANIFEST),recovery_record='FRR/evaluation/discovery-450-to-500-v1/recovery/INTERRUPTION.json',attempt_kind='explicit_recovery_of_uncommitted_plan' if step==492 else 'continuation_after_runtime_recovery');j.commit(row);print(json.dumps(dict(step=step,next_step=step+1,host_kind=row['host_result']['kind'],recovery=True)),flush=True)
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];runner.freeze_check();assert sha(ENV/'plans/000492.json')==proof['original_plan_sha256'] and sha(ENV/'sessions/0090_RESOURCE.jsonl')==proof['old_resource_sha256']
  (ENV/'PAUSE').touch();j.project();runner.dump_new(ENV/'sessions'/f'{session}.json',dict(session=session,start_step=492,next_step=495,calls=3,requested_steps=3,input_limit=8096,environment_version=runner.NEW_VERSION,delay_seconds=0,stop_reason='recovery_window_complete',boundary=None,weights_unchanged=True,training_updates=0,recovery=True,recovery_attempt_at492=True));put(R/'RECOVERY_RESULT.json',dict(status='pass',completed_steps=[492,493,494],original_plan492_preserved=True,old_resource0090_preserved=True,unknown_prior_attempt_not_scored=True,weights_checked_before_after_reload=True,condition_changes=[],next_step=495,session=session))
 finally:(ENV/'PAUSE').touch();lock.unlink(missing_ok=True)
if __name__=='__main__':main()
