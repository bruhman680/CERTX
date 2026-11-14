"""Read retained observation results without model calls or world writes."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parents[1]
D=H/'observation'

def read(p):return json.loads(p.read_text())
def main():
    out=D/'READOUT.json';assert not out.exists(),'Preserve earlier readout'
    jobs=read(D/'jobs.json');rows=[]
    for job in jobs:
        case=job['case_id'];folder=H/'results'/case
        plan=read(folder/'plan1.json');raw=read(folder/'raw1.json');result=read(folder/'result1.json');batch=read(folder/'batch1.json')
        assert plan['messages']==job['messages']
        assert result['input_tokens']==len(raw['input_token_ids'])
        textsha=hashlib.sha256(raw['text'].encode()).hexdigest()
        assert textsha==result['text_sha256']
        assert result['complete_cells']==batch['parsed']['complete_executable_cells']
        assert result['feedback']=='' and result['world_verification']['status']=='pass'
        assert len(result['operations'])==1 and result['operations'][0]['channel']=='note'
        assert result['operations'][0]['changed_paths']==['notebook.txt']
        rows.append({'case_id':case,'measured_facts':job['metadata']['measured_facts'],
             'supplied_facts':job['metadata']['facts'],'input_tokens':result['input_tokens'],
             'input_sha256':result['input_sha256'],'output_tokens':result['output_tokens'],
             'text_sha256':textsha,'stop':result['stop'],'complete_cells':result['complete_cells'],
             'incomplete_fences':result['incomplete_fences'],'note_stored':batch['note_stored'],
             'code_operations':0,'world_verification':result['world_verification']})
    assert len({r['input_sha256'] for r in rows})==3
    assert len({r['text_sha256'] for r in rows})==1
    obj={'status':'pass','scope':'read-only retained-results consistency check',
         'rows':rows,'distinct_input_token_hashes':3,'distinct_output_text_hashes':1,
         'new_model_calls':0,'world_operations':0,
         'interpretation':'Three explicitly different inputs mapped to the same capped unfinished reply; no complete cell or new executed action.',
         'limits':'Selected one-step contexts; no task objective, internal perception measure, general sensitivity proof or treatment replication.'}
    out.write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='rows'}))

if __name__=='__main__':main()
