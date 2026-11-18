"""Audit length-only native-code check; incomplete-cell syntax is not execution."""
from pathlib import Path
import sys,json,ast
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B));import run512 as r
s=r.s

def main():
    r.guard();assert not (B/'RUN.lock').exists() and not (B/'PENDING.json').exists();tok=s.c.tokenizer()
    init=s.read(B/'INITIAL_INPUT.json');raw=s.read(B/'RAW.json');old=s.read(r.N/'code/RAW.json')
    assert raw['messages']==init['messages']==old['messages'] and raw['input_token_ids']==init['input_token_ids']==old['input_token_ids']==tok.apply_chat_template(init['messages'],tokenize=True,add_generation_prompt=True)
    assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text'] and raw['decoder']=='greedy_argmax'
    assert raw['generated_token_ids'][:256]==old['generated_token_ids'] and len(raw['input_token_ids'])+512<=8192
    assert (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==512) or (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id)
    original=(r.native.parent.E/'minimal-garden-candidate-v1/generation.py').read_text();variant=(B/'body512.py').read_text();assert variant.replace('MAX_OUTPUT = 512','MAX_OUTPUT = 256')==original
    world=B/'verification_world';rr=s.read(world/'replies/operator_code_verification.json');parsed=s.a.base.parse_notebook(raw['text']);batch=rr['actor_batch'];tick=rr['physical_tick'];snap=s.read(B/'SNAPSHOT.json')
    assert batch['raw_text']==raw['text'] and batch['parsed']==parsed and batch['automatic_note_append'] is False
    cells=[c for c in parsed['cells'] if c['executable']];assert len(batch['operations'])==len(cells)
    assert tick['source']==s.a.tick_source('changing') and tick['before_id']==batch['after_id'] and tick['step']==batch['end_step']+1 and tick['after_id']==snap['id']
    assert s.a.c.verify(world/'world')['bundle_id']==snap['id'] and s.read(world/'world/engine/STATE.json')['paused']
    assert not (world/'PENDING.json').exists() and not (world/'world/engine/LOCK.json').exists()
    snippets=[]
    for cell in parsed['cells']:
        if cell['language']=='python':
            try:ast.parse(cell['source']);valid=True
            except SyntaxError:valid=False
            snippets.append(dict(complete_transport_fence=cell['complete'],exact_source_valid_python_syntax=valid,source_repaired=False,source_executed=cell['executable']))
    v=s.read(B/'VERIFICATION.json');assert v['actor_cells']==len(batch['operations']) and v['operator_generated_cells_executed']==bool(batch['operations'])
    result=dict(status='pass',actual_model_calls=1,maximum_output_tokens=512,shared256_token_prefix_exact=True,output_tokens=len(raw['generated_token_ids']),stop=raw['stop'],syntax_only_snippets=snippets,operator_executed_cells=len(batch['operations']),physical_exit_code=tick['receipt']['exit_code'],world_paths=[x[0] for x in snap['entries']],autonomous_model_action=False,native_cases_unchanged=len(r.inventory()),training_updates=0,old_gardens_unchanged=True)
    s.save(B/'RESULTS.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
