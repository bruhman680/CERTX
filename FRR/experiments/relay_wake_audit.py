"""Reproduce and scope new Claude wake claims; originals unchanged."""
import contextlib,io,itertools,json,runpy
from pathlib import Path
import numpy as np
from fractions import Fraction
R=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):
 W=runpy.run_path(str(R/'lineage/sources/claude-relay-2026-10-15/wake.py'))

def hankel(h,depth=3):
 levels=W['expand'](h,{0:[.25,.25],1:[.25,.25]},2*depth)
 words=[()]+[x for k in range(1,depth+1) for x in itertools.product((0,1),repeat=k)]
 def prob(w):return 1. if not w else float(levels[len(w)-1][w].sum())
 H=np.array([[prob(a+b) for b in words] for a in words]);s=np.linalg.svd(H,compute_uv=False)
 return {'rank_tolerance1e-10':int(sum(s>1e-10)),'singular_values':s.tolist()}

def exact_hankel_rank(h,depth=3):
 K=[[[Fraction(17,20),Fraction(3,20)],[Fraction(1,10),Fraction(9,10)]],[[Fraction(11,20),Fraction(9,20)],[Fraction(2,5),Fraction(3,5)]]]
 words=[()]+[x for k in range(1,depth+1) for x in itertools.product((0,1),repeat=k)]
 def probability(w):
  if not w:return Fraction(1)
  a=[Fraction(1,4),Fraction(1,4)]
  for i in range(1,len(w)):
   nxt=[Fraction(0),Fraction(0)]
   for e in (0,1):nxt[e if h==0 else w[i-1]]+=a[e]*K[e][w[i-1]][w[i]]
   a=nxt
  return sum(a)
 matrix=[[probability(a+b) for b in words] for a in words];row=0
 for col in range(len(words)):
  pivot=next((i for i in range(row,len(words)) if matrix[i][col]),None)
  if pivot is None:continue
  matrix[row],matrix[pivot]=matrix[pivot],matrix[row];v=matrix[row][col]
  matrix[row]=[x/v for x in matrix[row]]
  for i in range(row+1,len(words)):
   v=matrix[i][col]
   if v:matrix[i]=[x-v*y for x,y in zip(matrix[i],matrix[row])]
  row+=1
 return row

def run():
 out={'scope':'Finite 4-state model, numerical matrix operations/exact finite-word enumeration up to float precision. No semantic or physical-memory claim. Finite Hankel ranks do not identify infinite predictive-state cardinality.','records':[]}
 for h in (0,.02,.05,.2,.5,1.):
  P=W['joint_chain'](h);pi=W['stationary'](P);eig=np.linalg.eigvals(P)
  d=np.array([-1.,1.,0,0]);signed=[];joint_tvs=[]
  for t in (1,2,4,8,16,32):
   diff=d@np.linalg.matrix_power(P,t)
   signed.append(float(diff[2:].sum()));joint_tvs.append(float(.5*abs(diff).sum()))
  out['records'].append({'h':h,'row_error':float(abs(P.sum(1)-1).max()),'stationarity_error':float(abs(pi@P-pi).max()),'eigenvalues':[[float(z.real),float(z.imag)] for z in eig], 'signed_visible_reset_difference_t1_2_4_8_16_32':signed,'visible_TV':list(map(abs,signed)),'full_joint_TV':joint_tvs})
  assert abs(abs(signed[0])-.3)<1e-12
  assert all(joint_tvs[i+1]<=joint_tvs[i]+1e-12 for i in range(len(joint_tvs)-1))
  if h==0:assert all(abs(x-1)<1e-12 for x in joint_tvs)
 out['hankel_prefix_suffix_depth3']={str(h):hankel(h) for h in (0.,1.)}
 out['exact_rational_hankel_ranks_depth3']={str(h):exact_hankel_rank(h) for h in (0,1)}
 assert all(v==4 for v in out['exact_rational_hankel_ranks_depth3'].values())
 assert all(x['rank_tolerance1e-10']==4 for x in out['hankel_prefix_suffix_depth3'].values())
 # Equality B=M10 for reported post-reset horizon is structural: min(k,historylen) uses all observed history.
 prior_note='For t<=8 the visible history has t+1<=9 symbols. M10 therefore conditions on the full available word, with the same stationary initial belief and filtering equations as B. Equality here does not demonstrate that two different predictors independently agree.'
 out['B_M10_identity_scope']=prior_note
 out['reset_prior_comparison']=[]
 for h in (.02,.05,.2,.5,1.):
  P=W['joint_chain'](h);pi=W['stationary'](P);pi=pi/pi.sum()
  conditioned=pi[:2]/pi[:2].sum()
  retained=pi.reshape(2,2).sum(axis=0)
  emission=W['K'][:,0,:]
  q_cond=conditioned@emission;q_do=retained@emission
  risk=lambda q:sum(retained[e]*W['KL'](emission[e],q) for e in (0,1))
  delta=risk(q_cond)-risk(q_do)
  assert delta>=-1e-12
  assert abs(delta-W['KL'](q_do,q_cond))<1e-12
  out['reset_prior_comparison'].append({'h':h,'observational_prior_e_given_y0':conditioned.tolist(),'stationary_field_retained_under_independent_do_y0':retained.tolist(),'extra_one_step_risk_of_conditioning_prior_nats':float(delta)})
 out['prior_scope']='This additional comparison specifies a new preparation: retain the stationary environmental marginal while independently setting y=0. Under that protocol observational P(e|y=0) differs from interventional P(e). Original fixed-e tests are defined experiments; this is not a claim every chosen predictor prior is a code error.'
 out['conditional_prediction_note']='A Bayes posterior optimized for stationary/no-reset data need not minimize conditional risk after a fixed-environment reset. B<=M4<=M2 is not a general risk theorem under this shifted evaluation distribution.'
 return out
if __name__=='__main__':
 d=run();(R/'evaluation/results/relay-wake-audit.json').write_text(json.dumps(d,indent=2)+'\n')
 for row in d['records']:print('h',row['h'],'eigenvalues',row['eigenvalues'],'signed reset',row['signed_visible_reset_difference_t1_2_4_8_16_32'])
 print('Hankel ranks:',{k:v['rank_tolerance1e-10'] for k,v in d['hankel_prefix_suffix_depth3'].items()})
