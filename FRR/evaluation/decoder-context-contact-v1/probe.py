"""Detached decoder comparison. No generated code executes; no live changes."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items(): os.environ[k]=v
from pathlib import Path
import sys, json, time, hashlib, ast
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
H=Path(__file__).resolve().parent
C=H.parent/'minimal-garden-candidate-v1'
O=H.parent/'output-cap-contact-v1'
sys.path[:0]=[str(C/'world'),str(H.parent/'source-access-three-cycle-v1')]
from garden_world import parse_notebook
from runtime_reference import parameter_digest
SEEDS=[27101,27102,27103,27104]
CAP=512
def write(name,x):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def inventory(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def assess(text):
    parsed=parse_notebook(text)
    syntax=[]
    for c in parsed['cells']:
        if c['executable'] and c['language']=='python':
            try: ast.parse(c['source']);syntax.append({'parseable':True})
            except SyntaxError as e: syntax.append({'parseable':False,'exception':str(e)})
    return {'complete_executable_cells':parsed['complete_executable_cells'],
       'incomplete_fences':sum(not c['complete'] for c in parsed['cells']),
       'python_syntax':syntax,'code_executed':False}
def main():
    assert not (H/'RESULTS.json').exists(),'Preserve existing results'
    before=inventory(C/'run')
    plan={'date':'2026-11-13 America/Chicago','contexts':['retained_01','prospective_13'],
       'seeds':SEEDS,'sampling':{'temperature':.8,'top_p':.9,'cap':CAP},
       'greedy_reference':'saved output-cap-contact-v1 exact-token outputs, prefix up to 512 or EOS',
       'primary_observation':'complete executable fence count; no correctness or action-success score',
       'secondary':'EOS, incomplete fences, static Python syntax only',
       'inference_calls_planned':8,'training':False,'canonical_mutation':False,
       'design':'two fixed contexts, four sample seeds each; selected after prior cap diagnostic; exploratory'}
    write('PLAN.json',plan)
    torch.set_num_threads(2)
    base='/workspace/cache_backend_models/smollm2-135m'
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest']
    assert parameter_digest(model,False)==expected
    rows=[]
    for label in plan['contexts']:
        refpath=O/(label+'.json');ref=json.loads(refpath.read_text())
        ids=ref['input_token_ids']
        assert ids==tok.apply_chat_template(ref['messages'],tokenize=True,add_generation_prompt=True)
        assert len(ids)+CAP<=8192
        prefix=ref['generated_token_ids'][:CAP]
        write('references/'+label+'.json',{'source_sha256':hashlib.sha256(refpath.read_bytes()).hexdigest(),
            'source':str(refpath),'messages':ref['messages'],'input_token_ids':ids,
            'generated_token_ids':prefix,'assessment':assess(tok.decode(prefix,skip_special_tokens=True))})
        for seed in SEEDS:
            started=time.perf_counter();rng=torch.Generator(device='cpu').manual_seed(seed)
            generated=[];stop='token_limit';milestones=[]
            with torch.inference_mode():
                x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
                cache,logits=out.past_key_values,out.logits[0,-1]
                for i in range(CAP):
                    scores,indices=torch.sort(logits/.8,descending=True)
                    probabilities=torch.softmax(scores,dim=-1)
                    # Retain the first token crossing the threshold, matching conventional nucleus sampling.
                    probabilities[(probabilities.cumsum(-1)-probabilities)>.9]=0
                    probabilities=probabilities/probabilities.sum()
                    token=int(indices[torch.multinomial(probabilities,1,generator=rng)])
                    generated.append(token)
                    if token==tok.eos_token_id:stop='eos'
                    if len(generated)==256 or stop=='eos' or i==CAP-1:
                        milestones.append({'tokens':len(generated),**assess(tok.decode(generated,skip_special_tokens=True))})
                    if stop=='eos':break
                    if i<CAP-1:
                        out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                            attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                        cache,logits=out.past_key_values,out.logits[0,-1]
            text=tok.decode(generated,skip_special_tokens=True)
            row={'context':label,'seed':seed,'output_tokens':len(generated),'stop':stop,
               'assessment':assess(text),'milestones':milestones,'seconds':time.perf_counter()-started}
            write(f'raw/{label}_{seed}.json',{**row,'generated_token_ids':generated,'text':text})
            rows.append(row);print(json.dumps(row),flush=True)
    assert before==inventory(C/'run')
    assert parameter_digest(model,False)==expected
    write('RESULTS.json',{'plan':plan,'rows':rows,'canonical_run_unchanged':True,
       'weights_unchanged':True,'actual_inference_calls':len(rows),'generated_code_executions':0})
if __name__=='__main__': main()
