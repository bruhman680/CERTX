"""Four single-factor conditional probes; original histories remain frozen."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,uuid,copy,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'decoder-context-controls-v1'))
spec=importlib.util.spec_from_file_location('preserved_decoder_controls',E/'decoder-context-controls-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s;save=s.save;read=s.read
CASES=[('rle_change','change',False),('array_change','change',True),('general_action','action',False),('python_action','action',True)]
SENSOR_OLD='field.bin bytes as lossless run-length pairs [byte_value,count]'
SENSOR_NEW='field.bin bytes as an ordered list of unsigned byte values'
ACTION='Use an executable Python cell to create a file named note.txt containing a short observation about field.bin.'

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'decoder-context-controls-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def array_packet(packet):
    out=copy.deepcopy(packet)
    if out['material']['kind']=='regular':
        runs=out['material'].pop('runs');data=[v for v,count in runs for _ in range(count)]
        assert len(data)==out['material']['bytes'] and all(type(v) is int and 0<=v<256 for v in data)
        out['material']['values']=data
    return out

def prepare():
    old.guard();save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'decoder-context-controls-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=4,decoder='greedy_argmax',cases=CASES,tensor_digest=read(E/'decoder-context-controls-v1/CONTRACT.json')['tensor_digest']))
    seed=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for name,task,treatment in CASES:
        d=H/name;d.mkdir();ref=read(E/'decoder-context-controls-v1'/('full_'+task)/'INITIAL_INPUT.json');ms=copy.deepcopy(ref['messages']);obs=copy.deepcopy(ref['observation'])
        w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:
            before=w.world.checkpoint();save(d/'SETUP_INITIAL_SNAPSHOT.json',before)
            if task=='change':
                w.complete('','operator_setup_tick');after=w.world.checkpoint();save(d/'SETUP_AFTER_SNAPSHOT.json',after)
                # Pure historical observations use their own clocks, not the live final state.
                pure=old.old.old.old.observe
                assert pure(d,before,0,dict(replies=0,ticks=0,actor_operations=0),None)==obs['before']
                assert pure(d,after,1,dict(replies=1,ticks=1,actor_operations=0),None)==obs['after']
            else:assert old.old.observe(d,before,0,None)==obs
        finally:w.close()
        if name=='array_change':
            assert ms[0]['content'].count(SENSOR_OLD)==1
            ms[0]['content']=ms[0]['content'].replace(SENSOR_OLD,SENSOR_NEW)
            obs={label:array_packet(packet) for label,packet in obs.items()}
            suffix=ref['messages'][1]['content'][len(s.text(ref['observation'])):]
            ms[1]['content']=s.text(obs)+suffix
        elif name=='python_action':
            old_question=old.old.QUESTIONS['action'];assert ms[1]['content'].endswith(old_question)
            ms[1]['content']=ms[1]['content'][:-len(old_question)]+ACTION
        ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936 and len(s.text(obs).encode())<=8192
        if not treatment:assert ids==ref['input_token_ids']
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,observation=obs,task=task,treatment=treatment,operator_setup_ticks=int(task=='change')));save(d/'STATE.json',dict(model_calls=0,paused=True))
        pre.append(dict(branch=name,input_tokens=len(ids),observation_bytes=len(s.text(obs).encode()),operator_setup_ticks=int(task=='change')))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',branches=pre,exact_baseline_inputs=True,lossless_array_transform=True,actual_operator_setup_ticks=2,protected_files=len(protected()),model_calls=0));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name,task,treatment in CASES:
            guard();d=H/name;assert read(d/'STATE.json')['model_calls']==0;init=read(d/'INITIAL_INPUT.json')
            save(d/'PENDING.json',dict(stage='generation/effects unresolved; no automatic replay'))
            raw=s.ref.body.generate(model,tok,init['messages'],resource,name);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
            w=s.a.MediumWorld.open(d/'world')
            try:rr=w.complete(raw['text'],'model_reply');bundle=w.world.checkpoint();step=w.world.step
            finally:w.close()
            save(d/'SNAPSHOT.json',bundle);clock=read(d/'world/STATE.json');pure=old.old.old.old.observe
            packet=pure(d,bundle,step,clock,1)
            if name=='array_change':packet=array_packet(packet)
            if len(s.text(packet).encode())>8192:raise RuntimeError('observation capacity; known effects retained')
            save(d/'OBSERVATION.json',packet);save(d/'RECORD.json',dict(raw_sha256=s.sha(d/'RAW.json'),reply_sha256=s.sha(d/'world/replies/model_reply.json'),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],world_step=step))
            s.a.base.atomic(d/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json')
            print(s.text(dict(branch=name,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=len(rr['actor_batch']['operations']))),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
