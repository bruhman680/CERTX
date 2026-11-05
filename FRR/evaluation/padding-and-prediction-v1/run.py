"""Declared24padding trials +24prediction-before-host-execution trials; primary frozen500."""
from pathlib import Path
from collections import Counter
import hashlib,json,os,random,re,sys,traceback
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment';sys.path.insert(0,str(ROOT/'evaluation/world-control-diagnostic-v1'))
import run_diagnostic as util
from world import view,transition
put=util.put;sha=util.sha;runner=util.runner

def unchanged():
 before=json.loads((R/'PRIMARY_BEFORE.json').read_text());after={str(p.relative_to(ROOT)):sha(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts};assert before==after,'Primary bytes changed';assert json.loads((ENV/'STATE.json').read_text())['next_step']==500 and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists();return len(before)
def diverse_source(seed):
 rng=random.Random(seed);nouns=['ribbon','lantern','harbor','window','basket','curtain','pebble','bridge','cushion','vessel','meadow','canyon','cabin','shelf','path','canvas','valley','copper','marble','forest','island','shore','cloud','fabric','ceiling','tower','feather','mirror','railway','stone'];adjs=['quiet','distant','pale','soft','narrow','bright','wooden','silver','heavy','gentle','smooth','amber','blue','warm','rounded','shallow'];verbs=['rests beside','stands near','faces','lies beyond','borders','reflects','shadows','overlooks'];sentences=[];seen=set()
 while len(sentences)<900:
  s=f'The {rng.choice(adjs)} {rng.choice(nouns)} {rng.choice(verbs)} the {rng.choice(adjs)} {rng.choice(nouns)}.'
  if s not in seen:seen.add(s);sentences.append(s)
 text='\n'.join(sentences);assert not re.search(r'\d|\b(?:LOOK|TOUCH|READ|NOTE|HOST|RULE|COMMAND|NUMBER|A|B)\b',text,re.I);return text

def build_trials(tok,plan):
 def ids(q):return tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True)
 pad=plan['padding'];tail='\n\n'+view(0)+'\n\n'+pad['request']+'\nYour next move:';prefix=pad['filler_label']+'\n';post='\n'+pad['end_label']+tail;source=diverse_source(pad['diverse_generation_seed']);put(R/'DIVERSE_FILLER_SOURCE.json',dict(text=source,seed=pad['diverse_generation_seed'],scope='Synthetic deterministic sentences, not facts supplied as evidence'))
 pools={'repeated':tok.encode(' plain'*6000,add_special_tokens=False),'diverse':tok.encode(source,add_special_tokens=False)}
 def make(body):return prefix+body+post
 arms={'short_reference':view(0)+'\n\n'+pad['request']+'\nYour next move:','empty_wrapper':make('')};meta={a:dict(input_tokens=len(ids(q)),padding_tokens=0) for a,q in arms.items()}
 for length in (721,1600,3085):
  for kind in ('repeated','diverse'):
   guess=length-len(ids(make('')));found=None
   for n in range(max(0,guess-64),guess+65):
    body=tok.decode(pools[kind][:n],skip_special_tokens=True);q=make(body)
    if len(ids(q))==length:found=(q,body,n);break
   assert found is not None,(kind,length)
   q,body,n=found;key=f'{kind}_{length}';arms[key]=q;bodyids=tok.encode(body,add_special_tokens=False);meta[key]=dict(input_tokens=length,padding_tokens=len(bodyids),source_prefix_tokens=n,distinct_padding_token_ids=len(set(bodyids)),distinct_padding_words=len(set(body.lower().split())),body_sha256=hashlib.sha256(body.encode()).hexdigest())
 assert list(arms)==pad['arms'];trials=[]
 for j,seed in enumerate(pad['seeds']):
  order=pad['arms'][j:]+pad['arms'][:j]
  for arm in order:
   q=arms[arm];trials.append(dict(id=f'padding_{arm}_{seed}',stage='padding',arm=arm,rng_seed=seed,prompt=q,input_token_ids=ids(q),initial_number=0,requested_command='TOUCH A'))
 pred=plan['prediction']
 for j,seed in enumerate(pred['seeds']):
  conditions=pred['conditions'] if j%2==0 else list(reversed(pred['conditions']))
  for condition in conditions:
   cases=pred['cases'][j:]+pred['cases'][:j]
   for case in cases:
    q=view(case['number'])+'\n\n'+(pred['rule_card']+'\n\n' if condition=='supplied_rule' else '')+pred['request'].format(action=case['action'])+'\nYour prediction:'
    trials.append(dict(id=f"prediction_{case['id']}_{condition}_{seed}",stage='prediction',case=case['id'],condition=condition,rng_seed=seed,prompt=q,input_token_ids=ids(q),initial_number=case['number'],declared_action=case['action']))
 assert len(trials)==48 and all(len(t['input_token_ids'])<=8096 for t in trials);return trials,meta

def main():
 runner.freeze_check();unchanged();lock=R/'PROBE.lock';fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY);os.write(fd,str(os.getpid()).encode());os.close(fd)
 try:
  os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1'
  import torch
  from transformers import AutoTokenizer,AutoModelForCausalLM
  from lora_cpu import inject_lora,load_adapter
  from runtime_reference import Guard,parameter_digest
  from generate_capacity import generate
  torch.set_num_threads(2);plan=json.loads((R/'PLAN.json').read_text());tok=AutoTokenizer.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False);trials,meta=build_trials(tok,plan);put(R/'ALL_TRIAL_PLANS.json',trials);put(R/'PADDING_METADATA.json',meta);_,events,_=runner.Journal(ENV).state();assert len(events)==500;put(R/'SNAPSHOT_EVENTS.json',events)
  put(R/'FREEZE.json',dict(files={str(p):sha(p) for p in (R/'run.py',R/'PLAN.json',R/'ALL_TRIAL_PLANS.json',R/'PADDING_METADATA.json',R/'DIVERSE_FILLER_SOURCE.json',R/'SNAPSHOT_EVENTS.json',G/'world_routine.py',ENV/'ENVIRONMENT_DISCOVERY_PATCH_V1.json')},scope='All48trial prompts and IDs frozen before any model call'))
  for name in ('starts','padding','prediction','host_transitions'):(R/name).mkdir()
  m=json.loads((runner.parent.ACQ/'MANIFEST.json').read_text());assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];padrows=[];predrows=[]
  for index,t in enumerate(trials):
   key=t['id'];put(R/'starts'/f'{key}.json',dict(trial_id=key,index=index,stage=t['stage'],plan_sha256=sha(R/'ALL_TRIAL_PLANS.json'),rng_seed=t['rng_seed']));row=generate(model,tok,t['prompt'],guard,key,t['rng_seed']);assert row['input_token_ids']==t['input_token_ids'] and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text']
   if t['stage']=='padding':
    h=runner.world_dispatch(row['text'],events.copy());world=h['kind']=='play_patch_receipt';accepted=world and bool(h['executed']);after=h['after']['number'] if world else 0;assert after==(1 if accepted and h['action']=='TOUCH A' else 0);row.update(stage='padding',arm=t['arm'],host_result=h,virtual_world_before=0,virtual_world_after=after,accepted_world_action=accepted,exact_requested_command=row['text'].strip().upper()=='TOUCH A',not_primary_history=True);put(R/'padding'/f'{key}.json',row);padrows.append(row);print(json.dumps(dict(trial_id=key,text=row['text'],exact=row['exact_requested_command'],after=after)),flush=True)
   else:
    row.update(stage='prediction',case=t['case'],condition=t['condition'],initial_number=t['initial_number'],declared_action=t['declared_action'],not_primary_history=True,model_action_generated=False);path=R/'prediction'/f'{key}.json';put(path,row)
    # Only now, after prediction is durable, execute the predeclared host action. Model text is never dispatched here.
    n=t['initial_number'];action=t['declared_action'];after,h=transition(n,action);oracle=min(n+1,8) if action=='TOUCH A' else -n;assert after==oracle;text=row['text'].strip();formatted=re.fullmatch(r'[+-]?\d+',text) is not None;value=int(text) if formatted else None
    result=dict(trial_id=key,prediction_sha256=sha(path),prediction_saved_before_execution=True,host_action_predeclared=True,model_text_dispatched=False,initial_number=n,action=action,after=after,receipt=h,independent_numeric_oracle=oracle,integer_format=formatted,predicted_value=value,correct=formatted and value==after,case=t['case'],condition=t['condition'],rng_seed=t['rng_seed']);put(R/'host_transitions'/f'{key}.json',result);predrows.append(result);print(json.dumps(dict(trial_id=key,text=row['text'],format=formatted,prediction=value,actual=after,correct=result['correct'])),flush=True)
  assert len(padrows)==24 and len(predrows)==24;assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert sha(runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];runner.freeze_check();count=unchanged()
  for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h
  resource=[json.loads(l) for l in (R/'RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resource)
  checks=dict(status='pass',calls=48,padding_calls=24,prediction_calls=24,primary_cursor=500,primary_files_unchanged=count,primary_bytes_unchanged=True,primary_paused=True,weights_unchanged=True,training_updates=0,paid_inference_api_calls=0,diagnostic_imported=False,padding={arm:dict(calls=3,exact_requested_commands=sum(x['exact_requested_command'] for x in padrows if x['arm']==arm),accepted_world_actions=sum(x['accepted_world_action'] for x in padrows if x['arm']==arm),input_tokens=meta[arm]['input_tokens']) for arm in plan['padding']['arms']},prediction={condition:dict(calls=12,integer_formatted=sum(x['integer_format'] for x in predrows if x['condition']==condition),correct=sum(x['correct'] for x in predrows if x['condition']==condition),cases={case['id']:dict(calls=2,correct=sum(x['correct'] for x in predrows if x['condition']==condition and x['case']==case['id'])) for case in plan['prediction']['cases']}) for condition in plan['prediction']['conditions']},prediction_before_host_execution=True,model_prediction_text_never_dispatched=True,max_working_bytes=max(x['working_estimate'] for x in resource),working_limit=resource[0]['working_limit'],scope='Two small diagnostic studies on copies, no primary continuation; no discovery/transfer/general capability claim');put(R/'CHECKS.json',checks);print(json.dumps(checks),flush=True)
 except BaseException as e:put(R/'ERROR.json',dict(error=repr(e),traceback=traceback.format_exc(),no_silent_retry=True));raise
 finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
