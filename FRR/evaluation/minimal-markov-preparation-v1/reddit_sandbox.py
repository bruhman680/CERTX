"""Reproduction of matrices in the user's Reddit post, not the thermal ladder.

The article's grouping and defect calculations stay on the observer side.
No model calls, active world changes, or new actions are implemented here.
"""
from pathlib import Path
from fractions import Fraction
import json
import numpy as np
SOURCE_URL='https://www.reddit.com/r/ImRightAndYoureWrong/comments/1w8dgmo/when_does_a_coarsegrained_state_preserve_the/'
STATE_ORDER=('a0','a1','b0','b1','b2','b3','c0','c1')
Q=np.array([[1,0,0],[1,0,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,0,1],[0,0,1]],dtype=float)
P_EXACT=np.array([[.5,0,.5,0,0,0,0,0],[.5,0,.5,0,0,0,0,0],[.25,0,.5,0,0,0,.25,0],[.25,0,.5,0,0,0,.25,0],[.25,0,.5,0,0,0,.25,0],[.25,0,.5,0,0,0,.25,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0]],dtype=float)
P_APPROX=P_EXACT.copy();P_APPROX[1]=[.4,0,.6,0,0,0,0,0]
P_NON=np.array([[.5,.5,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[1,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,1,0]],dtype=float)
KERNELS={'post_exact':P_EXACT,'post_approximate':P_APPROX,'post_nonlumpable_historical':P_NON}
def macro(P):return np.array([(P@Q)[Q[:,i]==1].mean(axis=0) for i in range(3)])
def defects(P,t):
 d=np.abs(np.linalg.matrix_power(P,t)@Q-Q@np.linalg.matrix_power(macro(P),t)).sum(axis=1)/2
 return float(d.mean()),float(d.max())
def closed_classes(P):
 reach=P>0
 for i in range(8):reach[i,i]=True
 for k in range(8):reach|=reach[:,k,None]&reach[None,k,:]
 groups=[];seen=set()
 for i in range(8):
  if i in seen:continue
  g=[j for j in range(8) if reach[i,j] and reach[j,i]];seen.update(g)
  if all(not P[a,b] for a in g for b in range(8) if b not in g):groups.append(g)
 return groups

def check():
 expected={'post_exact':[(0,0)]*3,'post_approximate':[(.0125,.05),(.0134375,.035),(.014015625,.028875)],'post_nonlumpable_historical':[(.375,.5),(.40625,.75),(.375,.625)]}
 results={}
 for name,P in KERNELS.items():
  assert P.shape==(8,8) and np.all(P>=0) and np.allclose(P.sum(1),1,rtol=0,atol=1e-15)
  measured=[defects(P,t) for t in (1,2,3)];assert np.allclose(measured,expected[name],rtol=0,atol=1e-14)
  closed=closed_classes(P)
  one_block=np.ones((8,1));assert np.max(np.abs(P@one_block-one_block))<1e-15
  results[name]=dict(matrix=P.tolist(),defects=measured,absorbing_states=[i for i in range(8) if P[i,i]==1],closed_classes=closed,states_with_zero_incoming_probability=[j for j in range(8) if not np.any(P[:,j]>0)])
 # Expected absorption time into c0 for exact/approximate from all other states.
 for name in ('post_exact','post_approximate'):
  P=KERNELS[name];transient=[i for i in range(8) if i!=6];times=np.linalg.solve(np.eye(7)-P[np.ix_(transient,transient)],np.ones(7))
  results[name]['expected_steps_to_c0']={STATE_ORDER[i]:float(x) for i,x in zip(transient,times)}
 out=dict(status='pass',source_url=SOURCE_URL,source_kind='Published matrices and reported outputs manually transcribed from minimal reproduction section; not a byte-exact source export',state_order=STATE_ORDER,variants=results,important_lineage_note='The article code gives the historical non-lumpable defects .375/.40625/.375; later summary posts also mention a different canonical .25/.25/.25 variant. Do not blend their matrices/results.',model_calls=0,live_cursor=750,live_activated=False,thermal_ladder_candidate_superseded=True)
 (Path(__file__).parent/'REDDIT_SANDBOX_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(status='pass',variants={k:{f:v for f,v in x.items() if f!='matrix'} for k,x in results.items()},model_calls=0,live_activated=False)))
if __name__=='__main__':check()
