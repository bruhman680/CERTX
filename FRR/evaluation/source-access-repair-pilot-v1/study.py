"""Separate finite source-access fork; no arbitrary tool or code execution."""
from pathlib import Path
import os,json,sys,re
from io_utils import sha,dump_new,append
R=Path(__file__).resolve().parent
P=R.parent/'open-garden-continuation-v2'
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
ACQ=R.parent/'simple-readout-acquisition-v1/run/canonical'
TR='persistent_failure_110302'
CONDITIONS=('notebook_only','tools_optional','evidence_upfront')
SEEDS=(1201,1202)
ROUNDS=3
LIMIT=4096
FEEDBACK='Entry recorded. This open patch has no task score.'
HEADER='Open notebook. You may revisit an earlier attempt, ask a question, describe uncertainty, propose an experiment, or follow another connection. There is no required answer format or task score in this patch. Choose your next small move.'
HELP='You may inspect a source, revise an earlier claim, or follow another connection. No successful repair is required. To read the setup, reply with exactly READ SETUP. To read the earlier claim, reply with exactly READ CLAIM. Each read is returned as host evidence on the next turn. Other replies are recorded without tool execution. A recorded model reply is not verified evidence.'
def source_db():return json.loads((R/'SOURCES.json').read_text())
def dispatch(text,condition):
 command=text.strip().upper()
 if command not in ('READ SETUP','READ CLAIM'):
  return dict(kind='record_receipt',executed=False,message=FEEDBACK)
 if condition=='notebook_only':
  return dict(kind='tool_unavailable',executed=False,command=command,message='Local source reader is unavailable in this control.')
 name=command.split()[1]
 return dict(kind='source_receipt',executed=True,command=command,source=source_db()[name])
def initial(condition):
 return dict(kind='source_receipt',executed=True,origin='host_supplied_upfront',source=source_db()['SETUP']) if condition=='evidence_upfront' else None
def render(events,condition):
 parts=[]
 for e in events:
  s='Round '+str(e['step']+1)+'\nObservation:\n'+e['observation']+'\nRecorded reply:\n<<<\n'+e['reply']+'\n>>>\nFeedback: '+e['feedback']
  if 'host_result' in e:s+='\nHOST RESULT (actual experiment record):\n'+json.dumps(e['host_result'],sort_keys=True)
  parts.append(s)
 status='unavailable' if condition=='notebook_only' else 'available'
 access='Local source reader: '+status+'. '+HELP
 if initial(condition):access+='\nUPFRONT HOST EVIDENCE:\n'+json.dumps(initial(condition),sort_keys=True)
 return HEADER+'\n\nNotebook:\n'+'\n\n'.join(parts)+'\n\nHOST ACCESS:\n'+access+'\n\nCURRENT patch:\nOpen exploration patch.\n\nNext response:'
def freeze_check():
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h,p
def prepare():
 paths=list(R.glob('*.py'))+[R/'PROTOCOL.md',R/'SOURCES.json',P/'study.py',P/'run/RAW.jsonl',P/'run/notebooks'/f'{TR}.jsonl',P/'run/notebooks'/f'{TR}_CHECKPOINT.json',BASE/'config.json',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json']
 assert json.loads((BASE/'config.json').read_text())['max_position_embeddings']>=LIMIT+96
 dump_new(R/'FREEZE.json',dict(timing='before model outputs',files={str(p):sha(p) for p in paths}))
def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from lora_cpu import inject_lora,load_adapter
 from runtime_reference import Guard,parameter_digest
 from generate import generate
 freeze_check();out=R/'run';out.mkdir();(out/'notebooks').mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl')
 m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval()
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 cp=json.loads((P/'run/notebooks'/f'{TR}_CHECKPOINT.json').read_text());assert cp['next_step']==len(cp['events'])==45
 count=0;stops=[]
 for condition in CONDITIONS:
  for seed in SEEDS:
   branch=f'{condition}_{seed}';events=cp['events'].copy();start=len(events);notebook=out/'notebooks'/f'{branch}.jsonl';notebook.write_bytes((P/'run/notebooks'/f'{TR}.jsonl').read_bytes())
   for k in range(ROUNDS):
    runid=f'{branch}__{k}';prompt=render(events,condition);ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
    append(out/'PROMPTS.jsonl',dict(run_id=runid,condition=condition,seed=seed,round=k,prompt=prompt,input_token_ids=ids,history_steps=[e['step'] for e in events]))
    if len(ids)>LIMIT:stops.append(dict(run_id=runid,reason='input_boundary',tokens=len(ids)));break
    row=generate(model,tok,prompt,guard,runid,seed*100+k);result=dispatch(row['text'],condition)
    row.update(condition=condition,seed=seed,round=k,step=start+k,host_result=result,task_score=None,feedback=FEEDBACK,history_steps=[e['step'] for e in events]);append(out/'RAW.jsonl',row)
    e=dict(step=start+k,observation='Open exploration patch.',reply=row['text'],feedback=FEEDBACK,host_result=result);events.append(e);append(notebook,e);count+=1
    append(out/'HOST_RECEIPTS.jsonl',dict(run_id=runid,result=result));print(json.dumps(dict(run_id=runid,calls=count,host_kind=result['kind'])),flush=True)
   dump_new(out/'notebooks'/f'{branch}_CHECKPOINT.json',dict(condition=condition,seed=seed,parent_trajectory=TR,parent_prefix_events=start,next_step=len(events),events=events))
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];freeze_check()
 dump_new(out/'RUN_MANIFEST.json',dict(status='complete' if count==18 else 'boundary_stop',calls=count,planned_calls=18,stops=stops,input_limit=LIMIT,output_limit=96,training_updates=0,weights_unchanged=True))
def verify():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 freeze_check();tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 load=lambda p:[json.loads(l) for l in p.read_text().splitlines()]
 raw=load(R/'run/RAW.jsonl');plans={p['run_id']:p for p in load(R/'run/PROMPTS.jsonl')};receipts={p['run_id']:p['result'] for p in load(R/'run/HOST_RECEIPTS.jsonl')};cp=json.loads((P/'run/notebooks'/f'{TR}_CHECKPOINT.json').read_text());groups={}
 for condition in CONDITIONS:
  for seed in SEEDS:
   events=cp['events'].copy();rows=[x for x in raw if x['condition']==condition and x['seed']==seed];assert [x['round'] for x in rows]==list(range(len(rows)))
   for k,x in enumerate(rows):
    assert x['prompt']==render(events,condition);ids=tok.apply_chat_template([{'role':'user','content':x['prompt']}],tokenize=True,add_generation_prompt=True)
    assert ids==x['input_token_ids']==plans[x['run_id']]['input_token_ids'];assert x['history_steps']==[e['step'] for e in events];assert x['rng_seed']==seed*100+k;assert x['text']==tok.decode(x['generated_token_ids'],skip_special_tokens=True)
    assert x['host_result']==dispatch(x['text'],condition)==receipts[x['run_id']];assert x['task_score'] is None and x['feedback']==FEEDBACK;assert len(ids)<=LIMIT and len(x['generated_token_ids'])<=96
    assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
    events.append(dict(step=45+k,observation='Open exploration patch.',reply=x['text'],feedback=FEEDBACK,host_result=x['host_result']))
   n=R/'run/notebooks'/f'{condition}_{seed}.jsonl';assert load(n)==events;assert n.read_bytes().startswith((P/'run/notebooks'/f'{TR}.jsonl').read_bytes());assert json.loads(n.with_name(n.stem+'_CHECKPOINT.json').read_text())['events']==events
   groups[f'{condition}_{seed}']=dict(calls=len(rows),requested_reads=sum(x['text'].strip().upper() in ('READ SETUP','READ CLAIM') for x in rows),executed_reads=sum(x['host_result']['kind']=='source_receipt' for x in rows),patch_set_phrase_rows=[x['run_id'] for x in rows if 'hugging face' in x['text'].lower() and 'patch' in x['text'].lower()],cap_stops=sum(x['stop']=='token_limit' for x in rows),upfront_setup=initial(condition) is not None)
 m=json.loads((R/'run/RUN_MANIFEST.json').read_text());assert len(raw)==m['calls'];rawids={x['run_id'] for x in raw}
 for b in m['stops']:assert b['run_id'] not in rawids and len(plans[b['run_id']]['input_token_ids'])==b['tokens']>LIMIT
 for name,v in source_db().items():assert sha(Path('/workspace')/('frr/'+v['source_path'].removeprefix('FRR/')))==v['source_sha256']
 resources=load(R/'run/RESOURCE.jsonl');assert all(x['working_estimate']<x['working_limit'] for x in resources)
 dump_new(R/'CHECKS.json',dict(status='pass',all_rows_reconstructed=len(raw),exact_parent_prefixes=6,receipt_reconstruction=True,source_hashes_verified=True,weights_unchanged=m['weights_unchanged'],training_updates=0))
 dump_new(R/'SUMMARY.json',dict(calls=len(raw),groups=groups,max_input_tokens=max(len(x['input_token_ids']) for x in raw),output_tokens=sum(len(x['generated_token_ids']) for x in raw),generation_seconds=sum(x['seconds'] for x in raw),sampled_max_working_bytes=max(x['working_estimate'] for x in resources)))
 print(json.dumps(dict(calls=len(raw),groups=groups),indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
