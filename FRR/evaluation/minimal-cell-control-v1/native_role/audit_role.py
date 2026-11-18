"""Audit additive native-preface control, preserving both parent cases."""
from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import run_role as r
s=r.s

def main():
    r.guard();assert not (R/'RUN.lock').exists() and not (R/'PENDING.json').exists();tok=s.c.tokenizer()
    init=s.read(R/'INITIAL_INPUT.json');full=s.read(r.H/'full/INITIAL_INPUT.json');native=s.read(r.H/'native/INITIAL_INPUT.json');prefix=native['rendered_chat'].split('<|im_start|>system\n',1)[1].split('<|im_end|>',1)[0]
    assert init['messages']==[{'role':'system','content':prefix+'\n\n'+full['messages'][0]['content']},full['messages'][1]]
    raw=s.read(R/'RAW.json');assert raw['messages']==init['messages'] and raw['input_token_ids']==init['input_token_ids']==tok.apply_chat_template(init['messages'],tokenize=True,add_generation_prompt=True)
    assert init['rendered_chat']==tok.apply_chat_template(init['messages'],tokenize=False,add_generation_prompt=True)
    assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'] and raw['decoder']=='greedy_argmax'
    assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
    assert s.read(R/'STATE.json')==dict(model_calls=1,paused=True)
    rr=s.read(R/'world/replies/operator_verification.json');batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(R/'SNAPSHOT.json');before=s.read(R/'INITIAL_SNAPSHOT.json')
    assert before==s.read(r.H/'full/INITIAL_SNAPSHOT.json') and batch['before_id']==before['id'] and batch['start_step']==0
    assert batch['raw_text']==raw['text'] and batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['automatic_note_append'] is False
    cells=[c for c in batch['parsed']['cells'] if c['executable']];assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
    for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
    assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1 and tick['after_id']==snap['id']
    assert tick==s.read(R/'world/world/engine/events'/f"{tick['step']:06d}.json")
    v=s.a.c.verify(R/'world/world');assert v['step']==tick['step'] and v['bundle_id']==snap['id']
    assert s.read(R/'world/world/engine/STATE.json')['paused'] and not (R/'world/PENDING.json').exists() and not (R/'world/world/engine/LOCK.json').exists()
    assert s.read(R/'world/STATE.json')==dict(replies=1,ticks=1,actor_operations=len(batch['operations']))
    verification=s.read(R/'VERIFICATION.json');assert verification['complete_cells']==len(batch['operations']) and verification['actual_operator_executed_cells']==bool(batch['operations']) and verification['reply_sha256']==s.sha(R/'world/replies/operator_verification.json')
    ops=batch['operations'];task_met=len(ops)==1 and ops[0]['channel']=='python' and ops[0]['receipt']['exit_code']==0 and ops[0]['receipt']['stdout'] in ('1','1\n') and ops[0]['receipt']['stderr']=='' and ops[0]['receipt']['boundary'] is None
    result=dict(status='pass',actual_model_calls=1,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],text=raw['text'],actual_cells=len(ops),runtime_receipts=[op['receipt'] for op in ops],physical_exit_code=tick['receipt']['exit_code'],task_met=task_met,parent_files_unchanged=len(r.parent_cases()),protected_prior_files_unchanged=len(r.parent.protected()),training_updates=0,autonomous_action_claim=False,cleanly_paused=True)
    s.save(R/'RESULTS.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
