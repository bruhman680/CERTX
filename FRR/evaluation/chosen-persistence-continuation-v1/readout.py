"""External continuation summary and retained-history checks; no model call."""
from pathlib import Path
import json,hashlib,importlib.util
H=Path(__file__).resolve().parent;P=H.parent/'chosen-persistence-prototype-v1';D=P/'candidate'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    plan=read(H/'PLAN.json');state=read(D/'STATE.json')
    assert plan['start_turn']==3 and state['turn']==plan['target_turn']==13 and state['paused'] and state['stop_reason'] is None
    assert all(sha(D/path)==v for path,v in plan['prior_records_sha256'].items())
    assert sha(D/'CONTRACT.json')==plan['candidate_contract_sha256']
    assert not any((D/p).exists() for p in ('PENDING.json','CREATE_PENDING.json','RUN.lock'))
    assert not any((D/'world/engine'/p).exists() for p in ('PENDING.json','BATCH_PENDING.json','LOCK.json'))
    rows=[]
    for n in range(4,14):
        r=read(D/f'records/{n:06d}.json');raw=read(D/f'raw/{n:06d}.json');snap=read(D/f'snapshots/{n:06d}.json')
        rows.append({'turn':n,'input_tokens':r['input_tokens'],'output_tokens':r['output_tokens'],'stop':raw['stop'],
            'literal_last_user_message_copy':raw['text']==raw['messages'][-1]['content'],'actual_cell_operations':r['complete_cells'],
            'world_step':r['world_step'],'supported_world_entries':len(snap['entries']),'world_id':snap['id']})
    s=importlib.util.spec_from_file_location('chosen_session_readout',P/'session.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    audit=m.audit(D);assert audit['status']=='pass'
    tok=m.c.tokenizer();next_ids=tok.apply_chat_template(m.messages(D),tokenize=True,add_generation_prompt=True)
    assert len(next_ids)==read(D/'records/000013.json')['next_input_tokens']
    runs=[read(p) for p in (D/'runs').glob('*_RESULT.json')]
    matching=[r for r in runs if r['model_calls_this_invocation']==10 and r['candidate_turn']==13]
    assert len(matching)==1 and matching[0]['weights_unchanged']
    out={'status':'pass','start_turn':3,'end_turn':13,'actual_model_calls_this_window':10,'actual_model_calls_candidate_total':13,
         'prior_records_unchanged':True,'contract_unchanged':True,'actual_model_cell_operations_this_window':sum(r['actual_cell_operations'] for r in rows),
         'literal_last_user_message_copies':sum(r['literal_last_user_message_copy'] for r in rows),'automatic_world_note_appends':0,
         'end_world_step':state['world_step'],'end_world_entries':len(read(D/'snapshots/000013.json')['entries']),
         'exact_next_input_tokens':len(next_ids),'input_token_limit':7936,'weights_unchanged':True,'main_entry':1630,'main_unchanged':True,
         'pending':False,'rows':rows,'interpretation':'ten dependent replies in the same world, not independent replications; no action-error/reuse opportunity elicited; no learning/improvement claim'}
    with (H/'RESULTS.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
