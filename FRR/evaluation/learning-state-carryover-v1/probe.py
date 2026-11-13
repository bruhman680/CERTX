"""Exploratory optimizer-carrier factorial. Fresh objects, no checkpoint loads."""
from pathlib import Path
import sys, json, hashlib, copy, platform
import numpy as np

H=Path(__file__).resolve().parent
S=H.parent/'neural-garden-v01-intake-v1/learning/sources'
sys.path.insert(0,str(S))
from NEXT_WELFARE_garden import WelfareGarden

SEEDS=list(range(12400,12404))
SIZE=6
TRAIN=300
TEST=1000

def write(name,data):
    (H/name).write_text(json.dumps(data,indent=2)+'\n')

def arrhash(a):
    return hashlib.sha256(a.tobytes()).hexdigest()

def fingerprint(g):
    return {k:arrhash(getattr(g,k)) for k in ('resource','energy','theta')}

def metrics(g):
    return {'energy':float(g.energy.mean()),'resource':float(g.resource.mean()),
            'floor':float(np.mean(g.energy<=.01)),
            'baseline_rms':float(np.sqrt(np.mean(g.baseline**2))),
            'trace_rms':float(np.sqrt(np.mean(g.trace**2))),
            'theta_rms':float(np.sqrt(np.mean(g.theta**2)))}

def main():
    files=['garden.py','SOC_ENERGY_AWARE_policy.py','NEXT_WELFARE_garden.py']
    hashes={f:hashlib.sha256((S/f).read_bytes()).hexdigest() for f in files}
    plan={'date':'2026-11-13 America/Chicago','status':'exploratory new protocol, not published-cohort reproduction',
      'seeds':SEEDS,'size':SIZE,'train_steps':TRAIN,'test_steps':TEST,
      'physical_contexts':['fresh physical test world','trained physical continuation'],
      'factorial':'baseline retained/reset x trace retained/reset x online/frozen',
      'objective':'reserve_resource','penalty':.3,'regrowth':'.06 first/final thirds, .055 middle third',
      'primary_metric':'final mean energy; report every seed and contrast, no general-learning claim',
      'source_sha256':hashes,'model_inference':False,'canonical_mutation':False}
    write('PLAN.json',plan)
    rows=[]
    for seed in SEEDS:
        trained=WelfareGarden(seed=seed,size=SIZE,learning=True,objective='reserve_resource',penalty=.3)
        for _ in range(TRAIN): trained.step()
        fresh=WelfareGarden(seed=seed+20000,size=SIZE,learning=True,objective='reserve_resource',penalty=.3)
        fresh.theta=trained.theta.copy()
        for context,base in [('fresh',fresh),('continuation',trained)]:
            arms={}
            for baseline_keep in (False,True):
                for trace_keep in (False,True):
                    for online in (False,True):
                        label=f'b{int(baseline_keep)}t{int(trace_keep)}_'+('online' if online else 'frozen')
                        g=copy.deepcopy(base)
                        g.learning=online
                        g.baseline=trained.baseline.copy() if baseline_keep else np.zeros_like(trained.baseline)
                        g.trace=trained.trace.copy() if trace_keep else np.zeros_like(trained.trace)
                        arms[label]=g
            initial={label:fingerprint(g) for label,g in arms.items()}
            assert all(v==initial['b0t0_online'] for v in initial.values())
            initial_rng={label:json.dumps(g.rng_action.bit_generator.state,sort_keys=True) for label,g in arms.items()}
            assert len(set(initial_rng.values()))==1
            snapshots={}
            for t in range(1,TEST+1):
                for g in arms.values():
                    g.regrowth=.055 if TEST//3<t<=2*TEST//3 else .06
                    g.step()
                if t==1:
                    assert all(np.array_equal(g.last_action,arms['b0t0_online'].last_action) for g in arms.values())
                    assert all(np.array_equal(g.resource,arms['b0t0_online'].resource) for g in arms.values())
                    assert all(np.array_equal(g.energy,arms['b0t0_online'].energy) for g in arms.values())
                if t in (1,100,500,1000): snapshots[t]={label:metrics(g) for label,g in arms.items()}
            final_rng={label:json.dumps(g.rng_action.bit_generator.state,sort_keys=True) for label,g in arms.items()}
            assert len(set(final_rng.values()))==1
            frozen=[g for label,g in arms.items() if label.endswith('frozen')]
            assert all(fingerprint(g)==fingerprint(frozen[0]) for g in frozen)
            assert all(np.array_equal(g.theta,base.theta) for g in frozen)
            final={label:metrics(g) for label,g in arms.items()}
            contrasts={bt:final[bt+'_online']['energy']-final[bt+'_frozen']['energy'] for bt in ('b0t0','b0t1','b1t0','b1t1')}
            rows.append({'seed':seed,'context':context,'train_end':metrics(trained),
               'initial_physics_theta_hash':initial['b0t0_online'],'initial_rng_sha256':hashlib.sha256(initial_rng['b0t0_online'].encode()).hexdigest(),
               'matched_initial_physics_theta_rng':True,'matched_first_actions_physics':True,
               'matched_final_rng':True,'frozen_factorial_identical':True,
               'snapshots':snapshots,'final':final,'online_minus_frozen_energy':contrasts,
               'both_retained_minus_both_reset_online_energy':final['b1t1_online']['energy']-final['b0t0_online']['energy']})
            print(seed,context,contrasts,flush=True)
    summary={}
    for context in ('fresh','continuation'):
        rr=[r for r in rows if r['context']==context]
        summary[context]={'online_minus_frozen':{
            bt:{'mean_energy_delta':float(np.mean([r['online_minus_frozen_energy'][bt] for r in rr])),
                'seed_wins':sum(r['online_minus_frozen_energy'][bt]>0 for r in rr)}
            for bt in ('b0t0','b0t1','b1t0','b1t1')},
            'both_retained_minus_both_reset_online_energy_mean':float(np.mean([r['both_retained_minus_both_reset_online_energy'] for r in rr]))}
    assert hashes=={f:hashlib.sha256((S/f).read_bytes()).hexdigest() for f in files}
    write('RESULTS.json',{'plan':plan,'platform':{'python':platform.python_version(),'numpy':np.__version__},
         'rows':rows,'summary':summary,'source_unchanged':True,'test_worlds':64,'test_ticks':64000,'training_ticks':1200})

if __name__=='__main__': main()
