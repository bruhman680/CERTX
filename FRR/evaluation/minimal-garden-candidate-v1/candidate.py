"""Durable, auditable candidate continuation. Import never runs the model."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, sys, traceback, uuid

H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
BASE = Path('/workspace/cache_backend_models/smollm2-135m')
sys.path[:0] = [str(H/'world'),str(P.parent/'source-access-three-cycle-v1')]
from garden_world import GardenWorld, atomic, immutable, read, digest, parse_notebook
_spec = importlib.util.spec_from_file_location('candidate_model_body',H/'generation.py')
_body = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_body)

SEED = 'Follow your curiosity and explore your universe. You may play, observe, wonder, experiment, and learn. 😁'
MECHANICS = ('This is a computational notebook in /world. Files persist. Complete fenced python or sh cells execute; '
    'other text is writing. Each cell starts a new process. Real results return after each reply. '
    'Exact syntax and limits are in WORLD_RULES.txt.')

def inventory(root):
    return {str(p.relative_to(root)):digest(p) for p in Path(root).rglob('*')
        if p.is_file() and '__pycache__' not in p.parts}

def code_pins():
    files = [H/'candidate.py',H/'generation.py',H/'world/garden_world.py',H/'CONTRACT.json',H/'ENVIRONMENT.md',
        P/'world.py',P/'server.py',P/'HOST_RUNTIME_IDENTITY.json',BASE/'config.json',BASE/'tokenizer_config.json',BASE/'tokenizer.json']
    return {str(p):digest(p) for p in files}

def check_reference(r):
    if inventory(P) != read(r/'REFERENCE_INVENTORY.json'):
        raise RuntimeError('Preserved reference version changed')
    m = read(r/'MANIFEST.json')
    assert digest(r/'INITIAL_MESSAGES.json')==m['initial_messages_sha256']
    assert digest(r/'CONTROL_TASKS.json')==m['control_tasks_sha256']
    for file,key in [('INITIAL_WORLD.json','initial_world_sha256'),('INITIALIZATION.json','initialization_sha256'),('PARENT_WORLD.json','parent_world_sha256')]:
        assert digest(r/file)==m[key]
    for p,expected in m['pins'].items():
        if digest(p)!=expected:
            raise RuntimeError('Candidate dependency drift: '+p)
    if digest(BASE/'model.safetensors') != m['weights_sha256']:
        raise RuntimeError('Pinned model weights changed')

def project_feedback(batch):
    """Only actual consequences; no observer scores, interpretation or timings."""
    values = []
    for op in batch['operations']:
        receipt = op['feedback']
        if receipt is None:
            continue
        values.append({'channel':op['channel'],**{k:receipt[k] for k in ['stdout','stderr','exit_code','boundary']}})
    if batch['boundary'] is None and not values:
        return ''
    return json.dumps({'receipts':values,'boundary':batch['boundary']},ensure_ascii=False,sort_keys=True)

def rows(r):
    return [read(p) for p in sorted((r/'events').glob('*.json'))]

def messages(r, prior=None):
    result = read(r/'INITIAL_MESSAGES.json')
    tasks = read(r/'CONTROL_TASKS.json')
    history = rows(r) if prior is None else prior
    for number,row in enumerate(history,1):
        if str(number) in tasks:
            result[-1]['content']+='\n\n'+tasks[str(number)]
        result.extend([{'role':'assistant','content':row['text']},{'role':'user','content':row['feedback']}])
    if str(len(history)+1) in tasks:
        result[-1]['content']+='\n\n'+tasks[str(len(history)+1)]
    return result

def prepare(r, initial_messages=None, purpose='open invitation', control_tasks=None):
    """All mutation is in a new store; the old phase is a checked parent."""
    r = Path(r)
    r.mkdir(parents=True,exist_ok=False)
    for name in ['events','plans','raw','batches','sessions']:
        (r/name).mkdir()
    reference = inventory(P)
    s = read(P/'run/STATE.json')
    assert s['paused'] and s['next_entry']==1550
    assert not (P/'run/PENDING.json').exists() and not (P/'run/RUN.lock').exists()
    immutable(r/'REFERENCE_INVENTORY.json',reference)
    immutable(r/'PARENT_ACTIVE_POINTER.json',read(H.parent.parent/'ACTIVE_GARDEN_PHASE.json'))
    initial = initial_messages if initial_messages is not None else [
        {'role':'system','content':''},{'role':'user','content':MECHANICS+'\n\n'+SEED}]
    assert initial[0]=={'role':'system','content':''}
    immutable(r/'INITIAL_MESSAGES.json',initial)
    tasks = {} if control_tasks is None else control_tasks
    assert isinstance(tasks,dict) and all(k.isdigit() and int(k)>0 and isinstance(v,str) for k,v in tasks.items())
    if tasks and purpose=='open invitation':
        raise ValueError('Explicit tasks must be labeled diagnostic, never hidden in open exploration')
    immutable(r/'CONTROL_TASKS.json',tasks)
    immutable(r/'MANIFEST.json',{'version':'minimal-garden-candidate-v1','purpose':purpose,
        'parent_entry':1550,'pins':code_pins(),'weights_sha256':read(P/'CONTRACT.json')['model']['weights_sha256'],
        'tensor_digest':read(P/'run/MODEL_CONDITION.json')['tensor_digest'],
        'context_reset':'new candidate context; old filesystem and original records retained',
        'memory':'entire actual candidate conversation until exact capacity pause; no summaries or forced directory suffix',
        'input_limit':_body.MAX_INPUT,'output_limit':_body.MAX_OUTPUT,'decoder':'greedy_argmax',
        'initial_messages_sha256':digest(r/'INITIAL_MESSAGES.json'),'control_tasks_sha256':digest(r/'CONTROL_TASKS.json'),
        'initialization':'inherit1550 then add mechanical WORLD_RULES.txt via an explicitly recorded operator action',
        'cell_grammar':'complete explicit python/sh notebook cells; no semantic extraction/repair',
        'training_updates':0,'added_adapter':False})
    world = GardenWorld.create(r/'world',P/'run/bundles/001550.json',P/'run/objects',parent_entry=1550)
    try:
        immutable(r/'PARENT_WORLD.json',world.bundle)
        rules = (H/'ENVIRONMENT.md').read_text()
        source = "from pathlib import Path\nPath('WORLD_RULES.txt').write_text("+repr(rules)+",encoding='utf-8')\n"
        initialization = world.apply('python',source)
        if initialization['receipt']['exit_code']!=0 or initialization['receipt']['boundary'] is not None:
            raise RuntimeError('Known initialization failure; inspect the new candidate store')
        immutable(r/'INITIALIZATION.json',{'actor':'operator','model_generation':False,'operation':initialization})
        immutable(r/'INITIAL_WORLD.json',world.checkpoint())
    finally:
        world.close()
    manifest = read(r/'MANIFEST.json')
    manifest.update(initial_world_sha256=digest(r/'INITIAL_WORLD.json'),
        initialization_sha256=digest(r/'INITIALIZATION.json'),parent_world_sha256=digest(r/'PARENT_WORLD.json'))
    atomic(r/'MANIFEST.json',manifest)
    atomic(r/'STATE.json',{'parent_entry':1550,'turn':0,'human_entry':1550,'paused':True,
        'last_event_sha256':None,'world_step':read(r/'world/STATE.json')['step']})
    assert inventory(P)==reference
    return read(r/'STATE.json')

def verify(r, tokenizer=None):
    r = Path(r)
    check_reference(r)
    state = read(r/'STATE.json')
    if (r/'PENDING.json').exists():
        raise RuntimeError('Unfinished generation/action; inspect retained plan and effects, never replay automatically')
    if tokenizer is None:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
    last,previous = None,[]
    world_before = read(r/'INITIAL_WORLD.json')
    parent = read(r/'PARENT_WORLD.json')
    assert parent==read(P/'run/bundles/001550.json')
    initialization = read(r/'INITIALIZATION.json')
    assert initialization['actor']=='operator' and initialization['model_generation'] is False
    assert initialization['operation']==read(r/'world/events/000001.json')
    assert initialization['operation']['before_id']==parent['id']
    assert initialization['operation']['changed_paths']==['WORLD_RULES.txt']
    assert world_before==read(r/'world/bundles/000001.json')
    rule = next(e for e in world_before['entries'] if e[0]=='WORLD_RULES.txt')
    assert rule[1]=='file' and rule[3]==hashlib.sha256((H/'ENVIRONMENT.md').read_bytes()).hexdigest()
    for turn,row in enumerate(rows(r),1):
        assert row['turn']==turn and row['human_entry']==1550+turn and row['parent_event_sha256']==last
        raw = read(r/'raw'/f'{turn:06d}.json')
        p = read(r/'plans'/f'{turn:06d}.json')
        b = read(r/'batches'/f'{turn:06d}.json')
        expected = messages(r,previous)
        ids = tokenizer.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
        assert expected==raw['messages']==p['messages'] and ids==raw['input_token_ids']==p['input_token_ids']
        assert len(ids)<=_body.MAX_INPUT
        assert tokenizer.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==row['text']
        assert raw['decoder']=='greedy_argmax'
        assert raw['stop']==row['stop']
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tokenizer.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==_body.MAX_OUTPUT)
        assert row['raw_sha256']==digest(r/'raw'/f'{turn:06d}.json')
        assert p['before_id']==row['before_id']==world_before['id']
        assert b['raw_text']==row['text'] and row['feedback']==project_feedback(b)
        assert b['parsed']==parse_notebook(row['text'])
        assert b==read(r/'world/batches'/(b['batch_id']+'.json'))
        assert row['cell_count']==b['parsed']['complete_executable_cells'] and row['boundary']==b['boundary']
        ops = b['operations']
        for op in ops:
            plain = {k:v for k,v in op.items() if k not in ['cell_index','source_start','source_end']}
            assert plain==read(r/'world/events'/f"{op['step']:06d}.json")
            if 'cell_index' in op:
                cell = b['parsed']['cells'][op['cell_index']]
                assert cell['executable'] and op['source']==cell['source']
                assert op['source_start']==cell['source_start'] and op['source_end']==cell['source_end']
                assert op['channel']==('python' if cell['language']=='python' else 'shell')
        if ops:
            assert ops[0]['before_id']==world_before['id']
            after_step = ops[-1]['step']
            world_before = read(r/'world/bundles'/f'{after_step:06d}.json')
        assert world_before['id']==row['after_id']
        previous.append(row)
        last = digest(r/'events'/f'{turn:06d}.json')
    assert len(previous)==state['turn'] and state['human_entry']==1550+len(previous)
    assert state['last_event_sha256']==last
    w = GardenWorld.open(r/'world')
    try:
        assert w.checkpoint()==world_before
        assert w.step==state['world_step']
    finally:
        w.close()
    next_ids = tokenizer.apply_chat_template(messages(r),tokenize=True,add_generation_prompt=True)
    return {'status':'pass','parent_entry':1550,'turns':len(previous),'human_entry':state['human_entry'],
        'exact_messages_and_tokens':True,'reference_unchanged':True,'world_restored':True,
        'next_input_tokens':len(next_ids),'next_input_within_capacity':len(next_ids)<=_body.MAX_INPUT,
        'training_updates':0,'verification_model_calls':0}

def run(r, steps, report_every=5):
    r = Path(r)
    if type(steps) is not int or not 1<=steps<=50:
        raise ValueError('Candidate blocks are explicitly bounded to1–50 replies')
    if type(report_every) is not int or report_every<1:
        raise ValueError('Reporting interval must be a positive integer')
    token = uuid.uuid4().hex
    immutable(r/'RUN.lock',{'token':token,'pid':os.getpid()})
    world = None
    reason = 'completed'
    try:
        if (r/'PENDING.json').exists():
            raise RuntimeError('Unfinished attempt; inspect, do not replay')
        state = read(r/'STATE.json')
        assert state['paused']
        for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
            os.environ[k]=v
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from runtime_reference import Guard, parameter_digest
        torch.set_num_threads(2)
        tok = AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
        precheck = verify(r,tok)
        session = f"{state['turn']:06d}_"+uuid.uuid4().hex
        immutable(r/'sessions'/(session+'_PLAN.json'),{'steps':steps,'start_turn':state['turn'],'precheck':precheck})
        guard = Guard(5153960755,r/'sessions'/(session+'_RESOURCE.jsonl'))
        guard.read('before_model_load')
        model = AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,
            use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
        model.requires_grad_(False)
        model.eval()
        expected_tensor = read(r/'MANIFEST.json')['tensor_digest']
        assert parameter_digest(model,False)==expected_tensor
        world = GardenWorld.open(r/'world')
        state['paused']=False
        atomic(r/'STATE.json',state)
        start = state['turn']
        for _ in range(steps):
            if (r/'PAUSE_REQUEST').exists():
                reason='user_pause'
                break
            m = messages(r)
            ids = tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True)
            if len(ids)>_body.MAX_INPUT:
                reason='context_capacity'
                break
            number = read(r/'STATE.json')['turn']+1
            before = world.checkpoint()
            p = {'turn':number,'human_entry':1550+number,'before_id':before['id'],'messages':m,'input_token_ids':ids}
            immutable(r/'plans'/f'{number:06d}.json',p)
            immutable(r/'PENDING.json',{'turn':number,'status':'plan retained before generation/action; no automatic replay'})
            raw = _body.generate(model,tok,m,guard,'candidate_'+f'{number:06d}')
            immutable(r/'raw'/f'{number:06d}.json',raw)
            batch = world.receive_notebook(raw['text'])
            immutable(r/'batches'/f'{number:06d}.json',batch)
            after = world.checkpoint()
            old = read(r/'STATE.json')
            event = {'turn':number,'human_entry':1550+number,'text':raw['text'],'stop':raw['stop'],
                'feedback':project_feedback(batch),'before_id':before['id'],'after_id':after['id'],
                'parent_event_sha256':old['last_event_sha256'],'raw_sha256':digest(r/'raw'/f'{number:06d}.json'),
                'cell_count':batch['parsed']['complete_executable_cells'],'boundary':batch['boundary']}
            immutable(r/'events'/f'{number:06d}.json',event)
            atomic(r/'STATE.json',{'parent_entry':1550,'turn':number,'human_entry':1550+number,'paused':False,
                'last_event_sha256':digest(r/'events'/f'{number:06d}.json'),'world_step':world.step})
            (r/'PENDING.json').unlink()
            assert parameter_digest(model,False)==expected_tensor
            check_reference(r)
            if number%report_every==0 or number==start+steps:
                print(json.dumps({'turn':number,'human_entry':1550+number,'cells_this_reply':event['cell_count'],
                    'stop':raw['stop'],'world_step':world.step,'boundary':event['boundary']}),flush=True)
        assert parameter_digest(model,False)==expected_tensor
        world.close()
        world = None
        final_state = read(r/'STATE.json')
        final_state['paused']=True
        atomic(r/'STATE.json',final_state)
        final_check = verify(r,tok)
        immutable(r/'sessions'/(session+'_RESULT.json'),{'reason':reason,'start_turn':start,'end_turn':final_state['turn'],
            'model_calls':final_state['turn']-start,'verification':final_check,'training_updates':0})
        print(json.dumps({'paused':final_state,'reason':reason,'verification':final_check}),flush=True)
        return final_check
    except BaseException as error:
        immutable(r/'sessions'/('ERROR_'+uuid.uuid4().hex+'.json'),{'type':type(error).__name__,
            'message':str(error),'traceback':traceback.format_exc(),'pending':(r/'PENDING.json').exists()})
        raise
    finally:
        try:
            if world is not None:
                world.close()
        finally:
            if (r/'STATE.json').exists():
                s = read(r/'STATE.json')
                s['paused']=True
                atomic(r/'STATE.json',s)
            if (r/'RUN.lock').exists() and read(r/'RUN.lock').get('token')==token:
                (r/'RUN.lock').unlink()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command',choices=['prepare','resume','verify','status'])
    parser.add_argument('--store',type=Path,default=H/'run')
    parser.add_argument('--steps',type=int,default=12)
    args = parser.parse_args()
    if args.command=='prepare':
        print(json.dumps(prepare(args.store)))
    elif args.command=='resume':
        run(args.store,args.steps)
    elif args.command=='verify':
        print(json.dumps(verify(args.store)))
    else:
        print(json.dumps(read(args.store/'STATE.json')))
