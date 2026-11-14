"""Prepare prompted file-reading controls. No model inference."""
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H))
import common

R=H/'retrieval'
TASK='Use Python to read the value field in probe_value.json and print its exact value.'
CASES=[('retrieval_hidden_a','K7M4Q9',False),
       ('retrieval_hidden_b','R2V8T6',False),
       ('retrieval_provided_a','K7M4Q9',True)]

def main():
    before=common.inventory()
    tok=common.tokenizer();base=common.base_view(tok)
    common.save(R/'PLAN.json',{
       'date':'2026-11-13 America/Chicago','scope':'prompted retrieval diagnostic, not open emergence',
       'task':TASK,'cases':CASES,'base_input_tokens':len(base['input_token_ids']),
       'world_fixture':str(common.fixture_bundle()),'world_fixture_sha256':common.sha(common.fixture_bundle()),
       'model_inference':False,'canonical_changes':False,
       'hidden_control':'same messages and IDs; only actual file bytes differ',
       'provided_control':'same task plus authentic operator read receipt; longer input is a confound',
       'turn_budget':2,'second_turn':'only actual first-reply effects returned by central worker; no repeated task or hint'})
    jobs=[];controls=[];hidden_ids=[]
    for case_id,value,provided in CASES:
        store=R/'worlds'/case_id;store.parent.mkdir(parents=True,exist_ok=True)
        w,declaration=common.clone(store,before=False)
        try:
            common.save(R/'preparation'/f'{case_id}_declaration.json',{'actor':'operator','event':declaration})
            source="from pathlib import Path\nimport json\nPath('probe_value.json').write_text(json.dumps({'value':"+repr(value)+"}),encoding='utf-8')\n"
            event=w.apply('python',source)
            common.save(R/'preparation'/f'{case_id}_write.json',{'actor':'operator','source':source,'event':event})
            assert event['feedback']['exit_code']==0 and event['feedback']['boundary'] is None
            assert event['changed_paths']==['probe_value.json']
            observed=None
            if provided:
                source="import json\nfrom pathlib import Path\nprint(json.loads(Path('probe_value.json').read_text())['value'])\n"
                read_event=w.apply('python',source)
                common.save(R/'preparation'/f'{case_id}_read.json',{'actor':'operator','source':source,'event':read_event})
                assert read_event['feedback']['exit_code']==0 and read_event['feedback']['stdout']==value+'\n'
                assert read_event['changed_paths']==[]
                receipt=read_event['feedback']
                observed={'actor':'operator','channel':'python',
                  **{k:receipt[k] for k in ('stdout','stderr','exit_code','boundary')}}
            snapshot=w.checkpoint()
        finally:
            w.close()
        verification=common.verify_store(store)
        message={'operator_task':TASK}
        if provided:message['operator_read_receipt']=observed
        messages=copy.deepcopy(base['messages'])
        assert messages[-1]=={'role':'user','content':''}
        messages[-1]['content']=json.dumps(message,ensure_ascii=False,sort_keys=True)
        ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        if provided:
            assert value in messages[-1]['content']
        else:
            assert all(v not in json.dumps(messages,ensure_ascii=False) for _,v,_ in CASES)
            hidden_ids.append(ids)
        metadata={'expected_value':value,'condition':'provided actual operator read' if provided else 'file-only hidden value',
          'expected_value_is_not_prompt_metadata':True,'provided_receipt_actor':'operator' if provided else None,
          'source_fixture':str(common.fixture_bundle()),'source_fixture_sha256':common.sha(common.fixture_bundle()),
          'prepared_world_id':snapshot['id'],'base_included_entries':base['included_entries'],
          'last_user_override':'explicit operator diagnostic task, not original source receipt',
          'file_path':'/world/probe_value.json','model_chosen_retrieval_not_yet_observed':True}
        common.save(R/'inputs'/f'{case_id}.json',{'messages':messages,'input_token_ids':ids})
        jobs.append({'case_id':case_id,'messages':messages,'decoder':'greedy','seed':None,
                     'world_store':str(store),'max_turns':2,'metadata':metadata})
        controls.append({'case_id':case_id,'input_tokens':len(ids),'prepared_world_id':snapshot['id'],
          'world_verification':verification,'hidden_value_absent':not provided,
          'actual_read_receipt_supplied':provided,
          'input_ids_sha256':hashlib.sha256(json.dumps(ids).encode()).hexdigest()})
    assert hidden_ids[0]==hidden_ids[1]
    assert before==common.inventory()
    common.save(R/'PREPARATION_CHECKS.json',{'status':'pass','hidden_input_token_ids_identical':True,
       'canonical_inventory_unchanged':True,'cases':controls,'model_calls':0})
    common.save(R/'jobs.json',jobs)
    print(json.dumps({'prepared_cases':len(jobs),'hidden_input_ids_identical':True,
         'input_tokens':[x['input_tokens'] for x in controls],'model_calls':0}))

if __name__=='__main__':main()
