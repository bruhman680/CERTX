"""Independent scalar probability/identified-set check of saved artifacts."""
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
j=json.loads((D/'RESULTS.json').read_text());errors=[];outside_checks=0;maxerr=0.
for row in j['cells']:
    v,a1,a0=row['v'],row['a1'],row['a0']
    p1=v*a1;p0=(1-v)*a0;pm=1-p1-p0
    expected=[p1,p0,pm]
    actual=row['observations']['ternary_1_0_missing']
    maxerr=max(maxerr,max(abs(a-b) for a,b in zip(actual,expected)))
    lo,hi=row['survival_interval']
    for candidate in [lo-.01,hi+.01]:
        if not 0<=candidate<=1:continue
        outside_checks+=1
        # Gate probabilities are feasible iff observed mass does not exceed total mass of S.
        if p1<=candidate+1e-12 and p0<=1-candidate+1e-12:errors.append(['outside_feasible',row,candidate])
    if abs(a1-a0)<1e-12 and a1==0 and (lo!=0 or hi!=1):errors.append(['unreadable_not_unidentified',row])
    if abs(row['restored_preserving_survival']-v)>1e-12:errors.append(['preserving_failed',row])
    if abs(row['restored_rewriting_survival']-.6)>1e-12:errors.append(['rewrite_failed',row])
checks={'scalar_laws_agree':maxerr<1e-12,'outside_set_infeasible':not errors,'protocol_unchanged':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'all_recorded_checks_pass':all(j['checks'].values()),'empty_stderr':(D/'RUN.stderr.txt').stat().st_size==0}
out={'scope':'Same authored model checked with scalar constraints; not independent empirical replication','outside_points_checked':outside_checks,'max_observation_probability_error':maxerr,'checks':checks,'errors':errors,'sha256':{p:hashlib.sha256((D/p).read_bytes()).hexdigest() for p in ['PROTOCOL.md','run.py','RESULTS.json','RUN.stdout.txt','RUN.stderr.txt']}}
(D/'CHECKS.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
