"""Six prospectively declared model calls, two three-turn framing conditions."""
from pathlib import Path
import base64, hashlib, importlib.util, json, os, subprocess, sys
HERE=Path(__file__).resolve().parent
H=HERE.parent.parent
PYTHON='/workspace/cache_backend_venv/bin/python'

def read(p):return json.loads(Path(p).read_text())
def dump(p,v):
    Path(p).parent.mkdir(parents=True,exist_ok=True)
    with Path(p).open('x') as f:
        json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def files(store):
    s=read(store/'world/STATE.json')
    b=read(store/'world/bundles'/s['bundle'])
    result={}
    for e in b['entries']:
        if e[1]!='file':
            result[e[0]]={'kind':e[1]}
            continue
        obj=read(store/'world/objects'/(e[3]+'.json'))
        data=base64.b64decode(obj['base64'],validate=True)
        assert hashlib.sha256(data).hexdigest()==e[3] and len(data)==e[4]
        result[e[0]]={'kind':'file','bytes':len(data),'sha256':e[3],
            'utf8':data.decode(errors='replace') if e[0] not in ('notebook.txt','prior_replies.jsonl','WORLD_RULES.txt') else None}
    return result

def main():
    plan=read(HERE/'PLAN.json')
    sys.path.insert(0,str(H))
    spec=importlib.util.spec_from_file_location('framing_pair_candidate',H/'candidate.py')
    candidate=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    pins=candidate.code_pins()
    dump(HERE/'SOURCE_PINS.json',pins)
    all_results={}
    stores={}
    for arm in plan['arms']:
        directory=HERE/arm
        directory.mkdir(exist_ok=False)
        store=directory/'run'
        kwargs={'purpose':('minimal' if arm=='minimal' else 'standard')+' familiar-file-question diagnostic',
                'control_tasks':plan['control_tasks']}
        if arm=='minimal':kwargs['initial_messages']=plan['initial_messages_minimal']
        candidate.prepare(store,**kwargs)
        dump(directory/'PREPARED_CHECK.json',candidate.verify(store))
        dump(directory/'INITIAL_FILES.json',files(store))
        stores[arm]=store
    for arm in plan['arms']:
        directory=HERE/arm
        store=stores[arm]
        initial_files=read(directory/'INITIAL_FILES.json')
        outcomes=[]
        for number in range(1,4):
            env=os.environ.copy()
            env.update(HF_HUB_OFFLINE='1',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1')
            with (directory/f'TURN_{number:02d}.stdout').open('xb') as out,(directory/f'TURN_{number:02d}.stderr').open('xb') as error:
                p=subprocess.run([PYTHON,str(H/'candidate.py'),'resume','--store',str(store),'--steps','1'],stdout=out,stderr=error,env=env)
            if p.returncode:
                dump(HERE/'INTERRUPTION.json',{'arm':arm,'turn_attempted':number,'returncode':p.returncode,
                    'completed_in_arm':len(outcomes),'automatic_replay':False})
                raise RuntimeError('Integrity interruption; retain evidence and do not replay')
            state=read(store/'STATE.json')
            assert state['turn']==number and state['paused']
            row=read(store/'events'/f'{number:06d}.json')
            batch=read(store/'batches'/f'{number:06d}.json')
            current=files(store)
            operations=[{'channel':o['channel'],'source':o['source'],'receipt':o['receipt']}
                for o in batch['operations'] if o['channel'] in ('python','shell')]
            observation={'arm':arm,'turn':number,'task':plan['control_tasks'][str(number)],
                'text':row['text'],'stop':row['stop'],'cells':row['cell_count'],'boundary':row['boundary'],
                'operations':operations,'memory_file_after':current.get('memory.txt'),
                'new_files_since_initial':{name:value for name,value in current.items() if name not in initial_files},
                'state':state,'fresh_subprocess':True,'verification':candidate.verify(store)}
            dump(directory/f'TURN_{number:02d}_OBSERVATION.json',observation)
            outcomes.append(observation)
            assert candidate.code_pins()==pins
            print(json.dumps(observation,ensure_ascii=False),flush=True)
        feedback=[]
        for number in (1,2):
            prior=read(store/'events'/f'{number:06d}.json')['feedback']
            following=read(store/'raw'/f'{number+1:06d}.json')['messages']
            feedback.append({'from_turn':number,'to_turn':number+1,'nonempty':bool(prior),
                'delivered':any(m['role']=='user' and m['content'].startswith(prior) for m in following) if prior else None})
        result={'arm':arm,'model_calls':3,'outcomes':outcomes,'final_memory_file':outcomes[-1]['memory_file_after'],
            'feedback_delivery':feedback,'verification':candidate.verify(store)}
        dump(directory/'RESULT.json',result)
        all_results[arm]=result
    result={'status':'completed','new_model_calls':6,'source_pins_unchanged':candidate.code_pins()==pins,
        'canonical_reference_unchanged':True,'arms':all_results,
        'scope':'Joint mechanics/invitation framing comparison under fixed candidate physics/body. Six prompted calls, no claim of spontaneous behavior or isolated word causation.'}
    assert result['source_pins_unchanged']
    dump(HERE/'RESULT.json',result)
    print(json.dumps({'status':'completed','new_model_calls':6,
        'final_files':{a:r['final_memory_file'] for a,r in all_results.items()}},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
