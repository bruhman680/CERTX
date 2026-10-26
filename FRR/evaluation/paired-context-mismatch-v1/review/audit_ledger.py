#!/usr/bin/env python3
"""Independent ledger reconstruction. Imports no experiment code."""
import collections
import hashlib
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
RUN=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'run'
STATUS=('A','N','U')
errors=[]
def check(condition,message):
    if not condition: errors.append(message)
def load(name): return json.loads((RUN/name).read_text())
def canonical(row): return tuple(row[k] for k in ('seed','Q','r','eval_eta','arm','delta','kind','m','method'))
ledger=[json.loads(x) for x in (RUN/'LEDGER.jsonl').read_text().splitlines()]
paired=[json.loads(x) for x in (RUN/'PAIRED_ROWS.jsonl').read_text().splitlines()]
agg={}; indexed={}; reasons=collections.Counter()
for n,row in enumerate(ledger):
    ids=row['returned_indices']; pred=row['predictions']; reason=row['reasons']; claim=row['claim']
    check(len(ids)==3 and len(set(ids))==3 and all(0<=i<48 for i in ids),f'invalid returned IDs {n}')
    check(row['query_index']//2==claim and row['query_index']%2==row['repetition'],f'claim/repetition {n}')
    check(row['returned_record_ids']==[f'eval-e{i//6}-t{(i//3)%2}-{STATUS[i%3]}' for i in ids],f'text IDs {n}')
    rel=[i//3==claim for i in ids]; good=[r and p==STATUS[i%3] for i,p,r in zip(ids,pred,rel)]
    wanted={'evidence_count':sum(rel),'joint_label_count':sum(good),'evidence_recall':sum(rel)/3,'evidence_complete':int(all(rel)),'joint_label_recall':sum(good)/3,'joint_complete':int(all(good)),'wrong_scope_count':sum(not x for x in rel),'encoded_U_recall':int(any(i==3*claim+2 and p=='U' for i,p in zip(ids,pred))),'abstain_count':pred.count('ABSTAIN'),'abstain_calibration_unavailable':reason.count('calibration_unavailable'),'abstain_ambiguous_centre':reason.count('ambiguous_centre'),'abstain_zero_product':reason.count('zero_product'),'oracle_relevant_stance_accuracy':sum(x==y for x,y in zip(row['oracle_relevant_predictions'],STATUS))/3}
    check(row['metrics']==wanted,f'metrics {n}')
    check(sum(wanted[k] for k in ('abstain_calibration_unavailable','abstain_ambiguous_centre','abstain_zero_product'))==wanted['abstain_count'],f'abstain sum {n}')
    check(all((p=='ABSTAIN')==(r!='ok') for p,r in zip(pred,reason)),f'reason consistency {n}')
    check(row['near_boundary_tie']==(row['boundary_gap']<=1e-10),f'boundary flag {n}')
    reasons.update(reason)
    key=canonical(row)
    if key not in agg: agg[key]={'count':0,'sums':dict.fromkeys(wanted,0.)}
    agg[key]['count']+=1
    for k,v in wanted.items(): agg[key]['sums'][k]+=v
    index=key+(row['query_index'],)
    check(index not in indexed,f'duplicate index {n}'); indexed[index]=row
saved=load('AGGREGATES.json')
check(len(saved)==len(agg)==720,'aggregate count')
for a in saved:
    k=canonical(a['condition']); actual=agg[k]
    check(a['count']==actual['count']==32,f'aggregate count {k}')
    check(a['metric_sums'].keys()==actual['sums'].keys() and all(abs(a['metric_sums'][x]-v)<=1e-10 for x,v in actual['sums'].items()),f'aggregate sums {k}')
    check(a['metric_means'].keys()==actual['sums'].keys() and all(abs(a['metric_means'][x]-v/actual['count'])<=1e-10 for x,v in actual['sums'].items()),f'aggregate means {k}')
linked=set()
for n,p in enumerate(paired):
    check(set(p['method_record_indices'])=={'full','oracle','estimated'},f'paired methods {n}')
    for method,i in p['method_record_indices'].items():
        linked.add(i); r=ledger[i]
        check(r['method']==method and all(p[k]==r[k] for k in ('seed','Q','r','eval_eta','arm','delta','kind','m','query_id')),f'paired linkage {n}')
check(len(paired)==7680 and len(ledger)==23040 and linked==set(range(23040)),'complete paired links')
# Nonestimated arms must repeat unchanged across all 20 training conditions.
duplicate_checks=0
for key,row in indexed.items():
    seed,q,r,e,arm,delta,kind,m,method,j=key
    if method=='estimated': continue
    base=indexed[(seed,q,r,e,'CLEAN',0.,'clean',12,method,j)]
    for field in ('returned_indices','predictions','reasons','scores','metrics','oracle_relevant_predictions','oracle_relevant_reasons','boundary_gap','within_top3_score_differences'):
        check(row[field]==base[field],f'duplicate control {key} {field}')
    duplicate_checks+=1
repeated=load('REPEATED_CONTROL_CHECKS.json')
check(len(repeated)==456,'repeated control count')
for item in repeated:
    check(item['max_product_error']==0 and all(item[k] for k in ('labels_equal','reasons_equal','top_equal','metrics_equal')),'repeated control saved failure')
# Exhaustive predecessor comparisons reconstructed from old/new ledgers.
prior=ROOT.parent/'structural-access-three-cycle-v1/run/LEDGER.jsonl'
oldrows=[json.loads(x) for x in prior.read_text().splitlines()]
oldrows=[r for r in oldrows if r['Q']=='dense' and r['method'] in ('full','oracle')]
saved_prior=load('PREDECESSOR_CONTROL_CHECKS.json')
check(len(saved_prior)==len(oldrows)==4608,'predecessor comparison count')
for n,(old,item) in enumerate(zip(oldrows,saved_prior)):
    k=(old['seed'],'dense',old['r'],old['eval_eta'],'CLEAN',0.,'clean',12,old['method'],old['query_index'])
    new=indexed[k]
    diffs={x:new['metrics'][x]-v for x,v in old['metrics'].items() if new['metrics'][x]!=v}
    check(item['metric_differences']==diffs,f'prior metric differences {n}')
    for field,actual in (('top_order_equal',old['returned_indices']==new['returned_indices']),('top_set_equal',set(old['returned_indices'])==set(new['returned_indices'])),('returned_predictions_equal',old['predictions']==new['predictions']),('returned_reasons_equal',old['reasons']==new['reasons']),('oracle_relevant_predictions_equal',old['oracle_relevant_predictions']==new['oracle_relevant_predictions'])):
        check(item[field]==actual,f'prior {field} {n}')
manifest=load('QUERY_MANIFEST.json'); summary=load('SUMMARY.json')
check(len(manifest)==384 and len({x['query_id'] for x in manifest})==384,'query IDs')
check(summary['base_unique_query_arrays']==len({x['array_sha256'] for x in manifest}),'unique query hash count')
check(summary['base_query_ids']==len(manifest),'query count summary')
check(len({(r['seed'],r['claim']) for r in ledger})==48,'latent claims')
check(set(collections.Counter(r['query_id'] for r in ledger).values())=={60},'reuse count')
# Every stored reason checked against its method calibration availability.
centres=np.load(RUN/'structures_centres.npz',allow_pickle=False)
availability_counts=collections.Counter(); availability_cache={}
for n,row in enumerate(ledger):
    ck=row['outcome_key'].rsplit('_e',1)[0]
    if ck not in availability_cache:
        available=centres[ck+'_available']
        actual=np.abs(centres[ck+'_centres'])>1e-10
        check(np.array_equal(available,actual),f'center availability {ck}')
        availability_cache[ck]=bool(np.all(available))
    all_available=availability_cache[ck]
    availability_counts[(row['arm'],row['r'],row['method'],'available' if all_available else 'unavailable')]+=1
    all_reasons=row['reasons']+row['oracle_relevant_reasons']
    if not all_available:
        check(set(all_reasons)=={'calibration_unavailable'},f'unavailable priority {n}')
    else:
        check('calibration_unavailable' not in all_reasons,f'available reason {n}')
    # Source zero-noise repetitions must preserve all actual task readouts.
    if row['eval_eta']==0. and row['repetition']==1:
        k=canonical(row)+(row['query_index']-1,)
        peer=indexed[k]
        for field in ('returned_indices','predictions','reasons','scores','metrics','oracle_relevant_predictions'):
            check(row[field]==peer[field],f'zero-noise repetition {n} {field}')
centres.close()
check(len(availability_cache)==360,'calibration configuration count')
frozen=load('OUTPUT_HASHES.json')
for name,sha in frozen.items(): check(hashlib.sha256((RUN/name).read_bytes()).hexdigest()==sha,f'output hash {name}')
result={'aggregate_numeric_tolerance':1e-10,'audit_repair':'Initial exact aggregate comparison retained in audit_ledger.initial.py and LEDGER_AUDIT.initial.json; compensated Python sum differs from += by roundoff only. Experiment unchanged.','status':'PASS' if not errors else 'FAIL','method_records_reconstructed':len(ledger),'paired_rows_checked':len(paired),'condition_aggregates_reconstructed':len(agg),'predecessor_comparison_records_checked':len(saved_prior),'repeated_control_records_checked':duplicate_checks,'actual_unique_base_query_hashes':len({x['array_sha256'] for x in manifest}),'returned_reason_counts':dict(reasons),'calibration_availability_record_counts':{str(k):v for k,v in availability_counts.items()},'discrepancy_count':len(errors),'errors':errors[:100],'scope_limit':'Saved-array replay independently verifies numeric inference. This exhaustive ledger audit verifies stored returned IDs/predictions, all metrics/aggregates, paired links, reasons, repeated controls and predecessor comparison claims.'}
(ROOT/'review/LEDGER_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if errors: raise SystemExit(1)
