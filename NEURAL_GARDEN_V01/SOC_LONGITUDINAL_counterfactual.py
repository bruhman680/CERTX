"""Adversarial control: is the rescue policy merely a fixed lower threshold?"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_LONGITUDINAL_explore import run

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'SOC_LONGITUDINAL_counterfactual_results.json'
SEEDS=list(range(20800,20816))
FIXED=[.48,.485,.49,.495,.50,.505,.51]
POLICIES={f'fixed_{x:g}':{'kind':'fixed','theta':x} for x in FIXED}
POLICIES['energy_rescue']={'kind':'energy_rescue','theta':.51,'low_energy':.12,'discount':.025}

def main():
    rows=[]
    for seed in SEEDS:
        anchor=Garden(seed=seed,size=16,learning=False)
        for arm,policy in POLICIES.items():
            measure=run(anchor,policy,horizon=20_000)
            rows.append({'seed':seed,'arm':arm,
                'energy':measure['energy'],'floor':measure['floor'],
                'raw_tail':measure['raw_tail']})
    by_arm={}
    for arm in POLICIES:
        d=[r for r in rows if r['arm']==arm]
        by_arm[arm]={k:float(np.mean([x[k] for x in d])) for k in ['energy','floor','raw_tail']}
    rescue=np.array([r['energy'] for r in rows if r['arm']=='energy_rescue'])
    contrast={}
    for arm in POLICIES:
        values=np.array([r['energy'] for r in rows if r['arm']==arm])
        diff=rescue-values
        contrast[arm]={'mean_delta':float(diff.mean()),'seed_sd':float(diff.std(ddof=1)),
                       'n_rescue_better':int((diff>0).sum())}
    out={'status':'executed','n_runs':len(rows),'horizon':20_000,'seeds':SEEDS,
       'policies':POLICIES,'by_arm':by_arm,'rescue_contrast':contrast,'rows':rows,
       'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                           for f in ['garden.py','SOC_LONGITUDINAL_explore.py','SOC_LONGITUDINAL_counterfactual.py']},
       'warning':'Posthoc fixed threshold candidates after same-world exploration. This cannot establish optimality or broad external validity.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'energy':{k:round(v['energy'],5) for k,v in by_arm.items()},
                      'contrasts':contrast},indent=2))

if __name__=='__main__':main()
