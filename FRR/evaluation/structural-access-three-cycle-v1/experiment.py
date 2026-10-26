#!/usr/bin/env python3
"""Frozen SA-C1/2/3 numerical contact. NumPy and Python standard library only."""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_name] = '1'
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
import numpy as np

SEEDS = (92501,92507,92509)
D = 12
N = 24
RS = (.5,2.)
ETAS = (0.,1.5)
TRAIN_ETAS = (0.,.25)
MS = (4,12,48)
QNAMES = ('identity','dense','plane')
METHODS = ('full','naive','oracle','estimated')
STATUS = ('A','N','U')
PHASE = np.array([1.,-1.,np.exp(1j*np.pi/3)])
TOL = 1e-10
P = np.diag([0.]*D+[1.]*D).astype(complex)


def digest_array(x):
    x = np.ascontiguousarray(x)
    h = hashlib.sha256()
    h.update(str(x.dtype).encode()); h.update(str(x.shape).encode()); h.update(x.tobytes())
    return h.hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+'\n')


def unit(x):
    return x / np.linalg.norm(x,axis=-1,keepdims=True)


def complex_noise(rng,shape):
    raw = rng.normal(size=shape)+1j*rng.normal(size=shape)
    return raw,unit(raw)


def records(c,b,r):
    # Entity-time is the major axis; status A,N,U is the minor axis.
    return np.concatenate((np.repeat(r*c,3,axis=0),
                           (b[:,None,:]*PHASE[None,:,None]).reshape(-1,D)),axis=1)/np.sqrt(r*r+1)


def generate():
    arrays = {}
    for seed in SEEDS:
        streams = np.random.SeedSequence(seed).spawn(5)
        latent,rotation,train,calnoise,evalnoise = [np.random.default_rng(s) for s in streams]
        # Calibration noise has a reserved, disjoint stream; eta_cal is exactly zero.
        prefix = f's{seed}_'
        def save(k,v): arrays[prefix+k] = np.asarray(v); return v
        save('stream_spawn_keys',np.array([s.spawn_key for s in streams]))
        pred_raw = save('predicate_raw',latent.normal(size=D))
        pred = save('predicate',unit(pred_raw))
        for pool,count in (('eval',8),('cal',4)):
            e = save(pool+'_entity_raw',latent.normal(size=(count,D)))
            t = save(pool+'_time_raw',latent.normal(size=(2,D)))
            eu = save(pool+'_entity_unit',unit(e)); tu = save(pool+'_time_unit',unit(t))
            c = save(pool+'_context',unit((eu[:,None,:]+tu[None,:,:]+pred).reshape(-1,D)))
            b = save(pool+'_binding_raw',latent.normal(size=(count*2,D)))
            b = save(pool+'_binding',unit(b))
            for ri,r in enumerate(RS): save(f'{pool}_records_r{ri}',records(c,b,r))
        a = save('rotation_raw',rotation.normal(size=(N,N)))
        q,rr = np.linalg.qr(a)
        signs = np.where(np.diag(rr)<0,-1.,1.)
        q = q*signs[None,:]
        plane = np.eye(N); theta = np.pi/4
        plane[np.ix_([0,D],[0,D])] = [[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]]
        save('Q',np.stack([np.eye(N),q,plane]))
        tc = save('train_context_raw',latent.normal(size=(48,D)))
        tb = save('train_binding_raw',latent.normal(size=(48,D)))
        tc = save('train_context',unit(tc)); tb = save('train_binding',unit(tb))
        clean = save('train_clean_pairs',np.stack([np.concatenate([tc,tb],axis=1),np.concatenate([tc,-tb],axis=1)],axis=1)/np.sqrt(2))
        raw,noise = complex_noise(train,(48,2,N))
        save('train_noise_raw',raw); save('train_noise_unit',noise)
        for ti,eta in enumerate(TRAIN_ETAS): save(f'train_pairs_t{ti}',clean+eta*noise)
        # One saved query noise bank is reused for both r and eta conditions.
        raw,noise = complex_noise(evalnoise,(32,N))
        save('query_noise_raw',raw); save('query_noise_unit',noise)
        save('query_claim_index',np.repeat(np.arange(16),2))
        save('query_repetition',np.tile(np.arange(2),16))
        for ri in range(2):
            ref = np.repeat(arrays[prefix+f'eval_records_r{ri}'][::3],2,axis=0)
            for ei,eta in enumerate(ETAS): save(f'queries_r{ri}_e{ei}',unit(ref+eta*noise))
    return arrays


def projected(x,proj):
    y = x @ proj.T  # Column P x represented as rows, also for complex Hermitian P.
    norms = np.linalg.norm(y,axis=1)
    valid = norms>TOL
    z = np.zeros_like(y,dtype=complex)
    z[valid] = y[valid]/norms[valid,None]
    return z,norms,valid


def products(q,w,proj):
    qn,qnorm,qok = projected(q,proj); wn,wnorm,wok = projected(w,proj)
    h = qn.conj() @ wn.T
    valid = qok[:,None]&wok[None,:]&(np.abs(h)>TOL)
    return h,valid


def centres(q,w,proj):
    h,valid = products(q,w,proj)
    result = np.zeros(3,dtype=complex); available = np.zeros(3,dtype=bool)
    for k in range(3):
        vals = h[np.arange(len(q)),3*np.arange(len(q))+k]
        ok = valid[np.arange(len(q)),3*np.arange(len(q))+k]
        if np.any(ok):
            mean = np.mean(vals[ok]/np.abs(vals[ok]))
            result[k] = mean
            available[k] = abs(mean)>TOL
    return result,available


def decode(h,valid,centre,available):
    labels = np.full(h.shape,'ABSTAIN',dtype='<U7')
    reasons = np.full(h.shape,'zero_product',dtype='<U24')
    if not np.all(available):
        reasons[:] = 'calibration_unavailable'
        return labels,reasons
    distances = np.abs(np.angle(np.exp(1j*(np.angle(h)[...,None]-np.angle(centre)))))
    order = np.argsort(distances,axis=-1,kind='stable')
    tie = np.take_along_axis(distances,order,axis=-1)
    ambiguous = (tie[...,1]-tie[...,0])<=TOL
    good = valid&~ambiguous
    labels[good] = np.array(STATUS)[order[...,0][good]]
    reasons[good] = 'ok'; reasons[valid&ambiguous] = 'ambiguous_centre'
    return labels,reasons


def err(x): return float(np.max(np.abs(x))) if np.size(x) else 0.


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output',default='run')
    args = parser.parse_args(); out = Path(args.output); out.mkdir(parents=True,exist_ok=True)
    if (out/'ATTEMPT.json').exists(): raise SystemExit('Refusing to overwrite an existing attempt')
    started = time.time()
    dump(out/'ATTEMPT.json',{'started_unix':started,'status':'started','numpy':np.__version__,'threads':{k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')}})
    shutil.copy2(__file__,out/'experiment.py'); shutil.copy2(Path(__file__).with_name('PROTOCOL.md'),out/'PROTOCOL.md')
    a = generate()
    np.savez_compressed(out/'inputs.npz',**a)
    # The first durable checkpoint precedes fitting, decoding, retrieval and gold scoring.
    dump(out/'INPUT_MANIFEST.json',{'file_sha256':file_hash(out/'inputs.npz'),'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype),'sha256':digest_array(v)} for k,v in a.items()},'streams':['latent','rotation','training_noise','calibration_noise_reserved_zero','evaluation_noise']})
    derived = {}; fits = {}; structural = []; algebra = []; query_manifest = []
    for seed in SEEDS:
        pre = f's{seed}_'; qs = a[pre+'Q']; fitted_identity = {}
        for ti in range(2):
            pairs = a[pre+f'train_pairs_t{ti}']; diff = (pairs[:,0]-pairs[:,1])/2
            for m in MS:
                u,s,_ = np.linalg.svd(diff[:m].T,full_matrices=False)
                fitted_identity[ti,m] = u[:,:min(m,D)] @ u[:,:min(m,D)].conj().T
        for qi,q in enumerate(qs):
            oracle = q @ P @ q.T
            for ti in range(2):
                pairs = a[pre+f'train_pairs_t{ti}'] @ q.T
                diff = (pairs[:,0]-pairs[:,1])/2
                for m in MS:
                    u,s,_ = np.linalg.svd(diff[:m].T,full_matrices=False)
                    basis = u[:,:min(m,D)]; phat = basis @ basis.conj().T
                    fits[seed,qi,ti,m] = phat
                    stem = f'{pre}q{qi}_t{ti}_m{m}'
                    derived[stem+'_projector'] = phat; derived[stem+'_singular_values'] = s
                    cosines = np.linalg.svd((q[:,D:]).conj().T@basis,compute_uv=False)
                    structural.append({'seed':seed,'Q':QNAMES[qi],'train_eta':TRAIN_ETAS[ti],'m':m,'rank':int(np.linalg.matrix_rank(phat,tol=TOL)),'retained_rank':min(m,D),'difference_numeric_rank':int(np.sum(s>TOL)),'rank_tolerance':TOL,'rank_cutoff_gap':float(s[min(m,D)-1]-(s[min(m,D)] if len(s)>min(m,D) else 0.)),'rank_cutoff_near_tie':bool(len(s)>min(m,D) and abs(s[min(m,D)-1]-s[min(m,D)])<=TOL),'principal_angle_cosines':cosines.tolist(),'projector_distance':float(np.linalg.norm(phat-oracle)/np.sqrt(2*D)),'hermitian_error':err(phat-phat.conj().T),'idempotent_error':err(phat@phat-phat),'transport_error':err(phat-q@fitted_identity[ti,m]@q.T),'singular_values':s.tolist()})
            for ri in range(2):
                w = a[pre+f'eval_records_r{ri}']; cal = a[pre+f'cal_records_r{ri}']
                for ei in range(2):
                    query = a[pre+f'queries_r{ri}_e{ei}']
                    if qi==0:
                        for j,x in enumerate(query): query_manifest.append({'query_id':f'{seed}-r{ri}-e{ei}-q{j:02d}','seed':seed,'r':RS[ri],'eval_eta':ETAS[ei],'claim':j//2,'repetition':j%2,'array_sha256':digest_array(x)})
                    # Include all declared raw/derived vector banks in Gram/norm controls.
                    x = np.concatenate([w,cal,query,a[pre+'train_clean_pairs'].reshape(-1,N),a[pre+'train_pairs_t0'].reshape(-1,N),a[pre+'train_pairs_t1'].reshape(-1,N)])
                    xq = x@q.T; basep = x@P.T; rotp = xq@oracle.T
                    gram = xq.conj()@xq.T
                    real_h = xq.real@xq.real.T+xq.imag@xq.imag.T+1j*(xq.real@xq.imag.T-xq.imag@xq.real.T)
                    algebra.append({'seed':seed,'Q':QNAMES[qi],'r':RS[ri],'eval_eta':ETAS[ei],'orthogonality_error':err(q.T@q-np.eye(N)),'full_product_error':err(gram-x.conj()@x.T),'full_norm_error':err(np.linalg.norm(xq,axis=1)-np.linalg.norm(x,axis=1)),'oracle_product_error':err(rotp.conj()@rotp.T-basep.conj()@basep.T),'oracle_norm_error':err(np.linalg.norm(rotp,axis=1)-np.linalg.norm(basep,axis=1)),'real_channel_error':err(gram-real_h),'oracle_hermitian_error':err(oracle-oracle.conj().T),'oracle_idempotent_error':err(oracle@oracle-oracle)})
                for ti in range(2):
                    for m in MS:
                        for method in METHODS:
                            proj = {'full':np.eye(N),'naive':P,'oracle':oracle,'estimated':fits[seed,qi,ti,m]}[method]
                            centre,available = centres(cal[::3]@q.T,cal@q.T,proj)
                            key = f'{pre}q{qi}_r{ri}_t{ti}_m{m}_{method}'
                            derived[key+'_centres'] = centre; derived[key+'_available'] = available
    np.savez_compressed(out/'structures_centres.npz',**derived)
    dump(out/'QUERY_MANIFEST.json',query_manifest)
    dump(out/'STRUCTURAL_DIAGNOSTICS.json',structural); dump(out/'ALGEBRA_DIAGNOSTICS.json',algebra)
    dump(out/'PRE_SCORING_CHECKPOINT.json',{'inputs_sha256':file_hash(out/'inputs.npz'),'structures_centres_sha256':file_hash(out/'structures_centres.npz'),'query_manifest_sha256':file_hash(out/'QUERY_MANIFEST.json'),'time_unix':time.time()})
    ledger = []; paired = []; aggregates = {}; invariance = []; baselines = {}
    for seed in SEEDS:
        pre = f's{seed}_'
        for qi,q in enumerate(a[pre+'Q']):
            oracle = q@P@q.T
            for ri,r in enumerate(RS):
                w = a[pre+f'eval_records_r{ri}']@q.T
                for ei,eta in enumerate(ETAS):
                    query = a[pre+f'queries_r{ri}_e{ei}']@q.T
                    for ti,teta in enumerate(TRAIN_ETAS):
                        for m in MS:
                            pair_ids = []
                            for method in METHODS:
                                proj = {'full':np.eye(N),'naive':P,'oracle':oracle,'estimated':fits[seed,qi,ti,m]}[method]
                                key = f'{pre}q{qi}_r{ri}_t{ti}_m{m}_{method}'
                                h,valid = products(query,w,proj)
                                labels,reasons = decode(h,valid,derived[key+'_centres'],derived[key+'_available'])
                                scores = np.abs(h); top = np.argsort(-scores,axis=1,kind='stable')[:,:3]
                                gap = np.sort(scores,axis=1)[:,-3]-np.sort(scores,axis=1)[:,-4]
                                control_key = (seed,ri,ei,ti,m,method)
                                metrics_for_condition = []
                                for j,indices in enumerate(top):
                                    claim = j//2; relevant = indices//3==claim
                                    correct = labels[j,indices]==np.array(STATUS)[indices%3]
                                    abst = reasons[j,indices]; pred = labels[j,indices]
                                    gold_indices = np.arange(3*claim,3*claim+3)
                                    metrics = {'evidence_recall':float(np.sum(relevant)/3),'evidence_complete':int(np.all(relevant)),'joint_label_recall':float(np.sum(relevant&correct)/3),'joint_complete':int(np.all(relevant&correct)),'wrong_scope_count':int(np.sum(~relevant)),'encoded_U_recall':int(np.any((indices==3*claim+2)&(pred=='U'))),'abstain_count':int(np.sum(pred=='ABSTAIN')),'abstain_calibration_unavailable':int(np.sum(abst=='calibration_unavailable')),'abstain_ambiguous_centre':int(np.sum(abst=='ambiguous_centre')),'abstain_zero_product':int(np.sum(abst=='zero_product')),'oracle_relevant_stance_accuracy':float(np.mean(labels[j,gold_indices]==np.array(STATUS)))}
                                    condition = {'seed':seed,'Q':QNAMES[qi],'r':r,'eval_eta':eta,'train_eta':teta,'m':m}
                                    rowid = len(ledger)
                                    ledger.append(dict(condition,method=method,query_id=f'{seed}-r{ri}-e{ei}-q{j:02d}',query_index=j,claim=claim,repetition=j%2,returned_record_ids=[f'eval-e{x//6}-t{(x//3)%2}-{STATUS[x%3]}' for x in indices],returned_indices=indices.tolist(),scores=scores[j,indices].tolist(),predictions=pred.tolist(),reasons=abst.tolist(),angles=np.angle(h[j,indices]).tolist(),boundary_gap=float(gap[j]),near_boundary_tie=bool(gap[j]<=TOL),oracle_relevant_predictions=labels[j,gold_indices].tolist(),oracle_relevant_reasons=reasons[j,gold_indices].tolist(),metrics=metrics))
                                    metrics_for_condition.append(metrics)
                                    aggkey = json.dumps(dict(condition,method=method),sort_keys=True)
                                    if aggkey not in aggregates: aggregates[aggkey] = {'condition':dict(condition,method=method),'count':0,'metric_sums':{k:0. for k in metrics}}
                                    ag = aggregates[aggkey]; ag['count']+=1
                                    for k,v in metrics.items(): ag['metric_sums'][k]+=v
                                    pair_ids.append((j,method,rowid))
                                if method in ('full','oracle'):
                                    if qi==0: baselines[control_key]=(top.copy(),scores.copy(),labels.copy(),reasons.copy(),metrics_for_condition)
                                    else:
                                        bt,bs,bl,br,bm = baselines[control_key]
                                        set_mismatch = [j for j in range(32) if set(top[j])!=set(bt[j])]
                                        invariance.append({'seed':seed,'Q':QNAMES[qi],'r':r,'eval_eta':eta,'train_eta':teta,'m':m,'method':method,'top3_set_mismatch_queries':set_mismatch,'top3_order_mismatch_queries':np.flatnonzero(np.any(top!=bt,axis=1)).tolist(),'max_all_score_error':err(scores-bs),'prediction_mismatch_items':int(np.sum(labels!=bl)),'reason_mismatch_items':int(np.sum(reasons!=br)),'metric_mismatch_queries':[j for j in range(32) if metrics_for_condition[j]!=bm[j]],'near_boundary_queries':np.flatnonzero(gap<=TOL).tolist(),'set_mismatch_boundary_gaps':[float(gap[j]) for j in set_mismatch]})
                            for j in range(32):
                                paired.append({'seed':seed,'Q':QNAMES[qi],'r':r,'eval_eta':eta,'train_eta':teta,'m':m,'query_id':f'{seed}-r{ri}-e{ei}-q{j:02d}','method_record_indices':{method:rowid for jj,method,rowid in pair_ids if jj==j}})
    assert len(paired)==6912 and len(ledger)==27648
    with (out/'LEDGER.jsonl').open('w') as f:
        for row in ledger: f.write(json.dumps(row,allow_nan=False)+'\n')
    with (out/'PAIRED_ROWS.jsonl').open('w') as f:
        for row in paired: f.write(json.dumps(row)+'\n')
    aglist = list(aggregates.values())
    for ag in aglist: ag['metric_means']={k:v/ag['count'] for k,v in ag['metric_sums'].items()}
    dump(out/'AGGREGATES.json',aglist); dump(out/'INVARIANCE.json',invariance)
    diag_max = {k:max(row[k] for row in algebra) for k in algebra[0] if k.endswith('_error')}
    diag_max.update({'estimated_'+k:max(row[k] for row in structural) for k in ('hermitian_error','idempotent_error','transport_error')})
    dump(out/'SUMMARY.json',{'paired_rows':len(paired),'method_records':len(ledger),'base_query_ids':len(query_manifest),'unique_query_array_hashes':len({x['array_sha256'] for x in query_manifest}),'underlying_eval_entity_time_claims':48,'zero_noise_repetitions_are_duplicates':True,'controls_repeated_across_6_supervision_conditions':['full','naive','oracle'],'per_base_query_method_records':72,'diagnostic_max_errors':diag_max,'diagnostic_tolerance':TOL,'algebra_within_tolerance':all(v<=TOL for v in diag_max.values()),'elapsed_seconds':time.time()-started})
    dump(out/'OUTPUT_HASHES.json',{p.name:file_hash(p) for p in sorted(out.iterdir()) if p.is_file() and p.name not in ('OUTPUT_HASHES.json','ATTEMPT.json')})
    dump(out/'ATTEMPT.json',{'started_unix':started,'finished_unix':time.time(),'status':'complete','numpy':np.__version__,'elapsed_seconds':time.time()-started})
    print(json.dumps(json.loads((out/'SUMMARY.json').read_text()),indent=2))


if __name__=='__main__': main()
