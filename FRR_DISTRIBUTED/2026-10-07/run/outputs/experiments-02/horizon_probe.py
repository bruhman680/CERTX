import json, math, statistics, hashlib
from pathlib import Path
from graph_two_route_probe import stochastic_run, p_first, mean_field_fixed_difference
rows=[]
for gamma in (.7,.8,.9):
    for horizon in (1000,10000,200000):
        runs=[stochastic_run(gamma,.2,2.,steps=horizon,seed=s) for s in range(30)]
        switches=[r[1] for r in runs]
        fractions=[r[0][0]/horizon for r in runs]
        rows.append(dict(gamma=gamma,horizon=horizon,seeds=list(range(30)),switches_min=min(switches),switches_median=statistics.median(switches),switches_max=max(switches),zero_switch_runs=sum(s==0 for s in switches),first_route_fraction_min=min(fractions),first_route_fraction_max=max(fractions)))
bounds=[]
for gamma in (.7,.8,.9):
    q=p_first(-.2/(1-gamma),2.)
    L=math.floor(math.log(.5)/math.log(gamma))+1
    bounds.append(dict(gamma=gamma,q=q,opposite_block_length=L,block_success_floor=q**L,sign_no_escape_upper_200000=math.exp(math.floor(200000/L)*math.log1p(-q**L)),no_specified_route_upper_1000=math.exp(1000*math.log1p(-q)),positive_mean_field_fixed_point=mean_field_fixed_difference(gamma,.2,2.)))
result=dict(protocol='30 fixed seeds 0..29; separately reset z=0 for each horizon; overlapping streams are dependent',rows=rows,bounds=bounds)
Path('horizon-results.json').write_text(json.dumps(result,indent=2)+'\n')
for row in rows: print(row)
print('BOUNDS',json.dumps(bounds,indent=2))
