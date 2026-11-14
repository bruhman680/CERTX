"""Operator-stage readable transcript on a detached snapshot, then reopen/read."""
from pathlib import Path
import json,hashlib,sys
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1'
sys.path.insert(0,str(C/'world'))
from garden_world import GardenWorld,verify_store
def save(name,obj):
    p=H/name;assert not p.exists(),f'Preserve existing {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def inv():
    return {str(p.relative_to(C)):hashlib.sha256(p.read_bytes()).hexdigest() for p in C.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    before=inv();archive=json.loads((H/'SOURCE_ARCHIVE.json').read_text())
    state=json.loads((C/'run/world/STATE.json').read_text());bundle=C/'run/world/bundles'/state['bundle']
    parent=json.loads(bundle.read_text());assert not any(x[0]=='conversation_archive_v1' or x[0].startswith('conversation_archive_v1/') for x in parent['entries'])
    entries=archive['exchanges'];payload={'initial_messages':archive['initial_messages'],'entries':entries}
    save('ARCHIVE_PLAN.json',{'date':'2026-11-13 America/Chicago','actor':'operator diagnostic',
      'parent_bundle':str(bundle),'parent_bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),
      'scope':'exact current source condition initial messages +30 actual assistant/receipt pairs, not all pre1550 history',
      'path':'/world/conversation_archive_v1','model_calls':0,'canonical_changes':False,
      'deployment':False,'purpose':'demonstrate supported file readability/persistence, not model retrieval competence',
      'permissions':'ordinary model-writable files; observer originals remain outside world',
      'capacity':'existing world and per-file quotas apply; no indefinite storage claim'})
    source="from pathlib import Path\nimport json\npayload=json.loads("+repr(json.dumps(payload,ensure_ascii=False))+ ")\np=Path('conversation_archive_v1')\np.mkdir()\n(p/'entries').mkdir()\n(p/'initial_messages.json').write_text(json.dumps(payload['initial_messages'],ensure_ascii=False),encoding='utf-8')\nindex=[]\nfor x in payload['entries']:\n    name='entries/'+str(x['entry']).zfill(6)+'.json'\n    (p/name).write_text(json.dumps(x,ensure_ascii=False),encoding='utf-8')\n    index.append({'entry':x['entry'],'path':name})\n(p/'index.json').write_text(json.dumps({'scope':'source notebook condition1551-1580','entries':index}),encoding='utf-8')\nprint(len(index))\n"
    save('ARCHIVE_INITIALIZATION_SOURCE.json',{'actor':'operator','source':source})
    world=GardenWorld.create(H/'archive_sandbox',bundle,C/'run/world/objects',parent_entry=1580)
    try:
        event=world.apply('python',source);save('ARCHIVE_INITIALIZATION.json',event)
        assert event['feedback']['exit_code']==0 and event['feedback']['boundary'] is None
        after=world.checkpoint();old={x[0]:x for x in parent['entries']};new={x[0]:x for x in after['entries']}
        assert all(new[k]==v for k,v in old.items())
        newpaths=sorted(set(new)-set(old));assert newpaths and all(p=='conversation_archive_v1' or p.startswith('conversation_archive_v1/') for p in newpaths)
    finally:world.close()
    expected_digest=hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    read_source="from pathlib import Path\nimport json,hashlib\np=Path('conversation_archive_v1')\ni=json.loads((p/'index.json').read_text())\na={'initial_messages':json.loads((p/'initial_messages.json').read_text()),'entries':[json.loads((p/x['path']).read_text()) for x in i['entries']]}\nprint(hashlib.sha256(json.dumps(a,sort_keys=True,ensure_ascii=False).encode()).hexdigest())\n"
    save('ARCHIVE_READ_SOURCE.json',{'actor':'operator diagnostic','source':read_source})
    world=GardenWorld.open(H/'archive_sandbox')
    try:
        event=world.apply('python',read_source);save('ARCHIVE_READ_AFTER_REOPEN.json',event)
        assert event['feedback']['exit_code']==0 and event['feedback']['stdout'].strip()==expected_digest
        assert event['changed_paths']==[]
    finally:world.close()
    assert before==inv()
    save('ARCHIVE_RESULTS.json',{'status':'pass','entries':len(entries),'scope_entries':[entries[0]['entry'],entries[-1]['entry']],
      'exact_source_digest':expected_digest,'readable_after_reopen':True,'all_original_world_paths_unchanged':True,
      'new_archive_paths':newpaths,'canonical_unchanged':True,'model_calls':0,'model_retrieval_observed':False,
      'sandbox_verification':verify_store(H/'archive_sandbox'),'live_policy_adopted':False})
if __name__=='__main__':main()
