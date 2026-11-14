"""Deterministic, content-independent recent-pair view. No archive mutation."""
from copy import deepcopy

class ViewCapacity(ValueError):
    pass

def select_view(initial, exchanges, tokenizer, *, max_pairs=8, max_input=7936):
    if type(max_pairs) is not int or max_pairs<1 or type(max_input) is not int or max_input<1:
        raise ValueError('Positive integer limits required')
    if len(initial)!=2 or initial[0].get('role')!='system' or initial[1].get('role')!='user':
        raise ValueError('Exact two-message initial framing required')
    if any(type(m.get('content')) is not str for m in initial):
        raise ValueError('Initial message text required')
    ids=[]
    for x in exchanges:
        if set(x)!={'entry','assistant','receipt'} or type(x['entry']) is not int or type(x['assistant']) is not str or type(x['receipt']) is not str:
            raise ValueError('Complete identified assistant/receipt pair required')
        ids.append(x['entry'])
    if any(b<=a for a,b in zip(ids,ids[1:])):
        raise ValueError('Strictly ordered unique entries required')
    start=max(0,len(exchanges)-max_pairs)
    while True:
        selected=exchanges[start:]
        messages=deepcopy(initial)
        for x in selected:
            messages.extend([{'role':'assistant','content':x['assistant']},{'role':'user','content':x['receipt']}])
        tokens=tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        if len(tokens)<=max_input:
            return {'messages':messages,'input_token_ids':tokens,'included_entries':ids[start:],
                'omitted_entries':ids[:start],'policy':'latest complete contiguous pairs; oldest-first budget fallback',
                'max_pairs':max_pairs,'max_input':max_input,'archive_exchanges':len(exchanges),
                'summaries_added':False,'receipt_text_modified':False,'mandatory_latest_pair_preserved':bool(selected) or not exchanges}
        if len(selected)<=1:
            raise ViewCapacity('Initial framing plus latest complete pair exceeds input capacity; no truncation')
        start+=1
