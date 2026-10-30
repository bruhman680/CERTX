"""Frozen scoring: no model invocation, no posthoc extraction or row removal."""
from pathlib import Path
import sys,json,hashlib
from collections import Counter
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
from evidence_threshold import load_json
from stored_run_audit import evaluate
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def dump(p,x):
 with p.open('x') as f:f.write(json.dumps(x,indent=2)+'\n')
for freeze in ('FREEZE.json','RAW_FREEZE.json'):
 for name,v in load_json((P/freeze).read_bytes())['sha256'].items():assert h(P/name)==v,name
lines=(P/'RAW_OUTPUTS.jsonl').read_text().splitlines(keepends=True);rows=[load_json(l) for l in lines]
cases=load_json((P/'EVAL_CASES.json').read_bytes());keys=load_json((P/'KEYS.json').read_bytes())
assert len(cases)==len(keys)==60 and {c['id'] for c in cases}=={k['id'] for k in keys}
keymap={k['id']:k for k in keys}
armorder=['original_dev','adapted_dev','adapted_test','original_test']
expected=[c['id']+'__'+a for a in armorder for c in cases if c['split']==a.split('_')[1]]
assert len(rows)==len(expected)==len({r['run_id'] for r in rows})==120
assert [r['run_id'] for r in rows]==expected
summary={'scope':'single-seed authored narrow fine-tuning pilot; original vs separate adapted checkpoint','arms':{}}
for arm in armorder:
 chosen=[c for c in cases if c['split']==arm.split('_')[1]];ids=[c['id']+'__'+arm for c in chosen]
 folder=P/arm;folder.mkdir(exist_ok=False)
 (folder/'RAW_SUBSET.jsonl').write_text(''.join(line for line,row in zip(lines,rows) if row['run_id'] in ids))
 dump(folder/'KEY_SUBSET.json',[{'id':c['id']+'__'+arm,'expected':keymap[c['id']]['expected']} for c in chosen])
 contract={'claim_id':'NT1-'+arm,'identity':{'family':'narrow_source_state','facet':'state_label','cycle':'NT1','arm':arm},'expected_run_ids':ids,'parser':'strip_upper_exact_label_v1','raw':{'path':'RAW_SUBSET.jsonl','sha256':h(folder/'RAW_SUBSET.jsonl')},'keys':{'path':'KEY_SUBSET.json','sha256':h(folder/'KEY_SUBSET.json')}}
 dump(folder/'contract.json',contract);receipt=evaluate(contract,folder);assert receipt['status']=='computed',receipt
 dump(folder/'RECEIPT.json',receipt);out=receipt['summary'];rs=[r for r in rows if r['run_id'] in ids]
 labels={r['record_id']:(r['text'].strip().upper() if r['text'].strip().upper() in ('YES','NO','WITHHOLD') else 'UNRESOLVED') for r in rs}
 out['perclass']={label:{'n':sum(keymap[c['id']]['expected']==label for c in chosen),'matches':sum(labels[c['id']]==label for c in chosen if keymap[c['id']]['expected']==label)} for label in ('YES','NO','WITHHOLD')}
 out['confusion']={label:dict(Counter(labels[c['id']] for c in chosen if keymap[c['id']]['expected']==label)) for label in ('YES','NO','WITHHOLD')}
 out['by_family']={family:{'n':sum(c['structure_family']==family for c in chosen),'matches':sum(labels[c['id']]==keymap[c['id']]['expected'] for c in chosen if c['structure_family']==family)} for family in sorted({c['structure_family'] for c in chosen})}
 out['constant_label_baselines']={label:sum(keymap[c['id']]['expected']==label for c in chosen) for label in ('YES','NO','WITHHOLD')}
 out['inference_seconds_excluding_serialization']=sum(r['inference_seconds_excluding_serialization'] for r in rs)
 out['new_cache_bytes']=sum(r['cache_artifact']['bytes'] for r in rs)
 summary['arms'][arm]=out
 dump(folder/'DERIVATION.json',{'raw_parent_sha256':h(P/'RAW_OUTPUTS.jsonl'),'key_parent_sha256':h(P/'KEYS.json'),'ids':ids,'recipe':'Predeclared split/arm selects exact raw lines; key IDs gain arm suffix. All120IDs checked before views; no correctness filtering.'})
summary['test_pairs']=[]
outputs={r['run_id']:r['text'].strip().upper() for r in rows}
for c in cases:
 if c['split']!='test':continue
 key=keymap[c['id']]['expected'];a=outputs[c['id']+'__original_test'];b=outputs[c['id']+'__adapted_test']
 summary['test_pairs'].append({'id':c['id'],'expected':key,'original':a,'adapted':b,'original_match':a==key,'adapted_match':b==key})
summary['paired_changes']=dict(Counter('both_match' if r['original_match'] and r['adapted_match'] else 'adapted_only' if r['adapted_match'] else 'original_only' if r['original_match'] else 'neither_matches' for r in summary['test_pairs']))
dump(P/'SUMMARY.json',summary)
print(json.dumps({'arms':summary['arms'],'paired_changes':summary['paired_changes']},indent=2))
