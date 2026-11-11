"""Probe timing distributions in the near-neutral .50 resource threshold."""
import json
import hashlib
from collections import Counter
from pathlib import Path
import numpy as np
from DYNAMICS_diffusion import DiffusionGarden

ROOT=Path(__file__).resolve().parent

def run_one(seed,diff):
    g=DiffusionGarden(seed,diff)
    last=np.full(g.count,-1,dtype=int)
    intervals=Counter()
    actions=0
    resources_at_action=0.
    resource_sum=0.
    n=0
    for t in range(5000):
        r=g.resource.copy()
        a=(r>.5)
        if t>=3000:
            idx=np.nonzero(a)[0]
            for i in idx:
                if last[i]>=0:
                    intervals[int(t-last[i])]+=1
                last[i]=t
            actions+=len(idx)
            resources_at_action+=float(r[a].sum())
            resource_sum+=float(r.sum())
            n+=g.count
        g.step()
    return {'seed':seed,'diffusion':diff,'interval_counts':dict(intervals),
            'mean_resource_at_harvest':resources_at_action/actions,
            'harvest_fraction':actions/n,
            'mean_resource':resource_sum/n}

def run():
    rows=[run_one(seed,diff) for diff in (0.,.08) for seed in range(995,1003)]
    summary={}
    for diff in (0.,.08):
        subset=[r for r in rows if r['diffusion']==diff]
        c=Counter()
        for row in subset:c.update({int(k):v for k,v in row['interval_counts'].items()})
        summary[str(diff)]={'mean_resource_at_harvest':float(np.mean([r['mean_resource_at_harvest'] for r in subset])),
                            'mean_harvest_fraction':float(np.mean([r['harvest_fraction'] for r in subset])),
                            'mean_resource':float(np.mean([r['mean_resource'] for r in subset])),
                            'interval_frequency':{str(k):v/sum(c.values()) for k,v in sorted(c.items())}}
    data={'design':'posthoc phase and action interval diagnostic; 8 fresh seeds per diffusion coefficient; original .5 threshold',
          'rows':rows,'summary':summary,'seeds':list(range(995,1003)), 'tail':2000,'ticks':5000,
          'source_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
                            ('garden.py','threshold_policy.py','DYNAMICS_diffusion.py','DYNAMICS_phase.py')}}
    (ROOT/'DYNAMICS_phase_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()
