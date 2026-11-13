"""Continue only the fault-test world we created locally, not any canonical run."""
from pathlib import Path
import contextlib, io, json, sys, types
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'sources'))
import LIVING_GARDEN as living
world=H/'disposable/fault'
before,manifest=living._open(world)
assert before.learning is False and manifest['learning'] is True
output=io.StringIO()
with contextlib.redirect_stdout(output):
    living.advance(types.SimpleNamespace(directory=str(world),ticks=1,delay_ms=0.,checkpoint_every=1,snapshot_every=1,report_every=1,resume=True))
after,m=living._open(world)
assert after.tick==before.tick+1 and after.learning is False and m['learning'] is True
record={'same_tick_partial_intervention_resumed':True,'before_tick':before.tick,'after_tick':after.tick,
    'actual_learning':after.learning,'manifest_learning':m['learning'],
    'scope':'One extra tick in our disposable fault-injection world; no canonical world or remote pickle involved'}
(H/'GAP_CONTINUATION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
