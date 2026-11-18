"""One frozen continuation-length control, fresh generation and verification."""
from pathlib import Path
import sys,uuid,importlib.util
B=Path(__file__).resolve().parent;N=B.parent
sys.path.insert(0,str(N));import run_native as native
s=native.s;save=s.save;read=s.read
spec=importlib.util.spec_from_file_location('native_fixed_body512',B/'body512.py');body=importlib.util.module_from_spec(spec);spec.loader.exec_module(body)

def inventory():
    return {str(p.relative_to(N)):s.sha(p) for name in ['comparison','code'] for p in (N/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    native.guard();assert inventory()==read(B/'NATIVE_CASES_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(B/'CONTRACT.json')['pins'].items())

def prepare():
    native.guard();save(B/'NATIVE_CASES_BEFORE.json',inventory())
    pins=read(N/'CONTRACT.json')['pins']|{str(B/n):s.sha(B/n) for n in ['run512.py','body512.py','PROTOCOL.md']}
    save(B/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',budget=1,max_output_tokens=512,pins=pins,tensor_digest=read(N/'CONTRACT.json')['tensor_digest']))
    init=read(N/'code/INITIAL_INPUT.json');assert len(init['input_token_ids'])+512<=8192;save(B/'INITIAL_INPUT.json',init)
    seed=native.parent.E/'byte-medium-model-pilot-v1/seed';w=s.a.MediumWorld.create(B/'verification_world',seed/'bundle.json',seed/'objects','changing');w.close()
    save(B/'STATE.json',dict(model_calls=0,paused=True));guard()

def run():
    guard();save(B/'RUN.lock',dict(pid=__import__('os').getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(B/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,B/'RESOURCE.jsonl');resource.read('loaded');init=read(B/'INITIAL_INPUT.json');save(B/'PENDING.json',dict(stage='generation/verification unresolved; no replay'))
        raw=body.generate(model,tok,init['messages'],resource,'native_code_512');save(B/'RAW.json',raw)
        assert raw['input_token_ids']==init['input_token_ids'];old=read(N/'code/RAW.json');assert old['stop']=='token_limit' and len(old['generated_token_ids'])==256
        assert raw['generated_token_ids'][:256]==old['generated_token_ids'];save(B/'PREFIX_CHECK.json',dict(status='pass',shared_generated_prefix_tokens=256,new_model_calls=1))
        w=s.a.MediumWorld.open(B/'verification_world')
        try:rr=w.complete(raw['text'],'operator_code_verification');bundle=w.world.checkpoint()
        finally:w.close()
        save(B/'SNAPSHOT.json',bundle);save(B/'VERIFICATION.json',dict(reply_sha256=s.sha(B/'verification_world/replies/operator_code_verification.json'),actor_cells=len(rr['actor_batch']['operations']),operator_generated_cells_executed=bool(rr['actor_batch']['operations']),autonomous_model_action=False))
        s.a.base.atomic(B/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(B/'PENDING.json');print(s.text(dict(output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],complete_cells=len(rr['actor_batch']['operations']))),flush=True)
    except BaseException as e:
        import traceback
        save(B/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(B/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
