"""External exact-history/world audit, without model generation or execution."""
import json,re
from collections import Counter
import run as r
s=r.s;H=r.H

def main():
    r.guard();assert not (H/'RUN.lock').exists();tok=s.c.tokenizer()
    prior=s.read(s.E/'observation-three-contact-v1/rle17/INITIAL_INPUT.json');seed_bundle=s.read(s.E/'byte-medium-model-pilot-v1/seed/bundle.json');rows=[];total=0
    for name,invited,seed in r.BRANCHES:
        d=H/name;state=s.read(d/'STATE.json');initial=s.read(d/'INITIAL_INPUT.json')
        assert state['turn']==2 and state['paused'];assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        assert initial['messages'][0]==prior['messages'][0]
        assert initial['messages'][1]['content']==s.text(initial['observation'])+('\n\n'+(H/'INVITATION.txt').read_text().strip() if invited else '')
        assert initial['observation']==prior['observation'] and initial['input_token_ids']==tok.apply_chat_template(initial['messages'],tokenize=True,add_generation_prompt=True)
        ms=initial['messages'];last=None;previous=seed_bundle;step=0;actors=0;out=[]
        assert len(list((d/'records').glob('*.json')))==2
        for n in range(1,3):
            label=f'{n:06d}';raw=s.read(d/'raw'/(label+'.json'));rec=s.read(d/'records'/(label+'.json'));rr=s.read(d/'world/replies'/('reply_'+label+'.json'));snap=s.read(d/'snapshots'/(label+'.json'));batch=rr['actor_batch'];tick=rr['physical_tick']
            assert raw['messages']==ms and raw['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            assert raw['decoder']=='nucleus_multinomial' and raw['seed']==seed and raw['temperature']==0.8 and raw['top_p']==0.95
            assert len(raw['rng_state_after'])>0
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==rec['text']==rr['raw_text']==batch['raw_text']
            assert len(raw['input_token_ids'])<=7936 and 0<len(raw['generated_token_ids'])<=256
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
            assert rec['raw_sha256']==s.sha(d/'raw'/(label+'.json')) and rec['adapter_reply_sha256']==s.sha(d/'world/replies'/('reply_'+label+'.json')) and rec['parent_record_sha256']==last
            assert batch['before_id']==previous['id'] and batch['start_step']==step and batch['automatic_note_append'] is False and batch['parsed']==s.a.base.parse_notebook(raw['text'])
            cells=[x for x in batch['parsed']['cells'] if x['executable']]
            assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
            for op,cell in zip(batch['operations'],cells):assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1
            assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json") and tick['after_id']==snap['id']==rec['world_id']
            actors+=len(batch['operations']);clock=dict(replies=n,ticks=n,actor_operations=actors);assert rr['after_state']==clock
            packet=r.observe(d,snap,tick['step'],clock,n)
            feedback=s.text(dict(actor_feedback={'boundary':batch['boundary'],'receipts':[op['receipt'] for op in batch['operations']]},physical_feedback=tick['receipt'],**packet))
            assert rec['feedback']==feedback and len(feedback.encode())<=8192
            pieces=re.split(r'(?<=[.!?])\s+',raw['text']);_,count=Counter(pieces).most_common(1)[0]
            replay=None
            if not invited and (seed==17 or n==1):
                oldname='rle'+str(seed);oldraw=s.read(s.E/'observation-three-contact-v1'/oldname/'raw'/(label+'.json'));replay=raw['generated_token_ids']==oldraw['generated_token_ids'];assert replay
            out.append(dict(turn=n,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),actor_exit_codes=[op['receipt']['exit_code'] for op in batch['operations']],physical_exit_code=tick['receipt']['exit_code'],exact_latest_packet_copy=raw['text']==ms[-1]['content'],dominant_sentence_occurrences=count,longest_zero_run=max([len(z) for z in re.findall('0+',raw['text'])]+[0]),prior_token_replay_match=replay,text_start=raw['text'][:360]))
            ms=ms+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}];last=s.sha(d/'records'/(label+'.json'));previous=snap;step=tick['step']
        assert state['last_record_sha256']==last and s.read(d/'world/STATE.json')==dict(replies=2,ticks=2,actor_operations=actors)
        verified=s.a.c.verify(d/'world/world');assert verified['bundle_id']==previous['id'] and verified['step']==step
        assert s.read(d/'world/world/engine/STATE.json')['paused'] and not (d/'world/world/engine/LOCK.json').exists()
        rows.append(dict(branch=name,invited=invited,seed=seed,turns=2,actor_operations=actors,world_paths=[x[0] for x in previous['entries']],next_input_tokens=len(tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)),outputs=out));total+=2
    result=dict(status='pass',model_calls=total,branches=rows,protected_files_unchanged=len(r.protected()),training_updates=0,old_gardens_unchanged=True,cleanly_paused=True,sensor_v2_activated_in_this_new_contract_only=True)
    s.save(H/'RESULTS.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
