"""External exact-input/effect audit; no model generation or execution."""
import json,sys,base64,hashlib
import run as r
s=r.s;H=r.H

def data(d,bundle,name='field.bin'):
    rows={x[0]:x for x in bundle['entries']};row=rows.get(name)
    if row is None:return None
    if row[1]=='hardlink':row=rows[row[2]]
    if row[1]!='file':return None
    obj=s.read(d/'world/world/engine/objects'/(row[3]+'.json'));raw=base64.b64decode(obj['base64'],validate=True)
    assert hashlib.sha256(raw).hexdigest()==row[3] and len(raw)==row[4]
    return raw

def main():
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer();pure=r.old.old.old.old.observe;rows=[]
    for name,task,treatment in r.CASES:
        d=H/name;init=s.read(d/'INITIAL_INPUT.json');state=s.read(d/'STATE.json');ref=s.read(s.E/'decoder-context-controls-v1'/('full_'+task)/'INITIAL_INPUT.json')
        assert state==dict(model_calls=1,paused=True) and not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        ms=[dict(x) for x in ref['messages']];obs=ref['observation'];setup=int(task=='change')
        if name=='array_change':
            ms[0]['content']=ms[0]['content'].replace(r.SENSOR_OLD,r.SENSOR_NEW);obs={label:r.array_packet(packet) for label,packet in obs.items()};ms[1]['content']=s.text(obs)+ref['messages'][1]['content'][len(s.text(ref['observation'])):]
        elif name=='python_action':
            question=r.old.old.QUESTIONS['action'];ms[1]['content']=ms[1]['content'][:-len(question)]+r.ACTION
        assert init['messages']==ms and init['observation']==obs and init['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
        before=s.read(d/'SETUP_INITIAL_SNAPSHOT.json');assert data(d,before)==b'\x01'+bytes(61)
        if setup:
            after=s.read(d/'SETUP_AFTER_SNAPSHOT.json');assert data(d,after)==b'\x00\x01'+bytes(60)
            sr=s.read(d/'world/replies/operator_setup_tick.json');assert sr['raw_text']=='' and sr['actor_batch']['operations']==[] and sr['physical_tick']['after_id']==after['id'] and sr['physical_tick']['receipt']['exit_code']==0
            for label,bundle,step,clock in [('before',before,0,dict(replies=0,ticks=0,actor_operations=0)),('after',after,1,dict(replies=1,ticks=1,actor_operations=0))]:
                packet=pure(d,bundle,step,clock,None)
                if name=='array_change':packet=r.array_packet(packet);assert bytes(packet['material']['values'])==data(d,bundle)
                assert init['observation'][label]==packet
            start=after
        else:
            assert init['observation']==pure(d,before,0,dict(replies=0,ticks=0,actor_operations=0),None);start=before
        raw=s.read(d/'RAW.json');rec=s.read(d/'RECORD.json');rr=s.read(d/'world/replies/model_reply.json');batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(d/'SNAPSHOT.json')
        assert raw['messages']==ms and raw['input_token_ids']==init['input_token_ids'] and raw['decoder']=='greedy_argmax'
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
        packet=pure(d,snap,tick['step'],clock,1)
        if name=='array_change':packet=r.array_packet(packet)
        assert s.read(d/'OBSERVATION.json')==packet
        verified=s.a.c.verify(d/'world/world');assert verified['step']==tick['step'] and verified['bundle_id']==snap['id']
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        replay=None
        if not treatment:
            prior=s.read(s.E/'decoder-context-controls-v1'/('full_'+task)/'RAW.json');assert raw['input_token_ids']==prior['input_token_ids'];replay=raw['generated_token_ids']==prior['generated_token_ids'];assert replay
        note=data(d,snap,'note.txt')
        rows.append(dict(branch=name,task=task,treatment=treatment,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],exact_baseline_token_replay=replay,complete_executable_cells=len(cells),incomplete_fences=sum(not c['complete'] for c in batch['parsed']['cells']),actor_operations=len(batch['operations']),actor_receipts=[op['receipt'] for op in batch['operations']],physical_exit_code=tick['receipt']['exit_code'],note_regular_file=note is not None,note_bytes=None if note is None else len(note),note_utf8=None if note is None else note.decode(errors='replace'),world_paths=[x[0] for x in snap['entries']],text=raw['text']))
    result=dict(status='pass',actual_model_calls=4,operator_preparation_ticks=2,model_response_ticks=4,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,old_gardens_unchanged=True,cleanly_paused=True)
    s.save(H/'RESULTS.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
