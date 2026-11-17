"""Three frozen, one-shot branches; all analysis external to world feedback."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,uuid,traceback
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'byte-medium-model-pilot-v1'))
import session as s
from sampling import generate,checks
save=s.save;read=s.read
CONFIGS=[dict(name='greedy',decoder='greedy_argmax',seed=None),dict(name='sample17',decoder='nucleus_multinomial',seed=17),dict(name='sample29',decoder='nucleus_multinomial',seed=29)]

def protected():
    extra={str(p.relative_to(E.parent)):s.sha(p) for p in (E/'byte-medium-model-pilot-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    return s.inventory()|extra

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def prepare():
    s.guard();assert not (H/'CONTRACT.json').exists()
    save(H/'SAMPLER_CHECKS.json',checks());save(H/'PROTECTED_BEFORE.json',protected())
    pins=s.source_pins()|{str(H/n):s.sha(H/n) for n in ['run.py','sampling.py','PROTOCOL.md']}|{str(E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json'):s.sha(E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json')}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',identity='fresh one-shot decoder branches; prior worlds unchanged',configs=CONFIGS,temperature=0.8,top_p=0.95,budget=3,max_output_tokens=256,pins=pins,tensor_digest=read(E/'byte-medium-model-pilot-v1/CONTRACT.json')['tensor_digest']))
    initial=read(E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json');tok=s.c.tokenizer()
    assert tok.apply_chat_template(initial['messages'],tokenize=True,add_generation_prompt=True)==initial['input_token_ids']
    seed=E/'byte-medium-model-pilot-v1/seed'
    for cfg in CONFIGS:
        d=H/cfg['name'];d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:
            b=w.world.checkpoint();obs=s.observation(d,b,0,read(d/'world/STATE.json'),None)
            assert obs==initial['observation']
        finally:w.close()
        save(d/'INITIAL_INPUT.json',initial);save(d/'STATE.json',dict(turn=0,paused=True))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',model_calls=0,input_tokens=len(initial['input_token_ids']),all_initial_messages_ids_worlds_observations_matched=True,protected_files=len(protected())))
    print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==expected;resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for cfg in CONFIGS:
            guard();d=H/cfg['name'];assert read(d/'STATE.json')['turn']==0
            initial=read(d/'INITIAL_INPUT.json');ms=initial['messages'];save(d/'PENDING.json',dict(stage='generation/effects unresolved; no automatic replay'))
            raw=s.ref.body.generate(model,tok,ms,resource,cfg['name']) if cfg['seed'] is None else generate(model,tok,ms,resource,cfg['name'],cfg['seed'])
            assert raw['input_token_ids']==initial['input_token_ids'];save(d/'RAW.json',raw)
            w=s.a.MediumWorld.open(d/'world')
            try:
                r=w.complete(raw['text'],'reply_000001');bundle=w.world.checkpoint();step=w.world.step
            finally:w.close()
            save(d/'SNAPSHOT.json',bundle);save(d/'OBSERVATION.json',s.observation(d,bundle,step,read(d/'world/STATE.json'),1))
            save(d/'RECORD.json',dict(raw_sha256=s.sha(d/'RAW.json'),adapter_reply_sha256=s.sha(d/'world/replies/reply_000001.json'),actor_operations=len(r['actor_batch']['operations']),world_id=bundle['id'],world_step=step))
            s.a.base.atomic(d/'STATE.json',dict(turn=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json')
            print(s.text(dict(branch=cfg['name'],output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],actor_operations=len(r['actor_batch']['operations']))),flush=True)
        assert parameter_digest(model,False)==expected;guard()
    except BaseException as e:
        save(H/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(H/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='run':run()
