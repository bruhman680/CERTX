"""Real committed effect + injected final-record/unlink interruption; no model calls."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
import coupling as p

out=H/'checks/finalization';out.mkdir(parents=True,exist_ok=False)
seed=H/'checks/attempt001/seed'
w=p.ChosenWorld.create(out/'world',seed/'bundle.json',seed/'objects')
original=p.unlink_durable
def interrupt_unlink(path):
    if Path(path).name=='BATCH_PENDING.json':raise InterruptedError('operator injection: final batch saved, pending unlink not done')
    return original(path)
p.unlink_durable=interrupt_unlink
try:
    try:w.receive_expression("```python\nfrom pathlib import Path\np=Path('count')\np.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n```",'committed')
    except InterruptedError:pass
    else:raise AssertionError('Injection did not fire')
finally:
    p.unlink_durable=original;w.close()
assert (out/'world/engine/BATCH_PENDING.json').exists()
before=p.base.read(out/'world/engine/batches/committed.json')
sealed=p.recover_known_prefix(out/'world','operator mechanics check: finalize saved complete batch without execution')
assert sealed==before and sealed['status']=='completed' and len(sealed['operations'])==1
w=p.ChosenWorld.open(out/'world')
try:
    try:w.receive_expression("```python\nprint('duplicate')\n```",'committed')
    except p.base.PendingOutcome:pass
    else:raise AssertionError('Completed reply replayed')
    r=w.receive_expression("```python\nprint(open('count').read())\n```",'read_count')
    assert r['operations'][0]['receipt']['stdout']=='1\n'
finally:w.close()
p.base.immutable(out/'RESULTS.json',{'status':'pass','final_record_unchanged':True,'action_replays':0,'counter':1,'model_calls':0,'verification':p.verify(out/'world')})
print(json.dumps({'status':'pass','action_replays':0,'counter':1,'model_calls':0}))
