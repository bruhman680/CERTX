"""Actual-feedback versus explicit coached repair, then paired artifact checks."""
from pathlib import Path
import sys,json,copy
H=Path(__file__).resolve().parent;E=H.parent
sys.path.insert(0,str(E/'history-retrieval-three-cycle-v1'))
import run as r
r.H=H
import torch
from transformers import AutoModelForCausalLM
from runtime_reference import parameter_digest,Guard
PRIOR=E/'retrieval-task-transfer-v1'
CASES={
 'original_signal_merged':'The requested file is probe_value.json and its key is signal. The previous attempt selected a different path. Return one complete Python cell that reads the requested file and prints only its field value.',
 'renamed_value_merged':'json.load expects an open file object, while json.loads expects JSON text. The requested file is sample_record.json and its key is value. Return one complete Python cell that reads that file and prints only its field value.',
 'renamed_signal_merged':'The previous code fence was incomplete, so no code ran. The requested file is sample_record.json and its key is signal. Return one complete short Python cell that reads that file and prints only its field value.'}

def clone(name,source_store):
    state=r.c.read(source_store/'STATE.json')
    store=H/'worlds'/name
    w=r.c.GardenWorld.create(store,source_store/'bundles'/state['bundle'],source_store/'objects',parent_entry=1580)
    try:
        declaration='\n\n## Detached repair diagnostic transport\nThis branch inherits a completed prior diagnostic attempt. It may receive that actual attempt and receipt, with or without an explicitly labeled operator correction, then one new reply. Paired artifact checks execute saved text without a new model call. This is a controlled diagnostic, not the selected main memory or behavioral policy. Physical execution laws remain unchanged.\n'
        code="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(declaration)+",encoding='utf-8')"
        event=w.apply('python',code);assert event['feedback']['exit_code']==0 and event['changed_paths']==['WORLD_RULES.txt']
        snapshot=w.checkpoint()
    finally:w.close()
    r.save(Path('preparation')/(name+'.json'),{'actor':'operator','source':code,'event':event,'source_store':str(source_store),'source_bundle':state['bundle'],'prepared_world_id':snapshot['id']})
    return store,snapshot

def main():
    assert not (H/'PLAN.json').exists(),'No automatic replay'
    r.canonical=r.c.inventory();r.save(Path('CANONICAL_BEFORE.json'),r.canonical)
    r.tok=r.c.tokenizer()
    r.save(Path('PLAN.json'),{'date':'2026-11-15 UTC','cycles':['actual receipt only,3replies','same post-failure state and input plus explicitly labeled operator correction,3replies','all6unchanged new notebook artifacts executed on pairedB post-failure worlds,0modelcalls'],'corrections_predeclared':CASES,'same_body':'cached pinned135M float32CPU eager2threads greedy256 freshKV','source_states':'completed prior failures, not pre-model fixtures; no unknown actions replayed','readout':['exact actual stdout','correct nonce in actual stdout','code completion','process receipt','changed paths'],'claims':'feedback-conditioned repair, not training or autonomous discovery; hints introduce instruction/information/length changes','main_changes':False,'activation':False,'model_replies':6,'extra_artifact_executions':6})
    jobs=[]
    for condition in ['feedback','coached']:
      for case,hint in CASES.items():
        source=r.c.read(PRIOR/'jobs'/(case+'.json'))
        raw=r.c.read(PRIOR/'results'/(case+'_t1_raw.json'))
        batch=r.c.read(PRIOR/'results'/(case+'_t1_batch.json'))
        actual=r.c.candidate.project_feedback(batch)
        feedback=actual
        if condition=='coached':
            obj=json.loads(actual) if actual else {}
            obj['operator_correction']={'actor':'operator','text':hint}
            feedback=json.dumps(obj,ensure_ascii=False,sort_keys=True)
        messages=copy.deepcopy(source['messages'])+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        name=condition+'_'+case
        a,sa=clone(name+'_a',Path(source['world_store']))
        b,sb=clone(name+'_b',Path(source['pair']['b']['store']))
        j={'case_id':name,'messages':messages,'max_turns':1,'decoder':'greedy','seed':None,'world_store':str(a),'expected_value':'N4C8P2','prepared_world_id':sa['id'],'artifact_store':str(b),'artifact_prepared_id':sb['id'],'source_case':case,'condition':condition,'actual_feedback':actual,'operator_correction':hint if condition=='coached' else None}
        r.save(Path('jobs')/(name+'.json'),j);jobs.append(j)
    torch.set_num_threads(2)
    r.model=AutoModelForCausalLM.from_pretrained(r.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    r.model.requires_grad_(False);r.model.eval();r.digest=r.c.read(r.c.C/'run/MANIFEST.json')['tensor_digest']
    assert parameter_digest(r.model,False)==r.digest
    r.guard=Guard(5153960755,H/'RESOURCE.jsonl');r.rows=[]
    for j in jobs:r.run(j)
    artifacts=[]
    for j in jobs:
        name=j['case_id'];raw=r.c.read(H/'results'/(name+'_t1_raw.json'))
        r.save(Path('ARTIFACT_PENDING.json'),{'case':name,'stage':'known saved notebook counterfactual execution unresolved'})
        w=r.c.GardenWorld.open(Path(j['artifact_store']))
        try:batch=w.receive_notebook(raw['text']);snapshot=w.checkpoint()
        finally:w.close()
        r.save(Path('artifacts')/(name+'_batch.json'),batch)
        stdout=[x['feedback']['stdout'] for x in batch['operations'] if x['feedback'] is not None]
        row={'case':name,'expected_value':'H9D3L7','stdout':stdout,'target_in_stdout':any('H9D3L7' in s for s in stdout),'exact_value_stdout':any(s.strip()=='H9D3L7' for s in stdout),'world_id':snapshot['id'],'verification':r.c.verify_store(Path(j['artifact_store']))}
        artifacts.append(row);r.save(Path('artifacts')/(name+'_result.json'),row);(H/'ARTIFACT_PENDING.json').unlink()
    assert r.c.inventory()==r.canonical and parameter_digest(r.model,False)==r.digest
    r.save(Path('RESULTS.json'),{'model_rows':r.rows,'artifact_rows':artifacts,'model_replies':6,'extra_artifact_executions':6,'main_unchanged':True,'weights_unchanged':True,'training_updates':0,'activation':False})

if __name__=='__main__':main()
