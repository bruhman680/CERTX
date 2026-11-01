from pathlib import Path
import json
from collections import Counter
from design import cases,raw_prompt,worker_prompt,MAP
from verifier import verify
from io_utils import sha,dump_new,append
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);cs=cases();qs=[];links=[];seen={}
 def query(prompt,role):
  if prompt not in seen:
   qid=f'q_{len(qs):03d}';seen[prompt]=qid;qs.append({'id':qid,'prompt':prompt,'role':role,'cap':16 if role=='raw' else 8})
  return seen[prompt]
 for c in cs:links.append({'case_id':c['id'],'raw_id':query(raw_prompt(c),'raw')})
 assert len(qs)==318
 for c in cs:
  v=verify(c['source'],c['layout'],c['target'],'supported')
  if v['verdict']=='READY':query(worker_prompt(v['canonical']),'selected')
 assert len(qs)==327
 lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs};assert max(lengths.values())<=768
 for n,v in [('DATA.json',cs),('QUERIES.json',qs),('LINKS.json',links),('TOKENIZATION.json',{'lengths':lengths,'max':max(lengths.values()),'no_truncation':True})]:dump_new(ROOT/n,v)
 names=['DATA.json','QUERIES.json','LINKS.json','TOKENIZATION.json','PROTOCOL.md','design.py','verifier.py','study.py','verify_run.py','test_design.py','generate.py','runtime_reference.py','lora_cpu.py','io_utils.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[ROOT.parent/'unknown-clause-notepad-v1/FINAL_CHECKS.json']
 dump_new(ROOT/'FREEZE.json',{'timing':'after parser fixtures/tokenizer checks, before model loading and new outputs','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'cases':len(cs),'raw_generations':318,'selected_generations':9,'max_prompt_tokens':max(lengths.values())}))

def routes(raw):
 qs=json.loads((ROOT/'QUERIES.json').read_text());probes={p['run_id']:p for p in raw};promptid={q['prompt']:q['id'] for q in qs};links={l['case_id']:l['raw_id'] for l in json.loads((ROOT/'LINKS.json').read_text())};out=[]
 for c in cases():
  raw_id=links[c['id']];p=probes[raw_id];answer=p['answer']
  for policy in ['strict','supported']:
   v=verify(c['source'],c['layout'],c['target'],policy);wid=promptid.get(worker_prompt(v['canonical'])) if v['verdict']=='READY' else None
   w=probes[wid] if wid else None;expected=MAP[v['state']] if v['verdict']=='READY' else None
   out.append({'id':f'r_{len(out):03d}','case_id':c['id'],'kind':c['kind'],'layout':c['layout'],'target':c['target'],'policy':policy,'verifier':v,'raw_id':raw_id,'raw_answer':answer,'selected_id':wid,'selected_answer':w['answer'] if w else None,'expected_from_supported_record':expected,'raw_grounded_correct':expected is not None and answer==expected,'selected_grounded_correct':expected is not None and w['answer']==expected,'raw_proposal_on_hold':expected is None and answer in LABELS,'raw_class_label_on_hold':expected is None and answer in MAP.values()})
 return out

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 raw=[];qs=json.loads((ROOT/'QUERIES.json').read_text());lengths=json.loads((ROOT/'TOKENIZATION.json').read_text())['lengths']
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],q['cap'],guard,q['id']);assert len(p['input_token_ids'])==lengths[q['id']];p['role']=q['role'];p['answer']=p['text'].strip() if p['text'].strip() in LABELS else None;raw.append(p);append(out/'RAW.jsonl',p)
  if i%54==0:print(json.dumps({'completed':i,'planned':327}),flush=True)
 for row in routes(raw):append(out/'ROUTES.jsonl',row)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];check_freeze();assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_raw_generations':318,'actual_selected_generations':9,'total_generations':327,'logical_case_policy_routes':648,'training_updates':0,'weights_unchanged':True,'tool_actions':0,'no_feedback_loop_or_output_projection':True});print('Completed327generations/648policy-case routes',flush=True)

def metrics(rs):
 ready=[r for r in rs if r['verifier']['verdict']=='READY'];held=[r for r in rs if r['verifier']['verdict']!='READY']
 return {'n':len(rs),'ready':len(ready),'held':len(held),'verdicts':dict(Counter(r['verifier']['verdict'] for r in rs)),'raw_grounded_correct':sum(r['raw_grounded_correct'] for r in rs),'selected_grounded_correct':sum(r['selected_grounded_correct'] for r in rs),'raw_proposals_on_hold':sum(r['raw_proposal_on_hold'] for r in rs),'raw_class_labels_on_hold':sum(r['raw_class_label_on_hold'] for r in rs),'warnings':dict(Counter(w for r in rs for w in r['verifier']['warnings']))}

def summarize(raw,rs):
 return {'policies':{p:{'total':metrics([r for r in rs if r['policy']==p]),'by_layout':{l:metrics([r for r in rs if r['policy']==p and r['layout']==l]) for l in ['lines','brackets','json']},'by_kind':{k:metrics([r for r in rs if r['policy']==p and r['kind']==k]) for k in sorted({r['kind'] for r in rs})}} for p in ['strict','supported']},'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw),'generation_seconds':sum(p['seconds'] for p in raw),'cap_stops':sum(p['stop']=='token_limit' for p in raw),'raw_probes':sum(p['role']=='raw' for p in raw),'selected_probes':sum(p['role']=='selected' for p in raw),'raw_outputs':dict(Counter(p['answer'] or 'INVALID' for p in raw if p['role']=='raw'))}

def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];rs=[json.loads(s) for s in (ROOT/'run/ROUTES.jsonl').read_text().splitlines()];assert len(raw)==327 and len(rs)==648
 s=summarize(raw,rs);dump_new(ROOT/'run/SUMMARY.json',s);print(json.dumps({k:v for k,v in s.items() if k!='policies'}));print(json.dumps({p:v['total'] for p,v in s['policies'].items()},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
