"""External material facts at actual call boundaries; no model/world execution."""
from pathlib import Path
import json,base64,hashlib
H=Path(__file__).resolve().parent

def material(root,bundle):
    rows={r[0]:r for r in bundle['entries']};row=rows.get('field.bin')
    if row is None:return {'kind':'absent'}
    if row[1]=='hardlink':row=rows[row[2]]
    if row[1]!='file':return {'kind':row[1]}
    obj=json.loads((root/'objects'/(row[3]+'.json')).read_text());data=base64.b64decode(obj['base64'],validate=True)
    assert hashlib.sha256(data).hexdigest()==row[3] and len(data)==row[4]
    return {'kind':'regular','bytes':len(data),'nonzero_offsets_values':[[i,v] for i,v in enumerate(data) if v],'sha256':row[3]}

def main():
    rows=[]
    for name in ['ambiguous17','named17','ambiguous29','named29','named17_silent','named17_question','named29_silent','named29_question']:
        d=H/name;n=2 if (d/'FORK.json').exists() else 1;path=d/'world/replies'/f'reply_{n:06d}.json'
        if not path.exists():raise RuntimeError('actual call not yet committed: '+name)
        rr=json.loads(path.read_text());batch=rr['actor_batch'];tick=rr['physical_tick'];root=d/'world/world/engine'
        bundle=lambda step:json.loads((root/'bundles'/f'{step:06d}.json').read_text())
        rows.append({'branch':name,'new_call_turn':n,'before_reply':material(root,bundle(batch['start_step'])),'after_actor_cells_before_tick':material(root,bundle(batch['end_step'])),'after_physical_tick':material(root,bundle(tick['step']))})
    (H/'GROUND_TRUTH.json').write_text(json.dumps({'observer_only':True,'model_calls':0,'actual_call_material_boundaries':rows},indent=2)+'\n');print(json.dumps({'material_boundaries_checked':len(rows),'model_calls':0}))
if __name__=='__main__':main()
