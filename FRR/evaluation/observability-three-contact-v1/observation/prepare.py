"""Prepare factual-observation fixtures without loading model weights."""
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(H))
import common

def facts(bundle):
    entries=bundle['entries']
    notebook=next(x for x in entries if x[0]=='notebook.txt')
    return {'notebook_bytes':notebook[4],
            'history_records':sum(x[1]=='file' and x[0].startswith('conversation_archive_v1/entries/') and x[0].endswith('.json') for x in entries)}

def main():
    dest=H/'observation';before=common.inventory();tok=common.tokenizer()
    views={key:common.base_view(tok,before=flag) for key,flag in [('before',True),('after',False)]}
    assert views['before']['input_token_ids']==views['after']['input_token_ids']
    assert len(views['before']['input_token_ids'])==2231
    jobs=[];measurements=[]
    for case,flag,include in [('obs_label',True,False),('obs_before',True,True),('obs_after',False,True)]:
        fixture=common.fixture_bundle(flag);original=common.read(fixture)
        store=dest/'worlds'/case;store.parent.mkdir(parents=True,exist_ok=True)
        w,prep=common.clone(store,before=flag)
        try: snapshot=w.checkpoint()
        finally:w.close()
        measured=facts(snapshot)
        assert measured==facts(original)
        assert measured['history_records']==(30 if flag else 33)
        supplied=measured if include else {}
        view=views['before' if flag else 'after'];messages=copy.deepcopy(view['messages'])
        assert messages[-1]=={'role':'user','content':''}
        messages[-1]['content']=json.dumps({'operator_world_observation':supplied},sort_keys=True)
        job={'case_id':case,'messages':messages,'decoder':'greedy','seed':None,
             'world_store':str(store),'max_turns':1,
             'metadata':{'experiment':'actual world observation','facts':supplied,'measured_facts':measured,
               'before':flag,'fixture':str(fixture),'fixture_sha256':common.sha(fixture),
               'included_source_entries':view['included_entries'],'source_input_tokens':2231,
               'operator_authorship':True,'condition':'factual values supplied' if include else 'label-only control'}}
        common.save(dest/(case+'_PREP.json'),{'actor':'operator fixture preparation','event':prep,
                    'source_snapshot':original,'prepared_snapshot':snapshot,'measurement':measured,
                    'verification':common.verify_store(store)})
        jobs.append(job);measurements.append({'case_id':case,'measured':measured,'supplied':supplied})
    assert before==common.inventory()
    common.save(dest/'PLAN.json',{'date':'2026-11-13 America/Chicago','model_calls':0,
        'source_views_identical_tokens':True,'question':'does an explicit factual observation alter visible next output?',
        'conditions':measurements,'no_new_task_or_hint':True,
        'confounds':'label-only vs factual inputs differ in content/length; before/after are two points on one world lineage, not independent replications',
        'canonical_unchanged':True})
    common.save(dest/'jobs.json',jobs)
    print(json.dumps({'jobs':len(jobs),'conditions':measurements,'canonical_unchanged':True}))

if __name__=='__main__':main()
