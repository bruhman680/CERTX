"""Three consecutive replies on one detached persistent branch. No replay."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,hashlib,time
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1';P=E/'error-feedback-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import GardenWorld,parse_notebook,verify_store
from runtime_reference import parameter_digest
def save(name,obj):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),f'Preserve prior artifact: {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inv(root):return {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    live_before=inv(C/'run');parent_before=inv(P)
    label='full_traceback_27201'
    parent_raw=json.loads((P/'raw'/f'{label}.json').read_text())
    parent_batch=json.loads((P/'batches'/f'{label}.json').read_text())
    messages=json.loads((P/'INPUT_MESSAGES.json').read_text())['full_traceback']
    messages += [{'role':'assistant','content':parent_raw['text']},
                 {'role':'user','content':candidate.project_feedback(parent_batch)}]
    parent=P/'worlds'/label;state=json.loads((parent/'STATE.json').read_text());bundle=parent/'bundles'/state['bundle']
    plan={'date':'2026-11-13 America/Chicago','loops':3,
      'selection':'first predeclared full-traceback seed 27201, not selected by output quality',
      'parent_branch':label,'parent_world':str(bundle),'parent_world_sha256':sha(bundle),
      'source_sha256':sha(Path(__file__)),
      'decoder':{'temperature':.8,'top_p':.9,'output_cap':512,'new_session_seed':27301},
      'rng_continuity':'previous diagnostic RNG state was not retained; new stream declared once, then retained across all 3 loops',
      'continuity':'same persistent world, complete actual conversation, fresh KV per reply, exact actual projected receipts',
      'instructions_changed':False,'training':False,'canonical_mutation':False,
      'capacity':'pause before generation if input + 512 exceeds 8192; no truncation',
      'interruption':'artifacts are immutable; no automatic rerun or replay of unknown effects',
      'observer':'no code/accuracy requirement or success score in model inputs'}
    save('PLAN.json',plan);save('INITIAL_MESSAGES.json',messages)
    torch.set_num_threads(2);base='/workspace/cache_backend_models/smollm2-135m'
    tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(base,local_files_only=True,trust_remote_code=False,
       use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest']
    assert parameter_digest(model,False)==expected
    w=GardenWorld.create(H/'world',bundle,parent/'objects',parent_entry=1550)
    initial=w.checkpoint();w.close();save('INITIAL_WORLD.json',initial)
    rng=torch.Generator(device='cpu').manual_seed(27301);rows=[];prev=None
    for loop in range(1,4):
      ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
      if len(ids)+512>8192:
        save('CAPACITY_PAUSE.json',{'loop':loop,'input_tokens':len(ids)});break
      save(f'plans/{loop:02d}.json',{'loop':loop,'messages':messages,'input_token_ids':ids,'rng_state':rng.get_state().tolist(),
           'world_state':json.loads((H/'world/STATE.json').read_text()),'previous_record_sha256':prev})
      pending=H/'PENDING.json';assert not pending.exists()
      pending.write_text(json.dumps({'loop':loop,'stage':'generation or application unknown until record committed'}))
      tokens=[];stop='token_limit';started=time.perf_counter()
      with torch.inference_mode():
        x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
        cache,logits=out.past_key_values,out.logits[0,-1]
        for i in range(512):
          scores,indices=torch.sort(logits/.8,descending=True);p=torch.softmax(scores,dim=-1)
          p[(p.cumsum(-1)-p)>.9]=0;p=p/p.sum()
          token=int(indices[torch.multinomial(p,1,generator=rng)]);tokens.append(token)
          if token==tok.eos_token_id:stop='eos';break
          if i<511:
            out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
              attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
            cache,logits=out.past_key_values,out.logits[0,-1]
      text=tok.decode(tokens,skip_special_tokens=True);parsed=parse_notebook(text)
      save(f'raw/{loop:02d}.json',{'loop':loop,'input_token_ids':ids,'generated_token_ids':tokens,'text':text,
          'stop':stop,'seconds':time.perf_counter()-started,'rng_state_after':rng.get_state().tolist(),'parsed':parsed})
      w=GardenWorld.open(H/'world')
      try:
        batch=w.receive_notebook(text);save(f'batches/{loop:02d}.json',batch)
        after=w.checkpoint()
      finally:w.close()
      feedback=candidate.project_feedback(batch)
      messages += [{'role':'assistant','content':text},{'role':'user','content':feedback}]
      row={'loop':loop,'input_tokens':len(ids),'output_tokens':len(tokens),'stop':stop,
        'complete_executable_cells':parsed['complete_executable_cells'],'incomplete_fences':sum(not c['complete'] for c in parsed['cells']),
        'feedback':feedback,'after_world_id':after['id'],'previous_record_sha256':prev,
        'raw_sha256':sha(H/f'raw/{loop:02d}.json'),'batch_sha256':sha(H/f'batches/{loop:02d}.json'),
        'world_verification':verify_store(H/'world'),
        'operations':[{'channel':o['channel'],'changed_paths':o['changed_paths'],'feedback':o['feedback']} for o in batch['operations']]}
      save(f'records/{loop:02d}.json',row);prev=sha(H/f'records/{loop:02d}.json');rows.append(row)
      pending.unlink()
      assert live_before==inv(C/'run') and parent_before==inv(P)
      print(json.dumps({k:v for k,v in row.items() if k not in ('operations','feedback','world_verification')}),flush=True)
    assert parameter_digest(model,False)==expected
    save('FINAL_MESSAGES.json',messages)
    save('RESULTS.json',{'plan':plan,'rows':rows,'completed_loops':len(rows),'world_verification':verify_store(H/'world'),
      'canonical_run_unchanged':live_before==inv(C/'run'),'parent_diagnostic_unchanged':parent_before==inv(P),
      'weights_unchanged':True,'paused':True,'pending':pending.exists()})
if __name__=='__main__':main()
