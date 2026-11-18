"""External native-chat sanity audit; records an operator metadata flag error."""
from pathlib import Path
import sys,json,base64,hashlib,ast
N=Path(__file__).resolve().parent;sys.path.insert(0,str(N));import run_native as r
s=r.s

def filedata(world,bundle,name):
    rows={x[0]:x for x in bundle['entries']};row=rows.get(name)
    if row is None:return None
    if row[1]=='hardlink':row=rows[row[2]]
    if row[1]!='file':return None
    obj=s.read(world/'world/engine/objects'/(row[3]+'.json'));data=base64.b64decode(obj['base64'],validate=True);assert hashlib.sha256(data).hexdigest()==row[3] and len(data)==row[4];return data

def main():
    r.guard();assert not (N/'RUN.lock').exists();tok=s.c.tokenizer();rows=[]
    for name in ['comparison','code']:
        d=N/name;init=s.read(d/'INITIAL_INPUT.json');raw=s.read(d/'RAW.json')
        assert s.read(d/'STATE.json')==dict(model_calls=1,paused=True) and not (d/'PENDING.json').exists()
        assert init['messages']==[{'role':'user','content':r.VALUE if name=='comparison' else r.CODE}]
        assert raw['messages']==init['messages'] and raw['input_token_ids']==init['input_token_ids']==tok.apply_chat_template(init['messages'],tokenize=True,add_generation_prompt=True)
        assert init['rendered_chat']==tok.apply_chat_template(init['messages'],tokenize=False,add_generation_prompt=True)
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'] and raw['decoder']=='greedy_argmax'
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256)
        row=dict(case=name,input_tokens=len(raw['input_token_ids']),output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],text=raw['text'])
        if name=='code':
            world=d/'verification_world';rr=s.read(world/'replies/operator_code_verification.json');parsed=s.a.base.parse_notebook(raw['text']);batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(d/'SNAPSHOT.json')
            assert batch['raw_text']==raw['text'] and batch['parsed']==parsed and batch['automatic_note_append'] is False
            cells=[c for c in parsed['cells'] if c['executable']];assert len(batch['operations'])==len(cells)
            assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1 and tick['after_id']==snap['id']
            verified=s.a.c.verify(world/'world');assert verified['bundle_id']==snap['id'] and verified['step']==tick['step']
            assert s.read(world/'world/engine/STATE.json')['paused'] and not (world/'PENDING.json').exists() and not (world/'world/engine/LOCK.json').exists()
            note=filedata(world,snap,'note.txt');v=s.read(d/'VERIFICATION.json');assert v['actor_cells']==len(batch['operations'])
            metadata_flag_correct=v['operator_executed_generated_code']==bool(batch['operations'])
            row.update(operator_executed_cells=len(batch['operations']),incomplete_fences=sum(not c['complete'] for c in parsed['cells']),physical_exit_code=tick['receipt']['exit_code'],note_bytes=None if note is None else len(note),note_utf8=None if note is None else note.decode(errors='replace'),source_repaired=False,verification_flag_correct=metadata_flag_correct,actual_autonomous_world_action=False)
            if not metadata_flag_correct:
                s.save(N/'VERIFICATION_FLAG_ERRATUM.json',dict(original_file='code/VERIFICATION.json',field='operator_executed_generated_code',recorded_value=v['operator_executed_generated_code'],correct_value=bool(batch['operations']),actual_cells=len(batch['operations']),reason='unconditional operator flag overstated execution; actual committed cell ledger is authoritative',original_preserved=True,model_calls_repeated=0))
        rows.append(row)
    s.save(N/'RESULTS.json',dict(status='pass_with_documented_metadata_erratum' if any(not x.get('verification_flag_correct',True) for x in rows) else 'pass',actual_model_calls=2,branches=rows,training_updates=0,parent_case_files_unchanged=len(r.parent_inventory()),old_gardens_unchanged=True));print(json.dumps({'audited_native_calls':2,'actual_code_cells':rows[1]['operator_executed_cells'],'metadata_flag_correct':rows[1]['verification_flag_correct']}))
if __name__=='__main__':main()
