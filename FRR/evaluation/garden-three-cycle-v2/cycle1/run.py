"""Exact finite witness-access model, with floating-point arithmetic."""
from pathlib import Path
import hashlib,itertools,json,time
import numpy as np
D=Path(__file__).resolve().parent
STATES=list(itertools.product((0,1),repeat=2))
TOL=1e-12

def joint(v,a1,a0):
    return np.array([(v if s else 1-v)*((a1 if s else a0) if g else 1-(a1 if s else a0)) for s,g in STATES])

def observe(p):
    binary=np.zeros(2);ternary=np.zeros(3)
    for mass,(s,g) in zip(p,STATES):
        binary[s*g]+=mass
        ternary[0 if (s,g)==(1,1) else 1 if (s,g)==(0,1) else 2]+=mass
    return {'zero_coded':binary.tolist(),'ternary_1_0_missing':ternary.tolist(),'external_survival':float(sum(m for m,(s,g) in zip(p,STATES) if s))}

def attain(p1,p0,v):
    a1=p1/v if v else 0.
    a0=p0/(1-v) if v<1 else 0.
    return a1,a0

def main():
    start=time.perf_counter();grid=[0.,.2,.4,.6,.8,1.];cells=[];maxsharp=0.;mcarerr=0.;maxbias=0.;mcarcount=0
    preserve=np.array([[float((u,h)==(s,1)) for u,h in STATES] for s,g in STATES])
    rewrite=np.tile(np.array([0.,.4,0.,.6]),(4,1))
    restoration_errors=[]
    for v,a1,a0 in itertools.product(grid,repeat=3):
        p=joint(v,a1,a0);o=observe(p);p1,p0,missing=o['ternary_1_0_missing'];lo,hi=p1,1-p0
        assert min(p)>-TOL and abs(sum(p)-1)<TOL
        witnesses=[]
        for u in (lo,(lo+hi)/2,hi):
            b1,b0=attain(p1,p0,u)
            assert -TOL<=b1<=1+TOL and -TOL<=b0<=1+TOL
            z=observe(joint(u,b1,b0))
            err=float(np.max(abs(np.array(z['ternary_1_0_missing'])-[p1,p0,missing])));maxsharp=max(maxsharp,err)
            witnesses.append({'v':u,'a1':b1,'a0':b0,'error':err})
        conditional=p1/(p1+p0) if p1+p0>0 else None
        if a1==a0 and a1>0:
            mcarcount+=1;mcarerr=max(mcarerr,abs(conditional-v))
        if conditional is not None:maxbias=max(maxbias,abs(conditional-v))
        observed_preserve=observe(p@preserve);observed_rewrite=observe(p@rewrite)
        restoration_errors.extend([abs(observed_preserve['zero_coded'][1]-v),abs(observed_rewrite['zero_coded'][1]-.6)])
        cells.append({'v':v,'a1':a1,'a0':a0,'joint':p.tolist(),'observations':o,'survival_interval':[lo,hi],'zero_coded_survival_interval':[p1,1.],'conditional_readable_survival':conditional,'sharpness_witnesses':witnesses,'restored_preserving_survival':observed_preserve['zero_coded'][1],'restored_rewriting_survival':observed_rewrite['zero_coded'][1]})
    examples={}
    for label,params in {'same_zero_coded':[(.2,1.,1.),(1.,.2,.2)],'same_ternary':[(.2,1.,.25),(.8,.25,1.)]}.items():
        examples[label]=[{'parameters':z,'observations':observe(joint(*z)),'preserving_restore':observe(joint(*z)@preserve),'rewriting_restore':observe(joint(*z)@rewrite)} for z in params]
    z=examples['same_zero_coded'];t=examples['same_ternary']
    checks={'cells216':len(cells)==216,'ternary_interval_contains_truth':all(x['survival_interval'][0]-TOL<=x['v']<=x['survival_interval'][1]+TOL for x in cells),'interval_endpoint_midpoint_attainable':maxsharp<TOL,'mcar_identification_when_readable':mcarerr<TOL and mcarcount==30,'same_binary_different_survival':np.allclose(z[0]['observations']['zero_coded'],z[1]['observations']['zero_coded'],atol=TOL) and abs(z[0]['parameters'][0]-z[1]['parameters'][0])>.5,'same_ternary_different_survival':np.allclose(t[0]['observations']['ternary_1_0_missing'],t[1]['observations']['ternary_1_0_missing'],atol=TOL) and abs(t[0]['parameters'][0]-t[1]['parameters'][0])>.5,'restoration_maps':max(restoration_errors)<TOL,'restoration_matrices_stochastic':np.allclose(preserve.sum(1),1) and np.allclose(rewrite.sum(1),1)}
    checks={k:bool(v) for k,v in checks.items()}
    out={'scope':'Population observation-model enumeration, not empirical witness validation','protocol_sha256':hashlib.sha256((D/'PROTOCOL.md').read_bytes()).hexdigest(),'states_S_G':STATES,'restoration_preserving_operator':preserve.tolist(),'restoration_rewriting_operator':rewrite.tolist(),'examples':examples,'cells':cells,'max_interval_attainability_error':maxsharp,'max_mcar_error':mcarerr,'mcar_readable_cells':mcarcount,'max_conditional_readable_bias':maxbias,'checks':checks,'elapsed_seconds':time.perf_counter()-start}
    (D/'RESULTS.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('cells',)},indent=2,allow_nan=False));assert all(checks.values()),checks
if __name__=='__main__':main()
