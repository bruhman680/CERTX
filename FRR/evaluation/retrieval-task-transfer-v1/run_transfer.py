"""Prospective name/key/layout task family. Cached local inference only."""
from pathlib import Path
import sys,json,copy,hashlib
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parent/'history-retrieval-three-cycle-v1'))
import run as r
r.H=H
import torch
from transformers import AutoModelForCausalLM
from runtime_reference import parameter_digest,Guard

VALUES={'a':'N4C8P2','b':'H9D3L7'}
SOURCE=r.c.read(r.OLD/'retrieval/jobs.json')[0]
SOURCE_STORE=Path(SOURCE['world_store'])

def prepare(case,filename,key,value):
    store=H/'worlds'/case
    w=r.c.GardenWorld.create(store,SOURCE_STORE/'bundles/000002.json',SOURCE_STORE/'objects',parent_entry=1580)
    try:
        addition='\n\n## Task-transfer diagnostic transport\nThis detached copy receives either a fresh role-shell or merged initial/task message. The explicit task concerns the file named in that message. One model reply is executed, with no corrective followup. Paired worlds test unchanged generated text against different file values. This diagnostic is not the selected live memory policy. Physical execution laws remain unchanged.\n'
        code="from pathlib import Path\nimport json\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(addition)+",encoding='utf-8')\n"
        if filename!='probe_value.json':code+="Path('probe_value.json').unlink()\n"
        code+="Path("+repr(filename)+").write_text(json.dumps({"+repr(key)+":"+repr(value)+"}),encoding='utf-8')\n"
        event=w.apply('python',code)
        assert event['feedback']['exit_code']==0 and event['feedback']['boundary'] is None
        snapshot=w.checkpoint()
    finally:w.close()
    r.save(Path('preparation')/(case+'.json'),{'actor':'operator','source':code,'event':event,'prepared_world_id':snapshot['id']})
    return store,snapshot

def main():
    assert not (H/'PLAN.json').exists(),'No replay into existing experiment'
    r.canonical=r.c.inventory();r.save(Path('CANONICAL_BEFORE.json'),r.canonical)
    r.tok=r.c.tokenizer();base=copy.deepcopy(SOURCE['messages'][:2]);jobs=[]
    arrays={}
    for file_tag,filename in [('original','probe_value.json'),('renamed','sample_record.json')]:
      for key in ['value','signal']:
       for layout in ['shell','merged']:
        name=file_tag+'_'+key+'_'+layout
        task=f'Use Python to read the {key} field in {filename} and print its exact value.'
        text=json.dumps({'operator_task':task},ensure_ascii=False,sort_keys=True)
        if layout=='shell':m=copy.deepcopy(base)+[{'role':'assistant','content':''},{'role':'user','content':text}]
        else:m=[copy.deepcopy(base[0]),{'role':'user','content':base[1]['content']+'\n\n'+text}]
        arrays[name]=m
    r.save(Path('PLAN.json'),{'date':'2026-11-15 UTC','scope':'prospective 2 filenames x2 fieldnames x2 layouts; one reply each; artifact-only paired nonce check','all_messages_predeclared':arrays,'nonce_values':VALUES,'expected_values_not_in_model_inputs':True,'model_replies':8,'extra_artifact_executions':8,'no_corrective_followup':True,'metrics':['complete executable cells','actual process status/receipts','requested value substring in actual stdout','bare exact-value stdout','generated artifact follows paired nonce change'],'limits':'tiny deterministic task family; layouts differ in length/topology; paired artifact execution is not an additional model sample','main_entry':1580,'main_changes':False,'stale_original_filename':'removed whenever renamed','model':'same cached pinned135M CPUfloat32 eager greedy256 freshKV','training_updates':0})
    for name,m in arrays.items():
        file_tag,key,layout=name.split('_');filename='probe_value.json' if file_tag=='original' else 'sample_record.json'
        pair={}
        for suffix,value in VALUES.items():
            store,snapshot=prepare(name+'_'+suffix,filename,key,value);pair[suffix]={'store':str(store),'id':snapshot['id']}
        j={'case_id':name,'messages':m,'max_turns':1,'decoder':'greedy','seed':None,'world_store':pair['a']['store'],'expected_value':VALUES['a'],'prepared_world_id':pair['a']['id'],'pair':pair,'filename':filename,'key':key,'layout':layout}
        assert all(value not in json.dumps(m) for value in VALUES.values())
        r.save(Path('jobs')/(name+'.json'),j);jobs.append(j)
    torch.set_num_threads(2)
    r.model=AutoModelForCausalLM.from_pretrained(r.c.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    r.model.requires_grad_(False);r.model.eval()
    r.digest=r.c.read(r.c.C/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(r.model,False)==r.digest
    r.guard=Guard(5153960755,H/'RESOURCE.jsonl');r.rows=[];transfers=[]
    for j in jobs:
        r.run(j)
        raw=r.c.read(H/'results'/(j['case_id']+'_t1_raw.json'))
        pending=H/'TRANSFER_PENDING.json';assert not pending.exists()
        r.save(Path('TRANSFER_PENDING.json'),{'case':j['case_id'],'action':'execute unchanged saved notebook text on paired B world'})
        w=r.c.GardenWorld.open(Path(j['pair']['b']['store']))
        try:batch=w.receive_notebook(raw['text']);snapshot=w.checkpoint()
        finally:w.close()
        r.save(Path('transfers')/(j['case_id']+'_batch.json'),batch)
        stdouts=[x['feedback']['stdout'] for x in batch['operations'] if x['feedback'] is not None]
        row={'case':j['case_id'],'expected_value':VALUES['b'],'stdout':stdouts,'target_in_stdout':any(VALUES['b'] in s for s in stdouts),'exact_value_stdout':any(s.strip()==VALUES['b'] for s in stdouts),'world_id':snapshot['id'],'verification':r.c.verify_store(Path(j['pair']['b']['store']))}
        transfers.append(row);r.save(Path('transfers')/(j['case_id']+'_result.json'),row);pending.unlink()
    assert r.c.inventory()==r.canonical and parameter_digest(r.model,False)==r.digest
    r.save(Path('RESULTS.json'),{'model_rows':r.rows,'artifact_rows':transfers,'model_replies':8,'extra_artifact_executions':8,'main_unchanged':True,'weights_unchanged':True,'training_updates':0,'activation':False})

if __name__=='__main__':main()
