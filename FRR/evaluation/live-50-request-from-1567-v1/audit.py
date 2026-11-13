"""Dynamic read-only audit of actual bounded continuation from 1567."""
from pathlib import Path
import json,hashlib,sys
from transformers import AutoTokenizer

H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1';R=C/'run'
sys.path[:0]=[str(C),str(C/'world'),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import parse_notebook,verify_store

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory():return {str(p.relative_to(C)):sha(p) for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def main():
    start=read(H/'BEFORE_STATE.json');state=read(R/'STATE.json');plan=read(H/'PLAN.json')
    assert state['paused'] and state['turn']>=start['turn']
    actual=state['turn']-start['turn'];assert actual<=plan['requested_replies']
    sessions=[p for p in (R/'sessions').glob('*_RESULT.json') if 'run/'+str(p.relative_to(R)) not in read(H/'BEFORE_INVENTORY.json')]
    assert len(sessions)==1,sessions
    session=read(sessions[0]);assert session['start_turn']==start['turn'] and session['end_turn']==state['turn']
    assert session['model_calls']==actual
    assert session['reason'] in ('context_capacity','completed','user_pause')
    assert not any((R/x).exists() for x in ['PENDING.json','RUN.lock'])
    assert not any((R/'world'/x).exists() for x in ['PENDING.json','BATCH_PENDING.json','LOCK.json'])
    before=read(H/'BEFORE_INVENTORY.json');after=inventory()
    allowed={'run/STATE.json','run/world/STATE.json'}
    deleted=[k for k in before if k not in after]
    changed=[k for k,v in before.items() if after.get(k)!=v and k not in allowed]
    assert not deleted and not changed,(deleted,changed)
    checks={'prior_immutable_prefix_preserved':True,'changed_preexisting_files_only_expected_states':True,
      'pointer_unchanged':read(E.parent/'ACTIVE_GARDEN_PHASE.json')==plan['pointer'],
      'contract_unchanged':sha(C/'CONTRACT.json')==plan['pointer']['contract_sha256'],
      'start_actual_entry_1567':start['human_entry']==1567 and start['turn']==17,
      'actual_count_not_assumed_50':actual==state['human_entry']-start['human_entry'] and actual<=50,
      'paused_without_pending_or_locks':True}
    tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
    assert read(R/'CONTROL_TASKS.json')=={}
    messages=read(R/'INITIAL_MESSAGES.json')
    for n in range(1,start['turn']+1):
      old=read(R/f'events/{n:06d}.json')
      messages += [{'role':'assistant','content':old['text']},{'role':'user','content':old['feedback']}]
    last=sha(R/f"events/{start['turn']:06d}.json");world_id=read(R/f"events/{start['turn']:06d}.json")['after_id'];world_step=start['world_step']
    rows=[]
    for turn in range(start['turn']+1,state['turn']+1):
      raw=read(R/f'raw/{turn:06d}.json');p=read(R/f'plans/{turn:06d}.json')
      event=read(R/f'events/{turn:06d}.json');batch=read(R/f'batches/{turn:06d}.json')
      ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
      flags={'entry_and_turn':event['turn']==turn and event['human_entry']==1550+turn,
       'actual_history_exact':p['messages']==raw['messages']==messages,
       'actual_input_ids_exact':p['input_token_ids']==raw['input_token_ids']==ids,
       'input_within_capacity':len(ids)<=7936,
       'decoded_raw_equals_event':tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==event['text'],
       'unchanged_greedy_decoder':raw['decoder']=='greedy_argmax' and raw['temperature'] is None and raw['top_p'] is None,
       'raw_hash_matches_event':sha(R/f'raw/{turn:06d}.json')==event['raw_sha256'],
       'event_parent_hash_exact':event['parent_event_sha256']==last,
       'plan_and_event_before_world_exact':p['before_id']==event['before_id']==world_id,
       'batch_is_actual_output':batch['raw_text']==raw['text'],
       'batch_parsed_exact':batch['parsed']==parse_notebook(raw['text']),
       'feedback_actual_projection':event['feedback']==candidate.project_feedback(batch),
       'batch_matches_world_batch':batch==read(R/'world/batches'/(batch['batch_id']+'.json')),
       'count_boundary_matches':event['cell_count']==batch['parsed']['complete_executable_cells'] and event['boundary']==batch['boundary']}
      stop=raw['stop'];tokens=raw['generated_token_ids']
      flags['stop_consistent']=stop==event['stop'] and ((stop=='eos' and tokens[-1]==tok.eos_token_id) or (stop=='token_limit' and len(tokens)==256))
      for op in batch['operations']:
       assert op['step']==world_step+1
       assert op['before_id']==world_id
       plain={k:v for k,v in op.items() if k not in ('cell_index','source_start','source_end')}
       assert plain==read(R/f"world/events/{op['step']:06d}.json")
       world_step=op['step'];world_id=read(R/f"world/bundles/{world_step:06d}.json")['id']
       assert world_id==op['after_id']
      flags['event_after_exact_world']=world_id==event['after_id']
      assert all(flags.values()),(turn,flags)
      rows.append({'human_entry':1550+turn,'turn':turn,'checks':flags,'stop':stop,
        'input_tokens':len(ids),'output_tokens':len(tokens),'complete_executable_cells':event['cell_count'],
        'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),
        'world_step':world_step,'changed_paths':[path for op in batch['operations'] for path in op['changed_paths']]})
      messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':event['feedback']}]
      last=sha(R/f'events/{turn:06d}.json')
    checks['final_state_hash_step']=state['last_event_sha256']==last and state['world_step']==world_step
    checks['world_final_state_step']=read(R/'world/STATE.json')['step']==world_step
    next_ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    checks['next_input_matches_session_verifier']=len(next_ids)==session['verification']['next_input_tokens']
    if session['reason']=='context_capacity':
      checks['next_input_over_limit']=len(next_ids)>plan['input_limit']
      checks['last_generated_input_within_limit']=bool(rows) and len(read(R/f"raw/{state['turn']:06d}.json")['input_token_ids'])<=plan['input_limit']
      checks['overlimit_generation_not_attempted']=not (R/f"plans/{state['turn']+1:06d}.json").exists() and not (R/f"raw/{state['turn']+1:06d}.json").exists()
    elif session['reason']=='completed':
      checks['completed_exact_requested_count']=actual==plan['requested_replies']
    checks['initial_input_matches_start_plan']=len(tok.apply_chat_template(read(R/f"plans/{start['turn']+1:06d}.json")['messages'],tokenize=True,add_generation_prompt=True))==plan['next_input_at_start'] if actual else True
    assert all(checks.values()),checks
    verification=verify_store(R/'world')
    new=[k for k in after if k not in before]
    groups={}
    for row in rows:
      groups.setdefault(row['text_sha256'],[]).append(row['human_entry'])
    result={'status':'pass','scope':f"Actual canonical entries {start['human_entry']+1}-{state['human_entry']}, not detached diagnostic loops",
      'requested_replies':plan['requested_replies'],'actual_replies':actual,'reason':session['reason'],
      'final_entry':state['human_entry'],'next_input_tokens':len(next_ids),
      'last_generated_input_tokens':len(read(R/f"raw/{state['turn']:06d}.json")['input_token_ids']) if actual else None,
      'checks':checks,'rows':rows,'distinct_text_groups':groups,'world_verification':verification,
      'new_files':new,'allowed_preexisting_state_updates':[k for k in allowed if before.get(k)!=after.get(k)],
      'before_file_count':len(before),'after_file_count':len(after),
      'model_calls':0,'world_replay_operations':0,'weights_loaded':False,
      'canonical_writes':False,'limitation':'Artifact/tokenizer audit and read-only store verifier; not a new model generation or proof of behavioral competence.'}
    assert inventory()==after,'Read-only audit unexpectedly changed candidate files'
    (H/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','new_files')},indent=2))

if __name__=='__main__':main()
