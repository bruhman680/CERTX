"""External prerequisite-probe audit; no inference or world execution."""
import json,base64,hashlib
import run as r
s=r.s;H=r.H

def material(d,bundle):
    rows={x[0]:x for x in bundle['entries']};row=rows.get('field.bin')
    if row is None:return None
    if row[1]=='hardlink':row=rows[row[2]]
    if row[1]!='file':return None
    obj=s.read(d/'world/world/engine/objects'/(row[3]+'.json'));data=base64.b64decode(obj['base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==row[3] and len(data)==row[4]
    return data

def main():
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();rows=[];setup_count=0
    expected_system=s.read(s.E/'object-evidence-contact-v1/named17/INITIAL_INPUT.json')['messages'][0]['content']
    pure=r.old.old.observe
    for name,task,seed in r.BRANCHES:
        d=H/name;init=s.read(d/'INITIAL_INPUT.json');assert s.read(d/'STATE.json')==dict(model_calls=1,paused=True)
        assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        raw=s.read(d/'RAW.json');rec=s.read(d/'RECORD.json');rr=s.read(d/'world/replies/model_reply.json');batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(d/'SNAPSHOT.json');setup=1 if task=='change' else 0
        assert init['setup_model_calls']==0 and init['operator_setup_ticks']==setup
        first_bundle=s.read(d/'SETUP_INITIAL_SNAPSHOT.json');first=pure(d,first_bundle,0,dict(replies=0,ticks=0,actor_operations=0),None)
        assert material(d,first_bundle)==b'\x01'+bytes(61)
        if setup:
            setup_rr=s.read(d/'world/replies/operator_setup_tick.json');assert setup_rr['raw_text']=='' and setup_rr['actor_batch']['operations']==[] and setup_rr['physical_tick']['receipt']['exit_code']==0
            after_bundle=s.read(d/'SETUP_AFTER_SNAPSHOT.json');assert material(d,after_bundle)==b'\x00\x01'+bytes(60)
            assert setup_rr['physical_tick']['after_id']==after_bundle['id']
            after=pure(d,after_bundle,1,dict(replies=1,ticks=1,actor_operations=0),None)
            user=s.text(dict(before=first,after=after))+'\n\nThe after observation follows one actual operator preparation tick; no model action preceded it.\n\n'+r.QUESTIONS[task]
            observation=dict(before=first,after=after);start=after_bundle
        else:user=s.text(first)+'\n\n'+r.QUESTIONS[task];observation=first;start=first_bundle
        assert init['messages']==[{'role':'system','content':expected_system},{'role':'user','content':user}] and init['observation']==observation
        assert raw['messages']==init['messages'] and raw['input_token_ids']==init['input_token_ids']==tok.apply_chat_template(init['messages'],tokenize=True,add_generation_prompt=True)
        assert raw['decoder']=='nucleus_multinomial' and raw['seed']==seed and raw['temperature']==0.8 and raw['top_p']==0.95
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rr['raw_text']==batch['raw_text']
        assert len(raw['input_token_ids'])<=7936 and 0<len(raw['generated_token_ids'])<=256
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
        assert rec['raw_sha256']==s.sha(d/'RAW.json') and rec['reply_sha256']==s.sha(d/'world/replies/model_reply.json')
        assert batch['before_id']==start['id'] and batch['start_step']==setup and batch['automatic_note_append'] is False and batch['parsed']==s.a.base.parse_notebook(raw['text'])
        cells=[x for x in batch['parsed']['cells'] if x['executable']];assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
        for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
        assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1
        assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json") and tick['after_id']==snap['id']==rec['world_id']
        clock=dict(replies=setup+1,ticks=setup+1,actor_operations=len(batch['operations']));assert s.read(d/'world/STATE.json')==clock
        assert s.read(d/'OBSERVATION.json')==pure(d,snap,tick['step'],clock,1)
        verified=s.a.c.verify(d/'world/world');assert verified['step']==tick['step'] and verified['bundle_id']==snap['id']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        entries={x[0]:x for x in snap['entries']};note=entries.get('note.txt');note_data=None
        if note is not None:
            if note[1]=='hardlink':note=entries[note[2]]
            if note[1]=='file':note_data=base64.b64decode(s.read(d/'world/world/engine/objects'/(note[3]+'.json'))['base64'],validate=True)
        rows.append(dict(branch=name,task=task,seed=seed,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),actor_receipts=[op['receipt'] for op in batch['operations']],physical_exit_code=tick['receipt']['exit_code'],note_regular_file=note_data is not None,note_bytes=None if note_data is None else len(note_data),note_utf8=None if note_data is None else note_data.decode(errors='replace'),world_paths=list(entries),text=raw['text']))
        setup_count+=setup
    out=dict(status='pass',actual_model_calls=6,actual_operator_setup_ticks=setup_count,model_reply_physical_ticks=6,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,cleanly_paused=True,old_gardens_unchanged=True)
    s.save(H/'RESULTS.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':main()
