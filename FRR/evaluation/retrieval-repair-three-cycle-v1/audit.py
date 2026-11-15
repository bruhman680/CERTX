"""Artifact-only repair comparison audit. No model or sandbox actions."""
from pathlib import Path
import sys,json,base64
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'observability-three-contact-v1'))
import common as c
tok=c.tokenizer();result=c.read(H/'RESULTS.json');details=[]
assert result['model_replies']==6 and result['extra_artifact_executions']==6
for p in sorted((H/'jobs').glob('*.json')):
    j=c.read(p);name=j['case_id'];source=c.read(E/'retrieval-task-transfer-v1/jobs'/(j['source_case']+'.json'))
    priorraw=c.read(E/'retrieval-task-transfer-v1/results'/(j['source_case']+'_t1_raw.json'))
    priorbatch=c.read(E/'retrieval-task-transfer-v1/results'/(j['source_case']+'_t1_batch.json'))
    actual=c.candidate.project_feedback(priorbatch)
    assert j['actual_feedback']==actual
    assert j['messages'][:-2]==source['messages'] and j['messages'][-2]=={'role':'assistant','content':priorraw['text']}
    if j['condition']=='feedback':assert j['messages'][-1]['content']==actual
    else:
        supplied=json.loads(j['messages'][-1]['content']);correction=supplied.pop('operator_correction')
        assert correction=={'actor':'operator','text':j['operator_correction']}
        assert supplied==(json.loads(actual) if actual else {})
    raw=c.read(H/'results'/(name+'_t1_raw.json'));batch=c.read(H/'results'/(name+'_t1_batch.json'));transfer=c.read(H/'artifacts'/(name+'_batch.json'))
    assert raw['messages']==j['messages']
    assert tok.apply_chat_template(raw['messages'],tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
    assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==batch['raw_text']==transfer['raw_text']
    assert all(v not in json.dumps(raw['messages']) for v in ['N4C8P2','H9D3L7'])
    pa=c.read(Path(j['world_store'])/'bundles/000001.json');pb=c.read(Path(j['artifact_store'])/'bundles/000001.json')
    assert pa['id']==j['prepared_world_id'] and pb['id']==j['artifact_prepared_id']
    a={x[0]:x for x in pa['entries']};b={x[0]:x for x in pb['entries']}
    assert set(a)==set(b)
    differences=[key for key in a if a[key]!=b[key]]
    assert differences==[source['filename']]
    for store in [Path(j['world_store']),Path(j['artifact_store'])]:assert c.verify_store(store)['status']=='pass'
    for bt in [batch,transfer]:
        assert bt['parsed']==c.parse_notebook(raw['text'])
    ops=[x for x in batch['operations'] if x['feedback'] is not None]
    details.append({'case':name,'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],'complete_cells':batch['parsed']['complete_executable_cells'],'receipts':[x['feedback'] for x in ops],'model_changed_paths':[x['changed_paths'] for x in batch['operations']],'paired_start_differences':differences})
assert c.inventory()==c.read(H/'CANONICAL_BEFORE.json')
assert not any(H.rglob('*PENDING.json'))
c.save(H/'AUDIT.json',{'status':'pass','model_replies':6,'extra_artifact_executions':6,'details':details,'original_main_files_unchanged':len(c.inventory()),'diagnostic_activation':False,'pending':False})
print({'status':'pass','model_replies':6,'artifact_executions':6})
