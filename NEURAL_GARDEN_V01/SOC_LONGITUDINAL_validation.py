"""Held-out, matched-seed checks for exploratory living-world policy hypotheses.

Do not treat these seeds as separate research loops; validation is one new
scientific decision after the sequential single-world search.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

from garden import Garden
from SOC_LONGITUDINAL_explore import PolicyFork,run

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'SOC_LONGITUDINAL_validation.json'
SEEDS=list(range(20_300,20_324))
POLICIES={
 'fixed_050':{'kind':'fixed','theta':.5},
 'fixed_051':{'kind':'fixed','theta':.51},
 'fixed_0515':{'kind':'fixed','theta':.515},
 'energy_rescue':{'kind':'energy_rescue','theta':.51,'low_energy':.12,'discount':.025},
 'neighbor_gradient':{'kind':'neighbor','theta':.51,'coupling':.5},
}

def main():
    records=[]
    for seed in SEEDS:
        anchor=Garden(seed=seed,size=16,learning=False)
        initial=anchor.fingerprint()
        for name,policy in POLICIES.items():
            out=run(anchor,policy,horizon=10_000)
            records.append({'seed':seed,'arm':name,'config':policy,
                            'initial_fingerprint':initial,
                            'final':{k:out[k] for k in ('energy','resource','floor','upper','raw_tail','mean_energy_tail')},
                            'trajectory':out['points']})
    s={}
    for arm in POLICIES:
        rows=[r['final'] for r in records if r['arm']==arm]
        s[arm]={k:float(np.mean([x[k] for x in rows])) for k in rows[0]}
    rescue=np.array([r['final']['energy'] for r in records if r['arm']=='energy_rescue'])
    paired={}
    for arm in POLICIES:
        vals=np.array([r['final']['energy'] for r in records if r['arm']==arm])
        delta=rescue-vals
        paired[arm]={'mean_delta_energy_rescue_minus':float(delta.mean()),
                     'n_better':int((delta>0).sum()),
                     'n_equal':int(np.isclose(delta,0).sum()),
                     'seed_sd':float(delta.std(ddof=1))}
    assert len(records)==len(SEEDS)*len(POLICIES)
    result={'status':'executed','description':'heldout_matched_seed_validation',
            'seeds':SEEDS,'steps':10_000,'size':16,
            'policies':POLICIES,'summary':s,'paired':paired,'run_rows':records,
            'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                 for f in ['garden.py','SOC_LONGITUDINAL_explore.py','SOC_LONGITUDINAL_validation.py']},
            'warning':'Selected policies were posthoc from a single historical world; this is synthetic held-out seed evaluation, not an independent pre-registered discovery or proof of indefinite viability.'}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'n_runs':len(records),'summary':{k:round(v['energy'],5) for k,v in s.items()},
        'rescue_vs_fixed050':paired['fixed_050'], 'rescue_vs_fixed051':paired['fixed_051']},indent=2))

if __name__=='__main__':main()
