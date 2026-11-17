"""External trajectory/physics audit; no generation or world execution."""
import json,re,sys
from collections import Counter
import run as r
s=r.s;H=r.H

def audit(stage):
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();rows=[];total=0
    original=s.read(s.E/'byte-medium-model-pilot-v1/changing/INITIAL_INPUT.json')
    seed=s.read(s.E/'byte-medium-model-pilot-v1/seed/bundle.json')
    for name,style,seed_id in r.BRANCHES:
        d=H/name;state=s.read(d/'STATE.json');initial=s.read(d/'INITIAL_INPUT.json');assert state['paused']
        assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        assert initial['messages'][0]['content'].replace(r.NEW_SENSOR[style],r.OLD_SENSOR)==original['messages'][0]['content']
        assert initial['input_token_ids']==tok.apply_chat_template(initial['messages'],tokenize=True,add_generation_prompt=True)
        previous=seed;step=0;ms=initial['messages'];last=None;actors=0;outputs=[]
        assert initial['observation']==r.observe(d,seed,0,dict(replies=0,ticks=0,actor_operations=0),None,style)
        assert len(list((d/'records').glob('*.json')))==state['turn']
        for n in range(1,state['turn']+1):
            label=f'{n:06d}';raw=s.read(d/'raw'/(label+'.json'));rec=s.read(d/'records'/(label+'.json'));rr=s.read(d/'world/replies'/('reply_'+label+'.json'));snap=s.read(d/'snapshots'/(label+'.json'))
            batch=rr['actor_batch'];tick=rr['physical_tick']
            assert raw['messages']==ms and raw['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            assert raw['decoder']=='nucleus_multinomial' and raw['seed']==seed_id and raw['temperature']==0.8 and raw['top_p']==0.95
            assert isinstance(raw['rng_state_after'],list) and len(raw['rng_state_after'])>0
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rec['text']==rr['raw_text']==batch['raw_text']
            assert 0<len(raw['generated_token_ids'])<=256 and len(raw['input_token_ids'])<=7936
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
            assert rec['raw_sha256']==s.sha(d/'raw'/(label+'.json')) and rec['adapter_reply_sha256']==s.sha(d/'world/replies'/('reply_'+label+'.json')) and rec['parent_record_sha256']==last
            assert batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['before_id']==previous['id'] and batch['start_step']==step and batch['automatic_note_append'] is False
            cells=[x for x in batch['parsed']['cells'] if x['executable']]
            assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
            for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1
            assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json") and tick['after_id']==snap['id']==rec['world_id']
            actors+=len(batch['operations']);clock=dict(replies=n,ticks=n,actor_operations=actors)
            assert rr['after_state']==clock
            packet=r.observe(d,snap,tick['step'],clock,n,style)
            feedback=s.text(dict(actor_feedback={'boundary':batch['boundary'],'receipts':[op['receipt'] for op in batch['operations']]},physical_feedback=tick['receipt'],**packet))
            assert rec['feedback']==feedback and len(feedback.encode())<=8192
            pieces=re.split(r'(?<=[.!?])\s+',raw['text']);dominant,count=Counter(pieces).most_common(1)[0]
            outputs.append(dict(turn=n,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),physical_exit_code=tick['receipt']['exit_code'],dominant_sentence_occurrences=count,longest_zero_run=max([len(x) for x in re.findall('0+',raw['text'])]+[0]),exact_latest_packet_copy=raw['text']==ms[-1]['content'],text_start=raw['text'][:240]))
            ms=ms+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}];previous=snap;step=tick['step'];last=s.sha(d/'records'/(label+'.json'))
        assert state['last_record_sha256']==last
        assert s.read(d/'world/STATE.json')==dict(replies=state['turn'],ticks=state['turn'],actor_operations=actors)
        verified=s.a.c.verify(d/'world/world');assert verified['step']==step and verified['bundle_id']==previous['id']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        rows.append(dict(branch=name,style=style,seed=seed_id,turns=state['turn'],actor_operations=actors,world_paths=[x[0] for x in previous['entries']],next_input_tokens=len(tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)),outputs=outputs));total+=state['turn']
    expected={1:2,2:4,3:6}[stage];assert total==expected
    if stage==3:
        chosen=s.read(H/'STAGE3_SELECTION.json')['branch'];assert chosen==r.selection()
        assert next(x['turns'] for x in rows if x['branch']==chosen)==3
    out=dict(status='pass',stage=stage,model_calls=total,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,old_gardens_unchanged=True,cleanly_paused=True)
    savepath=H/('RESULTS.json' if stage==3 else f'AUDIT_STAGE{stage}.json');s.save(savepath,out);print(json.dumps(out,indent=2))

if __name__=='__main__':audit(int(sys.argv[1]))
