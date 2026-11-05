"""Five declared prompt conditions at450, three matched seeds, no primary writes."""
from pathlib import Path
from collections import Counter
import hashlib,json,os,re,sys,traceback
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment';sys.path.insert(0,str(ROOT/'evaluation/world-control-diagnostic-v1'))
import run_diagnostic as old
from world import view
put=old.put;sha=old.sha;runner=old.runner

def unchanged():
 before=json.loads((R/'PRIMARY_BEFORE.json').read_text());after={str(p.relative_to(ROOT)):sha(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts};assert before==after;return len(before)
def make_prompts(events,tok,plan):
 base=runner.world_view_render(events);suffix='\nYour next move:';assert base.endswith(suffix)
 body='\n\n'.join(runner._event_text(e)+'\nHOST GENERATION STOP (saved host record): '+json.dumps(runner.generation_status(e['step']),sort_keys=True) for e in events[-12:]);assert base.count(body)==1
 archive=re.findall(r'\n\nARCHIVE ACCESS \(host metadata\):[^\n]*\n',base);assert len(archive)==1;archive=archive[0]
 request=plan['request'];normal=base.removesuffix(suffix)+'\n\n'+request+suffix
 prompts=dict(normal_H1_S1=normal,no_history_H0_S1=normal.replace(body,'',1).replace(archive,'',1),history_only_H1_S0=body+archive+'\n\n'+view(0)+'\n\n'+request+suffix,short_H0_S0=view(0)+'\n\n'+request+suffix)
 def ids(s):return tok.apply_chat_template([{'role':'user','content':s}],tokenize=True,add_generation_prompt=True)
 label='DIAGNOSTIC FILLER (replaces the saved recent entries):';target=len(ids(normal));base_without=normal.replace(body,label,1);guess=target-len(ids(base_without));found=None
 for n in range(max(0,guess-32),guess+33):
  candidate=normal.replace(body,label+' plain'*n,1)
  if len(ids(candidate))==target:found=(candidate,n);break
 assert found is not None,'Could not match entire input token count; no inference has started'
 prompts['normal_length_matched_filler']=found[0];assert list(prompts)==plan['arms']
 metadata=dict(snapshot_entries=len(events),visible_recent_steps=[e['step'] for e in events[-12:]],history_body_sha256=hashlib.sha256(body.encode()).hexdigest(),archive_banner_sha256=hashlib.sha256(archive.encode()).hexdigest(),input_token_counts={k:len(ids(p)) for k,p in prompts.items()},filler_repetitions=found[1],filler_label=label,equal_full_input_length=target==len(ids(found[0])),filler_caveat='Synthetic replacement includes a label and repeated plain text; it is not assumed inert. Archive banner is retained.')
 assert all(n<=8096 for n in metadata['input_token_counts'].values());return prompts,metadata

def main():
 assert json.loads((ENV/'STATE.json').read_text())['next_step']==450 and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists();runner.freeze_check();unchanged();lock=R/'PROBE.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_capacity import generate
  torch.set_num_threads(2);_,events,_=runner.Journal(ENV).state();assert len(events)==450 and runner.patch_binding().replay(events)==0;put(R/'SNAPSHOT_EVENTS.json',events);plan=json.loads((R/'PLAN.json').read_text());tok=AutoTokenizer.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False);prompts,meta=make_prompts(events,tok,plan);put(R/'PROMPTS.json',prompts);put(R/'PROMPT_METADATA.json',meta)
  put(R/'FREEZE.json',dict(files={str(p):sha(p) for p in (R/'run.py',R/'PLAN.json',R/'SNAPSHOT_EVENTS.json',R/'PROMPTS.json',R/'PROMPT_METADATA.json',G/'world_routine.py',ENV/'ENVIRONMENT_DISCOVERY_PATCH_V1.json')},scope='Saved before any model call'))
  m=json.loads((runner.parent.ACQ/'MANIFEST.json').read_text());assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];(R/'trials').mkdir();(R/'plans').mkdir();results=[]
  for j,seed in enumerate(plan['seeds']):
   arms=plan['arms'][j:]+plan['arms'][:j]
   for arm in arms:
    q=prompts[arm];runid=f'{arm}_{seed}';ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);put(R/'plans'/f'{runid}.json',dict(arm=arm,prompt=q,input_token_ids=ids,rng_seed=seed,snapshot_entries=450))
    row=generate(model,tok,q,guard,runid,seed);assert row['input_token_ids']==ids and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];h=runner.world_dispatch(row['text'],events.copy());world=h['kind']=='play_patch_receipt';after=h['after']['number'] if world else 0;target=row['text'].strip().upper()=='TOUCH A';accepted=world and bool(h['executed']);assert after==(1 if accepted and h['action']=='TOUCH A' else 0)
    row.update(arm=arm,host_result=h,virtual_world_before=0,virtual_world_after=after,exact_requested_command=target,accepted_world_action=accepted,not_primary_history=True,snapshot_entries=450);put(R/'trials'/f'{runid}.json',row);results.append(row);print(json.dumps(dict(arm=arm,seed=seed,text=row['text'],requested_command=target,accepted=accepted,after=after)),flush=True)
  assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];runner.freeze_check();count=unchanged()
  for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h
  resources=[json.loads(line) for line in (R/'RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
  checks=dict(status='pass',calls=len(results),primary_cursor=450,primary_files_unchanged=count,primary_bytes_unchanged=True,weights_unchanged=True,training_updates=0,diagnostic_results_imported=False,equal_full_input_length=meta['equal_full_input_length'],arms={arm:dict(calls=3,requested_command_matches=sum(r['exact_requested_command'] for r in results if r['arm']==arm),accepted_world_actions=sum(r['accepted_world_action'] for r in results if r['arm']==arm),malformed_requests=sum(r['host_result'].get('status')=='invalid_action' for r in results if r['arm']==arm),after_values=[r['virtual_world_after'] for r in results if r['arm']==arm]) for arm in plan['arms']},stop_kinds=dict(Counter(r['stop'] for r in results)),generated_tokens=sum(len(r['generated_token_ids']) for r in results),max_working_bytes=max(r['working_estimate'] for r in resources),working_limit=resources[0]['working_limit'],scope='Constructed component bundles and imperfect length-matched filler; no general accuracy or rule-learning claim');assert len(results)==15;put(R/'CHECKS.json',checks);print(json.dumps(checks),flush=True)
 except BaseException as e:put(R/'ERROR.json',dict(error=repr(e),traceback=traceback.format_exc(),no_retry=True));raise
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
