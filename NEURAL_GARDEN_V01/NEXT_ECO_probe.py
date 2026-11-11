"""Four falsifiable ecology mechanisms in the unchanged Neural Garden resource laws.

Each study is one conceptual research loop, not one loop per seed or tick.
Resource diffusion is deliberately altered ONLY in a separate labeled ablation.
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
SEEDS=list(range(9300,9308))
TICKS=8000
TAIL=1500


def neighbors(v,n):
    a=v.reshape(n,n)
    return ((np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1))/4).reshape(-1)


def actions(kind,r,e,n,ncount,rng,history):
    if kind=='rescue':return r>np.where(e<.12,.485,.51)
    if kind=='reverse':return r>np.where(e<.12,.535,.51)
    if kind=='neighbor_gradient':return r>(.51+.5*(neighbors(r,n)-r))
    if kind=='fixed50':return r>.50
    if kind in ('lag1','lag2'):
        lag=int(kind[-1])
        delayed=history[-lag] if len(history)>=lag else r
        return delayed>np.where(e<.12,.485,.51)
    if kind in ('lagcount1','lagcount2'):
        if ncount is None:raise ValueError('Matched delay targeting needs rescue counts')
        lag=int(kind[-1])
        delayed=history[-lag] if len(history)>=lag else r
        a=np.zeros(len(r),dtype=bool)
        if ncount:a[np.argpartition(delayed,-ncount)[-ncount:]]=True
        return a
    if ncount is None:raise ValueError('matched targeting needs counts')
    a=np.zeros(len(r),dtype=bool)
    if ncount:
        if kind=='top':a[np.argpartition(r,-ncount)[-ncount:]]=True
        elif kind=='bottom':a[np.argpartition(r,ncount-1)[:ncount]]=True
        elif kind=='shuffle':a[rng.choice(len(r),ncount,replace=False)]=True
        else:raise ValueError(kind)
    return a


def simulate(seed,kind,diffusion=.08,counts=None):
    g=Garden(seed=seed,size=16,learning=False)
    r=g.resource.copy(); e=g.energy.copy(); history=[]
    rng=np.random.default_rng(seed+2_019_011)
    trace=[]; action_counts=[]
    for t in range(TICKS):
        count=None if counts is None else counts[t]
        a=actions(kind,r,e,16,count,rng,history).astype(float)
        action_counts.append(int(a.sum()))
        p=float(a.mean())
        raw=.25*r*a-.03-.055*a+.008*(1-a)
        rr=np.clip(r+diffusion*(neighbors(r,16)-r)+.06*(1-r)-.18*r*a,0,1)
        ee=np.clip(e+raw,0,1)
        if t>=TICKS-TAIL:
            trace.append((float(ee.mean()),float((ee<=.01).mean()),
                float(np.mean(np.sort(ee)[:max(1,len(ee)//10)])),
                float(raw.mean()),p,float(r.mean()),float(np.mean(r*a)),
                float(np.mean(r*a)-r.mean()*p),float((ee>=.99).mean())))
        # Keep two past resource fields for controlled sensor-delay hypotheses.
        history.append(r)
        if len(history)>3:history.pop(0)
        r,e=rr,ee
    avg=np.asarray(trace).mean(axis=0)
    names=('tail_mean_energy','tail_floor','tail_bottom_decile','tail_raw_drift',
        'tail_harvest_rate','tail_resource','tail_resource_action',
        'tail_resource_action_cov','tail_ceiling')
    out={k:float(v) for k,v in zip(names,avg)}
    out.update(final_energy=float(e.mean()),final_floor=float((e<=.01).mean()),
        final_bottom_decile=float(np.mean(np.sort(e)[:max(1,len(e)//10)])),
        harvest_total=int(sum(action_counts)),
        mean_resource_per_harvest=float(avg[6]/avg[4]) if avg[4]>0 else None)
    return out,action_counts


def invariant():
    standard=ThresholdGarden(seed=9911,size=16,threshold=.5)
    g=Garden(seed=9911,size=16,learning=False)
    for _ in range(120):
        standard.step()
        r=g.resource.copy();e=g.energy.copy();a=(r>.50).astype(float)
        g.resource=np.clip(r+.08*(g._neighbors(r)-r)+.06*(1-r)-.18*r*a,0,1)
        g.energy=np.clip(e+.25*r*a-.03-.055*a+.008*(1-a),0,1)
    assert np.allclose(standard.energy,g.energy,rtol=0,atol=1e-12)
    assert np.allclose(standard.resource,g.resource,rtol=0,atol=1e-12)


def run():
    invariant()
    studies={
        'targeting_exact_counts':{'question':'Does harvest location matter at exactly equal per-tick harvest counts?',
            'regimes':[('rescue',.08),('top',.08),('bottom',.08),('shuffle',.08)]},
        'spatial_diffusion':{'question':'Does spatial exchange interact with state-targeted harvesting?',
            'regimes':[('rescue',.08),('top',.08),('rescue',0.),('top',0.)]},
        'observation_delay':{'question':'Does delayed sensing of resource alter phase and energy retention?',
            'regimes':[('rescue',.08),('lag1',.08),('lag2',.08)]},
        'delay_exact_counts':{'question':'Does outdated resource targeting harm energy even when per-tick action count is held fixed?',
            'regimes':[('rescue',.08),('top',.08),('lagcount1',.08),('lagcount2',.08)]},
        'energy_equity':{'question':'Do policies maximizing mean energy also preserve lower-tail cells?',
            'regimes':[('rescue',.08),('reverse',.08),('neighbor_gradient',.08),('fixed50',.08)]},
    }
    rows=[];summaries={}; contrasts={}
    for title,study in studies.items():
        these=[]
        for seed in SEEDS:
            ref,counts=simulate(seed,'rescue',.08)
            for kind,diff in study['regimes']:
                if kind=='rescue' and diff==.08:
                    obs=dict(ref); used=counts
                else:
                    obs,used=simulate(seed,kind,diff,counts if kind in ('top','bottom','shuffle','lagcount1','lagcount2') else None)
                if kind in ('top','bottom','shuffle','lagcount1','lagcount2'):
                    assert used==counts, (kind,seed,'count mismatch')
                row={'study':title,'seed':seed,'policy':kind,
                    'diffusion':diff,'world_law_changed':diff!=.08,**obs}
                rows.append(row);these.append(row)
        labels=sorted({(r['policy'],r['diffusion']) for r in these})
        summaries[title]={}
        for label in labels:
            sub=[r for r in these if (r['policy'],r['diffusion'])==label]
            summaries[title][f'{label[0]}__diff{label[1]:.2f}']={
                k:float(np.mean([r[k] for r in sub])) for k in
                ['final_energy','final_floor','final_bottom_decile',
                 'tail_raw_drift','tail_harvest_rate','tail_resource_action_cov',
                 'mean_resource_per_harvest','tail_ceiling']}
        base=np.array([r['final_energy'] for r in these if r['policy']=='rescue' and r['diffusion']==.08])
        contrasts[title]={}
        for label in labels:
            if label==('rescue',.08):continue
            sub=np.array([r['final_energy'] for r in these if (r['policy'],r['diffusion'])==label])
            if len(base)!=len(sub):raise AssertionError('misaligned seeds')
            d=base-sub
            contrasts[title][str(label)]={'rescue_minus_other':float(d.mean()),
                'rescue_wins':int((d>0).sum()),'n':len(d)}
    return {'status':'completed','design':studies,
        'actual_substantive_loops':len(studies),'seeds':SEEDS,'ticks':TICKS,
        'tail':TAIL,'row_count':len(rows),'rows':rows,'summaries':summaries,
        'paired_contrasts':contrasts,
        'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
            for f in ['garden.py','threshold_policy.py',Path(__file__).name]},
        'versions':{'python':platform.python_version(),'numpy':np.__version__},
        'limitations':['Only eight synthetic matched seeds per conceptual study',
            'Policies hand-coded; not evidence of neural adaptation',
            'Ablation diffusion=0 is changed physics',
            'Hypothesis family informed by prior exploratory Garden results',
            'Clipping may conceal negative energy budget; tail raw drift tracked',
            'Finite 8000 ticks cannot establish indefinite sustainability']}


if __name__=='__main__':
    result=run()
    out=ROOT/'NEXT_ECO_results.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print('Wrote',out,'with',result['row_count'],'rows')
    print(json.dumps(result['summaries'],indent=2))
