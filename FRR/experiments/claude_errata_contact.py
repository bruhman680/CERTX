"""Source-isolated checks of the supplied bundle; does not edit or rerun its originals."""
import ast
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'lineage/sources/claude-errata-intake-2026-10-22'
OUT=ROOT/'evaluation/claude-errata-intake-v1'


def definitions(name, assignments=()):
    tree=ast.parse((SRC/name).read_text())
    nodes=[]
    for node in tree.body:
        if isinstance(node,ast.FunctionDef):nodes.append(node)
        elif isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in assignments for t in node.targets):nodes.append(node)
    env={'np':np,'itertools':itertools}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SRC/name),'exec'),env)
    return env


def main():
    dest=OUT/'DIAGNOSTICS.json'
    if dest.exists():raise SystemExit('Refusing to overwrite diagnostics')
    env=definitions('erase_gate_unequal_carriers.py');contrast=env['contrast'];ck=env['ck'];prony=env['prony']
    F,P=.128,.06
    pure=contrast(.9,.8,.4,0,.1)
    private=contrast(.9,.8,0,.4,.1)
    adjusted_wP=.4*(.9-.5)/(.8-.5)
    matched=contrast(.9,.8,0,adjusted_wP,.1)
    equal_rates=[ck(F,P,.5,.5,k) for k in range(4)]
    a,b=.9,.1;c=[F*a**k+P*b**k for k in range(4)]
    moment_det=c[0]*c[2]-c[1]**2
    inverse={'unequal_original_pure_keep':pure,'unequal_original_gated_private_keep':private,
             'original_P1_equality_holds':bool(np.isclose(pure,private)),
             'new_matched_private_route_weight':adjusted_wP,'new_matched_private_keep':matched,
             'moment_determinant':moment_det,'moment_expected':F*P*(a-b)**2,
             'amplitude_vandermonde_determinant':b-a,
             'equal_rates_only_sum':[float(x) for x in equal_rates]}
    rng=np.random.default_rng(12345);samples=[]
    for s,d in ((.9,.1),(.8,.3),(.7,.5),(.6,.55),(.6,.58)):
        cs=np.array([ck(F,P,s,d,k) for k in range(4)])
        counts={x:0 for x in ['valid','linear_solve_failure','complex','rates_outside_unit','nonphysical_amplitudes']}
        original_accepted=0;accepted_invalid=0;example=None
        for _ in range(400):
            hat=np.array([rng.binomial(200000,.5+x)/200000-.5 for x in cs])
            try:
                old_roots,old_amps=prony(hat)
                old_ok=bool(np.all(np.isfinite(old_amps)))
            except Exception:old_ok=False
            original_accepted+=int(old_ok)
            try:
                rec=np.linalg.solve([[hat[1],hat[0]],[hat[2],hat[1]]],[hat[2],hat[3]])
                roots=np.roots([1,-rec[0],-rec[1]])
                if np.max(np.abs(roots.imag))>1e-10:category='complex'
                else:
                    roots=np.sort(roots.real)
                    amps=np.linalg.solve([[1,1],[roots[0],roots[1]]],hat[:2])
                    if np.any(roots < -1e-10) or np.any(roots > 1+1e-10):category='rates_outside_unit'
                    elif not np.all(np.isfinite(amps)) or np.any(amps < -1e-10) or amps.sum() > .5+1e-10:category='nonphysical_amplitudes'
                    else:category='valid'
            except (np.linalg.LinAlgError,ValueError):category='linear_solve_failure'
            counts[category]+=1
            if old_ok and category!='valid':
                accepted_invalid+=1
                if example is None:example={'category':category,'measurements':hat.tolist(),'original_roots':old_roots.tolist(),'original_amplitudes':old_amps.tolist()}
        samples.append({'s':s,'d':d,'gap':abs(s-d),'replicates':400,'original_accepted':original_accepted,'original_accepted_but_invalid':accepted_invalid,'classification':counts,'example':example})
    thermo=definitions('boltz_check.py',('N','dec','E'))
    thermal=[]
    for beta in (.5,1.,2.,5.):
        k=thermo['rates'](beta);S=k.sum(1);boltz=np.exp(-beta*thermo['E']);boltz/=boltz.sum()
        old=k/(S+1)[:,None];old[np.diag_indices(8)]=1/(S+1)
        fixed=k/(1.05*S.max());fixed[np.diag_indices(8)]=1-fixed.sum(1)
        def stationary(matrix):
            M=matrix.T-np.eye(8);M[-1]=1;rhs=np.zeros(8);rhs[-1]=1
            return np.linalg.solve(M,rhs)
        pi_old=stationary(old);pi_fixed=stationary(fixed)
        predicted=boltz*(S+1);predicted/=predicted.sum()
        thermal.append({'beta':beta,'old_error':float(np.max(abs(pi_old-boltz))),
                        'old_predicted_error':float(np.max(abs(pi_old-predicted))),
                        'fixed_error':float(np.max(abs(pi_fixed-boltz))),
                        'fixed_stationarity_residual':float(np.max(abs(boltz@fixed-boltz)))})
    shadow=definitions('shadow_echo_v2.py',('K',));law=shadow['word_law']
    laws={w:law(8,w,None) for w in ['frozen','echo']}
    shadow_results={'n8_TV':shadow['tv'](laws['frozen'],laws['echo']),
                    'normalization':{w:sum(v.values()) for w,v in laws.items()},
                    'finite_numeric_hankel_rank':{w:int(shadow['hankel'](w)) for w in laws}}
    checks={'unequal_P1_not_matched':not inverse['original_P1_equality_holds'],
            'new_calibration_restores_matched_signal':bool(np.isclose(pure,matched)),
            'moment_determinant_identity':bool(np.isclose(moment_det,F*P*(a-b)**2)),
            'original_accepts_nonphysical_fits':any(x['original_accepted_but_invalid'] for x in samples),
            'direct_Boltzmann_checks':all(x['fixed_error']<1e-12 and x['old_predicted_error']<1e-12 for x in thermal),
            'word_laws_normalize':all(abs(x-1)<1e-12 for x in shadow_results['normalization'].values()),
            'both_numeric_ranks_four':set(shadow_results['finite_numeric_hankel_rank'].values())=={4}}
    result={'scope':'Targeted development diagnostics; same conceptual ancestry, no physical/agent transfer test',
            'inverse':inverse,'sampling_model':'Original unequal-carrier binomial sequence, same seed/parameters, new physical-admissibility classification; c=P(correct)-0.5 so nonnegative amplitudes sum<=0.5',
            'sampling':samples,'thermal_direct_solve':thermal,'shadow_echo':shadow_results,'checks':checks,
            'diagnostic_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'fits':[{k:x[k] for k in ['gap','original_accepted','original_accepted_but_invalid','classification']} for x in samples],'shadow':shadow_results,'thermal':thermal},indent=2))
    if not all(checks.values()):raise SystemExit('Diagnostic check failed; preserve and investigate')


if __name__=='__main__':main()
