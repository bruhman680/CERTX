"""Reconstruct ten saved diagnostic prompts/receipts without another model call or primary write."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run_diagnostic as source
from world import view
from transformers import AutoTokenizer

def main():
 for freeze in (R/'FREEZE.json',R/'followup_A/FREEZE.json'):
  for p,h in json.loads(freeze.read_text())['files'].items():assert source.sha(Path(p))==h
 source.runner.freeze_check();events=json.loads((R/'SNAPSHOT_EVENTS.json').read_text());assert len(events)==400 and source.runner.patch_binding().replay(events)==0
 base=source.runner.world_view_render(events);suffix='\nYour next move:';look='DIAGNOSTIC REQUEST: For this reply, output exactly LOOK on its own line. Do not add commentary.';a='DIAGNOSTIC REQUEST: Use object A once now. Reply only with the valid control command, without commentary.'
 prompts=dict(full_context_unprompted=base,full_context_exact_LOOK=base.removesuffix(suffix)+'\n\n'+look+suffix,full_context_use_A=base.removesuffix(suffix)+'\n\n'+a+suffix,short_context_exact_LOOK=view(0)+'\n\n'+look+suffix,short_context_use_A=view(0)+'\n\n'+a+suffix)
 tok=AutoTokenizer.from_pretrained(source.runner.parent.BASE,local_files_only=True,trust_remote_code=False);verified=[]
 for seed in (120455,120456):
  for arm,prompt in prompts.items():
   f=(R/'followup_A'/f'TRIAL_{seed}.json') if arm=='short_context_use_A' else (R/'trials'/f'{arm}_{seed}.json');p=(R/'followup_A'/f'PLAN_{seed}.json') if arm=='short_context_use_A' else (R/'plans'/f'{arm}_{seed}.json');row=json.loads(f.read_text());plan=json.loads(p.read_text());ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
   assert row['prompt']==plan['prompt']==prompt and row['input_token_ids']==plan['input_token_ids']==ids;assert row['rng_seed']==plan['rng_seed']==seed;assert tok.decode(row['generated_token_ids'],skip_special_tokens=True)==row['text'];assert row['host_result']==source.runner.world_dispatch(row['text'],events.copy())
   assert len(row['generated_token_ids'])<=96 and len(ids)<=8096;assert (row['stop']=='eos' and row['generated_token_ids'][-1]==tok.eos_token_id) or (row['stop']=='token_limit' and len(row['generated_token_ids'])==96)
   h=row['host_result'];expected=1 if h.get('action')=='TOUCH A' and h.get('executed') else 0;assert row['virtual_world_after']==expected
   verified.append(dict(arm=arm,seed=seed,accepted=row['accepted_world_action'],after=row['virtual_world_after']))
 result=dict(status='pass',saved_generations_verified=len(verified),snapshot_entries=400,prompt_token_decode_receipt_stop_reconstruction=True,independent_single_step_numeric_oracle=True,new_model_calls=0,primary_writes=0,rows=verified)
 source.put(R/'RECORD_VERIFICATION.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
