"""Real-error receipt alias contact: four replies executed in detached post-failure worlds."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,copy,uuid,traceback,base64
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1';OLD=E/'retrieval-repair-three-cycle-v1';PRIOR=E/'retrieval-task-transfer-v1'
sys.path.insert(0,str(E/'observability-three-contact-v1'))
import common as c
from worker import generate
def save(p,v):c.candidate.immutable(Path(p),v)
def read(p):return c.read(p)
CASES={'path':('original_signal_merged','probe_value.json','signal'),'parser':('renamed_value_merged','sample_record.json','value')}
def alias(o):
    if isinstance(o,dict):return {('limit' if k=='boundary' else k):alias(v) for k,v in o.items()}
    if isinstance(o,list):return [alias(v) for v in o]
    return o
def inverse(o):
    if isinstance(o,dict):return {('boundary' if k=='limit' else k):inverse(v) for k,v in o.items()}
    if isinstance(o,list):return [inverse(v) for v in o]
    return o
def guard():
    p=read(H/'PLAN.json');b=read(H/'BASELINE.json')
    assert c.inventory(M)==b['main'] and c.inventory()==b['original']
    assert c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')==b['active_sha256']
    assert all(c.inventory(Path(p))==inv for p,inv in b['source_stores'].items())
    assert all(c.sha(Path(p))==sha for p,sha in read(H/'SOURCE_PINS.json').items())
def prepare():
    assert not (H/'PLAN.json').exists(),'Single preparation, no replay'
    state=read(M/'run/STATE.json');assert state['human_entry']==1630 and state['paused']
    assert not (M/'run/PENDING.json').exists() and not (M/'run/RUN.lock').exists()
    sources={kind:read(OLD/'jobs'/('feedback_'+case+'.json')) for kind,(case,_,_) in CASES.items()}
    save(H/'BASELINE.json',{'main':c.inventory(M),'original':c.inventory(),'active_sha256':c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json'),
      'source_stores':{s['world_store']:c.inventory(Path(s['world_store'])) for s in sources.values()}})
    save(H/'PLAN.json',{'date':'2026-11-15 UTC','purpose':'real_error_receipt_representation','planned_model_calls':4,
      'factors':'two existing real failure types x native boundary versus limit receipt-key alias; one actual reply/execution each',
      'changes':'only two null boundary-key names in prior receipt; no error value/stdout/stderr/path/status changes, hints, repeated task or code repair',
      'source_state':'exact old prepared post-original-failure snapshots, before old repair replies; historical parent1580; not main1630 entry',
      'original_task':'preexisting explicit retrieval task remains in inherited diagnostic input; this is not task-free primary exploration or an FRR treatment',
      'body':'exact pinned old worker.generate, cached135M float32CPU eager2threads greedy256 freshKV',
      'readout':'actual code/parser/action/receipt/effects and hidden target stdout; verbal/schema drift separately; one-step repair opportunity not durable learning',
      'conditional_check':'if a hidden value is returned correctly, separately test unchanged generated artifact with changed target bytes before any read/transfer benefit claim',
      'promotion':False,'training_updates':0})
    tok=c.tokenizer();jobs=[];pins=[Path(__file__),H/'PROTOCOL.md',H/'PLAN.json',H/'BASELINE.json',c.H/'common.py',c.H/'worker.py',c.C/'candidate.py',c.C/'world/garden_world.py',E/'final-garden-contract-v1/world.py',E/'final-garden-contract-v1/server.py',c.MODEL/'config.json',c.MODEL/'tokenizer.json',c.MODEL/'tokenizer_config.json']
    for kind,(case,target,key) in CASES.items():
        src=sources[kind];sp=Path(src['world_store']);bundle=sp/'bundles/000001.json';snap=read(bundle)
        assert snap['id']==src['prepared_world_id']
        old_batch=read(PRIOR/'results'/(case+'_t1_batch.json'));old_raw=read(PRIOR/'results'/(case+'_t1_raw.json'))
        actual=c.candidate.project_feedback(old_batch);assert actual==src['actual_feedback']==src['messages'][-1]['content']
        assert src['messages'][-2]=={'role':'assistant','content':old_raw['text']}
        packet=json.loads(actual);assert packet['boundary'] is None and len(packet['receipts'])==1 and packet['receipts'][0]['boundary'] is None
        assert packet['receipts'][0]['exit_code']==1 and packet['receipts'][0]['stderr']
        assert inverse(alias(packet))==packet
        ent=next(x for x in snap['entries'] if x[0]==target);obj=read(sp/'objects'/(ent[3]+'.json'));value=json.loads(base64.b64decode(obj['base64']))[key]
        assert value==src['expected_value'] and value not in json.dumps(src['messages'])
        save(H/'sources'/(kind+'_job.json'),src);save(H/'sources'/(kind+'_failure_batch.json'),old_batch);save(H/'sources'/(kind+'_failure_raw.json'),old_raw)
        old_control=OLD/'results'/('feedback_'+case+'_t1_raw.json');save(H/'sources'/(kind+'_control_raw.json'),read(old_control))
        pins.extend([OLD/'jobs'/('feedback_'+case+'.json'),bundle,PRIOR/'results'/(case+'_t1_batch.json'),PRIOR/'results'/(case+'_t1_raw.json'),old_control])
        worlds=[]
        for condition in ('native','alias'):
            name=kind+'_'+condition;store=H/'worlds'/name
            w=c.GardenWorld.create(store,bundle,sp/'objects',parent_entry=1580)
            try:before=w.checkpoint()
            finally:w.close()
            assert before['id']==snap['id'] and c.verify_store(store)['status']=='pass';worlds.append(before)
            messages=copy.deepcopy(src['messages'])
            if condition=='alias':messages[-1]['content']=json.dumps(alias(packet),ensure_ascii=False,sort_keys=True)
            assert messages[:-1]==src['messages'][:-1]
            assert (inverse(json.loads(messages[-1]['content'])) if condition=='alias' else json.loads(messages[-1]['content']))==packet
            ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
            if condition=='native':assert ids==read(old_control)['input_token_ids']
            j={'name':name,'kind':kind,'condition':condition,'messages':messages,'input_token_ids':ids,'input_tokens':len(ids),
               'world_store':str(store),'before_id':before['id'],'expected_value':value,'target_file':target,'target_key':key,'decoder':'greedy','seed':None}
            save(H/'jobs'/(name+'.json'),j);jobs.append(j)
        assert worlds[0]==worlds[1]
    save(H/'JOBS.json',jobs)
    save(H/'SOURCE_PINS.json',{str(p):c.sha(p) for p in pins})
    guard();print(json.dumps({'status':'pass','model_calls':0,'jobs':[(j['name'],j['input_tokens']) for j in jobs]}))

def audit(write=True):
    guard();assert not (H/'PENDING.json').exists();tok=c.tokenizer();rows=[]
    for j in read(H/'JOBS.json'):
        name=j['name'];raw=read(H/'raw'/(name+'.json'));batch=read(H/'batches'/(name+'.json'));row=read(H/'records'/(name+'.json'))
        assert raw['messages']==j['messages'] and raw['input_token_ids']==j['input_token_ids']==tok.apply_chat_template(j['messages'],tokenize=True,add_generation_prompt=True)
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==batch['raw_text']
        assert batch['parsed']==c.parse_notebook(raw['text']) and row['before_id']==j['before_id']
        assert 0<len(raw['generated_token_ids'])<=256 and raw['decoder']=='greedy'
        assert (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256) or (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id)
        store=Path(j['world_store']);assert batch==read(store/'batches'/(batch['batch_id']+'.json'))
        for op in batch['operations']:
            ev={k:v for k,v in op.items() if k not in ('cell_index','source_start','source_end')};assert ev==read(store/'events'/f"{op['step']:06d}.json")
        v=c.verify_store(store);assert v['status']=='pass' and v['bundle_id']==row['after_id']
        assert row['feedback']==c.candidate.project_feedback(batch)
        rows.append(row)
    out={'status':'pass','actual_model_calls':len(rows),'rows':rows,'main_entry':1630,'main_unchanged':True,'training_updates':0,'activation':False,'pending':False}
    if write:save(H/'AUDIT.json',out)
    return out

def run():
    assert not (H/'RUN_STARTED.json').exists(),'No automatic replay'
    token=uuid.uuid4().hex;save(H/'RUN.lock',{'token':token,'pid':os.getpid()})
    try:
        guard();save(H/'RUN_STARTED.json',{'planned_model_calls':4})
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest,Guard
        tok=c.tokenizer();torch.set_num_threads(2)
        model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        expected=read(c.C/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected;resource=Guard(5153960755,H/'RESOURCE.jsonl');resource.read('loaded')
        for j in read(H/'JOBS.json'):
            guard();assert not (H/'PENDING.json').exists();name=j['name'];save(H/'PENDING.json',{'case':name,'stage':'generation/action unresolved; no automatic replay'})
            raw=generate(model,tok,j['messages'],j,resource,name);save(H/'raw'/(name+'.json'),raw)
            w=c.GardenWorld.open(Path(j['world_store']))
            try:
                before=w.checkpoint();assert before['id']==j['before_id'];batch=w.receive_notebook(raw['text']);save(H/'batches'/(name+'.json'),batch);after=w.checkpoint()
            finally:w.close()
            save(H/'snapshots'/(name+'.json'),after)
            receipts=[{'channel':op['channel'],'feedback':op['feedback'],'changed_paths':op['changed_paths'],'source':op['source']} for op in batch['operations'] if op['channel'] in ('python','shell')]
            stdout=[(a['feedback'] or {}).get('stdout','') for a in receipts]
            control=read(H/'sources'/(j['kind']+'_control_raw.json'))
            row={'name':name,'kind':j['kind'],'condition':j['condition'],'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),
                 'complete_cells':batch['parsed']['complete_executable_cells'],'incomplete_fences':sum(not a['complete'] for a in batch['parsed']['cells']),
                 'actions':receipts,'before_id':before['id'],'after_id':after['id'],'feedback':c.candidate.project_feedback(batch),
                 'target_in_stdout':any(j['expected_value'] in s for s in stdout),'exact_value_stdout':any(s.strip()==j['expected_value'] for s in stdout),
                 'prior_control_output_equal':raw['generated_token_ids']==control['generated_token_ids'] if j['condition']=='native' else None,
                 'world_verification':c.verify_store(Path(j['world_store']))}
            save(H/'records'/(name+'.json'),row)
            assert row['world_verification']['status']=='pass' and parameter_digest(model,False)==expected;guard();(H/'PENDING.json').unlink()
            print(json.dumps({k:row[k] for k in ('name','input_tokens','output_tokens','complete_cells','target_in_stdout')}),flush=True)
        out=audit(False);out['weights_unchanged']=parameter_digest(model,False)==expected;save(H/'RESULTS.json',out);print(json.dumps({'status':out['status'],'actual_model_calls':out['actual_model_calls'],'successes':sum(r['target_in_stdout'] for r in out['rows'])}),flush=True)
    except BaseException as e:save(H/('ERROR_'+uuid.uuid4().hex+'.json'),{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'pending':(H/'PENDING.json').exists()});raise
    finally:
        if (H/'RUN.lock').exists() and read(H/'RUN.lock')['token']==token:(H/'RUN.lock').unlink()

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run','audit'));a=p.parse_args()
    if a.command=='prepare':prepare()
    elif a.command=='run':run()
    else:print(json.dumps(audit()))
