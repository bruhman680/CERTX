"""Independent artifact consistency checks; no inference, no world mutation."""
from pathlib import Path
import sys,json,hashlib,copy
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'observability-three-contact-v1'))
import common as c
r=c.read(H/'RESULTS.json');jobs=[c.read(p) for p in sorted((H/'jobs').glob('*.json'))]
checks={'actual_replies_14':len(r['rows'])==14,'main_inventory_unchanged':c.inventory()==c.read(H/'CANONICAL_BEFORE.json'),'no_unresolved_pending':not (H/'PENDING.json').exists(),'jobs_10':len(jobs)==10}
calls=[];tok=c.tokenizer()
for j in jobs:
    m=copy.deepcopy(j['messages'])
    if not j['case_id'].startswith('provided_'):
        assert all(v not in json.dumps(m) for v in ['K7M4Q9','R2V8T6'])
    for turn in range(1,j['max_turns']+1):
        name=j['case_id']+f'_t{turn}'
        raw=c.read(H/'results'/(name+'_raw.json'));b=c.read(H/'results'/(name+'_batch.json'));row=c.read(H/'results'/(name+'_result.json'))
        assert raw['messages']==m and b['raw_text']==raw['text']
        assert tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']
        assert row==next(x for x in r['rows'] if x['case']==name)
        assert row['text_sha256']==hashlib.sha256(raw['text'].encode()).hexdigest()
        assert row['complete_cells']==b['parsed']['complete_executable_cells']
        ops=[x for x in b['operations'] if x['feedback'] is not None]
        calls.append({'case':name,'cells':[{'language':x['language'],'source':x['source']} for x in b['parsed']['cells'] if x['complete'] and x['executable']],'process_receipts':[{'channel':x['channel'],'feedback':x['feedback']} for x in ops]})
        m += [{'role':'assistant','content':raw['text']},{'role':'user','content':c.candidate.project_feedback(b)}]
    assert c.verify_store(Path(j['world_store']))['status']=='pass'
by={j['case_id']:j for j in jobs}
for prefix in ['inherited','fresh','control_stone','control_river']:
    checks[prefix+'_a_b_same_initial_messages']=by[prefix+'_a']['messages']==by[prefix+'_b']['messages']
for suffix in ['a','b']:
    checks[suffix+'_same_prepared_world_all_hidden']=len({j['prepared_world_id'] for j in jobs if j['case_id'].endswith('_'+suffix)})==1
checks['all_checks_pass']=all(checks.values())
c.save(H/'AUDIT.json',{'checks':checks,'canonical_files_checked':len(c.inventory()),'call_details':calls,'no_model_calls':True,'recovered_known_first_result_without_replay':c.read(H/'RECORDER_RECOVERY.json')['actions_replayed']==0})
assert checks['all_checks_pass'],checks
print(json.dumps(checks))
