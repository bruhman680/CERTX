from pathlib import Path
import json,numpy as np
r=Path(__file__).resolve().parent
j=json.loads((r/'RESULTS.json').read_text());out={}
for label,case in j['cases'].items():
 names=('sham','agent','soil');x=np.array([[*case['resets'][n]['direct_witness_marginal_survival'],case['resets'][n]['joint_survival']] for n in names]);y=np.array([case['resets'][n]['first_outcome_response'] for n in names]);fit=np.linalg.solve(x,y)
 t=case['resets']['shared'];a,b=t['rA'],t['rS'];lo=max(0,1-a-b);hi=min(1-a,1-b);nom=np.array(case['independence_assumed_fit']);base=(1-a)*nom[0]+(1-b)*nom[1];ends=[float(base+lo*nom[2]),float(base+hi*nom[2])]
 out[label]={'joint_witness_calibrated_fit':fit.tolist(),'joint_witness_fit_error':(fit-np.array(case['true_contributions'])).tolist(),'shared_frechet_survival_interval':[lo,hi],'out_of_fit_shared_prediction_interval_using_nominal_fit':[min(ends),max(ends)],'actual_shared_response':t['first_outcome_response'],'frechet_interval_covers_shared_response':bool(min(ends)-1e-10<=t['first_outcome_response']<=max(ends)+1e-10)}
checks={'joint_witness_recovers':all(max(abs(z) for z in c['joint_witness_fit_error'])<1e-10 for c in out.values()),'frechet_interval_covers_three_selected_cases':all(c['frechet_interval_covers_shared_response'] for c in out.values())}
result={'scope':'Adaptive sandbox sensitivity analysis, not sealed confirmation or confidence coverage guarantee','cases':out,'checks':checks}
(r/'SUPPLEMENT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
