#!/usr/bin/env python3
"""Independent bounded saved-array readout audit. Does not import study code.

Prospective selection: first two ledger rows per mode/evaluation ratio; first
noise-free matched SCOPED row per seed/ratio; first shifted/noisy row per mode.
This is independent recalculation on supplied data, not empirical replication.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np

TOL = 1e-10
LABELS = ['A', 'N', 'U']
METHODS = {'full_cos_angle': 'full', 'full_mod_angle': 'full',
           'real_AB_angle': 'real_AB', 'binding_mod_angle': 'binding'}

def products(q, records, family):
    if family == 'binding':
        q, records = q[24:], records[:, 24:]
    den = np.linalg.norm(q) * np.linalg.norm(records, axis=1)
    if family == 'real_AB':
        h = ((records.real @ q.real + records.imag @ q.imag)
             + 1j * (records.imag @ q.real - records.real @ q.imag))
    else:
        h = records @ q.conj()
    return np.divide(h, den, out=np.zeros_like(h), where=den > 0)

def fit(queries, records, family):
    angles = [[] for _ in LABELS]
    for row, q in enumerate(queries):
        entity_time = row // 2
        h = products(q, records[3*entity_time:3*entity_time+3], family)
        for s, value in enumerate(h):
            if abs(value) > TOL:
                angles[s].append(float(np.angle(value)))
    result = []
    for a in angles:
        z = np.mean(np.exp(1j*np.array(a))) if a else 0j
        result.append({'centre': float(np.angle(z)) if a and abs(z)>TOL else None,
                       'resultant_length': float(abs(z)), 'valid_angle_count': len(a)})
    return result

def decode(h, centres):
    if any(c['centre'] is None for c in centres):
        return 'ABSTAIN', 'calibration_unavailable'
    if abs(h) <= TOL:
        return 'ABSTAIN', 'zero_product'
    d = np.abs(np.angle(np.exp(1j*(np.angle(h)-np.array([c['centre'] for c in centres])))))
    order = np.argsort(d, kind='stable')
    if d[order[1]] - d[order[0]] <= TOL:
        return 'ABSTAIN', 'ambiguous_centre'
    return LABELS[int(order[0])], ''

def metrics(indices, predictions, reasons, entity, time, available):
    true = list(range(3*(2*entity+time), 3*(2*entity+time)+3))
    relevant = [i in true for i in indices]
    correct = [r and p == LABELS[i%3] for i,p,r in zip(indices,predictions,relevant)]
    return relevant, {
        'evidence_recall': sum(relevant)/3,
        'evidence_complete': int(all(relevant)),
        'joint_label_recall': sum(correct)/3,
        'joint_complete': int(all(correct)),
        'wrong_scope_count': 3-sum(relevant),
        'abstain_count': predictions.count('ABSTAIN'),
        'encoded_U_recall': int(any(i==true[2] and p=='U' for i,p in zip(indices,predictions))),
        'A_reference_agreement_at_1': int(indices[0]==true[0]),
        'decoded_A_at_1_if_relevant': (predictions[0]=='A') if relevant[0] else None,
        'top1_relevant': relevant[0],
        'top1_source_A': indices[0]%3==0,
        'decoder_calibration_available': int(available),
        **{'abstain_'+reason+'_count': reasons.count(reason) for reason in
           ('calibration_unavailable','zero_product','ambiguous_centre')},
    }

def select(rows):
    selected = set()
    groups = {}
    matched = set()
    shifted = set()
    for i,row in enumerate(rows):
        c = row['condition']
        key = (c['mode'], float(c['eval_ratio']))
        groups.setdefault(key, [])
        if len(groups[key]) < 2:
            groups[key].append(i); selected.add(i)
        k = (c['seed'], float(c['eval_ratio']))
        if (c['mode']=='SCOPED' and c['cal_ratio']==c['eval_ratio']
                and c['cal_noise']==0 and c['eval_noise']==0 and k not in matched):
            selected.add(i); matched.add(k)
        if (c['cal_ratio']!=c['eval_ratio'] and c['eval_noise']>0
                and c['mode'] not in shifted):
            selected.add(i); shifted.add(c['mode'])
    assert len(selected)<=96
    assert len(groups)==6 and len(matched)==9 and len(shifted)==2
    return sorted(selected)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output_dir'); args=ap.parse_args()
    out=Path(args.output_dir)
    with gzip.open(out/'ledger.jsonl.gz','rt') as f: rows=[json.loads(x) for x in f]
    queries=np.load(out/'queries.npz'); arrays=np.load(out/'latent_noise_records.npz')
    saved_centres=json.loads((out/'centres.json').read_text())
    hashes=json.loads((out/'frozen_query_hashes.json').read_text())
    failures=[]; checked=[]; fitted={}; metric_keys=set(); ranking_diagnostics=[]
    schema_notes=[]; centre_checks=0; analytical=[]
    centre_map={(x['seed'],x['mode'],x['cal_ratio'],x['cal_noise'],x['family']):x for x in saved_centres}
    def check(ok, message):
        if not ok: failures.append(message)
    check(len(rows)==10368, 'ledger cardinality')
    for index in select(rows):
        row=rows[index]; c=row['condition']; qid=row['query_id']
        qkey,qrow=qid.rsplit('_q',1); q=queries[qkey][int(qrow)]
        digest=hashlib.sha256(np.ascontiguousarray(q,dtype='<c16').tobytes()).hexdigest()
        check(digest==row['query_sha256']==hashes[qid], f'query hash row {index}')
        record_key=f"eval_s{c['seed']}_{c['mode']}_r{float(c['eval_ratio'])}_records"
        if row['evaluation_record_key'] not in arrays.files:
            schema_notes.append('evaluation_record_key identifies ledger condition/query rather than saved NPZ key; audit derived NPZ key from condition')
        records=arrays[record_key]
        for method,family in METHODS.items():
            key=(c['seed'],c['mode'],c['cal_ratio'],c['cal_noise'],family)
            if key not in fitted:
                prefix=f"cal_s{c['seed']}_{c['mode']}_r{float(c['cal_ratio'])}"
                fitted[key]=fit(queries[prefix+f"_eta{float(c['cal_noise'])}"],
                                arrays[prefix+'_records'],family)
                saved=centre_map[key]
                check(saved['calibration_entities']==[8,9,10,11],f'centre {key} isolation')
                for ours,theirs in zip(fitted[key],saved['diagnostics']):
                    centre_checks+=1
                    check(ours['valid_angle_count']==theirs['valid_angle_count'],f'centre {key} counts')
                    check(abs(ours['resultant_length']-theirs['resultant_length'])<=TOL,f'centre {key} resultant')
                    if ours['centre'] is None or theirs['centre'] is None:
                        check(ours['centre'] is theirs['centre'],f'centre {key} availability')
                    else:
                        check(abs(np.angle(np.exp(1j*(ours['centre']-theirs['centre']))))<=TOL,f'centre {key} angle')
            centres=fitted[key]
            h=products(q,records,family)
            scores=h.real if method=='full_cos_angle' else np.abs(h)
            recomputed_indices=np.argsort(-scores,kind='stable')[:3].tolist()
            recorded=row['methods'][method]
            indices=recorded['retrieved_indices']
            if indices!=recomputed_indices:
                omitted=[i for i in recomputed_indices if i not in indices]
                selected_only=[i for i in indices if i not in recomputed_indices]
                boundary=max((float(scores[a]-scores[b]) for a in omitted for b in selected_only),default=0.)
                ranking_diagnostics.append({'row':index,'method':method,'independent':recomputed_indices,
                    'recorded':indices,'same_set':set(indices)==set(recomputed_indices),'boundary_advantage':boundary})
                check(boundary<=TOL,f'row {index} {method} top3 set outside numerical tolerance')
            check(len(set(indices))==3 and all(0<=i<48 for i in indices),f'row {index} {method} index validity')
            check(all(scores[indices[j+1]]-scores[indices[j]]<=TOL for j in range(2)),f'row {index} {method} score ordering')
            decoded=[decode(h[i],centres) for i in indices]
            predictions=[p for p,r in decoded]; reasons=[r for p,r in decoded]
            label=f'row {index} {method}'
            check(predictions==recorded['predictions'],label+' predictions')
            check(reasons==recorded['reasons'],label+' reasons')
            relevant,m=metrics(indices,predictions,reasons,row['entity'],row['time'],
                               all(x['centre'] is not None for x in centres))
            true=list(range(3*(2*row['entity']+row['time']),3*(2*row['entity']+row['time'])+3))
            oracle_dec=[decode(h[i],centres) for i in true]
            m['oracle_relevant_stance_accuracy']=sum(p==LABELS[j] for j,(p,r) in enumerate(oracle_dec))/3
            check(relevant==recorded['relevant'],label+' relevant')
            for name, value in recorded['metrics'].items():
                metric_keys.add(name)
                aliases={'encoded_u_recall':'encoded_U_recall',
                         'a_reference_agreement_at_1':'A_reference_agreement_at_1',
                         'a_reference_agreement_at1':'A_reference_agreement_at_1'}
                canonical=aliases.get(name,name)
                if canonical in m:
                    if value is None or m[canonical] is None: check(value is m[canonical],label+' metric '+name)
                    else: check(abs(value-m[canonical])<=TOL,label+' metric '+name)
                else: failures.append(label+' unknown metric '+name)
            oracle=recorded['oracle_relevant_diagnostic']
            check(oracle['indices']==true,label+' oracle indices')
            check(oracle['predictions']==[p for p,r in oracle_dec],label+' oracle predictions')
            check(oracle['reasons']==[r for p,r in oracle_dec],label+' oracle reasons')
        checked.append({'ledger_index':index,'query_id':qid,'condition':c})
    for ratio in (.5,1.,2.):
        phases=np.array([1,-1,np.exp(1j*np.pi/3)])
        q=np.array([ratio,1],complex)/np.sqrt(ratio**2+1)
        w=np.column_stack((np.full(3,ratio),phases))/np.sqrt(ratio**2+1)
        actual=w@q.conj(); expected=(ratio**2+phases)/(ratio**2+1)
        check(np.max(abs(actual-expected))<=TOL,'analytical scoped product')
        analytical.append({'ratio':ratio,'full_own_scope_products':[[float(x.real),float(x.imag)] for x in actual],
                           'N_zero':bool(abs(actual[1])<=TOL),
                           'A_N_angle_collision':bool(abs(actual[1])>TOL and abs(np.angle(actual[1])-np.angle(actual[0]))<=TOL)})
    result={'independence':'Independent code on same supplied arrays/platform; not empirical replication.',
            'sample_rule':__doc__,'sample_count':len(checked),'method_count':4*len(checked),
            'checked_rows':checked,'metric_keys':sorted(metric_keys),
            'failure_count':len(failures),'failures':failures,
            'centres_diagnostic_checks':centre_checks,
            'ranking_diagnostics':ranking_diagnostics,'schema_notes':sorted(set(schema_notes)),
            'analytical_scoped_cases':analytical,
            'saved_centres_type':type(saved_centres).__name__}
    destination=Path(__file__).parent/'AUDIT_RESULTS.json'
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'result':str(destination),'sample_count':len(checked),'failure_count':len(failures)}))

if __name__=='__main__': main()
