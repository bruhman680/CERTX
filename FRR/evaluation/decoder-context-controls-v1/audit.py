"""Historical audit; explicit per-snapshot counters, no live feedback replay."""
import json,sys,base64,hashlib
import run as r
s=r.s;H=r.H

def bytes_at(d,bundle,name='field.bin'):
    rows={x[0]:x for x in bundle['entries']};row=rows.get(name)
    if row is None:return None
    if row[1]=='hardlink':row=rows[row[2]]
    if row[1]!='file':return None
    obj=s.read(d/'world/world/engine/objects'/(row[3]+'.json'));data=base64.b64decode(obj['base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==row[3] and len(data)==row[4]
    return data

def main(stage):
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();rows=[];calls=0;setup_total=0
    frr=(s.E/'chosen-persistence-prototype-v1/FRR_COMPACT.md').read_text();pure=r.old.old.old.observe
    for cond in ['full','mechanics']:
        for task in r.TASKS:
            d=H/(cond+'_'+task);init=s.read(d/'INITIAL_INPUT.json');state=s.read(d/'STATE.json');ref=s.read(s.E/'prerequisite-calibration-v1'/(task+'17')/'INITIAL_INPUT.json');setup=1 if task=='change' else 0
            assert state['paused'] and not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
            expected=[dict(x) for x in ref['messages']]
            if cond=='mechanics':expected[0]['content']=expected[0]['content'][len(frr+'\n\n'):].replace(r.SELF_OLD,r.SELF_NEW)
            assert init['messages']==expected and init['input_token_ids']==tok.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
            if cond=='full':assert init['input_token_ids']==ref['input_token_ids']
            assert init['observation']==ref['observation']
            before=s.read(d/'SETUP_INITIAL_SNAPSHOT.json');assert bytes_at(d,before)==b'\x01'+bytes(61)
            if setup:
                after=s.read(d/'SETUP_AFTER_SNAPSHOT.json');assert bytes_at(d,after)==b'\x00\x01'+bytes(60)
                rr0=s.read(d/'world/replies/operator_setup_tick.json');assert rr0['raw_text']=='' and rr0['actor_batch']['operations']==[] and rr0['physical_tick']['after_id']==after['id'] and rr0['physical_tick']['receipt']['exit_code']==0
                assert pure(d,before,0,dict(replies=0,ticks=0,actor_operations=0),None)==ref['observation']['before']
                assert pure(d,after,1,dict(replies=1,ticks=1,actor_operations=0),None)==ref['observation']['after']
                start=after
            else:
                assert pure(d,before,0,dict(replies=0,ticks=0,actor_operations=0),None)==ref['observation'];start=before
            setup_total+=setup
            should_run=cond=='full' or stage==2
            assert state['model_calls']==int(should_run)
            if not should_run:
                verified=s.a.c.verify(d/'world/world');assert verified['step']==setup and verified['bundle_id']==start['id']
                rows.append(dict(branch=d.name,model_calls=0,operator_setup_ticks=setup,status='prepared_unrun'));continue
            raw=s.read(d/'RAW.json');rec=s.read(d/'RECORD.json');rr=s.read(d/'world/replies/model_reply.json');batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(d/'SNAPSHOT.json')
            assert raw['messages']==expected and raw['input_token_ids']==init['input_token_ids']
            assert raw['decoder']=='greedy_argmax' and raw['temperature'] is None and raw['top_p'] is None
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rr['raw_text']==batch['raw_text']
            assert len(raw['input_token_ids'])<=7936 and 0<len(raw['generated_token_ids'])<=256
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
            assert rec['raw_sha256']==s.sha(d/'RAW.json') and rec['reply_sha256']==s.sha(d/'world/replies/model_reply.json')
            assert batch['before_id']==start['id'] and batch['start_step']==setup and batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['automatic_note_append'] is False
            cells=[x for x in batch['parsed']['cells'] if x['executable']];assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
            for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1
            assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json") and tick['after_id']==snap['id']==rec['world_id']
            clock=dict(replies=setup+1,ticks=setup+1,actor_operations=len(batch['operations']));assert s.read(d/'world/STATE.json')==clock
            assert s.read(d/'OBSERVATION.json')==pure(d,snap,tick['step'],clock,1)
            verified=s.a.c.verify(d/'world/world');assert verified['step']==tick['step'] and verified['bundle_id']==snap['id']
            assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
            note=bytes_at(d,snap,'note.txt')
            rows.append(dict(branch=d.name,condition=cond,task=task,model_calls=1,operator_setup_ticks=setup,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),actor_receipts=[op['receipt'] for op in batch['operations']],physical_exit_code=tick['receipt']['exit_code'],note_regular_file=note is not None,note_bytes=None if note is None else len(note),note_utf8=None if note is None else note.decode(errors='replace'),world_paths=[x[0] for x in snap['entries']],text=raw['text']));calls+=1
    assert calls==(3 if stage==1 else 6) and setup_total==2
    out=dict(status='pass',stage=stage,actual_model_calls=calls,actual_operator_setup_ticks=setup_total,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,old_gardens_unchanged=True,cleanly_paused=True)
    s.save(H/('AUDIT_STAGE1.json' if stage==1 else 'RESULTS.json'),out);print(json.dumps(out,indent=2))
if __name__=='__main__':main(int(sys.argv[1]))
