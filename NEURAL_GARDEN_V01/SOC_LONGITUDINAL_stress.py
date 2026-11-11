"""Pre-frozen policies under deeper horizon and resource-shock tests.

One additional research movement after held-out screening, not one loop per seed.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_LONGITUDINAL_explore import run

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'SOC_LONGITUDINAL_stress_results.json'
SEEDS=list(range(20500,20512))
POLICIES={
 'fixed_050':{'kind':'fixed','theta':.50},
 'energy_rescue':{'kind':'energy_rescue','theta':.51,'low_energy':.12,'discount':.025},
 'neighbor_gradient':{'kind':'neighbor','theta':.51,'coupling':.5},
}
SCENARIOS={'unchanged_20000':{'horizon':20000,'shock':None},
           'shocked_10000':{'horizon':10000,'shock':{3000:.7,6000:.7}}}

def main():
    rows=[]
    for seed in SEEDS:
        anchor=Garden(seed=seed,size=16,learning=False)
        for scene,scfg in SCENARIOS.items():
            for arm,policy in POLICIES.items():
                result=run(anchor,policy,horizon=scfg['horizon'],shock=scfg['shock'])
                rows.append({'seed':seed,'scenario':scene,'policy':arm,
                  'energy':result['energy'],'floor':result['floor'],
                  'raw_tail':result['raw_tail'],
                  'energy_tail':result['mean_energy_tail'],
                  'timeline':result['points']})
    summary={}
    for scene in SCENARIOS:
        summary[scene]={}
        for arm in POLICIES:
            records=[x for x in rows if x['scenario']==scene and x['policy']==arm]
            summary[scene][arm]={key:float(np.mean([r[key] for r in records]))
                                 for key in ('energy','floor','raw_tail','energy_tail')}
    paired={}
    for scene in SCENARIOS:
        paired[scene]={}
        for arm in ('energy_rescue','neighbor_gradient'):
            values=np.array([x['energy'] for x in rows if x['scenario']==scene and x['policy']==arm])
            baseline=np.array([x['energy'] for x in rows if x['scenario']==scene and x['policy']=='fixed_050'])
            diff=values-baseline
            paired[scene][arm]={'mean_delta':float(diff.mean()),
                'seed_sd':float(diff.std(ddof=1)),'n_positive':int((diff>0).sum())}
    assert len(rows)==len(SEEDS)*len(SCENARIOS)*len(POLICIES)
    out={'status':'executed','seeds':SEEDS,'scenarios':SCENARIOS,
         'policies':POLICIES,'rows':rows,'summary':summary,'paired':paired,
         'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                           for f in ['garden.py','SOC_LONGITUDINAL_explore.py','SOC_LONGITUDINAL_stress.py']},
         'warning':'Posthoc fixed policies, fresh but synthetic seeds; finite horizon; the shock multiplies resources after noted ticks and does not alter the baseline laws otherwise.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'n':len(rows),'summary':summary,'paired':paired},indent=2))

if __name__=='__main__':main()
