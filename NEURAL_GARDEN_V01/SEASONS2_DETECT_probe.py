"""Blind seasonal inference from local synthetic observations."""
from __future__ import annotations
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from garden import Garden
from SEASONS2_probe import neighbor

ROOT=Path(__file__).resolve().parent
SEEDS=tuple(range(41160,41172))
NOISE=(0.,.01,.03)
METHODS=('residual_0','residual_001','residual_003','resource_naive','parity_sham')
SWITCHES=(1501,3001,4501)
TICKS=6000

def summer(t): return t<=1500 or 3001<=t<=4500

def one(seed):
    g=Garden(seed=seed,size=16,learning=False)
    r=g.resource.copy()
    rng=np.random.default_rng(seed+500000)
    state={noise:{'ema':np.full(256,.06), 'accuracy':[], 'correctness':[]} for noise in NOISE}
    result={k:{'accurate':0,'total':0,'transition_accurate':0,'transition_total':0,'majority_correct':[]} for k in METHODS}
    def record(key,label,t,true_summer):
        q=result[key]
        q['accurate']+=int(label.sum()) if true_summer else int((~label).sum())
        q['total']+=256
        if any(sw<=t<sw+250 for sw in SWITCHES):
            q['transition_accurate']+=int(label.sum()) if true_summer else int((~label).sum())
            q['transition_total']+=256
        q['majority_correct'].append(float(label.mean() if true_summer else (~label).mean())>.60)
    for t in range(1,TICKS+1):
        true_summer=summer(t)
        a=(r>.51).astype(float)
        next_r=np.clip(r+.08*(neighbor(r)-r)+(.06 if true_summer else .048)*(1.-r)-.18*r*a,0.,1.)
        if t>=100:
            record('resource_naive',r>.48,t,true_summer)
            record('parity_sham',np.full(256,((t-1)//1000)%2==0,dtype=bool),t,true_summer)
        for noise in NOISE:
            observed_prev=np.clip(r+rng.normal(0.,noise,256),0.,1.) if noise else r
            observed_next=np.clip(next_r+rng.normal(0.,noise,256),0.,1.) if noise else next_r
            ng=neighbor(observed_prev)
            # Conditional model inversion only. Environmental coefficients are known.
            residual=(observed_next-observed_prev-.08*(ng-observed_prev)+.18*observed_prev*a)/np.maximum(.08,1.-observed_prev)
            obj=state[noise]
            obj['ema']=.98*obj['ema']+.02*residual
            if t>=100:
                key={0.:'residual_0',.01:'residual_001',.03:'residual_003'}[noise]
                record(key,obj['ema']>.054,t,true_summer)
        r=next_r
    out={}
    for k,counts in result.items():
        out[k]={'accuracy':counts['accurate']/counts['total'],
                'transition_accuracy':counts['transition_accurate']/counts['transition_total']}
        for change in SWITCHES:
            # Logs began at tick 100; list index 0 corresponds to tick 100.
            lo=change-100
            majority=counts['majority_correct']
            delay=next((d for d in range(0,251) if all(majority[lo+d:lo+d+10])),None)
            out[k][f'delay_after_{change}']=delay
    return {'seed':seed,'metrics':out}

def main():
    rows=[one(s) for s in SEEDS]
    summary={}
    for k in METHODS:
        summary[k]={'accuracy':float(np.mean([r['metrics'][k]['accuracy'] for r in rows])),
            'transition_accuracy':float(np.mean([r['metrics'][k]['transition_accuracy'] for r in rows])),
            'per_seed_accuracy':[r['metrics'][k]['accuracy'] for r in rows]}
        for change in SWITCHES:
            vals=[r['metrics'][k][f'delay_after_{change}'] for r in rows]
            summary[k][f'delay_after_{change}']={'detected':sum(x is not None for x in vals),
               'median_detected_delay':float(np.median([x for x in vals if x is not None])) if any(x is not None for x in vals) else None}
    names=('garden.py','SEASONS2_DETECT_PLAN.md','SEASONS2_DETECT_probe.py')
    obj={'created_utc':datetime.now(timezone.utc).isoformat(),
         'source_sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
         'design':{'seeds':SEEDS,'ticks':TICKS,'noise':NOISE,'methods':METHODS,'switches':SWITCHES},
         'summary':summary,'rows':rows,
         'limitations':['Exact physical model coefficients are privileged knowledge, not learned.',
                        'No learned policy or effect of inferred labels tested.',
                        'Local noisy resources can be below/above clipping bounds; finite sample only.',
                        'Sham parity deliberately misaligned to the season schedule.']}
    (ROOT/'SEASONS2_DETECT_results.json').write_text(json.dumps(obj,indent=2)+'\n')

if __name__=='__main__':main()
