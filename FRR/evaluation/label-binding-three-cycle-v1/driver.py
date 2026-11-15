"""Generation-only, explicitly counterfactual context diagnostics. No world execution."""
import os
for key,value in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[key]=value
from pathlib import Path
import sys,json,copy,argparse,importlib.util,uuid,traceback
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1'
sys.path.insert(0,str(E/'observability-three-contact-v1'))
import common as c
s=importlib.util.spec_from_file_location('unchanged_body',c.C/'generation.py');body=importlib.util.module_from_spec(s);s.loader.exec_module(body)
def save(p,v):c.candidate.immutable(Path(p),v)
def load(p):return c.read(p)
def encode(v):return json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':'))
def guard():
    before=load(H/'BASELINE.json')
    assert c.inventory(M)==before['main_inventory'] and c.inventory()==before['original_inventory']
    assert c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json')==before['active_sha256']
def pins():
    ps=[Path(__file__),H/'PLAN.md',H/'BASELINE.json',c.H/'common.py',c.C/'generation.py',c.C/'candidate.py',c.C/'world/garden_world.py',c.MODEL/'config.json',c.MODEL/'tokenizer.json',c.MODEL/'tokenizer_config.json']
    ps+=sorted((H/'sources').glob('*.json'))
    return {str(p):c.sha(p) for p in ps}
def check_plan(cycle):
    guard();p=load(H/f'cycle{cycle}/PLAN.json')
    assert all(c.sha(Path(path))==sha for path,sha in p['pins'].items())
    assert not (H/f'cycle{cycle}/PENDING.json').exists()
    if cycle>1:assert c.sha(H/f'cycle{cycle-1}/RESULTS.json')==p['previous_results_sha256']
    return p

def prepare(cycle):
    d=H/f'cycle{cycle}';d.mkdir(exist_ok=False)
    if cycle>1:assert load(H/f'cycle{cycle-1}/RESULTS.json')['status']=='pass'
    guard();tok=c.tokenizer()
    t1=load(H/'sources/compact_t1.json');t2=load(H/'sources/compact_t2.json')
    assert len(t1['messages'])==2 and len(t2['messages'])==4
    assert t2['messages'][2]=={'role':'assistant','content':t1['text']}
    assert json.loads(t2['messages'][3]['content'])=={'runtime_feedback':None}
    cases=[]
    if cycle==1:
        specifications=[('native','world','runtime_feedback'),('renamed','world','cell_results')]
    elif cycle==2:
        specifications=[('native','world','runtime_feedback'),('renamed','directory','runtime_feedback')]
    else:
        specifications=[('world_native','world','runtime_feedback'),('world_renamed','world','cell_results'),('directory_native','directory','runtime_feedback'),('directory_renamed','directory','cell_results')]
    for name,prior,key in specifications:
        source=t1 if cycle==2 else t2;messages=copy.deepcopy(source['messages'])
        if cycle==2 and prior=='directory':
            packet=json.loads(messages[1]['content']);assert list(packet)==['world_snapshot']
            messages[1]['content']=encode({'directory_state':packet['world_snapshot']})
        if cycle!=2:
            messages[3]['content']=encode({key:None})
            if prior=='directory':
                original=messages[2]['content'];assert 'world-snapshot' in original and '"world_snapshot"' in original
                messages[2]['content']=original.replace('world-snapshot','directory-state').replace('world_snapshot','directory_state')
        ids=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True);assert len(ids)<=7936
        if name in ('native','world_native'):assert messages==source['messages'] and ids==source['input_token_ids']
        if cycle!=2:assert messages[:2]==t2['messages'][:2] and json.loads(messages[3]['content'])=={key:None}
        else:assert messages[0]==t1['messages'][0] and list(json.loads(messages[1]['content']).values())==list(json.loads(t1['messages'][1]['content']).values())
        cases.append({'name':name,'messages':messages,'input_token_ids':ids,'input_tokens':len(ids),'source_reply':source['run_id'],
                      'historical_control':name in ('native','world_native'),'prior_label':prior,'receipt_key':key if cycle!=2 else None,
                      'synthetic_prior_assistant':cycle==3 and prior=='directory','effects_executed':False})
    p={'cycle':cycle,'purpose':'generation_only_context_intervention','planned_model_calls':len(cases),'cases':cases,
       'pins':pins(),'model_tensor_digest':load(c.C/'run/MANIFEST.json')['tensor_digest'],
       'previous_results_sha256':c.sha(H/f'cycle{cycle-1}/RESULTS.json') if cycle>1 else None,
       'source_semantics':'actual source messages/receipt; only declared keys or counterfactual prior nouns change; not a native world history',
       'body':'cached135M CPUfloat32 eager2threads greedy256 freshKV; no parameter updates or source repair',
       'limits':'input7936; generation-only outputs are never sent to executor or appended to any world'}
    save(d/'PLAN.json',p);print(encode({'cycle':cycle,'cases':[(x['name'],x['input_tokens']) for x in cases],'model_calls':0}))

def audit(cycle,write=True):
    d=H/f'cycle{cycle}';p=check_plan(cycle);tok=c.tokenizer();rows=[]
    for case in p['cases']:
        raw=load(d/'raw'/f"{case['name']}.json")
        assert raw['messages']==case['messages'] and raw['input_token_ids']==case['input_token_ids']
        assert tok.apply_chat_template(raw['messages'],tokenize=True,add_generation_prompt=True)==raw['input_token_ids']
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']
        assert raw['decoder']=='greedy_argmax' and 0<len(raw['generated_token_ids'])<=256
        assert (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==256) or (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id)
        parsed=c.parse_notebook(raw['text'])
        reference=load(H/'sources'/('compact_t1.json' if cycle==2 else 'compact_t2.json'))
        rows.append({'case':case['name'],'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],
                     'source_control_output_equal':raw['generated_token_ids']==reference['generated_token_ids'] if case['historical_control'] else None,
                     'complete_executable_cells_as_text':parsed['complete_executable_cells'],'incomplete_fences':sum(not x['complete'] for x in parsed['cells']),
                     'literal_label_counts':{word:raw['text'].count(word) for word in ('world_snapshot','directory_state','runtime_feedback','cell_results')},
                     'raw_sha256':c.sha(d/'raw'/f"{case['name']}.json"),'effects_executed':False})
    out={'status':'pass','cycle':cycle,'actual_model_calls':len(rows),'cases':rows,'main_entry':1630,'main_unchanged':True,'world_actions':0,'automatic_note_appends':0,'training_updates':0,
         'scope':'one deterministic output per declared context; literal counts are not semantic understanding or population effects; synthetic histories are interventions not model-originated history'}
    if write:save(d/'AUDIT.json',out)
    return out

def run(cycle):
    d=H/f'cycle{cycle}';assert not (d/'RUN_STARTED.json').exists() and not (d/'RESULTS.json').exists(),'No automatic replay'
    token=uuid.uuid4().hex;save(d/'RUN.lock',{'token':token,'pid':os.getpid()})
    try:
        p=check_plan(cycle);save(d/'RUN_STARTED.json',{'planned_model_calls':p['planned_model_calls']})
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import Guard,parameter_digest
        torch.set_num_threads(2);tok=c.tokenizer()
        model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager');model.requires_grad_(False);model.eval()
        assert parameter_digest(model,False)==p['model_tensor_digest'];resource=Guard(5153960755,d/'RESOURCE.jsonl');resource.read('loaded')
        for case in p['cases']:
            guard();assert not (d/'PENDING.json').exists();save(d/'PENDING.json',{'case':case['name'],'stage':'generation unresolved; no automatic replay'})
            raw=body.generate(model,tok,case['messages'],resource,f'label_cycle{cycle}_{case["name"]}')
            save(d/'raw'/f"{case['name']}.json",raw)
            assert raw['input_token_ids']==case['input_token_ids'] and parameter_digest(model,False)==p['model_tensor_digest']
            guard();(d/'PENDING.json').unlink();print(encode({'cycle':cycle,'case':case['name'],'tokens':len(raw['generated_token_ids'])}),flush=True)
        out=audit(cycle,False);out['weights_unchanged']=parameter_digest(model,False)==p['model_tensor_digest'];save(d/'RESULTS.json',out);print(encode(out),flush=True)
    except BaseException as e:
        save(d/('ERROR_'+uuid.uuid4().hex+'.json'),{'type':type(e).__name__,'message':str(e),'traceback':traceback.format_exc(),'pending':(d/'PENDING.json').exists()});raise
    finally:
        if (d/'RUN.lock').exists() and load(d/'RUN.lock')['token']==token:(d/'RUN.lock').unlink()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=('prepare','run','audit'));p.add_argument('--cycle',required=True,type=int,choices=(1,2,3));a=p.parse_args()
    if a.command=='prepare':prepare(a.cycle)
    elif a.command=='run':run(a.cycle)
    else:print(encode(audit(a.cycle)))
