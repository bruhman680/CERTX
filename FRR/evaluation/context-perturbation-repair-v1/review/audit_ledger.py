#!/usr/bin/env python3
"""Independent exhaustive ledger audit; no experiment imports."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RUN = ROOT / 'run'

def read(name):
    return json.loads((RUN/name).read_text())

def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines()]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ledger = lines(RUN/'LEDGER.jsonl')
    pairs = lines(RUN/'PAIRED_ROWS.jsonl')
    aggregates = read('AGGREGATES.json')
    mapping = read('OUTCOME_MAP.json')
    source = np.load(RUN/'source_inputs.npz', allow_pickle=False)
    pool = np.load(RUN/'outcomes.npz', allow_pickle=False)
    cached = {}
    assert len(ledger) == 30720 and len(pairs) == 7680 and len(aggregates) == 960
    assert len(mapping['conditions']) == 960
    reasons = ('calibration_unavailable', 'ambiguous_centre', 'zero_product')
    statuses = np.array(['A', 'N', 'U'])
    bycondition, byquery = defaultdict(list), defaultdict(list)
    controls, unavailable, returned_reasons = {}, Counter(), Counter()
    prior = {}
    for row in lines(ROOT.parent/'paired-context-mismatch-v1/run/LEDGER.jsonl'):
        if row['method'] in ('full', 'oracle'):
            key = (row['query_id'], row['method'])
            value = {k: row[k] for k in ('returned_indices', 'predictions', 'reasons', 'oracle_relevant_predictions', 'oracle_relevant_reasons', 'metrics')}
            assert key not in prior or prior[key] == value
            prior[key] = value
    for number, row in enumerate(ledger):
        fields = {}
        for name,key in mapping['conditions'][row['outcome_key']].items():
            if key not in cached:
                cached[key] = pool[key]
            fields[name] = cached[key]
        j = row['query_index']
        assert 0 <= j < 32
        seed = row['seed']
        claim = int(source[f's{seed}_query_claim_index'][j])
        assert claim == row['claim']
        assert row['repetition'] == int(source[f's{seed}_query_repetition'][j])
        ri, ei = (0 if row['r'] == .5 else 1), (0 if row['eval_eta'] == 0 else 1)
        assert row['query_id'] == f'{seed}-r{ri}-e{ei}-q{j:02d}'
        ix = np.asarray(row['returned_indices'])
        assert len(set(ix)) == 3 and np.all((ix >= 0) & (ix < 48))
        assert np.array_equal(ix, fields['top'][j])
        order = np.argsort(-fields['scores'][j], kind='stable')
        assert np.array_equal(ix, order[:3])
        predictions = fields['labels'][j, ix]
        why = fields['reasons'][j, ix]
        assert predictions.tolist() == row['predictions'] and why.tolist() == row['reasons']
        assert row['returned_record_ids'] == [f'eval-e{x//6}-t{(x//3)%2}-{statuses[x%3]}' for x in ix]
        assert fields['products'][j, ix].real.tolist() == row['products_real']
        assert fields['products'][j, ix].imag.tolist() == row['products_imag']
        assert fields['scores'][j, ix].tolist() == row['scores']
        assert np.angle(fields['products'][j, ix]).tolist() == row['angles']
        relevant_predictions = fields['labels'][j, 3*claim:3*claim+3]
        assert relevant_predictions.tolist() == row['oracle_relevant_predictions']
        assert fields['reasons'][j, 3*claim:3*claim+3].tolist() == row['oracle_relevant_reasons']
        gap = float(fields['scores'][j, order[2]]-fields['scores'][j, order[3]])
        assert gap == row['boundary_gap'] and (gap <= 1e-10) == row['near_boundary_tie']
        assert np.diff(fields['scores'][j, ix]).tolist() == row['within_top3_score_differences']
        relevant = ix//3 == claim
        correct = relevant & (predictions == statuses[ix%3])
        evidence, joint = int(sum(relevant)), int(sum(correct))
        expected = dict(evidence_count=evidence, evidence_recall=evidence/3,
            evidence_complete=int(evidence==3), joint_label_count=joint,
            joint_label_recall=joint/3, joint_complete=int(joint==3), wrong_scope_count=3-evidence,
            encoded_U_recall=int(np.any(relevant & (ix%3==2) & (predictions=='U'))),
            abstain_count=int(sum(predictions=='ABSTAIN')),
            oracle_relevant_stance_accuracy=float(np.mean(relevant_predictions==statuses)))
        expected.update({'abstain_'+r: int(sum(why==r)) for r in reasons})
        assert row['metrics'] == expected, (number, row['metrics'], expected)
        assert expected['abstain_count'] == sum(expected['abstain_'+r] for r in reasons)
        flag = row['method']=='solved' and row['probe'] in ('COPY','GLOBAL_FLIP')
        assert row['unidentified_operator'] == flag
        assert row['solved_available'] == (not flag if row['method']=='solved' else None)
        assert row['solved_reason'] == (('unidentified_operator' if flag else 'ok') if row['method']=='solved' else None)
        unavailable[(row['method'], flag)] += 1
        returned_reasons.update(why.tolist())
        bycondition[row['outcome_key']].append(row)
        byquery[row['query_id']].append(number)
        if row['method'] in ('full','oracle'):
            key = (row['query_id'],row['method'])
            value = {k: row[k] for k in ('returned_indices','predictions','reasons','oracle_relevant_predictions','oracle_relevant_reasons','metrics')}
            assert key not in controls or controls[key] == value
            controls[key] = value
            assert prior[key] == value, ('predecessor control', key)
    assert len(byquery)==384 and set(map(len,byquery.values()))=={80}
    assert len(controls)==768
    max_aggregate_error=0.
    for aggregate in aggregates:
        rows = bycondition[aggregate['outcome_key']]
        assert len(rows)==32 and {x['query_index'] for x in rows}==set(range(32))
        for name in ('seed','delta','probe','m','r','eval_eta','method','Q','unidentified_operator','solved_available','solved_reason'):
            assert all(row[name]==aggregate[name] for row in rows)
        sums = {key:sum(row['metrics'][key] for row in rows) for key in rows[0]['metrics']}
        assert aggregate['count']==32 and set(aggregate['metric_sums'])==set(sums)
        for k,v in sums.items():
            error=abs(aggregate['metric_sums'][k]-v)
            mean_error=abs(aggregate['metric_means'][k]-v/32)
            max_aggregate_error=max(max_aggregate_error,error,mean_error)
            assert error<=1e-11 and mean_error<=1e-11
            if isinstance(v,int):
                assert error==0
    seen=set()
    for pair in pairs:
        indices=pair['method_record_indices']
        assert set(indices)=={'full','oracle','repaired','solved'}
        rows=[ledger[x] for x in indices.values()]
        assert all(x['query_id']==pair['query_id'] for x in rows)
        for name in ('seed','delta','probe','m','r','eval_eta','query_index'):
            assert len({x[name] for x in rows})==1
        assert set(indices.values()).isdisjoint(seen)
        seen.update(indices.values())
    assert seen==set(range(len(ledger)))
    manifest=read('QUERY_MANIFEST.json')
    ids=[]; hashes=[]
    for entry in manifest['queries']:
        seed, rtxt, etxt, qtxt=entry['query_id'].split('-')
        ri,ei,j=int(rtxt[1:]),int(etxt[1:]),int(qtxt[1:])
        query=source[f's{seed}_queries_r{ri}_e{ei}'][j]
        h=hashlib.sha256(np.ascontiguousarray(query).tobytes()).hexdigest()
        assert h==entry['array_sha256']
        assert entry['paired_reuses']==20 and entry['method_reuses']==80
        ids.append(entry['query_id']); hashes.append(h)
    assert len(ids)==len(set(ids))==384 and len(set(hashes))==288
    assert set(ids)==set(byquery)
    declared=read('PREDECESSOR_CONTROL_CHECKS.json')
    assert len(declared)==15360 and all(not x['differences'] for x in declared)
    repeated=read('REPEATED_CONTROL_CHECKS.json')
    assert len(repeated)==14592 and all(x['equal'] for x in repeated)
    result={'passed':True,'method_records':len(ledger),'paired_rows':len(pairs),
        'aggregate_conditions':len(aggregates),'query_ids':384,'unique_base_arrays':288,
        'per_query_method_uses':80,'predecessor_control_records':15360,
        'repeated_control_records':14592,'returned_reason_counts':dict(returned_reasons),
        'max_aggregate_arithmetic_error':max_aggregate_error,
        'unidentified_method_records':sum(v for (m,b),v in unavailable.items() if b),
        'source_inspection':'PROTOCOL,SCHEMA,experiment.py inspected prospectively; no implementation imports',
        'audit_sha256':digest(Path(__file__)),'ledger_sha256':digest(RUN/'LEDGER.jsonl')}
    (HERE/'LEDGER_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':
    main()
