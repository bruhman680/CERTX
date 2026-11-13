"""Candidate model body. No loading/inference on import; no training."""
import time

MAX_INPUT = 7936
MAX_OUTPUT = 256

def generate(model, tokenizer, messages, guard, run_id):
    import torch
    ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    if len(ids) > MAX_INPUT:
        raise ValueError('Exact context capacity reached; no truncation or summary')
    guard.read('before_generate', run_id=run_id)
    started = time.perf_counter()
    new, stop = [], 'token_limit'
    with torch.inference_mode():
        x = torch.tensor([ids])
        out = model(input_ids=x, attention_mask=torch.ones_like(x), use_cache=True, logits_to_keep=1)
        cache, logits = out.past_key_values, out.logits[0,-1]
        for index in range(MAX_OUTPUT):
            token = int(logits.argmax())
            new.append(token)
            if token == tokenizer.eos_token_id:
                stop = 'eos'
                break
            if index < MAX_OUTPUT - 1:
                out = model(input_ids=torch.tensor([[token]]), past_key_values=cache,
                    attention_mask=torch.ones((1,cache.get_seq_length()+1), dtype=torch.long),
                    use_cache=True, logits_to_keep=1)
                cache, logits = out.past_key_values, out.logits[0,-1]
    guard.read('after_generate', run_id=run_id)
    return {'run_id':run_id,'messages':messages,'input_token_ids':ids,
        'generated_token_ids':new,'text':tokenizer.decode(new,skip_special_tokens=True),
        'stop':stop,'decoder':'greedy_argmax','temperature':None,'top_p':None,
        'seconds':time.perf_counter()-started}
