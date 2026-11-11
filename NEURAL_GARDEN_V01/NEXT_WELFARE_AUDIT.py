"""Independent, untouched-seed long-horizon audit of welfare-shaped policies.

No model selection occurs here. All action modes are frozen deterministic.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import numpy as np

from NEXT_WELFARE_garden import WelfareGarden
from NEXT_WELFARE_study import RuleGarden,train

ROOT=Path(__file__).resolve().parent
SEEDS=tuple(range(9600,9608))
POLICIES=('reserve_neural','neighbor_manual','reverse_manual','fixed50_manual')
REGIMES=('stable','mild')
TICKS=8000


def run_one(seed, policy, regime, theta):
    if policy=='reserve_neural':
        g=WelfareGarden(seed=seed+20000,size=10,learning=False,
                        objective='reserve',deterministic=True)
        g.theta=theta.copy()
    else:
        rule={'neighbor_manual':'neighbor','reverse_manual':'reverse',
              'fixed50_manual':'fixed50'}[policy]
        g=RuleGarden(seed=seed+20000,size=10,rule=rule)
    tails=[];floor_integral=[];milestones={}
    for t in range(1,TICKS+1):
        g.regrowth=.055 if regime=='mild' and 1000<t<=2000 else .06
        m=g.step()
        if t>TICKS-500:tails.append(float(m['raw_drift']))
        floor_integral.append(float(np.mean(g.energy<=.01)))
        if t in (1000,2000,3000,5000,8000):
            milestones[str(t)]={'energy':float(g.energy.mean()),
                                'floor':float(np.mean(g.energy<=.01)),
                                'resource':float(g.resource.mean())}
    return {'seed':seed,'policy':policy,'regime':regime,
            'energy':float(g.energy.mean()),
            'floor':float(np.mean(g.energy<=.01)),
            'ceiling':float(np.mean(g.energy>=.99)),
            'bottom_decile':float(np.mean(np.sort(g.energy)[:g.count//10])),
            'cumulative_floor':float(np.mean(floor_integral)),
            'tail_raw_drift':float(np.mean(tails)),
            'milestones':milestones}


def run():
    rows=[]
    for seed in SEEDS:
        theta=train('reserve',seed,10,1000)
        for regime in REGIMES:
            for policy in POLICIES:
                rows.append(run_one(seed,policy,regime,theta))
    summary={}
    for regime in REGIMES:
        summary[regime]={}
        for policy in POLICIES:
            z=[r for r in rows if r['regime']==regime and r['policy']==policy]
            summary[regime][policy]={k:float(np.mean([r[k] for r in z])) for k in
                ('energy','floor','bottom_decile','cumulative_floor','tail_raw_drift')}
            summary[regime][policy]['t3000_energy']=float(np.mean([r['milestones']['3000']['energy'] for r in z]))
    comparison={}
    for regime in REGIMES:
        a=np.array([r['energy'] for r in rows if r['regime']==regime and r['policy']=='reserve_neural'])
        for policy in POLICIES[1:]:
            b=np.array([r['energy'] for r in rows if r['regime']==regime and r['policy']==policy])
            d=a-b
            comparison[regime+'/'+policy]={
                'reserve_minus_control_mean':float(d.mean()),
                'paired_sd':float(d.std(ddof=1)),
                'reserve_wins':int((d>0).sum()), 'n':len(d)}
    result={'design':{'fresh_seeds':SEEDS,'size':10,'train_ticks':1000,
                      'evaluation_ticks':TICKS,'policies':POLICIES,'regimes':REGIMES,
                      'mild_schedule':'regrowth 0.055 over ticks1001..2000; baseline otherwise',
                      'identical_action_mode':'all frozen deterministic',
                      'no_tuning_or_selection':True},
            'rows':rows,'summary':summary,'paired_comparisons':comparison,
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
              for f in ('garden.py','NEXT_WELFARE_garden.py',
                        'NEXT_WELFARE_study.py','NEXT_WELFARE_AUDIT.py')},
            'platform':{'python':platform.python_version(),'numpy':np.__version__},
            'caveat':'Fresh seeds but same synthetic world family; reward is hand-shaped, no online learning during deployment, end-of-horizon comparison remains conditional.'}
    (ROOT/'NEXT_WELFARE_AUDIT_results.json').write_text(json.dumps(result,indent=2)+'\n')
    return summary,comparison


if __name__=='__main__':
    a,b=run();print(json.dumps({'summary':a,'comparisons':b},indent=2))
