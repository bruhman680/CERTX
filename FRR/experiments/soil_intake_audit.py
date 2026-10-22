"""Independent transition/analytic stationary checks; shared toy definitions, no new carrier experiment."""
import ast
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'lineage/sources/claude-soil-intake-2026-10-21/soil_toy.py'
OUT=ROOT/'evaluation/soil-intake-v1'


def kl(p,q):
    p=np.clip(p,1e-12,1-1e-12);q=np.clip(q,1e-12,1-1e-12)
    return p*np.log(p/q)+(1-p)*np.log((1-p)/(1-q))


def main():
    if (OUT/'AUDIT.json').exists():raise SystemExit('Refusing overwrite')
    # Load function definitions only: do not repeat source tuning or top-level execution.
    env={'np':np,'itertools':itertools,'alpha':.3,'STATES':[(s,l) for s in (0,1) for l in (0,1)],'NS':4}
    env['idx']={x:i for i,x in enumerate(env['STATES'])}
    defs=[x for x in ast.parse(SRC.read_text()).body if isinstance(x,ast.FunctionDef)]
    exec(compile(ast.Module(body=defs,type_ignores=[]),str(SRC),'exec'),env)
    R,C,L,U=.2,.032,.02,.5
    H=R+C/(R-L*(1-U));h=(R-L)/(H-L)
    D=L*U*(1-h)/(h*(1-H))
    configs={'SH':{'P':(R-np.sqrt(C),R+np.sqrt(C))},'EC':{'c':C/(R*(1-R)),'p0':R*(1-C/(R*(1-R)))},'WK':{'P':(L,H),'u':U,'d':D}}
    rows=[];laws={};all_decomp=[]
    for world,kw in configs.items():
        p=np.array([kw['p0']+kw['c']*l if world=='EC' else kw['P'][s] for s,l in env['STATES']])
        M=np.zeros((2,4,4));forced=np.zeros((4,4))
        for i,(s,l) in enumerate(env['STATES']):
            for outcome in (0,1):
                # Rebuild as a high-soil probability, not the source's successor dictionaries.
                high=float(s)
                if world=='WK':high=s+(1-s)*kw['u'] if outcome else s*(1-kw['d'])
                prob=p[i] if outcome else 1-p[i]
                for snext in (0,1):
                    route=high if snext else 1-high;j=2*snext+outcome
                    M[outcome,i,j]=prob*route
                    if outcome:forced[i,j]=route
        T=M.sum(0)
        if world=='SH':pi=np.array([.5*(p[i] if l else 1-p[i]) for i,(s,l) in enumerate(env['STATES'])])
        elif world=='EC':pi=np.array([.5*(R if l else 1-R) for s,l in env['STATES']])
        else:
            eq=T.T-np.eye(4);eq[-1]=1;rhs=np.array([0.,0.,0.,1.]);pi=np.linalg.solve(eq,rhs)
        sourceM,sourceD,sourcep=env['build'](world,**kw)
        c=[float(pi@M[1]@np.linalg.matrix_power(T,k-1)@p-R*R) for k in range(1,7)]
        do=pi@forced;obs=pi@M[1]/R
        effects={key:[float(v@np.linalg.matrix_power(T,k-1)@p-R) for k in range(1,7)] for key,v in [('do',do),('observe',obs)]}
        words={}
        for word in itertools.product((0,1),repeat=6):
            v=pi.copy()
            for o in word:v=v@M[o]
            words[word]=float(v.sum())
        laws[world]=words
        parts={}
        for probe in [False,True]:
            states=[(do if probe else pi,.44 if probe else R)];risks=[]
            for lag in range(6):
                latent=predictive=unobserved=0.
                for v,q in states:
                    mass=v.sum()
                    if mass<=0:continue
                    pp=float(v@p/mass)
                    latent+=float(v@kl(p,q))
                    predictive+=mass*float(kl(pp,q))
                    unobserved+=float(v@kl(p,pp))
                risks.append({'lag':lag+1,'latent_oracle_KL':latent,'posterior_predictive_regret':predictive,'hidden_state_information_term':unobserved,'decomposition_residual':latent-predictive-unobserved})
                states=[(v@M[o],.7*q+.3*o) for v,q in states for o in (0,1)]
            sourceRisk=env['ewma_excess'](world,probe,**kw)
            parts['probe' if probe else 'control']=risks
            all_decomp.extend(risks)
            assert max(abs(a['latent_oracle_KL']-b) for a,b in zip(risks,sourceRisk))<1e-10
        rows.append({'world':world,'parameters':kw,'stationary':pi.tolist(),'stationarity_residual':float(np.max(abs(pi@T-pi))),
                     'transition_difference_to_source':float(np.max(abs(M-np.array(sourceM)))),'forced_transition_difference':float(np.max(abs(forced-sourceD))),
                     'rate':float(pi@p),'covariances':c,'effects':effects,'EWMA_decomposition':parts,
                     'soil_reset_baseline_rate':float(np.array([pi[0]+pi[2],pi[1]+pi[3],0,0])@p)})
    tv={a+'-'+b:.5*sum(abs(laws[a][w]-laws[b][w]) for w in laws[a]) for a,b in [('SH','EC'),('SH','WK'),('EC','WK')]}
    text=(OUT/'RUN.stdout.txt').read_text();supplied=(SRC.parent/'soil_toy_output.txt').read_text()
    spectral_gap=L*U+(1-H)*D
    checks={'rebuild_transitions_agree':all(x['transition_difference_to_source']<1e-14 and x['forced_transition_difference']<1e-14 for x in rows),
            'stationary_rate_cov_match':all(x['stationarity_residual']<1e-12 and abs(x['rate']-R)<1e-12 and abs(x['covariances'][0]-C)<1e-12 for x in rows),
            'all_passive_word_laws_differ':all(v>1e-8 for v in tv.values()),
            'do_alone_distinct_in_supplied_family':len(set(round(x['effects']['do'][0],10) for x in rows))==3,
            'KL_decomposition_identity':max(abs(x['decomposition_residual']) for x in all_decomp)<1e-12}
    checks={k:bool(v) for k,v in checks.items()}
    result={'scope':'Same parameterization, separately coded transition/direct stationary audit; not a different-parameterization replication or real-world carrier identification',
            'analytic_tuning':{'high':H,'d':D,'high_stationary_probability':h,'soil_spectral_gap':spectral_gap,'soil_subdominant_eigenvalue':1-spectral_gap},
            'rows':rows,'length6_passive_TV':tv,'supplied_stdout_matches_exactly':text==supplied,'supplied_stdout_matches_ignoring_edge_whitespace':text.strip()==supplied.strip(),
            'checks':checks,'audit_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'analytic_tuning':result['analytic_tuning'],'passive_TV':tv,'stdout_match':text.strip()==supplied.strip(),
                      'lag1_risk_decomposition':{x['world']:{k:v[0] for k,v in x['EWMA_decomposition'].items()} for x in rows}},indent=2))
    if not all(checks.values()):raise SystemExit('Check failed; preserve')

if __name__=='__main__':main()
