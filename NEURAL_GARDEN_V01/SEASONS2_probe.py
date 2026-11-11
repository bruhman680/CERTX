"""Frozen seasonal longitudinal probe. Read SEASONS2_PLAN.md before editing."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

import numpy as np

from garden import Garden

HERE = Path(__file__).resolve().parent
SEEDS = tuple(range(41100, 41112))
POLICIES = ('fixed', 'reverse', 'early', 'late', 'reactive', 'oracle')
BOUNDARIES = (1500, 3000, 4500, 6000, 7500, 9000, 12000)


def neighbor(v):
    z=v.reshape(16,16)
    return ((np.roll(z, 1, 0)+np.roll(z, -1, 0)+np.roll(z, 1, 1)+np.roll(z, -1, 1))/4).reshape(-1)


def summer(tick):
    return tick <= 1500 or 3001 <= tick <= 4500 or 6001 <= tick <= 7500 or tick >= 9001


def simulate(seed, policy):
    initial=Garden(seed=seed,size=16,learning=False)
    resource=initial.resource.copy()
    energy=initial.energy.copy()
    activated=False
    activated_at=None
    points=[]
    harvests=0
    for t in range(1, 12001):
        is_summer=summer(t)
        if policy == 'fixed': reverse=False
        elif policy == 'reverse': reverse=True
        elif policy == 'early': reverse=(t >= 1400)
        elif policy == 'late': reverse=(t >= 5500)
        elif policy == 'oracle': reverse=not is_summer
        elif policy == 'reactive':
            if not activated and float(np.mean(energy <= .01)) > .10:
                activated=True
                activated_at=t
            reverse=activated
        else: raise ValueError(policy)
        thresh=np.where(energy < .12, .535, .51) if reverse else .51
        action=(resource > thresh).astype(float)
        harvests+=int(np.sum(action))
        rg=.06 if is_summer else .048
        resource_new=np.clip(resource+.08*(neighbor(resource)-resource)+rg*(1.-resource)-.18*resource*action,0.,1.)
        energy=np.clip(energy+.25*resource*action-.03-.055*action+.008*(1.-action),0.,1.)
        resource=resource_new
        if t in BOUNDARIES:
            points.append({'tick':t,'mean_energy':float(energy.mean()),
                'mean_resource':float(resource.mean()),'floor_frac':float(np.mean(energy <= .01)),
                'lower_decile':float(np.quantile(energy,.10)),
                'cumulative_harvest_rate':float(harvests/(256*t)),
                'summer':is_summer})
    return {'seed':seed,'policy':policy,'reactive_switch_tick':activated_at,'points':points}


def main():
    rows=[]
    for seed in SEEDS:
        for policy in POLICIES:
            rows.append(simulate(seed,policy))
        print('seasonal seed',seed,'complete',flush=True)
    summary={}
    for t in BOUNDARIES:
        summary[str(t)]={}
        for p in POLICIES:
            pts=[x for r in rows if r['policy']==p for x in r['points'] if x['tick']==t]
            summary[str(t)][p]={k:float(np.mean([x[k] for x in pts])) for k in
                ('mean_energy','mean_resource','floor_frac','lower_decile','cumulative_harvest_rate')}
    pairs={}
    for p in POLICIES:
        if p=='fixed':continue
        diffs=[]
        for s in SEEDS:
            a=next(r for r in rows if r['seed']==s and r['policy']==p)['points'][-1]['mean_energy']
            b=next(r for r in rows if r['seed']==s and r['policy']=='fixed')['points'][-1]['mean_energy']
            diffs.append(float(a-b))
        pairs[p]={'mean_delta':float(np.mean(diffs)),'wins':sum(d>0 for d in diffs), 'deltas':diffs}
    source={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in
            ('SEASONS2_PLAN.md','SEASONS2_probe.py','garden.py')}
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':source,
        'design':{'seeds':SEEDS,'policies':POLICIES,'boundaries':BOUNDARIES,'ticks':12000,
                  'distinct_persistent_trajectories':len(rows)},
        'summary':summary,'paired_vs_fixed_at_12000':pairs,'rows':rows,
        'caveats':['predeclared manual and oracle policies, no neural online learning',
                   'identical initial states per seed, divergent trajectories thereafter',
                   'season schedule deterministic and repeated; seed not season is replication unit',
                   'finite 12000 ticks do not show indefinite adaptation']}
    (HERE/'SEASONS2_results.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__': main()
