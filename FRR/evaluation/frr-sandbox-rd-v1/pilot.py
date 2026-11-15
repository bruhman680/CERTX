"""Three context conditions, unchanged physical laws; no training or main activation."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1'
sys.path.insert(0,str(E/'observability-three-contact-v1'))
import common as c
from worker import generate
from runtime_reference import parameter_digest,Guard
import torch
from transformers import AutoModelForCausalLM

def save(path,obj):c.save(H/path,obj)
def atomic(path,obj):
    tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,sort_keys=True)+'\n');tmp.replace(path)
def unchanged():
    assert c.inventory(M)==main_before and c.inventory()==source_before
    assert (E.parent/'ACTIVE_GARDEN_PHASE.json').read_bytes()==pointer_before
    assert all(c.sha(Path(p))==sha for p,sha in pins.items())

def main():
    global main_before,source_before,pointer_before,pins
    assert not (H/'pilot/PLAN.json').exists(),'Existing pilot: inspect; never replay automatically'
    state=c.read(M/'run/STATE.json');assert state['human_entry']==1630 and state['paused']
    assert not (M/'run/RUN.lock').exists() and not (M/'run/PENDING.json').exists()
    main_before=c.inventory(M);source_before=c.inventory();pointer_before=(E.parent/'ACTIVE_GARDEN_PHASE.json').read_bytes()
    assert c.verify_store(M/'run/world')['status']=='pass'
    textpaths=[H/'interface/mechanics_user.txt',H/'interface/world_rules.txt',H/'frr/candidate.md',H/'frr/full_source_reference.md']
    assert all(p.exists() for p in textpaths)
    pins={str(p):c.sha(p) for p in [Path(__file__),*textpaths,c.H/'common.py',c.H/'worker.py',c.C/'world/garden_world.py']}
    mechanics,rules,compact,full=[p.read_text() for p in textpaths]
    tok=c.tokenizer();conditions={'control':'','compact':compact,'full':full}
    save(Path('pilot/PLAN.json'),{'date':'2026-11-14 America/Chicago','status':'prospective detached3arm pilot','arms':list(conditions),'turns_per_arm':3,'total_model_calls_planned':9,'order':'round-robin control,compact,full for eachturn','source_main_entry':1630,'same_source_world':True,'common_fresh_context':'system-slot condition text + exact common mechanical user; no old assistant history','physical_delta':'replace only WORLD_RULES.txt with same fresh mechanical document in each clone; inherited writing/data untouched','FRR_delivery':'context only; compact named adaptation versus fullsource; no neural installation/training','no_task_or_solution':'No user puzzle/task, demonstration, repair hint, grade, curiosity/productivity instruction is added to common framing or followups. Historical files still contain old writing.','history':'all actual branch pairs retained in order, no pruning; pause before7936','body':'same pinned cached135M float32CPU eager2threads greedy256 freshKV','resource_budget':'same reply count and physical limits, not same FLOPs/inputlength','stop':'requestedpause, inputcapacity or unknownoutcome; ordinary known action/resource errors remain feedback, not a semantic productivity gate','metrics':'descriptive actions/receipts/changedpaths; automaticnotebookgrowth separate; no scalarintelligence or publishedbenchmarkcomparison','claims':'whole presentation conditions, small deterministicpilot; not independentreplication or framework-specificmechanism','pins':pins})
    save(Path('pilot/MAIN_BEFORE.json'),main_before);save(Path('pilot/SOURCE_BEFORE.json'),source_before)
    world_state=c.read(M/'run/world/STATE.json');parent=M/'run/world/bundles'/world_state['bundle'];bundle=c.read(parent)
    save(Path('pilot/PARENT_WORLD.json'),bundle)
    ruleentry=next(x for x in bundle['entries'] if x[0]=='WORLD_RULES.txt')
    import base64
    original=base64.b64decode(c.read(M/'run/world/objects'/(ruleentry[3]+'.json'))['base64'])
    (H/'pilot/PARENT_WORLD_RULES.txt').write_bytes(original)
    cases={};prepared=[]
    for name,system in conditions.items():
        store=H/'pilot/branches'/name/'world'
        save(Path('pilot/PREPARATION_PENDING.json'),{'arm':name,'stage':'operator initialization unresolved'})
        w=c.GardenWorld.create(store,parent,M/'run/world/objects',parent_entry=1630)
        try:
            before=w.checkpoint();code="from pathlib import Path\nPath('WORLD_RULES.txt').write_text("+repr(rules)+",encoding='utf-8')"
            op=w.apply('python',code);save(Path('pilot/preparation')/(name+'.json'),{'actor':'operator','source':code,'event':op})
            assert op['feedback']['exit_code']==0 and op['feedback']['boundary'] is None and op['changed_paths']==['WORLD_RULES.txt']
            after=w.checkpoint();a={x[0]:x for x in before['entries']};b={x[0]:x for x in after['entries']}
            assert set(a)==set(b) and all(a[p]==b[p] for p in a if p!='WORLD_RULES.txt')
            assert b['WORLD_RULES.txt'][3]==hashlib.sha256(rules.encode()).hexdigest()
        finally:w.close()
        (H/'pilot/PREPARATION_PENDING.json').unlink()
        messages=[{'role':'system','content':system},{'role':'user','content':mechanics}]
        tokens=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        assert len(tokens)<=7936
        job={'case_id':name,'decoder':'greedy','seed':None,'messages':messages,'world_store':str(store)}
        save(Path('pilot/inputs')/(name+'.json'),{'messages':messages,'input_token_ids':tokens,'condition_sha256':hashlib.sha256(system.encode()).hexdigest(),'condition_text_tokens':len(tok.encode(system,add_special_tokens=False)),'prepared_world_id':after['id']})
        atomic(store.parent/'STATE.json',{'turn':0,'paused':True,'last_record_sha256':None,'source_main_entry':1630,'label':'detached branch turns, not mainentries'})
        cases[name]={'job':job,'messages':copy.deepcopy(messages),'rows':[],'paused_reason':None}
        prepared.append({'arm':name,'world_id':after['id'],'input_tokens':len(tokens),'world_verification':c.verify_store(store)})
    assert len({p['world_id'] for p in prepared})==1
    save(Path('pilot/PREPARATION_CHECKS.json'),{'status':'pass','same_prepared_world':True,'conditions':prepared,'model_calls':0})
    unchanged();torch.set_num_threads(2)
    model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval();expected=c.read(c.C/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected
    guard=Guard(5153960755,H/'pilot/RESOURCE.jsonl');rows=[]
    for turn in range(1,4):
      for name,case in cases.items():
        if case['paused_reason']:continue
        unchanged();messages=case['messages'];tokens=tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        if len(tokens)>7936:
            case['paused_reason']='context_capacity';save(Path('pilot/capacity')/(name+f'_t{turn}.json'),{'input_tokens':len(tokens),'limit':7936,'generation':False,'no_trimming':True});continue
        if (H/'pilot/PAUSE_REQUEST').exists():case['paused_reason']='user_pause';continue
        store=Path(case['job']['world_store']);base=store.parent;branchstate=c.read(base/'STATE.json');assert branchstate['turn']==turn-1
        label=name+f'_t{turn}';save(Path('pilot/plans')/(label+'.json'),{'arm':name,'turn':turn,'messages':copy.deepcopy(messages),'input_token_ids':tokens,'before_world_state':c.read(store/'STATE.json'),'parent_record_sha256':branchstate['last_record_sha256']})
        save(Path('pilot/PENDING.json'),{'arm':name,'turn':turn,'stage':'generation/effects unresolved; no automatic replay'})
        raw=generate(model,tok,messages,case['job'],guard,label);save(Path('pilot/raw')/(label+'.json'),raw)
        w=c.GardenWorld.open(store)
        try:
            before=w.checkpoint();batch=w.receive_notebook(raw['text']);save(Path('pilot/batches')/(label+'.json'),batch);after=w.checkpoint()
        finally:w.close()
        feedback=c.candidate.project_feedback(batch)
        actions=[x for x in batch['operations'] if x['channel'] in ['python','shell']]
        row={'arm':name,'turn':turn,'label':label,'before_id':before['id'],'after_id':after['id'],'input_tokens':len(tokens),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],'text':raw['text'],'feedback':feedback,'raw_sha256':c.sha(H/'pilot/raw'/(label+'.json')),'batch_sha256':c.sha(H/'pilot/batches'/(label+'.json')),'parent_record_sha256':branchstate['last_record_sha256'],'complete_cells':batch['parsed']['complete_executable_cells'],'incomplete_fences':sum(not x['complete'] for x in batch['parsed']['cells']),'model_initiated_actions':[{'channel':x['channel'],'source':x['source'],'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in actions],'automatic_note_operations':[{'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations'] if x['channel']=='note'],'boundary':batch['boundary'],'world_verification':c.verify_store(store)}
        path=Path('pilot/records')/(label+'.json');save(path,row)
        atomic(base/'STATE.json',{'turn':turn,'paused':True,'last_record_sha256':c.sha(H/path),'source_main_entry':1630,'label':'detached branch turns, not mainentries'})
        (H/'pilot/PENDING.json').unlink();case['rows'].append(row);rows.append(row)
        case['messages'] += [{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        assert parameter_digest(model,False)==expected;unchanged()
        print(json.dumps({k:row[k] for k in ['arm','turn','input_tokens','output_tokens','complete_cells','incomplete_fences','stop']}),flush=True)
    save(Path('pilot/RESULTS.json'),{'actual_model_calls':len(rows),'planned_model_calls':9,'rows':rows,'paused_reasons':{n:x['paused_reason'] for n,x in cases.items()},'main_entry':1630,'main_unchanged':True,'weights_unchanged':True,'training_updates':0,'activation':False,'pending':False})
    unchanged()

if __name__=='__main__':main()
