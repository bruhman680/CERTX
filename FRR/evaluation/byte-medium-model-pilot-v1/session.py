"""Small matched world-package pilot; no training, repair, or hidden feedback."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,copy,importlib.util,hashlib,uuid
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'byte-medium-execution-v1'))
import adapter as a
spec=importlib.util.spec_from_file_location('preserved_chosen_session',E/'chosen-persistence-prototype-v1/session.py');ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
c=ref.c
save=a.base.immutable;read=a.base.read

def text(value):return json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def inventory():
    return {str(p.relative_to(E.parent)):sha(p) for root in [E/'chosen-persistence-prototype-v1',E/'bounded-main-continuation-v1',E.parent/'ACTIVE_GARDEN_PHASE.json'] for p in (root.rglob('*') if root.is_dir() else [root]) if p.is_file() and '__pycache__' not in p.parts}
def source_pins():
    paths=[H/'session.py',H/'PROTOCOL.md',H/'LAWS_COMMON.txt',H/'STATIC_LAW.txt',H/'CHANGING_LAW.txt',E/'byte-medium-execution-v1/adapter.py']
    return ref.pins() | {str(p):sha(p) for p in paths}
def guard():
    contract=read(H/'CONTRACT.json')
    assert inventory()==read(H/'PROTECTED_BEFORE.json')
    assert all(sha(p)==v for p,v in contract['pins'].items())

def observation(d,bundle,engine_step,clock,index):
    directory=ref.make_snapshot(bundle,timing='initial' if index is None else 'after_reply',world_step=engine_step,reply_index=index,max_packet_bytes=8192)
    rows={r[0]:r for r in bundle['entries']};row=rows.get('field.bin')
    if row is None:material={'kind':'absent'}
    else:
        if row[1]=='hardlink':row=rows[row[2]]
        if row[1]=='file':
            obj=read(d/'world/world/engine/objects'/(row[3]+'.json'))
            import base64
            data=base64.b64decode(obj['base64'],validate=True)
            material={'kind':'regular','bytes':len(data),'hex':data.hex()}
        else:material={'kind':row[1]}
    packet={'world_observation':directory.model_packet['world_snapshot'],'material':material,'clock':clock}
    if len(text(packet).encode())>8192:raise RuntimeError('observation capacity; do not emit partial packet')
    return packet

def history(d):
    ms=copy.deepcopy(read(d/'INITIAL_INPUT.json')['messages'])
    for n in range(1,read(d/'STATE.json')['turn']+1):
        r=read(d/'records'/f'{n:06d}.json');ms.extend([{'role':'assistant','content':r['text']},{'role':'user','content':r['feedback']}])
    return ms

def prepare():
    assert not (H/'CONTRACT.json').exists()
    assert read(E/'byte-medium-execution-v1/RESULTS.json')['checks_passed']==16
    save(H/'PROTECTED_BEFORE.json',inventory())
    save(H/'CONTRACT.json',dict(identity='fresh detached alternate worlds, not continuation',date='2026-11-17 America/Chicago',body='SmolLM2-135M-Instruct cached CPUfloat32 eager 2threads greedy256 fixedweights',tensor_digest=read(c.C/'run/MANIFEST.json')['tensor_digest'],pins=source_pins(),budget_per_condition=3,condition_order=['static','changing'],history='full native-role context; no pruning',max_input=7936,max_packet_bytes=8192,FRR_sha256=sha(E/'chosen-persistence-prototype-v1/FRR_COMPACT.md')))
    seed=H/'seed';(seed/'objects').mkdir(parents=True)
    raw=bytes([1,0])+bytes(60);s=a.base._runtime.sha(raw)
    import base64
    save(seed/'objects'/(s+'.json'),dict(sha256=s,bytes=len(raw),base64=base64.b64encode(raw).decode()))
    payload={'entries':[['field.bin','file',0o644,s,len(raw)]],'root_mode':0o755};bundle=dict(payload,id=a.base._runtime.sha(a.base._runtime.stable(payload)));save(seed/'bundle.json',bundle)
    initial=[];tok=c.tokenizer()
    for mode in ['static','changing']:
        d=H/mode;d.mkdir();w=a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects',mode)
        try:obs=observation(d,w.world.checkpoint(),0,read(d/'world/STATE.json'),None)
        finally:w.close()
        system=(E/'chosen-persistence-prototype-v1/FRR_COMPACT.md').read_text()+'\n\n'+(H/'LAWS_COMMON.txt').read_text()+'\n'+(H/(mode.upper()+'_LAW.txt')).read_text()
        ms=[{'role':'system','content':system},{'role':'user','content':text(obs)}];ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
        assert len(ids)<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,observation=obs))
        save(d/'STATE.json',dict(turn=0,paused=True,stop_reason=None,last_record_sha256=None))
        initial.append(dict(mode=mode,input_tokens=len(ids),observation_bytes=len(text(obs).encode()),world_id=bundle['id']))
    assert read(H/'static/INITIAL_INPUT.json')['observation']==read(H/'changing/INITIAL_INPUT.json')['observation']
    guard();save(H/'PREFLIGHT.json',dict(status='pass',initial=initial,initial_material_and_observation_matched=True,model_calls=0,protected_files=len(inventory())))
    print(text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();assert not (H/'RUN.lock').exists();save(H/'RUN.lock',{'pid':os.getpid()})
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for mode in ['static','changing']:
            d=H/mode
            assert not (d/'PENDING.json').exists()
            while read(d/'STATE.json')['turn']<3:
                guard();old=read(d/'STATE.json');assert old['stop_reason'] is None
                n=old['turn']+1;label=f'{n:06d}';ms=history(d);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
                if len(ids)>7936:raise RuntimeError('input capacity before generation')
                save(d/'PENDING.json',dict(turn=n,stage='generation/effects unresolved; no automatic replay'))
                save(d/'plans'/(label+'.json'),dict(messages=ms,input_token_ids=ids))
                raw=ref.body.generate(model,tok,ms,resource,mode+'_'+label);save(d/'raw'/(label+'.json'),raw)
                w=a.MediumWorld.open(d/'world')
                try:
                    record=w.complete(raw['text'],'reply_'+label);bundle=w.world.checkpoint();step=w.world.step
                finally:w.close()
                save(d/'snapshots'/(label+'.json'),bundle)
                obs=observation(d,bundle,step,read(d/'world/STATE.json'),n)
                feedback=text(dict(actor_feedback={'boundary':record['actor_batch']['boundary'],'receipts':[op['receipt'] for op in record['actor_batch']['operations']]},physical_feedback=record['physical_tick']['receipt'],**obs))
                if len(feedback.encode())>8192:raise RuntimeError('feedback capacity after retained known effects')
                r=dict(turn=n,text=raw['text'],feedback=feedback,input_tokens=len(ids),output_tokens=len(raw['generated_token_ids']),raw_sha256=sha(d/'raw'/(label+'.json')),parent_record_sha256=old['last_record_sha256'],actor_operations=len(record['actor_batch']['operations']),world_id=bundle['id'],world_step=step)
                save(d/'records'/(label+'.json'),r)
                a.base.atomic(d/'STATE.json',dict(turn=n,paused=True,stop_reason=None,last_record_sha256=sha(d/'records'/(label+'.json'))))
                assert parameter_digest(model,False)==expected;guard();a.c.unlink_durable(d/'PENDING.json')
                print(text(dict(condition=mode,turn=n,input_tokens=len(ids),output_tokens=r['output_tokens'],actor_operations=r['actor_operations'],world_step=step)),flush=True)
        assert parameter_digest(model,False)==expected;guard()
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:
        a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='run':run()
