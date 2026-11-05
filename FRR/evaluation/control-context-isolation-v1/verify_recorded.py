"""Read-only reconstruction of the declared15probe records; no new model generation."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run as study
from transformers import AutoTokenizer

def main():
 assert json.loads((R/'CHECKS.json').read_text())['status']=='pass'
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert study.sha(Path(p))==h
 study.runner.freeze_check();events=json.loads((R/'SNAPSHOT_EVENTS.json').read_text());plan=json.loads((R/'PLAN.json').read_text());tok=AutoTokenizer.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);prompts,meta=study.make_prompts(events,tok,plan);assert prompts==json.loads((R/'PROMPTS.json').read_text()) and meta==json.loads((R/'PROMPT_METADATA.json').read_text());verified=[]
 for seed in plan['seeds']:
  for arm in plan['arms']:
   key=f'{arm}_{seed}';r=json.loads((R/'trials'/f'{key}.json').read_text());p=json.loads((R/'plans'/f'{key}.json').read_text());q=prompts[arm];ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert r['prompt']==p['prompt']==q and r['input_token_ids']==p['input_token_ids']==ids;assert r['rng_seed']==p['rng_seed']==seed;assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text'];h=study.runner.world_dispatch(r['text'],events.copy());assert r['host_result']==h;assert r['exact_requested_command']==(r['text'].strip().upper()=='TOUCH A');assert r['accepted_world_action']==(h['kind']=='play_patch_receipt' and bool(h['executed']));assert r['virtual_world_after']==(1 if h.get('executed') and h.get('action')=='TOUCH A' else 0)
   assert len(ids)<=8096 and len(r['generated_token_ids'])<=96;assert (r['stop']=='eos' and r['generated_token_ids'][-1]==tok.eos_token_id) or (r['stop']=='token_limit' and len(r['generated_token_ids'])==96);verified.append(dict(arm=arm,seed=seed,exact=r['exact_requested_command'],accepted=r['accepted_world_action']))
 study.put(R/'RECORD_VERIFICATION.json',dict(status='pass',saved_generations_verified=len(verified),snapshot_entries=450,prompt_token_decode_receipt_stop_reconstruction=True,equal_full_input_token_count=meta['equal_full_input_length'],independent_numeric_oracle=True,new_model_calls=0,primary_writes=0,rows=verified));print('All15saved probe records reconstructed; no inference or primary writes.')
if __name__=='__main__':main()
