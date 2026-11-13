"""Test energy-aware rescue and spatial-gradient harvesting vs matched-count control.

The count-matched shuffled comparator receives exactly the rescue reference's
number of harvest actions at EACH tick, but scatters those actions uniformly
over cells, erasing local resource/energy targeting. World laws are original.
This separates amount of harvesting from its spatiotemporal selection.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from garden import Garden
from threshold_policy import ThresholdGarden

ROOT=Path(__file__).resolve().parent
SEEDS=list(range(5800,5812))
TICKS=10000
TAIL=2500
POLICIES=("rescue", "fixed_051", "fixed_050", "fixed_0485", "neighbor_gradient", "count_shuffled")


def run_one(seed,policy,counts=None):
    g=Garden(seed=seed,size=16,learning=False)
    rng=np.random.default_rng(seed+900000)
    records=[]
    cnt=[]
    for t in range(TICKS):
        r=g.resource.copy();e=g.energy.copy()
        if policy=="rescue":
            threshold=np.where(e<.12,.485,.51)
            action=r>threshold
        elif policy=="neighbor_gradient":
            threshold=.51+.5*(g._neighbors(r)-r)
            action=r>threshold
        elif policy=="count_shuffled":
            if counts is None:raise ValueError('Shuffled control requires rescue action counts')
            n=int(counts[t]);action=np.zeros(g.count,dtype=bool)
            action[rng.permutation(g.count)[:n]]=True
        else:
            threshold={"fixed_051":.51,"fixed_050":.50,"fixed_0485":.485}[policy]
            action=r>threshold
        a=action.astype(float)
        cnt.append(int(a.sum()))
        raw=.25*r*a-.03-.055*a+.008*(1-a)
        next_resource=np.clip(r+.08*(g._neighbors(r)-r)+.06*(1-r)-.18*r*a,0,1)
        g.energy=np.clip(e+raw,0,1)
        g.resource=next_resource
        g.tick+=1
        if t>=TICKS-TAIL:
            p=float(a.mean());r_bar=float(r.mean());e_bar=float(e.mean())
            records.append({
                'raw_drift':float(raw.mean()),
                'harvest':p,
                'resource':r_bar,
                'energy':e_bar,
                'resource_action_cov':float((r*a).mean()-r_bar*p),
                'energy_action_cov':float((e*a).mean()-e_bar*p),
                'resource_action':float((r*a).mean()),
                'floor':float((g.energy<=.01).mean()),
            })
    means={k:float(np.mean([x[k] for x in records])) for k in records[0]}
    # Pool across all harvest events: averaging per-tick ratios would bias
    # the estimate down when some ticks contain no harvests.
    means['resource_yield_per_harvest']=float(means['resource_action']/means['harvest'])
    means.update({'energy_final':float(g.energy.mean()),
                  'floor_final':float((g.energy<=.01).mean()),
                  'ceiling_final':float((g.energy>=.99).mean()),
                  'resource_final':float(g.resource.mean())})
    return means, cnt


def invariant():
    g=ThresholdGarden(seed=9911,threshold=.51)
    q=Garden(seed=9911,learning=False)
    for _ in range(100):
        g.step();r=q.resource.copy();a=(r>.51).astype(float)
        q.energy=np.clip(q.energy+.25*r*a-.03-.055*a+.008*(1-a),0,1)
        q.resource=np.clip(r+.08*(q._neighbors(r)-r)+.06*(1-r)-.18*r*a,0,1)
    assert np.allclose(g.energy,q.energy,rtol=0,atol=1e-12)
    assert np.allclose(g.resource,q.resource,rtol=0,atol=1e-12)


def main():
    invariant()
    rows=[]
    for seed in SEEDS:
        reference, counts=run_one(seed,"rescue")
        rows.append({'seed':seed,'policy':'rescue',**reference})
        for p in POLICIES[1:]:
            outcome,used=run_one(seed,p, counts if p=='count_shuffled' else None)
            if p=='count_shuffled' and used!=counts:
                raise AssertionError('Matched-count comparator did not preserve harvest counts')
            rows.append({'seed':seed,'policy':p,**outcome})
    summary={}
    for p in POLICIES:
        selection=[r for r in rows if r['policy']==p]
        summary[p]={k:float(np.mean([r[k] for r in selection])) for k in
                    ['energy_final','floor_final','ceiling_final','resource_final',
                     'raw_drift','harvest','resource_action_cov','energy_action_cov',
                     'resource_yield_per_harvest','floor']}
    contrasts={}
    for p in POLICIES[1:]:
        a=np.array([r['energy_final'] for r in rows if r['policy']=='rescue'])
        b=np.array([r['energy_final'] for r in rows if r['policy']==p])
        d=a-b
        contrasts[p]={
            'mean_rescue_minus_comparator':float(d.mean()),
            'paired_sd':float(d.std(ddof=1)),
            'rescue_wins':int((d>0).sum()),
            'n':len(d),
        }
    result={
        'status':'completed','design':'Original-laws matched-seed resource/energy targeting vs same-count random location control',
        'seeds':SEEDS,'ticks':TICKS,'tail_ticks':TAIL,
        'policies':POLICIES,'total_runs':len(rows),
        'rows':rows,'summary':summary,'paired_contrasts':contrasts,
        'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
                         for f in ['garden.py','threshold_policy.py','SOC_PHYSICS_targeting.py']},
        'python_version':platform.python_version(),'numpy_version':np.__version__,
        'caveat':'Posthoc policy family; matched-count shuffled arm uses an external per-tick count trajectory from rescue in the same seed. This is an intentionally synthetic counterfactual, not an independent learnable agent.'
    }
    (ROOT/'SOC_PHYSICS_targeting_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'summary':summary,'contrasts':contrasts},indent=2))


if __name__=='__main__':main()
