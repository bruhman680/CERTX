"""Prespecified full-cohort check, derived source bindings, arm and paired scoring."""
from pathlib import Path
from collections import Counter
import json,hashlib,sys
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
from evidence_threshold import load_json
from stored_run_audit import evaluate
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x') as f:f.write(json.dumps(v,indent=2)+'\n')
assert not (P/'SUMMARY.json').exists(),'No silent rescoring'
for name,v in load_json((P/'FREEZE.json').read_bytes())['sha256'].items():assert h(P/name)==v,name
for name,v in load_json((P/'RAW_FREEZE.json').read_bytes())['sha256'].items():assert h(P/name)==v,name
lines=(P/'RAW_OUTPUTS.jsonl').read_text().splitlines(keepends=True)
rows=[load_json(l) for l in lines]
cases=load_json((P/'CASES.json').read_bytes());keys=load_json((P/'KEYS.json').read_bytes())
expected=[c['id'] for c in cases]
assert len(rows)==len(expected)==24 and len({r['run_id'] for r in rows})==24
assert [r['run_id'] for r in rows]==expected
assert len(keys)==24 and {k['id'] for k in keys}==set(expected)
byid={k['id']:k['expected'] for k in keys}
outputs={r['run_id']:r for r in rows}
summary={'scope':'single paired deterministic authored pilot, not independent sampling/general efficacy','arms':{},'paired':[]}
for arm in ('ordinary','compact'):
    folder=P/arm;folder.mkdir(exist_ok=False)
    ids=[c['id'] for c in cases if c['arm']==arm]
    with (folder/'RAW_SUBSET.jsonl').open('x') as f:
        f.writelines(line for line,row in zip(lines,rows) if row['run_id'] in ids)
    dump(folder/'KEY_SUBSET.json',[k for k in keys if k['id'] in ids])
    contract={'claim_id':'BGP1-'+arm,'identity':{'family':'balanced_conditional_variance','facet':'candidate_answer','cycle':'BGP1','arm':arm},'expected_run_ids':ids,'parser':'strip_upper_exact_label_v1','raw':{'path':'RAW_SUBSET.jsonl','sha256':h(folder/'RAW_SUBSET.jsonl')},'keys':{'path':'KEY_SUBSET.json','sha256':h(folder/'KEY_SUBSET.json')}}
    dump(folder/'contract.json',contract)
    receipt=evaluate(contract,folder);assert receipt['status']=='computed',receipt
    dump(folder/'RECEIPT.json',receipt)
    chosen=[outputs[id] for id in ids];s=receipt['summary']
    s['by_expected_label']={label:{'n':sum(byid[id]==label for id in ids),'matches':sum(outputs[id]['text'].strip().upper()==label for id in ids if byid[id]==label)} for label in ('YES','NO','WITHHOLD')}
    s['constant_label_baselines']={label:sum(byid[id]==label for id in ids) for label in ('YES','NO','WITHHOLD')}
    s['inference_seconds_excluding_serialization']=sum(x['inference_seconds_excluding_serialization'] for x in chosen)
    s['serialization_seconds']=sum(x['serialization_seconds'] for x in chosen)
    s['new_cache_bytes']=sum(x['cache_artifact']['bytes'] for x in chosen)
    summary['arms'][arm]=s
    dump(folder/'DERIVATION.json',{'parent_raw_sha256':h(P/'RAW_OUTPUTS.jsonl'),'parent_keys_sha256':h(P/'KEYS.json'),'run_ids':ids,'recipe':'Exact source lines selected by predeclared arm IDs after checking all24 ordered IDs; no output-based filtering.'})
for c in cases:
    if c['arm']!='ordinary':continue
    a=outputs[c['id']];b=outputs[c['record_id']+'_compact'];key=byid[c['id']]
    summary['paired'].append({'record_id':c['record_id'],'expected':key,'ordinary':a['text'],'compact':b['text'],'ordinary_match':a['text'].strip().upper()==key,'compact_match':b['text'].strip().upper()==key})
summary['paired_changes']=dict(Counter('both_match' if x['ordinary_match'] and x['compact_match'] else 'compact_only' if x['compact_match'] else 'ordinary_only' if x['ordinary_match'] else 'neither_matches' for x in summary['paired']))
dump(P/'SUMMARY.json',summary)
print(json.dumps(summary,indent=2))
