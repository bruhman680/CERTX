from pathlib import Path
import os,sys,json
R=Path(__file__).resolve().parent;D=R.parent;sys.path.insert(0,str(D))
import run_diagnostic as first
from world import view
from generate_capacity import generate
from runtime_reference import Guard,parameter_digest
from lora_cpu import inject_lora,load_adapter
from transformers import AutoTokenizer,AutoModelForCausalLM
import torch

def main():
 first.unchanged();first.runner.freeze_check();plan=json.loads((R/'PLAN.json').read_text());events=json.loads((D/'SNAPSHOT_EVENTS.json').read_text());assert len(events)==400
 first.put(R/'FREEZE.json',dict(files={str(p):first.sha(p) for p in (R/'run.py',R/'PLAN.json',D/'SNAPSHOT_EVENTS.json')}))
 os.environ['HF_HUB_OFFLINE']='1';os.environ['HF_HUB_DISABLE_PROGRESS_BARS']='1';torch.set_num_threads(2);m=json.loads((first.runner.parent.ACQ/'MANIFEST.json').read_text());guard=Guard(5153960755,R/'RESOURCE.jsonl');guard.read('before_model_load');tok=AutoTokenizer.from_pretrained(first.runner.parent.BASE,local_files_only=True,trust_remote_code=False)
 model=AutoModelForCausalLM.from_pretrained(first.runner.parent.BASE,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');inject_lora(model,rank=4,alpha=8,dropout=0.);load_adapter(model,first.runner.parent.ACQ/'final',base_pin=m['base_pin']);model.eval();assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];assert first.sha(first.runner.parent.BASE/'model.safetensors')==m['base_pin']['weights_sha256']
 prompt=view(0)+'\n\n'+plan['request']+'\nYour next move:';rows=[]
 for seed in plan['seeds']:
  runid=f'short_context_use_A_{seed}';ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True);first.put(R/f'PLAN_{seed}.json',dict(prompt=prompt,input_token_ids=ids,rng_seed=seed))
  row=generate(model,tok,prompt,guard,runid,seed);assert row['input_token_ids']==ids and tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];h=first.runner.world_dispatch(row['text'],events.copy());isworld=h['kind']=='play_patch_receipt';row.update(host_result=h,virtual_world_before=0,virtual_world_after=h['after']['number'] if isworld else 0,not_primary_history=True,exact_requested_command=row['text'].strip().upper()=='TOUCH A',accepted_world_action=isworld and bool(h['executed']));first.put(R/f'TRIAL_{seed}.json',row);rows.append(row);print(json.dumps(dict(seed=seed,text=row['text'],host=h,after=row['virtual_world_after'])),flush=True)
 assert parameter_digest(model,True)==m['final_digest'] and parameter_digest(model,False)==m['base_digest_after'];first.runner.freeze_check();count=first.unchanged()
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert first.sha(Path(p))==h
 first.put(R/'CHECKS.json',dict(status='pass',calls=2,accepted_world_actions=sum(r['accepted_world_action'] for r in rows),requested_command_matches=sum(r['exact_requested_command'] for r in rows),primary_bytes_unchanged=True,primary_files_checked=count,primary_cursor=400,weights_unchanged=True,training_updates=0,adaptive=True))
if __name__=='__main__':main()
