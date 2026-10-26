#!/usr/bin/env python3
"""Independent RB-C exact replay. Never imports or reads the experiment implementation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
PROBES = {'CONTEXT': (F(-1), F(1)), 'WEAK': (F(9,10), F(1)),
          'SIGNAL': (F(1), F(-1)), 'COPY': (F(1), F(1))}
BIASES = {'ZERO': (F(0), F(0)), 'COMMON': (F(3,25), F(3,25)),
          'OPPOSED': (F(3,25), F(-3,25))}
CONTRACTS = ('BLIND', 'WIDE', 'REFERENCE', 'BAD_REFERENCE')
RHOS = (F(1,2), F(1), F(2))

def dot(v, w):
    return sum((x*y for x,y in zip(v,w)), F(0))

def vector_minus(v,w):
    return tuple(x-y for x,y in zip(v,w))

def serialize(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {k:serialize(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [serialize(v) for v in value]
    return value

def rebuild(probe,bias,contract,rho, coefficients=None, biases=None):
    alpha,beta=PROBES[probe] if coefficients is None else coefficients
    ba,bb=BIASES[bias] if biases is None else biases
    ya,yb=alpha+ba,beta+bb
    if contract in ('BLIND','WIDE'):
        allowance=F(1,50) if contract=='BLIND' else F(3,20)
        ra=rb=None
        ia=(ya-allowance,ya+allowance)
        ib=(yb-allowance,yb+allowance)
        ah,bh=ya,yb
        cost=0
        bias_valid=abs(ba)<=allowance and abs(bb)<=allowance
    else:
        ra,rb=(ba,bb) if contract=='REFERENCE' else (F(0),F(0))
        allowance=F(1,100)
        ia=(ya-ra-allowance,ya-ra+allowance)
        ib=(yb-rb-allowance,yb-rb+allowance)
        ah,bh=ya-ra,yb-rb
        cost=2
        bias_valid=abs(ra-ba)<=allowance and abs(rb-bb)<=allowance
    gap=(ib[0]-ia[1],ib[1]-ia[0])
    covered=ia[0]<=alpha<=ia[1] and ib[0]<=beta<=ib[1]
    gate=gap[0]>0 or gap[1]<0
    h=bh-ah
    da,db=ah-alpha,bh-beta
    # Explicit orthogonal 2D physical model, n=(rho,0), s=(0,1).
    n,s=(rho,F(0)),(F(0),F(1))
    D=tuple(x+y for x,y in zip(n,s))
    Dprime=tuple(alpha*x+beta*y for x,y in zip(n,s))
    reconstructed=None if h==0 else tuple((x-ah*y)/h for x,y in zip(Dprime,D))
    error=None if reconstructed is None else vector_minus(reconstructed,s)
    squared_error=None if error is None else dot(error,error)/dot(s,s)
    ea=max(abs(ah-z) for z in ia)
    eb=max(abs(bh-z) for z in ib)
    # Corner maximization evaluates task error on the supplied coefficient rectangle.
    # This is the fixed point denominator, not a denominator interval.
    corner_errors=[]
    if h:
        for actual_a in ia:
            for actual_b in ib:
                alt_Dprime=tuple(actual_a*x+actual_b*y for x,y in zip(n,s))
                alt_hat=tuple((x-ah*y)/h for x,y in zip(alt_Dprime,D))
                alt_error=vector_minus(alt_hat,s)
                corner_errors.append(dot(alt_error,alt_error)/dot(s,s))
    envelope=max(corner_errors) if corner_errors else None
    formula=None if not h else ((da*rho)**2+db**2)/h**2
    envelope_formula=None if not h else ((ea*rho)**2+eb**2)/h**2
    assert squared_error==formula
    assert envelope==envelope_formula
    assert bias_valid==covered
    assert not (covered and h and squared_error>envelope)
    raw=bool(gate and envelope is not None and envelope<=F(1,100))
    return locals()

# Schema-specific comparisons are defined below only after reviewing SCHEMA.md.

def interval(pair):
    return {'lower':pair[0], 'upper':pair[1]}

def expected_row(x):
    alpha,beta,ba,bb=x['alpha'],x['beta'],x['ba'],x['bb']
    ia,ib=x['ia'],x['ib']
    h,gate=x['h'],x['gate']
    err,env=x['squared_error'],x['envelope']
    refs=x['contract'] in ('REFERENCE','BAD_REFERENCE')
    r_a,r_b=x['ra'],x['rb']
    radius=x['allowance']
    return serialize({
        'row_id':f"{x['probe']}:{x['bias']}:{x['contract']}:rho={x['rho']}",
        'probe':x['probe'],'bias_case':x['bias'],'contract':x['contract'],'rho':x['rho'],
        'world':{'world_id':f"{x['probe']}:{x['bias']}",'alpha':alpha,'beta':beta,
                 'bias_a':ba,'bias_b':bb,'true_gap':beta-alpha,'true_nonsingular':alpha!=beta,
                 'orthogonal_n_s':True,'signal_norm':F(1),'nuisance_norm':x['rho']},
        'observations':{'y_a':x['ya'],'y_b':x['yb'],'r_a':r_a,'r_b':r_b},
        'method':{'declared_radius':radius,'primary_scalar_measurements':2,
                  'extra_scalar_measurements':x['cost'],'total_scalar_measurements':2+x['cost'],
                  'reference_role_authority_supplied':refs,
                  'declared_bias_intervals':{'a':interval(((r_a or F(0))-radius,(r_a or F(0))+radius)),
                                             'b':interval(((r_b or F(0))-radius,(r_b or F(0))+radius))},
                  'actual_bias_contract_valid':x['bias_valid']},
        'coefficient_intervals':{'a':interval(ia),'b':interval(ib)},
        'compatible_gap_interval':interval(x['gap']),
        'coverage':{'a':ia[0]<=alpha<=ia[1],'b':ib[0]<=beta<=ib[1],
                    'both':x['covered'],'true_gap':x['gap'][0]<=beta-alpha<=x['gap'][1]},
        'gate':{'intervals_nonempty':True,'gap_strictly_excludes_zero':gate,
                'status':'PASS' if gate else 'WITHHOLD','reason':'gap_excludes_zero' if gate else 'gap_contains_zero'},
        'point':{'alpha_hat':x['ah'],'beta_hat':x['bh'],'h':h,'delta_a':x['da'],'delta_b':x['db'],
                 'available':bool(h),'offered':bool(h and gate),'unavailable_reason':None if h else 'zero_point_gap',
                 'nuisance_coefficient':-x['da']/h if h else None,
                 'signal_gain':(beta-alpha-x['da'])/h if h else None,'relative_error_squared':err},
        'envelope':{'error_radius_a':x['ea'],'error_radius_b':x['eb'],'available':bool(h),
                    'relative_error_squared_upper_bound':env,
                    'actual_error_within_envelope':None if not h else err<=env,
                    'condition_satisfied':x['covered']},
        'raw_budget':{'relative_error_limit':F(1,10),'squared_limit':F(1,100),
                      'actual_point_meets_budget':None if not h else err<=F(1,100),
                      'raw_certified':x['raw'], 'false_raw_certificate':bool(x['raw'] and err>F(1,100))}
    })

def counts(xs):
    return {
        'rows':len(xs), 'coefficient_coverage':sum(x['covered'] for x in xs),
        'actual_bias_contract_valid':sum(x['bias_valid'] for x in xs),
        'gate_pass':sum(x['gate'] for x in xs),'gate_withhold':sum(not x['gate'] for x in xs),
        'empty_intervals':0,'true_nonsingular':sum(x['alpha']!=x['beta'] for x in xs),
        'true_nonsingular_withheld':sum(x['alpha']!=x['beta'] and not x['gate'] for x in xs),
        'true_singular_gate_pass':sum(x['alpha']==x['beta'] and x['gate'] for x in xs),
        'point_available':sum(bool(x['h']) for x in xs),'point_unavailable':sum(not x['h'] for x in xs),
        'point_offered':sum(bool(x['h'] and x['gate']) for x in xs),
        'exact_point_recovery':sum(x['h']!=0 and x['squared_error']==0 for x in xs),
        'conditional_envelope_checks':sum(bool(x['covered'] and x['h']) for x in xs),
        'conditional_envelope_violations':sum(bool(x['covered'] and x['h'] and x['squared_error']>x['envelope']) for x in xs),
        'uncovered_envelope_violations':sum(bool(not x['covered'] and x['h'] and x['squared_error']>x['envelope']) for x in xs),
        'actual_point_meets_raw_budget':sum(bool(x['h'] and x['squared_error']<=F(1,100)) for x in xs),
        'raw_certified':sum(x['raw'] for x in xs),
        'false_raw_certificates':sum(bool(x['raw'] and x['squared_error']>F(1,100)) for x in xs)
    }

def compare(expected, actual, path, checks, errors):
    """Compare expected exact subset, permitting explanatory prose/display fields."""
    if isinstance(expected,dict):
        if not isinstance(actual,dict):
            errors.append({'path':path,'expected':expected,'actual':actual}); return
        for key,value in expected.items():
            if key not in actual: errors.append({'path':f'{path}.{key}','error':'missing'})
            else: compare(value,actual[key],f'{path}.{key}',checks,errors)
    else:
        checks[0]+=1
        if type(expected) is not type(actual) or expected!=actual:
            errors.append({'path':path,'expected':expected,'actual':actual})

def main():
    rows=json.loads((ROOT/'run/ROWS.json').read_text())
    summary=json.loads((ROOT/'run/SUMMARY.json').read_text())
    checks,errors=[0],[]
    xs=[rebuild(p,b,c,r) for p in PROBES for b in BIASES for c in CONTRACTS for r in RHOS]
    expected=[expected_row(x) for x in xs]
    by_id={r['row_id']:r for r in rows}
    compare(144,len(rows),'rows.length',checks,errors)
    compare(144,len(by_id),'rows.unique_ids',checks,errors)
    for want in expected:
        rid=want['row_id']
        compare(want,by_id.get(rid),f'rows[{rid}]',checks,errors)
    expected_summary={'authored_exact_toy':True,'independent_repetitions':0,'probability_claims':False,
                      'totals':counts(xs)}
    for field,key,values in (('by_contract','contract',CONTRACTS),('by_probe','probe',PROBES),
                             ('by_bias','bias',BIASES),('by_rho','rho',RHOS)):
        expected_summary[field]={str(v):counts([x for x in xs if x[key]==v]) for v in values}
    expected_summary['by_contract_and_bias']={c:{b:counts([x for x in xs if x['contract']==c and x['bias']==b]) for b in BIASES} for c in CONTRACTS}
    compare(expected_summary,summary,'summary',checks,errors)
    # Independence of primary observations from contract and rho is directly checked.
    for p in PROBES:
        for b in BIASES:
            observations={(r['observations']['y_a'],r['observations']['y_b']) for r in rows if r['probe']==p and r['bias_case']==b}
            compare(1,len(observations),f'shared_primary.{p}.{b}',checks,errors)
    ambiguous=summary['ambiguous_worlds']
    compare(False,ambiguous['included_in_main_grid_counts'],'ambiguity.excluded',checks,errors)
    compare(True,ambiguous['primary_observations_identical'],'ambiguity.primary_same',checks,errors)
    compare(True,ambiguous['valid_reference_observations_differ'],'ambiguity.references_differ',checks,errors)
    ambiguity_expected=[]
    for label,coeff,bias in [('OBSERVED_COPY',(F(1),F(1)),(F(3,25),-F(3,25))),
                             ('ALTERNATIVE',(F(28,25),F(22,25)),(F(0),F(0)))]:
        worlds=ambiguous['worlds']
        world=next(w for w in worlds if w['label']==label) if isinstance(worlds,list) else worlds[label]
        a,b=coeff;ba,bb=bias
        want={'label':label,'alpha':a,'beta':b,'bias_a':ba,'bias_b':bb,
              'true_gap':b-a,'true_nonsingular':a!=b,'y_a':a+ba,'y_b':b+bb}
        compare(serialize(want),world,f'ambiguity.{label}',checks,errors)
        diag=world['contract_diagnostics_at_rho_one']
        for c in CONTRACTS:
            actual=next(r for r in diag if r['contract']==c) if isinstance(diag,list) else diag[c]
            z=rebuild(actual['probe'],'AMBIGUITY',c,F(1),coeff,bias)
            wantrow=expected_row(z)
            compare(wantrow,actual,f'ambiguity.{label}.{c}',checks,errors)
            ambiguity_expected.append(wantrow)
    # Exact world calculation demonstrates identical primaries but different singularity.
    compare((F(28,25),F(22,25)),(F(1)+F(3,25),F(1)-F(3,25)),'ambiguity.exact_readings',checks,errors)
    audit={'status':'PASS' if not errors else 'FAIL','independence':'Only PROTOCOL.md and SCHEMA.md read; experiment.py never read/imported.',
           'exact_leaf_comparisons':checks[0],'errors':errors,'expected_rows':expected,
           'expected_summaries':expected_summary,'expected_ambiguity_diagnostics':ambiguity_expected,
           'vector_validation':{'rows_checked':144,'method':'n=(rho,0), s=(0,1), explicit reconstruction and dot product; envelope independently maximized over four rectangle corners',
            'conditional_claim':'Valid under coefficient coverage, orthogonality and known norm ratio; fixed point denominator h.',
            'orthogonality_supplied_not_inferred':True},
           'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (ROOT/'review/AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    lines=['# Independent exact audit', '',f"Status: **{audit['status']}**. Rebuilt all 144 rows and every grouped count independently using Fraction; compared {checks[0]} exact leaves. Main implementation was neither read nor imported.",
           '', 'The reconstruction was also computed directly in two dimensions with n=(rho,0), s=(0,1). Its squared error was a vector dot product. The envelope was independently maximized over all four coefficient-rectangle corners, then checked against the stated algebraic formula. All reference measurement costs and shared primary readings were checked.',
           '', 'The envelope is conditional on coefficient coverage, orthogonality and the known norm ratio. Those are supplied assumptions. Corner maximization keeps the point denominator h fixed; it does not claim uniform inversion stability over all compatible worlds. The audit evaluates false certificates against the authored actual model, without probability claims.',
           '', 'Both observed-equivalent worlds and all eight contract diagnostics were rebuilt: primaries are exactly (28/25,22/25), while the true gaps are 0 and -6/25. Valid references differ only because additional authoritative observations were supplied.',
           '', '| Contract | Rows | Covered | Gate pass | Raw certified | False raw |', '|---|---:|---:|---:|---:|---:|']
    for c,v in expected_summary['by_contract'].items():
        lines.append(f"| {c} | {v['rows']} | {v['coefficient_coverage']} | {v['gate_pass']} | {v['raw_certified']} | {v['false_raw_certificates']} |")
    lines+=['', 'All expected rows and summaries, individual mismatches, exact check count and auditor hash are retained in AUDIT.json. Display square roots and explanatory prose are not treated as exact arithmetic; their underlying rational quantities are checked.']
    if errors: lines+=['','## Mismatches','',json.dumps(errors,indent=2)]
    (ROOT/'review/AUDIT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'status':audit['status'],'exact_leaf_comparisons':checks[0],'mismatches':len(errors)}))
    return 0 if not errors else 1

if __name__=='__main__':
    raise SystemExit(main())
