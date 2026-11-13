"""Create/test an isolated proposed operator guard. Original sources unchanged."""
from pathlib import Path
import contextlib, difflib, io, json, shutil, sys, types
H=Path(__file__).resolve().parent
src=H/'sources'
target=H/'guard_proposal';target.mkdir(exist_ok=False)
old=(src/'LIVING_GARDEN.py').read_text()
new=old
sentinel='        garden, manifest = _open(directory)\n'
assert new.count(sentinel)==2
new=new.replace(sentinel,'        if (directory / "INTERVENTION_PENDING.json").exists():\n            raise SystemExit("Unfinished intervention; inspect backup/events before continuing")\n'+sentinel)
sentinel='        parent, manifest = _open(source)\n'
assert new.count(sentinel)==1
new=new.replace(sentinel,'        if (source / "INTERVENTION_PENDING.json").exists():\n            raise SystemExit("Unfinished intervention; use explicit backup recovery, not an ordinary fork")\n'+sentinel)
sentinel='        if args.learning is not None:\n'
assert new.count(sentinel)==1
new=new.replace(sentinel,'        pending_path = directory / "INTERVENTION_PENDING.json"\n        base._atomic_json(pending_path, {"tick":garden.tick,"before":previous,"backup":backup_name,"change":change})\n'+sentinel)
sentinel='                           "new_fingerprint": garden.fingerprint()})\n'
assert new.count(sentinel)==1
new=new.replace(sentinel,sentinel+'        pending_path.unlink()\n')
(target/'LIVING_GARDEN.py').write_text(new)
for n in ['garden.py','run_garden.py']:shutil.copyfile(src/n,target/n)
(H/'OPERATOR_GUARD_PROPOSAL.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='pinned/LIVING_GARDEN.py',tofile='proposal/LIVING_GARDEN.py')))
sys.path.insert(0,str(target))
import LIVING_GARDEN as living
import run_garden as base
from garden import Garden
def call(fn,**kw):
    with contextlib.redirect_stdout(io.StringIO()):fn(types.SimpleNamespace(**kw))
world=target/'fresh_world'
call(living.initialize,directory=str(world),seed=61014,size=4,no_learning=False)
call(living.advance,directory=str(world),ticks=5,delay_ms=0,checkpoint_every=2,snapshot_every=2,report_every=5,resume=False)
call(living.pause,directory=str(world))
before=living._open(world)[0].fingerprint()
normal=base._checkpoint
def fault(d,g,m,t):
    g.save(d/base.CHECKPOINT)
    raise RuntimeError('injected same-tick commit gap')
base._checkpoint=fault
try:
    try:call(living.intervene,directory=str(world),learning='off',resource_multiplier=.8,energy_multiplier=None,reason='isolated guard test')
    except RuntimeError as e:assert 'injected' in str(e)
finally:base._checkpoint=normal
assert (world/'INTERVENTION_PENDING.json').exists()
partial=living._open(world)[0].fingerprint()
try:
    call(living.advance,directory=str(world),ticks=1,delay_ms=0,checkpoint_every=1,snapshot_every=1,report_every=1,resume=True)
    raise AssertionError('Guard must reject continuation')
except SystemExit as e:assert 'Unfinished intervention' in str(e)
assert living._open(world)[0].fingerprint()==partial
backup=next((world/'backups/interventions').glob('*.pkl')).name
recovered=target/'recovered'
call(living.restore_fork,directory=str(world),backup=backup,destination=str(recovered))
assert living._open(recovered)[0].fingerprint()==before
call(living.intervene,directory=str(recovered),learning=None,resource_multiplier=.8,energy_multiplier=None,reason='known completed intervention')
assert not (recovered/'INTERVENTION_PENDING.json').exists()
assert (world/'INTERVENTION_PENDING.json').exists()
result={'status':'pass','guard_rejects_unfinished_same_tick_intervention':True,
 'rejection_does_not_modify_partial_state':True,'explicit_backup_recovery_fork_retains_original':True,
 'completed_intervention_clears_guard':True,'original_physics_source_unchanged':(src/'garden.py').read_bytes()==(target/'garden.py').read_bytes(),
 'scope':'Proposed operator-only patch, tested on newly generated local states with injected exceptions. No upstream merge, canonical mutation, power-loss durability or full crash-matrix claim.'}
(H/'GUARD_PROPOSAL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
