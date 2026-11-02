from pathlib import Path
import json,math
from collections import Counter
from io_utils import sha,dump_new,append
from design import cases,schedules,review,LABELS,KINDS,STATES,MAP
ROOT=Path(__file__).resolve().parent;BASE=Path('/workspace/cache_backend_models/smollm2-135m');ACQ=ROOT.parent/'simple-readout-acquisition-v1/run/canonical'
EPS=1e-5

def check_freeze():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items());assert all(sha(Path(n))==h for n,h in f['dependencies'].items())

def prepare():
 import os
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);cs=cases();sc=schedules()
 prompts={c['id']:len(tok.apply_chat_template([{'role':'user','content':c['prompt']}],tokenize=True,add_generation_prompt=True)) for c in cs}
 previews=[len(tok.apply_chat_template([{'role':'user','content':review(c,k,a,'PLACEHOLDER')}],tokenize=True,add_generation_prompt=True)) for c in cs for k in KINDS for a in [False,True]]
 assert max(prompts.values())<=768 and max(previews)+64<=768
 dump_new(ROOT/'DATA.json',cs);dump_new(ROOT/'SCHEDULE.json',sc);dump_new(ROOT/'TOKENIZATION.json',{'initial_lengths':prompts,'placeholder_review_max':max(previews),'conservative_proposal_extra_allowance':64,'runtime_input_ceiling':768,'label_tokens':{label:tok.encode(label,add_special_tokens=False)+[tok.eos_token_id] for label in LABELS}})
 names=['DATA.json','SCHEDULE.json','TOKENIZATION.json','PROTOCOL.md','design.py','probability.py','study.py','verify_run.py','test_design.py','generate.py','runtime_reference.py','lora_cpu.py','io_utils.py']
 deps=[ACQ/n for n in ['MANIFEST.json','final/adapter.safetensors','final/manifest.json']]+[ROOT.parent/'real-artifact-provenance-v1/scouts/SDPO_EXTRACTION.md']
 dump_new(ROOT/'FREEZE.json',{'timing':'before all new initial generations, feedback instantiation and model forwards','sha256':{n:sha(ROOT/n) for n in names},'dependencies':{str(p):sha(p) for p in deps}})
 print(json.dumps({'cases':21,'initial_probes':21,'review_probes':168,'generation_probes':189,'candidate_score_forwards':756,'head_check_forwards':8,'placeholder_review_max':max(previews)}))

def run():
 import os
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from runtime_reference import Guard,parameter_digest
 from lora_cpu import inject_lora,load_adapter
 from generate import generate
 from probability import score,check_heads
 check_freeze();out=ROOT/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 torch.set_num_threads(2);torch.manual_seed(73103);tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);assert parameter_digest(model,True)==m['final_digest']
 cs={c['id']:c for c in json.loads((ROOT/'DATA.json').read_text())};dump_new(out/'HEAD_CHECK.json',check_heads(model,tok,next(iter(cs.values()))['prompt'],guard));probes=[];initial={}
 def probe(c,prompt,run_id,kind,attempt):
  p=generate(model,tok,prompt,16,guard,run_id);p.update({'case_id':c['id'],'frame':c['frame'],'state':c['state'],'expected':c['expected'],'kind':kind,'include_attempt':attempt,'answer':p['text'].strip() if p['text'].strip() in LABELS else None});p['correct']=p['answer']==c['expected'];p['scores']=score(model,tok,prompt,guard,run_id);append(out/'RAW.jsonl',p);probes.append(p);return p
 for i,c in enumerate(cs.values(),1):
  initial[c['id']]=probe(c,c['prompt'],'initial_'+c['id'],'initial',None)
  if i%7==0:print(json.dumps({'initial_complete':i,'planned':21}),flush=True)
 for i,entry in enumerate(json.loads((ROOT/'SCHEDULE.json').read_text())):
  c=cs[entry['case_id']];prompt=review(c,entry['kind'],entry['include_attempt'],initial[c['id']]['text']);probe(c,prompt,f'review_{i:03d}',entry['kind'],entry['include_attempt'])
  if (i+1)%21==0:print(json.dumps({'reviews_complete':i+1,'planned':168}),flush=True)
 assert len(probes)==189
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];check_freeze();assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 dump_new(out/'RUN_MANIFEST.json',{'status':'complete','generation_probes':189,'candidate_score_forwards':756,'head_check_forwards':8,'generation_forward_steps':sum(len(p['generated_token_ids']) for p in probes),'training_updates':0,'saved_and_in_memory_weights_unchanged':True,'no_candidate_projection':True,'full_logit_vectors_retained':False});print('Completed frozen-weight feedback-quality preflight',flush=True)

def metrics(rows):
 return {'n':len(rows),'correct':sum(p['correct'] for p in rows),'answers':dict(Counter(p['answer'] or 'INVALID' for p in rows)),'invalid':sum(p['answer'] is None for p in rows),'unknown_on_present':sum(p['state']!='absent' and p['answer']=='UNKNOWN' for p in rows),'unknown_on_absent':sum(p['state']=='absent' and p['answer']=='UNKNOWN' for p in rows),'cap_stops':sum(p['stop']=='token_limit' for p in rows)}

def contrasts(rows,left,case_by):
 out=[]
 for p in rows:
  b=left[p['case_id']];gold=p['expected'];d=p['scores']['candidates'][gold]['sequence_logp']-b['scores']['candidates'][gold]['sequence_logp'];first=p['scores']['candidates'][gold]['token_logps'][0]-b['scores']['candidates'][gold]['token_logps'][0]
  out.append({'id':p['run_id'],'case_id':p['case_id'],'baseline_id':b['run_id'],'initial_or_baseline_correct':b['correct'],'current_correct':p['correct'],'gold_logp_delta':d,'first_token_logp_delta':first,'candidate_normalized_gold_delta':p['scores']['candidate_normalized_mass'][gold]-b['scores']['candidate_normalized_mass'][gold]})
 return out

def contrast_metrics(rows):
 n=len(rows)
 return {'n':n,'correct_before':sum(r['initial_or_baseline_correct'] for r in rows),'correct_after':sum(r['current_correct'] for r in rows),'repairs':sum(not r['initial_or_baseline_correct'] and r['current_correct'] for r in rows),'harms':sum(r['initial_or_baseline_correct'] and not r['current_correct'] for r in rows),'gold_logp_increases':sum(r['gold_logp_delta']>EPS for r in rows),'gold_logp_decreases':sum(r['gold_logp_delta']<-EPS for r in rows),'gold_logp_ties':sum(abs(r['gold_logp_delta'])<=EPS for r in rows),'first_token_logp_increases':sum(r['first_token_logp_delta']>EPS for r in rows),'mean_gold_logp_delta':sum(r['gold_logp_delta'] for r in rows)/n if n else None,'mean_normalized_gold_delta':sum(r['candidate_normalized_gold_delta'] for r in rows)/n if n else None}

def summarize(raw):
 initial={p['case_id']:p for p in raw if p['kind']=='initial'};cs={c['id']:c for c in cases()};groups={};records=[]
 for attempt in [False,True]:
  none={p['case_id']:p for p in raw if p['kind']=='none' and p['include_attempt']==attempt}
  for kind in KINDS:
   rows=[p for p in raw if p['kind']==kind and p['include_attempt']==attempt];contra=contrasts(rows,none,cs);records.extend({**x,'kind':kind,'include_attempt':attempt,'comparison':'matched_none'} for x in contra)
   orig=contrasts(rows,initial,cs)
   strata={}
   for status in [False,True]:
    subset=[x for x in orig if initial[x['case_id']]['correct']==status];strata['initial_correct_'+str(status)]=contrast_metrics(subset)
   wrong_scores=[]
   for row in rows:
    c=cs[row['case_id']];wrong_state='positive' if c['state']=='absent' else STATES[(STATES.index(c['state'])+1)%3];label=MAP[wrong_state];base=none[row['case_id']]
    wrong_scores.append({'free_answer_equals_wrong_note_value':row['answer']==label,'normalized_mass':row['scores']['candidate_normalized_mass'][label],'normalized_mass_delta':row['scores']['candidate_normalized_mass'][label]-base['scores']['candidate_normalized_mass'][label]})
   wrong_summary={'n':len(wrong_scores),'free_answers':sum(x['free_answer_equals_wrong_note_value'] for x in wrong_scores),'mean_normalized_mass':sum(x['normalized_mass'] for x in wrong_scores)/len(wrong_scores),'mean_mass_delta_vs_none':sum(x['normalized_mass_delta'] for x in wrong_scores)/len(wrong_scores)}
   groups[kind+'__attempt'+str(int(attempt))]={'wrong_alternative_diagnostic':wrong_summary,'total':metrics(rows),'by_frame':{f:metrics([p for p in rows if p['frame']==f]) for f in ['canonical','contextual']},'by_state':{s:metrics([p for p in rows if p['state']==s]) for s in MAP},'versus_matched_none':contrast_metrics(contra),'versus_initial':contrast_metrics(orig),'initial_success_error_strata':strata}
 # Attempt retention pair: left omitted, right retained.
 retention={}
 for kind in KINDS:
  left={p['case_id']:p for p in raw if p['kind']==kind and p['include_attempt']==False};right=[p for p in raw if p['kind']==kind and p['include_attempt']==True];retention[kind]=contrast_metrics(contrasts(right,left,cs))
 return {'initial':metrics(list(initial.values())),'initial_by_frame':{f:metrics([p for p in initial.values() if p['frame']==f]) for f in ['canonical','contextual']},'groups':groups,'retention_omitted_to_retained':retention,'pair_records':records,'generation_probes':len(raw),'candidate_score_forwards':sum(p['scores']['scoring_forwards'] for p in raw),'input_tokens_generation_prompts':sum(len(p['input_token_ids']) for p in raw),'generated_tokens':sum(len(p['generated_token_ids']) for p in raw),'scoring_target_tokens':sum(len(r['target_ids']) for p in raw for r in p['scores']['candidates'].values()),'generation_seconds':sum(p['seconds'] for p in raw),'candidate_scoring_seconds':sum(p['scores']['seconds'] for p in raw)}

def score():
 raw=[json.loads(s) for s in (ROOT/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==189
 s=summarize(raw);dump_new(ROOT/'run/SUMMARY.json',s);print(json.dumps({'initial':s['initial'],'groups':{k:{'total':v['total'],'versus_none':v['versus_matched_none']} for k,v in s['groups'].items()}},indent=2))
if __name__=='__main__':
 import sys
 {'prepare':prepare,'run':run,'score':score}[sys.argv[1]]()
