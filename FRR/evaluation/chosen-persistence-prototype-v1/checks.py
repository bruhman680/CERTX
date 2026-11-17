"""Operator-only mechanics checks. No model calls or behavioral objectives."""
from pathlib import Path
import sys,json,traceback
H=Path(__file__).resolve().parent;E=H.parent
sys.path[:0]=[str(H),str(E/'observability-three-contact-v1')]
import coupling as p
import common as c

def main():
    out=H/'checks/attempt001';out.mkdir(parents=True,exist_ok=False)
    baseline={'main':c.inventory(E/'bounded-main-continuation-v1'),'original':c.inventory(),'active':c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')}
    p.base.immutable(out/'BEFORE.json',baseline)
    seed=out/'seed';seed.mkdir();(seed/'objects').mkdir()
    payload={'entries':[],'root_mode':0o755};bundle=dict(payload,id=p.base._runtime.sha(p.base._runtime.stable(payload)))
    p.base.immutable(seed/'bundle.json',bundle)
    results=[]
    def record(name,**data):results.append({'check':name,'status':'pass',**data})
    def create(name):return p.ChosenWorld.create(out/name,seed/'bundle.json',seed/'objects')
    w=None
    try:
        w=create('mechanics');initial=w.checkpoint()
        b=w.receive_expression('Unfinished ideas may remain writing. 😁','prose')
        assert b['operations']==[] and w.step==0 and w.checkpoint()==initial
        assert p.base.read(w.store/'engine/batches/prose.json')['raw_text']==b['raw_text']
        assert not any(x[0]=='notebook.txt' for x in w.checkpoint()['entries'])
        record('prose_external_only',world_id=initial['id'],world_step=0)
        text="```python\nfrom pathlib import Path\nprivate = 7\nPath('seed.txt').write_text('hello')\nprint('stored')\n```\n"
        b=w.receive_expression(text,'write');assert len(b['operations'])==1 and b['operations'][0]['changed_paths']==['seed.txt']
        assert b['operations'][0]['receipt']['exit_code']==0 and b['operations'][0]['receipt']['stdout']=='stored\n'
        record('explicit_world_write',changed_paths=b['operations'][0]['changed_paths'])
        text="```python\nraise ValueError('ordinary error')\n```\n```sh\nprintf after > after.txt\n```\n"
        b=w.receive_expression(text,'error_then_write')
        assert b['operations'][0]['receipt']['exit_code']!=0 and 'ordinary error' in b['operations'][0]['receipt']['stderr']
        assert b['operations'][1]['receipt']['exit_code']==0 and b['operations'][1]['changed_paths']==['after.txt']
        record('ordinary_error_does_not_gate_later_cell',operations=len(b['operations']))
        b=w.receive_expression('```python\nprint(private)\n```','variables_reset')
        assert 'NameError' in b['operations'][0]['receipt']['stderr']
        snapshot=w.checkpoint();w.close();w=p.ChosenWorld.open(out/'mechanics');assert w.checkpoint()==snapshot
        b=w.receive_expression("```python\nfrom pathlib import Path\nprint(Path('seed.txt').read_text(), Path('after.txt').read_text())\n```",'reopen_read')
        assert b['operations'][0]['receipt']['stdout']=='hello after\n'
        record('files_persist_variables_do_not',before_reopen_id=snapshot['id'])
        before=w.checkpoint();step=w.step
        b=w.receive_expression("````text\n```python\nopen('unexpected','w').write('bad')\n```\n````\n",'shielded')
        assert b['operations']==[] and w.checkpoint()==before and w.step==step
        record('unknown_fence_shields_inner_code')
        nine=''.join("```python\nopen('unexpected','w').write('bad')\n```\n" for _ in range(9))
        b=w.receive_expression(nine,'too_many');assert b['boundary']=='cell_count_limit' and b['operations']==[] and w.checkpoint()==before
        record('cell_count_boundary_before_effects')
        try:w.receive_expression("```python\nprint('should not replay')\n```",'write')
        except p.base.PendingOutcome:pass
        else:raise AssertionError('Recorded reply was replayed')
        assert w.checkpoint()==before;record('duplicate_reply_refused')
        w.close();w=None
        assert p.verify(out/'mechanics')['status']=='pass'
        w=create('interruption');original=w.engine.apply
        def stop_after_commit(*args,**kwargs):
            event=original(*args,**kwargs)
            raise InterruptedError('operator injection after committed first action, before batch update')
        w.engine.apply=stop_after_commit
        text="```python\nfrom pathlib import Path\np=Path('count')\np.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n```\n```python\nopen('second','w').write('should remain unexecuted')\n```"
        try:w.receive_expression(text,'interrupted')
        except InterruptedError:pass
        else:raise AssertionError('Injection did not fire')
        assert w.step==1 and (w.store/'engine/BATCH_PENDING.json').exists()
        w.close();w=None
        try:p.ChosenWorld.open(out/'interruption')
        except p.base.PendingOutcome:pass
        else:raise AssertionError('Pending batch reopened without inspection')
        sealed=p.recover_known_prefix(out/'interruption','operator mechanics test: seal known prefix, abandon remaining cell')
        assert len(sealed['operations'])==1 and sealed['unexecuted_cells']==1 and sealed['status']=='interrupted'
        w=p.ChosenWorld.open(out/'interruption')
        b=w.receive_expression("```python\nfrom pathlib import Path\nprint(Path('count').read_text(), Path('second').exists())\n```",'inspect_prefix')
        assert b['operations'][0]['receipt']['stdout']=='1 False\n'
        record('interrupted_prefix_preserved_not_replayed',committed_prefix=1,abandoned_remaining=1)
        w.close();w=None
        assert p.verify(out/'interruption')['status']=='pass'
        # A synthetic unknown-operation marker must be refused, not interpreted as a known prefix.
        w=create('unknown_marker');w.close();w=None
        marker=out/'unknown_marker/engine/PENDING.json'
        p.base.immutable(marker,{'fixture_only':True,'actual_operation_attempted':False})
        try:p.recover_known_prefix(out/'unknown_marker','synthetic unknown-operation refusal test')
        except p.base.PendingOutcome:pass
        else:raise AssertionError('Unknown individual operation was treated as known')
        assert marker.exists();record('unknown_individual_outcome_refused',synthetic_fixture_only=True,marker_retained=True)
        assert c.inventory(E/'bounded-main-continuation-v1')==baseline['main'] and c.inventory()==baseline['original']
        assert c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')==baseline['active']
        p.base.immutable(out/'RESULTS.json',{'status':'pass','checks':results,'model_calls':0,'main_entry':1630,'main_unchanged':True,'original_unchanged':True,'activation':False,'live_pending_actions':False,'synthetic_blocked_fixture':'unknown_marker/engine/PENDING.json'})
        print(json.dumps({'status':'pass','checks':len(results),'model_calls':0,'main_entry':1630}),flush=True)
    except BaseException as error:
        p.base.immutable(out/'ERROR.json',{'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'completed_checks':results})
        raise
    finally:
        if w is not None:w.close()

if __name__=='__main__':main()
