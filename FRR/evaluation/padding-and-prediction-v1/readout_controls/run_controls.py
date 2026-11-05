from pathlib import Path
import json,os,re,sys
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P));import run as study
from world import Rules,view
from transformers import AutoTokenizer,AutoModelForCausalLM
from lora_cpu import inject_lora,load_adapter
from runtime_reference import Guard,parameter_digest
from generate_capacity import generate
import torch

def make_cases():
 out=[dict(id='literal_three',prompt='Reply with exactly the integer 3 and no other text.',expected=3,kind='literal'),dict(id='addition_two_plus_one',prompt='What is 2 + 1? Reply with only the resulting integer, without commentary.',expected=3,kind='arithmetic'),dict(id='negate_negative_two',prompt='What is the negative of -2? Reply with only the resulting integer, without commentary.',expected=2,kind='arithmetic')]
 for upper in (8,4):
  rules=Rules(lower=-upper,upper=upper)
  for field in ('current','upper'):
   request='Read the Current number field. Reply with only that integer, without commentary.' if field=='current' else 'Read the upper bound of the range. Reply with only that integer, without commentary.'
   out.append(dict(id=f'{field}_bound{upper}',prompt=view(2,rules)+'\n\n'+request+'\nYour answer:',expected=2 if field=='current' else upper,kind='field_readout',rendered_number=2,rendered_upper=upper))
 return out

def main():
 assert json.loads((P/'CHECKS.json').read_text())['status']=='pass';study.unchanged();study.runner.freeze_check();plan=json.loads((R/'PLAN.json').read_text());cases=make_cases();assert [c['id'] for c in cases]==plan['cases'];study.put(R/'CASES.json',cases);study.put(R/'FREEZE.json',dict(files={str(p):study.sha(p) for p in (R/'run_controls.py',R/'PLAN.json',R/'CASES.json')}));os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1';torch.set_num_threads(2);tok=AutoTokenizer.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);m=json.loads((study.runner.parent.ACQ/'MANIFEST.json').read_text());assert study.sha(study.runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,study.runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];(R/'trials').mkdir();(R/'plans').mkdir();rows=[]
 for j,seed in enumerate(plan['seeds']):
  order=cases[j:]+cases[:j]
  for c in order:
   key=f"{c['id']}_{seed}";q=c['prompt'];ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);study.put(R/'plans'/f'{key}.json',dict(case=c,prompt=q,input_token_ids=ids,rng_seed=seed));row=generate(model,tok,q,guard,key,seed);assert row['input_token_ids']==ids and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];t=row['text'].strip();formatted=re.fullmatch(r'[+-]?\d+',t) is not None;value=int(t) if formatted else None;row.update(case=c['id'],kind=c['kind'],expected=c['expected'],integer_format=formatted,predicted_value=value,correct=formatted and value==c['expected'],not_primary_history=True,no_action_dispatched=True);study.put(R/'trials'/f'{key}.json',row);rows.append(row);print(json.dumps(dict(case=c['id'],seed=seed,text=row['text'],expected=c['expected'],correct=row['correct'])),flush=True)
 assert len(rows)==14;assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert study.sha(study.runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];study.runner.freeze_check();count=study.unchanged()
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert study.sha(Path(p))==h
 resources=[json.loads(l) for l in (R/'RESOURCE.jsonl').read_text().splitlines()];assert all(x['working_estimate']<x['working_limit'] for x in resources)
 checks=dict(status='pass',calls=14,adaptive=True,primary_cursor=500,primary_files_unchanged=count,primary_bytes_unchanged=True,weights_unchanged=True,training_updates=0,no_action_dispatched=True,cases={c['id']:dict(calls=2,integer_formatted=sum(r['integer_format'] for r in rows if r['case']==c['id']),correct=sum(r['correct'] for r in rows if r['case']==c['id']),outputs=[r['text'] for r in rows if r['case']==c['id']]) for c in cases});study.put(R/'CHECKS.json',checks);print(json.dumps(checks),flush=True)
if __name__=='__main__':main()
