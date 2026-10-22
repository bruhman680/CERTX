"""Scalar replay of saved witness-access laws, not witness validation."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent
P=D.parent/'cycle1'
j=json.loads((P/'RESULTS.json').read_text());states=[tuple(z) for z in j['states_S_G']]
errors=[];maxerr=0.;mcar=0;closed=0
for ix,c in enumerate(j['cells']):
 v,a1,a0=c['v'],c['a1'],c['a0']
 expected_joint=[]
 for s,g in states:
  survival=v if s else 1-v;gate=a1 if s else a0
  expected_joint.append(survival*(gate if g else 1-gate))
 binary=[0.,0.];ternary=[0.,0.,0.]
 for mass,(s,g) in zip(expected_joint,states):
  binary[s*g]+=mass
  ternary[0 if s and g else 1 if g else 2]+=mass
 lo,hi=ternary[0],1-ternary[1]
 for a,b in zip(expected_joint,c['joint']):maxerr=max(maxerr,abs(a-b))
 for a,b in zip(binary,c['observations']['zero_coded']):maxerr=max(maxerr,abs(a-b))
 for a,b in zip(ternary,c['observations']['ternary_1_0_missing']):maxerr=max(maxerr,abs(a-b))
 for a,b in zip([lo,hi],c['survival_interval']):maxerr=max(maxerr,abs(a-b))
 if not lo-1e-12<=v<=hi+1e-12:errors.append(['containment',ix])
 # Check a dense interval too; constructive formula proves general attainability.
 for t in range(101):
  u=lo+(hi-lo)*t/100;b1=lo/u if u else 0.;b0=ternary[1]/(1-u) if u<1 else 0.
  if not (-1e-12<=b1<=1+1e-12 and -1e-12<=b0<=1+1e-12):errors.append(['gate_bounds',ix,t])
  maxerr=max(maxerr,abs(u*b1-lo),abs((1-u)*b0-ternary[1]))
 if a1==a0:
  if a1>0:
   mcar+=1;maxerr=max(maxerr,abs(ternary[0]/(ternary[0]+ternary[1])-v))
  else:closed+=1
 for name,target in [('restoration_preserving_operator',v),('restoration_rewriting_operator',.6)]:
  mat=j[name];post=[sum(expected_joint[i]*mat[i][k] for i in range(4)) for k in range(4)]
  p1=sum(z for z,(s,g) in zip(post,states) if s and g)
  maxerr=max(maxerr,abs(sum(post)-1),abs(p1-target))
checks={'216cells':len(j['cells'])==216,'scalar_replay_and_dense_sharpness':maxerr<1e-12 and not errors,'mcar30_readable6_closed':mcar==30 and closed==6,'protocol_bound':hashlib.sha256((P/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'main_checks_pass':all(j['checks'].values())}
out={'scope':'Separate scalar enumeration/dense attainability replay; same authored population model, no empirical witness validation','cells':len(j['cells']),'dense_interval_points_per_cell':101,'max_absolute_error':maxerr,'mcar_readable_cells':mcar,'mcar_closed_gate_cells':closed,'errors':errors,'checks':checks}
(D/'CYCLE1_AUDIT.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2,allow_nan=False));assert all(checks.values())
