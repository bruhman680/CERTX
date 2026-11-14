"""Single local model process for all three planned detached contacts."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import json,time,copy,hashlib
import torch
from transformers import AutoModelForCausalLM
import common as c
from runtime_reference import parameter_digest,Guard

def profile(model,tok):
    view=c.base_view(tok);ref=c.read(c.P/'raw/01.json')
    assert view['input_token_ids']==ref['input_token_ids']
    target=ref['generated_token_ids'];x=torch.tensor([view['input_token_ids']+target[:-1]])
    with torch.inference_mode():
      logits=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=False,logits_to_keep=len(target)).logits[0]
      probs=torch.softmax(logits/.8,dim=-1);sorted_probs,indices=torch.sort(probs,descending=True,dim=-1)
      size=((sorted_probs.cumsum(-1)-sorted_probs)<=.9).sum(-1)
      rows=[{'output_index':i,'greedy_matches_reference':int(logits[i].argmax())==target[i],
          'nucleus_size_p90':int(size[i]),'top1_probability_temp08':float(sorted_probs[i,0]),
          'eos_probability_temp08':float(probs[i,tok.eos_token_id])} for i in range(len(target))]
    c.save(c.H/'decoder/NUCLEUS_PROFILE.json',{'scope':'one teacher-forced saved greedy path; parallel prefill may differ numerically from incremental decoding',
      'rows':rows,'all_argmax_match_reference':all(r['greedy_matches_reference'] for r in rows),
      'positions_with_more_than_one_p90_choice':sum(r['nucleus_size_p90']>1 for r in rows),
      'min_p90_size':min(r['nucleus_size_p90'] for r in rows),'max_p90_size':max(r['nucleus_size_p90'] for r in rows),
      'model_generations':0,'extra_teacher_forced_forward_passes':1})

def generate(model,tok,messages,job,guard,run_id):
    ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    if len(ids)>7936:raise ValueError('Capacity reached; no trimming')
    tokens=[];stop='token_limit';started=time.perf_counter()
    rng=torch.Generator(device='cpu').manual_seed(job['seed']) if job['decoder']=='nucleus' else None
    guard.read('before_generate',run_id=run_id)
    with torch.inference_mode():
      x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
      cache,logits=out.past_key_values,out.logits[0,-1]
      for i in range(256):
        if rng is None:token=int(logits.argmax())
        else:
          scores,order=torch.sort(logits/job['temperature'],descending=True);p=torch.softmax(scores,dim=-1)
          if job['top_p']<1.0:p[(p.cumsum(-1)-p)>job['top_p']]=0
          p=p/p.sum();token=int(order[torch.multinomial(p,1,generator=rng)])
        tokens.append(token)
        if token==tok.eos_token_id:stop='eos';break
        if i<255:
          out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
            attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
          cache,logits=out.past_key_values,out.logits[0,-1]
    guard.read('after_generate',run_id=run_id)
    return {'messages':messages,'input_token_ids':ids,'generated_token_ids':tokens,'text':tok.decode(tokens,skip_special_tokens=True),
       'stop':stop,'decoder':job['decoder'],'temperature':job.get('temperature'),'top_p':job.get('top_p'),
       'seed':job.get('seed'),'seconds':time.perf_counter()-started}

def main():
    assert not (c.H/'WORKER_PLAN.json').exists(),'Do not rerun into prior artifacts'
    before=c.inventory();assert before==c.read(c.H/'CANONICAL_BEFORE.json')
    jobs=c.read(c.H/'retrieval/jobs.json')+c.read(c.H/'observation/jobs.json')+c.read(c.H/'decoder/jobs.json')
    assert len(jobs)==12 and len({j['case_id'] for j in jobs})==12
    assert sum(j['max_turns'] for j in jobs)==15
    for j in jobs:assert Path(j['world_store']).resolve().is_relative_to(c.H.resolve())
    c.save(c.H/'WORKER_PLAN.json',{'jobs':jobs,'planned_generations':15,'teacher_forced_profile_passes':1,
      'source_sha256':c.sha(Path(__file__)),'common_sha256':c.sha(c.H/'common.py'),
      'core_inputs':'only job messages; case labels/metadata/expected values never injected',
      'execution':'all complete notebook cells run unchanged in case-specific sandbox copies',
      'followup':'for retrieval only, append actual assistant/receipt once; no repeat task or hint'})
    torch.set_num_threads(2);tok=c.tokenizer()
    model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,
       use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=c.read(c.C/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected
    guard=Guard(5153960755,c.H/'RESOURCE.jsonl');guard.read('model_loaded');rows=[]
    for job in jobs:
      messages=copy.deepcopy(job['messages'])
      for turn in range(1,job['max_turns']+1):
        name=f"{job['case_id']}_t{turn}";outdir=c.H/'results'/job['case_id'];outdir.mkdir(parents=True,exist_ok=True)
        pending=c.H/'PENDING.json';assert not pending.exists()
        pending.write_text(json.dumps({'case_id':job['case_id'],'turn':turn,'stage':'generation/action unresolved'}))
        c.save(outdir/f'plan{turn}.json',{'messages':messages,'world_state':c.read(Path(job['world_store'])/'STATE.json')})
        raw=generate(model,tok,messages,job,guard,name);c.save(outdir/f'raw{turn}.json',raw)
        world=c.GardenWorld.open(Path(job['world_store']))
        try:
          before_world=world.checkpoint();batch=world.receive_notebook(raw['text']);c.save(outdir/f'batch{turn}.json',batch)
          after=world.checkpoint()
        finally:world.close()
        feedback=c.candidate.project_feedback(batch)
        row={'case_id':job['case_id'],'turn':turn,'metadata':job['metadata'],
          'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],
          'input_sha256':hashlib.sha256(json.dumps(raw['input_token_ids']).encode()).hexdigest(),
          'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),
          'complete_cells':batch['parsed']['complete_executable_cells'],
          'incomplete_fences':sum(not x['complete'] for x in batch['parsed']['cells']),
          'before_id':before_world['id'],'after_id':after['id'],'feedback':feedback,
          'operations':[{'channel':x['channel'],'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations']],
          'world_verification':c.verify_store(Path(job['world_store']))}
        c.save(outdir/f'result{turn}.json',row);rows.append(row);pending.unlink()
        messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        assert before==c.inventory();assert parameter_digest(model,False)==expected
        print(json.dumps({k:row[k] for k in ['case_id','turn','input_tokens','output_tokens','complete_cells','stop']}),flush=True)
    profile(model,tok)
    assert before==c.inventory();assert parameter_digest(model,False)==expected
    c.save(c.H/'RESULTS.json',{'rows':rows,'actual_model_generations':len(rows),'teacher_forced_profile_passes':1,
      'canonical_unchanged':True,'weights_unchanged':True,'activation':False,'pending':False})
if __name__=='__main__':main()
