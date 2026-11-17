"""Frozen paired object-reference and sibling evidence-followup diagnostic."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,uuid,shutil,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'invitation-interaction-v1'))
spec=importlib.util.spec_from_file_location('preserved_invitation_run',E/'invitation-interaction-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s
from receipt_view import model_receipt
AMBIGUOUS='What, if anything, can you discover about this material?'
NAMED='What, if anything, can you discover about the bytes in field.bin?'
FOLLOWUP='Which observations support or challenge what you just said?'
DISCLOSURE='Wrapper-measured elapsed seconds are not included in supplied process receipts. Complete raw receipts remain in the external records.'
BRANCHES=[('ambiguous17',AMBIGUOUS,17),('named17',NAMED,17),('ambiguous29',AMBIGUOUS,29),('named29',NAMED,29)]
save=s.save;read=s.read

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'invitation-interaction-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def initial_plan(d):return read(d/'INITIAL_INPUT.json')

def feedback(d,bundle,step,index,reply):
    packet=old.observe(d,bundle,step,read(d/'world/STATE.json'),index)
    out=s.text(dict(actor_feedback={'boundary':reply['actor_batch']['boundary'],'receipts':[model_receipt(op['receipt']) for op in reply['actor_batch']['operations']]},physical_feedback=model_receipt(reply['physical_tick']['receipt']),**packet))
    if len(out.encode())>8192:raise RuntimeError('feedback capacity; no partial packet')
    return out

def messages(d):
    ms=initial_plan(d)['messages']
    for n in range(1,read(d/'STATE.json')['turn']+1):
        rec=read(d/'records'/f'{n:06d}.json');user=rec['feedback']
        if n==1 and (d/'FORK.json').exists() and read(d/'FORK.json')['question']:user+='\n\n'+FOLLOWUP
        ms=ms+[{'role':'assistant','content':rec['text']},{'role':'user','content':user}]
    return ms

def prepare():
    old.guard();assert read(E/'invitation-interaction-v1/RECEIPT_VIEW_CHECKS.json')['status']=='pass'
    save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'invitation-interaction-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md']}|{str(E/'invitation-interaction-v1/receipt_view.py'):s.sha(E/'invitation-interaction-v1/receipt_view.py')}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=8,branches=BRANCHES,followup=FOLLOWUP,receipt_policy='four fields, raw seconds external only',tensor_digest=read(E/'invitation-interaction-v1/CONTRACT.json')['tensor_digest']))
    prior=read(E/'observation-three-contact-v1/rle17/INITIAL_INPUT.json');seed=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for name,question,seed_id in BRANCHES:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:bundle=w.world.checkpoint();packet=old.observe(d,bundle,0,read(d/'world/STATE.json'),None)
        finally:w.close()
        assert packet==prior['observation']
        ms=[{'role':'system','content':prior['messages'][0]['content']+'\n\n'+DISCLOSURE},{'role':'user','content':s.text(packet)+'\n\n'+question}]
        ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,question=question,seed=seed_id,observation=packet));save(d/'STATE.json',dict(turn=0,paused=True,last_record_sha256=None))
        pre.append(dict(branch=name,input_tokens=len(ids),observation_bytes=len(s.text(packet).encode()),world_id=bundle['id']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',branches=pre,model_calls=0,protected_files=len(protected()),receipt_view_activated=True,initial_physics_and_observations_matched=True));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def fork():
    guard();assert (H/'STAGE1_REVIEW.json').exists();plans=[]
    for seed in [17,29]:
        source=H/('named'+str(seed));assert read(source/'STATE.json')['turn']==1
        for name,question in [('silent',False),('question',True)]:
            dest=H/(source.name+'_'+name)
            assert not (source/'PENDING.json').exists() and not (source/'world/PENDING.json').exists() and not (source/'world/world/engine/LOCK.json').exists()
            shutil.copytree(source,dest)
            marker=dict(source=str(source),question=question,inherited_model_calls=1,new_model_calls=0,source_first_raw_sha256=s.sha(source/'raw/000001.json'),source_first_record_sha256=s.sha(source/'records/000001.json'),source_world_state_sha256=s.sha(source/'world/STATE.json'),seed=seed)
            save(dest/'FORK.json',marker)
            assert read(dest/'world/STATE.json')==read(source/'world/STATE.json')
            assert s.a.c.verify(dest/'world/world')['bundle_id']==s.a.c.verify(source/'world/world')['bundle_id']
            plans.append(dict(branch=dest.name,source=source.name,question=question))
        a=H/(source.name+'_silent');b=H/(source.name+'_question');aa=messages(a);bb=messages(b)
        assert aa[:-1]==bb[:-1] and bb[-1]['content']==aa[-1]['content']+'\n\n'+FOLLOWUP
        assert read(a/'raw/000001.json')['rng_state_after']==read(b/'raw/000001.json')['rng_state_after']
    save(H/'FORK_PREFLIGHT.json',dict(status='pass',plans=plans,new_model_calls=0,paired_history_world_rng_matched=True));guard()

def run(stage):
    guard()
    targets=[name for name,q,seed in BRANCHES] if stage==1 else ['named17_silent','named17_question','named29_silent','named29_question']
    assert stage in (1,2)
    if stage==2:assert read(H/'FORK_PREFLIGHT.json')['status']=='pass'
    save(H/'RUN.lock',dict(stage=stage,pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name in targets:
            guard();d=H/name;state=read(d/'STATE.json');assert state['turn']==(0 if stage==1 else 1)
            n=state['turn']+1;label=f'{n:06d}';ms=messages(d);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            if len(ids)>7936:raise RuntimeError('context capacity; no pruning')
            rng=None if n==1 else read(d/'raw/000001.json')['rng_state_after'];seed=initial_plan(d)['seed']
            save(d/'PENDING.json',dict(turn=n,stage='generation/effects unresolved; no replay'))
            save(d/'plans'/(label+'.json'),dict(messages=ms,input_token_ids=ids,rng_state_before_sha256=None if rng is None else s.a.fingerprint(s.text(rng))))
            raw=old.old.generate(model,tok,ms,resource,name+'_'+label,seed,rng_state=rng);save(d/'raw'/(label+'.json'),raw);assert raw['input_token_ids']==ids
            w=s.a.MediumWorld.open(d/'world')
            try:rr=w.complete(raw['text'],'reply_'+label);bundle=w.world.checkpoint();step=w.world.step
            finally:w.close()
            save(d/'snapshots'/(label+'.json'),bundle);fb=feedback(d,bundle,step,n,rr)
            rec=dict(turn=n,text=raw['text'],feedback=fb,raw_sha256=s.sha(d/'raw'/(label+'.json')),adapter_reply_sha256=s.sha(d/'world/replies'/('reply_'+label+'.json')),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],parent_record_sha256=state['last_record_sha256'])
            save(d/'records'/(label+'.json'),rec);s.a.base.atomic(d/'STATE.json',dict(turn=n,paused=True,last_record_sha256=s.sha(d/'records'/(label+'.json'))))
            assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json');print(s.text(dict(stage=stage,branch=name,turn=n,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=rec['actor_operations'])),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='fork':fork()
    else:run(int(sys.argv[1]))
