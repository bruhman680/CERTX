"""Supplemental effect/readout audit, never delivered to model input."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
if __name__=='__main__':
    rows=[]
    for j in read(H/'JOBS.json'):
        name=j['name'];r=read(H/'records'/(name+'.json'));b=read(H/'batches'/(name+'.json'));store=Path(j['world_store'])
        assert read(store/'bundles/000000.json')['id']==j['before_id']==b['operations'][0]['before_id']
        assert b['operations'][-1]['after_id']==r['after_id']
        state=read(store/'STATE.json');snapshot=read(H/'snapshots'/(name+'.json'))
        assert snapshot==read(store/'bundles'/state['bundle']) and snapshot['id']==r['after_id']
        actions=[{k:op[k] for k in ('channel','feedback','changed_paths','source')} for op in b['operations'] if op['channel'] in ('python','shell')]
        assert actions==r['actions'] and r['complete_cells']==b['parsed']['complete_executable_cells']
        stdout=[(op['feedback'] or {}).get('stdout','') for op in actions]
        assert r['target_in_stdout']==any(j['expected_value'] in s for s in stdout)
        assert r['exact_value_stdout']==any(s.strip()==j['expected_value'] for s in stdout)
        assert j['expected_value'] not in json.dumps(j['messages'])
        notes=[op for op in b['operations'] if op['channel']=='note'];assert len(notes)==1 and notes[0]['receipt']['exit_code']==0 and b['note_stored'] and b['note_storage_fault'] is None
        rows.append({'name':name,'input_tokens':r['input_tokens'],'output_tokens':r['output_tokens'],'complete_cells':r['complete_cells'],
                     'actual_action_errors':[a['feedback']['stderr'].splitlines()[-1] for a in actions if a['feedback']['exit_code']!=0 and a['feedback']['stderr']],
                     'target_in_stdout':r['target_in_stdout'],'historical_control_output_equal':r['prior_control_output_equal']})
    a=read(H/'raw/parser_native.json');b=read(H/'raw/parser_alias.json')
    result={'status':'pass','actual_model_calls':4,'actual_model_program_executions':sum(x['complete_cells'] for x in rows),'automatic_note_appends':4,
            'target_successes':sum(x['target_in_stdout'] for x in rows),'conditional_changed_nonce_checks_triggered':any(x['target_in_stdout'] for x in rows),
            'parser_native_alias_output_ids_equal':a['generated_token_ids']==b['generated_token_ids'],'rows':rows,
            'scope':'one-step repair after authentic error, two source failures; no durable learning or broad capability estimate'}
    with (H/'READOUT.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result))
