"""Check supplemental contexts, outcomes and preserved main without new actions."""
import sys,json,copy
from pathlib import Path
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'observability-three-contact-v1'))
import common as c
tok=c.tokenizer();D=H/'format-followup';result=c.read(D/'RESULTS.json')
checks={'three_new_replies':result['actual_model_replies']==3,'main_unchanged':c.inventory()==c.read(H/'CANONICAL_BEFORE.json'),'no_pending':not any(H.rglob('PENDING.json')),'base_audit_pass':c.read(H/'AUDIT.json')['checks']['all_checks_pass']}
for p in sorted((D/'jobs').glob('*.json')):
    j=c.read(p);name=j['case_id']+'_t1'
    raw=c.read(D/'results'/(name+'_raw.json'));batch=c.read(D/'results'/(name+'_batch.json'))
    assert raw['messages']==j['messages']
    assert all(v not in json.dumps(j['messages']) for v in ['K7M4Q9','R2V8T6'])
    assert tok.apply_chat_template(raw['messages'],tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
    assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==batch['raw_text']
    assert c.verify_store(Path(j['world_store']))['status']=='pass'
transfer=c.read(H/'program-transfer/RESULTS.json')
checks['transfer_two_exact_generated_artifact_executions']=transfer['artifact_executions']==2 and transfer['same_generated_text']
for row in transfer['rows']:
    name=row['case'];j=c.read(H/'program-transfer/jobs'/(name+'.json'))
    batch=c.read(H/'program-transfer/results'/(name+'_batch.json'))
    assert batch['raw_text']==c.read(H/'results/provided_value_t1_raw.json')['text']
    assert row['expected_labeled_stdout']
    assert c.verify_store(Path(j['world_store']))['status']=='pass'
checks['all_checks_pass']=all(checks.values());assert checks['all_checks_pass']
c.save(H/'FOLLOWUP_AUDIT.json',{'checks':checks,'model_replies_total':17,'artifact_executions_extra':2,'main_files':len(c.inventory()),'main_entry':c.read(c.C/'run/STATE.json')['human_entry']})
print(json.dumps(checks))
