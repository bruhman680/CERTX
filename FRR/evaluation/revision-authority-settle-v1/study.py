from pathlib import Path
from collections import Counter
import json
from io_utils import sha,dump_new,append
from design import cases,raw_prompt,worker_prompt,MAP
from ledger import resolve,shortcut
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical';LABELS=tuple(MAP.values())+('UNKNOWN',)
def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())
def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);qs=[];links=[];seen={};cs=cases()
 def query(prompt,role):
  if prompt not in seen:
   qid=f'q_{len(qs):03d}';seen[prompt]=qid;qs.append({'id':qid,'prompt':prompt,'role':role,'cap':16 if role=='raw' else 8})
  return seen[prompt]
 for c in cs:links.append({'case_id':c['id'],'raw_id':query(raw_prompt(c),'raw')})
 nraw=len(qs)
 for c in cs:
  v=resolve(c['events'],c['target'])
  if v['verdict']=='KNOWN':query(worker_prompt(c['target'],v['state']),'selected')
 assert len(qs)-nraw==9 and len(qs)<=159
 lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs};assert max(lengths.values())<=768
 for n,v in [('DATA.json',cs),('QUERIES.json',qs),('LINKS.json',links),('TOKENIZATION.json',{'lengths':lengths,'max':max(lengths.values()),'no_truncation':True})]:dump_new(ROOT/n,v)
 names=['DATA.json','QUERIES.json','LINKS.json','TOKENIZATION.json','PROTOCOL.md','design.py','ledger.py','study.py','verify_run.py','test_design.py','generate.py','runtime_reference.py','lora_cpu.py','io_utils.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[ROOT.parent/'evidence-boundary-transfer-v1/CHECKS.json']
 dump_new(ROOT/'FREEZE.json',{'timing':'after authored permutation tests and tokenizer checks; before new model load/outputs','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}});print(json.dumps({'logical_cases':150,'raw_calls':nraw,'selected_calls':9,'total_calls':len(qs),'max_prompt_tokens':max(lengths.values())}))

def receipts(raw):
 by={p['run_id']:p for p in raw};qs=json.loads((ROOT/'QUERIES.json').read_text());pid={q['prompt']:q['id'] for q in qs};links={l['case_id']:l['raw_id'] for l in json.loads((ROOT/'LINKS.json').read_text())};out=[]
 for c in cases():
  v=resolve(c['events'],c['target']);rid=links[c['id']];known=v['verdict']=='KNOWN';expected=MAP[v['state']] if known else None;wid=pid[worker_prompt(c['target'],v['state'])] if known else None
  labels={mode:MAP.get(shortcut(c['events'],c['target'],mode)) for mode in ['arrival_last','max_revision']}
  out.append({'case_id':c['id'],'kind':c['kind'],'target':c['target'],'reverse':c['reverse'],'resolution':v,'raw_id':rid,'raw_answer':by[rid]['answer'],'selected_id':wid,'selected_answer':by[wid]['answer'] if wid else None,'expected_label':expected,'raw_known_correct':known and by[rid]['answer']==expected,'selected_known_correct':known and by[wid]['answer']==expected,'raw_class_on_hold':not known and by[rid]['answer'] in MAP.values(),'shortcuts':labels})
 return out

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2);torch.manual_seed(73103)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 raw=[];qs=json.loads((ROOT/'QUERIES.json').read_text())
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],q['cap'],guard,q['id']);p['role']=q['role'];p['answer']=p['text'].strip() if p['text'].strip() in LABELS else None;append(out/'RAW.jsonl',p);raw.append(p)
  if i%30==0:print(json.dumps({'complete':i,'planned':len(qs)}),flush=True)
 for row in receipts(raw):append(out/'RECEIPTS.jsonl',row)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];check_freeze();assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':len(qs),'raw_generations':sum(q['role']=='raw' for q in qs),'selected_generations':9,'logical_cases':150,'training_updates':0,'weights_unchanged':True,'tool_actions':0});print('Completed bounded ledger run',flush=True)

def metrics(rs):
 return {'n':len(rs),'known':sum(r['resolution']['verdict']=='KNOWN' for r in rs),'verdicts':dict(Counter(r['resolution']['verdict'] for r in rs)),'raw_known_correct':sum(r['raw_known_correct'] for r in rs),'selected_known_correct':sum(r['selected_known_correct'] for r in rs),'raw_class_on_hold':sum(r['raw_class_on_hold'] for r in rs),'shortcuts':{mode:{'known_correct':sum(r['expected_label'] is not None and r['shortcuts'][mode]==r['expected_label'] for r in rs),'class_on_hold':sum(r['expected_label'] is None and r['shortcuts'][mode] is not None for r in rs)} for mode in ['arrival_last','max_revision']}}
def summarize(raw,rs):
 return {'total':metrics(rs),'by_kind':{k:metrics([r for r in rs if r['kind']==k]) for k in sorted({r['kind'] for r in rs})},'by_arrival':{str(v):metrics([r for r in rs if r['reverse']==v]) for v in [False,True]},'actual_calls':len(raw),'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw),'generation_seconds':sum(p['seconds'] for p in raw),'cap_stops':sum(p['stop']=='token_limit' for p in raw),'raw_outputs':dict(Counter(p['answer'] or 'INVALID' for p in raw if p['role']=='raw'))}
def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];rs=[json.loads(s) for s in (ROOT/'run/RECEIPTS.jsonl').read_text().splitlines()];s=summarize(raw,rs);dump_new(ROOT/'run/SUMMARY.json',s);print(json.dumps({k:v for k,v in s.items() if k!='by_kind'},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
