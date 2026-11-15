"""Post-block main artifact readout; no inference or model action replay."""
from pathlib import Path
import sys,json,hashlib,statistics
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
import runner as r
def main():
    assert not (H/'BLOCK_AUDIT.json').exists(),'Preserve previous audit'
    store=H/'run';state=r.read(store/'STATE.json')
    assert state['paused'] and state['human_entry']==1630 and state['turn']==50
    assert not (store/'RUN.lock').exists() and not (store/'PENDING.json').exists()
    tok=r.tokenizer();verification=r.verify(store,tok)
    raws=[r.read(p) for p in sorted((store/'raw').glob('*.json'))]
    rows=r.events(store);assert len(rows)==len(raws)==50
    sessions=[r.read(p) for p in (store/'sessions').glob('*_RESULT.json')]
    assert len(sessions)==1 and sessions[0]['actual_model_replies']==50 and sessions[0]['reason']=='completed'
    checks=[r.read(p) for p in sorted((store/'sessions').glob('*_CHECK_*.json'))]
    assert [c['human_entry'] for c in checks]==[1590,1600,1610,1620,1630]
    assert all(c['status']=='pass' for c in checks)
    assert not list((store/'sessions').glob('*_ERROR.json'))
    active=r.read(H.parent.parent/'ACTIVE_GARDEN_PHASE.json');activation=r.read(H/'ACTIVATION.json')
    assert active==activation['new_pointer'] and active['contract_sha256']==r.digest(H/'CONTRACT.json')
    assert active['version']=='bounded-main-continuation-v1'
    source_rows=r.candidate.rows(r.C/'run')
    archive=r.read(store/'BASE_ARCHIVE.json')
    full_messages=list(archive['initial_messages'])
    for e in archive['exchanges']+[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in rows]:
        full_messages += [{'role':'assistant','content':e['assistant']},{'role':'user','content':e['receipt']}]
    final_world=r.read(store/'world/bundles'/r.read(store/'world/STATE.json')['bundle'])
    final_note=next(x for x in final_world['entries'] if x[0]=='notebook.txt')
    initial_note=next(x for x in r.read(store/'INITIAL_WORLD.json')['entries'] if x[0]=='notebook.txt')
    result={'status':'pass','start_entry':1580,'end_entry':1630,'actual_model_replies':50,'source_phase_preserved_files':len(r.inventory(r.C)),'main_version':active['version'],'verification':verification,'completed_ten_entry_checks':[x['human_entry'] for x in checks],
       'distinct_input_token_sequences':len({json.dumps(x['input_token_ids']) for x in raws}),
       'distinct_output_token_sequences':len({json.dumps(x['generated_token_ids']) for x in raws}),
       'distinct_reply_texts':len({x['text'] for x in raws}),
       'all_replies_equal_parent_last_reply':all(x['text']==source_rows[-1]['text'] for x in raws),
       'incomplete_executable_language_fences':sum(sum(not c['complete'] and c['language'] in ['python','sh'] for c in r.read(store/'batches'/f'{n:06d}.json')['parsed']['cells']) for n in range(1,51)),'complete_executable_cells':sum(x['cell_count'] for x in rows),'nonempty_feedback':sum(bool(x['feedback']) for x in rows),'boundaries':[x['boundary'] for x in rows if x['boundary'] is not None],
       'initial_notebook_bytes':initial_note[4],'final_notebook_bytes':final_note[4],
       'literal_append_bytes':sum(len((x['text']+'\n').encode()) for x in rows),
       'external_current_phase_exchanges':len(archive['exchanges'])+len(rows),'full_unselected_input_tokens':len(tok.apply_chat_template(full_messages,tokenize=True,add_generation_prompt=True)),
       'input_tokens':sorted({len(x['input_token_ids']) for x in raws}),'output_tokens':sorted({len(x['generated_token_ids']) for x in raws}),
       'generation_seconds_total':sum(x['seconds'] for x in raws),'generation_seconds_median':statistics.median(x['seconds'] for x in raws),'session_result':sessions[0],'training_updates':0,'pending':False,'synthetic_tests_not_main_progress':True}
    assert final_note[4]-initial_note[4]==result['literal_append_bytes']
    r.immutable(H/'BLOCK_AUDIT.json',result)
    print(json.dumps(result))
if __name__=='__main__':main()
