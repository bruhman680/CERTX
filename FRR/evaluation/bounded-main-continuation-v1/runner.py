"""Explicit linked continuation: bounded input, full external records, unchanged body/world."""
from pathlib import Path
import argparse,base64,copy,hashlib,importlib.util,json,os,sys,traceback,uuid
H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1';V=E/'bounded-view-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(V),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import GardenWorld,verify_store,immutable,atomic,read,digest,parse_notebook
from view import select_view,ViewCapacity
spec=importlib.util.spec_from_file_location('bounded_main_unchanged_body',C/'generation.py')
body=importlib.util.module_from_spec(spec);spec.loader.exec_module(body)
MODEL=candidate.BASE

def inventory(root):
    return {str(p.relative_to(root)):digest(p) for p in Path(root).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def code_pins():
    paths=[Path(__file__),V/'view.py',C/'generation.py',C/'candidate.py',C/'world/garden_world.py',MODEL/'config.json',MODEL/'tokenizer.json',MODEL/'tokenizer_config.json',E/'retrieval-task-transfer-v1/main50-proposal/PROPOSED_WORLD_RULE_APPEND.txt']
    return {str(p):digest(p) for p in paths}

def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False)

def events(r):return [read(p) for p in sorted((Path(r)/'events').glob('*.json'))]

def current_view(r,tok,prior=None):
    r=Path(r);base=read(r/'BASE_ARCHIVE.json');rows=events(r) if prior is None else prior
    exchanges=base['exchanges']+[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in rows]
    return select_view(base['initial_messages'],exchanges,tok,max_pairs=8,max_input=7936)

def guard_parent(r):
    r=Path(r);manifest=read(r/'MANIFEST.json')
    assert inventory(C)==read(r/'PARENT_INVENTORY.json'),'Preserved parent phase changed'
    assert all(digest(p)==sha for p,sha in manifest['pins'].items()),'Runner/body/view dependency drift'

def prepare(r,purpose='main continuation'):
    r=Path(r);r.mkdir(parents=True,exist_ok=False)
    for name in ['events','plans','raw','batches','sessions']:(r/name).mkdir()
    parent_inventory=inventory(C);parent_state=read(C/'run/STATE.json')
    assert parent_state['human_entry']==1580 and parent_state['paused']
    assert not (C/'run/PENDING.json').exists() and not (C/'run/RUN.lock').exists()
    archive={'initial_messages':read(C/'run/INITIAL_MESSAGES.json'),'exchanges':[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in candidate.rows(C/'run')]}
    assert len(archive['exchanges'])==30 and archive['exchanges'][-1]['entry']==1580
    immutable(r/'BASE_ARCHIVE.json',archive);immutable(r/'PARENT_INVENTORY.json',parent_inventory)
    immutable(r/'PARENT_STATE.json',parent_state)
    immutable(r/'PARENT_ACTIVE_POINTER.json',read(E.parent/'ACTIVE_GARDEN_PHASE.json'))
    parent_world_state=read(C/'run/world/STATE.json')
    parent_bundle=C/'run/world/bundles'/parent_world_state['bundle']
    immutable(r/'PARENT_WORLD.json',read(parent_bundle))
    addition=(E/'retrieval-task-transfer-v1/main50-proposal/PROPOSED_WORLD_RULE_APPEND.txt').read_text()
    immutable(r/'PROPOSED_RULE_APPEND.json',{'text':addition})
    manifest={'version':'bounded-main-continuation-v1','purpose':purpose,'parent_entry':1580,'parent_phase':'minimal-garden-candidate-v1','parent_bundle_sha256':digest(parent_bundle),'pins':code_pins(),'tensor_digest':read(C/'run/MANIFEST.json')['tensor_digest'],'weights_sha256':read(C/'run/MANIFEST.json')['weights_sha256'],'input_policy':'original initial framing plus latest8 complete pairs, oldest-first budget fallback; latest mandatory','input_limit':7936,'output_limit':256,'decoder':'greedy_argmax','archive':'full external base+new events; no automatic in-world copies','operator_world_delta':['WORLD_RULES.txt'],'training_updates':0,'authorizing_user_request':'run several cycles ... go ahead and run the50block ... if tokenlimit exceeded you may limitit if confident','status':'prepared; activation is separately recorded'}
    immutable(r/'MANIFEST.json',manifest)
    immutable(r/'PENDING.json',{'stage':'operator initialization unresolved'})
    w=GardenWorld.create(r/'world',parent_bundle,C/'run/world/objects',parent_entry=1580)
    try:
        before=w.checkpoint()
        code="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(addition)+",encoding='utf-8')"
        op=w.apply('python',code);immutable(r/'INITIALIZATION.json',{'actor':'operator','source':code,'event':op})
        assert op['feedback']['exit_code']==0 and op['feedback']['boundary'] is None and op['changed_paths']==['WORLD_RULES.txt']
        after=w.checkpoint();old={x[0]:x for x in before['entries']};new={x[0]:x for x in after['entries']}
        assert set(old)==set(new) and all(old[k]==new[k] for k in old if k!='WORLD_RULES.txt')
        immutable(r/'INITIAL_WORLD.json',after)
    finally:w.close()
    atomic(r/'STATE.json',{'parent_entry':1580,'turn':0,'human_entry':1580,'paused':True,'last_event_sha256':None,'world_step':1})
    (r/'PENDING.json').unlink()
    guard_parent(r)
    return read(r/'STATE.json')

def verify(r,tok=None):
    r=Path(r);guard_parent(r)
    if (r/'PENDING.json').exists():raise RuntimeError('Pending outcome: inspect saved effects; never replay automatically')
    tok=tok or tokenizer();state=read(r/'STATE.json');manifest=read(r/'MANIFEST.json')
    base=read(r/'BASE_ARCHIVE.json')
    assert base['initial_messages']==read(C/'run/INITIAL_MESSAGES.json')
    assert base['exchanges']==[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in candidate.rows(C/'run')]
    assert read(r/'PARENT_STATE.json')==read(C/'run/STATE.json')
    parent=read(r/'PARENT_WORLD.json');assert digest(r/'world/bundles/000000.json')==manifest['parent_bundle_sha256']
    init=read(r/'INITIALIZATION.json');assert init['actor']=='operator' and init['event']==read(r/'world/events/000001.json')
    assert init['event']['before_id']==parent['id'] and init['event']['changed_paths']==['WORLD_RULES.txt']
    previous=[];last=None;world_before=read(r/'INITIAL_WORLD.json')
    assert world_before==read(r/'world/bundles/000001.json')
    addition=read(r/'PROPOSED_RULE_APPEND.json')['text']
    assert addition==(E/'retrieval-task-transfer-v1/main50-proposal/PROPOSED_WORLD_RULE_APPEND.txt').read_text()
    expected_source="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(addition)+",encoding='utf-8')"
    assert init['source']==init['event']['source']==expected_source
    old_rule=next(x for x in parent['entries'] if x[0]=='WORLD_RULES.txt')
    new_rule=next(x for x in world_before['entries'] if x[0]=='WORLD_RULES.txt')
    old_bytes=base64.b64decode(read(C/'run/world/objects'/(old_rule[3]+'.json'))['base64'],validate=True)
    new_bytes=base64.b64decode(read(r/'world/objects'/(new_rule[3]+'.json'))['base64'],validate=True)
    assert new_bytes==old_bytes+addition.encode('utf-8')
    for n,row in enumerate(events(r),1):
        assert row['turn']==n and row['human_entry']==1580+n and row['parent_event_sha256']==last
        assert row['parent_phase_last_event_sha256']==read(r/'PARENT_STATE.json')['last_event_sha256']
        view=current_view(r,tok,previous);plan=read(r/'plans'/f'{n:06d}.json');raw=read(r/'raw'/f'{n:06d}.json');batch=read(r/'batches'/f'{n:06d}.json')
        assert plan['view']==view and plan['human_entry']==row['human_entry'] and plan['before_id']==world_before['id']
        assert raw['messages']==view['messages'] and raw['input_token_ids']==view['input_token_ids']
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==row['text']==batch['raw_text']
        if manifest['purpose']=='main continuation':assert raw['decoder']=='greedy_argmax'
        else:assert raw['decoder'] in ['greedy_argmax','fixture_no_inference']
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
        assert row['raw_sha256']==digest(r/'raw'/f'{n:06d}.json') and row['batch_sha256']==digest(r/'batches'/f'{n:06d}.json')
        assert row['feedback']==candidate.project_feedback(batch) and batch['parsed']==parse_notebook(raw['text'])
        assert batch==read(r/'world/batches'/(batch['batch_id']+'.json'))
        assert row['before_id']==world_before['id'] and row['cell_count']==batch['parsed']['complete_executable_cells'] and row['boundary']==batch['boundary']
        for op in batch['operations']:
            plain={k:v for k,v in op.items() if k not in ['cell_index','source_start','source_end']}
            assert plain==read(r/'world/events'/f"{op['step']:06d}.json")
            if 'cell_index' in op:
                cell=batch['parsed']['cells'][op['cell_index']]
                assert cell['complete'] and cell['executable'] and op['source']==cell['source']
                assert op['source_start']==cell['source_start'] and op['source_end']==cell['source_end']
        if batch['operations']:
            assert batch['operations'][0]['before_id']==world_before['id']
            world_before=read(r/'world/bundles'/f"{batch['operations'][-1]['step']:06d}.json")
        assert row['after_id']==world_before['id']
        previous.append(row);last=digest(r/'events'/f'{n:06d}.json')
    assert len(previous)==state['turn'] and state['human_entry']==1580+len(previous) and state['last_event_sha256']==last
    check=verify_store(r/'world');assert check['bundle_id']==world_before['id'] and check['step']==state['world_step']
    w=GardenWorld.open(r/'world')
    try:assert w.checkpoint()==world_before
    finally:w.close()
    try:
        view=current_view(r,tok);capacity={'next_input_tokens':len(view['input_token_ids']),'included_entries':view['included_entries'],'omitted_entries':view['omitted_entries'],'within_capacity':True}
    except ViewCapacity as e:capacity={'within_capacity':False,'reason':str(e)}
    return {'status':'pass','human_entry':state['human_entry'],'turns':state['turn'],'world':check,'next_view':capacity,'parent_files_unchanged':len(read(r/'PARENT_INVENTORY.json')),'pending':False,'training_updates':0}

def commit_reply(r,tok,world,view,raw):
    """Called only after an immutable plan+pending marker; never repairs/replays."""
    r=Path(r);old=read(r/'STATE.json');n=old['turn']+1
    assert (r/'PENDING.json').exists()
    assert raw['messages']==view['messages'] and raw['input_token_ids']==view['input_token_ids']
    immutable(r/'raw'/f'{n:06d}.json',raw)
    before=world.checkpoint();batch=world.receive_notebook(raw['text']);immutable(r/'batches'/f'{n:06d}.json',batch);after=world.checkpoint()
    row={'turn':n,'human_entry':1580+n,'text':raw['text'],'stop':raw['stop'],'feedback':candidate.project_feedback(batch),'before_id':before['id'],'after_id':after['id'],'parent_event_sha256':old['last_event_sha256'],'parent_phase_last_event_sha256':read(r/'PARENT_STATE.json')['last_event_sha256'],'raw_sha256':digest(r/'raw'/f'{n:06d}.json'),'batch_sha256':digest(r/'batches'/f'{n:06d}.json'),'cell_count':batch['parsed']['complete_executable_cells'],'boundary':batch['boundary']}
    immutable(r/'events'/f'{n:06d}.json',row)
    atomic(r/'STATE.json',{'parent_entry':1580,'turn':n,'human_entry':1580+n,'paused':False,'last_event_sha256':digest(r/'events'/f'{n:06d}.json'),'world_step':world.step})
    (r/'PENDING.json').unlink()
    return row

def plan_reply(r,tok,world):
    r=Path(r);state=read(r/'STATE.json');n=state['turn']+1
    if (r/'PENDING.json').exists():raise RuntimeError('Pending outcome; no automatic replay')
    view=current_view(r,tok);before=world.checkpoint()
    immutable(r/'plans'/f'{n:06d}.json',{'human_entry':1580+n,'view':view,'before_id':before['id']})
    immutable(r/'PENDING.json',{'turn':n,'human_entry':1580+n,'stage':'generation and action unresolved; no automatic replay'})
    return view

def resume(r,steps=50,check_every=10):
    if type(steps)is not int or not 1<=steps<=50:raise ValueError('Block must be1–50 actual replies')
    if type(check_every)is not int or check_every<1:raise ValueError('Positive check interval required')
    r=Path(r);token=uuid.uuid4().hex
    immutable(r/'RUN.lock',{'token':token,'pid':os.getpid()})
    world=None;session=uuid.uuid4().hex;started=None
    try:
        assert read(r/'MANIFEST.json')['purpose']=='main continuation','Test fixture is not a main run'
        tok=tokenizer();pre=verify(r,tok);state=read(r/'STATE.json');assert state['paused'];started=state['turn']
        immutable(r/'sessions'/(session+'_PLAN.json'),{'steps':steps,'check_every':check_every,'start_entry':state['human_entry'],'precheck':pre})
        for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import Guard,parameter_digest
        torch.set_num_threads(2)
        guard=Guard(5153960755,r/'sessions'/(session+'_RESOURCE.jsonl'));guard.read('before_model_load')
        model=AutoModelForCausalLM.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        model.requires_grad_(False);model.eval();expected=read(r/'MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected
        reason='completed';world=GardenWorld.open(r/'world');state['paused']=False;atomic(r/'STATE.json',state)
        for i in range(steps):
            if (r/'PAUSE_REQUEST').exists():reason='user_pause';break
            guard_parent(r)
            try:view=plan_reply(r,tok,world)
            except ViewCapacity as e:
                reason='context_capacity';immutable(r/'sessions'/(session+'_CAPACITY.json'),{'reason':str(e),'entry':read(r/'STATE.json')['human_entry']});break
            raw=body.generate(model,tok,view['messages'],guard,'bounded_main_'+str(read(r/'STATE.json')['human_entry']+1))
            row=commit_reply(r,tok,world,view,raw)
            assert parameter_digest(model,False)==expected
            if (i+1)%check_every==0 or i+1==steps:
                world.close();world=None;check=verify(r,tok)
                immutable(r/'sessions'/(session+f'_CHECK_{i+1:03d}.json'),check)
                print(json.dumps({'human_entry':row['human_entry'],'block_completed':i+1,'complete_cells_this_reply':row['cell_count'],'check':check['status']}),flush=True)
                world=GardenWorld.open(r/'world')
        world.close();world=None
        state=read(r/'STATE.json');state['paused']=True;atomic(r/'STATE.json',state)
        assert parameter_digest(model,False)==expected;check=verify(r,tok)
        result={'reason':reason,'start_entry':1580+started,'end_entry':state['human_entry'],'actual_model_replies':state['turn']-started,'verification':check,'weights_unchanged':True,'training_updates':0}
        immutable(r/'sessions'/(session+'_RESULT.json'),result);print(json.dumps(result),flush=True);return result
    except BaseException as e:
        immutable(r/'sessions'/(session+'_ERROR.json'),{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'pending':(r/'PENDING.json').exists()});raise
    finally:
        if world is not None:world.close()
        if (r/'STATE.json').exists():
            state=read(r/'STATE.json');state['paused']=True;atomic(r/'STATE.json',state)
        if (r/'RUN.lock').exists() and read(r/'RUN.lock').get('token')==token:(r/'RUN.lock').unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prepare','resume','verify','status']);p.add_argument('--store',type=Path,default=H/'run');p.add_argument('--steps',type=int,default=50);p.add_argument('--check-every',type=int,default=10);a=p.parse_args()
    if a.command=='prepare':print(json.dumps(prepare(a.store)))
    elif a.command=='resume':resume(a.store,a.steps,a.check_every)
    elif a.command=='verify':print(json.dumps(verify(a.store)))
    else:print(json.dumps(read(a.store/'STATE.json')))
