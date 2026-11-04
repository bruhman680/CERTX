"""Read-only verification of this historical continuation; no model calls or pointer writes."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mutable={'evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl','evaluation/source-access-three-cycle-v1/cycle3/environment/STATE.json','evaluation/source-access-three-cycle-v1/cycle3/CURRENT_VERIFY.json'}
for p,h in json.loads((R/'PRIMARY_BEFORE.json').read_text()).items():
 if p not in mutable:assert sha(ROOT/p)==h,p
for p,h in json.loads((R/'FREEZE.json').read_text())['files'].items():assert sha(ROOT/p)==h,p
old=(R/'before/evaluation/source-access-three-cycle-v1/cycle3/environment/NOTEBOOK.jsonl').read_bytes();current=(E/'NOTEBOOK.jsonl').read_bytes();assert current.startswith(old)
rows=[json.loads((E/'events'/f'{i:06}.json').read_text()) for i in range(100,105)];s=json.loads((R/'SUMMARY.json').read_text());assert s['calls']==len(rows)==5 and s['output_tokens']==sum(len(x['generated_token_ids']) for x in rows) and s['caps']==sum(x['stop']=='token_limit' for x in rows)
assert json.loads((G/'cycle3/verification/0013_CHECKS.json').read_text())['status']=='pass'
assert json.loads((E/'sessions/0012.json').read_text())['weights_unchanged']
assert all(x['task_score'] is None and x['environment_version']=='archive-view-v1' for x in rows)
print('Historical100to105records and prior immutable files verified read-only; no state writes.')
