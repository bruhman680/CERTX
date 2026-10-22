"""SR-C1: finite enumeration with floating-point algebra, no sampling."""
from pathlib import Path
import hashlib,itertools,json
import numpy as np
ROOT=Path(__file__).resolve().parent
STATES=list(itertools.product(range(2),range(3)))
M=np.array([m for m,s in STATES],float)
S=np.array([s for m,s in STATES],float)
TOL=1e-10
RESETS={'sham':(0.,0.),'agent':(.8,.1),'soil':(.1,.8),'shared':(.6,.6),'both':(1.,1.)}

def kernel(kind,y):
    rows=[]
    for m,s in STATES:
        ma=np.eye(2)[m]*.6+.4*np.array([.9-.8*y,.1+.8*y]) if kind in ('echo','mixed') else np.ones(2)/2
        so=np.eye(3)[s]*.7+.3*np.array([.7,.2,.1] if y==0 else [.1,.2,.7]) if kind in ('wake','mixed') else np.eye(3)[s] if kind=='shadow' else np.ones(3)/3
        rows.append(np.kron(ma,so))
    return np.array(rows)

def reset(a,b):
    return np.array([np.kron((1-a)*np.eye(2)[m]+a*np.array([1,0]),(1-b)*np.eye(3)[s]+b*np.array([1,0,0])) for m,s in STATES])

def stationary(P):
    # Minimum-norm solution fixes uniform soil mixture for reducible shadow.
    mat=np.vstack([P.T-np.eye(6),np.ones(6)])
    pi=np.linalg.lstsq(mat,np.r_[np.zeros(6),1],rcond=None)[0]
    assert np.min(pi)>-TOL and np.max(abs(pi@P-pi))<TOL
    return pi

def words(v,p,B,n=4):
    out=[]
    for word in itertools.product((0,1),repeat=n):
        q=v.copy()
        for y in word:q=(q*(p if y else 1-p))@B[y]
        out.append(float(q.sum()))
    return np.array(out)

def js(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)

def main():
    R={k:reset(*v) for k,v in RESETS.items()}
    models={}; maxerr=0.;maxinteraction=0.; laws={}
    for interaction,kind in itertools.product((False,True),('shadow','echo','wake','mixed')):
        key=kind+('_interaction' if interaction else '_additive')
        p=.05+.2*M+.2*S+( .08*M*S if interaction else 0)
        B=[kernel(kind,y) for y in (0,1)]
        P=(1-p[:,None])*B[0]+p[:,None]*B[1]
        pi=stationary(P)
        assert np.max(abs(P.sum(1)-1))<TOL and np.all((p>=0)&(p<=1))
        if kind=='shadow':assert np.max(abs(pi-np.ones(6)/6))<TOL
        d=pi@B[1]-pi@B[0]
        a,b,c=.2*(d@M),.2*(d@S),(.08*(d@(M*S)) if interaction else 0.)
        natural=[]
        for y in (0,1):
            w=pi*(p if y else 1-p); natural.append(w@B[y]/w.sum())
        data={}
        for name,(ra,rs) in RESETS.items():
            r=R[name]; assert np.max(abs(r.sum(1)-1))<TOL
            before=[pi@B[y]@r for y in (0,1)]
            ctrl=pi@r
            obs=[natural[y]@r for y in (0,1)]
            curves={'forced1_minus_forced0':[],'forced1_minus_no_probe':[],'forced0_minus_no_probe':[],'observed1_minus_observed0':[],'baseline_error':[]}
            for lag in range(6):
                power=np.linalg.matrix_power(P,lag)
                curves['forced1_minus_forced0'].append(float((before[1]-before[0])@power@p))
                curves['forced1_minus_no_probe'].append(float((before[1]-ctrl)@power@p))
                curves['forced0_minus_no_probe'].append(float((before[0]-ctrl)@power@p))
                curves['observed1_minus_observed0'].append(float((obs[1]-obs[0])@power@p))
                curves['baseline_error'].append(float(ctrl@power@p))
            expected=(1-ra)*a+(1-rs)*b+(1-ra)*(1-rs)*c
            err=abs(expected-curves['forced1_minus_forced0'][0]); maxerr=max(maxerr,err)
            maxinteraction=max(maxinteraction,abs((1-ra)*a+(1-rs)*b-curves['forced1_minus_forced0'][0]))
            data[name]=curves
            for prep,v in [('natural',ctrl),('forced0',before[0]),('forced1',before[1])]:laws[(key,name,prep)]=words(v,p,B)
        X2=np.array([[1-RESETS[n][0],1-RESETS[n][1]] for n in ('sham','agent','soil')])
        X3=np.column_stack([X2,np.prod(X2,axis=1)])
        response=np.array([data[n]['forced1_minus_forced0'][0] for n in ('sham','agent','soil')])
        fit2=np.linalg.lstsq(X2,response,rcond=None)[0]
        fit3=np.linalg.solve(X3,response)
        # Incorrectly assume agent reset erases agent only, soil reset soil only.
        naive=np.array([data['soil']['forced1_minus_forced0'][0],data['agent']['forced1_minus_forced0'][0]])
        models[key]={'emission':p,'B0':B[0],'B1':B[1],'P':P,'stationary':pi,'error_rate':pi@p,'lag1_covariance':(pi*p)@B[1]@p-(pi@p)**2,'contributions':[a,b,c],'responses':data,'known_two_component_fit':fit2,'two_component_residual':float(np.linalg.norm(X2@fit2-response)),'known_three_component_fit':fit3,'naive_perfect_reset_allocation':naive,'naive_error_vs_agent_soil_contributions':naive-np.array([a,b])}
    allkeys=sorted(models)
    comparisons={}
    for names in [('sham',),('sham','shared'),('sham','agent','soil')]:
        label='+'.join(names)
        vectors={k:np.concatenate([laws[k,n,prep] for n in names for prep in ('natural','forced0','forced1')]) for k in allkeys}
        tv={}
        sets={}
        for a,b in itertools.combinations(allkeys,2):
            # Average per-context TV; a design selects contexts uniformly.
            tv[a+'|'+b]=float(.5*np.abs(vectors[a]-vectors[b]).sum()/(len(names)*3))
        for k in allkeys:sets[k]=[j for j in allkeys if np.max(abs(vectors[k]-vectors[j]))<=TOL]
        comparisons[label]={'average_context_TV':tv,'candidate_sets':sets,'minimum_pair_TV':min(tv.values())}
    Xdiv=np.array([[1,1],[.2,.9],[.9,.2]])
    Xconf=np.array([[1,1],[.4,.4],[.4,.4]])
    Xint=np.column_stack([Xdiv,np.prod(Xdiv,axis=1)])
    ambiguity={'matrix':Xconf,'rank':int(np.linalg.matrix_rank(Xconf,tol=TOL)),'example_contributions':[[.1,0],[0,.1]],'same_responses':bool(np.allclose(Xconf@np.array([.1,0]),Xconf@np.array([0,.1]),atol=TOL)),'scope':'Arbitrary two-component first-outcome response summary; not full-word-law equivalence.'}
    checks={'operator_algebra':maxerr<TOL,'additive_recovery':all(np.max(abs(v['known_two_component_fit']-v['contributions'][:2]))<TOL for k,v in models.items() if k.endswith('additive')),'interaction_recovery':all(np.max(abs(v['known_three_component_fit']-v['contributions']))<TOL for v in models.values()),'two_component_interaction_misspecification_detected':models['mixed_interaction']['two_component_residual']>1e-5,'confounded_summary_ambiguous':ambiguity['same_responses'],'shadow_has_zero_probe_contrast':abs(models['shadow_additive']['responses']['sham']['forced1_minus_forced0'][0])<TOL,'shadow_reset_changes_baseline':abs(models['shadow_additive']['responses']['soil']['baseline_error'][0]-models['shadow_additive']['error_rate'])>1e-3}
    result={'scope':'Exact finite enumeration in floating point, no Monte Carlo; known kernels/operators','protocol_sha256':hashlib.sha256((ROOT/'PROTOCOL.md').read_bytes()).hexdigest(),'states':STATES,'resets':{k:{'rates':RESETS[k],'matrix':v} for k,v in R.items()},'models':models,'word_length':4,'observation_laws':{'|'.join(k):v for k,v in laws.items()},'full_candidate_law_comparisons':comparisons,'identification':{'diverse_rank':int(np.linalg.matrix_rank(Xdiv,tol=TOL)),'diverse_condition_number':float(np.linalg.cond(Xdiv)),'interaction_rank':int(np.linalg.matrix_rank(Xint,tol=TOL)),'interaction_condition_number':float(np.linalg.cond(Xint)),'confounded':ambiguity},'max_operator_algebra_error':maxerr,'max_omitted_interaction_error':maxinteraction,'checks':checks}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,default=js,indent=2)+'\n')
    print(json.dumps({'checks':checks,'models':{k:{'contributions':v['contributions'],'two_component_residual':v['two_component_residual'],'naive_bias':v['naive_error_vs_agent_soil_contributions'].tolist()} for k,v in models.items()},'minimum_word_TV':{k:v['minimum_pair_TV'] for k,v in comparisons.items()},'identification':result['identification']},default=js,indent=2))
    assert all(checks.values()),checks

if __name__=='__main__':main()
