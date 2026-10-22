from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parent
src=R.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json'
j=json.loads(src.read_text());v=j['models']['mixed_interaction']
states=[tuple(s) for s in j['states']];index={s:i for i,s in enumerate(states)}
d=np.array(v['stationary'])@(np.array(v['B1'])-np.array(v['B0']));p=np.array(v['emission'])
true=np.array(v['contributions']); rates={n:tuple(x['rates']) for n,x in j['resets'].items()}
train=('sham','agent','soil');test='shared'
def reset(ra,rs,q):
 out=np.zeros((6,6));pr=[1-ra-rs+q,ra-q,rs-q,q]
 assert min(pr)>-1e-12
 for i,(m,s) in enumerate(states):
  for (ea,es),prob in zip(((0,0),(1,0),(0,1),(1,1)),pr):out[i,index[(0 if ea else m,0 if es else s)]]+=prob
 return out,pr
X=np.array([[1-rates[n][0],1-rates[n][1],(1-rates[n][0])*(1-rates[n][1])] for n in train])
xt=np.array([1-rates[test][0],1-rates[test][1],(1-rates[test][0])*(1-rates[test][1])])
rows={};maxerr=0.
for label,func in [('independent',lambda a,b:a*b),('positive',min),('negative',lambda a,b:max(0,a+b-1))]:
 data={}
 for n,(a,b) in rates.items():
  q=func(a,b);op,erase_pr=reset(a,b,q);J=1-a-b+q;actual=float(d@op@p);derived=float(np.array([1-a,1-b,J])@true)
  maxerr=max(maxerr,abs(actual-derived));assert np.max(abs(op.sum(1)-1))<1e-10
  data[n]={'rA':a,'rS':b,'q_both_erased':q,'joint_survival':J,'erase_event_probabilities':erase_pr,'operator':op.tolist(),'first_outcome_response':actual,'direct_witness_marginal_survival':[1-a,1-b],'direct_witness_joint_survival':J}
 y=np.array([data[n]['first_outcome_response'] for n in train]);fit=np.linalg.solve(X,y)
 predicted=float(xt@fit);actual=data[test]['first_outcome_response']
 rows[label]={'resets':data,'independence_assumed_fit':fit.tolist(),'true_contributions':true.tolist(),'fit_bias':(fit-true).tolist(),'training_residual':float(np.linalg.norm(X@fit-y)),'held_out_shared_prediction':predicted,'held_out_shared_actual':actual,'held_out_shared_error':predicted-actual}
checks={'operator_formula':maxerr<1e-10,'same_marginal_witnesses':all(rows['independent']['resets'][n]['direct_witness_marginal_survival']==rows['positive']['resets'][n]['direct_witness_marginal_survival']==rows['negative']['resets'][n]['direct_witness_marginal_survival'] for n in rates),'correlated_fit_training_residual_small':rows['positive']['training_residual']<1e-10,'correlated_fit_biased':max(abs(x) for x in rows['positive']['fit_bias'])>1e-4,'held_out_shared_detects_dependence':abs(rows['positive']['held_out_shared_error'])>1e-3,'independent_control_predicts':abs(rows['independent']['held_out_shared_error'])<1e-10}
out={'scope':'Exact population counterexample conditional on SR-C1 mixed interaction readout and known direct-access witnesses','max_operator_formula_error':maxerr,'cases':rows,'checks':checks}
(R/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'max_formula_error':maxerr,'checks':checks,'case_summaries':{k:{x:v[x] for x in ('fit_bias','training_residual','held_out_shared_error')} for k,v in rows.items()}},indent=2));assert all(checks.values())
