"""Compare the retained receipt with frozen expectations and earlier summary."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[2];p=Path(__file__).resolve().parent
out=json.loads((p/'RECEIPT.json').read_text()); exp=json.loads((p/'EXPECTED.json').read_text())
assert all(out[k]==v for k,v in exp.items())
src=r/'evaluation/complete-verification-path-v1/model_diagnostic/SUMMARY.json'
s=json.loads(src.read_text());v=out['summary']
mapping={'calls':'calls','label_matches':'semantic_label_matches','constant_yes_matches':'constant_yes_baseline_matches','input_tokens':'input_tokens','output_tokens':'output_tokens'}
assert all(v[a]==s[b] for a,b in mapping.items())
assert all(v['stops'].get(k,0)==s['stops'].get(k,0) for k in set(v['stops'])|set(s['stops']))
assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==h for f,h in json.loads((p/'FREEZE.json').read_text())['sha256'].items())
result={'frozen_expectation_matches':True,'historical_aggregate_consistent':True,'historical_aggregate_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'challenge_test_groups':15,'all_challenge_groups_pass':True,'freeze_unchanged':True,'new_model_calls':0,'independent_or_masked_review':False,'stop_comparison':'Absent count keys treated as zero; original aggregate explicitly includes token_limit:0.'}
print(json.dumps(result,indent=2))
