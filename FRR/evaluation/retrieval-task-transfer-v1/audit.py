"""Recompute context and fixture/effect consistency without inference or actions."""
from pathlib import Path
import sys,json,base64
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'observability-three-contact-v1'))
import common as c
tok=c.tokenizer();results=c.read(H/'RESULTS.json');checks=[];details=[]
assert results['model_replies']==8 and results['extra_artifact_executions']==8
for p in sorted((H/'jobs').glob('*.json')):
    j=c.read(p);name=j['case_id'];raw=c.read(H/'results'/(name+'_t1_raw.json'));batch=c.read(H/'results'/(name+'_t1_batch.json'))
    assert raw['messages']==j['messages']
    assert all(v not in json.dumps(raw['messages']) for v in ['N4C8P2','H9D3L7'])
    assert tok.apply_chat_template(raw['messages'],tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
    assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==batch['raw_text']
    pair={}
    for suffix in ['a','b']:
        store=Path(j['pair'][suffix]['store']);bundle=c.read(store/'bundles/000001.json')
        assert bundle['id']==j['pair'][suffix]['id']
        pair[suffix]={e[0]:e for e in bundle['entries']}
        target=pair[suffix][j['filename']];data=json.loads(base64.b64decode(c.read(store/'objects'/(target[3]+'.json'))['base64']))
        assert data=={j['key']:('N4C8P2' if suffix=='a' else 'H9D3L7')}
        if j['filename']!='probe_value.json':assert 'probe_value.json' not in pair[suffix]
        assert c.verify_store(store)['status']=='pass'
    differences=[k for k in pair['a'] if pair['a'][k]!=pair['b'][k]]
    assert set(pair['a'])==set(pair['b']) and differences==[j['filename']]
    transfer=c.read(H/'transfers'/(name+'_batch.json'));assert transfer['raw_text']==raw['text']
    for b in [batch,transfer]:
        assert b['parsed']==c.parse_notebook(raw['text'])
        for op in b['operations']:
            assert not (set(op['changed_paths'])-{'notebook.txt'}),'Unexpected program writes; inspect before retrieval attribution'
    ops=[x for x in batch['operations'] if x['feedback'] is not None]
    details.append({'case':name,'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],'complete_cells':batch['parsed']['complete_executable_cells'],'target_literal_in_generated_text':any(v in raw['text'] for v in ['N4C8P2','H9D3L7']),'receipts':[x['feedback'] for x in ops],'paired_fixture_differences':differences})
assert c.inventory()==c.read(H/'CANONICAL_BEFORE.json')
assert not any(H.rglob('*PENDING.json'))
proposal=c.read(H/'main50-proposal/EXACT_NEXT_VIEW.json')
assert proposal==c.select_view(c.read(c.C/'run/INITIAL_MESSAGES.json'),[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in c.candidate.rows(c.C/'run')],tok,max_pairs=8,max_input=7936)
c.save(H/'AUDIT.json',{'status':'pass','cases':details,'model_replies':8,'extra_artifact_executions':8,'main_files_unchanged':len(c.inventory()),'main_entry':c.read(c.C/'run/STATE.json')['human_entry'],'pending':False,'proposal_only_no_main_calls':True})
print({'status':'pass','cases':len(details),'main_entry':1580,'main_files':len(c.inventory())})
