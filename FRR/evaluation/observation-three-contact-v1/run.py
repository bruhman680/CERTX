"""Declared three-stage new-world diagnostic. Observer decisions stay external."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import json,sys,uuid,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'byte-medium-decoding-v1'))
spec=importlib.util.spec_from_file_location('old_decoder_run',E/'byte-medium-decoding-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s
from sampling_stateful import generate,checks
save=s.save;read=s.read
BRANCHES=[('rle17','rle',17),('rle29','rle',29),('directory17','directory',17),('directory29','directory',29)]
OLD_SENSOR="field.bin bytes in hexadecimal when it is a regular file, including through a hardlink alias. This automatic byte observation is a supplied sensor; other files' contents require explicit access."
NEW_SENSOR={
 'rle':"field.bin bytes as lossless run-length pairs [byte_value,count] when it is a regular file, including through a hardlink alias. This automatic byte observation is a supplied sensor; other files' contents require explicit access.",
 'directory':"directory metadata and operation clocks. No file contents are automatically supplied; file contents are available through explicit access."}

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'byte-medium-decoding-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def runs(data):
    out=[]
    for value in data:
        if out and out[-1][0]==value:out[-1][1]+=1
        else:out.append([value,1])
    return out

def observe(d,bundle,step,clock,index,style):
    packet=s.observation(d,bundle,step,clock,index)
    if style=='directory':packet.pop('material')
    elif packet['material']['kind']=='regular':
        data=bytes.fromhex(packet['material'].pop('hex'));packet['material']['runs']=runs(data)
        assert bytes(v for value,count in packet['material']['runs'] for v in [value]*count)==data
    if len(s.text(packet).encode())>8192:raise RuntimeError('observation capacity; no partial packet')
    return packet

def prepare():
    old.guard();save(H/'PROTECTED_BEFORE.json',protected());save(H/'SAMPLER_CHECKS.json',checks())
    assert runs(b'\x01'+bytes(61))==[[1,1],[0,61]] and runs(b'')==[]
    for data in [b'abc',bytes(range(256)),b'\x00',b'aaaabbc']:
        assert bytes(v for value,count in runs(data) for v in [value]*count)==data
    pins=read(E/'byte-medium-decoding-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','sampling_stateful.py','PROTOCOL.md']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',branches=BRANCHES,budget=6,temperature=0.8,top_p=0.95,pins=pins,tensor_digest=read(E/'byte-medium-decoding-v1/CONTRACT.json')['tensor_digest']))
    original=read(E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json');tok=s.c.tokenizer();seed=E/'byte-medium-model-pilot-v1/seed';pre=[]
    assert original['messages'][0]['content'].count(OLD_SENSOR)==1
    for name,style,seed_id in BRANCHES:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:bundle=w.world.checkpoint();packet=observe(d,bundle,0,read(d/'world/STATE.json'),None,style)
        finally:w.close()
        ms=[{'role':'system','content':original['messages'][0]['content'].replace(OLD_SENSOR,NEW_SENSOR[style])},{'role':'user','content':s.text(packet)}]
        assert ms[0]['content'].replace(NEW_SENSOR[style],OLD_SENSOR)==original['messages'][0]['content']
        ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,observation=packet,style=style,seed=seed_id))
        save(d/'STATE.json',dict(turn=0,paused=True,last_record_sha256=None))
        pre.append(dict(branch=name,input_tokens=len(ids),observation_bytes=len(s.text(packet).encode()),world_id=bundle['id']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',branches=pre,protected_files=len(protected()),model_calls=0,lossless_cases_checked=6))
    print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def history(d):
    ms=read(d/'INITIAL_INPUT.json')['messages']
    for n in range(1,read(d/'STATE.json')['turn']+1):
        rec=read(d/'records'/f'{n:06d}.json');ms=ms+[{'role':'assistant','content':rec['text']},{'role':'user','content':rec['feedback']}]
    return ms

def selection():
    for name,style,seed in BRANCHES:
        d=H/name
        if read(d/'records/000001.json')['actor_operations']>0:return name
    return 'rle17'

def run(stage):
    guard();assert stage in (1,2,3)
    if stage==1:targets=[('rle17',1),('rle29',1)]
    elif stage==2:
        assert (H/'STAGE1_REVIEW.json').exists();targets=[('directory17',1),('directory29',1)]
    else:
        assert (H/'STAGE2_REVIEW.json').exists();chosen=selection();save(H/'STAGE3_SELECTION.json',dict(branch=chosen,rule='first acted in declared order, otherwise rle17',adaptive=True));targets=[(chosen,2)]
    save(H/'RUN.lock',dict(pid=os.getpid(),stage=stage))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==expected;resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name,count in targets:
            d=H/name;initial=read(d/'INITIAL_INPUT.json');style,seed=initial['style'],initial['seed']
            assert read(d/'STATE.json')['turn']==(1 if stage==3 else 0)
            for _ in range(count):
                guard();state=read(d/'STATE.json');n=state['turn']+1;label=f'{n:06d}';ms=history(d);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
                if len(ids)>7936:raise RuntimeError('input capacity; no pruning')
                rng=None if n==1 else read(d/'raw'/f'{n-1:06d}.json')['rng_state_after']
                save(d/'PENDING.json',dict(turn=n,stage='generation/effects unresolved; no replay'))
                raw=generate(model,tok,ms,resource,name+'_'+label,seed,rng_state=rng);save(d/'raw'/(label+'.json'),raw)
                assert raw['input_token_ids']==ids
                w=s.a.MediumWorld.open(d/'world')
                try:rr=w.complete(raw['text'],'reply_'+label);bundle=w.world.checkpoint();step=w.world.step
                finally:w.close()
                save(d/'snapshots'/(label+'.json'),bundle);packet=observe(d,bundle,step,read(d/'world/STATE.json'),n,style)
                feedback=s.text(dict(actor_feedback={'boundary':rr['actor_batch']['boundary'],'receipts':[op['receipt'] for op in rr['actor_batch']['operations']]},physical_feedback=rr['physical_tick']['receipt'],**packet))
                if len(feedback.encode())>8192:raise RuntimeError('feedback capacity; known effects retained')
                rec=dict(turn=n,text=raw['text'],feedback=feedback,raw_sha256=s.sha(d/'raw'/(label+'.json')),adapter_reply_sha256=s.sha(d/'world/replies'/('reply_'+label+'.json')),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],parent_record_sha256=state['last_record_sha256'])
                save(d/'records'/(label+'.json'),rec);s.a.base.atomic(d/'STATE.json',dict(turn=n,paused=True,last_record_sha256=s.sha(d/'records'/(label+'.json'))))
                assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json')
                print(s.text(dict(stage=stage,branch=name,turn=n,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=rec['actor_operations'])),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run(int(sys.argv[1]))
