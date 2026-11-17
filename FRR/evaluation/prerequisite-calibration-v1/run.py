"""Six separate conditional capability probes, no coaching/training."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,uuid,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'object-evidence-contact-v1'))
spec=importlib.util.spec_from_file_location('preserved_object_run',E/'object-evidence-contact-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s;save=s.save;read=s.read
QUESTIONS={'count':'How many bytes are currently in field.bin?','change':'Between these two observations, what changed in the bytes of field.bin?','action':'Create a file named note.txt containing a short observation about field.bin.'}
BRANCHES=[(task+str(seed),task,seed) for seed in [17,29] for task in ['count','change','action']]

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'object-evidence-contact-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def observe(d,bundle,step,index):return old.old.observe(d,bundle,step,read(d/'world/STATE.json'),index)

def prepare():
    old.guard();save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'object-evidence-contact-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,branches=BRANCHES,questions=QUESTIONS,budget=6,tensor_digest=read(E/'object-evidence-contact-v1/CONTRACT.json')['tensor_digest']))
    system=read(E/'object-evidence-contact-v1/named17/INITIAL_INPUT.json')['messages'][0]['content'];seed_root=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for name,task,seed in BRANCHES:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed_root/'bundle.json',seed_root/'objects','changing')
        try:
            before=w.world.checkpoint();first=observe(d,before,0,None);save(d/'SETUP_INITIAL_SNAPSHOT.json',before)
            if task=='change':
                rr=w.complete('','operator_setup_tick');after=w.world.checkpoint();last=observe(d,after,w.world.step,None)
                save(d/'SETUP_AFTER_SNAPSHOT.json',after)
                user=s.text(dict(before=first,after=last))+'\n\nThe after observation follows one actual operator preparation tick; no model action preceded it.\n\n'+QUESTIONS[task]
            else:user=s.text(first)+'\n\n'+QUESTIONS[task];after=before
            packet=first if task!='change' else dict(before=first,after=last)
        finally:w.close()
        ms=[{'role':'system','content':system},{'role':'user','content':user}];ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936 and len(s.text(packet).encode())<=8192
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,task=task,seed=seed,observation=packet,setup_model_calls=0,operator_setup_ticks=1 if task=='change' else 0))
        save(d/'STATE.json',dict(model_calls=0,paused=True));pre.append(dict(branch=name,input_tokens=len(ids),operator_setup_ticks=1 if task=='change' else 0,world_id=after['id']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',model_calls=0,actual_operator_setup_ticks=2,branches=pre,protected_files=len(protected())));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name,task,seed in BRANCHES:
            guard();d=H/name;assert read(d/'STATE.json')['model_calls']==0;init=read(d/'INITIAL_INPUT.json')
            save(d/'PENDING.json',dict(stage='generation/effects unresolved; no automatic replay'))
            raw=old.old.old.generate(model,tok,init['messages'],resource,name,seed);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
            w=s.a.MediumWorld.open(d/'world')
            try:rr=w.complete(raw['text'],'model_reply');bundle=w.world.checkpoint();step=w.world.step
            finally:w.close()
            save(d/'SNAPSHOT.json',bundle);save(d/'OBSERVATION.json',observe(d,bundle,step,1))
            save(d/'RECORD.json',dict(raw_sha256=s.sha(d/'RAW.json'),reply_sha256=s.sha(d/'world/replies/model_reply.json'),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],world_step=step))
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
