"""Bounded independent physics checks; never reads or writes a live garden."""
from pathlib import Path
import hashlib, importlib.util, json, math, platform
import numpy as np

H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reviewed_neural_garden',H/'sources/garden.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
Garden=module.Garden

def main():
    residuals={'energy':0.,'resource':0.,'covariance':0.,'diffusion_sum':0.}
    rows=[]
    for seed in [12001,12017,12029,12043]:
        for learning in [False,True]:
            g=Garden(seed=seed,size=8,learning=learning)
            initial={k:getattr(g,k).copy() for k in ['win','wrec','bhidden','wpred','bpred','wact','bact']}
            tail=[]
            for t in range(300):
                r,e=g.resource.copy(),g.energy.copy()
                diffusion=.08*(g._neighbors(r)-r)
                residuals['diffusion_sum']=max(residuals['diffusion_sum'],abs(float(diffusion.sum())))
                g.step();a=g.last_action
                raw=.25*r*a-.063*a-.022
                z=e+raw
                floor=np.maximum(0.,-z).mean();ceiling=np.maximum(0.,z-1.).mean()
                energy=float((g.energy-e).mean())
                resource=float((g.resource-r).mean())
                p=float(a.mean());ra=float((r*a).mean());cov=ra-float(r.mean())*p
                residuals['energy']=max(residuals['energy'],abs(energy-float(raw.mean()+floor-ceiling)))
                residuals['resource']=max(residuals['resource'],abs(resource-(.06*(1-float(r.mean()))-.18*ra)))
                residuals['covariance']=max(residuals['covariance'],abs(float(raw.mean())-(.25*(float(r.mean())*p+cov)-.063*p-.022)))
                assert np.all((g.resource>=0)&(g.resource<=1)) and np.all((g.energy>=0)&(g.energy<=1))
                if t>=250:tail.append({'raw':float(raw.mean()),'actual':energy,'floor_correction':float(floor),'ceiling_correction':float(ceiling)})
            changed={k:not np.array_equal(v,getattr(g,k)) for k,v in initial.items()}
            assert learning or not any(changed.values())
            rows.append({'seed':seed,'learning':learning,'ticks':300,'mean_energy':float(g.energy.mean()),
                'mean_resource':float(g.resource.mean()),'changed_tensors':changed,
                'last50':{k:float(np.mean([r[k] for r in tail])) for k in tail[0]}})
    assert max(residuals.values())<1e-12
    pstar=(math.sqrt(.0009/.063)-.06)/.18
    drift=lambda p:.015*p/(.06+.18*p)-.063*p-.022
    opt={'p':pstar,'resource':.06/(.06+.18*pstar),'max_raw_drift':drift(pstar),
        'scope':'Homogeneous stationary constant-rate mean-field approximation, not all policies.'}
    assert opt['max_raw_drift']<0
    # Independent matched-count dynamics. Each seed starts identical; only the
    # shuffled arm's assignment receives the reference action-count schedule.
    targeting=[]
    for seed in [12101,12117,12129,12143]:
        ref=Garden(seed=seed,size=8,learning=False)
        shuffled=Garden(seed=seed,size=8,learning=False)
        rng=np.random.default_rng(seed+900000)
        counts_equal=True
        for t in range(2000):
            r=ref.resource.copy();e=ref.energy.copy()
            a=(r>np.where(e<.12,.485,.51)).astype(float)
            count=int(a.sum())
            rs=shuffled.resource.copy();es=shuffled.energy.copy()
            sa=np.zeros(shuffled.count);sa[rng.permutation(shuffled.count)[:count]]=1
            counts_equal=counts_equal and int(sa.sum())==count
            for g,before_r,before_e,acts in [(ref,r,e,a),(shuffled,rs,es,sa)]:
                g.resource=np.clip(before_r+.08*(g._neighbors(before_r)-before_r)+.06*(1-before_r)-.18*before_r*acts,0,1)
                g.energy=np.clip(before_e+.25*before_r*acts-.063*acts-.022,0,1)
            assert counts_equal
        targeting.append({'seed':seed,'ticks':2000,'size':8,'count_matched_every_tick':counts_equal,
            'targeted_energy':float(ref.energy.mean()),'shuffled_energy':float(shuffled.energy.mean()),
            'difference':float(ref.energy.mean()-shuffled.energy.mean())})
    result={'status':'pass','date_local':'2026-11-12 America/Chicago','source_commit':'3204c81ebc6922d66b0ae2623ee83d629f11f3b8',
        'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (H/'sources').iterdir() if p.is_file()},
        'python':platform.python_version(),'numpy':np.__version__,'identity_max_abs_residuals':residuals,
        'base_neural_runs':rows,'mean_field_optimum':opt,'new_matched_count_runs':targeting,
        'scope':'Independent bounded mathematical/physics reproduction on new seeds and smaller worlds. Not rerunning published72runs or THEORY2 WelfareGarden experiment. No foreign checkpoint, live state, pretrained LM or canonical garden accessed.'}
    with (H/'RESULTS.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps({'status':'pass','residuals':residuals,'optimum':opt,'targeting':targeting}))

if __name__=='__main__':main()
