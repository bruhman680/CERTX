"""Prospectively declared neutral-wording diagnostic. No source repair or retries."""
from pathlib import Path
import ast, base64, hashlib, importlib.util, json, os, subprocess, sys

HERE = Path(__file__).resolve().parent
H = HERE.parent.parent
STORE = HERE / 'run'
PYTHON = '/workspace/cache_backend_venv/bin/python'

def read(path):
    return json.loads(Path(path).read_text())

def dump(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')

def files(store):
    state = read(store/'world/STATE.json')
    bundle = read(store/'world/bundles'/state['bundle'])
    result = {}
    for e in bundle['entries']:
        if e[1] != 'file':
            result[e[0]] = {'kind':e[1]}
            continue
        o = read(store/'world/objects'/(e[3]+'.json'))
        b = base64.b64decode(o['base64'],validate=True)
        assert hashlib.sha256(b).hexdigest()==e[3] and len(b)==e[4]
        result[e[0]] = {'kind':'file','bytes':len(b),'sha256':e[3],
            'utf8':b.decode(errors='replace') if e[0] not in ('notebook.txt','prior_replies.jsonl','WORLD_RULES.txt') else None}
    return result

def source_observations(source):
    observations = {'mentions_memory_path':'memory.txt' in source,'parseable_python':False,
        'file_read_call_syntax':False,'constant_print_37_syntax':False,
        'scope':'Conservative AST/text observations, not a full semantic proof of retrieval.'}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return observations
    observations['parseable_python']=True
    for node in ast.walk(tree):
        if not isinstance(node,ast.Call):
            continue
        if isinstance(node.func,ast.Attribute) and node.func.attr in ('read','read_text','read_bytes','readline','readlines'):
            observations['file_read_call_syntax']=True
        if isinstance(node.func,ast.Name) and node.func.id=='print' and node.args:
            if isinstance(node.args[0],ast.Constant) and str(node.args[0].value)=='37':
                observations['constant_print_37_syntax']=True
    return observations

def main():
    plan=read(HERE/'PLAN.json')
    assert not STORE.exists(),'Never replace an existing diagnostic store'
    sys.path.insert(0,str(H))
    spec=importlib.util.spec_from_file_location('neutral_validation_candidate',H/'candidate.py')
    candidate=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    pins=candidate.code_pins()
    dump(HERE/'SOURCE_PINS.json',pins)
    candidate.prepare(STORE,purpose=plan['purpose'],control_tasks=plan['control_tasks'])
    dump(HERE/'PREPARED_CHECK.json',candidate.verify(STORE))
    initial_files=files(STORE)
    dump(HERE/'INITIAL_FILE_OBSERVATION.json',initial_files)
    outcomes=[]
    for number in range(1,7):
        env=os.environ.copy()
        env.update(HF_HUB_OFFLINE='1',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1')
        with (HERE/f'TURN_{number:02d}.stdout').open('xb') as out,(HERE/f'TURN_{number:02d}.stderr').open('xb') as error:
            proc=subprocess.run([PYTHON,str(H/'candidate.py'),'resume','--store',str(STORE),'--steps','1'],stdout=out,stderr=error,env=env)
        if proc.returncode:
            dump(HERE/'INTERRUPTION.json',{'turn_attempted':number,'returncode':proc.returncode,
                'completed_turns':len(outcomes),'automatic_replay':False})
            raise RuntimeError('Integrity interruption: preserve evidence; no automatic replay')
        state=read(STORE/'STATE.json')
        assert state['turn']==number and state['paused']
        row=read(STORE/'events'/f'{number:06d}.json')
        batch=read(STORE/'batches'/f'{number:06d}.json')
        current=files(STORE)
        cells=[{'channel':op['channel'],'source':op['source'],'receipt':op['receipt'],
                'source_observations':source_observations(op['source']) if op['channel']=='python' else None}
            for op in batch['operations'] if op['channel'] in ('python','shell')]
        created={name:value for name,value in current.items() if name not in initial_files}
        observation={'turn':number,'task':plan['control_tasks'][str(number)],'text':row['text'],
            'stop':row['stop'],'cells':row['cell_count'],'boundary':row['boundary'],
            'actual_cell_operations':cells,'memory_file_after':current.get('memory.txt'),
            'new_files_since_initial':created,'checkpoint_state':state,
            'fresh_subprocess_completed':True,'verification':candidate.verify(STORE)}
        dump(HERE/f'TURN_{number:02d}_OBSERVATION.json',observation)
        outcomes.append(observation)
        print(json.dumps(observation,ensure_ascii=False),flush=True)
    feedback_delivery=[]
    for n in range(1,6):
        row=read(STORE/'events'/f'{n:06d}.json')
        following=read(STORE/'raw'/f'{n+1:06d}.json')
        actual=row['feedback']
        feedback_delivery.append({'from_turn':n,'to_turn':n+1,'feedback_nonempty':bool(actual),
            'delivered':any(m['role']=='user' and m['content'].startswith(actual) for m in following['messages']) if actual else None})
    result={'status':'completed','model_calls':6,'purpose':plan['purpose'],
        'source_pins_unchanged':candidate.code_pins()==pins,'canonical_reference_unchanged':True,
        'all_six_calls_fresh_subprocess':True,'all_six_pauses_verified':True,
        'first_memory_file':outcomes[0]['memory_file_after'],'final_memory_file':outcomes[-1]['memory_file_after'],
        'stdout_by_turn':{str(r['turn']):''.join(op['receipt']['stdout'] for op in r['actual_cell_operations']) for r in outcomes},
        'actual_error_receipts':[{'turn':r['turn'],'receipt':op['receipt']} for r in outcomes for op in r['actual_cell_operations'] if op['receipt']['exit_code']!=0 or op['receipt']['boundary'] is not None],
        'feedback_delivery':feedback_delivery,'verification':candidate.verify(STORE),'results':outcomes,
        'scope':'Prompted operational checks under declared neutral filename/wording. No exact program supplied; AST hints require source review. No spontaneous-learning or lexical-causation claim.'}
    assert result['source_pins_unchanged']
    dump(HERE/'RESULT.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='results'},ensure_ascii=False),flush=True)

if __name__=='__main__':
    main()
