"""Recompute every stored pipeline metric from returned IDs/labels; no experiment import."""
from pathlib import Path
from collections import Counter
import gzip, json, hashlib, math, sys

R=Path(sys.argv[1]).resolve()
OUT=Path(__file__).resolve().parent
STAT=('A','N','U')
centres={ (x['seed'],x['mode'],x['cal_ratio'],x['cal_noise'],x['family']):x for x in json.loads((R/'centres.json').read_text()) }
keys={}; accum={}; discrepancies=[]; reasons_total=Counter(); methods_total=Counter(); qids=Counter(); qhashes=Counter(); rows=0

def same(a,b):
    if a is None or b is None:return a is b
    if isinstance(a,(float,int)) and isinstance(b,(float,int)):return abs(a-b)<=1e-12
    return a==b

def fail(kind,info):
    if len(discrepancies)<30:discrepancies.append({'kind':kind,'detail':info})

with gzip.open(R/'ledger.jsonl.gz','rt') as f:
 for line in f:
    x=json.loads(line);rows+=1;c=x['condition'];scope=2*x['entity']+x['time'];true=set(range(3*scope,3*scope+3))
    qids[x['query_id']]+=1;qhashes[x['query_sha256']]+=1
    if x['evaluation_record_key'] in keys:fail('duplicate_record_key',x['evaluation_record_key'])
    keys[x['evaluation_record_key']]=1
    if c['ratio_match']!=(c['cal_ratio']==c['eval_ratio']) or c['noise_match']!=(c['cal_noise']==c['eval_noise']):fail('match_flag',x['evaluation_record_key'])
    if set(x['methods'])!={'full_cos_angle','full_mod_angle','real_AB_angle','binding_mod_angle'}:fail('method_set',x['evaluation_record_key'])
    for method,m in x['methods'].items():
        methods_total[method]+=1;idx=m['retrieved_indices'];pred=m['predictions'];reason=m['reasons']
        if len(idx)!=3 or len(set(idx))!=3 or any(not 0<=j<48 for j in idx):fail('retrieved_indices',idx)
        if len(pred)!=3 or any(s not in (*STAT,'ABSTAIN') for s in pred):fail('predictions',pred)
        rel=[j in true for j in idx];correct=[r and p==STAT[j%3] for r,p,j in zip(rel,pred,idx)]
        family='binding' if method=='binding_mod_angle' else 'real_AB' if method=='real_AB_angle' else 'full'
        fitted=centres[c['seed'],c['mode'],c['cal_ratio'],c['cal_noise'],family]
        avail=all(d['centre'] is not None for d in fitted['diagnostics'])
        for p,rs in zip(pred,reason):
            reasons_total[rs or 'decoded']+=1
            if (p=='ABSTAIN')!=(rs in ('calibration_unavailable','zero_product','ambiguous_centre')):fail('reason_prediction',{'pred':p,'reason':rs})
            if not avail and rs!='calibration_unavailable':fail('missing_centre_reason',rs)
        oracle=m['oracle_relevant_diagnostic']
        if oracle['indices']!=list(range(3*scope,3*scope+3)):fail('oracle_indices',oracle['indices'])
        v={'evidence_recall':sum(rel)/3,'evidence_complete':set(idx)==true,'joint_label_recall':sum(correct)/3,
           'joint_complete':set(idx)==true and all(correct),'wrong_scope_count':sum(not r for r in rel),
           'abstain_count':sum(p=='ABSTAIN' for p in pred),'encoded_U_recall':int(any(j==3*scope+2 and p=='U' for j,p in zip(idx,pred))),
           'A_reference_agreement_at_1':idx[0]==3*scope,'decoded_A_at_1_if_relevant':pred[0]=='A' if rel[0] else None,
           'top1_relevant':rel[0],'top1_source_A':idx[0]%3==0 if rel[0] else None,
           'oracle_relevant_stance_accuracy':sum(p==s for p,s in zip(oracle['predictions'],STAT))/3,
           'decoder_calibration_available':avail}
        for rs in ('calibration_unavailable','zero_product','ambiguous_centre'):v['abstain_'+rs+'_count']=sum(r==rs for r in reason)
        if m['relevant']!=rel:fail('stored_relevance',x['evaluation_record_key'])
        if set(v)!=set(m['metrics']):fail('metric_fields',list(set(v)^set(m['metrics'])))
        for k,val in v.items():
            if not same(val,m['metrics'].get(k)):fail('metric_value',{'record':x['evaluation_record_key'],'method':method,'metric':k,'expected':val,'stored':m['metrics'].get(k)})
        key=tuple(c[k] for k in ('seed','mode','cal_ratio','eval_ratio','cal_noise','eval_noise'))+(method,)
        a=accum.setdefault(key,{'n':0,'sums':Counter(),'denominators':Counter()});a['n']+=1
        for k,val in v.items():
            if val is not None:a['sums'][k]+=val;a['denominators'][k]+=1

full=json.loads((R/'aggregates_full_condition.json').read_text())
for a in full:
    c=a['condition'];key=tuple(c[k] for k in ('seed','mode','cal_ratio','eval_ratio','cal_noise','eval_noise'))+(a['method'],);expected=accum.pop(key,None)
    if expected is None:fail('unexpected_aggregate',key);continue
    if expected['n']!=a['n']:fail('aggregate_n',key)
    for field in ('sums','denominators'):
        if set(expected[field])!=set(a[field]):fail('aggregate_fields',{'key':key,'field':field})
        for k,val in expected[field].items():
            if not same(val,a[field].get(k)):fail('aggregate_value',{'key':key,'field':field,'metric':k,'expected':val,'stored':a[field].get(k)})
    for k,val in expected['sums'].items():
        if not same(val/expected['denominators'][k],a['means'].get(k)):fail('aggregate_mean',{'key':key,'metric':k})
if accum:fail('missing_aggregates',len(accum))
controls=json.loads((R/'numerical_controls.json').read_text())
checks={'ledger_rows_10368':rows==10368,'method_records_41472':sum(methods_total.values())==41472,'full_condition_aggregates_1296':len(full)==1296,
        'unique_record_keys':len(keys)==rows,'all_stored_metrics_and_aggregates_recomputed':not discrepancies,
        'all_norm_and_algebra_discrepancies_within_declared_tolerance':all(v<=1e-10 for k,v in controls.items() if k.startswith('max_') and k.endswith('_error')),
        'cal_eval_entity_overlap_zero':controls['calibration_evaluation_entity_overlap']==0,'runtime_under180':controls['runtime_cap_passed']}
out={'scope':'every ledger metric and full-condition aggregate reconstructed from stored returned IDs/predictions, not matrix replay or independent empirical replication',
 'run':str(R),'checks':checks,'ledger_rows':rows,'method_records':dict(methods_total),'aggregate_rows':len(full),'reason_totals_across_methods':dict(reasons_total),
 'query_id_count':len(qids),'query_id_use_histogram':dict(Counter(qids.values())),'raw_query_hash_count':len(qhashes),'discrepancies':discrepancies,
 'numerical_controls':controls,'audit_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'LEDGER_AUDIT.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps({'checks':checks,'rows':rows,'method_records':sum(methods_total.values()),'discrepancies':discrepancies},indent=2))
assert all(checks.values())
