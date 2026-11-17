"""Prospective token-selection variant; no penalties, task scores or training."""
import time

def distribution(logits, temperature, top_p):
    import torch
    if not 0 < temperature or not 0 < top_p <= 1:
        raise ValueError('invalid sampling policy')
    if not torch.isfinite(logits).all():
        raise ValueError('nonfinite logits; stop without repair')
    probs=torch.softmax(logits / temperature,dim=-1)
    ordered,index=probs.sort(descending=True)
    keep=(ordered.cumsum(-1)-ordered)<top_p
    retained=ordered*keep
    retained=retained/retained.sum()
    return index,retained

def generate(model,tok,messages,guard,run_id,seed,temperature=0.8,top_p=0.95):
    import torch
    ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    if len(ids)>7936:raise ValueError('input capacity; no pruning')
    generator=torch.Generator(device='cpu');generator.manual_seed(seed)
    guard.read('before_generate',run_id=run_id);started=time.perf_counter();new=[];stop='token_limit'
    with torch.inference_mode():
        x=torch.tensor([ids]);out=model(input_ids=x,attention_mask=torch.ones_like(x),use_cache=True,logits_to_keep=1)
        cache,logits=out.past_key_values,out.logits[0,-1]
        for i in range(256):
            index,probs=distribution(logits,temperature,top_p)
            token=int(index[torch.multinomial(probs,1,generator=generator)[0]])
            new.append(token)
            if token==tok.eos_token_id:stop='eos';break
            if i<255:
                out=model(input_ids=torch.tensor([[token]]),past_key_values=cache,attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),use_cache=True,logits_to_keep=1)
                cache,logits=out.past_key_values,out.logits[0,-1]
    guard.read('after_generate',run_id=run_id)
    return dict(run_id=run_id,messages=messages,input_token_ids=ids,generated_token_ids=new,text=tok.decode(new,skip_special_tokens=True),stop=stop,decoder='nucleus_multinomial',temperature=temperature,top_p=top_p,seed=seed,seconds=time.perf_counter()-started)

def checks():
    import torch
    logits=torch.tensor([0.6,0.3,0.1]).log()
    idx,p=distribution(logits,1.0,0.8)
    assert idx.tolist()==[0,1,2] and torch.allclose(p,torch.tensor([2/3,1/3,0.]))
    _,p=distribution(logits,1.0,0.5);assert p.tolist()==[1.,0.,0.]
    _,p=distribution(logits,1.0,1.);assert torch.allclose(p,torch.tensor([0.6,0.3,0.1]))
    a=torch.Generator().manual_seed(17);b=torch.Generator().manual_seed(17)
    assert torch.multinomial(p,32,replacement=True,generator=a).tolist()==torch.multinomial(p,32,replacement=True,generator=b).tolist()
    try:distribution(torch.tensor([float('nan'),0.]),0.8,0.95)
    except ValueError:pass
    else:raise AssertionError('nonfinite logits accepted')
    return dict(status='pass',checks=['threshold crossing retained and renormalized','dominant token alone when sufficient','full mass at top_p1','private seed reproducibility','nonfinite logits refused'],model_calls=0)
