import time
import torch

def generate(model,tok,prompt,guard,run_id,seed):
 ids=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=True,add_generation_prompt=True)
 if len(ids)>2048:raise ValueError('No truncation: context boundary exceeded')
 guard.read('before_generate',run_id=run_id);started=time.perf_counter();rng=torch.Generator(device='cpu');rng.manual_seed(seed);new=[];stop='token_limit'
 with torch.inference_mode():
  x=torch.tensor([ids]);o=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1);cache,logits=o.past_key_values,o.logits[0,-1]
  for i in range(96):
   z=logits.float()/.8;v,ix=torch.sort(z,descending=True);p=torch.softmax(v,dim=-1);remove=torch.cumsum(p,0)-p>=.9;v=v.masked_fill(remove,float('-inf'));pick=int(torch.multinomial(torch.softmax(v,0),1,generator=rng));token=int(ix[pick]);new.append(token)
   if token==tok.eos_token_id:stop='eos';break
   if i<95:
    o=model(input_ids=torch.tensor([[token]]),past_key_values=cache,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1);cache,logits=o.past_key_values,o.logits[0,-1]
 guard.read('after_generate',run_id=run_id)
 return dict(run_id=run_id,prompt=prompt,input_token_ids=ids,generated_token_ids=new,text=tok.decode(new,skip_special_tokens=True),stop=stop,seconds=time.perf_counter()-started,rng_seed=seed,temperature=.8,top_p=.9)
