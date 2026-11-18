"""Conditional exact-input greedy and mechanics-only controls; no training."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,uuid,copy,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'prerequisite-calibration-v1'))
spec=importlib.util.spec_from_file_location('preserved_calibration_run',E/'prerequisite-calibration-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s;save=s.save;read=s.read
TASKS=['count','change','action']
SELF_OLD='Initial context contains FRR, these mechanics'
SELF_NEW='Initial context contains these mechanics'

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'prerequisite-calibration-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def prepare():
    old.guard();save(H/'PROTECTED_BEFORE.json',protected());frr=(E/'chosen-persistence-prototype-v1/FRR_COMPACT.md').read_text()
    pins=read(E/'prerequisite-calibration-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,max_model_calls=6,stage2_conditional=True,decoder='greedy_argmax',tensor_digest=read(E/'prerequisite-calibration-v1/CONTRACT.json')['tensor_digest']))
    seed=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for condition in ['full','mechanics']:
        for task in TASKS:
            d=H/(condition+'_'+task);d.mkdir();reference=read(E/'prerequisite-calibration-v1'/(task+'17')/'INITIAL_INPUT.json');ms=copy.deepcopy(reference['messages'])
            if condition=='mechanics':
                prefix=frr+'\n\n';assert ms[0]['content'].startswith(prefix)
                ms[0]['content']=ms[0]['content'][len(prefix):];assert ms[0]['content'].count(SELF_OLD)==1
                ms[0]['content']=ms[0]['content'].replace(SELF_OLD,SELF_NEW)
            ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
            if condition=='full':assert ids==reference['input_token_ids']
            w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
            try:
                before=w.world.checkpoint();save(d/'SETUP_INITIAL_SNAPSHOT.json',before)
                if task=='change':
                    w.complete('','operator_setup_tick');after=w.world.checkpoint();save(d/'SETUP_AFTER_SNAPSHOT.json',after)
                    assert old.observe(d,before,0,None)['material']==reference['observation']['before']['material']
                    assert old.observe(d,after,w.world.step,None)==reference['observation']['after']
                else:assert old.observe(d,before,0,None)==reference['observation']
            finally:w.close()
            save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,task=task,condition=condition,reference_input_sha256=s.sha(E/'prerequisite-calibration-v1'/(task+'17')/'INITIAL_INPUT.json'),observation=reference['observation'],operator_setup_ticks=reference['operator_setup_ticks']))
            save(d/'STATE.json',dict(model_calls=0,paused=True));pre.append(dict(branch=d.name,input_tokens=len(ids),operator_setup_ticks=reference['operator_setup_ticks']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',branches=pre,full_context_token_ids_exactly_match_previous=True,actual_operator_preparation_ticks=2,model_calls=0,protected_files=len(protected())));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run(stage):
    guard();assert stage in (1,2)
    condition='full' if stage==1 else 'mechanics'
    if stage==2:assert read(H/'STAGE1_REVIEW.json')['proceed_stage2']
    save(H/'RUN.lock',dict(stage=stage,pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for task in TASKS:
            guard();d=H/(condition+'_'+task);assert read(d/'STATE.json')['model_calls']==0;init=read(d/'INITIAL_INPUT.json')
            save(d/'PENDING.json',dict(stage='generation/effects unresolved; no replay'))
            raw=s.ref.body.generate(model,tok,init['messages'],resource,d.name);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
            w=s.a.MediumWorld.open(d/'world')
            try:rr=w.complete(raw['text'],'model_reply');bundle=w.world.checkpoint();step=w.world.step
            finally:w.close()
            save(d/'SNAPSHOT.json',bundle);save(d/'OBSERVATION.json',old.observe(d,bundle,step,1))
            save(d/'RECORD.json',dict(raw_sha256=s.sha(d/'RAW.json'),reply_sha256=s.sha(d/'world/replies/model_reply.json'),actor_operations=len(rr['actor_batch']['operations']),world_id=bundle['id'],world_step=step))
            s.a.base.atomic(d/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json');print(s.text(dict(branch=d.name,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=len(rr['actor_batch']['operations']))),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run(int(sys.argv[1]))
