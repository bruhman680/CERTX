from pathlib import Path
import json,hashlib,importlib.util,warnings,math
import numpy as np
D=Path(__file__).resolve().parent;src=D.parent/'cycle2'/'RESULTS.json';j=json.loads(src.read_bytes());base=json.loads((D.parents[1]/'soil-reset-robustness-v1'/'RESULTS.json').read_text())
errors=[];maximum=0.;envfail=0
for c in j['cells']:
 v=base['models'][c['world']];pi=v['stationary'];B0=v['B0'];B1=v['B1'];ra,rs,q=c['rA'],c['rS'],c['q_both_erased'];probs=[1-ra-rs+q,ra-q,rs-q,q];total=0.
 for origin,(m,s) in enumerate(base['states']):
  for target,(u,t) in enumerate(base['states']):
   weight=pi[origin]*(B1[origin][target]-B0[origin][target])
   for p,(ea,es) in zip(probs,[(0,0),(1,0),(0,1),(1,1)]):
    mr=0 if ea else u;sr=0 if es else t
    em=.05+.2*mr+.2*sr+(.08*mr*sr if c['world'].endswith('interaction') else 0)
    total+=weight*p*em
 maximum=max(maximum,abs(total-c['actual_response']))
 if not(c['true_term_frechet_response_interval'][0]-1e-10<=total<=c['true_term_frechet_response_interval'][1]+1e-10):envfail+=1
 if abs(c['joint_survival']-(1-ra-rs+q))>1e-12:errors.append('joint survival')
 if not(np.isclose(sum(probs),1) and min(probs)>-1e-10):errors.append('operator legal')
assert maximum<1e-10 and not errors and envfail==0
spec=importlib.util.spec_from_file_location('reviewed_guard',D.parent/'cycle3'/'allocation_guard.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
x=[[1,1],[.2,.9],[.9,.2]]
inputs={'nonfinite_X':([[1,1],[float('inf'),0]],[0,0],.1),'out_of_range_contrast':(x,[2,2,2],.01),'finite_overflow_radius':(x,[.1,.1,.1],1e308)}
guard={}
for k,(xx,yy,ee) in inputs.items():
 with warnings.catch_warnings(record=True) as w:
  warnings.simplefilter('always')
  try:z=mod.allocate(xx,yy,ee,calibration='estimated',population_rank=2)
  except Exception as e:z={'raised':type(e).__name__,'message':str(e)}
  guard[k]={'response':z,'warnings':[str(a.message) for a in w]}
out={'scope':'Separate scalar Cycle2 operator calculation and deterministic guard challenge; no new sampled efficacy data','cycle2_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'cycle2_cells_checked':len(j['cells']),'max_scalar_operator_difference':maximum,'envelope_failures':envfail,'errors':errors,'cycle2_protocol_hash_matches':hashlib.sha256((D.parent/'cycle2'/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'guard_source_sha256':hashlib.sha256((D.parent/'cycle3'/'allocation_guard.py').read_bytes()).hexdigest(),'guard_challenges':guard}
def normalize(z):
 if isinstance(z,float) and not math.isfinite(z):return str(z)
 if isinstance(z,list):return [normalize(v) for v in z]
 if isinstance(z,dict):return {k:normalize(v) for k,v in z.items()}
 return z
out=normalize(out)
(D/'CYCLE2_GUARD_AUDIT.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2,allow_nan=False))
