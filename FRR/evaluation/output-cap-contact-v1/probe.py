"""Detached greedy length probe; no generated code is executed."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k]=v
from pathlib import Path
import json, hashlib, sys, time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

H=Path(__file__).resolve().parent
C=H.parent/'minimal-garden-candidate-v1'
sys.path[:0]=[str(C),str(C/'world'),str(H.parent/'source-access-three-cycle-v1')]
import candidate
from garden_world import parse_notebook
from runtime_reference import parameter_digest

def inventory(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def save(name,obj):
    (H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main():
    before=inventory(C/'run')
    save('PLAN.json',{'date':'2026-11-13 America/Chicago','scope':'detached inference only',
      'inputs':['retained turn 1','retained turn 12','prospective turn 13'],
      'output_cap':1024,'milestones':[256,512,768,1024],
      'decoder':'greedy argmax; fresh prefill per input; contiguous KV continuation',
      'code_execution':False,'training':False,'canonical_mutation':False,
      'interpretation':'Milestones are prefixes of one generation, not independent trials. No continuation prompt is added.'})
    torch.set_num_threads(2)
    base='/workspace/cache_backend_models/smollm2-135m'
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False); model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest']
    assert parameter_digest(model,False)==expected
    summary=[]
    cases=[]
    for n in (1,12):
        raw=json.loads((C/f'run/raw/{n:06d}.json').read_text())
        cases.append((f'retained_{n:02d}',raw['messages'],raw))
    cases.append(('prospective_13',candidate.messages(C/'run'),None))
    for label,messages,reference in cases:
        ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        assert len(ids)+1024<=8192
        if reference: assert ids==reference['input_token_ids']
        started=time.perf_counter(); generated=[]; milestones=[]; stop='token_limit'
        with torch.inference_mode():
            x=torch.tensor([ids])
            out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
            cache,logits=out.past_key_values,out.logits[0,-1]
            for i in range(1024):
                token=int(logits.argmax()); generated.append(token)
                if token==tok.eos_token_id: stop='eos'
                if len(generated) in (256,512,768,1024) or stop=='eos':
                    text=tok.decode(generated,skip_special_tokens=True)
                    parsed=parse_notebook(text)
                    milestones.append({'tokens':len(generated),'complete_executable_cells':parsed['complete_executable_cells'],
                        'incomplete_fences':sum(not c['complete'] for c in parsed['cells'])})
                    save(label+'.json',{'label':label,'messages':messages,'input_token_ids':ids,
                        'generated_token_ids':generated,'text':text,'stop':stop,'milestones':milestones})
                    print(label,milestones[-1],flush=True)
                if stop=='eos': break
                if i<1023:
                    out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                        attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                    cache,logits=out.past_key_values,out.logits[0,-1]
        match=None if reference is None else generated[:256]==reference['generated_token_ids']
        if reference: assert match
        summary.append({'label':label,'input_tokens':len(ids),'output_tokens':len(generated),'stop':stop,
          'retained_256_prefix_exact':match,'milestones':milestones,'seconds':time.perf_counter()-started})
    after=inventory(C/'run')
    assert before==after
    assert parameter_digest(model,False)==expected
    save('RESULTS.json',{'cases':summary,'canonical_run_unchanged':True,'weights_unchanged':True,
         'run_inventory':before,'actual_model_generations':3,'generated_code_executions':0})

if __name__=='__main__': main()
