"""Exact-state paired historical recovery policy switches."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from datetime import datetime,timezone

import numpy as np
from garden import Garden
from SEASONS2_probe import neighbor, summer

ROOT=Path(__file__).resolve().parent
SEEDS=tuple(range(41140,41152))
FORKS=(3000,9000)

def step(r,e,rg,reverse):
    t=np.where(e<.12,.535,.51) if reverse else .51
    a=(r>t).astype(float)
    nr=np.clip(r+.08*(neighbor(r)-r)+rg*(1.-r)-.18*r*a,0.,1.)
    ne=np.clip(e+.25*r*a-.03-.055*a+.008*(1.-a),0.,1.)
    return nr,ne,a

def one(seed,fork):
    g=Garden(seed=seed,size=16,learning=False)
    r,e=g.resource.copy(),g.energy.copy()
    for tick in range(1,fork+1):r,e,_=step(r,e,.06 if summer(tick) else .048,False)
    parent={'energy':float(e.mean()),'floor':float(np.mean(e<=.01))}
    out={}
    for name,rev in [('fixed',False),('reverse',True)]:
        rr,ee=r.copy(),e.copy()
        action_switches=0
        for t in range(1,3001):
            aa=(rr>.51)
            bb=(rr>np.where(ee<.12,.535,.51))
            action_switches+=int(np.sum(aa!=bb))
            rr,ee,_=step(rr,ee,.06,rev)
        out[name]={'energy':float(ee.mean()),'resource':float(rr.mean()),
                   'floor':float(np.mean(ee<=.01)),'branch_activation_rate':action_switches/(3000*256)}
    return {'seed':seed,'fork_tick':fork,'parent':parent,'outcome':out}

def main():
    rows=[one(s,t) for s in SEEDS for t in FORKS]
    summary={}
    for t in FORKS:
        z=[x for x in rows if x['fork_tick']==t]
        diffs=[x['outcome']['reverse']['energy']-x['outcome']['fixed']['energy'] for x in z]
        summary[str(t)]={'mean_delta_reverse_minus_fixed':float(np.mean(diffs)),
            'reverse_wins':sum(d>0 for d in diffs),
            'paired_energy_deltas':diffs,
            'mean_parent_energy':float(np.mean([x['parent']['energy'] for x in z])),
            'mean_fixed_energy':float(np.mean([x['outcome']['fixed']['energy'] for x in z])),
            'mean_reverse_energy':float(np.mean([x['outcome']['reverse']['energy'] for x in z])),
            'mean_fixed_floor':float(np.mean([x['outcome']['fixed']['floor'] for x in z])),
            'mean_reverse_floor':float(np.mean([x['outcome']['reverse']['floor'] for x in z])),
            'mean_reverse_branch_activation_rate':float(np.mean([x['outcome']['reverse']['branch_activation_rate'] for x in z]))}
    hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('garden.py','SEASONS2_SWITCH_PLAN.md','SEASONS2_SWITCH_probe.py')}
    d={'created_utc':datetime.now(timezone.utc).isoformat(),'design':{'seeds':SEEDS,'fork_ticks':FORKS,'post_fork_ticks':3000},'source_sha256':hashes,'summary':summary,'rows':rows}
    (ROOT/'SEASONS2_SWITCH_results.json').write_text(json.dumps(d,indent=2)+'\n')

if __name__=='__main__':main()
