"""Exact energy/resource conservation identities, including saturation corrections."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
from NEXT_WELFARE_garden import WelfareGarden
from NEXT_WELFARE_study import train

HERE=Path(__file__).resolve().parent
SEEDS=list(range(10400,10408)); SIZE=10; TRAIN=600; TEST=3000
PHASES={'stable_early':(1,999), 'scarcity':(1000,1999), 'recovery':(2000,3000)}

def tick(g):
    r=g.resource.copy(); e=g.energy.copy(); old_r=float(r.mean()); old_e=float(e.mean())
    g.step()
    a=g.last_action.copy(); raw=g.last_raw.copy(); z=e+raw
    p=float(a.mean()); ra=float(np.mean(r*a)); y=ra/p if p else 0.
    expected_raw=p*(.25*y-.063)-.022
    under=float(np.maximum(0.,-z).mean());over=float(np.maximum(0.,z-1.).mean())
    actual=float(g.energy.mean()-old_e)
    resource_expected=g.regrowth*(1-old_r)-.18*ra
    resource_actual=float(g.resource.mean()-old_r)
    return {'raw':float(raw.mean()), 'raw_formula':float(expected_raw),
            'underflow_correction':under,'overflow_correction':over,
            'realized_delta':actual,
            'budget_residual':actual-(expected_raw+under-over),
            'resource_delta':resource_actual,
            'resource_expected':resource_expected,
            'resource_residual':resource_actual-resource_expected,
            'harvest_rate':p,'harvest_yield':y,'energy':float(g.energy.mean()),
            'resource':float(g.resource.mean()),
            'floor':float(np.mean(g.energy<=.01)),
            'ceiling':float(np.mean(g.energy>=.99)),
            'positive_raw_fraction':float(np.mean(raw>0))}

def averages(rs):
    return {k:float(np.mean([row[k] for row in rs])) for k in rs[0]}

def one_seed(seed):
    theta=train('reserve_resource',seed,SIZE,TRAIN)
    models={label:WelfareGarden(seed=seed+20000,size=SIZE,learning=(label=='online'),
              objective='reserve_resource', penalty=.3)
            for label in ('online','frozen')}
    for g in models.values():g.theta=theta.copy()
    rows={label:{phase:[] for phase in PHASES} for label in models}
    for t in range(1,TEST+1):
        phase='stable_early' if t<1000 else ('scarcity' if t<2000 else 'recovery')
        for label,g in models.items():
            g.regrowth=.055 if phase=='scarcity' else .06
            rows[label][phase].append(tick(g))
    return {'seed':seed,'phase_summary':{label:{phase:averages(ts)
            for phase,ts in phases.items()} for label,phases in rows.items()},
            'max_abs_residual':max(abs(x['budget_residual'])
                        for phases in rows.values() for ts in phases.values() for x in ts),
            'max_abs_resource_residual':max(abs(x['resource_residual'])
                        for phases in rows.values() for ts in phases.values() for x in ts)}

def run():
    rows=[one_seed(s) for s in SEEDS]
    summary={label:{phase:averages([r['phase_summary'][label][phase] for r in rows])
             for phase in PHASES} for label in ('online','frozen')}
    result={'status':'completed','seeds':SEEDS,'size':SIZE,'train_steps':TRAIN,
       'test_steps':TEST,'objective':'reserve_resource','phase_windows':PHASES,
       'identity_raw':'mean(raw)=p*(.25*harvest_yield-.063)-.022',
       'identity_clipped':'realized_delta=mean(raw)+underflow-overflow',
       'identity_resource':'delta mean resource=regrowth*(1-mean resource)-.18*mean(resource*action)',
       'rows':rows,'summary':summary,
       'max_abs_energy_identity_residual':max(r['max_abs_residual'] for r in rows),
       'max_abs_resource_identity_residual':max(r['max_abs_resource_residual'] for r in rows),
       'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()
          for n in ('THEORY2_budget_probe.py','NEXT_WELFARE_garden.py','NEXT_WELFARE_study.py')},
       'caveat':['These exact identities describe this specific simulator, not learned competence.',
                 'Observed online/frozen differences are causal in the matched treatment but mediator differences are not separately randomized.',
                 'Near-stationary clipped mean energy may conceal extensive saturated-floor populations.']}
    (HERE/'THEORY2_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print('energy residual',result['max_abs_energy_identity_residual'])
    print('resource residual',result['max_abs_resource_identity_residual'])
    for label,phases in summary.items():
      for phase,s in phases.items():
        print(label,phase,'energy',round(s['energy'],4),'raw',round(s['raw'],5),
             'actual',round(s['realized_delta'],5),'floor',round(s['floor'],3),
             'underflow',round(s['underflow_correction'],5))
    return result

if __name__=='__main__':run()
