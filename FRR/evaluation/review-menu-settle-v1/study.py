from pathlib import Path
import json
from collections import Counter
from io_utils import sha,dump_new,append
from design import queries,MENUS,LABELS
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical';PRIOR=ROOT.parent/'feedback-quality-probe-v1'

def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);qs=queries();lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs};assert max(lengths.values())<=768
 old=[json.loads(s) for s in (PRIOR/'run/RAW.jsonl').read_text().splitlines()];by_prompt={p['messages'][0]['content']:p for p in old};repeats=[{'new_id':q['id'],'prior_id':by_prompt[q['prompt']]['run_id']} for q in qs if q['prompt'] in by_prompt];assert len(repeats)==63
 dump_new(ROOT/'QUERIES.json',qs);dump_new(ROOT/'TOKENIZATION.json',{'lengths':lengths,'max':max(lengths.values()),'no_truncation':True,'prior_repeats':repeats})
 names=['QUERIES.json','TOKENIZATION.json','PROTOCOL.md','design.py','design_reference.py','study.py','verify_run.py','test_design.py','generate.py','runtime_reference.py','lora_cpu.py','io_utils.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[PRIOR/'run/RAW.jsonl',PRIOR/'run/RUN_MANIFEST.json']
 dump_new(ROOT/'FREEZE.json',{'timing':'after tokenizer checks,before model load/newoutputs','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}});print(json.dumps({'actual_unique_prompts':231,'original_anchors':21,'reviews':210,'prior_sequence_replays':63,'max_prompt_tokens':max(lengths.values())}))

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 qs=json.loads((ROOT/'QUERIES.json').read_text());raw=[]
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],16,guard,q['id']);p.update({k:q[k] for k in ['case_id','frame','state','expected','kind','menu','first_option']});p['answer']=p['text'].strip() if p['text'].strip() in LABELS else None;p['correct']=p['answer']==q['expected'];raw.append(p);append(out/'RAW.jsonl',p)
  if i%33==0:print(json.dumps({'complete':i,'planned':231}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];check_freeze();assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generation_probes':231,'generation_forward_steps':sum(len(p['generated_token_ids']) for p in raw),'new_probability_score_forwards':0,'training_updates':0,'weights_unchanged':True,'tool_actions':0});print('Completed final bounded review-menu run',flush=True)

def metrics(rows):
 return {'n':len(rows),'correct':sum(p['correct'] for p in rows),'outputs':dict(Counter(p['answer'] or 'INVALID' for p in rows)),'recognized':sum(p['answer'] is not None for p in rows),'first_option_matches':sum(p['first_option'] is not None and p['answer']==p['first_option'] for p in rows),'cap_stops':sum(p['stop']=='token_limit' for p in rows)}
def pairs(rows,baseline):
 return {'n':len(rows),'answer_changes':sum(p['answer']!=baseline[p['case_id']]['answer'] for p in rows),'correct_before':sum(baseline[p['case_id']]['correct'] for p in rows),'correct_after':sum(p['correct'] for p in rows),'repairs':sum(not baseline[p['case_id']]['correct'] and p['correct'] for p in rows),'harms':sum(baseline[p['case_id']]['correct'] and not p['correct'] for p in rows)}
def summarize(raw):
 initial={p['case_id']:p for p in raw if p['kind']=='initial'};groups={}
 for kind in ['none','verified']:
  baseline={p['case_id']:p for p in raw if p['kind']==kind and p['menu']=='rotation_0'}
  for menu in MENUS:
   rs=[p for p in raw if p['kind']==kind and p['menu']==menu]
   groups[kind+'__'+menu]={'total':metrics(rs),'by_frame':{f:metrics([p for p in rs if p['frame']==f]) for f in ['canonical','contextual']},'by_state':{s:metrics([p for p in rs if p['state']==s]) for s in ['positive','zero','missing','absent']},'versus_rotation0':pairs(rs,baseline),'versus_initial':pairs(rs,initial)}
 return {'initial':metrics(list(initial.values())),'groups':groups,'generation_probes':len(raw),'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw),'generation_seconds':sum(p['seconds'] for p in raw),'new_probability_scores':0}
def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==231
 s=summarize(raw);dump_new(ROOT/'run/SUMMARY.json',s);print(json.dumps({'initial':s['initial'],'groups':{k:{'total':v['total'],'paired':v['versus_rotation0']} for k,v in s['groups'].items()}},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
