"""Recompute pilot evidence; no model calls or sandbox actions."""
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1'
sys.path.insert(0,str(E/'observability-three-contact-v1'))
import common as c

def main():
    assert not (H/'pilot/AUDIT.json').exists(),'Preserve prior audit'
    plan=c.read(H/'pilot/PLAN.json');result=c.read(H/'pilot/RESULTS.json');tok=c.tokenizer()
    assert c.inventory(M)==c.read(H/'pilot/MAIN_BEFORE.json') and c.inventory()==c.read(H/'pilot/SOURCE_BEFORE.json')
    assert all(c.sha(Path(p))==sha for p,sha in plan['pins'].items())
    assert c.read(M/'run/STATE.json')['human_entry']==1630 and c.read(M/'run/STATE.json')['paused']
    assert not list((H/'pilot').rglob('*PENDING.json'))
    prepared=c.read(H/'pilot/PREPARATION_CHECKS.json');assert prepared['same_prepared_world']
    initial_ids=set();summaries=[];total=0
    for arm in ['control','compact','full']:
        original=c.read(H/'pilot/inputs'/(arm+'.json'));messages=copy.deepcopy(original['messages']);last=None
        assert messages[1]=={'role':'user','content':(H/'interface/mechanics_user.txt').read_text()}
        expected_system='' if arm=='control' else (H/('frr/candidate.md' if arm=='compact' else 'frr/full_source_reference.md')).read_text()
        assert messages[0]=={'role':'system','content':expected_system}
        store=H/'pilot/branches'/arm/'world';initial=c.read(store/'bundles/000001.json');initial_ids.add(initial['id'])
        rows=[x for x in result['rows'] if x['arm']==arm];raws=[];batches=[]
        for turn,row in enumerate(rows,1):
            label=arm+f'_t{turn}';raw=c.read(H/'pilot/raw'/(label+'.json'));batch=c.read(H/'pilot/batches'/(label+'.json'));p=c.read(H/'pilot/plans'/(label+'.json'))
            assert raw['messages']==messages==p['messages']
            assert tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)==raw['input_token_ids']==p['input_token_ids']
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==row['text']==batch['raw_text']
            assert row['raw_sha256']==c.sha(H/'pilot/raw'/(label+'.json')) and row['batch_sha256']==c.sha(H/'pilot/batches'/(label+'.json'))
            assert p['parent_record_sha256']==row['parent_record_sha256']==last
            assert row['feedback']==c.candidate.project_feedback(batch)
            assert batch['parsed']==c.parse_notebook(raw['text'])
            assert c.read(H/'pilot/records'/(label+'.json'))==row
            assert row['model_initiated_actions']==[{'channel':x['channel'],'source':x['source'],'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations'] if x['channel'] in ['python','shell']]
            messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':row['feedback']}]
            last=c.sha(H/'pilot/records'/(label+'.json'));raws.append(raw);batches.append(batch);total+=1
        s=c.read(store.parent/'STATE.json');assert s['turn']==len(rows) and s['paused'] and s['last_record_sha256']==last
        assert c.verify_store(store)['status']=='pass'
        actions=[a for row in rows for a in row['model_initiated_actions']]
        error_turns=[row['turn'] for row in rows if any(a['feedback']['exit_code']!=0 or a['feedback']['boundary'] is not None for a in row['model_initiated_actions'])]
        opportunities=[turn for turn in error_turns if any(r['turn']>turn for r in rows)]
        summaries.append({'arm':arm,'actual_replies':len(rows),'input_tokens':[r['input_tokens'] for r in rows],'output_tokens':[r['output_tokens'] for r in rows],'stop':[r['stop'] for r in rows],
          'distinct_output_token_sequences':len({json.dumps(r['generated_token_ids']) for r in raws}),
          'complete_parsed_cells':sum(r['complete_cells'] for r in rows),'actual_model_initiated_actions':len(actions),
          'incomplete_fences':sum(r['incomplete_fences'] for r in rows),'known_action_error_turns':error_turns,'later_reply_after_error_turns':opportunities,
          'repair_opportunity':'not elicited' if not error_turns else ('present,interpret actual subsequent actions' if opportunities else 'no later reply within pilot'),
          'model_action_changed_paths':[a['changed_paths'] for a in actions],
          'automatic_note_count':sum(len(r['automatic_note_operations']) for r in rows),'nonempty_feedback':sum(bool(r['feedback']) for r in rows)})
    assert len(initial_ids)==1 and total==result['actual_model_calls']
    c.save(H/'pilot/AUDIT.json',{'status':'pass','actual_model_calls':total,'same_initial_world':True,'main_entry':1630,'main_unchanged':True,'source823files_unchanged':True,'no_new_training':True,'activation':False,'summaries':summaries})
    print(json.dumps(summaries))

if __name__=='__main__':main()
