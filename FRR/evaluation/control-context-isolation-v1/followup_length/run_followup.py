from pathlib import Path
import json,os,sys
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(P));import run as study
from world import view
from transformers import AutoTokenizer,AutoModelForCausalLM
from runtime_reference import Guard,parameter_digest
from lora_cpu import inject_lora,load_adapter
from generate_capacity import generate
import torch

def make_prompt(tok,plan):
 request=json.loads((P/'PLAN.json').read_text())['request'];meta=json.loads((P/'PROMPT_METADATA.json').read_text());target=meta['input_token_counts']['normal_H1_S1'];label=meta['filler_label'];suffix='\n\n'+view(0)+'\n\n'+request+'\nYour next move:'
 def ids(q):return tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True)
 guess=target-len(ids(label+suffix))
 for n in range(max(0,guess-32),guess+33):
  q=label+' plain'*n+suffix
  if len(ids(q))==target:return q,dict(input_tokens=target,filler_repetitions=n,world_and_request_tail=suffix)
 raise ValueError('Could not match tokens; no model calls started')
def main():
 study.unchanged();study.runner.freeze_check();assert json.loads((P/'CHECKS.json').read_text())['status']=='pass';plan=json.loads((R/'PLAN.json').read_text());events=json.loads((P/'SNAPSHOT_EVENTS.json').read_text());os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1';torch.set_num_threads(2);tok=AutoTokenizer.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);q,meta=make_prompt(tok,plan);study.put(R/'PROMPT.json',dict(prompt=q,metadata=meta));study.put(R/'FREEZE.json',dict(files={str(p):study.sha(p) for p in (R/'run_followup.py',R/'PLAN.json',R/'PROMPT.json',P/'SNAPSHOT_EVENTS.json')}))
 m=json.loads((study.runner.parent.ACQ/'MANIFEST.json').read_text());assert study.sha(study.runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256'];guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');model=AutoModelForCausalLM.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,study.runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];rows=[]
 for seed in plan['seeds']:
  ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);study.put(R/f'PLAN_{seed}.json',dict(prompt=q,input_token_ids=ids,rng_seed=seed));row=generate(model,tok,q,guard,f'world_only_padded_{seed}',seed);assert row['input_token_ids']==ids and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];h=study.runner.world_dispatch(row['text'],events.copy());accepted=h['kind']=='play_patch_receipt' and bool(h['executed']);after=h['after']['number'] if h['kind']=='play_patch_receipt' else 0;assert after==(1 if accepted and h['action']=='TOUCH A' else 0);row.update(host_result=h,virtual_world_before=0,virtual_world_after=after,accepted_world_action=accepted,exact_requested_command=row['text'].strip().upper()=='TOUCH A',not_primary_history=True);study.put(R/f'TRIAL_{seed}.json',row);rows.append(row);print(json.dumps(dict(seed=seed,text=row['text'],accepted=accepted,after=after)),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];study.runner.freeze_check();count=study.unchanged()
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert study.sha(Path(p))==h
 resources=[json.loads(l) for l in (R/'RESOURCE.jsonl').read_text().splitlines()];assert all(r['working_estimate']<r['working_limit'] for r in resources)
 study.put(R/'CHECKS.json',dict(status='pass',calls=3,adaptive=True,input_tokens=meta['input_tokens'],requested_command_matches=sum(r['exact_requested_command'] for r in rows),accepted_world_actions=sum(r['accepted_world_action'] for r in rows),after_values=[r['virtual_world_after'] for r in rows],weights_unchanged=True,training_updates=0,primary_cursor=450,primary_files_unchanged=count,primary_bytes_unchanged=True,diagnostic_results_imported=False))
if __name__=='__main__':main()
