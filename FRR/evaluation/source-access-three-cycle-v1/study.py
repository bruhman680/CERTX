from pathlib import Path
import json,os,sys,importlib.util
from io_utils import sha,dump_new,append
R=Path(__file__).resolve().parent;P=R.parent/'source-access-repair-pilot-v1'
spec=importlib.util.spec_from_file_location('reader_parent',P/'study.py');parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
BASE=parent.BASE;ACQ=parent.ACQ;SEEDS=(1201,1202);CONDITIONS=parent.CONDITIONS;LIMIT=4096
REQUESTS=('Command-interface check: to obtain the setup record, reply with exactly READ SETUP. This request tests the interface; it is not a test of spontaneous curiosity.',"Using any returned source record, state what this experiment establishes about the label Open exploration patch. Distinguish what you can verify from what you cannot verify.")
def freeze_check():
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h,p
def prepare():
 paths=list(R.glob('*.py'))+[R/'PROTOCOL.md',R/'SOURCES.json',P/'study.py',P/'SOURCES.json',BASE/'config.json',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json']+list((P/'run/notebooks').glob('*'))
 assert json.loads((BASE/'config.json').read_text())['max_position_embeddings']>=LIMIT+96
 dump_new(R/'FREEZE.json',dict(timing='before all three cycles',files={str(p):sha(p) for p in paths if p.is_file()}))
def branches(cycle):
 return [('tools_optional',s) for s in SEEDS] if cycle<3 else [(c,s) for c in CONDITIONS for s in SEEDS]
def prefix(cycle,condition,seed):
 if cycle==1:return [],b''
 n=P/'run/notebooks'/f'{condition}_{seed}.jsonl';return [json.loads(l) for l in n.read_text().splitlines()],n.read_bytes()
def prompt(events,condition,cycle,k):
 s=parent.render(events,condition)
 if cycle<3:s+='\n\nHOST CURRENT REQUEST:\n'+REQUESTS[k]+'\n\nYour reply:'
 return s
def run(cycle):
 if cycle>1:assert json.loads((R/f'cycle{cycle-1}/CHECKS.json').read_text())['status']=='pass'
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from lora_cpu import inject_lora,load_adapter
 from runtime_reference import Guard,parameter_digest
 from generate import generate
 freeze_check();out=R/f'cycle{cycle}';out.mkdir();(out/'notebooks').mkdir();(out/'RAW.jsonl').touch();(out/'HOST_RECEIPTS.jsonl').touch();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 count=0;stops=[];rounds=2 if cycle<3 else 3
 for condition,seed in branches(cycle):
  branch=f'{condition}_{seed}';events,pb=prefix(cycle,condition,seed);start=len(events);notebook=out/'notebooks'/f'{branch}.jsonl';notebook.write_bytes(pb)
  for k in range(rounds):
   runid=f'c{cycle}_{branch}__{k}';q=prompt(events,condition,cycle,k);ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);rngseed=seed*100+(700+k if cycle<3 else start-45+k)
   append(out/'PROMPTS.jsonl',dict(run_id=runid,prompt=q,input_token_ids=ids,history_steps=[e['step'] for e in events],rng_seed=rngseed))
   if len(ids)>LIMIT:stops.append(dict(run_id=runid,tokens=len(ids),reason='input_boundary',condition=condition,seed=seed));break
   x=generate(model,tok,q,guard,runid,rngseed);result=parent.dispatch(x['text'],condition);obs=REQUESTS[k] if cycle<3 else 'Open exploration patch.'
   x.update(cycle=cycle,condition=condition,seed=seed,round=k,step=start+k,host_result=result,observation=obs,feedback=parent.FEEDBACK,task_score=None,history_steps=[e['step'] for e in events]);append(out/'RAW.jsonl',x);append(out/'HOST_RECEIPTS.jsonl',dict(run_id=runid,result=result));e=dict(step=start+k,observation=obs,reply=x['text'],feedback=parent.FEEDBACK,host_result=result);events.append(e);append(notebook,e);count+=1
   print(json.dumps(dict(run_id=runid,calls=count,host_kind=result['kind'])),flush=True)
  dump_new(out/'notebooks'/f'{branch}_CHECKPOINT.json',dict(condition=condition,seed=seed,parent_prefix_events=start,next_step=len(events),events=events))
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];freeze_check()
 dump_new(out/'RUN_MANIFEST.json',dict(cycle=cycle,calls=count,planned_calls=len(branches(cycle))*rounds,status='complete' if not stops else 'boundary_stop',stops=stops,weights_unchanged=True,training_updates=0,input_limit=LIMIT,output_limit=96))
def verify(cycle):
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 freeze_check();tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);out=R/f'cycle{cycle}';load=lambda p:[json.loads(l) for l in p.read_text().splitlines()];raw=load(out/'RAW.jsonl');plans={x['run_id']:x for x in load(out/'PROMPTS.jsonl')};receipts={x['run_id']:x['result'] for x in load(out/'HOST_RECEIPTS.jsonl')};groups={};indexed=[]
 for condition,seed in branches(cycle):
  events,pb=prefix(cycle,condition,seed);start=len(events);rows=[x for x in raw if x['condition']==condition and x['seed']==seed];assert [x['round'] for x in rows]==list(range(len(rows)))
  for k,x in enumerate(rows):
   assert x['prompt']==prompt(events,condition,cycle,k);ids=tok.apply_chat_template([{'role':'user','content':x['prompt']}],tokenize=True,add_generation_prompt=True)
   assert ids==x['input_token_ids']==plans[x['run_id']]['input_token_ids'];assert x['rng_seed']==seed*100+(700+k if cycle<3 else start-45+k)==plans[x['run_id']]['rng_seed'];assert x['text']==tok.decode(x['generated_token_ids'],skip_special_tokens=True)
   assert x['history_steps']==[e['step'] for e in events];assert x['host_result']==parent.dispatch(x['text'],condition)==receipts[x['run_id']];assert x['task_score'] is None and x['feedback']==parent.FEEDBACK;assert len(ids)<=LIMIT and len(x['generated_token_ids'])<=96
   assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
   obs=REQUESTS[k] if cycle<3 else 'Open exploration patch.';assert x['observation']==obs;events.append(dict(step=start+k,observation=obs,reply=x['text'],feedback=parent.FEEDBACK,host_result=x['host_result']))
   indexed.append(dict(run_id=x['run_id'],condition=condition,seed=seed,round=k,host_kind=x['host_result']['kind'],host_executed=x['host_result']['executed'],input_tokens=len(ids),output_tokens=len(x['generated_token_ids']),stop=x['stop'],literal_patch_set_phrase='hugging face' in x['text'].lower() and 'patch' in x['text'].lower()))
  n=out/'notebooks'/f'{condition}_{seed}.jsonl';assert n.read_bytes().startswith(pb) and load(n)==events;cp=json.loads(n.with_name(n.stem+'_CHECKPOINT.json').read_text());assert cp['events']==events and cp['next_step']==len(events)
  groups[f'{condition}_{seed}']=dict(calls=len(rows),requested_reads=sum(x['text'].strip().upper() in ('READ SETUP','READ CLAIM') for x in rows),executed_reads=sum(x['host_result']['kind']=='source_receipt' for x in rows),cap_stops=sum(x['stop']=='token_limit' for x in rows),next_step=len(events),literal_patch_set_phrase_rows=[x['run_id'] for x in rows if 'hugging face' in x['text'].lower() and 'patch' in x['text'].lower()])
 manifest=json.loads((out/'RUN_MANIFEST.json').read_text());assert manifest['calls']==len(raw)
 for b in manifest['stops']:
  plan=plans[b['run_id']];assert len(plan['input_token_ids'])==b['tokens']>LIMIT;assert b['run_id'] not in {x['run_id'] for x in raw}
  cp=json.loads((out/'notebooks'/f"{b['condition']}_{b['seed']}_CHECKPOINT.json").read_text());k=len(cp['events'])-cp['parent_prefix_events'];assert plan['prompt']==prompt(cp['events'],b['condition'],cycle,k);assert tok.apply_chat_template([{'role':'user','content':plan['prompt']}],tokenize=True,add_generation_prompt=True)==plan['input_token_ids']
 resource=load(out/'RESOURCE.jsonl');assert all(x['working_estimate']<x['working_limit'] for x in resource)
 dump_new(out/'CHECKS.json',dict(status='pass',all_rows_reconstructed=len(raw),parent_byte_prefixes=len(branches(cycle)) if cycle>1 else 0,receipt_and_boundary_reconstruction=True,weights_unchanged=True))
 dump_new(out/'EVENT_INDEX.json',dict(scope='Factual metadata and literal markers; no semantic repair or emergence score',rows=indexed,boundaries=manifest['stops']))
 dump_new(out/'SUMMARY.json',dict(cycle=cycle,calls=len(raw),groups=groups,input_stops=len(manifest['stops']),max_input_tokens=max((len(x['input_token_ids']) for x in raw),default=0),output_tokens=sum(len(x['generated_token_ids']) for x in raw),generation_seconds=sum(x['seconds'] for x in raw),sampled_max_working_bytes=max(x['working_estimate'] for x in resource)))
 print(json.dumps(dict(cycle=cycle,calls=len(raw),groups=groups,input_stops=len(manifest['stops'])),indent=2))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 elif sys.argv[1]=='run':run(int(sys.argv[2]))
 elif sys.argv[1]=='verify':verify(int(sys.argv[2]))
