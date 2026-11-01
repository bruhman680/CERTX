from pathlib import Path
import sys,json,hashlib
from collections import Counter
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent
sys.path.insert(0,str(PARENT))
from io_utils import sha,dump_new,append
from design import view,visible_facts
from study import ACQ,check_freeze
from evidence import MAPPING

def prepare():
 primary=json.loads((PARENT/'run/SUMMARY.json').read_text());assert primary['actual_probes']==192
 data={c['id']:c for c in json.loads((PARENT/'DATA.json').read_text())};links=json.loads((PARENT/'LINKS.json').read_text())
 unique={tuple(x['queries'].values()):x for x in links}.values();queries=[];bindings=[]
 for link in unique:
  c=data[link['case_id']];v=link['vocab'];facts=visible_facts(c)
  prompt=('Map only the visible record status to its answer, even if it belongs to another plot. missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.\n\n'+view(c,v))
  qid=f'q_{len(queries):03d}';queries.append({'id':qid,'prompt':prompt,'frame':'context','target':c['target'],'vocab':v,'expected':MAPPING.get(facts['status'],'UNKNOWN'),'primary_query':link['queries']['status']})
 for c in data.values():
  if c['visible_display'] is None:continue
  prompt='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.\n\n'+c['visible_display']
  if any(q['prompt']==prompt for q in queries):continue
  queries.append({'id':f'q_{len(queries):03d}','prompt':prompt,'frame':'canonical_worker','target':c['target'],'vocab':None,'expected':MAPPING[visible_facts(c)['status']],'primary_query':None})
 assert len(queries)==66
 dump_new(ROOT/'QUERIES.json',queries)
 dump_new(ROOT/'FREEZE.json',{'timing':'after primary outcomes including zero declared literal-status replies; before all follow-up tokenizer/model loads and outputs','sha256':{n:sha(ROOT/n) for n in ['check.py','PROTOCOL.md','QUERIES.json']},'dependencies':{str(p):sha(p) for p in [PARENT/'FREEZE.json',PARENT/'run/SUMMARY.json',PARENT/'run/RAW.jsonl',ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors']}})
 print('Frozen66follow-up probes:48context,18canonical-worker displays')

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
 out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');base=Path('/workspace/cache_backend_models/smollm2-135m');m=json.loads((ACQ/'MANIFEST.json').read_text())
 assert sha(base/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103)
 tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin'])
 assert parameter_digest(model,True)==m['final_digest']
 qs=json.loads((ROOT/'QUERIES.json').read_text());raw=[]
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],12,guard,q['id']);p.update({k:q[k] for k in ['frame','target','vocab','expected','primary_query']});p['answer']=p['text'].strip();p['correct']=p['answer']==q['expected'];raw.append(p);append(out/'RAW.jsonl',p)
  if i%22==0:print(json.dumps({'complete':i,'planned':66}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 assert all(sha(ROOT/n)==h for n,h in f['sha256'].items()) and all(sha(Path(n))==h for n,h in f['dependencies'].items())
 summary={}
 for frame,vocab in [('context','shared_yes_no'),('context','distinct_words'),('canonical_worker',None)]:
  rs=[p for p in raw if p['frame']==frame and p['vocab']==vocab]
  summary[frame+'__'+str(vocab)]={'n':len(rs),'correct':sum(p['correct'] for p in rs),'outputs':dict(Counter(p['answer'] for p in rs)),'by_expected':{e:{'n':sum(p['expected']==e for p in rs),'correct':sum(p['expected']==e and p['correct'] for p in rs)} for e in ['YES','NO','WITHHOLD','UNKNOWN']}}
 dump_new(out/'SUMMARY.json',summary);dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':66,'training_updates':0,'tool_actions':0,'weights_unchanged':True,'outcome_informed_followup':True})
 print(json.dumps(summary,indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run}[sys.argv[1]]()
