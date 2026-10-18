"""RR2: prediction versus reset-protocol identification, finite exact enumeration."""
import hashlib
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evaluation/reset-reader-rr2'
spec = importlib.util.spec_from_file_location('rr1_helpers', ROOT/'experiments/reset_reader_study.py')
rr1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rr1)


def mix(levels, weights):
    return {word: sum(weights[z]*levels[z][word] for z in range(5)) for word in levels[0]}


def difference(left, right):
    return max(float(abs(left[word]-right[word]).max()) for word in left)


def run():
    start = time.perf_counter()
    settings = json.loads((OUT/'SETTINGS.json').read_text())
    models = json.loads((ROOT/settings['models']).read_text())
    tol = settings['tolerance']
    aggregate_rows, component_rows = [], []
    maxima = {k: 0. for k in ['mass_error','joint_error','risk_identity_error','aggregate_order_violation',
        'collapsed_law_error','equal_marginal_protocol_law_error','uniform_identity_error',
        'identification_bound_violation','identification_monotonicity_violation','balanced_bound_error',
        'h1_predictive_error','h1_identification_plateau_error']}
    names = ('metadata','population','uniform','natural')
    for model, table in models.items():
        kernel = np.asarray(table['kernel'], dtype=float)
        for h in table['h']:
            p = rr1.joint_chain(kernel,h)
            pi = rr1.stationary(kernel,h,p)
            priors = np.array([pi[:2]/pi[:2].sum(),pi.reshape(2,2).sum(0),[1.,0.],[0.,1.],[.5,.5]])
            for population, declared in settings['populations'].items():
                w = np.array(declared,dtype=float)
                if min(w)<=0 or abs(w.sum()-1)>tol:
                    raise ValueError('Invalid population weights')
                levels = [{(0,): rho.copy()} for rho in priors]
                collapsed = {(0,): w @ priors}
                separate_uniform = {(0,): np.array([.5,.5])}
                bound = float(np.max(w[:,None]*priors,axis=0).sum())
                previous_accuracy, first_transition_accuracy = None, None
                for t in settings['times']:
                    actual_mix = mix(levels,w)
                    uniform_mix = mix(levels,np.full(5,.2))
                    maxima['collapsed_law_error'] = max(maxima['collapsed_law_error'],difference(actual_mix,collapsed))
                    fixed_pair = {word:.5*levels[2][word]+.5*levels[3][word] for word in levels[0]}
                    maxima['equal_marginal_protocol_law_error'] = max(maxima['equal_marginal_protocol_law_error'],difference(levels[4],fixed_pair),difference(levels[4],separate_uniform))
                    maxima['mass_error'] = max(maxima['mass_error'],abs(sum(a.sum() for a in actual_mix.values())-1))
                    initial = np.r_[w@priors,[0.,0.]]
                    joint = initial @ np.linalg.matrix_power(p,t)
                    enumerated_joint = np.zeros(4)
                    risk = [{name:0. for name in names} for _ in range(5)]
                    identity = [{name:0. for name in names} for _ in range(5)]
                    accuracy = 0.
                    for word, mixture_mass in actual_mix.items():
                        emissions = kernel[:,word[-1],:]
                        enumerated_joint[2*word[-1]:2*word[-1]+2] += mixture_mass
                        accuracy += max(w[z]*levels[z][word].sum() for z in range(5))
                        qs = {name: (weights/weights.sum())@emissions for name,weights in
                              [('population',mixture_mass),('uniform',uniform_mix[word]),('natural',levels[0][word])]}
                        for z in range(5):
                            a = levels[z][word]
                            mass = a.sum()
                            matched = (a/mass)@emissions
                            predictions = dict(qs,metadata=matched)
                            for name,q in predictions.items():
                                risk[z][name] += sum(a[e]*rr1.kl(emissions[e],q) for e in (0,1))
                                identity[z][name] += mass*rr1.kl(matched,q)
                    maxima['joint_error'] = max(maxima['joint_error'],float(abs(joint-enumerated_joint).max()))
                    aggregate = {name:float(sum(w[z]*risk[z][name] for z in range(5))) for name in names}
                    for z,prep in enumerate(settings['preparations']):
                        maxima['risk_identity_error'] = max(maxima['risk_identity_error'],max(abs(risk[z][name]-risk[z]['metadata']-identity[z][name]) for name in names))
                        component_rows.append(dict(model=model,h=h,population=population,preparation=prep,t=t,
                            risks_nats={name:float(value) for name,value in risk[z].items()},
                            population_minus_natural_nats=float(risk[z]['population']-risk[z]['natural'])))
                    maxima['aggregate_order_violation'] = max(maxima['aggregate_order_violation'],aggregate['metadata']-aggregate['population'],aggregate['population']-aggregate['uniform'],aggregate['population']-aggregate['natural'])
                    if population=='balanced':
                        maxima['uniform_identity_error'] = max(maxima['uniform_identity_error'],abs(aggregate['population']-aggregate['uniform']))
                        maxima['balanced_bound_error'] = max(maxima['balanced_bound_error'],abs(bound-.4))
                    maxima['identification_bound_violation'] = max(maxima['identification_bound_violation'],float(accuracy)-bound)
                    if previous_accuracy is not None:
                        maxima['identification_monotonicity_violation'] = max(maxima['identification_monotonicity_violation'],previous_accuracy-float(accuracy))
                    if t==1:
                        first_transition_accuracy=float(accuracy)
                    if h==1 and t>=1:
                        maxima['h1_predictive_error'] = max(maxima['h1_predictive_error'],max(abs(v) for v in aggregate.values()))
                        maxima['h1_identification_plateau_error'] = max(maxima['h1_identification_plateau_error'],abs(float(accuracy)-first_transition_accuracy))
                    aggregate_rows.append(dict(model=model,h=h,population=population,t=t,risks_nats=aggregate,
                        metadata_benefit_nats=aggregate['population']-aggregate['metadata'],
                        uniform_misspecification_nats=aggregate['uniform']-aggregate['population'],
                        natural_misspecification_nats=aggregate['natural']-aggregate['population'],
                        preparation_classification_accuracy=float(accuracy),initial_environment_classification_bound=bound))
                    previous_accuracy=float(accuracy)
                    levels=[rr1.advance(level,kernel,h) for level in levels]
                    collapsed=rr1.advance(collapsed,kernel,h)
                    separate_uniform=rr1.advance(separate_uniform,kernel,h)
    inputs=['evaluation/reset-reader-rr2/PROTOCOL.md','evaluation/reset-reader-rr2/SETTINGS.json',
            'experiments/reset_reader_rr2.py','experiments/reset_reader_study.py',settings['models']]
    maxima={k:float(v) for k,v in maxima.items()}
    harms=[r for r in component_rows if r['population_minus_natural_nats']>tol]
    balanced=[r for r in aggregate_rows if r['population']=='balanced']
    summary=dict(scope='Finite toy with known kernel family; prediction and protocol identification distinguished. No real-agent efficacy claim.',
        aggregate_cells=len(aggregate_rows),component_cells=len(component_rows),tolerance=tol,maxima=maxima,
        algebraic_and_integrity_checks_pass=all(v<=tol for v in maxima.values()),
        component_cells_population_reader_worse_than_natural=len(harms),
        first_component_reversal=harms[0] if harms else None,
        largest_component_reversal=max(harms,key=lambda r:r['population_minus_natural_nats']) if harms else None,
        balanced_max_observed_protocol_identification=max(r['preparation_classification_accuracy'] for r in balanced),
        balanced_protocol_identification_bound=.4,
        largest_metadata_benefit=max(aggregate_rows,key=lambda r:r['metadata_benefit_nats']),
        input_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in inputs},
        environment=dict(python=sys.version,numpy=np.__version__,platform=platform.platform()),
        elapsed_seconds=time.perf_counter()-start)
    (OUT/'RESULTS.json').write_text(json.dumps(dict(summary=summary,aggregate=aggregate_rows,components=component_rows),separators=(',',':'))+'\n')
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return summary['algebraic_and_integrity_checks_pass']


if __name__=='__main__':
    sys.exit(0 if run() else 1)
