"""One prospective additive native-preface control; parents remain frozen."""
from pathlib import Path
import sys,uuid
R=Path(__file__).resolve().parent;H=R.parent
sys.path.insert(0,str(H));import run as parent
s=parent.s;save=s.save;read=s.read

def parent_cases():
    return {str(p.relative_to(H)):s.sha(p) for name in ['native','full'] for p in (H/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    parent.guard();assert parent_cases()==read(R/'PARENT_CASES_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(R/'CONTRACT.json')['pins'].items())

def prepare():
    parent.guard();save(R/'PARENT_CASES_BEFORE.json',parent_cases())
    pins=read(H/'CONTRACT.json')['pins']|{str(R/n):s.sha(R/n) for n in ['run_role.py','PROTOCOL.md']}
    save(R/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=1,tensor_digest=read(H/'CONTRACT.json')['tensor_digest'],treatment='prepend native default system preface only'))
    native=read(H/'native/INITIAL_INPUT.json');full=read(H/'full/INITIAL_INPUT.json');rendered=native['rendered_chat'];prefix=rendered.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0]
    assert prefix=='You are a helpful AI assistant named SmolLM, trained by Hugging Face'
    ms=[{'role':'system','content':prefix+'\n\n'+full['messages'][0]['content']},dict(full['messages'][1])];tok=s.c.tokenizer();ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
    save(R/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,native_preface=prefix,rendered_chat=tok.apply_chat_template(ms,tokenize=False,add_generation_prompt=True)))
    seed=parent.E/'byte-medium-model-pilot-v1/seed';w=s.a.MediumWorld.create(R/'world',seed/'bundle.json',seed/'objects','changing')
    try:bundle=w.world.checkpoint();save(R/'INITIAL_SNAPSHOT.json',bundle)
    finally:w.close()
    assert bundle==read(H/'full/INITIAL_SNAPSHOT.json');save(R/'STATE.json',dict(model_calls=0,paused=True));guard();save(R/'PREFLIGHT.json',dict(status='pass',input_tokens=len(ids),parent_files_preserved=len(parent_cases()),model_calls=0));print(s.text(read(R/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(R/'RUN.lock',dict(pid=__import__('os').getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(R/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,R/'RESOURCE.jsonl');resource.read('loaded');init=read(R/'INITIAL_INPUT.json');save(R/'PENDING.json',dict(stage='generation/verification unresolved; no replay'))
        raw=s.ref.body.generate(model,tok,init['messages'],resource,'full_with_native_preface');save(R/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
        w=s.a.MediumWorld.open(R/'world')
        try:rr=w.complete(raw['text'],'operator_verification');bundle=w.world.checkpoint()
        finally:w.close()
        save(R/'SNAPSHOT.json',bundle);save(R/'VERIFICATION.json',dict(reply_sha256=s.sha(R/'world/replies/operator_verification.json'),complete_cells=len(rr['actor_batch']['operations']),actual_operator_executed_cells=bool(rr['actor_batch']['operations']),autonomous_action_claim=False))
        s.a.base.atomic(R/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(R/'PENDING.json');print(s.text(dict(output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actual_cells=len(rr['actor_batch']['operations']))),flush=True)
    except BaseException as error:
        import traceback
        save(R/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(R/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
