#!/usr/bin/env python3
"""Independent saved-input reconstruction. Never imports the experiment."""
import argparse, hashlib, json
from pathlib import Path
import numpy as np

T=1e-10
SEEDS=(92501,92507,92509); QS=('identity','dense','plane'); RS=(.5,2.); ES=(0.,1.5); TS=(0.,.25); MS=(4,12,48); METHODS=('full','naive','oracle','estimated'); STATUS=np.array(['A','N','U'])
P=np.diag([0.]*12+[1.]*12)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('run'); args=parser.parse_args(); root=Path(args.run)
    a=np.load(root/'inputs.npz'); saved=np.load(root/'structures_centres.npz')
    failures=[]; maxima={}; counts={}; near_ties=[]; order_differences=[]
    def check(name,x,y,tol=T):
        x=np.asarray(x); y=np.asarray(y)
        residual=float(np.max(np.abs(x-y))) if x.size else 0.
        maxima[name]=max(maxima.get(name,0.),residual); counts[name]=counts.get(name,0)+1
        if residual>tol: failures.append({'check':name,'residual':residual,'context':context})
    def same(name,x,y):
        counts[name]=counts.get(name,0)+1
        if np.asarray(x).tolist()!=np.asarray(y).tolist(): failures.append({'check':name,'actual':np.asarray(x).tolist(),'saved':np.asarray(y).tolist(),'context':context})
    def norm(v): return v/np.sqrt(np.sum(abs(v)**2,axis=-1,keepdims=True))
    def digest(v):
        v=np.ascontiguousarray(v); h=hashlib.sha256(); h.update(str(v.dtype).encode()); h.update(str(v.shape).encode()); h.update(v.tobytes()); return h.hexdigest()
    def prod(left,right,projector):
        # Explicit column action, represented as batches of row vectors.
        l=(projector@left.T).T; r=(projector@right.T).T
        ln=np.sqrt(np.sum(abs(l)**2,axis=1)); rn=np.sqrt(np.sum(abs(r)**2,axis=1))
        lu=np.divide(l,ln[:,None],out=np.zeros_like(l,dtype=complex),where=ln[:,None]>T)
        ru=np.divide(r,rn[:,None],out=np.zeros_like(r,dtype=complex),where=rn[:,None]>T)
        h=np.einsum('ik,jk->ij',lu.conj(),ru)
        real=(lu.real@ru.real.T+lu.imag@ru.imag.T)+1j*(lu.real@ru.imag.T-lu.imag@ru.real.T)
        check('normalized_real_channel',h,real)
        return h,(ln[:,None]>T)&(rn[None,:]>T)&(abs(h)>T)
    def decode(h,valid,c,avail):
        predictions=np.full(h.shape,'ABSTAIN',dtype='<U7'); reasons=np.full(h.shape,'zero_product',dtype='<U24')
        if not all(avail): reasons[:]='calibration_unavailable'; return predictions,reasons
        for index in np.ndindex(h.shape):
            if not valid[index]: continue
            distances=abs(np.angle(h[index]*np.conj(c)))
            rank=sorted(range(3),key=lambda k:distances[k])
            if distances[rank[1]]-distances[rank[0]]<=T: reasons[index]='ambiguous_centre'
            else: predictions[index]=STATUS[rank[0]]; reasons[index]='ok'
        return predictions,reasons
    context={}
    manifest=json.loads((root/'INPUT_MANIFEST.json').read_text())
    same('input_file_hash',hashlib.sha256((root/'inputs.npz').read_bytes()).hexdigest(),manifest['file_sha256'])
    for key in a.files:
        context={'array':key}; same('input_array_hash',digest(a[key]),manifest['arrays'][key]['sha256'])
    ledger={}
    for line in (root/'LEDGER.jsonl').read_text().splitlines():
        row=json.loads(line)
        if row['query_index'] in (0,31): ledger[(row['seed'],row['Q'],row['r'],row['eval_eta'],row['train_eta'],row['m'],row['method'],row['query_index'])]=row
    structural={(x['seed'],x['Q'],x['train_eta'],x['m']):x for x in json.loads((root/'STRUCTURAL_DIAGNOSTICS.json').read_text())}
    for seed in SEEDS:
        pre=f's{seed}_'; get=lambda k:a[pre+k]
        context={'seed':seed}
        check('predicate_normalization',get('predicate'),norm(get('predicate_raw')))
        for pool,n in [('eval',8),('cal',4)]:
            eu=norm(get(pool+'_entity_raw')); tu=norm(get(pool+'_time_raw'))
            check('entity_normalization',get(pool+'_entity_unit'),eu); check('time_normalization',get(pool+'_time_unit'),tu)
            c=norm((eu[:,None,:]+tu[None,:,:]+get('predicate')).reshape(-1,12)); b=norm(get(pool+'_binding_raw'))
            check('context_generation',get(pool+'_context'),c); check('binding_generation',get(pool+'_binding'),b)
            for ri,r in enumerate(RS):
                records=np.array([np.r_[r*c[j],phase*b[j]]/np.sqrt(1+r*r) for j in range(n*2) for phase in [1,-1,np.exp(1j*np.pi/3)]])
                check('record_generation',get(f'{pool}_records_r{ri}'),records)
        for bank in ['train','query']:
            check('noise_normalization',get(bank+'_noise_unit'),norm(get(bank+'_noise_raw')))
        tc=norm(get('train_context_raw')); tb=norm(get('train_binding_raw'))
        check('training_clean_pairs',get('train_clean_pairs'),np.stack([np.c_[tc,tb],np.c_[tc,-tb]],axis=1)/np.sqrt(2))
        for ti,eta in enumerate(TS): check('training_noise_addition',get(f'train_pairs_t{ti}'),get('train_clean_pairs')+eta*get('train_noise_unit'))
        for ri in range(2):
            for ei,eta in enumerate(ES): check('query_noise_addition',get(f'queries_r{ri}_e{ei}'),norm(np.repeat(get(f'eval_records_r{ri}')[::3],2,axis=0)+eta*get('query_noise_unit')))
        for qi,q in enumerate(get('Q')):
            context={'seed':seed,'Q':QS[qi]}; check('orthogonality',q.T@q,np.eye(24))
            oracle=q@P@q.T
            for ti in range(2):
                pairs=get(f'train_pairs_t{ti}'); base_diff=((pairs[:,0]-pairs[:,1])/2).T
                for m in MS:
                    context={'seed':seed,'Q':QS[qi],'train_eta':TS[ti],'m':m}
                    u,s,_=np.linalg.svd(q@base_diff[:,:m],full_matrices=False); basis=u[:,:min(m,12)]; fit=basis@basis.conj().T
                    ub,_,_=np.linalg.svd(base_diff[:,:m],full_matrices=False); identityfit=ub[:,:min(m,12)]@ub[:,:min(m,12)].conj().T
                    stem=f'{pre}q{qi}_t{ti}_m{m}'; check('saved_projector',fit,saved[stem+'_projector']); check('saved_singular_values',s,saved[stem+'_singular_values'])
                    diag=structural[(seed,QS[qi],TS[ti],m)]
                    values={'hermitian_error':np.max(abs(fit-fit.conj().T)),'idempotent_error':np.max(abs(fit@fit-fit)),'transport_error':np.max(abs(fit-q@identityfit@q.T)),'projector_distance':np.linalg.norm(fit-oracle)/np.sqrt(24),'principal_angle_cosines':np.linalg.svd(q[:,12:].T@basis,compute_uv=False),'singular_values':s}
                    for name,value in values.items(): check('structural_'+name,value,diag[name])
                    same('structural_rank',int(np.linalg.matrix_rank(fit,tol=T)),diag['rank'])
                    check('transported_estimate',fit,q@identityfit@q.T)
                    if ti==0: check('clean_distance_formula',np.linalg.norm(fit-oracle)/np.sqrt(24),np.sqrt((12-min(m,12))/24))
                    for ri,r in enumerate(RS):
                        w0=get(f'eval_records_r{ri}'); cal0=get(f'cal_records_r{ri}'); w=w0@q.T; cal=cal0@q.T
                        for method,projector in [('full',np.eye(24)),('naive',P),('oracle',oracle),('estimated',fit)]:
                            hcal,vcal=prod(cal[::3],cal,projector); c=np.zeros(3,complex); avail=np.zeros(3,bool)
                            for k in range(3):
                                vals=np.array([hcal[j,3*j+k] for j in range(8) if vcal[j,3*j+k]])
                                if len(vals): c[k]=np.mean(np.exp(1j*np.angle(vals))); avail[k]=abs(c[k])>T
                            key=f'{pre}q{qi}_r{ri}_t{ti}_m{m}_{method}'
                            check('saved_centres',c,saved[key+'_centres']); same('saved_available',avail,saved[key+'_available'])
                            for ei,eta in enumerate(ES):
                                context={'seed':seed,'Q':QS[qi],'r':r,'eval_eta':eta,'train_eta':TS[ti],'m':m,'method':method}
                                query0=get(f'queries_r{ri}_e{ei}')[[0,31]]; query=query0@q.T; h,valid=prod(query,w,projector)
                                if method in ('full','oracle'):
                                    baseprojector=np.eye(24) if method=='full' else P
                                    check(method+'_normalized_product_invariance',h,prod(query0,w0,baseprojector)[0])
                                pred,reasons=decode(h,valid,c,avail)
                                for j,queryindex in enumerate([0,31]):
                                    context['query_index']=queryindex; row=ledger[(seed,QS[qi],r,eta,TS[ti],m,method,queryindex)]
                                    scores=abs(h[j]); top=np.argsort(-scores,kind='stable')[:3]; savedidx=np.array(row['returned_indices'])
                                    sortedscore=np.sort(scores); gap=sortedscore[-3]-sortedscore[-4]
                                    check('boundary_gap',gap,row['boundary_gap']); same('near_boundary_tie',bool(gap<=T),row['near_boundary_tie'])
                                    check('returned_scores',scores[savedidx],row['scores']); check('returned_angles',np.angle(np.exp(1j*(np.angle(h[j,savedidx])-np.array(row['angles'])))),np.zeros(3))
                                    same('predictions',pred[j,savedidx],row['predictions']); same('reasons',reasons[j,savedidx],row['reasons'])
                                    gold=np.arange(3*(queryindex//2),3*(queryindex//2)+3)
                                    same('oracle_relevant_predictions',pred[j,gold],row['oracle_relevant_predictions']); same('oracle_relevant_reasons',reasons[j,gold],row['oracle_relevant_reasons'])
                                    if top.tolist()!=savedidx.tolist():
                                        item={'context':dict(context),'reconstructed':top.tolist(),'saved':savedidx.tolist(),'boundary_gap':float(gap),'saved_score_discrepancy':float(np.max(abs(scores[top]-scores[savedidx])))}
                                        order_differences.append(item)
                                        if item['saved_score_discrepancy']>T: failures.append({'check':'retrieval_order','detail':item})
                                    if gap<=T: near_ties.append(dict(context))
    algebra={(x['seed'],x['Q'],x['r'],x['eval_eta']):x for x in json.loads((root/'ALGEBRA_DIAGNOSTICS.json').read_text())}
    for seed in SEEDS:
        pre=f's{seed}_'; get=lambda k:a[pre+k]
        context={'seed':seed}
        same('stream_spawn_keys',get('stream_spawn_keys'),np.arange(5).reshape(5,1))
        qr,rr=np.linalg.qr(get('rotation_raw')); qr=qr*np.where(np.diag(rr)<0,-1,1)
        check('canonical_dense_Q',get('Q')[1],qr)
        check('identity_Q',get('Q')[0],np.eye(24))
        plane=np.eye(24); plane[0,0]=plane[12,12]=np.cos(np.pi/4); plane[0,12]=-np.sin(np.pi/4); plane[12,0]=np.sin(np.pi/4)
        # Either documented plane sign convention is equivalent to opposite angle; saved convention checked by orthogonality and nonmixed axes.
        nonmixed=[j for j in range(24) if j not in (0,12)]
        check('plane_fixed_axes',get('Q')[2][:,nonmixed],np.eye(24)[:,nonmixed])
        check('plane_angle_magnitude',abs(get('Q')[2][np.ix_([0,12],[0,12])]),abs(plane[np.ix_([0,12],[0,12])]))
        for qi,q in enumerate(get('Q')):
            oracle=q@P@q.T
            for ri,r in enumerate(RS):
                for ei,eta in enumerate(ES):
                    context={'seed':seed,'Q':QS[qi],'r':r,'eval_eta':eta}
                    x=np.concatenate([get(f'eval_records_r{ri}'),get(f'cal_records_r{ri}'),get(f'queries_r{ri}_e{ei}'),get('train_clean_pairs').reshape(-1,24),get('train_pairs_t0').reshape(-1,24),get('train_pairs_t1').reshape(-1,24)])
                    moved=(q@x.T).T; base=(P@x.T).T; actual=(oracle@moved.T).T
                    gram=np.einsum('ik,jk->ij',moved.conj(),moved); bg=np.einsum('ik,jk->ij',x.conj(),x)
                    real=moved.real@moved.real.T+moved.imag@moved.imag.T+1j*(moved.real@moved.imag.T-moved.imag@moved.real.T)
                    resid=lambda z:float(np.max(abs(z)))
                    values={'orthogonality_error':resid(q.T@q-np.eye(24)),'full_product_error':resid(gram-bg),'full_norm_error':resid(np.linalg.norm(moved,axis=1)-np.linalg.norm(x,axis=1)),'oracle_product_error':resid(actual.conj()@actual.T-base.conj()@base.T),'oracle_norm_error':resid(np.linalg.norm(actual,axis=1)-np.linalg.norm(base,axis=1)),'real_channel_error':resid(gram-real),'oracle_hermitian_error':resid(oracle-oracle.conj().T),'oracle_idempotent_error':resid(oracle@oracle-oracle)}
                    for name,value in values.items():
                        check('algebra_reconciled_'+name,value,algebra[(seed,QS[qi],r,eta)][name])
                        check('algebra_direct_'+name,value,0.)
    result={'status':'pass_with_tie_order_differences' if not failures and order_differences else ('pass' if not failures else 'fail'),'sample_method_records':len(ledger),'failures':failures,'max_residuals':maxima,'check_counts':counts,'near_boundary_samples':near_ties,'last_bit_order_differences':order_differences,'independence_disclosure':'No experiment or predecessor import and no main execution. Source inspection exceeded array-location scope: source expressions and projection/centres/decode definitions were read to identify complex resultant centre representation. This is independently coded numerical replay, not implementation-blind review.','selection':'Prospectively fixed first/last query each condition; all calibration pairs.'}
    Path(__file__).with_name('REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sample_method_records':len(ledger),'failures':len(failures),'tie_order_differences':len(order_differences),'max_residual':max(maxima.values())},indent=2))

if __name__=='__main__':main()
