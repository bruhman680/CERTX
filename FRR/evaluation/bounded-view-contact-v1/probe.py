"""Three detached greedy input-view comparisons; no world execution."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,hashlib,time
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
from view import select_view
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1'
sys.path[:0]=[str(C/'world'),str(H.parent/'source-access-three-cycle-v1')]
from garden_world import parse_notebook
from runtime_reference import parameter_digest
def save(name,obj):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),f'Preserve prior artifact: {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def inventory():
    return {str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest() for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    before=inventory();state=json.loads((C/'run/STATE.json').read_text());assert state['human_entry']==1580 and state['paused']
    initial=json.loads((C/'run/INITIAL_MESSAGES.json').read_text())
    events=[json.loads(p.read_text()) for p in sorted((C/'run/events').glob('*.json'))]
    exchanges=[{'entry':x['human_entry'],'assistant':x['text'],'receipt':x['feedback']} for x in events]
    save('PLAN.json',{'date':'2026-11-13 America/Chicago','source_entry':1580,'views':[4,8,12],
      'decoder':'unchanged greedy256 CPU float32 eager; fresh KV per input','new_model_generations':3,
      'question':'does each bounded view fit, what visible output results, and what history is omitted?',
      'baseline':'full current conversation exceeds7936 and is not run',
      'selection':'complete latest pairs, chronological and content-independent, original initial messages retained',
      'no_summaries_or_new_instructions':True,'code_execution':False,'training':False,
      'canonical_mutation':False,'deployment':False,
      'world_rules_note':'inherited WORLD_RULES.txt describes full-history source condition; an adopted version needs a declared consistent rule update; no world read/execution in this input-only test'})
    save('SOURCE_ARCHIVE.json',{'initial_messages':initial,'exchanges':exchanges,'canonical_state':state})
    save('BEFORE_INVENTORY.json',before)
    torch.set_num_threads(2);base='/workspace/cache_backend_models/smollm2-135m'
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    full=initial.copy()
    for x in exchanges:full.extend([{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}])
    full_tokens=tok.apply_chat_template(full,tokenize=True,add_generation_prompt=True)
    assert len(full_tokens)==8104
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest'];assert parameter_digest(model,False)==expected
    rows=[];prior={x['assistant'] for x in exchanges}
    for count in [4,8,12]:
        view=select_view(initial,exchanges,tok,max_pairs=count);save(f'views/recent{count}.json',view)
        ids=view['input_token_ids'];new=[];stop='token_limit';started=time.perf_counter()
        with torch.inference_mode():
            x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
            cache,logits=out.past_key_values,out.logits[0,-1]
            for i in range(256):
                token=int(logits.argmax());new.append(token)
                if token==tok.eos_token_id:stop='eos';break
                if i<255:
                    out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                        attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                    cache,logits=out.past_key_values,out.logits[0,-1]
        text=tok.decode(new,skip_special_tokens=True);parsed=parse_notebook(text)
        row={'recent_pairs':count,'input_tokens':len(ids),'output_tokens':len(new),'stop':stop,
            'included_entries':view['included_entries'],'omitted_entries':view['omitted_entries'],
            'complete_cells':parsed['complete_executable_cells'],'incomplete_fences':sum(not c['complete'] for c in parsed['cells']),
            'exact_prior_text_match':text in prior,'seconds':time.perf_counter()-started}
        save(f'raw/recent{count}.json',{**row,'generated_token_ids':new,'text':text,'parsed':parsed})
        rows.append(row);print(json.dumps(row),flush=True)
    assert before==inventory();assert parameter_digest(model,False)==expected
    save('RESULTS.json',{'rows':rows,'full_history_input_tokens':len(full_tokens),'canonical_unchanged':True,
      'weights_unchanged':True,'actual_model_generations':3,'code_executions':0,'policy_adopted':False})
if __name__=='__main__':main()
