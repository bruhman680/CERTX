"""External audit; inherited fork records are not counted as new calls."""
import json,sys,re
import run as r
s=r.s;H=r.H

def main(stage):
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();source=s.read(s.E/'observation-three-contact-v1/rle17/INITIAL_INPUT.json');seed_bundle=s.read(s.E/'byte-medium-model-pilot-v1/seed/bundle.json');rows=[];total=0
    names=[n for n,q,seed in r.BRANCHES]
    if stage==2:names+=['named17_silent','named17_question','named29_silent','named29_question']
    for name in names:
        d=H/name;init=r.initial_plan(d);state=s.read(d/'STATE.json');fork=s.read(d/'FORK.json') if (d/'FORK.json').exists() else None
        assert state['turn']==(2 if fork else 1) and state['paused']
        assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        assert init['messages'][0]['content']==source['messages'][0]['content']+'\n\n'+r.DISCLOSURE
        assert init['messages'][1]['content']==s.text(init['observation'])+'\n\n'+init['question']
        assert init['observation']==source['observation'] and init['input_token_ids']==tok.apply_chat_template(init['messages'],tokenize=True,add_generation_prompt=True)
        if fork:
            parent=H/PathName(fork['source'])
            assert s.sha(d/'raw/000001.json')==fork['source_first_raw_sha256']==s.sha(parent/'raw/000001.json')
            assert s.sha(d/'records/000001.json')==fork['source_first_record_sha256']==s.sha(parent/'records/000001.json')
            assert s.sha(parent/'world/STATE.json')==fork['source_world_state_sha256']
            assert s.read(d/'world/world/engine/bundles/000001.json')==s.read(parent/'world/world/engine/bundles/000001.json')
        ms=init['messages'];previous=seed_bundle;step=0;last=None;actor_total=0;new_actors=0;out=[]
        assert len(list((d/'records').glob('*.json')))==state['turn']
        for n in range(1,state['turn']+1):
            label=f'{n:06d}';raw=s.read(d/'raw'/(label+'.json'));plan=s.read(d/'plans'/(label+'.json'));rec=s.read(d/'records'/(label+'.json'));rr=s.read(d/'world/replies'/('reply_'+label+'.json'));snap=s.read(d/'snapshots'/(label+'.json'));batch=rr['actor_batch'];tick=rr['physical_tick']
            assert raw['messages']==plan['messages']==ms and raw['input_token_ids']==plan['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            assert raw['decoder']=='nucleus_multinomial' and raw['seed']==init['seed'] and raw['temperature']==0.8 and raw['top_p']==0.95
            expected_rng=None if n==1 else s.a.fingerprint(s.text(s.read(d/'raw/000001.json')['rng_state_after']))
            assert plan['rng_state_before_sha256']==expected_rng
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rec['text']==rr['raw_text']==batch['raw_text']
            assert len(raw['input_token_ids'])<=7936 and 0<len(raw['generated_token_ids'])<=256
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
            assert rec['raw_sha256']==s.sha(d/'raw'/(label+'.json')) and rec['adapter_reply_sha256']==s.sha(d/'world/replies'/('reply_'+label+'.json')) and rec['parent_record_sha256']==last
            assert batch['before_id']==previous['id'] and batch['start_step']==step and batch['automatic_note_append'] is False and batch['parsed']==s.a.base.parse_notebook(raw['text'])
            cells=[c for c in batch['parsed']['cells'] if c['executable']];assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
            for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1
            assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json") and tick['after_id']==snap['id']==rec['world_id']
            assert 'seconds' in tick['receipt']
            clock_at_turn=dict(replies=n,ticks=n,actor_operations=actor_total+len(batch['operations']));assert rr['after_state']==clock_at_turn
            packet=r.old.observe(d,snap,tick['step'],clock_at_turn,n)
            fb=s.text(dict(actor_feedback={'boundary':batch['boundary'],'receipts':[r.model_receipt(op['receipt']) for op in batch['operations']]},physical_feedback=r.model_receipt(tick['receipt']),**packet))
            assert rec['feedback']==fb and len(fb.encode())<=8192
            parsed=json.loads(fb);assert 'seconds' not in parsed['physical_feedback'] and all('seconds' not in op for op in parsed['actor_feedback']['receipts'])
            actor_total+=len(batch['operations']);is_new=not fork or n==2
            if is_new:new_actors+=len(batch['operations'])
            out.append(dict(turn=n,inherited=not is_new,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),physical_exit_code=tick['receipt']['exit_code'],exact_latest_packet_copy=raw['text']==ms[-1]['content'],text_start=raw['text'][:360]))
            user=fb
            if n==1 and fork and fork['question']:user+='\n\n'+r.FOLLOWUP
            ms=ms+[{'role':'assistant','content':raw['text']},{'role':'user','content':user}];previous=snap;step=tick['step'];last=s.sha(d/'records'/(label+'.json'))
        assert state['last_record_sha256']==last and s.read(d/'world/STATE.json')==dict(replies=state['turn'],ticks=state['turn'],actor_operations=actor_total)
        assert ms==r.messages(d)
        verified=s.a.c.verify(d/'world/world');assert verified['step']==step and verified['bundle_id']==previous['id']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        new_calls=state['turn']-(1 if fork else 0);total+=new_calls
        rows.append(dict(branch=name,turns=state['turn'],inherited_calls=1 if fork else 0,new_model_calls=new_calls,new_actor_operations=new_actors,world_paths=[x[0] for x in previous['entries']],next_input_tokens=len(tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)),outputs=out))
    if stage==2:
        for seed in [17,29]:
            a=H/f'named{seed}_silent';b=H/f'named{seed}_question';aa=s.read(a/'plans/000002.json');bb=s.read(b/'plans/000002.json')
            assert aa['messages'][:-1]==bb['messages'][:-1] and bb['messages'][-1]['content']==aa['messages'][-1]['content']+'\n\n'+r.FOLLOWUP
            assert aa['rng_state_before_sha256']==bb['rng_state_before_sha256']
            assert s.read(a/'world/world/engine/bundles/000001.json')==s.read(b/'world/world/engine/bundles/000001.json')
    assert total==(4 if stage==1 else 8)
    result=dict(status='pass',stage=stage,actual_new_model_calls=total,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,cleanly_paused=True,raw_receipts_preserved=True,timing_metadata_excluded_from_model_view=True)
    s.save(H/('RESULTS.json' if stage==2 else 'AUDIT_STAGE1.json'),result);print(json.dumps(result,indent=2))

def PathName(path):
    from pathlib import Path
    return Path(path).name
if __name__=='__main__':main(int(sys.argv[1]))
