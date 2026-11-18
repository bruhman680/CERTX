"""Two missing context corners; fixed outcome, literal operator verification."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,uuid,importlib.util
H=Path(__file__).resolve().parent;E=H.parent.parent
sys.path.insert(0,str(E/'matched-length-framing-v1'))
spec=importlib.util.spec_from_file_location('preserved_matched_run',E/'matched-length-framing-v1/run.py');parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
s=parent.s;save=s.save;read=s.read;QUESTION=parent.QUESTION
NAMES=['frr_native','geology_native','textiles_native']
BOUNDARY='\n\n\n/world is writable persistent storage.'
OLD='Initial context contains FRR, these mechanics, the condition law and the initial observation.'
NEW='Initial context contains these mechanics, the condition law and the initial observation.'

def components():
    full=read(E/'minimal-cell-control-v1/full/INITIAL_INPUT.json')['messages'][0]['content']
    assert full.count(BOUNDARY)==1
    n=full.index(BOUNDARY)
    frr,mechanics=full[:n],full[n:]
    assert frr+mechanics==full and mechanics.count(OLD)==1
    return frr,mechanics

def native_prefix():
    raw=read(E/'minimal-cell-control-v1/native/INITIAL_INPUT.json')['rendered_chat']
    return raw.split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0]

def match(tok):
    ref=read(E/'minimal-cell-control-v1/full/INITIAL_INPUT.json')['messages'];prefix=native_prefix();frr,_=components()
    def ms(p):return [{'role':'system','content':prefix+'\n\n'+p},ref[1]]
    target=200;out={'target_input_tokens':target,'native_prefix':prefix,'passages':{}}
    for name,source in read(H/'CONTROL_PASSAGES.json').items():
        ids=tok.encode(source,add_special_tokens=False);found=None
        for n in range(1,len(ids)+1):
            text=tok.decode(ids[:n],skip_special_tokens=False)+'.'
            if len(tok.apply_chat_template(ms(text),tokenize=True,add_generation_prompt=True))==target:
                found=dict(text=text,source_tokens_used=n,source_tokens_available=len(ids),matching_rule='first matching decoded token prefix plus terminal period');break
        assert found is not None,name
        out['passages'][name+'_native']=found
    return out

def messages(name):
    ref=read(E/'minimal-cell-control-v1/full/INITIAL_INPUT.json')['messages'];m=read(H/'MATCHING.json');assert name in NAMES
    return [{'role':'system','content':m['native_prefix']+'\n\n'+m['passages'][name]['text']},ref[1]]

def protected():
    return parent.protected()|{str(p.relative_to(E.parent)):s.sha(p) for p in (E/'matched-length-framing-v1').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def guard():
    assert protected()==read(H/'PROTECTED_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(H/'CONTRACT.json')['pins'].items())

def prepare():
    parent.guard();save(H/'PROTECTED_BEFORE.json',protected())
    pins=read(E/'matched-length-framing-v1/CONTRACT.json')['pins']|{str(H/n):s.sha(H/n) for n in ['run.py','audit.py','PROTOCOL.md','CONTROL_PASSAGES.json']}
    save(H/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=3,question=QUESTION,tensor_digest=read(E/'minimal-cell-control-v1/CONTRACT.json')['tensor_digest'],decoder='greedy_argmax',max_output_tokens=256))
    save(H/'MATCHING.json',match(s.c.tokenizer()))
    seed=E/'byte-medium-model-pilot-v1/seed';tok=s.c.tokenizer();pre=[]
    for name in NAMES:
        d=H/name;d.mkdir();w=s.a.MediumWorld.create(d/'world',seed/'bundle.json',seed/'objects','changing')
        try:bundle=w.world.checkpoint();save(d/'INITIAL_SNAPSHOT.json',bundle)
        finally:w.close()
        assert bundle==read(E/'minimal-cell-control-v1/native/INITIAL_SNAPSHOT.json')
        ms=messages(name);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);assert len(ids)==read(H/'MATCHING.json')['target_input_tokens']<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,rendered_chat=tok.apply_chat_template(ms,tokenize=False,add_generation_prompt=True),actual_seed_world_id=bundle['id']))
        save(d/'STATE.json',dict(model_calls=0,paused=True));pre.append(dict(context=name,input_tokens=len(ids),world_id=bundle['id']))
    guard();save(H/'PREFLIGHT.json',dict(status='pass',initial_worlds_identical=True,branches=pre,model_calls=0,protected_files=len(protected())));print(s.text(read(H/'PREFLIGHT.json')),flush=True)

def run():
    guard();assert not (H/'RUN.lock').exists();save(H/'RUN.lock',dict(pid=os.getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(H/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for name in NAMES:
            guard();d=H/name;assert read(d/'STATE.json')['model_calls']==0 and not (d/'PENDING.json').exists();init=read(d/'INITIAL_INPUT.json');save(d/'PENDING.json',dict(stage='generation/verification unresolved; no replay'))
            raw=s.ref.body.generate(model,tok,init['messages'],resource,'context_corner_'+name);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
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
