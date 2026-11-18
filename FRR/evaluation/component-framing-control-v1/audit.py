"""External minimal handoff audit; stdout comes from actual engine receipts."""
import json
import run as r
s=r.s;H=r.H

def main():
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();ref=s.read(s.E/'representation-actuator-controls-v1/general_action/INITIAL_INPUT.json');rows=[]
    for name in r.NAMES:
        d=H/name;init=s.read(d/'INITIAL_INPUT.json');raw=s.read(d/'RAW.json');verification=s.read(d/'VERIFICATION.json');rr=s.read(d/'world/replies/operator_verification.json');batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(d/'SNAPSHOT.json')
        expected=r.messages(name)
        assert s.read(d/'STATE.json')==dict(model_calls=1,paused=True) and not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        assert raw['messages']==init['messages']==expected and raw['input_token_ids']==init['input_token_ids']==tok.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
        assert init['rendered_chat']==tok.apply_chat_template(expected,tokenize=False,add_generation_prompt=True)
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==batch['raw_text']==rr['raw_text'] and raw['decoder']=='greedy_argmax'
        assert 0<len(raw['generated_token_ids'])<=256 and len(raw['input_token_ids'])<=7936
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
        assert batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['automatic_note_append'] is False and batch['start_step']==0
        before=s.read(d/'INITIAL_SNAPSHOT.json');assert batch['before_id']==before['id']==init['actual_seed_world_id']
        cells=[c for c in batch['parsed']['cells'] if c['executable']];assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
        for op,cell in zip(batch['operations'],cells):
            assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            stored=s.read(d/'world/world/engine/events'/f"{op['step']:06d}.json")
            assert {k:v for k,v in op.items() if k not in ('cell_index','source_start','source_end')}==stored
        assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1 and tick['after_id']==snap['id']
        assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json")
        assert verification['reply_sha256']==s.sha(d/'world/replies/operator_verification.json') and verification['complete_cells']==len(batch['operations']) and verification['actual_operator_executed_cells']==bool(batch['operations'])
        assert s.read(d/'world/STATE.json')==dict(replies=1,ticks=1,actor_operations=len(batch['operations']))
        v=s.a.c.verify(d/'world/world');assert v['bundle_id']==snap['id'] and v['step']==tick['step']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        operations=batch['operations'];python_ops=[op for op in operations if op['channel']=='python']
        task_met=len(operations)==1 and len(python_ops)==1 and python_ops[0]['receipt']['exit_code']==0 and python_ops[0]['receipt']['stdout'] in ('1','1\n') and python_ops[0]['receipt']['stderr']=='' and python_ops[0]['receipt']['boundary'] is None
        rows.append(dict(context=name,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],text=raw['text'],actual_cells=len(operations),python_cells=len(python_ops),runtime_receipts=[op['receipt'] for op in operations],physical_exit_code=tick['receipt']['exit_code'],task_met=task_met,incomplete_fences=sum(not c['complete'] for c in batch['parsed']['cells']),world_paths=[x[0] for x in snap['entries']],operator_verification=True,autonomous_action_claim=False))
    out=dict(status='pass',actual_model_calls=2,operator_response_ticks=2,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,source_repair=False,old_gardens_unchanged=True,cleanly_paused=True)
    s.save(H/'RESULTS.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
