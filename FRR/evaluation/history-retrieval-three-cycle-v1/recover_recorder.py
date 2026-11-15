"""Resolve saved, known effects after recorder error. Never generate or execute cells."""
import sys,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'observability-three-contact-v1'))
import common as c
assert c.read(H/'PENDING.json')['case']=='inherited_a_t1'
j=c.read(H/'jobs/inherited_a.json')
raw=c.read(H/'results/inherited_a_t1_raw.json');batch=c.read(H/'results/inherited_a_t1_batch.json')
state=c.read(Path(j['world_store'])/'STATE.json')
stdouts=[(op['feedback'] or {}).get('stdout','') for op in batch['operations']]
row={'case':'inherited_a_t1','input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),'complete_cells':batch['parsed']['complete_executable_cells'],'expected_value':j['expected_value'],'target_in_text':j['expected_value'] in raw['text'],'target_in_stdout':any(j['expected_value'] in s for s in stdouts),'exact_value_stdout':any(s.strip()==j['expected_value'] for s in stdouts),'stdout':stdouts,'before_id':j['prepared_world_id'],'after_id':c.read(Path(j['world_store'])/'bundles'/state['bundle'])['id'],'verification':c.verify_store(Path(j['world_store']))}
c.save(H/'results/inherited_a_t1_result.json',row)
c.save(H/'RECORDER_RECOVERY.json',{'error':'recorder treated notebook-only feedback None as dictionary','known_effects':'raw and batch saved; sandbox batch completed and store verified','generations_replayed':0,'actions_replayed':0,'pending_before':c.read(H/'PENDING.json'),'result':row})
assert c.inventory()==c.read(H/'CANONICAL_BEFORE.json')
(H/'PENDING.json').unlink()
print(json.dumps(row))
