#!/usr/bin/env python3
"""PC-C1/2/3: fixed paired-context mismatch contact; NumPy + stdlib only.
No predecessor implementation is imported. Main is deliberately guarded.
"""
import os
for _thread in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_thread] = '1'
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
import numpy as np

SEEDS = (92501, 92507, 92509)
TRAIN_SEEDS = (94101, 94111, 94121)
ARMS = (('CLEAN', 0., 'clean'), ('INDEPENDENT_0.5', .5, 'independent'),
        ('INDEPENDENT_1.5', 1.5, 'independent'), ('ALIGNED_0.5', .5, 'aligned'),
        ('ALIGNED_1.5', 1.5, 'aligned'))
MS = (12, 48, 192, 768)
RS = (.5, 2.)
ETAS = (0., 1.5)
METHODS = ('full', 'oracle', 'estimated')
STATUS = np.array(('A', 'N', 'U'))
D, N, TOL = 12, 24, 1e-10
PB = np.diag([0.]*D+[1.]*D)
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'structural-access-three-cycle-v1'


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)+'\n')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()


def ahash(x):
    x = np.ascontiguousarray(x)
    h = hashlib.sha256()
    h.update(str(x.dtype).encode()); h.update(str(x.shape).encode()); h.update(x.tobytes())
    return h.hexdigest()


def metadata(a):
    return {k: {'shape': list(x.shape), 'dtype': str(x.dtype), 'sha256': ahash(x)} for k,x in a.items()}


def err(a): return float(np.max(np.abs(a)))
def distance(a,b): return float(np.linalg.norm(a-b)/np.sqrt(2*D))
def relative_residual(x,p): return float(np.sum(np.abs(x-x@p.T)**2)/np.sum(np.abs(x)**2))


def population(delta, kind):
    i = np.eye(D); z = np.zeros((D,D))
    if kind == 'aligned':
        block = np.block([[delta*delta*i,delta*i],[delta*i,i]])
        return block/(2*D), block/(1+delta*delta), (1+delta*delta)/(2*D)
    moment = np.block([[delta*delta*i,z],[z,i]])/(2*D)
    return moment, PB.copy() if delta<1 else np.eye(N)-PB, abs(1-delta*delta)/(2*D)


def training_inputs():
    arrays = {}
    for seed, master in zip(SEEDS,TRAIN_SEEDS):
        streams = np.random.SeedSequence(master).spawn(3)
        prefix = f's{seed}_'
        arrays[prefix+'master_seed'] = np.array(master)
        arrays[prefix+'stream_spawn_keys'] = np.array([s.spawn_key for s in streams])
        for name,stream in zip(('context','binding','mismatch'),streams):
            raw = np.random.default_rng(stream).normal(size=(1024,D))
            arrays[prefix+name+'_raw'] = raw
            arrays[prefix+name+'_unit'] = raw/np.linalg.norm(raw,axis=1,keepdims=True)
        c,b,a = (arrays[prefix+x+'_unit'] for x in ('context','binding','mismatch'))
        for ai,(_,delta,kind) in enumerate(ARMS):
            mismatch = b if kind=='aligned' else a
            pairs = np.stack((np.concatenate((c+delta*mismatch,b),axis=1),
                              np.concatenate((c-delta*mismatch,-b),axis=1)),axis=1)/np.sqrt(2)
            arrays[prefix+f'a{ai}_pairs'] = pairs
            arrays[prefix+f'a{ai}_differences'] = (pairs[:,0]-pairs[:,1])/2
    return arrays


def project(x,p):
    y = x@p.T
    norms = np.linalg.norm(y,axis=1)
    ok = norms>TOL
    normalized = np.zeros(y.shape,dtype=complex)
    normalized[ok] = y[ok]/norms[ok,None]
    return normalized,norms,ok


def products(q,w,p):
    qn,qnrm,qok = project(q,p); wn,wnrm,wok = project(w,p)
    h = qn.conj()@wn.T
    ok = qok[:,None]&wok[None,:]&(np.abs(h)>TOL)
    # Independent real-channel expansion of the actual projected normalized inputs.
    real = qn.real@wn.real.T+qn.imag@wn.imag.T
    imag = qn.real@wn.imag.T-qn.imag@wn.real.T
    return h,ok,qnrm,wnrm,err(h-(real+1j*imag))


def fit_centres(cal,p):
    h,ok,qnrm,wnrm,realerr = products(cal[::3],cal,p)
    centre = np.zeros(3,dtype=complex); available = np.zeros(3,dtype=bool)
    selected = np.empty((len(cal)//3,3),dtype=complex)
    valid = np.empty(selected.shape,dtype=bool)
    for k in range(3):
        v = h[np.arange(len(cal)//3),3*np.arange(len(cal)//3)+k]
        good = ok[np.arange(len(cal)//3),3*np.arange(len(cal)//3)+k]
        selected[:,k] = v; valid[:,k] = good
        if np.any(good):
            centre[k] = np.mean(v[good]/np.abs(v[good]))
            available[k] = abs(centre[k])>TOL
    return centre,available,selected,valid,qnrm,wnrm,realerr


def decode(h,valid,centres,available):
    labels = np.full(h.shape,'ABSTAIN',dtype='<U7')
    reasons = np.full(h.shape,'zero_product',dtype='<U24')
    if not np.all(available):
        reasons[:] = 'calibration_unavailable'
        return labels,reasons
    dist = np.abs(np.angle(np.exp(1j*(np.angle(h)[...,None]-np.angle(centres)))))
    order = np.argsort(dist,axis=-1,kind='stable')
    sorted_dist = np.take_along_axis(dist,order,axis=-1)
    ambiguous = sorted_dist[...,1]-sorted_dist[...,0]<=TOL
    good = valid&~ambiguous
    labels[good] = STATUS[order[...,0][good]]
    reasons[good] = 'ok'; reasons[valid&ambiguous] = 'ambiguous_centre'
    return labels,reasons


def query_metrics(indices,labels,reasons,claim):
    relevant = indices//3==claim
    correct = labels[indices]==STATUS[indices%3]
    pred = labels[indices]; why = reasons[indices]
    gold = np.arange(3*claim,3*claim+3)
    return {'evidence_count':int(np.sum(relevant)), 'evidence_recall':float(np.sum(relevant)/3),
            'evidence_complete':int(np.all(relevant)), 'joint_label_count':int(np.sum(relevant&correct)),
            'joint_label_recall':float(np.sum(relevant&correct)/3), 'joint_complete':int(np.all(relevant&correct)),
            'wrong_scope_count':int(np.sum(~relevant)),
            'encoded_U_recall':int(np.any((indices==3*claim+2)&(pred=='U'))),
            'abstain_count':int(np.sum(pred=='ABSTAIN')),
            **{'abstain_'+r:int(np.sum(why==r)) for r in ('calibration_unavailable','ambiguous_centre','zero_product')},
            'oracle_relevant_stance_accuracy':float(np.mean(labels[gold]==STATUS))}


def write_jsonl(path, rows):
    with Path(path).open('w') as f:
        for row in rows: f.write(json.dumps(row,allow_nan=False)+'\n')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output',default=str(HERE/'run'))
    args = parser.parse_args(); out = Path(args.output); out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()): raise SystemExit('Refusing to overwrite a nonempty output directory')
    started = time.time()
    dump(out/'ATTEMPT.json',{'status':'started','started_unix':started,'numpy':np.__version__,
         'threads':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')}})
    for name in ('experiment.py','PROTOCOL.md','IMPLEMENTATION.md','SCHEMA.md'):
        shutil.copy2(HERE/name,out/name)
    source_manifest = json.loads((SOURCE/'ARCHIVE_MANIFEST.json').read_text())
    source_path = SOURCE/'run/inputs.npz'
    expected = source_manifest['files']['run/inputs.npz']['sha256']
    assert sha(source_path)==expected
    assert sha(SOURCE/source_manifest['archive'])==source_manifest['sha256']
    assert sha(SOURCE/'run/LEDGER.jsonl')==source_manifest['files']['run/LEDGER.jsonl']['sha256']
    assert sha(SOURCE/'run/INPUT_MANIFEST.json')==source_manifest['files']['run/INPUT_MANIFEST.json']['sha256']
    shutil.copy2(source_path,out/'source_inputs.npz')
    shutil.copy2(SOURCE/'ARCHIVE_MANIFEST.json',out/'SOURCE_ARCHIVE_MANIFEST.json')
    shutil.copy2(SOURCE/'run/INPUT_MANIFEST.json',out/'SOURCE_INPUT_MANIFEST.json')
    assert sha(out/'source_inputs.npz')==expected
    with np.load(out/'source_inputs.npz',allow_pickle=False) as z: source = {k:z[k] for k in z.files}
    original_meta = json.loads((SOURCE/'run/INPUT_MANIFEST.json').read_text())['arrays']
    assert all(ahash(x)==original_meta[k]['sha256'] for k,x in source.items())
    used = {}
    for seed in SEEDS:
        pre = f's{seed}_'
        used[pre+'denseQ'] = source[pre+'Q'][1]
        for name in ('query_claim_index','query_repetition','eval_context','eval_binding','cal_context','cal_binding',
                     'query_noise_raw','query_noise_unit','stream_spawn_keys'):
            used[pre+name] = source[pre+name]
        for ri in range(2):
            for pool in ('eval','cal'): used[pre+f'{pool}_records_r{ri}'] = source[pre+f'{pool}_records_r{ri}']
            for ei in range(2): used[pre+f'queries_r{ri}_e{ei}'] = source[pre+f'queries_r{ri}_e{ei}']
    train = training_inputs()
    np.savez_compressed(out/'training_inputs.npz',**train)
    # Durable raw input checkpoint: no SVD, calibration fit, or outcome scoring above.
    dump(out/'INPUT_MANIFEST.json',{'source_file_sha256':expected,'source_archive_sha256':sha(SOURCE/source_manifest['archive']),
        'source_arrays':metadata(source),'used_arrays':metadata(used),'training_arrays':metadata(train),
        'training_file_sha256':sha(out/'training_inputs.npz'),'training_stream_order':['context','binding','mismatch'],
        'fitting_indices':[0,768],'validation_indices':[768,1024],
        'provenance':'source eval/cal/query arrays reused unchanged; new independent train streams; no source training arrays used',
        'time_unix':time.time()})
    derived = {}; fits = {}; structural = []; algebra = []; populations = []
    query_manifest = []
    for seed in SEEDS:
        pre = f's{seed}_'; q = used[pre+'denseQ']; oracle = q@PB@q.T
        derived[pre+'oracle'] = oracle; derived[pre+'full'] = np.eye(N)
        algebra.append({'seed':seed,'orthogonality_error':err(q.T@q-np.eye(N)),
                        'oracle_idempotent_error':err(oracle@oracle-oracle),'oracle_hermitian_error':err(oracle-oracle.T)})
        for ai,(arm,delta,kind) in enumerate(ARMS):
            stem = pre+f'a{ai}'; pairs = train[stem+'_pairs']; base = train[stem+'_differences']
            c,b,a = (train[pre+x+'_unit'] for x in ('context','binding','mismatch'))
            mismatch = b if kind=='aligned' else a
            intended_diff = np.concatenate((delta*mismatch,b),axis=1)/np.sqrt(2)
            moment,target,gap = population(delta,kind)
            sigma = q@moment@q.T; targetq = q@target@q.T
            pairsq = pairs@q.T; diff = (pairsq[:,0]-pairsq[:,1])/2
            derived[stem+'_pairs_rotated'] = pairsq; derived[stem+'_differences_rotated'] = diff
            derived[stem+'_population_moment'] = sigma; derived[stem+'_population_target'] = targetq
            pdiag = {'seed':seed,'arm':arm,'delta':delta,'kind':kind,'population_gap':gap,
                'target_rank':int(np.linalg.matrix_rank(targetq,tol=TOL)),
                'target_hermitian_error':err(targetq-targetq.T),'target_idempotent_error':err(targetq@targetq-targetq),
                'population_target_distance_to_binding':distance(targetq,oracle),
                'analytic_distance_to_binding':delta/np.sqrt(1+delta*delta) if kind=='aligned' else float(delta>1),
                'difference_identity_error':err(base-intended_diff),
                'common_context_identity_error':err((pairs[:,0]+pairs[:,1])/2-np.concatenate((c,np.zeros_like(b)),axis=1)/np.sqrt(2)),
                'rotation_difference_error':err(diff-base@q.T),
                'population_eigenvalues':np.linalg.eigvalsh(sigma)[::-1].tolist()}
            assert pdiag['target_rank']==D
            for check in ('target_hermitian_error','target_idempotent_error','difference_identity_error',
                          'common_context_identity_error','rotation_difference_error'):
                assert pdiag[check]<=TOL, (seed,arm,check,pdiag[check])
            assert abs(pdiag['population_target_distance_to_binding']-pdiag['analytic_distance_to_binding'])<=TOL
            assert abs((pdiag['population_eigenvalues'][D-1]-pdiag['population_eigenvalues'][D])-gap)<=TOL
            populations.append(pdiag)
            for m in MS:
                key = stem+f'_m{m}'
                u,s,_ = np.linalg.svd(diff[:m].T,full_matrices=False)
                basis = u[:,:D]; p = basis@basis.T; fits[seed,ai,m] = p
                padded = np.pad(s,(0,N-len(s)))
                empirical = diff[:m].T@diff[:m]/m
                eigenvalues = np.linalg.eigvalsh(empirical)[::-1]
                target_basis = np.linalg.eigh(targetq)[1][:,-D:]
                binding_basis = q[:,D:]
                values = {'projector':p,'basis':basis,'singular_values':s,'empirical_second_moment':empirical,
                          'empirical_eigenvalues':eigenvalues,
                          'population_principal_cosines':np.linalg.svd(target_basis.T@basis,compute_uv=False),
                          'binding_principal_cosines':np.linalg.svd(binding_basis.T@basis,compute_uv=False),
                          'training_residuals':diff[:m]-diff[:m]@p.T,
                          'validation_residuals':diff[768:]-diff[768:]@p.T}
                for name,x in values.items(): derived[key+'_'+name] = x
                structural.append({'seed':seed,'arm':arm,'delta':delta,'kind':kind,'m':m,
                    'difference_numeric_rank':int(np.sum(s>TOL)),'retained_rank':D,'rank_tolerance':TOL,
                    'singular_values':s.tolist(),'rank_cutoff_gap':float(padded[D-1]-padded[D]),
                    'rank_cutoff_near_tie':bool(abs(padded[D-1]-padded[D])<=TOL),
                    'empirical_eigengap':float(eigenvalues[D-1]-eigenvalues[D]),'population_eigengap':gap,
                    'moment_operator_deviation':float(np.linalg.norm(empirical-sigma,ord=2)),
                    'distance_to_population_target':distance(p,targetq),'distance_to_intended_binding':distance(p,oracle),
                    'population_principal_cosines':values['population_principal_cosines'].tolist(),
                    'binding_principal_cosines':values['binding_principal_cosines'].tolist(),
                    'hermitian_error':err(p-p.T),'idempotent_error':err(p@p-p),
                    'projector_rank':int(np.linalg.matrix_rank(p,tol=TOL)),
                    'train_relative_residual':relative_residual(diff[:m],p),
                    'validation_relative_residual':relative_residual(diff[768:],p)})
                assert err(p-p.T)<=TOL and err(p@p-p)<=TOL
                assert np.sum(s>TOL)>=D
                if kind in ('clean','aligned'):
                    assert distance(p,targetq)<=TOL
                    assert relative_residual(diff[768:],p)<=TOL
                for ri in range(2):
                    cal = used[pre+f'cal_records_r{ri}']@q.T
                    for method in METHODS:
                        proj = {'full':np.eye(N),'oracle':oracle,'estimated':p}[method]
                        ck = key+f'_r{ri}_{method}'
                        centre,available,vals,valid,qnrm,wnrm,re = fit_centres(cal,proj)
                        for name,x in (('centres',centre),('available',available),('calibration_products',vals),
                                       ('calibration_valid',valid),('calibration_query_norms',qnrm),('calibration_record_norms',wnrm)):
                            derived[ck+'_'+name] = x
                        algebra.append({'seed':seed,'arm':arm,'m':m,'r':RS[ri],'method':method,'calibration_real_channel_error':re})
        for ri in range(2):
            for ei in range(2):
                query = used[pre+f'queries_r{ri}_e{ei}']
                for j,x in enumerate(query):
                    query_manifest.append({'query_id':f'{seed}-r{ri}-e{ei}-q{j:02d}','seed':seed,'r':RS[ri],
                        'eval_eta':ETAS[ei],'claim':int(used[pre+'query_claim_index'][j]),
                        'repetition':int(used[pre+'query_repetition'][j]),'array_sha256':ahash(x)})
    np.savez_compressed(out/'structures_centres.npz',**derived)
    dump(out/'STRUCTURAL_DIAGNOSTICS.json',structural); dump(out/'POPULATION_DIAGNOSTICS.json',populations)
    dump(out/'ALGEBRA_DIAGNOSTICS.json',algebra); dump(out/'QUERY_MANIFEST.json',query_manifest)
    dump(out/'PRE_SCORING_CHECKPOINT.json',{'time_unix':time.time(),
        'inputs_manifest_sha256':sha(out/'INPUT_MANIFEST.json'),
        'structures_centres_sha256':sha(out/'structures_centres.npz'),
        'population_diagnostics_sha256':sha(out/'POPULATION_DIAGNOSTICS.json'),
        'structural_diagnostics_sha256':sha(out/'STRUCTURAL_DIAGNOSTICS.json'),
        'query_manifest_sha256':sha(out/'QUERY_MANIFEST.json')})
    outcomes = {}; ledger = []; paired = []; aggregates = []; repeats = []; controls = {}; product_checks = []
    for seed in SEEDS:
        pre = f's{seed}_'; q = used[pre+'denseQ']; oracle = derived[pre+'oracle']
        for ai,(arm,delta,kind) in enumerate(ARMS):
            for m in MS:
                for ri,r in enumerate(RS):
                    w = used[pre+f'eval_records_r{ri}']@q.T
                    for ei,eta in enumerate(ETAS):
                        query = used[pre+f'queries_r{ri}_e{ei}']@q.T
                        indices_by_method = {}
                        for method in METHODS:
                            key = pre+f'a{ai}_m{m}_r{ri}_{method}'; okkey = key+f'_e{ei}'
                            p = {'full':np.eye(N),'oracle':oracle,'estimated':fits[seed,ai,m]}[method]
                            h,valid,qnrm,wnrm,re = products(query,w,p)
                            labels,reasons = decode(h,valid,derived[key+'_centres'],derived[key+'_available'])
                            scores = np.abs(h); top = np.argsort(-scores,axis=1,kind='stable')[:,:3]
                            sorted_scores = np.take_along_axis(scores,np.argsort(-scores,axis=1,kind='stable'),axis=1)
                            gaps = sorted_scores[:,2]-sorted_scores[:,3]
                            for name,x in (('products',h),('valid',valid),('labels',labels),('reasons',reasons),('top',top),
                                           ('query_norms',qnrm),('record_norms',wnrm)):
                                outcomes[okkey+'_'+name] = x
                            product_checks.append({'seed':seed,'arm':arm,'m':m,'r':r,'eval_eta':eta,'method':method,'real_channel_error':re})
                            condition = {'seed':seed,'Q':'dense','arm':arm,'delta':delta,'kind':kind,'m':m,'r':r,'eval_eta':eta}
                            rows = []; row_ids = []
                            for j,idx in enumerate(top):
                                claim = int(used[pre+'query_claim_index'][j]); rep = int(used[pre+'query_repetition'][j])
                                gold = np.arange(3*claim,3*claim+3); metrics = query_metrics(idx,labels[j],reasons[j],claim)
                                row_ids.append(len(ledger))
                                row = dict(condition,method=method,query_id=f'{seed}-r{ri}-e{ei}-q{j:02d}',query_index=j,
                                    claim=claim,repetition=rep,outcome_key=okkey,returned_indices=idx.tolist(),
                                    returned_record_ids=[f'eval-e{x//6}-t{(x//3)%2}-{STATUS[x%3]}' for x in idx],
                                    scores=scores[j,idx].tolist(),angles=np.angle(h[j,idx]).tolist(),
                                    predictions=labels[j,idx].tolist(),reasons=reasons[j,idx].tolist(),
                                    boundary_gap=float(gaps[j]),near_boundary_tie=bool(gaps[j]<=TOL),
                                    within_top3_score_differences=np.diff(sorted_scores[j,:3]).tolist(),
                                    oracle_relevant_predictions=labels[j,gold].tolist(),oracle_relevant_reasons=reasons[j,gold].tolist(),metrics=metrics)
                                ledger.append(row); rows.append(row)
                            indices_by_method[method] = row_ids
                            sums = {k:float(sum(row['metrics'][k] for row in rows)) for k in rows[0]['metrics']}
                            aggregates.append({'condition':dict(condition,method=method),'count':32,'metric_sums':sums,
                                               'metric_means':{k:v/32 for k,v in sums.items()}})
                            if method in ('full','oracle'):
                                control_key = (seed,ri,ei,method)
                                if control_key not in controls: controls[control_key] = (h.copy(),labels.copy(),reasons.copy(),top.copy(),rows)
                                else:
                                    bh,bl,br,bt,brows = controls[control_key]
                                    repeats.append(dict(condition,method=method,max_product_error=err(h-bh),
                                        labels_equal=bool(np.array_equal(labels,bl)),reasons_equal=bool(np.array_equal(reasons,br)),
                                        top_equal=bool(np.array_equal(top,bt)),metrics_equal=all(x['metrics']==y['metrics'] for x,y in zip(rows,brows))))
                        for j in range(32): paired.append(dict(condition,query_id=f'{seed}-r{ri}-e{ei}-q{j:02d}',
                            method_record_indices={method:indices_by_method[method][j] for method in METHODS}))
    assert len(paired)==7680 and len(ledger)==23040 and len(aggregates)==720
    assert all(x['real_channel_error']<=TOL for x in product_checks)
    assert all(x.get('calibration_real_channel_error',0.)<=TOL for x in algebra)
    np.savez_compressed(out/'outcomes.npz',**outcomes)
    write_jsonl(out/'LEDGER.jsonl',ledger); write_jsonl(out/'PAIRED_ROWS.jsonl',paired)
    dump(out/'AGGREGATES.json',aggregates); dump(out/'REPEATED_CONTROL_CHECKS.json',repeats)
    dump(out/'PRODUCT_CHECKS.json',product_checks)
    # Compare every eligible predecessor dense FULL/ORACLE record, not selected seeds.
    prior_comparisons = []
    with (SOURCE/'run/LEDGER.jsonl').open() as f:
        for line in f:
            old = json.loads(line)
            if old['Q']!='dense' or old['method'] not in ('full','oracle'): continue
            ri = RS.index(old['r']); ei = ETAS.index(old['eval_eta']); j = old['query_index']
            h,labels,reasons,top,rows = controls[old['seed'],ri,ei,old['method']]
            new = rows[j]; old_metrics = old['metrics']; new_metrics = new['metrics']
            metric_differences = {k:new_metrics[k]-v for k,v in old_metrics.items() if new_metrics[k]!=v}
            prior_comparisons.append({'source_condition':{k:old[k] for k in ('seed','r','eval_eta','train_eta','m','method')},
                'query_id':old['query_id'],'top_order_equal':old['returned_indices']==new['returned_indices'],
                'top_set_equal':set(old['returned_indices'])==set(new['returned_indices']),
                'returned_predictions_equal':old['predictions']==new['predictions'],
                'returned_reasons_equal':old['reasons']==new['reasons'],
                'oracle_relevant_predictions_equal':old['oracle_relevant_predictions']==new['oracle_relevant_predictions'],
                'max_returned_score_error':float(np.max(np.abs(np.asarray(old['scores'])-np.asarray(new['scores'])))),
                'source_boundary_gap':old['boundary_gap'],'new_boundary_gap':new['boundary_gap'],
                'metric_differences':metric_differences})
    dump(out/'PREDECESSOR_CONTROL_CHECKS.json',prior_comparisons)
    summary = {'paired_rows':len(paired),'method_records':len(ledger),'aggregates':len(aggregates),
        'base_query_ids':len(query_manifest),'base_unique_query_arrays':len({x['array_sha256'] for x in query_manifest}),
        'underlying_eval_entity_time_claims':48,'source_inputs_byte_identical':sha(out/'source_inputs.npz')==expected,
        'controls_repeated_across_training_settings':20,'all_repeated_controls_match':all(
            x['max_product_error']==0 and x['labels_equal'] and x['reasons_equal'] and x['top_equal'] and x['metrics_equal'] for x in repeats),
        'predecessor_control_records_compared':len(prior_comparisons),
        'predecessor_metric_difference_records':sum(bool(x['metric_differences']) for x in prior_comparisons),
        'predecessor_top_set_difference_records':sum(not x['top_set_equal'] for x in prior_comparisons),
        'max_task_real_channel_error':max(x['real_channel_error'] for x in product_checks),
        'max_projector_idempotent_error':max(x['idempotent_error'] for x in structural),
        'max_projector_hermitian_error':max(x['hermitian_error'] for x in structural),
        'elapsed_seconds':time.time()-started,'diagnostic_tolerance':TOL}
    assert summary['base_query_ids']==384 and summary['base_unique_query_arrays']==288
    dump(out/'SUMMARY.json',summary)
    dump(out/'ATTEMPT.json',{'status':'complete','started_unix':started,'finished_unix':time.time(),'numpy':np.__version__,
         'elapsed_seconds':time.time()-started})
    dump(out/'OUTPUT_HASHES.json',{p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='OUTPUT_HASHES.json'})
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
