from pathlib import Path
import base64,json,sys
import adapter as a
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'byte-medium-mechanics-v1'))
from medium import evolve

def main():
    checks_root=H/'checks';checks_root.mkdir(exist_ok=True)
    attempt=max([int(p.name[7:]) for p in checks_root.glob('attempt*') if p.name[7:].isdigit()]+[0])+1
    out=checks_root/f'attempt{attempt:03d}';out.mkdir(exist_ok=False)
    seed=out/'seed';seed.mkdir();(seed/'objects').mkdir()
    raw=bytes([1,0])+bytes(60);sha=a.base._runtime.sha(raw)
    a.base.immutable(seed/'objects'/(sha+'.json'),{'sha256':sha,'bytes':len(raw),'base64':base64.b64encode(raw).decode()})
    payload={'entries':[['field.bin','file',0o644,sha,len(raw)]],'root_mode':0o755}
    bundle=dict(payload,id=a.base._runtime.sha(a.base._runtime.stable(payload)));a.base.immutable(seed/'bundle.json',bundle)
    checks=[]
    def passed(name):checks.append(name)
    def create(name,mode='changing'):return a.MediumWorld.create(out/name,seed/'bundle.json',seed/'objects',mode)
    def material(w,name='field.bin'):
        rows={r[0]:r for r in w.world.checkpoint()['entries']};row=rows.get(name)
        if row is None:return None
        if row[1]=='hardlink':row=rows[row[2]]
        assert row[1]=='file',row
        return base64.b64decode(a.base.read(w.path/'world/engine/objects'/(row[3]+'.json'))['base64'])
    w=create('dynamic');s=create('static','static')
    try:
        assert material(w)==material(s)==raw
        w.complete('ordinary unexecuted expression','idle');s.complete('ordinary unexecuted expression','idle')
        assert material(w)==evolve(raw) and material(s)==raw
        assert a.base.read(w.path/'STATE.json')==dict(replies=1,ticks=1,actor_operations=0)
        passed('matched real worlds; prose is not stored; one idle tick')
        snap=w.world.checkpoint();w.close();w=a.MediumWorld.open(out/'dynamic');assert w.world.checkpoint()==snap
        passed('pause/reopen leaves material and counters unchanged')
        source="```python\nopen('field.bin','wb').write(b'abc')\nraise ValueError('real failure after write')\n```\n```sh\nprintf d >> field.bin\nprintf kept > other.txt\n```"
        rec=w.complete(source,'actions');assert rec['actor_batch']['operations'][0]['receipt']['exit_code']!=0
        assert rec['actor_batch']['operations'][1]['receipt']['exit_code']==0
        assert material(w)==evolve(b'abcd') and material(w,'other.txt')==b'kept'
        assert rec['physical_tick']['before_id']==rec['actor_batch']['after_id']
        passed('literal Python failure retains write; later shell runs; tick follows both')
        before=w.world.checkpoint();old=a.base.read(w.path/'STATE.json');assert w.complete(source,'actions')==rec
        assert w.world.checkpoint()==before and a.base.read(w.path/'STATE.json')==old
        passed('identical reply retry does not replay process or tick')
        try:w.complete('different','actions')
        except ValueError:pass
        else:raise AssertionError('conflict accepted')
        passed('conflicting reply identity refused')
        w.complete("```sh\nrm field.bin\n```",'delete');assert material(w) is None
        w.complete('no command','still_absent');assert material(w) is None
        passed('deletion is not repaired on later ticks')
        w.complete("```python\nopen('field.bin','wb').write(b'')\n```",'empty');assert material(w)==b''
        passed('empty material valid')
        w.complete("```sh\nrm field.bin\nln -s other.txt field.bin\n```",'symlink')
        assert material(w,'other.txt')==b'kept'
        assert json.loads(a.base.read(w.path/'replies/symlink.json')['physical_tick']['receipt']['stdout'])['material']=='nonregular'
        passed('symlink material not followed or restored')
        w.complete("```sh\nrm field.bin\nmkdir field.bin\n```",'directory')
        assert json.loads(a.base.read(w.path/'replies/directory.json')['physical_tick']['receipt']['stdout'])['material']=='nonregular'
        passed('directory remains directory; physical law skips nonregular entry')
        w.complete("```python\nimport os\nos.rmdir('field.bin')\nopen('field.bin','wb').write(b'xyz')\nos.link('field.bin','alias')\n```",'hardlink')
        assert material(w)==evolve(b'xyz')
        # Capture stores a hardlink row rather than independent bytes.
        rows={r[0]:r for r in w.world.checkpoint()['entries']}
        assert rows['field.bin'][1]=='hardlink' or rows['alias'][1]=='hardlink'
        passed('hardlinked material updated in place with link relationship retained')
    finally:w.close();s.close()
    # Two separate, real process interruption points, with non-idempotent actor.
    for name,stage in [('after_actions','after_actions'),('after_tick','after_tick')]:
        w=create(name)
        text="```python\nfrom pathlib import Path\np=Path('count')\np.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n```"
        try:
            try:w.complete(text,'r1',fail_at=stage)
            except InterruptedError:pass
            else:raise AssertionError('injection missing')
        finally:w.close()
        try:a.MediumWorld.open(out/name)
        except a.base.PendingOutcome:pass
        else:raise AssertionError('pending reopened')
        rec=a.recover(out/name,'operator integration check; finish known prefix without actor replay')
        w=a.MediumWorld.open(out/name)
        try:
            assert material(w,'count')==b'1' and material(w)==evolve(raw)
            assert a.base.read(w.path/'STATE.json')==dict(replies=1,ticks=1,actor_operations=1)
            assert w.complete(text,'r1')==rec
        finally:w.close()
        passed(stage+': explicit recovery, actor executes once, physical tick once')
    w=create('unknown_tick');w.close()
    a.base.immutable(out/'unknown_tick/world/engine/PENDING.json',{'synthetic_fixture':True,'actual_unknown_process':False})
    try:a.MediumWorld.open(out/'unknown_tick')
    except a.base.PendingOutcome:pass
    else:raise AssertionError('unknown operation admitted')
    passed('synthetic unresolved individual operation refuses open; no replay')
    # Validate every clean engine ledger with inherited verifier.
    clean=['dynamic','static','after_actions','after_tick']
    for name in clean:assert a.c.verify(out/name/'world')['status']=='pass'
    passed('all four clean operation/bundle/receipt chains verify')
    result=dict(status='pass',checks=checks,checks_passed=len(checks),model_calls=0,candidate_world_actions=0,
                synthetic_unknown_marker=str((out/'unknown_tick/world/engine/PENDING.json').relative_to(H)),scope='process injections and real sandbox operations; not all power-loss/concurrency failures')
    a.base.immutable(out/'RESULTS.json',result);a.base.atomic(H/'RESULTS.json',result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
