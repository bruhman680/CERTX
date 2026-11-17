"""External replay audit, with no model call or world execution."""
from pathlib import Path
import json
import session as s
H=s.H

def main():
    s.guard();tok=s.c.tokenizer();result=[]
    assert not (H/'RUN.lock').exists()
    for mode in ['static','changing']:
        d=H/mode;state=s.read(d/'STATE.json');assert state['paused'] and state['stop_reason'] is None
        assert not (d/'PENDING.json').exists() and not (d/'world/PENDING.json').exists()
        initial=s.read(d/'INITIAL_INPUT.json');ms=initial['messages'];last=None;actor_count=0;copy_count=0;rows=[]
        assert tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)==initial['input_token_ids']
        actual_system=(s.E/'chosen-persistence-prototype-v1/FRR_COMPACT.md').read_text()+'\n\n'+(H/'LAWS_COMMON.txt').read_text()+'\n'+(H/(mode.upper()+'_LAW.txt')).read_text()
        assert ms==[{'role':'system','content':actual_system},{'role':'user','content':s.text(initial['observation'])}]
        previous=s.read(d/'world/world/engine/bundles/000000.json');step=0
        assert initial['observation']==s.observation(d,previous,0,dict(replies=0,ticks=0,actor_operations=0),None)
        assert len(list((d/'records').glob('*.json')))==state['turn']==3
        for n in range(1,state['turn']+1):
            label=f'{n:06d}';r=s.read(d/'records'/(label+'.json'));raw=s.read(d/'raw'/(label+'.json'));plan=s.read(d/'plans'/(label+'.json'))
            rr=s.read(d/'world/replies'/('reply_'+label+'.json'));batch=rr['actor_batch'];tick=rr['physical_tick'];bundle=s.read(d/'snapshots'/(label+'.json'))
            assert raw['messages']==plan['messages']==ms
            assert raw['input_token_ids']==plan['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==r['text']==rr['raw_text']==batch['raw_text']
            assert r['raw_sha256']==s.sha(d/'raw'/(label+'.json')) and r['parent_record_sha256']==last
            assert rr['text_sha256']==s.a.fingerprint(raw['text'])
            assert batch==s.read(d/'world/world/engine/batches'/('reply_'+label+'.json'))
            assert batch['before_id']==previous['id'] and batch['start_step']==step
            assert batch['parsed']==s.a.base.parse_notebook(raw['text']) and batch['automatic_note_append'] is False
            cells=[c for c in batch['parsed']['cells'] if c['executable']]
            assert len(batch['operations'])==(len(cells) if batch['status']=='completed' else 0)
            for op,cell in zip(batch['operations'],cells):
                assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert tick['source']==s.a.tick_source(mode) and tick['before_id']==batch['after_id']
            assert tick==s.read(d/'world/world/engine/events'/f"{tick['step']:06d}.json")
            assert tick['step']==batch['end_step']+1 and tick['after_id']==bundle['id']==r['world_id']
            actor_count+=len(batch['operations']);clock=dict(replies=n,ticks=n,actor_operations=actor_count)
            assert rr['after_state']==clock
            obs=s.observation(d,bundle,tick['step'],clock,n)
            feedback=s.text(dict(actor_feedback={'boundary':batch['boundary'],'receipts':[op['receipt'] for op in batch['operations']]},physical_feedback=tick['receipt'],**obs))
            assert r['feedback']==feedback and len(feedback.encode())<=8192
            assert raw['decoder']=='greedy_argmax' and len(raw['generated_token_ids'])<=256 and len(raw['input_token_ids'])<=7936
            assert (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256) or (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id)
            exact_copy=raw['text']==ms[-1]['content'];copy_count+=int(exact_copy)
            rows.append(dict(turn=n,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],seconds=raw['seconds'],actor_operations=len(batch['operations']),exact_latest_packet_copy=exact_copy,physical_exit_code=tick['receipt']['exit_code'],physical_material_changed=tick['before_id']!=tick['after_id']))
            ms=ms+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
            last=s.sha(d/'records'/(label+'.json'));previous=bundle;step=tick['step']
        assert state['last_record_sha256']==last
        assert s.read(d/'world/STATE.json')==dict(replies=3,ticks=3,actor_operations=actor_count)
        verified=s.a.c.verify(d/'world/world');assert verified['bundle_id']==previous['id'] and verified['step']==step
        assert s.read(d/'world/world/engine/STATE.json')['paused']
        result.append(dict(condition=mode,turns=3,actor_operations=actor_count,exact_packet_copies=copy_count,world_entries=len(previous['entries']),next_input_tokens=len(tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)),rows=rows))
    out=dict(status='pass',conditions=result,model_calls=6,training_updates=0,protected_files_unchanged=len(s.inventory()),reference_candidate_turn=38,main_entry=1630,reference_unchanged=True,observer_only=True)
    s.a.base.atomic(H/'RESULTS.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':main()
