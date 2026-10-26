#!/usr/bin/env python3
"""Independent ledger reconstruction. Imports no experiment code."""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
RUN=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'run'
STATUS=('A','N','U')
errors=[]
def check(condition,message):
    if not condition: errors.append(message)
def load(name): return json.loads((RUN/name).read_text())
def canonical(row): return tuple(row[k] for k in ('seed','Q','r','eval_eta','train_eta','m','method'))
ledger=[json.loads(x) for x in (RUN/'LEDGER.jsonl').read_text().splitlines()]
paired=[json.loads(x) for x in (RUN/'PAIRED_ROWS.jsonl').read_text().splitlines()]
agg={}; indexed={}; reasons=collections.Counter()
for n,row in enumerate(ledger):
    ids=row['returned_indices']; pred=row['predictions']; reason=row['reasons']; claim=row['claim']
    check(len(ids)==3 and len(set(ids))==3 and all(0<=i<48 for i in ids),f'invalid returned IDs {n}')
    check(row['query_index']//2==claim and row['query_index']%2==row['repetition'],f'claim/repetition {n}')
    check(row['returned_record_ids']==[f'eval-e{i//6}-t{(i//3)%2}-{STATUS[i%3]}' for i in ids],f'text IDs {n}')
    rel=[i//3==claim for i in ids]; good=[r and p==STATUS[i%3] for i,p,r in zip(ids,pred,rel)]
    wanted={'evidence_recall':sum(rel)/3,'evidence_complete':int(all(rel)),'joint_label_recall':sum(good)/3,'joint_complete':int(all(good)),'wrong_scope_count':sum(not x for x in rel),'encoded_U_recall':int(any(i==3*claim+2 and p=='U' for i,p in zip(ids,pred))),'abstain_count':pred.count('ABSTAIN'),'abstain_calibration_unavailable':reason.count('calibration_unavailable'),'abstain_ambiguous_centre':reason.count('ambiguous_centre'),'abstain_zero_product':reason.count('zero_product'),'oracle_relevant_stance_accuracy':sum(x==y for x,y in zip(row['oracle_relevant_predictions'],STATUS))/3}
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
check(len(saved)==len(agg)==864,'aggregate count')
for a in saved:
    k=canonical(a['condition']); actual=agg[k]
    check(a['count']==actual['count']==32,f'aggregate count {k}')
    check(a['metric_sums']==actual['sums'],f'aggregate sums {k}')
    check(a['metric_means']=={x:y/actual['count'] for x,y in actual['sums'].items()},f'aggregate means {k}')
linked=set()
for n,p in enumerate(paired):
    check(set(p['method_record_indices'])=={'full','naive','oracle','estimated'},f'paired methods {n}')
    for method,i in p['method_record_indices'].items():
        linked.add(i); r=ledger[i]
        check(r['method']==method and all(p[k]==r[k] for k in ('seed','Q','r','eval_eta','train_eta','m','query_id')),f'paired linkage {n}')
check(len(paired)==6912 and len(ledger)==27648 and linked==set(range(27648)),'complete paired links')
for item in load('INVARIANCE.json'):
    keys=[(item['seed'],q,item['r'],item['eval_eta'],item['train_eta'],item['m'],item['method']) for q in ('identity',item['Q'])]
    a,b=[[indexed[k+(j,)] for j in range(32)] for k in keys]
    sets=[j for j in range(32) if set(a[j]['returned_indices'])!=set(b[j]['returned_indices'])]
    order=[j for j in range(32) if a[j]['returned_indices']!=b[j]['returned_indices']]
    metrics=[j for j in range(32) if a[j]['metrics']!=b[j]['metrics']]
    near=[j for j in range(32) if b[j]['boundary_gap']<=1e-10]
    check(item['top3_set_mismatch_queries']==sets,'invariance sets')
    check(item['top3_order_mismatch_queries']==order,'invariance order')
    check(item['metric_mismatch_queries']==metrics,'invariance metrics')
    check(item['near_boundary_queries']==near,'invariance near ties')
    check(item['set_mismatch_boundary_gaps']==[b[j]['boundary_gap'] for j in sets],'invariance gaps')
# Nonestimated arms must repeat unchanged across all six training conditions.
duplicate_checks=0
for key,row in indexed.items():
    seed,q,r,e,t,m,method,j=key
    if method=='estimated': continue
    base=indexed[(seed,q,r,e,0.,4,method,j)]
    for field in ('returned_indices','predictions','reasons','scores','metrics','oracle_relevant_predictions'):
        check(row[field]==base[field],f'duplicate control {key} {field}')
    duplicate_checks+=1
manifest=load('QUERY_MANIFEST.json'); summary=load('SUMMARY.json')
check(len(manifest)==384 and len({x['query_id'] for x in manifest})==384,'query IDs')
check(summary['unique_query_array_hashes']==len({x['array_sha256'] for x in manifest}),'unique query hash count')
check(summary['base_query_ids']==len(manifest),'query count summary')
check(len({(r['seed'],r['claim']) for r in ledger})==48,'latent claims')
check(set(collections.Counter(r['query_id'] for r in ledger).values())=={72},'reuse count')
frozen=load('OUTPUT_HASHES.json')
for name,sha in frozen.items(): check(hashlib.sha256((RUN/name).read_bytes()).hexdigest()==sha,f'output hash {name}')
result={'status':'PASS' if not errors else 'FAIL','method_records_reconstructed':len(ledger),'paired_rows_checked':len(paired),'condition_aggregates_reconstructed':len(agg),'invariance_records_checked':len(load('INVARIANCE.json')),'repeated_control_records_checked':duplicate_checks,'actual_unique_base_query_hashes':len({x['array_sha256'] for x in manifest}),'returned_reason_counts':dict(reasons),'discrepancy_count':len(errors),'errors':errors[:100],'scope_limit':'Stored full-item prediction mismatch counts require saved-array replay; ledger audit verifies returned IDs, returned/oracle-relevant predictions, all metrics/aggregates, paired links, repeated controls and task invariance.'}
(ROOT/'review/LEDGER_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if errors: raise SystemExit(1)
