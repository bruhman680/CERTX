"""Prospective matched invitation contact; old universes remain untouched."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,uuid,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'observation-three-contact-v1'))
spec=importlib.util.spec_from_file_location('preserved_observation_run',E/'observation-three-contact-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s
import sensor_v2 as sensor
BRANCHES=[('observation17',False,17),('invitation17',True,17),('observation29',False,29),('invitation29',True,29)]
save=s.save;read=s.read

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'observation-three-contact-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def observe(d,bundle,step,clock,index):
    directory=s.ref.make_snapshot(bundle,timing='initial' if index is None else 'after_reply',world_step=step,reply_index=index,max_packet_bytes=8192).model_packet['world_snapshot']
    return sensor.packet(bundle,d/'world/world/engine/objects',directory,clock,'rle',max_bytes=8192)

def prepare():
    old.guard();assert read(E/'observation-three-contact-v1/SENSOR_V2_CHECKS.json')['status']=='pass'
    save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'observation-three-contact-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md','INVITATION.txt']}|{str(E/'observation-three-contact-v1/sensor_v2.py'):s.sha(E/'observation-three-contact-v1/sensor_v2.py')}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',identity='fresh matched invitation/observation diagnostic; no prior continuation/reset',budget=8,replies_per_branch=2,branches=BRANCHES,pins=pins,tensor_digest=read(E/'observation-three-contact-v1/CONTRACT.json')['tensor_digest'],sensor='directly bounded v2 pinned for both conditions',temperature=0.8,top_p=0.95))
    initial=read(E/'observation-three-contact-v1/rle17/INITIAL_INPUT.json');tok=s.c.tokenizer();seed=E/'byte-medium-model-pilot-v1/seed';pre=[]
    for name,invited,seed_id in BRANCHES:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:bundle=w.world.checkpoint();packet=observe(d,bundle,0,read(d/'world/STATE.json'),None)
        finally:w.close()
        assert packet==initial['observation']
        ms=[{'role':'system','content':initial['messages'][0]['content']},{'role':'user','content':s.text(packet)+('\n\n'+(H/'INVITATION.txt').read_text().strip() if invited else '')}]
        if not invited:assert ms==initial['messages']
        ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,observation=packet,invited=invited,seed=seed_id));save(d/'STATE.json',dict(turn=0,paused=True,last_record_sha256=None))
        pre.append(dict(branch=name,input_tokens=len(ids),observation_bytes=len(s.text(packet).encode()),world_id=bundle['id']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',branches=pre,baseline_exact_prior_context=True,all_initial_worlds_and_observations_matched=True,only_arm_message_difference='appended invitation',protected_files=len(protected()),model_calls=0))
    print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def history(d):
    ms=read(d/'INITIAL_INPUT.json')['messages']
    for n in range(1,read(d/'STATE.json')['turn']+1):
        rec=read(d/'records'/f'{n:06d}.json');ms=ms+[{'role':'assistant','content':rec['text']},{'role':'user','content':rec['feedback']}]
    return ms

def run():
    guard();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==expected;resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name,invited,seed in BRANCHES:
            d=H/name;assert read(d/'STATE.json')['turn']==0
            for _ in range(2):
                guard();state=read(d/'STATE.json');n=state['turn']+1;label=f'{n:06d}';ms=history(d);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
                if len(ids)>7936:raise RuntimeError('context capacity; no pruning')
                rng=None if n==1 else read(d/'raw'/f'{n-1:06d}.json')['rng_state_after']
                save(d/'PENDING.json',dict(turn=n,stage='generation/effects unresolved; never replay automatically'))
                raw=old.generate(model,tok,ms,resource,name+'_'+label,seed,rng_state=rng);save(d/'raw'/(label+'.json'),raw);assert raw['input_token_ids']==ids
                w=s.a.MediumWorld.open(d/'world')
                try:rr=w.complete(raw['text'],'reply_'+label);bundle=w.world.checkpoint();step=w.world.step
                finally:w.close()
                save(d/'snapshots'/(label+'.json'),bundle);packet=observe(d,bundle,step,read(d/'world/STATE.json'),n)
                feedback=s.text(dict(actor_feedback={'boundary':rr['actor_batch']['boundary'],'receipts':[op['receipt'] for op in rr['actor_batch']['operations']]},physical_feedback=rr['physical_tick']['receipt'],**packet))
                if len(feedback.encode())>8192:raise RuntimeError('feedback capacity; retain known effects')
                rec=dict(turn=n,text=raw['text'],feedback=feedback,raw_sha256=s.sha(d/'raw'/(label+'.json')),adapter_reply_sha256=s.sha(d/'world/replies'/('reply_'+label+'.json')),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],parent_record_sha256=state['last_record_sha256'])
                save(d/'records'/(label+'.json'),rec);s.a.base.atomic(d/'STATE.json',dict(turn=n,paused=True,last_record_sha256=s.sha(d/'records'/(label+'.json'))))
                assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json')
                print(s.text(dict(branch=name,turn=n,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=rec['actor_operations'])),flush=True)
        assert parameter_digest(model,False)==expected;guard()
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
