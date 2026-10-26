"""Independent resumed classification; does not import experiment or replay code."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import json,hashlib,re
from pathlib import Path
from collections import Counter
import numpy as np
HERE=Path(__file__).resolve().parent; RUN=HERE.parent/'run'; T=1e-10
def main():
    source=np.load(RUN/'source_inputs.npz',allow_pickle=False)
    probe=np.load(RUN/'probe_inputs.npz',allow_pickle=False)
    saved=np.load(RUN/'structures_centres.npz',allow_pickle=False)
    pool=np.load(RUN/'outcomes.npz',allow_pickle=False)
    mapping=json.loads((RUN/'OUTCOME_MAP.json').read_text())['conditions']
    configs=json.loads((RUN/'CALIBRATION_CONFIGS.json').read_text())
    row_lookup={}
    for line in (RUN/'LEDGER.jsonl').read_text().splitlines():
        r=json.loads(line)
        if r['query_index'] in (0,31):row_lookup[(r['outcome_key'],r['query_index'])]=r
    projectors={}; calibration={}; differences=[]; maxima=Counter();counts=Counter()
    def prods(q,x,p):
        a=q@p.T;b=x@p.T
        an=np.linalg.norm(a,axis=1);bn=np.linalg.norm(b,axis=1)
        a=np.divide(a,an[:,None],out=np.zeros_like(a),where=an[:,None]>T)
        b=np.divide(b,bn[:,None],out=np.zeros_like(b),where=bn[:,None]>T)
        z=a.conj()@b.T
        return z,(an[:,None]>T)&(bn[None,:]>T)&(np.abs(z)>T)
    def labels(z,v,cent,available):
        lab=np.full(z.shape,'ABSTAIN',dtype='<U7');why=np.full(z.shape,'calibration_unavailable',dtype='<U23')
        if not all(available):return lab,why
        dist=np.abs(np.angle(np.exp(1j*(np.angle(z)[...,None]-np.angle(cent)))))
        nearest=np.argsort(dist,axis=-1,kind='stable');ds=np.take_along_axis(dist,nearest,axis=-1)
        tie=ds[...,1]-ds[...,0]<=T;good=v&~tie
        why[:]='zero_product';why[v&tie]='ambiguous_centre';why[good]='ok'
        lab[good]=np.array(['A','N','U'])[nearest[...,0][good]]
        return lab,why
    for cfg in configs:
        key=cfg['projector_key'];seed=cfg['seed'];q=source[f's{seed}_Q'][1]
        if key not in projectors:
            if cfg['method']=='full':p=np.eye(24)
            elif cfg['method']=='oracle':p=q@np.diag([0]*12+[1]*12)@q.T
            else:
                raw=f's{seed}_a{cfg["ai"]}_{cfg["probe"]}'
                field='average' if cfg['method']=='repaired' else 'solved'
                # Independent transpose-SVD reconstruction used by the failed replay.
                u,s,_=np.linalg.svd(probe[raw+'_'+field][:cfg['m']].T,full_matrices=False)
                rank=min(12,int(sum(s>T)));p=u[:,:rank]@u[:,:rank].T if rank else np.zeros((24,24))
            projectors[key]=p
        p=projectors[key];records=source[f's{seed}_cal_records_r{cfg["ri"]}']@q.T
        z,v=prods(records[::3],records,p);ix=np.arange(8)[:,None]*3+np.arange(3)
        z=np.take_along_axis(z,ix,1);v=np.take_along_axis(v,ix,1)
        cent=np.array([np.mean(z[v[:,j],j]/np.abs(z[v[:,j],j])) if any(v[:,j]) else 0j for j in range(3)])
        calibration[cfg['key']]=(cent,(v.sum(0)>0)&(np.abs(cent)>T))
    for key,fields in mapping.items():
        match=re.fullmatch(r's(\d+)_a([34])_(.+)_m(12|48)_r([01])_(full|oracle|repaired|solved)_e([01])',key)
        seed,ai,arm,m,ri,method,ei=match.groups();q=source[f's{seed}_Q'][1]
        stem=f's{seed}_a{ai}_{arm}_m{m}';p=projectors[stem+'_'+method+'_projector']
        queries=source[f's{seed}_queries_r{ri}_e{ei}']@q.T;records=source[f's{seed}_eval_records_r{ri}']@q.T
        z,v=prods(queries,records,p);lab,why=labels(z,v,*calibration[key.rsplit('_e',1)[0]])
        score=abs(z);rank=np.argsort(-score,axis=1,kind='stable')
        sv=pool[fields['valid']];sl=pool[fields['labels']];sr=pool[fields['reasons']]
        sz=pool[fields['products']];ss=pool[fields['scores']];st=pool[fields['top']]
        changed_condition=False
        for qi in (0,31):
            counts['selected_rows']+=1;counts['fixed_candidate_readouts']+=48
            for name,a,b in [('valid',v[qi],sv[qi]),('label',lab[qi],sl[qi]),('reason',why[qi],sr[qi])]:
                counts['fixed_'+name+'_differences']+=int(sum(a!=b))
            maxima['product_max_abs']=max(maxima['product_max_abs'],float(max(abs(z[qi]-sz[qi]))))
            maxima['score_max_abs']=max(maxima['score_max_abs'],float(max(abs(score[qi]-ss[qi]))))
            top=rank[qi,:3];old=st[qi]
            if not np.array_equal(top,old):
                changed_condition=True;counts['changed_top_rows']+=1
                same=set(top)==set(old);counts['order_only_rows' if same else 'membership_changed_rows']+=1
                ids=sorted(set(top)|set(old));gap=float(np.ptp(ss[qi,ids]));gap2=float(np.ptp(score[qi,ids]))
                if not same:
                    leaving=sorted(set(old)-set(top));entering=sorted(set(top)-set(old))
                    exchanged=leaving+entering
                    maxima['membership_exchange_saved_score_range']=max(maxima['membership_exchange_saved_score_range'],float(np.ptp(ss[qi,exchanged])))
                    maxima['membership_exchange_replay_score_range']=max(maxima['membership_exchange_replay_score_range'],float(np.ptp(score[qi,exchanged])))
                row=row_lookup[(key,qi)]
                changed_label=not np.array_equal(lab[qi,top],row['predictions'])
                counts['returned_label_mismatch_rows']+=changed_label
                differences.append(dict(condition=key,query_index=qi,saved=old.tolist(),replayed=top.tolist(),same_membership=same,
                    fixed_ids=ids,saved_scores=ss[qi,ids].tolist(),replay_scores=score[qi,ids].tolist(),
                    saved_labels=sl[qi,ids].tolist(),replayed_labels=lab[qi,ids].tolist(),
                    saved_reasons=sr[qi,ids].tolist(),replayed_reasons=why[qi,ids].tolist()))
        counts['changed_top_condition_arrays']+=changed_condition
    result=dict(counts=counts,maxima=maxima,classification= differences,
        contract='Exact ordering discrepancies remain original replay failures; near score values alone do not waive them.',
        imports='No experiment/replay imports; source inspection disclosed in prospective review.',
        code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'RESUME_INDEPENDENT_CHECKS.json').write_text(json.dumps(result,indent=2,default=lambda x:x.item())+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='classification'},indent=2,default=lambda x:x.item()))
if __name__=='__main__':main()
