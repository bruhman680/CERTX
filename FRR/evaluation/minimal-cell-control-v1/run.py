"""Two matched-outcome minimal code handoff probes, no training or source repair."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,uuid,importlib.util
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'representation-actuator-controls-v1'))
spec=importlib.util.spec_from_file_location('preserved_bridge_run',E/'representation-actuator-controls-v1/run.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=old.s;save=s.save;read=s.read
QUESTION='Produce one complete executable Python cell that prints the digit 1.'

def protected():
    return old.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'representation-actuator-controls-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def prepare():
    old.guard();save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'representation-actuator-controls-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','PROTOCOL.md']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=2,question=QUESTION,tensor_digest=read(E/'representation-actuator-controls-v1/CONTRACT.json')['tensor_digest'],decoder='greedy_argmax',max_output_tokens=256))
    ref=read(E/'representation-actuator-controls-v1/general_action/INITIAL_INPUT.json');seed=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for name in ['native','full']:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:bundle=w.world.checkpoint();save(d/'INITIAL_SNAPSHOT.json',bundle)
        finally:w.close()
        if name=='native':ms=[{'role':'user','content':QUESTION}]
        else:ms=[ref['messages'][0],{'role':'user','content':s.text(ref['observation'])+'\n\n'+QUESTION}]
        ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        rendered=tok.apply_chat_template(ms,tokenize=False,add_generation_prompt=True)
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,rendered_chat=rendered,actual_seed_world_id=bundle['id']));save(d/'STATE.json',dict(model_calls=0,paused=True));pre.append(dict(context=name,input_tokens=len(ids),world_id=bundle['id']))
    assert pre[0]['world_id']==pre[1]['world_id'];guard();save(H/'PREFLIGHT.json',dict(status='pass',initial_worlds_identical=True,branches=pre,model_calls=0,protected_files=len(protected())));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name in ['native','full']:
            guard();d=H/name;assert read(d/'STATE.json')['model_calls']==0;init=read(d/'INITIAL_INPUT.json');save(d/'PENDING.json',dict(stage='generation/verification unresolved; no replay'))
            raw=s.ref.body.generate(model,tok,init['messages'],resource,'minimal_cell_'+name);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
            w=s.a.MediumWorld.open(d/'world')
            try:rr=w.complete(raw['text'],'operator_verification');bundle=w.world.checkpoint()
            finally:w.close()
            save(d/'SNAPSHOT.json',bundle);save(d/'VERIFICATION.json',dict(reply_sha256=s.sha(d/'world/replies/operator_verification.json'),complete_cells=len(rr['actor_batch']['operations']),actual_operator_executed_cells=bool(rr['actor_batch']['operations']),autonomous_action_claim=False))
            s.a.base.atomic(d/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json');print(s.text(dict(context=name,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actual_cells=len(rr['actor_batch']['operations']))),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
