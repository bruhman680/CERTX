"""Known-parameter observer witness, separate from Claude's trajectory simulator."""
from pathlib import Path
import json,math,itertools
import numpy as np
P=Path(__file__).resolve().parent
R=.2; V=.032; LEVELS=np.array([R-math.sqrt(V),R+math.sqrt(V)])

def moments(T,mode):
 levels=LEVELS if mode=='fresh_soil' else LEVELS[:1] if mode=='shared_low' else LEVELS[1:]
 center=R if mode=='fresh_soil' else float(levels[0]);var=0.;fourth=0.
 for p in levels:
  d=float(p-center);v=float(p*(1-p));var+=(d*d+v/T)/len(levels)
  fourth+=(d**4+6*d*d*v/T+4*d*v*(1-2*p)/T**2+3*v*v/T**2+v*(1-6*v)/T**3)/len(levels)
 return var,fourth

def main():
 assert not(P/'OBSERVER_WITNESS.json').exists()
 rng=np.random.default_rng(2026103001);runs=6000;rows=[]
 for T in [320,800,1600]:
  for mode in ['fresh_soil','shared_low','shared_high']:
   ps=rng.choice(LEVELS,size=runs) if mode=='fresh_soil' else float(LEVELS[0 if mode=='shared_low' else 1])
   means=rng.binomial(T,ps,size=runs)/T;var,fourth=moments(T,mode);measured=float(means.var(ddof=1));se=math.sqrt(max(0,(fourth-(runs-3)/(runs-1)*var**2)/runs));z=abs(measured-var)/se
   rows.append({'T':T,'mode':mode,'runs':runs,'observed_variance':measured,'analytic_variance':var,'variance_se':se,'absolute_z':z,'within_5se':z<5,'observed_sd':float(means.std(ddof=1)),'analytic_sd':math.sqrt(var)})
 # Exact enumeration of the demeaned lag1 estimator for iid binary windows.
 ac=[];M=8
 for p in [.2,.7]:
  total=0.
  for values in itertools.product([0.,1.],repeat=M):
   x=np.array(values);z=x-x.mean();den=float(z@z);stat=float(z[:-1]@z[1:])/den if den else 0.;k=int(x.sum());total+=p**k*(1-p)**(M-k)*stat
  expected=-(1-p**M-(1-p)**M)/M;ac.append({'M':M,'p':p,'enumerated_mean':total,'analytic_mean':expected,'error':abs(total-expected),'passes':abs(total-expected)<1e-12})
 # Under actual n16shadow, exact finite-demeaning predictions (not new outcome-blind forecasts).
 forecasts=[]
 for T in [320,800,1600,3200]:
  M=T//16;acmean=0.;dimean=0.
  for p in LEVELS:
   countpmf=[math.comb(16,k)*p**k*(1-p)**(16-k) for k in range(17)]
   den_zero=sum(q**M for q in countpmf);acmean+=-.5*(1-den_zero)/M
   dimean+=.5*T/(T-1)*(1-p**T-(1-p)**T)
  forecasts.append({'T':T,'M':M,'expected_ac_estimator':acmean,'expected_di_estimator':dimean})
 n=16;pooled_var=n*R*(1-R)+(n*n-n)*V;pooled_di=pooled_var/(n*R*(1-R));pooled_adjacent_rho=n*n*V/pooled_var
 output={'scope':'Known two-level shadow model, no realagents. Conditional shared-soil variance differs from resampled-soil variance. Self-authored bounded witness, not independent dynamics reimplementation.','levels':LEVELS.tolist(),'variance_rows':rows,'exact_ac_checks':ac,'finite_estimator_means':forecasts,'pooled_population_window_di':pooled_di,'within_condition_population_di':1.0,'ensemble_adjacent_window_correlation':pooled_adjacent_rho,'all_checks_pass':all(x['within_5se'] for x in rows) and all(x['passes'] for x in ac)}
 (P/'OBSERVER_WITNESS.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'variance_cells':len(rows),'exact_ac_checks':len(ac),'all_checks_pass':output['all_checks_pass'],'pooled_di':pooled_di,'pooled_window_rho':pooled_adjacent_rho},indent=2))
if __name__=='__main__':main()
