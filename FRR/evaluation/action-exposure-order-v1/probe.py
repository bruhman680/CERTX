"""Greedy free output and separate complete-choice likelihood; no gold inputs."""
import time
import torch
import torch.nn.functional as F

def probe(model, tok, text, choices, guard, probe_id):
    model.eval()
    messages = [{'role': 'user', 'content': text}]
    ids = tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    if len(ids) > 256:
        raise ValueError('No truncation: prompt exceeds frozen256token guard')
    suffixes = {key: tok.encode(label, add_special_tokens=False)+[tok.eos_token_id] for key, label in choices.items()}
    guard.read('before_probe', probe_id=probe_id)
    start = time.perf_counter()
    with torch.inference_mode():
        x = torch.tensor([ids])
        out = model(input_ids=x, attention_mask=torch.ones_like(x), use_cache=True)
        cache, logits = out.past_key_values, out.logits[0, -1]
        generated, stop = [], 'token_limit'
        for i in range(8):
            token = int(logits.argmax()); generated.append(token)
            if token == tok.eos_token_id:
                stop = 'eos'; break
            if i < 7:
                out = model(input_ids=torch.tensor([[token]]), past_key_values=cache,
                    attention_mask=torch.ones((1, cache.get_seq_length()+1), dtype=torch.long), use_cache=True)
                cache, logits = out.past_key_values, out.logits[0, -1]
        del out, cache
        lengths = [len(ids)+len(t) for t in suffixes.values()]
        x = torch.full((len(choices), max(lengths)), tok.eos_token_id)
        mask = torch.zeros_like(x)
        for i, t in enumerate(suffixes.values()):
            seq = ids+t; x[i, :len(seq)] = torch.tensor(seq); mask[i, :len(seq)] = 1
        out = model(input_ids=x, attention_mask=mask, use_cache=False)
        scores = {}
        for i, (key, t) in enumerate(suffixes.items()):
            logp = F.log_softmax(out.logits[i, len(ids)-1:len(ids)+len(t)-1].float(), dim=-1)
            lp = logp.gather(1, torch.tensor(t).view(-1, 1)).flatten().tolist()
            scores[key] = {'label': choices[key], 'ids': t, 'token_logprobs': lp, 'sum': sum(lp), 'mean': sum(lp)/len(lp)}
        del out, x, mask
    result = tok.decode(generated, skip_special_tokens=True)
    inverse = {v: k for k, v in choices.items()}
    best = max(choices, key=lambda k: scores[k]['sum'])
    guard.read('after_probe', probe_id=probe_id)
    return {'probe_id': probe_id, 'messages': messages, 'input_token_ids': ids,
            'generated_token_ids': generated, 'text': result, 'stop': stop,
            'free_key': inverse.get(result.strip()), 'forced_key': best,
            'forced_tied': sum(s['sum'] == scores[best]['sum'] for s in scores.values()) > 1,
            'scores': scores, 'seconds': time.perf_counter()-start}
