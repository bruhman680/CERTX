from pathlib import Path
import json
from collections import Counter
from io_utils import sha,dump_new,append
from design import queries,decode,LABELS,CONTEXTS
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical';PRIOR=ROOT.parent/'worker-context-components-v1'

def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 logical=queries();unique=[];links=[];seen={}
 for q in logical:
  if q['prompt'] not in seen:
   u={**q,'id':f'u_{len(unique):04d}'};unique.append(u);seen[q['prompt']]=u['id']
  links.append({'logical_id':q['id'],'unique_id':seen[q['prompt']]})
 assert len(logical)==672 and len(unique)==560
 lengths={q['id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in unique};assert max(lengths.values())<=768
 old=[json.loads(s) for s in (PRIOR/'run/RAW.jsonl').read_text().splitlines()];oldmap={p['messages'][0]['content']:p for p in old}
 repeats=[{'unique_id':q['id'],'old_id':oldmap[q['prompt']]['run_id']} for q in unique if q['prompt'] in oldmap];assert len(repeats)==126
 dump_new(ROOT/'LOGICAL_QUERIES.json',logical);dump_new(ROOT/'QUERIES.json',unique);dump_new(ROOT/'LINKS.json',links)
 dump_new(ROOT/'TOKENIZATION.json',{'prompt_lengths':lengths,'max':max(lengths.values()),'no_truncation':True,'prior_prompt_repeats':repeats})
 names=['LOGICAL_QUERIES.json','QUERIES.json','LINKS.json','TOKENIZATION.json','PROTOCOL.md','design.py','study.py','test_design.py','verify.py','io_utils.py','generate.py','runtime_reference.py','lora_cpu.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[PRIOR/'run/RAW.jsonl',PRIOR/'CHECKS.json']
 dump_new(ROOT/'FREEZE.json',{'timing':'after tokenizer-only preparation, before model loading and all new outputs','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'actual_planned':560,'logical_links':672,'old_prompt_repeats':126,'max_input_tokens':max(lengths.values())}))

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
 inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 qs=json.loads((ROOT/'QUERIES.json').read_text());lengths=json.loads((ROOT/'TOKENIZATION.json').read_text())['prompt_lengths']
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],48,guard,q['id']);assert len(p['input_token_ids'])==lengths[q['id']]
  p.update({k:q[k] for k in ['name','state','present','context','clarify','absence','note_requested','expected']});p['decoded']=decode(p['text']);p['correct']=p['decoded']['answer']==q['expected'];p['strict_correct']=p['decoded']['strict_whole_answer']==q['expected'];append(out/'RAW.jsonl',p)
  if i%56==0:print(json.dumps({'complete':i,'planned':560}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];check_freeze()
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','actual_generations':560,'unique_prompts':560,'logical_links':672,'training_updates':0,'weights_unchanged':True,'tool_actions':0,'no_feedback_loop_or_output_projection':True});print('Completed560uniqueprobes',flush=True)

def metrics(rows):
 return {'n':len(rows),'correct':sum(p['correct'] for p in rows),'strict_whole_correct':sum(p['strict_correct'] for p in rows),'recognized_first_answer':sum(p['decoded']['answer'] is not None for p in rows),'answers':dict(Counter(p['decoded']['answer'] or 'INVALID' for p in rows)),'nonempty_notes':sum(bool(p['decoded']['note_text']) for p in rows),'note_tag':sum(p['decoded']['note_tag'] for p in rows),'unknown_on_present':sum(p['present'] and p['decoded']['answer']=='UNKNOWN' for p in rows),'correct_unknown_on_absent':sum(not p['present'] and p['decoded']['answer']=='UNKNOWN' for p in rows),'absence_cue_on_present':sum(p['present'] and bool(p['decoded']['absence_cues']) for p in rows),'quoted_status_notes':sum(bool(p['decoded']['status_quotes']) for p in rows),'later_answer_lines':sum(bool(p['decoded']['later_answer_lines']) for p in rows),'cap_stops':sum(p['stop']=='token_limit' for p in rows)}

def paired(pairs):
 return {'n':len(pairs),'same_answer':sum(a['decoded']['answer']==b['decoded']['answer'] for a,b in pairs),'left_correct':sum(a['correct'] for a,b in pairs),'right_correct':sum(b['correct'] for a,b in pairs),'left_correct_right_wrong':sum(a['correct'] and not b['correct'] for a,b in pairs),'left_wrong_right_correct':sum(not a['correct'] and b['correct'] for a,b in pairs),'both_wrong':sum(not a['correct'] and not b['correct'] for a,b in pairs)}

def summarize(raw):
 # For absent records the nominal name is not observed; normalize key to None.
 def key(p,**change):
  d={**p,**change};return (d['name'] if d['present'] else None,d['state'],d['context'],d['clarify'],d['absence'],d['note_requested'])
 by={key(p):p for p in raw};assert len(by)==560
 groups={};pairs_note=[];pairs_absence=[];pairs_clarify=[]
 for p in raw:
  group=f"clarify{int(p['clarify'])}__absence{int(p['absence'])}__note{int(p['note_requested'])}"
  groups.setdefault(group,[]).append(p)
  if not p['note_requested']:pairs_note.append((p,by[key(p,note_requested=True)]))
  if not p['absence']:pairs_absence.append((p,by[key(p,absence=True)]))
  if not p['clarify']:pairs_clarify.append((p,by[key(p,clarify=True)]))
 result={'total':metrics(raw),'groups':{g:{'all':metrics(rs),'present':metrics([p for p in rs if p['present']]),'absent':metrics([p for p in rs if not p['present']]),'by_state':{st:metrics([p for p in rs if p['state']==st]) for st in ['positive','zero','missing','absent']},'by_context':{c:metrics([p for p in rs if p['context']==c]) for c in CONTEXTS}} for g,rs in sorted(groups.items())},'paired_answer_only_left_note_right':paired(pairs_note),'paired_no_absence_clause_left_clause_right':paired(pairs_absence),'paired_no_clarification_left_clarification_right':paired(pairs_clarify),'input_tokens':sum(len(p['input_token_ids']) for p in raw),'output_tokens':sum(len(p['generated_token_ids']) for p in raw),'generation_seconds':sum(p['seconds'] for p in raw)}
 for label,pairs in [('answer_only_left_note_right',pairs_note),('no_absence_clause_left_clause_right',pairs_absence),('no_clarification_left_clarification_right',pairs_clarify)]:
  for present in [True,False]:result['paired_'+label+('__present' if present else '__absent')]=paired([(a,b) for a,b in pairs if a['present']==present])
 notes=sorted((p for p in raw if p['decoded']['note_text']),key=lambda p:p['run_id'])
 result['illustrations']={k:[{'id':p['run_id'],'state':p['state'],'answer':p['decoded']['answer'],'note':p['decoded']['note_text']} for p in [x for x in notes if pred(x)][:3]] for k,pred in [('unknown_notes',lambda p:p['decoded']['answer']=='UNKNOWN'),('status_quote_notes',lambda p:bool(p['decoded']['status_quotes'])),('absence_cue_present',lambda p:p['present'] and bool(p['decoded']['absence_cues']))]}
 return result

def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==560
 s=summarize(raw);dump_new(ROOT/'run/SUMMARY.json',s);print(json.dumps({k:v for k,v in s.items() if k!='groups'},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
