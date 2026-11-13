"""Detached exception-point matrix; trusted fresh local states only."""
from pathlib import Path
import contextlib, hashlib, io, json, shutil, sys, types

HOME=Path(__file__).resolve().parent
SOURCE=HOME.parent/'neural-garden-v01-intake-v1/operations/guard_proposal'
CODE=HOME/'source'; CODE.mkdir(exist_ok=True)
for name in ('garden.py','run_garden.py','LIVING_GARDEN.py'):
    shutil.copyfile(SOURCE/name,CODE/name)
sys.path.insert(0,str(CODE))
import LIVING_GARDEN as living
import run_garden as base

def call(fn,**kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(types.SimpleNamespace(**kwargs))

class Injected(Exception): pass

points=['before_pending','after_pending','checkpoint_state_only','after_checkpoint',
        'after_snapshot','after_final_manifest','after_applied_event']
rows=[]
for number,point in enumerate(points):
    world=HOME/'worlds'/point
    world.parent.mkdir(exist_ok=True)
    call(living.initialize,directory=str(world),seed=71000+number,size=4,no_learning=False)
    call(living.advance,directory=str(world),ticks=3,delay_ms=0,checkpoint_every=1,snapshot_every=1,report_every=3,resume=False)
    call(living.pause,directory=str(world))
    before=living._open(world)[0].fingerprint()
    atomic,checkpoint,snapshot,event=base._atomic_json,base._checkpoint,base._snapshot,living._event
    manifest_writes=[0]
    def injected_atomic(path,data):
        if path.name=='INTERVENTION_PENDING.json' and point=='before_pending':
            raise Injected(point)
        atomic(path,data)
        if path.name=='INTERVENTION_PENDING.json' and point=='after_pending':
            raise Injected(point)
        if path==world/base.MANIFEST:
            manifest_writes[0]+=1
            if point=='after_final_manifest' and manifest_writes[0]==2:
                raise Injected(point)
    def injected_checkpoint(d,g,m,t):
        if point=='checkpoint_state_only':
            g.save(d/base.CHECKPOINT)
            raise Injected(point)
        checkpoint(d,g,m,t)
        if point=='after_checkpoint': raise Injected(point)
    def injected_snapshot(d,g,t):
        snapshot(d,g,t)
        if point=='after_snapshot': raise Injected(point)
    def injected_event(d,p):
        event(d,p)
        if p['kind']=='intervention_applied' and point=='after_applied_event':
            raise Injected(point)
    base._atomic_json=injected_atomic; base._checkpoint=injected_checkpoint
    base._snapshot=injected_snapshot; living._event=injected_event
    try:
        try:
            call(living.intervene,directory=str(world),learning='off',resource_multiplier=.8,energy_multiplier=None,reason=point)
            raise AssertionError('fault point not reached')
        except Injected: pass
    finally:
        base._atomic_json=atomic; base._checkpoint=checkpoint
        base._snapshot=snapshot; living._event=event
    partial,manifest=living._open(world)
    fingerprint=partial.fingerprint()
    pending=(world/'INTERVENTION_PENDING.json').exists()
    row={'point':point,'pending':pending,'state_changed':fingerprint!=before,
         'actual_learning':bool(partial.learning),'manifest_learning':manifest['learning'],
         'blocked':{},'state_preserved_during_block_checks':True}
    if pending:
        for action,fn,kwargs in [
            ('advance',living.advance,dict(ticks=1,delay_ms=0,checkpoint_every=1,snapshot_every=1,report_every=1,resume=True)),
            ('intervene',living.intervene,dict(learning='off',resource_multiplier=.8,energy_multiplier=None,reason='must block')),
            ('fork',living.fork,dict(destination=str(HOME/'forbidden'/point)))]:
            try:
                call(fn,directory=str(world),**kwargs)
                raise AssertionError(action+' unexpectedly allowed')
            except SystemExit as exc:
                assert 'Unfinished intervention' in str(exc)
                row['blocked'][action]=True
            assert living._open(world)[0].fingerprint()==fingerprint
        call(living.inspect,directory=str(world),tail=10)
    else:
        assert point=='before_pending' and fingerprint==before
        # Retry is not automatically safe: preserved backup prevents overwrite.
        try:
            call(living.intervene,directory=str(world),learning='off',resource_multiplier=.8,energy_multiplier=None,reason='retry')
            raise AssertionError('expected preserved backup collision')
        except SystemExit as exc:
            assert 'Refusing to overwrite' in str(exc)
            row['retry_backup_collision']=True
    backup=next((world/'backups/interventions').glob('*.pkl')).name
    destination=HOME/'recovered'/point
    call(living.restore_fork,directory=str(world),backup=backup,destination=str(destination))
    assert living._open(destination)[0].fingerprint()==before
    row['exact_recovery_fork']=True
    row['original_pending_preserved']=(world/'INTERVENTION_PENDING.json').exists()==pending
    rows.append(row)

# Ordinary successful path after a clean recovery is still usable.
clean=HOME/'recovered'/points[-1]
call(living.intervene,directory=str(clean),learning='off',resource_multiplier=.8,energy_multiplier=None,reason='clean success')
assert not (clean/'INTERVENTION_PENDING.json').exists()
result={'status':'pass','method':'Injected Python exceptions, seven interruption boundaries; fresh 4x4 worlds, three ticks each',
        'rows':rows,'clean_success_clears_marker':True,
        'code_sha256':{n:hashlib.sha256((CODE/n).read_bytes()).hexdigest() for n in ('garden.py','run_garden.py','LIVING_GARDEN.py')},
        'limits':['No hard kill or power loss','No filesystem directory fsync guarantee','No deployment or canonical-state change','Lock finally cleanup remains active under Python exceptions']}
(HOME/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
