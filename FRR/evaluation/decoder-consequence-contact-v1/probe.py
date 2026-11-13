"""Post-sampling consequence test on independent exact world copies."""
from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parent
C=H.parent/'minimal-garden-candidate-v1'
D=H.parent/'decoder-context-contact-v1'
sys.path[:0]=[str(C/'world')]
from garden_world import GardenWorld,parse_notebook,verify_store
def write(name,x):
    (H/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def inv(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    assert not (H/'RESULTS.json').exists()
    r=json.loads((D/'RESULTS.json').read_text())
    selected=[a for a in r['rows'] if a['assessment']['complete_executable_cells']>0]
    state=json.loads((C/'run/world/STATE.json').read_text())
    bundles={'retained_01':C/'run/world/bundles/000001.json',
             'prospective_13':C/'run/world/bundles'/state['bundle']}
    plan={'date':'2026-11-13 America/Chicago','selection':'every sampled reply with at least one complete executable cell, chosen by syntax not outcome',
       'cases':[(a['context'],a['seed']) for a in selected],
       'parents':{k:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in bundles.items()},
       'condition':'each reply executes unchanged once on a fresh matching snapshot; real sandbox and ordinary errors; no subsequent LLM call',
       'scope':'post-hoc consequence diagnostic; not live continuation or policy adoption'}
    write('PLAN.json',plan)
    before=inv(C/'run');rows=[]
    for a in selected:
        label=f"{a['context']}_{a['seed']}"
        raw=json.loads((D/'raw'/f'{label}.json').read_text())
        assert parse_notebook(raw['text'])['complete_executable_cells']==a['assessment']['complete_executable_cells']
        store=H/'worlds'/label
        store.parent.mkdir(exist_ok=True)
        w=GardenWorld.create(store,bundles[a['context']],C/'run/world/objects',parent_entry=1550 if a['context']=='retained_01' else 1562)
        try:
            batch=w.receive_notebook(raw['text'])
            write(label+'_BATCH.json',batch)
            ops=[{'channel':o['channel'],'changed_paths':o['changed_paths'],'feedback':o['feedback']} for o in batch['operations']]
            rows.append({'case':label,'batch_status':batch['status'],'boundary':batch['boundary'],
                         'note_stored':batch['note_stored'],'operations':ops})
        finally:w.close()
        rows[-1]['store_verification']=verify_store(store)
    assert before==inv(C/'run')
    write('RESULTS.json',{'plan':plan,'cases':rows,'canonical_run_unchanged':True,'followup_model_calls':0})
if __name__=='__main__':main()
