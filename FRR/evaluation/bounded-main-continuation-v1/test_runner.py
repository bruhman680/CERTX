"""Real sandbox effects with explicitly synthetic model text; zero inference."""
from pathlib import Path
import json
import runner as r

def main():
    root=r.H/'tests-v2';root.mkdir(exist_ok=False)
    store=root/'fixture';before=r.inventory(r.C)
    r.prepare(store,purpose='fixture_no_inference');tok=r.tokenizer();first=r.verify(store,tok)
    assert first['human_entry']==1580 and first['next_view']['next_input_tokens']==2231
    assert first['next_view']['included_entries']==list(range(1573,1581))
    rows=[]
    for text in ["```python\nfrom pathlib import Path\nPath('continuity_test.txt').write_text('persisted')\nprint('first receipt')\n```", "```python\nraise ValueError('ordinary error')\n```\n```python\nfrom pathlib import Path\nprint(Path('continuity_test.txt').read_text())\n```"]:
        w=r.GardenWorld.open(store/'world')
        try:
            view=r.plan_reply(store,tok,w)
            if rows:assert 'first receipt' in view['messages'][-1]['content']
            raw={'run_id':'fixture_no_inference','messages':view['messages'],'input_token_ids':view['input_token_ids'],'generated_token_ids':tok.encode(text,add_special_tokens=False)+[tok.eos_token_id],'text':text,'stop':'eos','decoder':'fixture_no_inference','seconds':0}
            rows.append(r.commit_reply(store,tok,w,view,raw))
        finally:w.close()
        state=r.read(store/'STATE.json');state['paused']=True;r.atomic(store/'STATE.json',state)
        assert r.verify(store,tok)['human_entry']==1580+len(rows)
    feedback=json.loads(rows[-1]['feedback'])
    assert feedback['receipts'][0]['exit_code']==1 and feedback['receipts'][1]['exit_code']==0
    assert feedback['receipts'][1]['stdout']=='persisted\n'
    # A pending marker blocks both verify and planning before any action or generation.
    pending={'test':'known injected pending marker; no actual unknown action'}
    r.immutable(store/'PENDING.json',pending);snap=r.read(store/'world/STATE.json')
    rejected=0
    try:r.verify(store,tok)
    except RuntimeError:rejected+=1
    w=r.GardenWorld.open(store/'world')
    try:
        try:r.plan_reply(store,tok,w)
        except RuntimeError:rejected+=1
    finally:w.close()
    assert rejected==2 and snap==r.read(store/'world/STATE.json')
    r.immutable(root/'PENDING_TEST_RECORD.json',{'injected':pending,'rejections':rejected,'no_world_change':True})
    (store/'PENDING.json').unlink() # Test-created marker only, not unknown runtime work.
    # Existing run lock must not be removed by a caller that failed to acquire it.
    r.immutable(store/'RUN.lock',{'token':'test-existing-owner'})
    try:r.resume(store,1)
    except FileExistsError:pass
    else:raise AssertionError('Existing lock should reject caller before model load')
    assert r.read(store/'RUN.lock')=={'token':'test-existing-owner'}
    r.immutable(root/'LOCK_TEST_RECORD.json',{'owner_retained':True,'model_calls':0})
    (store/'RUN.lock').unlink()
    # Mandatory initial/latest pair is never silently truncated when over capacity.
    try:r.select_view(r.read(store/'BASE_ARCHIVE.json')['initial_messages'],r.read(store/'BASE_ARCHIVE.json')['exchanges'],tok,max_pairs=8,max_input=1)
    except r.ViewCapacity:pass
    else:raise AssertionError('Expected capacity pause')
    final=r.verify(store,tok);assert before==r.inventory(r.C)
    r.immutable(root/'RESULTS.json',{'status':'pass','model_calls':0,'sandbox_fixture_replies':2,'main_unchanged_files':len(before),'first':first,'final':final,'pending_rejections':2,'lock_owner_retained':True,'capacity_no_truncation':True,'ordinary_error_then_following_cell_succeeds':True,'persistent_file_after_close_reopen':True,'receipt_in_next_view':True})
    print(json.dumps({'status':'pass','model_calls':0,'fixture_entries':[1581,1582],'main_files_unchanged':len(before)}))

if __name__=='__main__':main()
