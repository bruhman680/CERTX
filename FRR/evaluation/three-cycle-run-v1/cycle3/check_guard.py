from pathlib import Path
import json,numpy as np
from allocation_guard import allocate
D=Path(__file__).resolve().parent
x=np.array([[1,1],[.2,.9],[.9,.2]]);truth=np.array([.064,.072]);d=x@truth
fixtures={}
z=allocate(x,d,0,calibration='known',population_rank=2)
fixtures['fullrank_exact']=z['status']=='conditional_interval' and np.allclose(z['estimate'],truth)
fixtures['semantic_rank_not_empirical_rank']=allocate([[1,1],[.39,.41],[.39,.41]],[.1,.04,.04],.01,calibration='estimated',population_rank=1)['reason']=='population_design_insufficient'
fixtures['singular_estimated']=allocate([[1,1],[.4,.4],[.4,.4]],[.1,.04,.04],.01,calibration='estimated',population_rank=2)['reason']=='estimated_design_singular'
fixtures['missing_calibration']=allocate(x,d,.01,calibration='absent',population_rank=2)['reason']=='calibration_unavailable'
invalid=[(x, [1], .01, (.2,.4)),(x, [1,float('nan'),0], .01,(.2,.4)),(x,d,-.1,(.2,.4)),(x,d,.1,(-1,.4)),([[1,1],[2,0]], [1,0], .1,(.2,.4))]
fixtures['invalid_inputs_unresolved']=all(allocate(a,b,c,calibration='estimated',population_rank=2,bounds=f)['reason']=='invalid_input' for a,b,c,f in invalid)
fixtures['contrast_out_of_range']=allocate(x,[2,2,2],.01,calibration='estimated',population_rank=2)['reason']=='invalid_input'
fixtures['derived_overflow_unresolved']=allocate(x,d,1e308,calibration='estimated',population_rank=2)['reason']=='derived_nonfinite'
j=json.loads((D.parent/'cycle1/RESULTS.json').read_text());n=0;err=0.
for r in j['replicates']:
 if r['design']!='diverse' or r['mode']=='absent':continue
 xm=x if r['mode']=='known' else r['witness_survival']
 z=allocate(xm,r['observed_contrasts'],j['epsilon'][str(r['n'])],calibration=r['mode'],population_rank=2)
 assert z['status']=='conditional_interval'
 err=max(err,float(np.max(abs(np.array(z['estimate'])-r['allocation']))),float(np.max(abs(2*np.array(z['half_width'])-r['width']))));n+=1
fixtures['saved_fullrank_outputs_preserved']=err<1e-10 and n==4800
out={'fixtures':fixtures,'saved_mode_assessments_checked':n,'maximum_saved_difference':err,'new_random_draws':0,'scope':'Scoped guard and saved-output replay; no new efficacy trial'}
(D/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(fixtures.values())
