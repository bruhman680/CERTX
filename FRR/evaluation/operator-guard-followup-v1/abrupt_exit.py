"""Real child os._exit probe; disposable state, no lock removal."""
from pathlib import Path
import contextlib, io, json, os, subprocess, sys, types
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'source'))
import LIVING_GARDEN as living
import run_garden as base
def call(fn,**kw):
    with contextlib.redirect_stdout(io.StringIO()):fn(types.SimpleNamespace(**kw))
world=H/'worlds/abrupt_child_exit'
if '--child' in sys.argv:
    def crash(d,g,m,t):
        g.save(d/base.CHECKPOINT)
        os._exit(93)
    base._checkpoint=crash
    call(living.intervene,directory=str(world),learning='off',resource_multiplier=.8,energy_multiplier=None,reason='abrupt child exit')
    raise AssertionError('child fault did not fire')
call(living.initialize,directory=str(world),seed=72000,size=4,no_learning=False)
call(living.advance,directory=str(world),ticks=3,delay_ms=0,checkpoint_every=1,snapshot_every=1,report_every=3,resume=False)
call(living.pause,directory=str(world))
before=living._open(world)[0].fingerprint()
r=subprocess.run([sys.executable,str(Path(__file__)), '--child'],capture_output=True,text=True)
assert r.returncode==93
assert (world/'INTERVENTION_PENDING.json').exists()
assert (world/base.LOCK).exists()
after,manifest=living._open(world)
assert after.fingerprint()!=before
assert after.learning is False and manifest['learning'] is True
backup=next((world/'backups/interventions').glob('*.pkl')).name
try:
    call(living.restore_fork,directory=str(world),backup=backup,destination=str(H/'recovered/abrupt_child_exit'))
    raise AssertionError('stale lock expected')
except SystemExit as exc:
    failure=str(exc)
    assert 'lock' in failure.lower()
result={'status':'observed_limitation','exit_code':r.returncode,
 'pending_marker_retained':True,'stale_lock_retained':True,'physical_state_changed':True,
 'manifest_learning_stale':True,'explicit_restore_fork_blocked_by_stale_lock':True,
 'restore_error':failure,'no_lock_or_pending_removed':True,
 'scope':'Actual child-process os._exit, not machine power loss. Exposes operator recovery workflow gap; preserved own disposable world only.'}
(H/'ABRUPT_EXIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
