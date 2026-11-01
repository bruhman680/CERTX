from pathlib import Path
import json,hashlib
from collections import Counter
from io_utils import sha,dump_new,append
from design import cases,render,visible_facts,action_from_facts,decode_fact
from decoder import decode_v2
from task_reference import finish_route
from routing_reference import retrieve
ROOT=Path(__file__).resolve().parent
ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'
TASKS=('action','role','status','access');VOCABS=('shared_yes_no','distinct_words')

def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text())
 assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
 assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 data=cases();queries=[];links=[];seen={}
 for c in data:
  for vocab in VOCABS:
   group={}
   for task in TASKS:
    prompt=render(c,vocab,task)
    if prompt not in seen:
     qid=f'q_{len(queries):03d}';seen[prompt]=qid
     queries.append({'id':qid,'prompt':prompt,'task':task,'vocab':vocab,'target':c['target'],'cap':24 if task=='action' else 12})
    group[task]=seen[prompt]
   links.append({'case_id':c['id'],'vocab':vocab,'queries':group})
 assert len(data)==72 and len(queries)==192 and len(links)==144
 dump_new(ROOT/'DATA.json',data);dump_new(ROOT/'QUERIES.json',queries);dump_new(ROOT/'LINKS.json',links)
 names=['DATA.json','QUERIES.json','LINKS.json','PROTOCOL.md','design.py','study.py','test_design.py','verify.py','generate.py','task_reference.py','routing_reference.py','evidence.py','runtime_reference.py','lora_cpu.py','io_utils.py','decoder.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]
 deps+=[ROOT.parent/'descriptions-and-rules-v1/run/ROUTER_RAW.jsonl']
 dump_new(ROOT/'FREEZE.json',{'timing':'before all new tokenizer/model loading and output inspection','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print('Frozen72logical worlds,48unique observations,192actual planned probes')

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from generate import generate
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl')
 base=Path('/workspace/cache_backend_models/smollm2-135m');manifest=json.loads((ACQ/'MANIFEST.json').read_text())
 assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103)
 tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
 queries=json.loads((ROOT/'QUERIES.json').read_text());links=json.loads((ROOT/'LINKS.json').read_text());data={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())}
 lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in queries}
 assert max(lengths.values())<=768
 dump_new(out/'TOKENIZATION.json',{'prompt_lengths':lengths,'max':max(lengths.values()),'no_truncation':True})
 guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=manifest['base_pin'])
 assert parameter_digest(model,True)==manifest['final_digest']
 probes={}
 for i,q in enumerate(queries,1):
  p=generate(model,tok,q['prompt'],q['cap'],guard,q['id'])
  p.update({k:q[k] for k in ('task','vocab','target')})
  p['proposal']=decode_v2(p['text'])['action'] if q['task']=='action' else decode_fact(p['text'],q['task'])
  probes[q['id']]=p;append(out/'RAW.jsonl',p)
  if i%32==0:print(json.dumps({'actual_probes':i,'planned':len(queries)}),flush=True)
 workers={};routes=[]
 def execute(c,action,meta):
  tool=None;state=None;wid=None;hit=False
  if action in ('FULL','TARGET'):
   tool=retrieve(c,action)
   if tool['available']:
    prompt='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+tool['source']
    if tool['kind']=='full':prompt='Read only the record for the target plot.\n'+prompt
    key=hashlib.sha256(prompt.encode()).hexdigest();hit=key in workers
    if not hit:
     w=generate(model,tok,prompt,8,guard,f'worker_{len(workers):03d}')
     w.update({'prompt_sha256':key,'state':{'YES':'positive','NO':'zero','WITHHOLD':'missing'}.get(w['text'].strip())})
     workers[key]=w;append(out/'WORKER_RAW.jsonl',w)
    w=workers[key];state=w['state'];wid=w['run_id']
  r={'route_id':f'r_{len(routes):04d}','case_id':c['id'],'target':c['target'],'kind':c['kind'],**meta,**finish_route(c,action,state,tool),'tool':tool,'worker_id':wid,'worker_cache_hit':hit}
  routes.append(r);append(out/'ROUTES.jsonl',r)
 for link in links:
  c=data[link['case_id']];expected=visible_facts(c)
  facts={task:probes[link['queries'][task]]['proposal'] for task in TASKS if task!='action'}
  corrected={k:expected[k] if facts[k]!=expected[k] else facts[k] for k in facts}
  meta={'vocab':link['vocab'],'queries':link['queries'],'fact_proposals':facts,'visible_facts':expected,'corrections':[k for k in facts if facts[k]!=expected[k]]}
  actions={'direct':probes[link['queries']['action']]['proposal'],'proposed_facts':action_from_facts(facts),'checked_facts':action_from_facts(corrected),'observed_input':action_from_facts(expected)}
  for policy,action in actions.items():execute(c,action,{**meta,'policy':policy})
 assert len(routes)==576
 assert parameter_digest(model,True)==manifest['final_digest']
 assert parameter_digest(model,False)==manifest['base_digest_after']
 check_freeze();assert sha(base/'model.safetensors')==manifest['base_pin']['weights_sha256']
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_observation_action_probes':len(probes),'actual_worker_probes':len(workers),'logical_routes':len(routes),'training_updates':0,'weights_unchanged':True,'no_feedback_loop_or_output_projection':True})
 print(json.dumps({'complete':True,'probes':len(probes),'workers':len(workers),'routes':len(routes)}),flush=True)

def metrics(rows):
 return {'n':len(rows),'grounded':sum(r['grounded_answer'] for r in rows),'justified_unknown':sum(r['justified_unknown'] for r in rows),'resolved':sum(r['resolved_in_this_toy'] for r in rows),'requests':sum(r['requested'] for r in rows),'unavailable_requests':sum(r['unavailable_request'] for r in rows),'nominal_units':sum(r['nominal_tool_cost'] for r in rows),'invalid':sum(r['end']=='INVALID_ACTION' for r in rows),'actions':dict(Counter(r['action'] or 'INVALID' for r in rows))}

def summarize(raw,rows):
 byid={p['run_id']:p for p in raw};data={c['id']:c for c in cases()};links=json.loads((ROOT/'LINKS.json').read_text())
 # Count observation tuples once, not their hidden-world repetitions.
 unique={tuple(link['queries'].values()):link for link in links}.values()
 facts=[]
 for link in unique:
  c=data[link['case_id']];e=visible_facts(c)
  facts.append({'target':c['target'],'vocab':link['vocab'],'expected':e,'proposed':{k:byid[link['queries'][k]]['proposal'] for k in ('role','status','access')},'direct':byid[link['queries']['action']]['proposal']})
 groups={}
 for v in VOCABS:
  for target in ['all','Aster','Linden','Rowan']:
   fs=[x for x in facts if x['vocab']==v and (target=='all' or x['target']==target)]
   groups[v+'__'+target]={'observations':len(fs),'fields':{k:{'recognized':sum(x['proposed'][k] is not None for x in fs),'correct':sum(x['proposed'][k]==x['expected'][k] for x in fs)} for k in ('role','status','access')},'joint_correct':sum(x['proposed']==x['expected'] for x in fs),'proposed_action_matches_observed_rule':sum(action_from_facts(x['proposed'])==action_from_facts(x['expected']) for x in fs),'direct_matches_observed_rule':sum(x['direct']==action_from_facts(x['expected']) for x in fs)}
 policies={v+'__'+p:metrics([r for r in rows if r['vocab']==v and r['policy']==p]) for v in VOCABS for p in ('direct','proposed_facts','checked_facts','observed_input')}
 return {'fact_groups':groups,'policies':policies,'observations':facts,'at_cap':sum(p['stop']=='token_limit' for p in raw),'actual_probes':len(raw),'generation_seconds':sum(p['seconds'] for p in raw),'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw)}

def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];rows=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()]
 s=summarize(raw,rows);dump_new(ROOT/'run/SUMMARY.json',s)
 print(json.dumps({k:v for k,v in s.items() if k!='observations'},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
