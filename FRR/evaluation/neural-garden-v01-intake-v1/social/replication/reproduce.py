"""Bounded offline replication after source inspection; no checkpoint loads."""
from pathlib import Path
import hashlib,json,sys,time
H=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(H/'sources'))
import numpy as np
import SOCIAL2_LAG_probe as lag
import SOC_MACRO_TRANSFER_probe as transfer
import SOC_MACRO_probe as macro

started=time.monotonic()
arch=json.loads((H/'sources/SOCIAL2_LAG_results.json').read_text())
rows=[]
for regrowth in [.06,.055]:
    new=lag.run(11000,regrowth,1500,2000)
    old=next(r for r in arch['rows'] if r['seed']==11000 and r['regrowth']==regrowth)
    maxerr=max(abs(new['arms'][a][h][m]-old['arms'][a][h][m])
        for a in lag.ARMS for h in ['500','2000'] for m in ['mean_energy','floor','bottom_decile','mean_resource'])
    rows.append({'regrowth':regrowth,'seed':11000,'max_absolute_error':maxerr,'match_tolerance_1e_12':maxerr<1e-12,'result':new})

train,_=transfer.observe(transfer.TRAIN,'fixed_50')
test,_=transfer.observe(transfer.TEST,'fixed_50')
reproduced=transfer.values(train,test,transfer.K3_FROM_LEARNED)
old=json.loads((H/'sources/SOC_MACRO_TRANSFER_results.json').read_text())['experiments']['fixed_50']['frozen_mapping']
comparison={k:{'reproduced':reproduced[k]['test_micro_nll'],'reported':old[k]['test_micro_nll'],
    'absolute_error':abs(reproduced[k]['test_micro_nll']-old[k]['test_micro_nll'])}
    for k in ['micro8_current','coarse3_current_aligned','coarse3_memory3']}

# Phase-only probe tests whether a fixed clock suffices across differently initialized worlds.
def phase_data(seq,period):
    ticks=np.arange(seq.shape[1]-1)
    phase=np.broadcast_to((ticks%period)[None,:,None],seq[:,:-1,:].shape).reshape(-1)
    y=seq[:,1:,:].reshape(-1)
    return phase,y
phase=[]
for period in [1,2,3,4,5,6]:
    x,y=phase_data(train,period); xt,yt=phase_data(test,period)
    count=np.full((period,8),.5);np.add.at(count,(x,y),1)
    p=count/count.sum(axis=1,keepdims=True)
    phase.append({'period':period,'heldout_nll':float(-np.log(p[xt,yt]).mean())})

payload={'scope':'Exact social seed11000 at2regimes/8arms plus fixed-policy macro full8train+8testseed reproduction; newphase-onlycontrol is exploratory',
    'social_rows':rows,'macro_fixed_policy':comparison,'macro_memory_gain':reproduced['memory_gain_nats'],
    'phase_only_clock_controls':phase,'elapsed_seconds':time.monotonic()-started,
    'python':sys.version,'numpy':np.__version__,
    'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (H/'sources').glob('*') if p.is_file()},
    'model_calls':0,'remote_checkpoint_loads':0,'canonical_world_changes':0}
with (H/'replication/RESULT.json').open('x') as f:json.dump(payload,f,indent=2);f.write('\n')
print(json.dumps({'social_max_errors':[r['max_absolute_error'] for r in rows],'macro':comparison,'phase_controls':phase,'elapsed_seconds':payload['elapsed_seconds']}))
