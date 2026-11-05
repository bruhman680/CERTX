"""Verify48saved plans, manipulations, outputs and host effects without new generation."""
from pathlib import Path
import json,re,sys
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run as study
from transformers import AutoTokenizer
from world import view,transition

def main():
 assert json.loads((R/'CHECKS.json').read_text())['status']=='pass'
 for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert study.sha(Path(p))==h
 study.runner.freeze_check();plan=json.loads((R/'PLAN.json').read_text());trials=json.loads((R/'ALL_TRIAL_PLANS.json').read_text());meta=json.loads((R/'PADDING_METADATA.json').read_text());source=json.loads((R/'DIVERSE_FILLER_SOURCE.json').read_text());assert source['text']==study.diverse_source(plan['padding']['diverse_generation_seed']);tok=AutoTokenizer.from_pretrained(study.runner.parent.BASE,local_files_only=True,trust_remote_code=False);events=json.loads((R/'SNAPSHOT_EVENTS.json').read_text());assert len(events)==500;results=[]
 pad=plan['padding'];tail='\n\n'+view(0)+'\n\n'+pad['request']+'\nYour next move:';prefix=pad['filler_label']+'\n';post='\n'+pad['end_label']+tail;pool={'repeated':tok.encode(' plain'*6000,add_special_tokens=False),'diverse':tok.encode(source['text'],add_special_tokens=False)}
 for t in trials:
  key=t['id'];q=t['prompt'];ids=tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert ids==t['input_token_ids'] and len(ids)<=8096
  r=json.loads((R/t['stage']/f'{key}.json').read_text());assert r['prompt']==q and r['input_token_ids']==ids and r['rng_seed']==t['rng_seed'];assert tok.decode(r['generated_token_ids'],skip_special_tokens=True)==r['text'];assert (r['stop']=='eos' and r['generated_token_ids'][-1]==tok.eos_token_id) or (r['stop']=='token_limit' and len(r['generated_token_ids'])==96)
  if t['stage']=='padding':
   arm=t['arm'];assert len(ids)==meta[arm]['input_tokens']
   if arm=='short_reference':assert q==view(0)+'\n\n'+pad['request']+'\nYour next move:'
   elif arm=='empty_wrapper':assert q==prefix+post
   else:
    kind,length=arm.rsplit('_',1);assert q.startswith(prefix) and q.endswith(post);body=q[len(prefix):-len(post)];m=meta[arm];assert body==tok.decode(pool[kind][:m['source_prefix_tokens']],skip_special_tokens=True);assert study.hashlib.sha256(body.encode()).hexdigest()==m['body_sha256'];assert len(ids)==int(length)
   h=study.runner.world_dispatch(r['text'],events.copy());assert r['host_result']==h;assert r['exact_requested_command']==(r['text'].strip().upper()=='TOUCH A');assert r['accepted_world_action']==(h['kind']=='play_patch_receipt' and bool(h['executed']));assert r['virtual_world_after']==(1 if h.get('executed') and h.get('action')=='TOUCH A' else 0)
  else:
   p=plan['prediction'];case=next(x for x in p['cases'] if x['id']==t['case']);expected=view(case['number'])+'\n\n'+(p['rule_card']+'\n\n' if t['condition']=='supplied_rule' else '')+p['request'].format(action=case['action'])+'\nYour prediction:';assert q==expected;h=json.loads((R/'host_transitions'/f'{key}.json').read_text());assert h['prediction_sha256']==study.sha(R/'prediction'/f'{key}.json') and h['prediction_saved_before_execution'] and h['host_action_predeclared'] and h['model_text_dispatched'] is False;after,receipt=transition(case['number'],case['action']);oracle=min(case['number']+1,8) if case['action']=='TOUCH A' else -case['number'];assert h['receipt']==receipt and h['after']==after==oracle==h['independent_numeric_oracle'];text=r['text'].strip();formatted=re.fullmatch(r'[+-]?\d+',text) is not None;value=int(text) if formatted else None;assert h['integer_format']==formatted and h['predicted_value']==value and h['correct']==(formatted and value==after)
  results.append(dict(trial_id=key,stage=t['stage'],verified=True))
 assert len(results)==48;study.put(R/'RECORD_VERIFICATION.json',dict(status='pass',saved_generations_verified=48,prompt_token_decode_stop_reconstruction=True,padding_types_and_exact_lengths_checked=True,host_receipts_and_numeric_oracle_checked=True,prediction_hash_linkage_checked=True,chronology_scope='Frozen code writes the prediction before host execution; hashes identify its bytes and are not independent timestamp proof',new_model_calls=0,primary_writes=0,rows=results));print('All48records verified without new model generation or primary writes.')
if __name__=='__main__':main()
