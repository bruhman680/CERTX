"""Independent read-only, predeclared ecological stress replication."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_study import train, WelfareGarden

HERE=Path(__file__).resolve().parent
SEEDS=range(11000,11008)
REGROWTHS=(.03,.06,.08)


def one(seed, regrowth, ticks=3000, size=10):
    theta=train('reserve_resource', seed, size, 1000)
    probe_seed=seed+50000
    a=WelfareGarden(seed=probe_seed,size=size,learning=True, objective='reserve_resource', penalty=.3,regrowth=regrowth)
    b=WelfareGarden(seed=probe_seed,size=size,learning=False, objective='reserve_resource', penalty=.3,regrowth=regrowth)
    a.theta=theta.copy();b.theta=theta.copy()
    assert np.array_equal(a.energy,b.energy) and np.array_equal(a.resource,b.resource)
    assert json.dumps(a.rng_action.bit_generator.state,sort_keys=True)==json.dumps(b.rng_action.bit_generator.state,sort_keys=True)
    auc_a=auc_b=0.; floor_a=floor_b=0.; raw_a=[];raw_b=[]
    for t in range(ticks):
        a.step();b.step()
        auc_a+=float(a.energy.mean())/ticks;auc_b+=float(b.energy.mean())/ticks
        floor_a+=float(np.mean(a.energy<=.01))/ticks;floor_b+=float(np.mean(b.energy<=.01))/ticks
        if t>=ticks-500:
            raw_a.append(float(a.last_raw.mean()));raw_b.append(float(b.last_raw.mean()))
    return dict(seed=seed,regrowth=regrowth,
                online=dict(energy=float(a.energy.mean()),auc=auc_a,mean_floor=floor_a,final_floor=float(np.mean(a.energy<=.01)),raw_tail=float(np.mean(raw_a)),harvest=float(a.last_action.mean()),resource=float(a.resource.mean())),
                frozen=dict(energy=float(b.energy.mean()),auc=auc_b,mean_floor=floor_b,final_floor=float(np.mean(b.energy<=.01)),raw_tail=float(np.mean(raw_b)),harvest=float(b.last_action.mean()),resource=float(b.resource.mean())),
                delta_energy=float(a.energy.mean()-b.energy.mean()),delta_auc=auc_a-auc_b,
                max_theta_distance=float(np.max(np.abs(a.theta-b.theta))))


def main():
    rows=[one(s,r) for r in REGROWTHS for s in SEEDS]
    summary={}
    for r in REGROWTHS:
        a=[x for x in rows if x['regrowth']==r]
        summary[str(r)]={key:{'online':float(np.mean([x['online'][key] for x in a])),
                              'frozen':float(np.mean([x['frozen'][key] for x in a]))}
                         for key in ('energy','auc','mean_floor','final_floor','raw_tail','harvest','resource')}
        summary[str(r)]['online_energy_wins']=sum(x['delta_energy']>0 for x in a)
        summary[str(r)]['online_auc_wins']=sum(x['delta_auc']>0 for x in a)
        summary[str(r)]['paired_delta_energy']=[x['delta_energy'] for x in a]
        summary[str(r)]['paired_delta_auc']=[x['delta_auc'] for x in a]
    out={'design':'AUDIT2_PLAN.md','seeds':list(SEEDS),'regrowth':list(REGROWTHS),'ticks':3000,'size':10,'rows':rows,'summary':summary}
    (HERE/'AUDIT2_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
