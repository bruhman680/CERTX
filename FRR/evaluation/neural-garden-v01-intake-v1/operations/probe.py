"""Bounded local persistence checks after source inspection. Only own pickles."""
from pathlib import Path
import contextlib, io, json, sys, types, hashlib
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'sources'))
from garden import Garden
import LIVING_GARDEN as living
import run_garden as base
import numpy as np

def args(**kw):return types.SimpleNamespace(**kw)
def invoke(fn,**kw):
    s=io.StringIO()
    with contextlib.redirect_stdout(s):fn(args(**kw))
    return s.getvalue()

def main():
    root=H/'disposable';root.mkdir(exist_ok=False)
    results={}
    g=Garden(seed=61012,size=4,learning=True)
    for _ in range(15):g.step()
    path=root/'own.pkl';g.save(path);copy=Garden.load(path)
    assert g.fingerprint()==copy.fingerprint()
    for _ in range(5):g.step();copy.step()
    assert g.fingerprint()==copy.fingerprint()
    results['same_checkpoint_same_five_future_ticks']=True
    f=Garden(seed=61013,size=4,learning=False)
    weights={n:getattr(f,n).copy() for n in ['win','wrec','bhidden','wpred','bpred','wact','bact']}
    for _ in range(30):f.step()
    assert all(np.array_equal(v,getattr(f,n)) for n,v in weights.items())
    results['all_seven_neural_tensors_frozen']=True
    world=root/'world'
    logs=[]
    logs.append(invoke(living.initialize,directory=str(world),seed=61014,size=4,no_learning=False))
    logs.append(invoke(living.advance,directory=str(world),ticks=5,delay_ms=0.,checkpoint_every=2,snapshot_every=2,report_every=5,resume=False))
    logs.append(invoke(living.pause,directory=str(world)))
    pre,m=living._open(world);before=pre.fingerprint()
    clone=root/'clone';logs.append(invoke(living.fork,directory=str(world),destination=str(clone)))
    cg,_=living._open(clone);assert cg.fingerprint()==before
    logs.append(invoke(living.intervene,directory=str(world),learning=None,resource_multiplier=.8,energy_multiplier=None,reason='local audited diagnostic'))
    after,_=living._open(world);after_fp=after.fingerprint();assert after_fp!=before
    backup=next((world/'backups/interventions').glob('*.pkl'))
    restored=root/'restored'
    logs.append(invoke(living.restore_fork,directory=str(world),destination=str(restored),backup=backup.name))
    rg,_=living._open(restored);assert rg.fingerprint()==before
    assert living._open(world)[0].fingerprint()==after_fp
    results['pause_fork_intervention_exact_restore_fork']={'pass':True,'before':before,'after':after_fp,'restored':rg.fingerprint(),'source_still_after':True}

    # Inject precisely the interrupted state-write / manifest-write gap. This
    # is a simulated exception, not an actual power-loss or hard-kill test.
    fault=root/'fault';logs.append(invoke(living.fork,directory=str(clone),destination=str(fault)))
    old_state,old_manifest=living._open(fault)
    old_fp=old_state.fingerprint();old_manifest_bytes=(fault/base.MANIFEST).read_bytes()
    normal=base._checkpoint
    def state_only(directory,garden,manifest,completed):
        garden.save(directory/base.CHECKPOINT)
        raise RuntimeError('injected after state replacement, before manifest replacement')
    base._checkpoint=state_only
    try:
        try:
            invoke(living.intervene,directory=str(fault),learning='off',resource_multiplier=.8,energy_multiplier=None,reason='declared local fault injection')
            raise AssertionError('Expected injected interruption')
        except RuntimeError as e:
            assert 'injected after state' in str(e)
    finally:base._checkpoint=normal
    resumed,stale=living._open(fault)
    events=[json.loads(x) for x in (fault/living.EVENTS).read_text().splitlines()]
    gap={'same_tick':resumed.tick==stale['completed_steps'],
         'manifest_bytes_unchanged':(fault/base.MANIFEST).read_bytes()==old_manifest_bytes,
         'world_fingerprint_changed':resumed.fingerprint()!=old_fp,
         'actual_learning':resumed.learning,'manifest_learning':stale['learning'],
         'last_event_kind':events[-1]['kind'],'open_accepted_interrupted_same_tick_state':True,
         'fault_method':'Injected Python exception after own checkpoint save, before manifest update; no power-loss test',
         'scope':'Disposable world only; no canonical state loaded, modified, repaired, resumed or merged'}
    assert gap['same_tick'] and gap['manifest_bytes_unchanged'] and gap['world_fingerprint_changed']
    assert resumed.learning is False and stale['learning'] is True and events[-1]['kind']=='intervention_prepare'
    results['same_tick_intervention_commit_gap']=gap
    results['source_commit']='3204c81ebc6922d66b0ae2623ee83d629f11f3b8'
    results['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (H/'sources').iterdir() if p.is_file()}
    results['remote_pickles_loaded']=0
    (H/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    (H/'CLI_TRANSCRIPT.txt').write_text('\n'.join(logs))
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
