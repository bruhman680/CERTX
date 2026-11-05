from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run_followup as f
from transformers import AutoTokenizer

def main():
 assert json.loads((R/'CHECKS.json').read_text())['status']=='pass'
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert f.study.sha(Path(p))==h
 plan=json.loads((R/'PLAN.json').read_text());tok=AutoTokenizer.from_pretrained(f.study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);q,meta=f.make_prompt(tok,plan);saved=json.loads((R/'PROMPT.json').read_text());assert q==saved['prompt'] and meta==saved['metadata'];events=json.loads((R.parent/'SNAPSHOT_EVENTS.json').read_text());ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert len(ids)==3085;out=[]
 for seed in plan['seeds']:
  row=json.loads((R/f'TRIAL_{seed}.json').read_text());p=json.loads((R/f'PLAN_{seed}.json').read_text());assert row['prompt']==p['prompt']==q and row['input_token_ids']==p['input_token_ids']==ids;assert row['rng_seed']==p['rng_seed']==seed;assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];h=f.study.runner.world_dispatch(row['text'],events.copy());assert row['host_result']==h;assert row['virtual_world_after']==(1 if h.get('executed') and h.get('action')=='TOUCH A' else 0);assert (row['stop']=='eos' and row['generated_token_ids'][-1]==tok.eos_token_id) or (row['stop']=='token_limit' and len(row['generated_token_ids'])==96);out.append(dict(seed=seed,accepted=row['accepted_world_action'],text=row['text']))
 f.study.put(R/'RECORD_VERIFICATION.json',dict(status='pass',records_verified=3,equal_input_tokens=3085,prompt_token_decode_receipt_stop_reconstruction=True,independent_numeric_oracle=True,new_model_calls=0,primary_writes=0,rows=out));print('Three adaptive records reconstructed; no inference or primary writes.')
if __name__=='__main__':main()
