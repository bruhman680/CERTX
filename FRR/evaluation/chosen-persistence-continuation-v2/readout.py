"""Read-only window verification and compact external trajectory summary."""
from pathlib import Path
import json,hashlib,importlib.util
H=Path(__file__).resolve().parent;P=H.parent/'chosen-persistence-prototype-v1';D=P/'candidate'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if __name__=='__main__':
    plan=read(H/'PLAN.json');state=read(D/'STATE.json');start=plan['start_turn'];end=state['turn']
    assert start==13 and start<end<=plan['target_turn']==38 and state['paused']
    assert all(sha(D/path)==v for path,v in plan['prior_records_sha256'].items())
    assert sha(D/'CONTRACT.json')==plan['candidate_contract_sha256']
    assert not any((D/p).exists() for p in ('PENDING.json','CREATE_PENDING.json','RUN.lock'))
    assert not any((D/'world/engine'/p).exists() for p in ('PENDING.json','BATCH_PENDING.json','LOCK.json'))
    rows=[]
    for n in range(start+1,end+1):
        r=read(D/f'records/{n:06d}.json');raw=read(D/f'raw/{n:06d}.json');snap=read(D/f'snapshots/{n:06d}.json')
        rows.append({'turn':n,'input_tokens':r['input_tokens'],'output_tokens':r['output_tokens'],'stop':raw['stop'],
            'literal_last_user_message_copy':raw['text']==raw['messages'][-1]['content'],'actual_cell_operations':r['complete_cells'],
            'world_step':r['world_step'],'supported_world_entries':len(snap['entries']),'world_id':snap['id']})
    s=importlib.util.spec_from_file_location('chosen_window2_readout',P/'session.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    audit=m.audit(D);assert audit['status']=='pass'
    next_tokens=None
    if read(D/f'records/{end:06d}.json')['feedback_for_next_input'] is not None:
        tok=m.c.tokenizer();next_tokens=len(tok.apply_chat_template(m.messages(D),tokenize=True,add_generation_prompt=True))
        assert next_tokens==read(D/f'records/{end:06d}.json')['next_input_tokens']
    runs=[read(p) for p in (D/'runs').glob('*_RESULT.json')]
    match=[r for r in runs if r['candidate_turn']==end and r['model_calls_this_invocation']==end-start]
    assert len(match)==1 and match[0]['weights_unchanged']
    out={'status':'pass','start_turn':start,'end_turn':end,'requested_replies':plan['requested_replies'],
         'actual_model_calls_this_window':end-start,'actual_model_calls_candidate_total':end,'prior_records_unchanged':True,'contract_unchanged':True,
         'actual_model_cell_operations_this_window':sum(r['actual_cell_operations'] for r in rows),
         'literal_last_user_message_copies':sum(r['literal_last_user_message_copy'] for r in rows),'automatic_world_note_appends':0,
         'end_world_step':state['world_step'],'end_world_entries':len(read(D/f'snapshots/{end:06d}.json')['entries']),
         'exact_next_input_tokens':next_tokens,'input_token_limit':7936,'weights_unchanged':True,'main_entry':1630,'main_unchanged':True,
         'stop_reason':state['stop_reason'],'pending':False,'rows':rows,
         'interpretation':'same dependent trajectory under unchanged laws; no independence, permanent-plateau or learning claim from a quiet window'}
    with (H/'RESULTS.json').open('x') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
