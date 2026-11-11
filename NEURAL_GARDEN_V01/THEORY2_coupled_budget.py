"""Cross-check an eliminated-action resource/energy bound from frozen phase summaries."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=json.loads((HERE/'THEORY2_results.json').read_text())
rows=[]
for cohort,phases in source['summary'].items():
  for phase,s in phases.items():
    alpha=.055 if phase=='scarcity' else .06
    resource_before=s['resource']-s['resource_delta']
    predicted=(.25/.18)*(alpha*(1-resource_before)-s['resource_delta'])-.063*s['harvest_rate']-.022
    resource_cap=(.25/.18)*alpha*(1-resource_before)-.022
    rows.append({'cohort':cohort,'phase':phase,'mean_harvest_rate':s['harvest_rate'],
       'mean_resource_before':resource_before,'mean_resource_delta':s['resource_delta'],
       'raw_observed':s['raw'],'raw_eliminated_action_predicted':predicted,
       'residual':s['raw']-predicted,
       'capacity_upper_bound_if_resource_stationary':resource_cap,
       'stationary_viability_would_require_raw_cost_frequency_not_exceed_capacity':
          .063*s['harvest_rate']<=resource_cap})
payload={'status':'completed','purpose':'coupled resource-energy budget identity',
         'formula':'raw=(.25/.18)*(alpha*(1-r_before)-delta_resource)-.063*p-.022',
         'conditional_stationary_bound':'if delta_resource≈0, raw≤(.25/.18)*alpha*(1-r_before)-.022 (since p≥0)',
         'rows':rows,'max_abs_residual':max(abs(r['residual']) for r in rows),
         'caveat':'Stationary viability requires phase stationarity, non-clipped resource dynamics and this synthetic model; an upper bound does not guarantee stable viability.'}
(HERE/'THEORY2_coupled_results.json').write_text(json.dumps(payload,indent=2)+'\n')
print('residual',payload['max_abs_residual'])
for r in rows:print(r['cohort'],r['phase'],r['raw_observed'],r['raw_eliminated_action_predicted'],r['capacity_upper_bound_if_resource_stationary'])
