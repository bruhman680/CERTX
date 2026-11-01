from pathlib import Path
import json
from collections import Counter
from io_utils import sha,dump_new,append
from design import queries,records,conditions,MAP
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'

def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 qs=queries();lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs}
 assert max(lengths.values())<=768
 by={(q['source_id'],q['header'],q['condition']):q for q in qs};pairs=[]
 for q in qs:
  if q['kind']!='relevant':continue
  other=by[(q['source_id'],q['header'],q['condition'].replace('relevant','unrelated',1))]
  pairs.append({'relevant_id':q['id'],'unrelated_id':other['id'],'relevant_tokens':lengths[q['id']],'unrelated_tokens':lengths[other['id']],'equal_tokens':lengths[q['id']]==lengths[other['id']]})
 assert len(pairs)==252
 dump_new(ROOT/'DATA.json',records());dump_new(ROOT/'CONDITIONS.json',conditions());dump_new(ROOT/'QUERIES.json',qs)
 dump_new(ROOT/'TOKENIZATION.json',{'prompt_lengths':lengths,'max':max(lengths.values()),'no_truncation':True,'control_pairs':pairs,'equal_length_pairs':sum(p['equal_tokens'] for p in pairs)})
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[ROOT.parent/'fact-first-control-v1/FINAL_CHECKS.json']
 names=['DATA.json','CONDITIONS.json','QUERIES.json','TOKENIZATION.json','PROTOCOL.md','design.py','study.py','test_design.py','verify.py','io_utils.py','generate.py','runtime_reference.py','lora_cpu.py']
 dump_new(ROOT/'FREEZE.json',{'timing':'after local tokenizer length measurements, before model load and all new outputs','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'frozen_probes':len(qs),'control_pairs':len(pairs),'token_equal_pairs':sum(p['equal_tokens'] for p in pairs),'max_prompt_tokens':max(lengths.values())}))

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text())
 assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 qs=json.loads((ROOT/'QUERIES.json').read_text());raw=[];lengths=json.loads((ROOT/'TOKENIZATION.json').read_text())['prompt_lengths']
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],12,guard,q['id']);assert len(p['input_token_ids'])==lengths[q['id']]
  p.update({k:q[k] for k in ['source_id','header','condition','kind','match','access','expected','state','name']})
  p['answer']=p['text'].strip();p['recognized']=p['answer'] in MAP.values();p['correct']=p['answer']==q['expected'];raw.append(p);append(out/'RAW.jsonl',p)
  if i%59==0:print(json.dumps({'complete':i,'planned':len(qs)}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];check_freeze()
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':len(raw),'unique_prompt_strings':len({p['messages'][0]['content'] for p in raw}),'training_updates':0,'weights_unchanged':True,'tool_actions':0,'no_feedback_loop_or_output_projection':True})
 print('Complete531actualgenerations; weights/dependencies unchanged',flush=True)

def metrics(rows):
 return {'n':len(rows),'correct':sum(p['correct'] for p in rows),'recognized':sum(p['recognized'] for p in rows),'outputs':dict(Counter(p['answer'] for p in rows)),'by_status':{s:{'n':sum(p['state']==s for p in rows),'correct':sum(p['state']==s and p['correct'] for p in rows)} for s in MAP},'by_name':{n:{'n':sum(p['name']==n for p in rows),'correct':sum(p['name']==n and p['correct'] for p in rows)} for n in sorted({p['name'] for p in rows})}}

def pair_metrics(pairs):
 return {'n':len(pairs),'same_output':sum(a['answer']==b['answer'] for a,b in pairs),'left_correct':sum(a['correct'] for a,b in pairs),'right_correct':sum(b['correct'] for a,b in pairs),'left_correct_right_wrong':sum(a['correct'] and not b['correct'] for a,b in pairs),'left_wrong_right_correct':sum(not a['correct'] and b['correct'] for a,b in pairs),'both_wrong':sum(not a['correct'] and not b['correct'] for a,b in pairs)}

def summarize(raw):
 by={(p['source_id'],p['header'],p['condition']):p for p in raw};groups={}
 for q in raw:groups.setdefault(q['header']+'__'+q['condition'],[]).append(q)
 controls=[];header_pairs=[];baseline_pairs=[];anchors=[];wordpairs=[]
 for p in raw:
  if p['kind']=='relevant':controls.append((p,by[(p['source_id'],p['header'],p['condition'].replace('relevant','unrelated',1))]))
  if p['header']=='canonical' and p['kind']!='anchor':header_pairs.append((p,by[(p['source_id'],'explicit_visible',p['condition'])]))
  if p['kind'] not in ('anchor','none'):baseline_pairs.append((by[(p['source_id'],p['header'],'no_fields')],p))
  if p['kind']=='anchor':anchors.append((p,by[(p['source_id'],'canonical','no_fields')]))
  if p['access'] in ('yes','no'):
   other=p['condition'].removesuffix(p['access'])+('available' if p['access']=='yes' else 'unavailable')
   wordpairs.append((p,by[(p['source_id'],p['header'],other)]))
 return {'total':metrics(raw),'groups':{k:metrics(v) for k,v in sorted(groups.items())},'paired_relevant_left_unrelated_right':pair_metrics(controls),'paired_canonical_left_explicit_right':pair_metrics(header_pairs),'paired_no_fields_left_extra_fields_right':pair_metrics(baseline_pairs),'paired_bare_left_visible_heading_right':pair_metrics(anchors),'paired_yes_no_left_available_unavailable_right':pair_metrics(wordpairs),'at_cap':sum(p['stop']=='token_limit' for p in raw),'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw),'generation_seconds':sum(p['seconds'] for p in raw)}

def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==531
 s=summarize(raw);dump_new(ROOT/'run/SUMMARY.json',s)
 print(json.dumps({k:v for k,v in s.items() if k!='groups'},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
