from pathlib import Path
import json,hashlib,time
import numpy as np
D=Path(__file__).resolve().parent
SRC=D.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json'

def main():
 start=time.perf_counter();j=json.loads(SRC.read_text());rng=np.random.default_rng(2026102201);rows=[]
 candidates=np.array([[0,0],[.064,0],[0,.072],[.064,.072]])
 names=['shadow','echo','wake','mixed'];epses={n:float(np.sqrt(np.log(24/.05)/(2*n))) for n in (100,1000,10000)}
 for design,arms in [('diverse',['sham','agent','soil']),('redundant',['sham','shared','shared'])]:
  X=np.array([[1-j['resets'][a]['rates'][0],1-j['resets'][a]['rates'][1]] for a in arms])
  for n,e in epses.items():
   for ki,kind in enumerate(names):
    model=j['models'][kind+'_additive'];means=np.array([[model['responses'][a]['baseline_error'][0]+model['responses'][a][f'forced{y}_minus_no_probe'][0] for y in (0,1)] for a in arms])
    assert np.max(abs(means[:,1]-means[:,0]-X@candidates[ki]))<1e-10
    for rep in range(200):
     observations=rng.binomial(n,means)/n;d=observations[:,1]-observations[:,0]
     xhat=rng.binomial(n,X)/n
     if design=='redundant':xhat[1:]=xhat[1:].mean(0)
     for mode in ('known','estimated','absent'):
      if mode=='absent':
       row={'design':design,'n':n,'world':kind,'rep':rep,'mode':mode,'candidate_set':names.copy(),'allocation':None,'width':None,'covered':None,'positive':None,'false_positive':None}
      else:
       xm=X if mode=='known' else xhat
       lo=xm if mode=='known' else np.maximum(0,xm-e)
       hi=xm if mode=='known' else np.minimum(1,xm+e)
       accept=[names[ix] for ix,c in enumerate(candidates) if np.all((hi@c>=d-2*e)&(lo@c<=d+2*e))]
       estimate=half=covered=positive=falsepositive=None
       if design=='diverse':
        pinv=np.linalg.pinv(xm);estimate=pinv@d
        half=abs(pinv)@np.full(3,2*e+(0 if mode=='known' else .6*e))
        covered=bool(np.all(abs(estimate-candidates[ki])<=half+1e-12))
        positive=(estimate-half>0)
        falsepositive=bool(np.any(positive&(candidates[ki]==0)))
       row={'design':design,'n':n,'world':kind,'rep':rep,'mode':mode,'candidate_set':accept,'allocation':None if estimate is None else estimate.tolist(),'width':None if half is None else (2*half).tolist(),'covered':covered,'positive':None if positive is None else positive.tolist(),'false_positive':falsepositive}
      row.update({'true_candidate_retained':kind in row['candidate_set'],'point_identified':len(row['candidate_set'])==1,'observed_contrasts':d.tolist(),'witness_survival':xhat.tolist(),'cost_draws':12*n})
      rows.append(row)
 groups=[]
 for design in ('diverse','redundant'):
  for n in epses:
   for mode in ('known','estimated','absent'):
    r=[z for z in rows if z['design']==design and z['n']==n and z['mode']==mode]
    cc=[z for z in r if z['covered'] is not None]
    groups.append({'design':design,'n':n,'mode':mode,'replicates':len(r),'true_candidate_retention':float(np.mean([z['true_candidate_retained'] for z in r])),'singleton_fraction':float(np.mean([z['point_identified'] for z in r])),'mean_candidate_count':float(np.mean([len(z['candidate_set']) for z in r])),'continuous_coverage':None if not cc else float(np.mean([z['covered'] for z in cc])),'mean_interval_width':None if not cc else np.mean([z['width'] for z in cc],axis=0).tolist(),'false_positive_fraction':None if not cc else float(np.mean([z['false_positive'] for z in cc]))})
 result={'scope':'Synthetic calibration with known witness semantics, finite candidate sets and conservative continuous intervals','seed':2026102201,'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'protocol_sha256':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest(),'epsilon':epses,'replicates':rows,'summary':groups,'elapsed_seconds':time.perf_counter()-start,'checks':{'main_response_probabilities_valid':True,'same_draw_budget':all(z['cost_draws']==12*z['n'] for z in rows),'absent_calibration_never_point_allocates':all(z['allocation'] is None for z in rows if z['mode']=='absent'),'redundant_never_point_allocates':all(z['allocation'] is None for z in rows if z['design']=='redundant'),'replicate_count':len(rows)==14400}}
 (D/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'summary':groups,'elapsed_seconds':result['elapsed_seconds'],'checks':result['checks']},indent=2));assert all(result['checks'].values())
if __name__=='__main__':main()
