"""Continuous detached candidate, with external records and chosen world writes."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,copy,uuid,traceback,importlib.util
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1'
sys.path[:0]=[str(H),str(E/'observability-three-contact-v1'),str(E/'frr-sandbox-rd-v1/interface/instrument')]
import coupling as p
import common as c
from snapshot_packet import make_snapshot,PacketCapacityError
s=importlib.util.spec_from_file_location('chosen_candidate_fixed_body',c.C/'generation.py');body=importlib.util.module_from_spec(s);s.loader.exec_module(body)
def save(path,v):p.base.immutable(Path(path),v)
def read(path):return p.base.read(path)
def encode(v):return json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def pins():
    paths=[Path(__file__),H/'coupling.py',H/'LAWS.txt',H/'FRR_COMPACT.md',H/'FRR_FULL_REFERENCE.md',H/'PROTOCOL.md',c.C/'generation.py',c.H/'common.py',
       E/'minimal-garden-candidate-v1/world/garden_world.py',E/'final-garden-contract-v1/world.py',E/'final-garden-contract-v1/server.py',
       E/'frr-sandbox-rd-v1/interface/instrument/snapshot_packet.py',c.MODEL/'config.json',c.MODEL/'tokenizer.json',c.MODEL/'tokenizer_config.json']
    return {str(x):c.sha(x) for x in paths}
def guard(d):
    b=read(d/'BEFORE.json');contract=read(d/'CONTRACT.json')
    assert c.inventory(M)==b['main'] and c.inventory()==b['original']
    assert c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')==b['active_sha256']
    assert all(c.sha(Path(path))==sha for path,sha in contract['pins'].items())
def snapshot(d,label,bundle,step,index):
    save(d/'snapshots'/(label+'.json'),bundle)
    try:
        v=make_snapshot(bundle,timing='initial' if index is None else 'after_reply',world_step=step,reply_index=index,max_packet_bytes=8192)
        result={'status':'complete','model_text':v.model_text,'model_packet':v.model_packet,'observer_record':v.observer_record}
    except PacketCapacityError as e:
        result={'status':'capacity','model_text':None,'required_bytes':e.required_bytes,'limit_bytes':e.limit_bytes,'partial_packet_emitted':False}
    save(d/'observations'/(label+'.json'),result);return result
def messages(d):
    state=read(d/'STATE.json');out=copy.deepcopy(read(d/'INITIAL_INPUT.json')['messages'])
    for n in range(1,state['turn']+1):
        r=read(d/'records'/f'{n:06d}.json');out.append({'role':'assistant','content':r['text']})
        if r['feedback_for_next_input'] is not None:out.append({'role':'user','content':r['feedback_for_next_input']})
    return out
def prepare(d):
    d=Path(d);d.mkdir(parents=True,exist_ok=False)
    assert read(M/'run/STATE.json')['human_entry']==1630 and read(M/'run/STATE.json')['paused']
    assert not (M/'run/PENDING.json').exists() and not (M/'run/RUN.lock').exists()
    assert read(H/'checks/attempt001/RESULTS.json')['status']=='pass' and read(H/'checks/finalization/RESULTS.json')['status']=='pass'
    save(d/'BEFORE.json',{'main':c.inventory(M),'original':c.inventory(),'active_sha256':c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')})
    save(d/'CONTRACT.json',{'version':'chosen-persistence-prototype-v1','date':'2026-11-16 America/Chicago','identity':'fresh detached FRR candidate, not main continuation',
       'initial_world':'empty filesystem from declared empty seed; no old notebooks/puzzles/operator test artifacts copied',
       'FRR':'exact archived compact adaptation in system context, plus mechanical laws; full reference external only',
       'history':'same initial messages and all actual native-role pairs, no pruning; stop before input exceeds7936',
       'observation':'full truthful supported directory packet initially and after known effects;8192bytes full-or-capacity pause',
       'automatic_world_note':False,'body':'cached135M CPUfloat32/eager/two threads greedy256 freshKV, fixed weights',
       'stopping':'explicit budget/user pause/resource or unknown-effect/dependency boundary; wrong/inert output is data',
       'promotion':False,'training_updates':0,'pins':pins(),'tensor_digest':read(c.C/'run/MANIFEST.json')['tensor_digest']})
    save(d/'CREATE_PENDING.json',{'stage':'fresh candidate initialization unresolved'})
    seed=H/'checks/attempt001/seed';w=p.ChosenWorld.create(d/'world',seed/'bundle.json',seed/'objects',parent_entry=0)
    try:bundle=w.checkpoint();assert bundle['entries']==[];step=w.step
    finally:w.close()
    obs=snapshot(d,'initial',bundle,step,None);assert obs['status']=='complete'
    initial=[{'role':'system','content':(H/'FRR_COMPACT.md').read_text()+'\n\n'+(H/'LAWS.txt').read_text()},{'role':'user','content':obs['model_text']}]
    tok=c.tokenizer();ids=tok.apply_chat_template(initial,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
    save(d/'INITIAL_INPUT.json',{'messages':initial,'input_token_ids':ids})
    p.base.atomic(d/'STATE.json',{'turn':0,'paused':True,'world_step':0,'world_id':bundle['id'],'last_record_sha256':None,'stop_reason':None})
    p.unlink_durable(d/'CREATE_PENDING.json');guard(d)
    print(encode({'status':'prepared','initial_tokens':len(ids),'world_files':0,'main_entry':1630,'model_calls':0}))

def audit(d,write=False):
    d=Path(d);guard(d);assert not (d/'PENDING.json').exists() and not (d/'CREATE_PENDING.json').exists()
    tok=c.tokenizer();state=read(d/'STATE.json');ms=copy.deepcopy(read(d/'INITIAL_INPUT.json')['messages']);last=None
    assert tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)==read(d/'INITIAL_INPUT.json')['input_token_ids']
    prev=read(d/'snapshots/initial.json');step=0;cells=0
    assert prev['entries']==[]
    initial_observation=make_snapshot(prev,timing='initial',world_step=0,reply_index=None,max_packet_bytes=8192)
    assert ms==[{'role':'system','content':(H/'FRR_COMPACT.md').read_text()+'\n\n'+(H/'LAWS.txt').read_text()},{'role':'user','content':initial_observation.model_text}]
    assert {x.name for x in (d/'records').glob('*.json')}=={f'{n:06d}.json' for n in range(1,state['turn']+1)}
    for n in range(1,state['turn']+1):
        label=f'{n:06d}';r=read(d/'records'/(label+'.json'));raw=read(d/'raw'/(label+'.json'));plan=read(d/'plans'/(label+'.json'))
        b=read(d/'world/engine/batches'/('reply_'+label+'.json'));snap=read(d/'snapshots'/(label+'.json'));obs=read(d/'observations'/(label+'.json'))
        assert plan['messages']==raw['messages']==ms and plan['input_token_ids']==raw['input_token_ids']==tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==r['text']==b['raw_text']
        assert b['parsed']==p.base.parse_notebook(raw['text']) and b['before_id']==prev['id'] and b['start_step']==step
        assert b['status'] in ('completed','boundary') and b['after_id']==snap['id'] and r['parent_record_sha256']==last
        assert b['automatic_note_append'] is False and all(op['channel'] in ('python','shell') for op in b['operations'])
        executable=[cell for cell in b['parsed']['cells'] if cell['executable']]
        assert len(b['operations'])==(len(executable) if b['status']=='completed' else 0)
        if b['status']=='boundary':assert b['boundary']=='cell_count_limit' and len(executable)>8
        for op,cell in zip(b['operations'],executable):
            assert op['source']==cell['source'] and op['channel']==('python' if cell['language']=='python' else 'shell')
            assert {k:v for k,v in op.items() if k not in ('cell_index','source_start','source_end')}==read(d/'world/engine/events'/f"{op['step']:06d}.json")
        assert b['end_step']==step+len(b['operations'])
        receipt={'boundary':b['boundary'],'receipts':[op['receipt'] for op in b['operations']]}
        if obs['status']=='complete':
            expected=make_snapshot(snap,timing='after_reply',world_step=b['end_step'],reply_index=n,max_packet_bytes=8192)
            assert obs['model_text']==expected.model_text and obs['model_packet']==expected.model_packet and obs['observer_record']==expected.observer_record
            assert r['feedback_for_next_input']==encode({'runtime_feedback':receipt,'world_observation':expected.model_packet['world_snapshot']})
        else:assert r['feedback_for_next_input'] is None and r['pause_reason']=='observation_capacity'
        assert raw['decoder']=='greedy_argmax' and 0<len(raw['generated_token_ids'])<=256
        assert (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256) or (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id)
        assert r['raw_sha256']==c.sha(d/'raw'/(label+'.json')) and r['batch_sha256']==c.sha(d/'world/engine/batches'/('reply_'+label+'.json'))
        ms.append({'role':'assistant','content':r['text']})
        if r['feedback_for_next_input'] is not None:ms.append({'role':'user','content':r['feedback_for_next_input']})
        last=c.sha(d/'records'/(label+'.json'));prev=snap;step=b['end_step'];cells+=len(b['operations'])
    verified=p.verify(d/'world');assert verified['bundle_id']==prev['id'] and verified['step']==step
    assert state['last_record_sha256']==last and state['world_step']==step and state['world_id']==prev['id']
    out={'status':'pass','candidate_turn':state['turn'],'actual_model_calls_total':state['turn'],'actual_cell_operations':cells,'automatic_world_note_appends':0,
         'world_entries':len(prev['entries']),'world_id':prev['id'],'main_entry':1630,'main_unchanged':True,'training_updates':0,'stop_reason':state['stop_reason'],'pending':False}
    if write:save(d/'audits'/(uuid.uuid4().hex+'.json'),out)
    return out

def run(d,budget):
    d=Path(d);assert 1<=budget<=100 and not (d/'PENDING.json').exists() and not (d/'CREATE_PENDING.json').exists()
    token=uuid.uuid4().hex;save(d/'RUN.lock',{'token':token,'pid':os.getpid()})
    try:
        before=audit(d);assert before['stop_reason'] is None
        save(d/'runs'/(token+'_START.json'),{'start_turn':before['candidate_turn'],'budget':budget,'automatic_resume':False})
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        torch.set_num_threads(2);tok=c.tokenizer();expected=read(d/'CONTRACT.json')['tensor_digest']
        model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==expected;resource=Guard(5153960755,d/'RESOURCE.jsonl');resource.read('loaded')
        completed=0
        for _ in range(budget):
            if (d/'PAUSE_REQUEST').exists():break
            guard(d);old=read(d/'STATE.json');n=old['turn']+1;label=f'{n:06d}';ms=messages(d);ids=tok.apply_chat_template(ms,tokenize=True,add_generation_prompt=True)
            if len(ids)>7936:
                save(d/'capacity'/('before_'+label+'.json'),{'input_tokens':len(ids),'limit':7936,'model_generation':False})
                old['stop_reason']='input_capacity';p.base.atomic(d/'STATE.json',old);break
            save(d/'plans'/(label+'.json'),{'messages':ms,'input_token_ids':ids,'before_id':old['world_id'],'parent_record_sha256':old['last_record_sha256']})
            save(d/'PENDING.json',{'turn':n,'stage':'generation and effects unresolved; no replay'})
            raw=body.generate(model,tok,ms,resource,'chosen_candidate_'+label);save(d/'raw'/(label+'.json'),raw)
            w=p.ChosenWorld.open(d/'world')
            try:
                assert w.checkpoint()['id']==old['world_id'];b=w.receive_expression(raw['text'],'reply_'+label);snap=w.checkpoint();step=w.step
            finally:w.close()
            assert p.verify(d/'world')['bundle_id']==snap['id']
            obs=snapshot(d,label,snap,step,n);receipt={'boundary':b['boundary'],'receipts':[op['receipt'] for op in b['operations']]}
            feedback=encode({'runtime_feedback':receipt,'world_observation':obs['model_packet']['world_snapshot']}) if obs['status']=='complete' else None
            pause='observation_capacity' if feedback is None else None
            next_tokens=None if feedback is None else len(tok.apply_chat_template(ms+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}],tokenize=True,add_generation_prompt=True))
            if next_tokens is not None and next_tokens>7936:pause='input_capacity'
            r={'turn':n,'text':raw['text'],'input_tokens':len(ids),'output_tokens':len(raw['generated_token_ids']),
               'raw_sha256':c.sha(d/'raw'/(label+'.json')),'batch_sha256':c.sha(d/'world/engine/batches'/('reply_'+label+'.json')),
               'parent_record_sha256':old['last_record_sha256'],'feedback_for_next_input':feedback,'pause_reason':pause,'next_input_tokens':next_tokens,
               'complete_cells':len(b['operations']),'incomplete_fences':sum(not cell['complete'] for cell in b['parsed']['cells']),
               'before_id':old['world_id'],'after_id':snap['id'],'world_step':step,'automatic_world_note_append':False}
            save(d/'records'/(label+'.json'),r)
            p.base.atomic(d/'STATE.json',{'turn':n,'paused':True,'world_step':step,'world_id':snap['id'],'last_record_sha256':c.sha(d/'records'/(label+'.json')),'stop_reason':pause})
            assert parameter_digest(model,False)==expected;guard(d);p.unlink_durable(d/'PENDING.json');completed+=1
            print(encode({k:r[k] for k in ('turn','input_tokens','output_tokens','complete_cells','world_step','pause_reason')}),flush=True)
            if pause:break
        out=audit(d,True);out.update(model_calls_this_invocation=completed,weights_unchanged=parameter_digest(model,False)==expected)
        save(d/'runs'/(token+'_RESULT.json'),out);print(encode(out),flush=True)
    except BaseException as e:
        save(d/'faults'/(uuid.uuid4().hex+'.json'),{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'pending':(d/'PENDING.json').exists()});raise
    finally:
        if (d/'RUN.lock').exists() and read(d/'RUN.lock')['token']==token:p.unlink_durable(d/'RUN.lock')

if __name__=='__main__':
    import argparse
    q=argparse.ArgumentParser();q.add_argument('command',choices=('prepare','run','audit'));q.add_argument('--directory',type=Path,default=H/'candidate');q.add_argument('--budget',type=int,default=3);a=q.parse_args()
    if a.command=='prepare':prepare(a.directory)
    elif a.command=='run':run(a.directory,a.budget)
    else:print(encode(audit(a.directory,True)))
