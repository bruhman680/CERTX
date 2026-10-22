"""Adaptive Cycle2: exact operator sensitivity after disclosed development."""
from pathlib import Path
import hashlib,json,time,itertools
import numpy as np
R=Path(__file__).resolve().parent
J=json.loads((R.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json').read_text())
STATES=[tuple(s) for s in J['states']]; INDEX={s:i for i,s in enumerate(STATES)}
TOL=1e-10
FAMILIES={'independent':lambda a,b:a*b,'positive':min,'negative':lambda a,b:max(0,a+b-1)}
TRAIN={'sham':(0.,0.),'agent':(.8,.1),'soil':(.1,.8)}
SHARED=(.6,.6)
GRID=[0.,.2,.4,.6,.8,1.]

def operator(ra,rs,q):
    probs=[1-ra-rs+q,ra-q,rs-q,q]
    out=np.zeros((6,6))
    for i,(m,s) in enumerate(STATES):
        for (ea,es),v in zip(((0,0),(1,0),(0,1),(1,1)),probs):
            out[i,INDEX[(0 if ea else m,0 if es else s)]]+=v
    return out,probs

def main():
    start=time.monotonic(); cells=[]; fits={}; err=0.; recovery=0.; max_independent_error=0.; additiveerr=0.; shared_errors={}
    for world,v in J['models'].items():
        pi=np.array(v['stationary']); d=pi@(np.array(v['B1'])-np.array(v['B0'])); p=np.array(v['emission']); truth=np.array(v['contributions'])
        fits[world]={};shared_errors[world]={}
        for family,qfun in FAMILIES.items():
            train_response=[]; nominal=[]; calibrated=[]
            for ra,rs in TRAIN.values():
                q=qfun(ra,rs); op,_=operator(ra,rs,q); u,w=1-ra,1-rs
                train_response.append(d@op@p);nominal.append([u,w,u*w]);calibrated.append([u,w,1-ra-rs+q])
            nominal=np.array(nominal);calibrated=np.array(calibrated);train_response=np.array(train_response)
            naive=np.linalg.solve(nominal,train_response); fit=np.linalg.solve(calibrated,train_response)
            recovery=max(recovery,float(np.max(abs(fit-truth))))
            fits[world][family]={'true_contributions':truth.tolist(),'independence_assumed_fit':naive.tolist(),'joint_witness_fit':fit.tolist(),'independence_assumed_training_residual':float(np.linalg.norm(nominal@naive-train_response)),'joint_witness_design_rank':int(np.linalg.matrix_rank(calibrated,tol=TOL)),'joint_witness_condition_number':float(np.linalg.cond(calibrated))}
            for ra,rs in itertools.product(GRID,repeat=2):
                q=qfun(ra,rs);op,probs=operator(ra,rs,q);u,w=1-ra,1-rs;survive=1-ra-rs+q
                assert min(probs)>-TOL and np.max(abs(op.sum(1)-1))<TOL
                actual=float(d@op@p);derived=float(np.array([u,w,survive])@truth);err=max(err,abs(actual-derived))
                pred_naive=float(np.array([u,w,u*w])@naive)
                pred_joint=float(np.array([u,w,survive])@fit)
                lo=max(0,1-ra-rs);hi=min(u,w);ends=[float(u*truth[0]+w*truth[1]+x*truth[2]) for x in (lo,hi)]
                covered=bool(min(ends)-TOL<=actual<=max(ends)+TOL)
                assert lo-TOL<=survive<=hi+TOL
                if family=='independent':max_independent_error=max(max_independent_error,abs(pred_naive-actual))
                if world.endswith('additive'):additiveerr=max(additiveerr,abs(pred_naive-actual))
                if (ra,rs)==SHARED:shared_errors[world][family]=pred_naive-actual
                cells.append({'world':world,'dependence':family,'rA':ra,'rS':rs,'q_both_erased':q,'erase_event_probabilities':probs,'marginal_survival':[u,w],'joint_survival':survive,'frechet_joint_survival_bounds':[lo,hi],'actual_response':actual,'operator_formula_response':derived,'independence_assumed_prediction':pred_naive,'joint_witness_prediction':pred_joint,'true_term_frechet_response_interval':[min(ends),max(ends)],'covered':covered})
    elapsed=time.monotonic()-start
    checks={'all864_cells_recorded':len(cells)==864,'operator_formula':err<TOL,'joint_witness_recovery':recovery<TOL,'all_joint_witness_predictions':all(abs(c['joint_witness_prediction']-c['actual_response'])<TOL for c in cells),'all_true_term_frechet_intervals_cover':all(c['covered'] for c in cells),'independent_control':max_independent_error<TOL,'additive_control':additiveerr<TOL,'mixed_interaction_out_of_fit_detects_dependence':abs(shared_errors['mixed_interaction']['positive'])>1e-3 and abs(shared_errors['mixed_interaction']['negative'])>1e-3,'compute_budget':elapsed<10}
    out={'scope':'Adaptive exact-population counterexample, prior sandbox exposure disclosed; no sealed test or empirical witness calibration','protocol_sha256':hashlib.sha256((R/'PROTOCOL.md').read_bytes()).hexdigest(),'source_results_sha256':hashlib.sha256((R.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json').read_bytes()).hexdigest(),'elapsed_seconds':elapsed,'max_operator_formula_error':err,'max_contribution_recovery_error':recovery,'max_independent_prediction_error':max_independent_error,'max_additive_prediction_error':additiveerr,'out_of_fit_shared_errors':shared_errors,'fits':fits,'cells':cells,'checks':checks}
    (R/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={k:out[k] for k in ['scope','elapsed_seconds','max_operator_formula_error','max_contribution_recovery_error','max_independent_prediction_error','max_additive_prediction_error','out_of_fit_shared_errors','checks']}
    print(json.dumps(summary,indent=2));assert all(checks.values())
if __name__=='__main__':main()
