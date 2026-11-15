"""Detached context controls. Prior artifacts are immutable inputs."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items(): os.environ[k]=v
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parent
OLD=H.parent/'observability-three-contact-v1'
sys.path.insert(0,str(OLD))
import common as c
from worker import generate
from runtime_reference import parameter_digest,Guard
import torch
from transformers import AutoModelForCausalLM

def save(p,x): c.save(H/p,x)
def ids(m): return tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True)
def fresh(m): return copy.deepcopy(m[:2])+[{'role':'assistant','content':''},copy.deepcopy(m[-1])]

def job(name,source,messages,turns=1,read=None):
    if (H/'jobs'/(name+'.json')).exists():return c.read(H/'jobs'/(name+'.json'))
    source_store=Path(source['world_store'])
    bundle=source_store/'bundles/000002.json'
    assert c.read(bundle)['id']==source['metadata']['prepared_world_id']
    store=H/'worlds'/name
    w=c.GardenWorld.create(store,bundle,source_store/'objects',parent_entry=1580)
    try:
        declaration='\n\n## History-control diagnostic transport\nThis detached copy may receive inherited, fresh, or deliberately substituted role histories and an explicit operator task, with at most one actual reply/receipt followup. Histories are controlled inputs, not a live memory policy. The physical execution laws remain unchanged.\n'
        code="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(declaration)+",encoding='utf-8')"
        event=w.apply('python',code)
        assert event['feedback']['exit_code']==0 and event['changed_paths']==['WORLD_RULES.txt']
        save(Path('preparation')/(name+'_declaration.json'),{'actor':'operator','source':code,'event':event})
        if read:
            code="from pathlib import Path\n"+('print(Path(\'probe_value.json\').read_text())' if read=='document' else "import json\nprint(json.loads(Path('probe_value.json').read_text())['value'])")
            event=w.apply('python',code)
            assert event['feedback']['exit_code']==0 and not event['changed_paths']
            save(Path('preparation')/(name+'_read.json'),{'actor':'operator','source':code,'event':event})
            task=json.loads(messages[-1]['content'])
            task['operator_read_receipt']={'actor':'operator','channel':'python',**{k:event['feedback'][k] for k in ('stdout','stderr','exit_code','boundary')}}
            messages[-1]['content']=json.dumps(task,ensure_ascii=False,sort_keys=True)
        snapshot=w.checkpoint()
    finally:w.close()
    j={'case_id':name,'messages':messages,'max_turns':turns,'decoder':'greedy','seed':None,'world_store':str(store),'expected_value':source['metadata']['expected_value'],'prepared_world_id':snapshot['id']}
    save(Path('jobs')/(name+'.json'),j)
    return j

def run(j):
    messages=copy.deepcopy(j['messages'])
    for turn in range(1,j['max_turns']+1):
        name=j['case_id']+f'_t{turn}'
        if (H/'results'/(name+'_result.json')).exists():
            row=c.read(H/'results'/(name+'_result.json'));rows.append(row)
            raw=c.read(H/'results'/(name+'_raw.json'));batch=c.read(H/'results'/(name+'_batch.json'))
            messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':c.candidate.project_feedback(batch)}]
            continue
        pending=H/'PENDING.json';assert not pending.exists()
        pending.write_text(json.dumps({'case':name,'stage':'generation and effects unresolved'}))
        raw=generate(model,tok,messages,j,guard,name)
        save(Path('results')/(name+'_raw.json'),raw)
        w=c.GardenWorld.open(Path(j['world_store']))
        try:
            before=w.checkpoint();batch=w.receive_notebook(raw['text']);after=w.checkpoint()
        finally:w.close()
        save(Path('results')/(name+'_batch.json'),batch)
        feedback=c.candidate.project_feedback(batch)
        stdouts=[(op['feedback'] or {}).get('stdout','') for op in batch['operations']]
        row={'case':name,'input_tokens':len(raw['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'text_sha256':hashlib.sha256(raw['text'].encode()).hexdigest(),'complete_cells':batch['parsed']['complete_executable_cells'],'expected_value':j['expected_value'],'target_in_text':j['expected_value'] in raw['text'],'target_in_stdout':any(j['expected_value'] in s for s in stdouts),'exact_value_stdout':any(s.strip()==j['expected_value'] for s in stdouts),'stdout':stdouts,'before_id':before['id'],'after_id':after['id'],'verification':c.verify_store(Path(j['world_store']))}
        save(Path('results')/(name+'_result.json'),row);rows.append(row)
        messages += [{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        assert c.inventory()==canonical
        assert parameter_digest(model,False)==digest
        pending.unlink()
        print(json.dumps(row),flush=True)

if __name__=='__main__':
    assert not (H/'RESULTS.json').exists(),'Completed study; no replay'
    canonical=c.read(H/'CANONICAL_BEFORE.json') if (H/'CANONICAL_BEFORE.json').exists() else c.inventory()
    if not (H/'CANONICAL_BEFORE.json').exists():save(Path('CANONICAL_BEFORE.json'),canonical)
    assert canonical==c.inventory()
    tok=c.tokenizer();sources=c.read(OLD/'retrieval/jobs.json')[:2]
    if not (H/'PLAN.json').exists():save(Path('PLAN.json'),{'date':'2026-11-14 America/Chicago','main_entry':1580,'main_changes':False,'cycle1':'two hidden nonce files crossed with inherited versus fresh framing; two replies each. Fresh = original initial two messages, empty assistant, same JSON operator task. Physical fixture preserved except same diagnostic declaration in all cases.','cycle2':'If cycle1 first replies differ by framing, two assistant-only filler styles crossed with nonce files, inherited topology and exactly matched token count, one reply each. Otherwise plain task vs JSON under fresh framing, two nonces, one reply each.','cycle3':'fresh framing with authentic operator full-document vs parsed-value read receipts for nonce A, one reply each; hidden reference from cycle1. Different information and length are explicit confounds.','maximum_model_replies':14,'model':'cached SmolLM2-135M-Instruct float32 CPU eager greedy 256 fresh KV','inference_changes':False,'claims':'context dependence only; no mechanism isolated, generalization or learning claimed','preservation':'new detached worlds and raw artifacts only; no adoption','readout':'complete cells, actual receipts, exact stdout and lexical target presence separately. No tracing installed; code inspection is not proof of every access.'})
    jobs=[]
    for s in sources:
        suffix=s['case_id'][-1]
        jobs += [job('inherited_'+suffix,s,copy.deepcopy(s['messages']),2),job('fresh_'+suffix,s,fresh(s['messages']),2)]
    torch.set_num_threads(2)
    model=AutoModelForCausalLM.from_pretrained(c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    digest=c.read(c.C/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==digest
    guard=Guard(5153960755,H/'RESOURCE.jsonl');rows=[]
    for j in jobs:run(j)
    differing=rows[0]['text_sha256']!=rows[2]['text_sha256']
    save(Path('CYCLE2_DECISION.json'),{'first_reply_context_difference':differing,'selected':'matched fillers' if differing else 'plain task format'})
    for style,word in [('stone',' stone'),('river',' river')]:
        for s in sources:
            m=copy.deepcopy(s['messages'])
            if differing:
                for message in m[2:-1]:
                    if message['role']=='assistant':message['content']=''
                target=len(ids(s['messages']));slot=m[2]
                # Single-token repeated words make exact total matching explicit and deterministic.
                n=target-len(ids(m));slot['content']=word*n
                assert len(ids(m))==target, (style,len(ids(m)),target)
            else:
                m=fresh(m)
                if style=='stone':m[-1]['content']=json.loads(m[-1]['content'])['operator_task']
            run(job('control_'+style+'_'+s['case_id'][-1],s,m))
    for kind in ['document','value']:
        run(job('provided_'+kind,sources[0],fresh(sources[0]['messages']),read=kind))
    save(Path('RESULTS.json'),{'rows':rows,'actual_model_replies':len(rows),'canonical_unchanged':c.inventory()==canonical,'weights_unchanged':parameter_digest(model,False)==digest,'pending':False,'activation':False})
