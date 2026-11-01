"""Public bounded greedy output; no hidden reasoning or candidate projection."""
import time
import torch

def generate(model,tok,prompt,cap,guard,run_id):
    messages=[{'role':'user','content':prompt}]
    ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    if len(ids)>768:raise ValueError('No truncation: prompt exceeds768tokens')
    guard.read('before_generate',run_id=run_id)
    began=time.perf_counter();new=[];stop='token_limit'
    with torch.inference_mode():
        x=torch.tensor([ids])
        output=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
        cache,logits=output.past_key_values,output.logits[0,-1]
        for i in range(cap):
            token=int(logits.argmax());new.append(token)
            if token==tok.eos_token_id:stop='eos';break
            if i+1<cap:
                output=model(input_ids=torch.tensor([[token]]),past_key_values=cache,
                    attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),
                    use_cache=True,logits_to_keep=1)
                cache,logits=output.past_key_values,output.logits[0,-1]
    guard.read('after_generate',run_id=run_id)
    return {'run_id':run_id,'messages':messages,'input_token_ids':ids,'generated_token_ids':new,
            'text':tok.decode(new,skip_special_tokens=True),'stop':stop,'cap':cap,
            'seconds':time.perf_counter()-began}
