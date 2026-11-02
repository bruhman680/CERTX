from pathlib import Path
import json,sys,os,math
from collections import Counter
from io_utils import sha,dump_new,append
from design import queries,LABELS
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical';PRIOR=ROOT.parent/'review-menu-settle-v1'

def frozen():
 f=json.loads((ROOT/'FREEZE.json').read_text())
 assert all(sha(ROOT/n)==h for n,h in f['files'].items())
 assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 qs=queries();lens={q['run_id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs};assert max(lens.values())<=768
 dump_new(ROOT/'QUERIES.json',qs);dump_new(ROOT/'TOKENIZATION.json',{'lengths':lens,'max':max(lens.values()),'no_truncation':True})
 names=[p.name for p in ROOT.iterdir() if p.suffix=='.py']+['PROTOCOL.md','QUERIES.json','TOKENIZATION.json']
 deps=[ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json',PRIOR/'run/RAW.jsonl']
 dump_new(ROOT/'FREEZE.json',{'timing':'after tests and tokenizer checks before model loading and new outputs','files':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'queries':len(qs),'max_tokens':max(lens.values()),'fresh_scores':240*4,'head_check_forwards':8}))

def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 from probability import score,check_heads
 frozen();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73104)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval()
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 qs=json.loads((ROOT/'QUERIES.json').read_text());dump_new(out/'HEAD_CHECK.json',check_heads(model,tok,qs[0]['prompt'],guard))
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],16,guard,q['run_id']);p.update({k:v for k,v in q.items() if k!='prompt'});p['answer']=p['text'].strip() if p['text'].strip() in LABELS else None;p['correct']=p['answer']==q['expected']
  if q['interface']!='legacy_anchor':p['probability']=score(model,tok,q['prompt'],guard,q['run_id'])
  append(out/'RAW.jsonl',p)
  if i%24==0:print(json.dumps({'complete':i,'planned':len(qs)}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];frozen()
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','generation_probes':len(qs),'candidate_scoring_forwards':960,'head_check_forwards':8,'weights_unchanged':True,'training_updates':0,'seed':73104,'threads':2,'dtype':'float32','device':'cpu','numpy_independent_of_model':True})
 print('Completed bounded diagnostic',flush=True)

def metrics(rs):
 return dict(n=len(rs),correct=sum(r['correct'] for r in rs),invalid=sum(r['answer'] is None for r in rs),answers=dict(Counter(r['answer'] or 'INVALID' for r in rs)),cap_stops=sum(r['stop']=='token_limit' for r in rs),mean_gold_logp=sum(r['probability']['candidates'][r['expected']]['sequence_logp'] for r in rs)/len(rs),mean_candidate_mass=sum(r['probability']['candidate_mass'] for r in rs)/len(rs))
def pair(rs,base):
 d=[r['probability']['candidates'][r['expected']]['sequence_logp']-base[r['case_id']]['probability']['candidates'][r['expected']]['sequence_logp'] for r in rs]
 return dict(n=len(rs),before=sum(base[r['case_id']]['correct'] for r in rs),after=sum(r['correct'] for r in rs),repairs=sum(not base[r['case_id']]['correct'] and r['correct'] for r in rs),harms=sum(base[r['case_id']]['correct'] and not r['correct'] for r in rs),gold_logp_increases=sum(x>1e-8 for x in d),gold_logp_decreases=sum(x< -1e-8 for x in d),gold_logp_mean_delta=sum(d)/len(d),gold_logp_deltas=d)
def summarize(raw):
 fresh=[r for r in raw if r['interface']!='legacy_anchor'];initial={r['case_id']:r for r in fresh if r['interface']=='original'};groups={}
 for interface in ('original','old_menu','no_list','simple'):
  none={r['case_id']:r for r in fresh if r['interface']==interface and r['kind']=='none'}
  for kind in (('none',) if interface=='original' else ('none','verified','irrelevant')):
   rs=[r for r in fresh if r['interface']==interface and r['kind']==kind]
   groups[interface+'__'+kind]={'metrics':metrics(rs),'vs_original':pair(rs,initial),'vs_interface_none':pair(rs,none),'by_state':{s:metrics([r for r in rs if r['state']==s]) for s in ('positive','zero','missing','absent')},'by_layout':{s:metrics([r for r in rs if r['layout']==s]) for s in ('lines','inline')}}
 return {'groups':groups,'generations':len(raw),'candidate_scoring_forwards':sum(r.get('probability',{}).get('scoring_forwards',0) for r in raw),'generation_seconds':sum(r['seconds'] for r in raw),'scoring_seconds':sum(r.get('probability',{}).get('seconds',0) for r in raw)}
def verify():
 from transformers import AutoTokenizer
 frozen();tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 qs=json.loads((ROOT/'QUERIES.json').read_text());raw=[json.loads(x) for x in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len(qs)==247
 prior=[json.loads(x) for x in (PRIOR/'run/RAW.jsonl').read_text().splitlines()];prior={r['messages'][0]['content']:r for r in prior};anchors=0
 for q,r in zip(qs,raw):
  assert q['run_id']==r['run_id'] and r['messages']==[{'role':'user','content':q['prompt']}]
  assert tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)==r['input_token_ids']
  assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text']
  assert r['correct']==(r['answer']==q['expected']);assert len(r['generated_token_ids'])<=16
  assert r['answer']==(r['text'].strip() if r['text'].strip() in LABELS else None)
  if r['stop']=='eos':assert r['generated_token_ids'][-1]==tok.eos_token_id
  else:assert r['stop']=='token_limit' and len(r['generated_token_ids'])==16
  if q['interface']=='legacy_anchor':
   old=prior[q['prompt']];assert old['input_token_ids']==r['input_token_ids'] and old['generated_token_ids']==r['generated_token_ids'];anchors+=1
  else:
   p=r['probability'];assert set(p['candidates'])==set(LABELS)
   for label,c in p['candidates'].items():
    assert c['target_ids']==tok.encode(label,add_special_tokens=False)+[tok.eos_token_id]
    assert all(abs(a-b-cv)<1e-9 for a,b,cv in zip(c['target_logits'],c['log_normalizers'],c['token_logps']))
    assert abs(sum(c['token_logps'])-c['sequence_logp'])<1e-9
   from probability import normalized
   rel,logmass=normalized(p['candidates']);assert abs(logmass-p['candidate_log_mass'])<1e-9 and abs(math.exp(logmass)-p['candidate_mass'])<1e-12
   assert all(abs(rel[k]-p['candidate_normalized_mass'][k])<1e-12 for k in rel)
 assert anchors==7
 dump_new(ROOT/'run/SUMMARY.json',summarize(raw));dump_new(ROOT/'CHECKS.json',{'status':'pass','generation_rows':247,'fresh_scored_queries':240,'candidate_sequence_records':960,'exact_prior_anchor_replays':anchors,'frozen_files_and_dependencies':True,'token_decode_scoring_and_probability_reconstruction':True,'weights_unchanged_from_run_manifest':json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['weights_unchanged']})
 print(json.dumps({k:{'score':v['metrics']['correct'],'invalid':v['metrics']['invalid'],'repairs':v['vs_interface_none']['repairs'],'harms':v['vs_interface_none']['harms'],'mean_delta_gold_logp':v['vs_interface_none']['gold_logp_mean_delta']} for k,v in summarize(raw)['groups'].items()},indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
