"""Read-only check of matched fixture states and decoded nonce file bytes."""
from pathlib import Path
import sys,json,base64,hashlib
H=Path(__file__).resolve().parents[1];sys.path.insert(0,str(H))
import common
R=H/'retrieval'
def main():
    jobs=common.read(R/'jobs.json');states={};values={}
    for job in jobs:
        store=Path(job['world_store']);state=common.read(store/'STATE.json')
        bundle=common.read(store/'bundles'/state['bundle'])
        states[job['case_id']]={e[0]:e for e in bundle['entries']}
        entry=states[job['case_id']]['probe_value.json']
        obj=common.read(store/'objects'/(entry[3]+'.json'))
        data=base64.b64decode(obj['base64'],validate=True)
        assert hashlib.sha256(data).hexdigest()==entry[3]
        value=json.loads(data)['value'];assert value==job['metadata']['expected_value']
        values[job['case_id']]=value
    a,b,p=(states[k] for k in ('retrieval_hidden_a','retrieval_hidden_b','retrieval_provided_a'))
    assert set(a)==set(b)==set(p)
    differences=[k for k in a if a[k]!=b[k]]
    assert differences==['probe_value.json']
    assert a==p
    common.save(R/'FIXTURE_PAIR_AUDIT.json',{'status':'pass','hidden_world_differences':differences,
       'hidden_a_and_provided_a_supported_files_identical':True,'decoded_values':values,
       'model_calls':0,'world_writes':False,'scope':'pre-inference fixture state; not future worker outcomes'})
    print(json.dumps({'status':'pass','hidden_differences':differences,'provided_matches_a':True}))
if __name__=='__main__':main()
