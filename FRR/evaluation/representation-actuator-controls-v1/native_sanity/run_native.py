"""Separate two-call native-chat comparison/code-generation sanity baseline."""
from pathlib import Path
import sys,json,uuid,ast
N=Path(__file__).resolve().parent;H=N.parent
sys.path.insert(0,str(H));import run as parent
s=parent.s;save=s.save;read=s.read
VALUE='field.bin contains 62 bytes. Before an update its first two byte values were [1, 0]. After the update they are [0, 1]. All other byte values remain 0. What changed?'
CODE='Write Python code that creates note.txt containing a short observation about field.bin, a file that contains 62 bytes.'

def parent_inventory():
    result={}
    for name,task,treatment in parent.CASES:
        for p in (H/name).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:result[str(p.relative_to(H))]=s.sha(p)
    return result

def guard():
    parent.guard();assert parent_inventory()==read(N/'PARENT_CASES_BEFORE.json')
    assert all(s.sha(p)==v for p,v in read(N/'CONTRACT.json')['pins'].items())

def prepare():
    parent.guard();save(N/'PARENT_CASES_BEFORE.json',parent_inventory())
    pins=read(H/'CONTRACT.json')['pins']|{str(N/n):s.sha(N/n) for n in ['run_native.py','PROTOCOL.md']}
    save(N/'CONTRACT.json',dict(date='2026-11-17 America/Chicago',pins=pins,budget=2,context='official template native default system, no explicit system message',tensor_digest=read(H/'CONTRACT.json')['tensor_digest']))
    before=read(H/'array_change/INITIAL_INPUT.json')['observation']['before']['material']['values'];after=read(H/'array_change/INITIAL_INPUT.json')['observation']['after']['material']['values']
    assert before==[1,0]+[0]*60 and after==[0,1]+[0]*60
    tok=s.c.tokenizer()
    for name,q in [('comparison',VALUE),('code',CODE)]:
        d=N/name;d.mkdir();ms=[{'role':'user','content':q}];ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True);rendered=tok.apply_chat_template(ms,tokenize=False,add_generation_prompt=True)
        assert rendered.startswith('<|im_start|>system\nYou are a helpful AI assistant named SmolLM, trained by Hugging Face') and len(ids)<=7936
        save(d/'INITIAL_INPUT.json',dict(messages=ms,input_token_ids=ids,rendered_chat=rendered));save(d/'STATE.json',dict(model_calls=0,paused=True))
    seed=parent.E/'byte-medium-model-pilot-v1/seed';w=s.a.MediumWorld.create(N/'code/verification_world',seed/'bundle.json',seed/'objects','changing');w.close()
    guard();save(N/'PREFLIGHT.json',dict(status='pass',actual_fact_provenance_checked=True,parent_case_files_preserved=len(parent_inventory()),model_calls=0));print(s.text(read(N/'PREFLIGHT.json')),flush=True)

def run():
    guard();save(N/'RUN.lock',dict(pid=__import__('os').getpid()))
    try:
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=s.c.tokenizer();expected=read(N/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(s.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval();assert parameter_digest(model,False)==expected
        resource=Guard(5153960755,N/'RESOURCE.jsonl');resource.read('loaded')
        for name in ['comparison','code']:
            guard();d=N/name;assert read(d/'STATE.json')['model_calls']==0;init=read(d/'INITIAL_INPUT.json');save(d/'PENDING.json',dict(stage='generation/verification unresolved; no replay'))
            raw=s.ref.body.generate(model,tok,init['messages'],resource,'native_'+name);save(d/'RAW.json',raw);assert raw['input_token_ids']==init['input_token_ids']
            if name=='code':
                parsed=s.a.base.parse_notebook(raw['text']);sources=[c['source'] for c in parsed['cells'] if c['executable'] and c['language']=='python'];kind='complete_python_cells'
                if not sources:sources=[raw['text']];kind='literal_whole_response_syntax_only'
                syntax=[]
                for source in sources:
                    try:ast.parse(source);syntax.append(dict(valid_python_syntax=True))
                    except SyntaxError as e:syntax.append(dict(valid_python_syntax=False,error=str(e)))
                save(d/'SYNTAX.json',dict(candidate_kind=kind,checks=syntax,source_repaired=False))
                w=s.a.MediumWorld.open(d/'verification_world')
                try:rr=w.complete(raw['text'],'operator_code_verification');bundle=w.world.checkpoint()
                finally:w.close()
                save(d/'SNAPSHOT.json',bundle);save(d/'VERIFICATION.json',dict(reply_sha256=s.sha(d/'verification_world/replies/operator_code_verification.json'),actor_cells=len(rr['actor_batch']['operations']),operator_executed_generated_code=True,not_autonomous_model_action=True))
            s.a.base.atomic(d/'STATE.json',dict(model_calls=1,paused=True));assert parameter_digest(model,False)==expected;guard();s.a.c.unlink_durable(d/'PENDING.json')
            print(s.text(dict(case=name,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'])),flush=True)
        guard();assert parameter_digest(model,False)==expected
    except BaseException as error:
        import traceback
        save(N/'FAULTS'/(uuid.uuid4().hex+'.json'),dict(type=type(error).__name__,message=str(error),traceback=traceback.format_exc()));raise
    finally:s.a.c.unlink_durable(N/'RUN.lock')

if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    else:run()
