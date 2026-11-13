"""In-memory KV versus exact raw-prefix prefill; no executable world actions."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k]=v
from pathlib import Path
import json, hashlib, sys, time
import torch
from transformers import AutoModelForCausalLM

H=Path(__file__).resolve().parent
E=H.parents[1]
C=E/'minimal-garden-candidate-v1'
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
sys.path.insert(0,str(E/'source-access-three-cycle-v1'))
from runtime_reference import parameter_digest

def inventory():
    return {str(p.relative_to(C/'run')):hashlib.sha256(p.read_bytes()).hexdigest()
       for p in (C/'run').rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def dump(name,obj):
    (H/name).write_text(json.dumps(obj,indent=2)+'\n')

def main():
    before=inventory()
    reference=json.loads((E/'output-cap-contact-v1/retained_01.json').read_text())
    prompt=reference['input_token_ids']; prefix=reference['generated_token_ids'][:256]
    expected=reference['generated_token_ids'][256:320]
    assert len(prefix)==256 and len(expected)==64
    dump('CHUNK_PLAN.json',{'date':'2026-11-13 America/Chicago','prefix_tokens':256,'suffix_tokens':64,
      'model':'cached SmolLM2-135M-Instruct','condition':'CPU float32 eager greedy',
      'cache_test':'in-memory only; no serialized KV or cross-process resume',
      'prefix_source':'output-cap-contact-v1/retained_01.json','fresh_prefill':'exact IDs, no retemplating',
      'logits_tolerance_atol':0.0001,'logits_tolerance_rtol':0.0001,'canonical_mutation':False})
    torch.set_num_threads(2)
    model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,
      use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected_digest=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest']
    assert parameter_digest(model,False)==expected_digest
    started=time.perf_counter()
    with torch.inference_mode():
        # Rebuild actual sequential cache state at the live loop's cap:
        # prompt + first 255 output tokens, with selected token 256 pending.
        ids=torch.tensor([prompt])
        out=model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=True,logits_to_keep=1)
        cache=out.past_key_values
        for token in prefix[:-1]:
            out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
            cache=out.past_key_values
        before_last=cache.get_seq_length()
        assert before_last==len(prompt)+255
        out=model(input_ids=torch.tensor([[prefix[-1]]]),past_key_values=cache,
            attention_mask=torch.ones((1,before_last+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
        cached,clogits=out.past_key_values,out.logits[0,-1]
        assert cached.get_seq_length()==len(prompt)+256
        raw=torch.tensor([prompt+prefix])
        fresh=model(input_ids=raw,attention_mask=torch.ones_like(raw),use_cache=True,logits_to_keep=1)
        fcache,flogits=fresh.past_key_values,fresh.logits[0,-1]
        rows=[];ctokens=[];ftokens=[]
        for i in range(64):
            ct=int(clogits.argmax());ft=int(flogits.argmax())
            ctokens.append(ct);ftokens.append(ft)
            rows.append({'suffix_index':i,'cached_token':ct,'fresh_token':ft,'uninterrupted_token':expected[i],
                'max_abs_logits_difference':float((clogits-flogits).abs().max()),
                'logits_within_tolerance':bool(torch.allclose(clogits,flogits,atol=1e-4,rtol=1e-4)),
                'cached_length':cached.get_seq_length(),'fresh_length':fcache.get_seq_length()})
            if i<63:
                co=model(input_ids=torch.tensor([[ct]]),past_key_values=cached,
                    attention_mask=torch.ones((1,cached.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                fo=model(input_ids=torch.tensor([[ft]]),past_key_values=fcache,
                    attention_mask=torch.ones((1,fcache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                cached,clogits=co.past_key_values,co.logits[0,-1]
                fcache,flogits=fo.past_key_values,fo.logits[0,-1]
    after=inventory();unchanged=before==after
    weights=parameter_digest(model,False)==expected_digest
    result={'condition':'64-token greedy suffix after exact 256-token prefix',
      'cache_length_before_last_prefix_token':before_last,'prompt_tokens':len(prompt),
      'cached_suffix_exact_uninterrupted':ctokens==expected,'fresh_suffix_exact_uninterrupted':ftokens==expected,
      'cached_fresh_suffix_exact':ctokens==ftokens,
      'all_logits_within_tolerance':all(r['logits_within_tolerance'] for r in rows),
      'max_abs_logits_difference':max(r['max_abs_logits_difference'] for r in rows),
      'first_cached_fresh_token_divergence':next((i for i,(a,b) in enumerate(zip(ctokens,ftokens)) if a!=b),None),
      'canonical_run_unchanged':unchanged,'weights_unchanged':weights,'rows':rows,'seconds':time.perf_counter()-started,
      'limits':'Single context, in-memory cache, no persistent cache serialization, no sampling RNG restoration.'}
    dump('CHUNK_RESULTS.json',result)
    assert unchanged and weights
    assert ctokens==expected and ftokens==expected
    assert result['all_logits_within_tolerance']
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))

if __name__=='__main__':main()
