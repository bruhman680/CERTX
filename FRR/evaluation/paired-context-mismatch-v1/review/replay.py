#!/usr/bin/env python3
"""Independent saved-array replay. Never imports or invokes experimental code."""
from pathlib import Path
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EPS = 1e-10
D = 12
STATUSES = np.array(['A', 'N', 'U'])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unit_rows(x):
    n = np.linalg.norm(x, axis=1)
    out = np.zeros_like(x)
    np.divide(x, n[:, None], out=out, where=n[:, None] > EPS)
    return out, n > EPS


def population(delta, aligned, q):
    i = np.eye(D)
    z = np.zeros((D, D))
    binding = np.block([[z, z], [z, i]])
    if aligned:
        block = np.block([[delta * delta * i, delta * i], [delta * i, i]])
        moment = block / (2 * D)
        target = block / (1 + delta * delta)
    else:
        moment = np.block([[delta * delta * i, z], [z, i]]) / (2 * D)
        target = binding if delta < 1 else np.eye(2 * D) - binding
    return tuple(q @ mat @ q.T for mat in (moment, target, binding))


def fit_projector(rows):
    # Difference observations are row vectors. Right singular vectors span columns.
    _, sv, vh = np.linalg.svd(rows, full_matrices=False)
    return vh[:D].T @ vh[:D], sv


def products(query, candidates, projector):
    qs, qvalid = unit_rows(np.atleast_2d(query) @ projector.T)
    cs, cvalid = unit_rows(candidates @ projector.T)
    prod = qs.conj() @ cs.T
    valid = qvalid[:, None] & cvalid[None, :] & (np.abs(prod) > EPS)
    return prod, valid


def calibrate(records, projector):
    # Source calibration records: entity/time claims, each A,N,U in that order.
    row, norms_valid = unit_rows(records @ projector.T)
    refs = np.repeat(row[::3], 3, axis=0)
    pv = np.sum(refs.conj() * row, axis=1)
    valid = norms_valid & np.repeat(norms_valid[::3], 3) & (abs(pv) > EPS)
    angles = np.angle(pv)
    centers, counts, resultants = [], [], []
    for j in range(3):
        vv = valid[j::3]
        aa = angles[j::3][vv]
        counts.append(len(aa))
        mean = np.mean(np.exp(1j * aa)) if len(aa) else 0j
        resultants.append(abs(mean))
        centers.append(float(np.angle(mean)) if len(aa) and abs(mean) > EPS else None)
    return centers, counts, resultants


def decode(prod, valid, centers):
    labels = np.full(prod.shape, 'ABSTAIN', dtype='<U7')
    reasons = np.full(prod.shape, '', dtype='<U25')
    if any(c is None for c in centers):
        reasons[:] = 'calibration_unavailable'
        return labels, reasons
    reasons[~valid] = 'zero_product'
    dist = abs(np.angle(np.exp(1j * (np.angle(prod)[..., None] - np.array(centers)))))
    order = np.argsort(dist, axis=-1, kind='stable')
    sorted_dist = np.take_along_axis(dist, order, axis=-1)
    ambiguous = sorted_dist[..., 1] - sorted_dist[..., 0] <= EPS
    reasons[valid & ambiguous] = 'ambiguous_centre'
    good = valid & ~ambiguous
    labels[good] = STATUSES[order[..., 0][good]]
    return labels, reasons


class Checks:
    def __init__(self):
        self.n = 0
        self.failures = []
        self.maxima = {}

    def yes(self, name, ok, details=None):
        self.n += 1
        if not bool(ok):
            self.failures.append({'check': name, 'details': details})

    def close(self, name, actual, expected, tol=1e-10):
        actual, expected = np.asarray(actual), np.asarray(expected)
        err = float(np.max(abs(actual - expected))) if actual.size else 0.
        self.maxima[name.split(':')[0]] = max(self.maxima.get(name.split(':')[0], 0.), err)
        self.yes(name, actual.shape == expected.shape and np.isfinite(err) and err <= tol, {'maximum_error': err, 'tolerance': tol})


def main():
    run = ROOT / 'run'
    src = np.load(run / 'source_inputs.npz', allow_pickle=False)
    train = np.load(run / 'training_inputs.npz', allow_pickle=False)
    saved = np.load(run / 'structures_centres.npz', allow_pickle=False)
    out = np.load(run / 'outcomes.npz', allow_pickle=False)
    ledger = [json.loads(line) for line in (run / 'LEDGER.jsonl').read_text().splitlines()]
    by_key = {(row['outcome_key'], row['query_index']): row for row in ledger}
    c = Checks()
    diagnostics = {(r['seed'], r['arm'], r['m']): r for r in json.loads((run/'STRUCTURAL_DIAGNOSTICS.json').read_text())}
    population_diagnostics = {(r['seed'], r['arm']): r for r in json.loads((run/'POPULATION_DIAGNOSTICS.json').read_text())}
    selection, tie_differences = [], []
    c.yes('source_bytes', digest(run/'source_inputs.npz') == digest(ROOT.parent/'structural-access-three-cycle-v1/run/inputs.npz'))
    for seed, master in zip((92501, 92507, 92509), (94101, 94111, 94121)):
        pre = f's{seed}_'
        q = src[pre+'Q'][1]
        c.close('rotation_orthogonal:'+pre, q.T@q, np.eye(24))
        c.yes('master_seed:'+pre, int(train[pre+'master_seed']) == master)
        rngs = [np.random.default_rng(s) for s in np.random.SeedSequence(master).spawn(3)]
        for name, rng in zip(('context','binding','mismatch'), rngs):
            raw = train[pre+name+'_raw']
            c.close('raw_rng:'+pre+name, raw, rng.normal(size=(1024,12)), 0.)
            c.close('unit_bank:'+pre+name, train[pre+name+'_unit'], raw/np.linalg.norm(raw,axis=1)[:,None])
        context, binding, mismatch = (train[pre+n+'_unit'] for n in ('context','binding','mismatch'))
        for ai, (delta, aligned) in enumerate(((0.,False),(.5,False),(1.5,False),(.5,True),(1.5,True))):
            ap = pre+f'a{ai}'
            arm = ('CLEAN','INDEPENDENT_0.5','INDEPENDENT_1.5','ALIGNED_0.5','ALIGNED_1.5')[ai]
            a = binding if aligned else mismatch
            pair = np.stack((np.concatenate((context+delta*a,binding),axis=1), np.concatenate((context-delta*a,-binding),axis=1)),axis=1)/np.sqrt(2)
            diff = (pair[:,0]-pair[:,1])/2
            rotated = diff @ q.T
            moment, target, pb = population(delta, aligned, q)
            for suffix, value, arr in (('_pairs',pair,train),('_differences',diff,train),('_pairs_rotated',pair@q.T,saved),('_differences_rotated',rotated,saved),('_population_moment',moment,saved),('_population_target',target,saved)):
                c.close('geometry:'+ap+suffix, arr[ap+suffix],value)
            c.close('full:'+pre,saved[pre+'full'],np.eye(24))
            c.close('oracle:'+pre,saved[pre+'oracle'],pb)
            c.close('population_idempotence:'+ap,target@target,target)
            c.close('population_symmetry:'+ap,target.T,target)
            c.close('population_rank:'+ap,np.trace(target),12)
            pd = population_diagnostics[(seed,arm)]
            gap = (1+delta**2 if aligned else abs(1-delta**2))/24
            expected_distance = delta/np.sqrt(1+delta**2) if aligned else float(delta>1)
            for name, value in {'population_gap':gap,'target_rank':12,'target_hermitian_error':np.linalg.norm(target-target.T),'target_idempotent_error':np.linalg.norm(target@target-target),'population_target_distance_to_binding':np.linalg.norm(target-pb)/np.sqrt(24),'analytic_distance_to_binding':expected_distance,'population_eigenvalues':np.linalg.eigvalsh(moment)[::-1]}.items():
                c.close('population_diagnostic:'+ap+name,pd[name],value)
            for name in ('difference_identity_error','common_context_identity_error','rotation_difference_error'):
                c.close('population_identity:'+ap+name,pd[name],0.)
            for m in (12,48,192,768):
                stem = ap+f'_m{m}'
                ph, sv = fit_projector(rotated[:m])
                empirical = rotated[:m].T@rotated[:m]/m
                c.close('projector:'+stem,saved[stem+'_projector'],ph)
                c.close('singular_values:'+stem,saved[stem+'_singular_values'],sv)
                basis = saved[stem+'_basis']
                c.close('basis_projector:'+stem,basis@basis.T,ph)
                c.close('projector_idempotence:'+stem,ph@ph,ph)
                c.close('moment:'+stem,saved[stem+'_empirical_second_moment'],empirical)
                c.close('eigenvalues:'+stem,saved[stem+'_empirical_eigenvalues'],np.linalg.eigvalsh(empirical)[::-1])
                for name, pp in (('population',target),('binding',pb)):
                    w,v=np.linalg.eigh(pp)
                    cos=np.linalg.svd(basis.T@v[:,-12:],compute_uv=False)
                    c.close('principal_cosines:'+stem+name,saved[stem+'_'+name+'_principal_cosines'],cos)
                    c.close('diagnostic_principal_cosines:'+stem+name,diagnostics[(seed,arm,m)][name+'_principal_cosines'],cos)
                for name, rows in (('training',rotated[:m]),('validation',rotated[768:])):
                    residual=rows-rows@ph.T
                    c.close('residual:'+stem+name,saved[stem+'_'+name+'_residuals'],residual)
                dd=diagnostics[(seed,arm,m)]
                eig=np.linalg.eigvalsh(empirical)[::-1]
                trainres=rotated[:m]-rotated[:m]@ph.T
                valres=rotated[768:]-rotated[768:]@ph.T
                cutoff=float(sv[11]-(sv[12] if len(sv)>12 else 0))
                independent_diagnostics={'difference_numeric_rank':int(sum(sv>EPS)),'retained_rank':12,'rank_tolerance':EPS,'singular_values':sv,'rank_cutoff_gap':cutoff,'empirical_eigengap':eig[11]-eig[12],'population_eigengap':gap,'moment_operator_deviation':np.linalg.norm(empirical-moment,ord=2),'distance_to_population_target':np.linalg.norm(ph-target)/np.sqrt(24),'distance_to_intended_binding':np.linalg.norm(ph-pb)/np.sqrt(24),'hermitian_error':np.linalg.norm(ph-ph.T),'idempotent_error':np.linalg.norm(ph@ph-ph),'projector_rank':np.linalg.matrix_rank(ph,tol=EPS),'train_relative_residual':np.sum(abs(trainres)**2)/np.sum(abs(rotated[:m])**2),'validation_relative_residual':np.sum(abs(valres)**2)/np.sum(abs(rotated[768:])**2)}
                for name,value in independent_diagnostics.items():
                    c.close('structural_diagnostic:'+stem+name,dd[name],value)
                c.yes('cutoff_tie:'+stem,bool(dd['rank_cutoff_near_tie'])==(cutoff<=EPS))
                for ri in (0,1):
                    cal = src[pre+f'cal_records_r{ri}']@q.T
                    records = src[pre+f'eval_records_r{ri}']@q.T
                    for method, proj in (('full',np.eye(24)),('oracle',pb),('estimated',ph)):
                        cp=stem+f'_r{ri}_{method}'
                        means, counts, resultants=calibrate(cal,proj)
                        # Reconstruct complex means, including unavailable centers.
                        pp,vv=products(cal[::3],cal,proj)
                        match=np.array([[pp[j,3*j+k] for k in range(3)] for j in range(8)])
                        matchv=np.array([[vv[j,3*j+k] for k in range(3)] for j in range(8)])
                        cm=np.array([np.mean(match[:,j][matchv[:,j]]/abs(match[:,j][matchv[:,j]])) if counts[j] else 0j for j in range(3)])
                        c.close('cal_products:'+cp,saved[cp+'_calibration_products'],match)
                        c.yes('cal_valid:'+cp,np.array_equal(saved[cp+'_calibration_valid'],matchv))
                        c.close('cal_centres:'+cp,saved[cp+'_centres'],cm)
                        c.yes('cal_available:'+cp,np.array_equal(saved[cp+'_available'],np.array([x is not None for x in means])))
                        c.close('cal_query_norms:'+cp,saved[cp+'_calibration_query_norms'],np.linalg.norm(cal[::3]@proj.T,axis=1))
                        c.close('cal_record_norms:'+cp,saved[cp+'_calibration_record_norms'],np.linalg.norm(cal@proj.T,axis=1))
                        for ei in (0,1):
                            op=cp+f'_e{ei}'
                            queries=src[pre+f'queries_r{ri}_e{ei}']@q.T
                            pr,valid=products(queries[[0,31]],records,proj)
                            uq,_=unit_rows(queries[[0,31]]@proj.T)
                            ur,_=unit_rows(records@proj.T)
                            real_channel=uq.real@ur.real.T+uq.imag@ur.imag.T
                            imag_channel=uq.real@ur.imag.T-uq.imag@ur.real.T
                            c.close('real_imag_product:'+op,pr,real_channel+1j*imag_channel)
                            labels,reasons=decode(pr,valid,means)
                            reasons[reasons=='']='ok'
                            for j,n in enumerate((0,31)):
                                selection.append({'outcome_key':op,'query_index':n})
                                c.close('products:'+op+str(n),out[op+'_products'][n],pr[j])
                                c.yes('valid:'+op+str(n),np.array_equal(out[op+'_valid'][n],valid[j]))
                                c.yes('labels:'+op+str(n),np.array_equal(out[op+'_labels'][n],labels[j]))
                                c.yes('reasons:'+op+str(n),np.array_equal(out[op+'_reasons'][n],reasons[j]))
                                c.close('query_norm:'+op+str(n),out[op+'_query_norms'][n],np.linalg.norm(queries[n]@proj.T))
                                c.close('record_norms:'+op+str(n),out[op+'_record_norms'],np.linalg.norm(records@proj.T,axis=1))
                                top=np.argsort(-abs(pr[j]),kind='stable')[:3]
                                stored=out[op+'_top'][n]
                                row=by_key[(op,n)]
                                c.yes('ledger_top:'+op+str(n),np.array_equal(row['returned_indices'],stored))
                                c.yes('saved_exact_sort:'+op+str(n),np.array_equal(stored,np.argsort(-abs(out[op+'_products'][n]),kind='stable')[:3]))
                                c.close('ledger_scores:'+op+str(n),row['scores'],abs(out[op+'_products'][n,stored]))
                                c.close('ledger_angles:'+op+str(n),row['angles'],np.angle(out[op+'_products'][n,stored]))
                                c.yes('ledger_predictions:'+op+str(n),np.array_equal(row['predictions'],out[op+'_labels'][n,stored]))
                                c.yes('ledger_reasons:'+op+str(n),np.array_equal(row['reasons'],out[op+'_reasons'][n,stored]))
                                if not np.array_equal(top,stored):
                                    differing=set(top)^set(stored)
                                    involved=list(differing) if differing else list(top)
                                    spread=float(np.ptp(abs(pr[j,involved])))
                                    tie_differences.append({'outcome_key':op,'query_index':n,'independent_top':top.tolist(),'saved_top':stored.tolist(),'score_spread':spread,'same_set':set(top)==set(stored)})
                                    c.yes('top_numerical_tie:'+op+str(n),spread<1e-12,{'spread':spread})
                                else:
                                    c.yes('top_exact:'+op+str(n),True)
    c.yes('sample_count',len(selection)==1440)
    result={'checks':c.n,'failures':c.failures,'maxima':c.maxima,'selection':selection,'tie_differences':tie_differences,'hashes':{p.name:digest(p) for p in (run/'source_inputs.npz',run/'training_inputs.npz',run/'structures_centres.npz',run/'outcomes.npz',run/'LEDGER.jsonl')},'source_inspection':'Read protocol, analytic review, saved-array SCHEMA.md and source NPZ schema only; no current or predecessor experiment implementation imported or read.'}
    (ROOT/'review/REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':c.n,'failures':len(c.failures),'maxima':c.maxima,'ties':len(tie_differences)},indent=2))


if __name__=='__main__':
    main()
