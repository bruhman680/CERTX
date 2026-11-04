"""Fixed separate action-binding diagnostic. Primary is read-only."""
from pathlib import Path
import os,sys,json,importlib.util,collections
from io_utils import sha,dump_new,append
R=Path(__file__).resolve().parent;OLD=R.parent/'action-room-capability-checks-v1'
spec=importlib.util.spec_from_file_location('prior_action_room',OLD/'study.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
routine=prior.routine;BASE=prior.BASE;ACQ=prior.ACQ
TARGETS=(('4 + 5',9),('9 - 3',6),('3 * 4',12),('8 / 2',4));CONTEXTS=('clean','carried');SEEDS=(2401,2402);RELATIONS=('matching','different')
CLAUSE='Example syntax: TRY 2 + 3. This example is not a task you must perform.'
def events(context):return [json.loads(x) for x in (R/'PRIMARY_SNAPSHOT.jsonl').read_text().splitlines()] if context=='carried' else []
def cases():
 for context in CONTEXTS:
  for ti,(target,gold) in enumerate(TARGETS):
   for seed in SEEDS:
    for relation in RELATIONS:
     di=ti if relation=='matching' else (ti+1)%len(TARGETS);demo,demo_gold=TARGETS[di]
     yield dict(run_id=f'{context}_t{ti}_{seed}_{relation}',context=context,target_index=ti,target=target,gold=gold,seed=seed,rng_seed=seed*1000+ti,relation=relation,demo=demo,demo_gold=demo_gold)
def prompt(case):
 request='Get the calculator result for '+case['target']+' by issuing a tool request.'
 q=prior.render(events(case['context']),'current',request)
 assert q.count(CLAUSE)==1
 return q.replace(CLAUSE,'Example syntax: TRY '+case['demo']+'. This example is not a task you must perform.',1)
def score(text,host,case):
 valid=host['kind']=='calculation';target=valid and prior.bound_expr(host.get('expression',''),case['target']);demo=valid and prior.bound_expr(host.get('expression',''),case['demo'])
 return dict(valid_calculator_request=valid,target_expression_bound=bool(target),demonstration_expression_bound=bool(demo),numeric_goal_match=bool(valid and host.get('result')==case['gold']),strict_success=bool(target and host.get('result')==case['gold']),wrong_demo_execution=bool(case['relation']=='different' and demo and host.get('result')==case['demo_gold']))
def freeze_check():
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h,p
 for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():assert sha(Path(p))==h,p
 assert json.loads((routine.ENV/'STATE.json').read_text())['next_step']==100 and (routine.ENV/'PAUSE').exists()
def prepare():
 paths=set(Path(p) for p in json.loads((OLD/'FREEZE.json').read_text())['files'])
 paths.update(R.glob('*.py'));paths.update(R/p for p in ('PROTOCOL.md','PRIMARY_SNAPSHOT.jsonl','PRIMARY_STATE.json','PRIMARY_BEFORE.json'))
 for mod in tuple(sys.modules.values()):
  p=getattr(mod,'__file__',None)
  if p and p.startswith('/workspace/frr/') and p.endswith('.py'):paths.add(Path(p))
 dump_new(R/'FREEZE.json',dict(timing='before all32calls',files={str(p):sha(p) for p in sorted(paths)}))
def run():
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
 import torch
 from transformers import AutoTokenizer,AutoModelForCausalLM
 from lora_cpu import inject_lora,load_adapter
 from runtime_reference import Guard,parameter_digest
 from generate_capacity import generate
 freeze_check();out=R/'run';out.mkdir();guard=Guard(5153960755,out/'RESOURCE.jsonl');m=json.loads((ACQ/'MANIFEST.json').read_text());assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];torch.set_num_threads(2)
 tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,ACQ/'final',base_pin=m['base_pin']);model.eval()
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];count=0
 for case in cases():
  q=prompt(case);ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert len(ids)<=8096
  append(out/'PROMPTS.jsonl',dict(**case,prompt=q,input_token_ids=ids,history_steps=[e['step'] for e in events(case['context'])[-12:]]))
  row=generate(model,tok,q,guard,case['run_id'],case['rng_seed']);row.update(case);row['host_result']=routine.view_dispatch(row['text'],events(case['context']));row['evaluation']=score(row['text'],row['host_result'],case);row['task_score']=None;row['feedback']=prior.FEEDBACK;append(out/'RAW.jsonl',row);count+=1
  print(json.dumps(dict(run_id=case['run_id'],calls=count,host_kind=row['host_result']['kind'])),flush=True)
 assert count==32 and parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(BASE/'model.safetensors')==m['base_pin']['weights_sha256'];freeze_check();dump_new(out/'RUN_MANIFEST.json',dict(status='complete',calls=count,weights_unchanged=True,training_updates=0,primary_untouched=True,input_limit=8096,output_limit=96))
def verify():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 freeze_check();tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False);raw=[json.loads(x) for x in (R/'run/RAW.jsonl').read_text().splitlines()];plans=[json.loads(x) for x in (R/'run/PROMPTS.jsonl').read_text().splitlines()];assert len(raw)==len(plans)==32
 for c,x,p in zip(cases(),raw,plans,strict=True):
  for k,v in c.items():assert x[k]==p[k]==v
  q=prompt(c);assert x['prompt']==p['prompt']==q;assert x['input_token_ids']==p['input_token_ids']==tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert len(x['input_token_ids'])<=8096 and len(x['generated_token_ids'])<=96;assert x['text']==tok.decode(x['generated_token_ids'],skip_special_tokens=True)
  assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
  h=routine.view_dispatch(x['text'],events(c['context']));assert x['host_result']==h and x['evaluation']==score(x['text'],h,c);assert x['task_score'] is None and x['feedback']==prior.FEEDBACK
  assert p['history_steps']==[e['step'] for e in events(c['context'])[-12:]]
 resources=[json.loads(x) for x in (R/'run/RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
 assert json.loads((R/'run/RUN_MANIFEST.json').read_text())['weights_unchanged']
 dump_new(R/'CHECKS.json',dict(status='pass',all32rows_reconstructed=True,dispatch_and_scores_recomputed=True,primary_untouched_at100=True,weight_digests_unchanged=True,sampled_resource_guard=True));print('32 rows verified; primary unchanged at100')
def analyze():
 raw=[json.loads(x) for x in (R/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==32;groups={}
 for context in CONTEXTS:
  for relation in RELATIONS:
   rows=[x for x in raw if x['context']==context and x['relation']==relation];groups[context+'__'+relation]=dict(n=len(rows),valid_requests=sum(x['evaluation']['valid_calculator_request'] for x in rows),target_success=sum(x['evaluation']['strict_success'] for x in rows),demo_bound=sum(x['evaluation']['demonstration_expression_bound'] for x in rows),wrong_demo_execution=sum(x['evaluation']['wrong_demo_execution'] for x in rows),host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in rows)),caps=sum(x['stop']=='token_limit' for x in rows))
 pairs=[]
 for context in CONTEXTS:
  for ti in range(4):
   for seed in SEEDS:
    pair={x['relation']:x for x in raw if x['context']==context and x['target_index']==ti and x['seed']==seed};pairs.append(dict(context=context,target=TARGETS[ti][0],seed=seed,matching=pair['matching']['evaluation']['strict_success'],different=pair['different']['evaluation']['strict_success'],wrong_demo=pair['different']['evaluation']['wrong_demo_execution']))
 summary=dict(calls=32,groups=groups,paired_both_correct=sum(x['matching'] and x['different'] for x in pairs),pairs_n=16,output_tokens=sum(len(x['generated_token_ids']) for x in raw),max_input_tokens=max(len(x['input_token_ids']) for x in raw),caps=sum(x['stop']=='token_limit' for x in raw),generation_seconds=sum(x['seconds'] for x in raw))
 dump_new(R/'SUMMARY.json',summary);dump_new(R/'PAIRS.json',pairs)
 dump_new(R/'EVENT_INDEX.json',[{**{k:x[k] for k in ('run_id','context','target','demo','relation','seed','evaluation','stop')},'host_kind':x['host_result']['kind'],'input_tokens':len(x['input_token_ids']),'output_tokens':len(x['generated_token_ids'])} for x in raw])
 sample=[dict(run_id=x['run_id'],text=x['text'][:450],excerpted=len(x['text'])>450,host_result=x['host_result'],evaluation=x['evaluation']) for x in raw if x['seed']==SEEDS[0]];dump_new(R/'REVIEW_SAMPLE.json',dict(policy='First seed per context/target/relation, specified before outputs; all metrics include both seeds',rows=sample));print(json.dumps(summary,indent=2))
if __name__=='__main__':{'prepare':prepare,'run':run,'verify':verify,'analyze':analyze}[sys.argv[1]]()
