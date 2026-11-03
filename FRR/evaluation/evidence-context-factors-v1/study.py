from pathlib import Path
import json,sys,os,math
from collections import Counter
from io_utils import sha,dump_new,append
from design import build,LABELS
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical';PRIOR=ROOT.parent/'review-menu-settle-v1'

def frozen():
 f=json.loads((ROOT/'FREEZE.json').read_text())
 assert all(sha(ROOT/n)==h for n,h in f['files'].items())
 assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 qs,padding=build(tok);ids={q['run_id']:tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True) for q in qs};dump_new(ROOT/'PADDING.json',padding);lens={q['run_id']:len(tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)) for q in qs};assert max(lens.values())<=768
 dump_new(ROOT/'QUERIES.json',qs);dump_new(ROOT/'TOKENIZATION.json',{'lengths':lens,'max':max(lens.values()),'no_truncation':True,'input_token_ids':ids,'candidate_target_ids':{label:tok.encode(label,add_special_tokens=False)+[tok.eos_token_id] for label in LABELS}})
 names=[p.name for p in ROOT.iterdir() if p.suffix=='.py']+['PROTOCOL.md','QUERIES.json','TOKENIZATION.json','PADDING.json']
 deps=[ACQ/'MANIFEST.json',ACQ/'final/adapter.safetensors',ACQ/'final/manifest.json',PRIOR/'run/RAW.jsonl']
 dump_new(ROOT/'FREEZE.json',{'timing':'after tests and tokenizer checks before model loading and new outputs','files':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'queries':len(qs),'max_tokens':max(lens.values()),'fresh_scores':160*4,'head_check_forwards':8}))

def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 from probability import score,check_heads
 frozen();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73105)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load')
 model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval()
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after']
 qs=json.loads((ROOT/'QUERIES.json').read_text());dump_new(out/'HEAD_CHECK.json',check_heads(model,tok,qs[0]['prompt'],guard))
 for i,q in enumerate(qs,1):
  p=generate(model,tok,q['prompt'],16,guard,q['run_id']);p.update({k:v for k,v in q.items() if k!='prompt'});p['answer']=p['text'].strip() if p['text'].strip() in LABELS else None;p['correct']=p['answer']==q['expected']
  if q['condition']!='legacy_anchor':p['probability']=score(model,tok,q['prompt'],guard,q['run_id'])
  append(out/'RAW.jsonl',p)
  if i%24==0:print(json.dumps({'complete':i,'planned':len(qs)}),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];frozen()
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','generation_probes':len(qs),'candidate_scoring_forwards':640,'head_check_forwards':8,'weights_unchanged':True,'training_updates':0,'seed':73105,'threads':2,'dtype':'float32','device':'cpu','numpy_independent_of_model':True})
 print('Completed bounded diagnostic',flush=True)

def metrics(rs):
 return dict(n=len(rs),correct=sum(r['correct'] for r in rs),invalid=sum(r['answer'] is None for r in rs),answers=dict(Counter(r['answer'] or 'INVALID' for r in rs)),cap_stops=sum(r['stop']=='token_limit' for r in rs),mean_gold_logp=sum(r['probability']['candidates'][r['expected']]['sequence_logp'] for r in rs)/len(rs),mean_gold_relative_mass=sum(r['probability']['candidate_normalized_mass'][r['expected']] for r in rs)/len(rs),mean_gold_first_token_prob=sum(r['probability']['candidates'][r['expected']]['first_token_full_vocab_prob'] for r in rs)/len(rs),mean_candidate_mass=sum(r['probability']['candidate_mass'] for r in rs)/len(rs))
def pair(rs,base):
 d=[r['probability']['candidates'][r['expected']]['sequence_logp']-base[r['case_id']]['probability']['candidates'][r['expected']]['sequence_logp'] for r in rs]
 return dict(n=len(rs),before=sum(base[r['case_id']]['correct'] for r in rs),after=sum(r['correct'] for r in rs),repairs=sum(not base[r['case_id']]['correct'] and r['correct'] for r in rs),harms=sum(base[r['case_id']]['correct'] and not r['correct'] for r in rs),gold_logp_increases=sum(x>1e-5 for x in d),gold_logp_decreases=sum(x< -1e-5 for x in d),gold_logp_ties=sum(abs(x)<=1e-5 for x in d),gold_logp_mean_delta=sum(d)/len(d),gold_logp_deltas=d)
def factor_rows(raw,axis):
 fresh=[r for r in raw if r['condition'] not in ('original','padded','legacy_anchor')]
 index={(r['case_id'],r['content'],r['authority'],r['placement']):r for r in fresh}
 rows=[]
 for left in fresh:
  if axis=='content' and left['content']=='filler':key=(left['case_id'],'duplicate',left['authority'],left['placement'])
  elif axis=='authority' and left['authority'] is False:key=(left['case_id'],left['content'],True,left['placement'])
  elif axis=='placement' and left['placement']=='before':key=(left['case_id'],left['content'],left['authority'],'after')
  else:continue
  right=index[key];gold=left['expected'];delta=right['probability']['candidates'][gold]['sequence_logp']-left['probability']['candidates'][gold]['sequence_logp']
  rows.append({'case_id':left['case_id'],'split':left['split'],'layout':left['layout'],'state':left['state'],'left':left['run_id'],'right':right['run_id'],'correct_before':left['correct'],'correct_after':right['correct'],'answer_changed':left['answer']!=right['answer'],'repair':not left['correct'] and right['correct'],'harm':left['correct'] and not right['correct'],'gold_logp_delta':delta})
 assert len(rows)==64
 return rows

def factor_metrics(rows):
 return {'paired_contrasts':len(rows),'cases':len({r['case_id'] for r in rows}),'correct_before':sum(r['correct_before'] for r in rows),'correct_after':sum(r['correct_after'] for r in rows),'repairs':sum(r['repair'] for r in rows),'harms':sum(r['harm'] for r in rows),'answer_changes':sum(r['answer_changed'] for r in rows),'mean_gold_logp_delta':sum(r['gold_logp_delta'] for r in rows)/len(rows),'logp_increases':sum(r['gold_logp_delta']>1e-5 for r in rows),'logp_decreases':sum(r['gold_logp_delta']< -1e-5 for r in rows),'logp_ties':sum(abs(r['gold_logp_delta'])<=1e-5 for r in rows)}

def summarize(raw):
 fresh=[r for r in raw if r['condition']!='legacy_anchor'];initial={r['case_id']:r for r in fresh if r['condition']=='original'};pad={r['case_id']:r for r in fresh if r['condition']=='padded'};groups={}
 for condition in dict.fromkeys(r['condition'] for r in fresh):
  rs=[r for r in fresh if r['condition']==condition]
  groups[condition]={'metrics':metrics(rs),'vs_original':pair(rs,initial),'vs_padded':pair(rs,pad),'by_state':{x:metrics([r for r in rs if r['state']==x]) for x in ('positive','zero','missing','absent')},'by_layout':{x:metrics([r for r in rs if r['layout']==x]) for x in ('lines','inline')},'by_split':{x:metrics([r for r in rs if r['split']==x]) for x in ('discovery','confirmation')}}
 factors={}
 for axis in ('content','authority','placement'):
  rows=factor_rows(raw,axis);factors[axis]={'total':factor_metrics(rows),'by_split':{x:factor_metrics([r for r in rows if r['split']==x]) for x in ('discovery','confirmation')},'by_state':{x:factor_metrics([r for r in rows if r['state']==x]) for x in ('positive','zero','missing','absent')},'by_layout':{x:factor_metrics([r for r in rows if r['layout']==x]) for x in ('lines','inline')},'rows':rows}
 return {'groups':groups,'factors':factors,'generations':len(raw),'candidate_scoring_forwards':sum(r.get('probability',{}).get('scoring_forwards',0) for r in raw),'generation_seconds':sum(r['seconds'] for r in raw),'scoring_seconds':sum(r.get('probability',{}).get('seconds',0) for r in raw)}
def verify():
 from transformers import AutoTokenizer
 frozen();tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
 qs=json.loads((ROOT/'QUERIES.json').read_text());raw=[json.loads(x) for x in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==len(qs)==167
 prior=[json.loads(x) for x in (PRIOR/'run/RAW.jsonl').read_text().splitlines()];prior={r['messages'][0]['content']:r for r in prior};anchors=0
 for q,r in zip(qs,raw):
  assert q['run_id']==r['run_id'] and r['messages']==[{'role':'user','content':q['prompt']}]
  assert tok.apply_chat_template(r['messages'],tokenize=True,add_generation_prompt=True)==r['input_token_ids']
  assert r['input_token_ids']==json.loads((ROOT/'TOKENIZATION.json').read_text())['input_token_ids'][q['run_id']]
  assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text']
  assert r['correct']==(r['answer']==q['expected']);assert len(r['generated_token_ids'])<=16
  assert r['answer']==(r['text'].strip() if r['text'].strip() in LABELS else None)
  if r['stop']=='eos':assert r['generated_token_ids'][-1]==tok.eos_token_id
  else:assert r['stop']=='token_limit' and len(r['generated_token_ids'])==16
  if q['condition']=='legacy_anchor':
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
 dump_new(ROOT/'run/SUMMARY.json',summarize(raw));dump_new(ROOT/'CHECKS.json',{'status':'pass','generation_rows':167,'fresh_scored_queries':160,'candidate_sequence_records':640,'exact_prior_anchor_replays':anchors,'frozen_files_and_dependencies':True,'token_decode_scoring_and_probability_reconstruction':True,'weights_unchanged_from_run_manifest':json.loads((ROOT/'run/RUN_MANIFEST.json').read_text())['weights_unchanged']})
 print(json.dumps({'groups':{k:{'score':v['metrics']['correct'],'invalid':v['metrics']['invalid']} for k,v in summarize(raw)['groups'].items()},'factors':{k:v['by_split'] for k,v in summarize(raw)['factors'].items()}},indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify}[sys.argv[1]]()
