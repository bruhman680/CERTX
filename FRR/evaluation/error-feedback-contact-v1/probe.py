"""One-step detailed-error versus status-only comparison, on detached copies."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,hashlib,time,copy,ast
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
H=Path(__file__).resolve().parent;E=H.parent
C=E/'minimal-garden-candidate-v1';D=E/'decoder-context-contact-v1';P=E/'decoder-consequence-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import GardenWorld,parse_notebook,verify_store
from runtime_reference import parameter_digest
SEEDS=[27201,27202,27203]
def save(name,obj):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),f'Preserve existing artifact: {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def inventory(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    before=inventory(C/'run');parent_before=inventory(P)
    base_messages=json.loads((D/'references/retained_01.json').read_text())['messages']
    sampled=json.loads((D/'raw/retained_01_27103.json').read_text())
    batch=json.loads((P/'retained_01_27103_BATCH.json').read_text())
    full=candidate.project_feedback(batch)
    reduced=json.loads(full)
    for r in reduced['receipts']:r['stderr']=''
    reduced=json.dumps(reduced,ensure_ascii=False,sort_keys=True)
    messages={label:base_messages+[{'role':'assistant','content':sampled['text']},{'role':'user','content':feedback}]
              for label,feedback in [('full_traceback',full),('status_only',reduced)]}
    parent=P/'worlds/retained_01_27103'
    state=json.loads((parent/'STATE.json').read_text());bundle=parent/'bundles'/state['bundle']
    plan={'date':'2026-11-13 America/Chicago','question':'one-step response to actual detailed error vs failure status only',
      'seeds':SEEDS,'conditions':['full_traceback','status_only'],
      'decoder':{'temperature':.8,'top_p':.9,'cap':512},
      'parent_sample':'retained_01_27103','parent_reply_was_capped':sampled['stop']=='token_limit',
      'feedback':'full uses unchanged canonical project_feedback; status-only changes only stderr to empty',
      'control_is_counterfactual':True,'tokens_not_length_matched':True,
      'world_parent':str(bundle),'world_parent_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),
      'world_state_same_for_all_cases':True,'followup_depth':1,'planned_model_replies':6,
      'primary':'record every reply and its actual notebook/cell consequences; no automatic success rubric',
      'diagnostic_only':True,'training':False,'canonical_mutation':False,
      'scope':'selected single parent; context length and error-content effects not separated; seed pairs are not six environments'}
    save('PLAN.json',plan);save('INPUT_MESSAGES.json',messages)
    torch.set_num_threads(2);base='/workspace/cache_backend_models/smollm2-135m'
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest']
    assert parameter_digest(model,False)==expected
    rows=[]
    for seed in SEEDS:
      for condition in plan['conditions']:
        label=f'{condition}_{seed}';ids=tok.apply_chat_template(messages[condition],tokenize=True,add_generation_prompt=True)
        assert len(ids)+512<=8192
        rng=torch.Generator(device='cpu').manual_seed(seed);tokens=[];stop='token_limit';started=time.perf_counter()
        with torch.inference_mode():
          x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
          cache,logits=out.past_key_values,out.logits[0,-1]
          for i in range(512):
            scores,indices=torch.sort(logits/.8,descending=True);probs=torch.softmax(scores,dim=-1)
            probs[(probs.cumsum(-1)-probs)>.9]=0;probs=probs/probs.sum()
            token=int(indices[torch.multinomial(probs,1,generator=rng)]);tokens.append(token)
            if token==tok.eos_token_id:stop='eos';break
            if i<511:
              out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
              cache,logits=out.past_key_values,out.logits[0,-1]
        text=tok.decode(tokens,skip_special_tokens=True);parsed=parse_notebook(text)
        raw={'condition':condition,'seed':seed,'input_token_ids':ids,'generated_token_ids':tokens,
          'text':text,'stop':stop,'seconds':time.perf_counter()-started,'parsed':parsed}
        save('raw/'+label+'.json',raw)
        store=H/'worlds'/label;store.parent.mkdir(exist_ok=True)
        w=GardenWorld.create(store,bundle,parent/'objects',parent_entry=1550)
        try:
          outcome=w.receive_notebook(text);save('batches/'+label+'.json',outcome)
        finally:w.close()
        ops=[{'channel':o['channel'],'changed_paths':o['changed_paths'],'feedback':o['feedback']} for o in outcome['operations']]
        row={'condition':condition,'seed':seed,'input_tokens':len(ids),'output_tokens':len(tokens),'stop':stop,
          'complete_executable_cells':parsed['complete_executable_cells'],
          'incomplete_fences':sum(not c['complete'] for c in parsed['cells']),
          'operations':ops,'store_verification':verify_store(store)}
        rows.append(row);print(json.dumps({k:v for k,v in row.items() if k not in ('operations','store_verification')}),flush=True)
    assert before==inventory(C/'run') and parent_before==inventory(P)
    assert parameter_digest(model,False)==expected
    save('RESULTS.json',{'plan':plan,'rows':rows,'canonical_run_unchanged':True,'parent_diagnostic_unchanged':True,
      'weights_unchanged':True,'actual_model_replies':len(rows),'extra_feedback_cycles':0})
if __name__=='__main__':main()
